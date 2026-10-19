import { pixelCell, npcAt, validPixelPosition, STREET_WIDTH, STREET_HEIGHT, type PixelCell, type PixelPlace, type PixelPosition } from './pixelTownLogic';

export const CHUNK_SIZE = 32;
/** Mathematical floor division works for negative infinite map coordinates. */
export function chunkOf(x: number, y: number): { cx: number; cy: number; lx: number; ly: number } {
  if (!Number.isSafeInteger(x) || !Number.isSafeInteger(y))
    throw Error('World coordinates must be integers');
  const cx = Math.floor(x / CHUNK_SIZE), cy = Math.floor(y / CHUNK_SIZE);
  return { cx, cy, lx: x - cx * CHUNK_SIZE, ly: y - cy * CHUNK_SIZE };
}
function mod(v: number, m: number): number { return ((v % m) + m) % m; }
/** Stable integer hash independent of visit order and chunk generation order. */
export function tileHash(seed: number, x: number, y: number): number {
  let n = ((x * 374761393) ^ (y * 668265263) ^ seed) | 0;
  n = Math.imul(n ^ (n >>> 13), 1274126177);
  return (n ^ (n >>> 16)) >>> 0;
}
export function seedFromTimeline(id: string): number {
  let h = 2166136261;
  for (let i = 0; i < id.length; i++) h = Math.imul(h ^ id.charCodeAt(i), 16777619);
  return h >>> 0;
}
export type WorldBiome = 'neighborhood' | 'market' | 'park' | 'arts' | 'country';
export function biomeAt(seed: number, x: number, y: number): WorldBiome {
  // Districts persist across 2x2 chunks for actual neighborhoods instead of
  // a random terrain type every single tile.
  const region = chunkOf(x,y);
  const n = tileHash(seed,Math.floor(region.cx/2),Math.floor(region.cy/2)) % 11;
  return n < 3 ? 'neighborhood' : n < 5 ? 'market' : n < 7 ? 'park'
    : n < 9 ? 'arts' : 'country';
}
/** Any integer coordinate is generated on demand. Starter town is preserved. */
export function worldCell(
  place: PixelPlace, x: number, y: number, seed: number,
): PixelCell {
  if (!Number.isSafeInteger(x) || !Number.isSafeInteger(y))
    return { terrain:'grass', solid:true };
  if (place === 'cafe' || (x >= 0 && y >= 0 && x < STREET_WIDTH && y < STREET_HEIGHT))
    return pixelCell(place, x, y);
  const biome = biomeAt(seed,x,y);
  const nx = mod(x,16), ny = mod(y,16);
  // Uninterrupted two-cell arteries at every 16th column and row.
  if ((nx === 7 || nx === 8) || (ny === 7 || ny === 8)) {
    return {
      terrain: (nx >= 7 && nx <= 8 && ny >= 7 && ny <= 8)
        ? 'crosswalk' : 'road', solid:false,
    };
  }
  const rand = tileHash(seed,x,y);
  if (nx === 6 || nx === 9 || ny === 6 || ny === 9)
    return { terrain:'walk', solid:false };
  if (biome === 'park' || biome === 'country') {
    if (rand % 31 === 0) return {terrain:'grass',prop:'tree',solid:true};
    if (rand % 23 === 0) return {terrain:'grass',prop:'bush',solid:true};
    if (rand % 59 === 0) return {terrain:'walk',prop:'bench',solid:true};
    return { terrain:rand % 5 ? 'grass' : 'grass2', solid:false };
  }
  if (nx >= 2 && nx <= 4 && ny >= 2 && ny <= 4) {
    if (nx === 3 && ny === 4) return {terrain:'walk',prop:'door',solid:true};
    return {terrain:'carpet',solid:true};
  }
  if (rand % 83 === 0) return {terrain:'grass',prop:'tree',solid:true};
  if (rand % 61 === 0) return {terrain:'walk',prop:'lamp',solid:true};
  if (rand % 67 === 0) return {terrain:'walk',prop:'bench',solid:true};
  return {terrain: biome==='market' || biome==='arts' ? 'walk' : 'grass', solid:false};
}
/** Bounded tile stream; camera position controls generation, not player steps. */
export function visibleWorldTiles(
  place: PixelPlace, left: number, top: number, cols: number, rows: number, seed: number,
): { x: number; y: number; cell: PixelCell }[] {
  if (!Number.isSafeInteger(left) || !Number.isSafeInteger(top) ||
      !Number.isSafeInteger(cols) || !Number.isSafeInteger(rows) ||
      cols <= 0 || rows <= 0 || cols * rows > 2500)
    throw Error('Visible tile window exceeds rendering budget');
  const tiles: {x:number;y:number;cell:PixelCell}[]=[];
  for(let y=top;y<top+rows;y++) for(let x=left;x<left+cols;x++)
    tiles.push({x,y,cell:worldCell(place,x,y,seed)});
  return tiles;
}

/** Saved player positions must use the SAME collision rules as the infinite
 * map renderer. The original town validator intentionally rejects off-map
 * coordinates; use it only for local café saves, never for street travel. */
export function validInfinitePosition(value: unknown, seed: number): value is PixelPosition {
  if(!value || typeof value!=='object')return false;
  const p=value as Partial<PixelPosition>;
  if(p.place==='cafe')return validPixelPosition(value);
  if(p.place!=='street'||!['up','down','left','right'].includes(p.facing??''))return false;
  if(!Number.isSafeInteger(p.x)||!Number.isSafeInteger(p.y))return false;
  const x=p.x as number,y=p.y as number;
  if(worldCell('street',x,y,seed).solid)return false;
  const npc=npcAt('street');
  return !(x===npc.x && y===npc.y);
}
