/**
 * Small, deterministic, top-down 2D game map. Visual assets can change without
 * changing collision, dialogue activation or the player's saved position.
 * Road/tile artwork is CC0 Pulse Everyday Streets, author and license recorded
 * in apps/player/src/pixelArt.ts. No 3D resources are involved.
 */
export type PixelPlace = 'street' | 'cafe';
export type Facing = 'up' | 'down' | 'left' | 'right';
export type PixelPosition = Readonly<{
  place: PixelPlace;
  x: number;
  y: number;
  facing: Facing;
}>;
export type PixelTerrain =
  'grass' | 'grass2' | 'walk' | 'road' | 'crosswalk' | 'floor' | 'carpet';
export type PixelProp =
  | 'tree'
  | 'bush'
  | 'bench'
  | 'lamp'
  | 'door'
  | 'window'
  | 'chair'
  | 'table'
  | 'plant'
  | 'shelf';
export type PixelCell = Readonly<{
  terrain: PixelTerrain;
  prop?: PixelProp;
  solid: boolean;
  portal?: PixelPlace;
}>;
export const STREET_WIDTH = 30;
export const STREET_HEIGHT = 23;
export const CAFE_WIDTH = 12;
export const CAFE_HEIGHT = 10;
export const INITIAL_POSITION: PixelPosition = {
  place: 'street',
  x: 11,
  y: 8,
  facing: 'down',
};
const directions: Record<Facing, readonly [number, number]> = {
  up: [0, -1],
  down: [0, 1],
  left: [-1, 0],
  right: [1, 0],
};
function inBounds(place: PixelPlace, x: number, y: number): boolean {
  return (
    Number.isSafeInteger(x) &&
    Number.isSafeInteger(y) &&
    x >= 0 &&
    y >= 0 &&
    x < (place === 'street' ? STREET_WIDTH : CAFE_WIDTH) &&
    y < (place === 'street' ? STREET_HEIGHT : CAFE_HEIGHT)
  );
}
export function pixelCell(place: PixelPlace, x: number, y: number): PixelCell {
  if (!inBounds(place, x, y)) return { terrain: 'grass', solid: true };
  if (place === 'cafe') {
    const border =
      x === 0 || x === CAFE_WIDTH - 1 || y === 0 || y === CAFE_HEIGHT - 1;
    if (x === 5 && y === 9)
      return { terrain: 'floor', prop: 'door', solid: false, portal: 'street' };
    if (border) return { terrain: 'carpet', prop: 'shelf', solid: true };
    if ((x === 3 && y === 3) || (x === 8 && y === 6))
      return { terrain: 'floor', prop: 'table', solid: true };
    if (
      (x === 2 && y === 3) ||
      (x === 4 && y === 3) ||
      (x === 7 && y === 6) ||
      (x === 9 && y === 6)
    ) {
      return { terrain: 'floor', prop: 'chair', solid: true };
    }
    if (x === 1 && y === 2)
      return { terrain: 'floor', prop: 'plant', solid: true };
    return { terrain: y < 2 ? 'carpet' : 'floor', solid: false };
  }
  // Market street: textured grass/sidewalk, a two-tile road, a tile-authored
  // café facade and several small landmarks. The map is fixed and testable.
  if ((x >= 13 && x <= 14) || (y >= 10 && y <= 11)) {
    const cross =
      (x >= 13 && x <= 14 && y >= 9 && y <= 12) ||
      (y >= 10 && y <= 11 && x >= 10 && x <= 16);
    return { terrain: cross ? 'crosswalk' : 'road', solid: false };
  }
  // The east side opens into a second neighborhood and a garden district.
  // All cells are deterministic so saved positions and collisions are stable.
  // Pixel props use the existing CC0 tileset and no external network assets.
  if (x >= 20 && x <= 27 && y >= 2 && y <= 8) {
    if (y === 8 && (x === 22 || x === 25)) {
      return { terrain: 'walk', prop: 'window', solid: true };
    }
    if (x === 24 && y === 8) {
      return { terrain: 'walk', prop: 'door', solid: true };
    }
    if (y === 2 || x === 20 || x === 27) {
      return { terrain: 'carpet', prop: 'shelf', solid: true };
    }
    return { terrain: 'carpet', solid: true };
  }
  if (x >= 3 && x <= 10 && y >= 15 && y <= 21) {
    if (y === 21 && (x === 5 || x === 8)) {
      return { terrain: 'walk', prop: 'window', solid: true };
    }
    if (y === 21 && x === 7) {
      return { terrain: 'walk', prop: 'door', solid: true };
    }
    return { terrain: 'carpet', solid: true };
  }
  if (x >= 17 && x <= 28 && y >= 14 && y <= 21) {
    if ((x === 18 || x === 27) && (y === 15 || y === 20))
      return { terrain: 'grass', prop: 'tree', solid: true };
    if ((x === 20 && y === 18) || (x === 25 && y === 17))
      return { terrain: 'grass2', prop: 'bench', solid: true };
    if ((x === 22 && y === 16) || (x === 26 && y === 19))
      return { terrain: 'grass', prop: 'bush', solid: true };
    if (y === 17 || x === 23) return { terrain: 'walk', solid: false };
    return { terrain: (x + y) % 4 === 0 ? 'grass2' : 'grass', solid: false };
  }
  if (
    (x === 22 && y === 9) ||
    (x === 27 && y === 13) ||
    (x === 2 && y === 17)
  ) {
    return { terrain: 'walk', prop: 'lamp', solid: true };
  }
  if (
    (x === 20 && y === 12) ||
    (x === 28 && y === 11) ||
    (x === 12 && y === 18)
  ) {
    return { terrain: 'walk', prop: 'plant', solid: true };
  }
  if (
    (x === 19 && y === 4) ||
    (x === 28 && y === 4) ||
    (x === 16 && y === 18)
  ) {
    return { terrain: 'grass', prop: 'tree', solid: true };
  }
  if (x >= 3 && x <= 8 && y >= 2 && y <= 6) {
    if (x === 5 && y === 6)
      return { terrain: 'walk', prop: 'door', solid: false, portal: 'cafe' };
    if (y === 6 && (x === 4 || x === 7))
      return { terrain: 'walk', prop: 'window', solid: true };
    return { terrain: 'carpet', solid: true };
  }
  if (
    (x === 1 && (y === 1 || y === 3)) ||
    (x === 16 && y === 2) ||
    (x === 17 && y === 7)
  ) {
    return { terrain: 'grass', prop: 'tree', solid: true };
  }
  if ((x === 1 && y === 6) || (x === 17 && y === 4)) {
    return { terrain: 'grass2', prop: 'bench', solid: true };
  }
  if ((x === 12 && y === 4) || (x === 16 && y === 9)) {
    return { terrain: 'walk', prop: 'lamp', solid: true };
  }
  if ((x === 2 && y === 8) || (x === 10 && y === 2)) {
    return { terrain: 'grass', prop: 'bush', solid: true };
  }
  return {
    terrain:
      x < 3 || y < 2 || x > 16
        ? (x + y) % 3 === 0
          ? 'grass2'
          : 'grass'
        : 'walk',
    solid: false,
  };
}
export function npcAt(
  place: PixelPlace,
): Readonly<{ x: number; y: number; name: string }> {
  return place === 'street'
    ? { x: 10, y: 7, name: 'Amelia' }
    : { x: 7, y: 4, name: 'Amelia' };
}
export function validPixelPosition(value: unknown): value is PixelPosition {
  if (!value || typeof value !== 'object') return false;
  const v = value as Partial<PixelPosition>;
  return (
    (v.place === 'street' || v.place === 'cafe') &&
    (v.facing === 'up' ||
      v.facing === 'down' ||
      v.facing === 'left' ||
      v.facing === 'right') &&
    inBounds(v.place, v.x as number, v.y as number) &&
    !pixelCell(v.place, v.x as number, v.y as number).solid &&
    !(npcAt(v.place).x === v.x && npcAt(v.place).y === v.y)
  );
}
export type StepResult = Readonly<{
  position: PixelPosition;
  event: 'moved' | 'blocked' | 'entered-cafe' | 'left-cafe' | 'npc-nearby';
}>;
export function movePixel(
  previous: PixelPosition,
  direction: Facing,
): StepResult {
  if (!validPixelPosition(previous)) {
    return { position: INITIAL_POSITION, event: 'blocked' };
  }
  const [dx, dy] = directions[direction];
  const next = {
    ...previous,
    facing: direction,
    x: previous.x + dx,
    y: previous.y + dy,
  };
  const aimed = pixelCell(previous.place, next.x, next.y);
  if (aimed.portal === 'cafe') {
    return {
      position: { place: 'cafe', x: 5, y: 8, facing: 'up' },
      event: 'entered-cafe',
    };
  }
  if (aimed.portal === 'street') {
    return {
      position: { place: 'street', x: 5, y: 7, facing: 'down' },
      event: 'left-cafe',
    };
  }
  const npc = npcAt(previous.place);
  if (npc.x === next.x && npc.y === next.y) {
    return {
      position: { ...previous, facing: direction },
      event: 'npc-nearby',
    };
  }
  if (aimed.solid) {
    return { position: { ...previous, facing: direction }, event: 'blocked' };
  }
  return { position: next, event: 'moved' };
}
export function isNpcAdjacent(p: PixelPosition): boolean {
  const npc = npcAt(p.place);
  return Math.abs(npc.x - p.x) + Math.abs(npc.y - p.y) === 1;
}
