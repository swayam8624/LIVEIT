import { describe, expect, it } from 'vitest';
import {
  findTileRoute,
  targetForTap,
} from '../apps/player/src/pixelPathfinding';
import {
  INITIAL_POSITION,
  npcAt,
  pixelCell,
  type PixelPlace,
} from '../apps/player/src/pixelTownLogic';

describe('touch-to-walk Bellweather navigation', () => {
  it('finds a continuous route to a legal market destination', () => {
    const from = { x: INITIAL_POSITION.x, y: INITIAL_POSITION.y };
    const path = findTileRoute('street', from, { x: 17, y: 9 });
    expect(path.length).toBeGreaterThan(0);
    let previous = from;
    for (const step of path) {
      expect(
        Math.abs(previous.x - step.x) + Math.abs(previous.y - step.y),
      ).toBe(1);
      expect(pixelCell('street', step.x, step.y).solid).toBe(false);
      previous = step;
    }
    expect(previous).toEqual({ x: 17, y: 9 });
  });

  it('avoids buildings but supports valid procedural terrain beyond town limits', () => {
    const start = { x: INITIAL_POSITION.x, y: INITIAL_POSITION.y };
    expect(findTileRoute('street', start, { x: 4, y: 4 })).toEqual([]);
    expect(
      findTileRoute('street', start, { x: -1, y: 0 }).length,
    ).toBeGreaterThan(0);
    expect(findTileRoute('cafe', { x: 5, y: 8 }, { x: -1, y: 0 })).toEqual([]);
    expect(targetForTap('street', { x: 4, y: 4 }, start)).toBeNull();
  });

  it('turns a tap on Amelia into an accessible adjacent talking position', () => {
    const start = { x: INITIAL_POSITION.x, y: INITIAL_POSITION.y };
    for (const place of ['street', 'cafe'] as PixelPlace[]) {
      const npc = npcAt(place);
      const origin = place === 'street' ? start : { x: 5, y: 8 };
      const dest = targetForTap(place, npc, origin);
      expect(dest).not.toBeNull();
      expect(Math.abs(dest!.x - npc.x) + Math.abs(dest!.y - npc.y)).toBe(1);
      const path = findTileRoute(place, origin, dest!);
      expect(
        path.length || (origin.x === dest!.x && origin.y === dest!.y),
      ).toBeTruthy();
    }
  });

  it('is deterministic and cannot cross the NPC collision cell', () => {
    const start = { x: INITIAL_POSITION.x, y: INITIAL_POSITION.y };
    const goal = { x: 8, y: 9 };
    const first = findTileRoute('street', start, goal);
    expect(first).toEqual(findTileRoute('street', start, goal));
    expect(first.some((step) => step.x === 10 && step.y === 7)).toBe(false);
  });
});
