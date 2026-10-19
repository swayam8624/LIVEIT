import {describe,expect,it} from 'vitest';
import {MODERN_DIRECTIONS,modernSpriteColumn} from '../apps/player/src/spriteDirections';
describe('owner supplied Modern 24-frame sprite sheet',()=>{
  it('maps sheet groups to right, up, left, down in that order',()=>{
    expect(MODERN_DIRECTIONS).toEqual({right:0,up:1,left:2,down:3});
    expect(modernSpriteColumn('right',0)).toBe(0);
    expect(modernSpriteColumn('up',0)).toBe(6);
    expect(modernSpriteColumn('left',0)).toBe(12);
    expect(modernSpriteColumn('down',0)).toBe(18);
    expect(modernSpriteColumn('right',5)).toBe(5);
    expect(modernSpriteColumn('left',8)).toBe(14);
  });
});
