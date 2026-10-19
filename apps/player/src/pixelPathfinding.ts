import {
  CAFE_HEIGHT, CAFE_WIDTH, STREET_HEIGHT, STREET_WIDTH,
  npcAt, pixelCell, type PixelPlace,
} from './pixelTownLogic';

/**
 * Bounded BFS over the authored logical grid. At most 690 cells in Bellweather,
 * giving predictable latency without LLM path plans or a cloud route service.
 *
 * Passability comes directly from the same map as keyboard collision, so tap
 * navigation cannot walk through a closed building or through an NPC.
 */
export type TilePoint = Readonly<{ x: number; y: number }>;
const CARDINAL: readonly TilePoint[] = [
  { x: 0, y: -1 }, { x: 1, y: 0 },
  { x: 0, y: 1 }, { x: -1, y: 0 },
];

function dims(place: PixelPlace): { width: number; height: number } {
  return place === 'street'
    ? { width: STREET_WIDTH, height: STREET_HEIGHT }
    : { width: CAFE_WIDTH, height: CAFE_HEIGHT };
}

function walkable(place: PixelPlace, p: TilePoint): boolean {
  const {width,height} = dims(place);
  if (!Number.isSafeInteger(p.x) || !Number.isSafeInteger(p.y) ||
      p.x < 0 || p.y < 0 || p.x >= width || p.y >= height) return false;
  const npc = npcAt(place);
  return !pixelCell(place, p.x, p.y).solid &&
    !(npc.x === p.x && npc.y === p.y);
}
const key = (p: TilePoint) => p.x + ',' + p.y;

/** Reach an adjacent tile when a player taps on a character. */
export function targetForTap(place: PixelPlace, tap: TilePoint, from: TilePoint): TilePoint | null {
  const npc = npcAt(place);
  if (tap.x !== npc.x || tap.y !== npc.y)
    return walkable(place, tap) ? tap : null;
  const alternatives = CARDINAL.map(d => ({x:tap.x + d.x, y:tap.y+d.y}))
    .filter(p => walkable(place, p))
    .sort((a,b) => (Math.abs(a.x-from.x)+Math.abs(a.y-from.y)) -
      (Math.abs(b.x-from.x)+Math.abs(b.y-from.y)));
  return alternatives[0] ?? null;
}

export function findTileRoute(
  place: PixelPlace, start: TilePoint, goal: TilePoint,
): TilePoint[] {
  if (!walkable(place, start) || !walkable(place, goal)) return [];
  if (start.x === goal.x && start.y === goal.y) return [];
  const queue: TilePoint[] = [start];
  const parent = new Map<string,string>();
  const visited = new Set<string>([key(start)]);
  let found = false;
  for (let head=0; head<queue.length; head++) {
    const node = queue[head]!;
    if (node.x===goal.x && node.y===goal.y) {found=true;break;}
    for (const d of CARDINAL) {
      const next = {x:node.x+d.x,y:node.y+d.y};
      const k = key(next);
      if (visited.has(k) || !walkable(place,next)) continue;
      visited.add(k);
      parent.set(k,key(node));
      queue.push(next);
    }
  }
  if (!found) return [];
  const route: TilePoint[] = [];
  let cursor = key(goal);
  const root = key(start);
  while (cursor!==root) {
    const [x,y] = cursor.split(',').map(Number);
    route.push({x:x!, y:y!});
    cursor = parent.get(cursor) ?? root;
  }
  return route.reverse();
}
