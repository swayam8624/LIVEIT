import type { LifeStage } from '@living/simulation-core';
import type { Appearance } from '@living/world-schema';

export type LifeArcLine = 'woman' | 'man';
export type LifeArcFrame = { row: number; direction: number; phase: number };

/** The reviewed family art only fits this narrow saved-appearance palette. */
export function playerLifeArcLine(
  appearance: Appearance | undefined,
): LifeArcLine | undefined {
  if (!appearance) return undefined;
  const shared =
    ['cocoa', 'mahogany', 'umber', 'espresso'].includes(appearance.skinTone) &&
    ['coils', 'afro'].includes(appearance.hair) &&
    ['midnight', 'black', 'espresso'].includes(appearance.hairColor) &&
    ['navy', 'teal'].includes(appearance.outfitColor) &&
    appearance.headwear === 'none' &&
    appearance.accessory === 'none';
  if (!shared) return undefined;
  if (appearance.facialHair && appearance.facialHair !== 'none') return 'man';
  if (appearance.makeup && appearance.makeup !== 'none') return undefined;
  return 'woman';
}

/** Returns the movement-atlas row and authored direction/phase cell. */
export function playerLifeArcFrame(
  stage: LifeStage,
  line: LifeArcLine,
  direction: 'down' | 'left' | 'right' | 'up',
  phase: number,
): LifeArcFrame {
  const earlyRows: Partial<Record<LifeStage, number>> = {
    infant: 0,
    toddler: 1,
    child: 2,
    teen: 3,
  };
  const row =
    earlyRows[stage] ??
    (stage === 'senior'
      ? line === 'woman'
        ? 6
        : 9
      : line === 'woman'
        ? 4
        : 7);
  const directions = { down: 0, left: 1, right: 2, up: 3 } as const;
  return {
    row,
    direction: directions[direction],
    phase: ((phase % 4) + 4) % 4,
  };
}

export function ameliaLifeArcFrame(
  stage: LifeStage,
  direction: 'down' | 'left' | 'right' | 'up',
  phase: number,
): LifeArcFrame | undefined {
  if (stage !== 'adult' && stage !== 'senior') return undefined;
  return {
    row: (stage === 'senior' ? 2 : 0) * 4,
    direction: { down: 0, left: 1, right: 2, up: 3 }[direction],
    phase: ((phase % 6) + 6) % 6,
  };
}
