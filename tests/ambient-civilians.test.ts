import {describe,it,expect} from 'vitest';
import {ambientPedestrians} from '../apps/player/src/ambientPedestrians';
import {seedFromTimeline,worldCell} from '../apps/player/src/proceduralWorld';

describe('chunk-aware pixel civilian routines',()=>{
  const seed=seedFromTimeline('living-world-3');
  it('repeats the same locations at the same time and seed',()=>{
    const a=ambientPedestrians(seed,-32,-32,48,48,480);
    expect(a).toEqual(ambientPedestrians(seed,-32,-32,64,64,480));
    expect(a.length).toBeGreaterThan(0);
  });
  it('never populates collisions or cells outside the rendered viewport',()=>{
    const people=ambientPedestrians(seed,-100,0,62,51,1120);
    for(const p of people){
      expect(p.x).toBeGreaterThanOrEqual(-100);
      expect(p.x).toBeLessThan(-38);
      expect(p.y).toBeGreaterThanOrEqual(0);
      expect(p.y).toBeLessThan(51);
      expect(worldCell('street',p.x,p.y,seed).solid).toBe(false);
      expect([1,2]).toContain(p.look);
    }
  });
  it('changes shifts by clock time, with fewer civilians sleeping at night',()=>{
    const night=ambientPedestrians(seed,128,128,32,32,90);
    const rush=ambientPedestrians(seed,128,128,32,32,490);
    expect(night.every(p=>p.shift==='home')).toBe(true);
    expect(rush.every(p=>p.shift==='commute')).toBe(true);
    expect(rush.length).toBeGreaterThanOrEqual(night.length);
  });
  it('refuses runaway viewport allocations',()=>{
    expect(ambientPedestrians(seed,0,0,100,100,600)).toEqual([]);
    expect(ambientPedestrians(seed,0,0,-1,1,600)).toEqual([]);
  });
});
