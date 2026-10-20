import { describe, expect, it } from 'vitest';
import {
  INITIAL_POSITION,
  CAFE_HEIGHT,
  CAFE_WIDTH,
  STREET_HEIGHT,
  STREET_WIDTH,
  isNpcAdjacent,
  movePixel,
  npcAt,
  pixelCell,
  validPixelPosition,
  type PixelPosition,
} from '../apps/player/src/pixelTownLogic';

describe('pixel-only Bellweather walking game', () => {
  it('has a valid persistent spawn and two real 2D authored collision maps', () => {
    expect(validPixelPosition(INITIAL_POSITION)).toBe(true);
    const areas = [
      { place: 'street' as const, w: STREET_WIDTH, h: STREET_HEIGHT },
      { place: 'cafe' as const, w: CAFE_WIDTH, h: CAFE_HEIGHT },
    ];
    for (const area of areas) {
      let floors = 0;
      let obstacles = 0;
      for (let y = 0; y < area.h; y++) {
        for (let x = 0; x < area.w; x++) {
          const tile = pixelCell(area.place, x, y);
          if (tile.solid) obstacles++;
          else floors++;
        }
      }
      expect(floors).toBeGreaterThan(30);
      expect(obstacles).toBeGreaterThan(8);
    }
    expect(pixelCell('street', -1, 0).solid).toBe(true);
    expect(pixelCell('cafe', 30, 100).solid).toBe(true);
  });

  it('walks with authentic cardinal movement but cannot cross walls or NPCs', () => {
    expect(movePixel(INITIAL_POSITION, 'left').position.x).toBe(10);
    expect(movePixel(INITIAL_POSITION, 'up').position.y).toBe(7);
    const nearAmelia = movePixel(INITIAL_POSITION, 'up').position;
    expect(isNpcAdjacent(nearAmelia)).toBe(true);
    const facingNpc = movePixel(nearAmelia, 'left');
    expect(facingNpc.event).toBe('npc-nearby');
    expect(facingNpc.position.x).toBe(11);
    expect(facingNpc.position.facing).toBe('left');
    const nearWall: PixelPosition = {
      place: 'street',
      x: 9,
      y: 3,
      facing: 'left',
    };
    expect(movePixel(nearWall, 'left').event).toBe('blocked');
  });

  it('can enter the café and exit through a genuine return portal', () => {
    const outside: PixelPosition = {
      place: 'street',
      x: 5,
      y: 7,
      facing: 'up',
    };
    expect(validPixelPosition(outside)).toBe(true);
    const entered = movePixel(outside, 'up');
    expect(entered.event).toBe('entered-cafe');
    expect(entered.position).toMatchObject({ place: 'cafe', x: 5, y: 8 });
    const exited = movePixel(entered.position, 'down');
    expect(exited.event).toBe('left-cafe');
    expect(exited.position).toMatchObject({ place: 'street', x: 5, y: 7 });
  });

  it('saves only valid coordinates, rejects out-of-bounds and invalid corrupt saves', () => {
    expect(
      validPixelPosition({ place: 'street', x: 4, y: 4, facing: 'down' }),
    ).toBe(false);
    expect(
      validPixelPosition({ place: 'street', x: 10, y: 7, facing: 'down' }),
    ).toBe(false);
    expect(
      validPixelPosition({ place: 'cafe', x: 5, y: 8, facing: 'down' }),
    ).toBe(true);
    expect(
      validPixelPosition({ place: 'cafe', x: NaN, y: 1, facing: 'down' }),
    ).toBe(false);
    expect(
      movePixel({ place: 'street', x: -1, y: 0, facing: 'up' }, 'left')
        .position,
    ).toEqual(INITIAL_POSITION);
    expect(npcAt('street').name).toBe('Amelia');
  });
});
