import type { District } from '@living/world-schema';

/**
 * Stable, renderer-neutral 3D city blocks (metres). Rendering must never
 * change simulation state; district travel remains an explicit world action.
 * Identical seed, dimensions and district IDs yield identical buildings on
 * Vulkan/Metal or the lightweight offline map.
 */
export type CityBlock = Readonly<{
  id: string;
  district: District;
  x: number;
  z: number;
  height: number;
  width: number;
  depth: number;
  roof: 'flat' | 'gable' | 'green';
  palette: number;
}>;
export type CityScene = Readonly<{
  seed: number;
  blocks: readonly CityBlock[];
  streets: readonly number[];
  worldRadius: number;
}>;
const DISTRICT_ORDER: readonly District[] = [
  'riverside',
  'university',
  'market',
  'studio',
  'gardens',
];
const GRID = 9;
const SPACING = 9;

/** Small deterministic PRNG; do not use Math.random() for reconstructable worlds. */
function randomStep(state: number): number {
  let x = state >>> 0;
  x ^= x << 13;
  x ^= x >>> 17;
  x ^= x << 5;
  return x >>> 0;
}

/** Nine blocks across, with central arterial roads and five landmarks. */
export function generateCityScene(seed = 0xb311): CityScene {
  if (!Number.isSafeInteger(seed) || seed < 0 || seed > 0xffffffff) {
    throw new RangeError('City seed must be an unsigned 32-bit integer');
  }
  const blocks: CityBlock[] = [];
  let state = (seed || 1) >>> 0;
  for (let row = 0; row < GRID; row++) {
    for (let col = 0; col < GRID; col++) {
      // Grid lanes are completely free of buildings; parks remain open.
      if (row === 4 || col === 4) continue;
      const centerX = (col - 4) * SPACING;
      const centerZ = (row - 4) * SPACING;
      const sector = (col < 4 ? 0 : 1) + (row < 4 ? 0 : 2);
      const district = DISTRICT_ORDER[
        sector === 0 ? 1 : sector === 1 ? 2 : sector === 2 ? 0 : 3
      ]!;
      state = randomStep(state);
      // Gardens contains fewer, shorter buildings and more vegetation.
      const garden = row >= 6 && col >= 6;
      if (garden && (state & 3) === 0) continue;
      const height = garden ? 3 + (state % 6) : 5 + (state % 19);
      const roof = garden ? 'green' : (state & 1) ? 'gable' : 'flat';
      blocks.push({
        id: `block-${row}-${col}`,
        district: garden ? 'gardens' : district,
        x: centerX,
        z: centerZ,
        width: 5 + ((state >>> 8) % 3),
        depth: 5 + ((state >>> 12) % 3),
        height,
        roof,
        palette: (state >>> 16) % 5,
      });
    }
  }
  return { seed, blocks, streets: [0], worldRadius: GRID * SPACING * 0.5 };
}

/** Converts world-space city coordinates into an orthographic isometric map. */
export function projectCityBlock(
  block: Pick<CityBlock, 'x' | 'z' | 'height'>,
  width: number,
  height: number,
  zoom = 1,
): { left: number; top: number; scale: number } {
  if (!(width > 0 && height > 0 && zoom > 0)) {
    throw new RangeError('Map dimensions and zoom must be positive');
  }
  const tile = (Math.min(width, height) / 110) * zoom;
  return {
    left: width * 0.5 + (block.x - block.z) * tile * 0.83,
    top: height * 0.51 + (block.x + block.z) * tile * 0.38 - block.height * tile * 0.08,
    scale: Math.max(0.4, Math.min(1.1, 0.64 + (block.x + block.z) / 280)),
  };
}
