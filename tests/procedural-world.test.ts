import { describe, expect, it } from 'vitest';
import { chunkOf, worldCell, visibleWorldTiles, seedFromTimeline, biomeAt, validInfinitePosition } from '../apps/player/src/proceduralWorld';
import { pixelCell } from '../apps/player/src/pixelTownLogic';
describe('procedural infinite world coordinate model', () => {
  const seed=seedFromTimeline('birth-A');
  it('maps positive and negative coordinates to stable 32x32 chunks',()=>{
    expect(chunkOf(-1,-33)).toEqual({cx:-1,cy:-2,lx:31,ly:31});
    expect(chunkOf(32,64)).toEqual({cx:1,cy:2,lx:0,ly:0});
    expect(chunkOf(0,0)).toEqual({cx:0,cy:0,lx:0,ly:0});
  });
  it('is deterministic and samples far-away tiles without allocating all chunks',()=>{
    for(const [x,y] of ([[-1,0],[409600,12],[-409601,-200000],[31,31],[32,32]] as Array<[number,number]>)) {
      expect(worldCell('street',x,y,seed)).toEqual(worldCell('street',x,y,seed));
      expect(biomeAt(seed,x,y)).toEqual(biomeAt(seed,x,y));
    }
  });
  it('preserves the old neighborhood and cafe',()=>{
    expect(worldCell('street',5,6,seed)).toEqual(pixelCell('street',5,6));
    expect(worldCell('cafe',5,9,seed)).toEqual(pixelCell('cafe',5,9));
  });
  it('guarantees passable roads at every distant chunk seam',()=>{
    for(const x of [-65,-64,-33,-32,-1,31,32,33,63,64,65,5000]) {
      expect(['road','crosswalk']).toContain(worldCell('street',x,-25,seed).terrain);
      expect(worldCell('street',x,-25,seed).solid).toBe(false);
    }
  });
  it('restores distant and negative travel positions instead of forgetting them',()=>{
    const east={place:'street',x:4096,y:7,facing:'right'};
    const west={place:'street',x:-39,y:-25,facing:'left'};
    expect(validInfinitePosition(east,seed)).toBe(true);
    expect(validInfinitePosition(west,seed)).toBe(true);
    expect(validInfinitePosition({...east,x:4.2},seed)).toBe(false);
    expect(validInfinitePosition({...east,facing:'diagonal'},seed)).toBe(false);
    expect(validInfinitePosition({place:'street',x:10,y:7,facing:'up'},seed)).toBe(false);
  });
  it('bounds visible tile memory independent of how far player traveled',()=>{
    const a=visibleWorldTiles('street',-200000,99990,15,18,seed);
    expect(a).toHaveLength(270);
    expect(a[0]).toEqual({x:-200000,y:99990,cell:worldCell('street',-200000,99990,seed)});
    expect(()=>visibleWorldTiles('street',0,0,100,100,seed)).toThrow('budget');
  });
});
