import { describe, expect, it } from 'vitest';
import { createWorld, ageUp, LIFE_MOMENTS, pendingLifeMoment, resolveLifeMoment } from '@living/simulation-core';
import { WorldSchema } from '@living/world-schema';

describe('annual life-event Director', () => {
  it('offers an authored choice rather than silently modifying a status screen', () => {
    const initial=createWorld('Taylor Quinn');
    const next=ageUp(initial);
    const pending=pendingLifeMoment(next);
    expect(pending).not.toBeNull();
    expect(pending!.choices.length).toBeGreaterThanOrEqual(2);
    expect(initial.lifeMoments).toBeUndefined();
    expect(next.lifeMoments?.seen.length).toBe(1);
    expect(WorldSchema.parse(next)).toEqual(next);
  });
  it('changes gameplay state, writes a permanent history event, and prevents double choices', () => {
    const world=ageUp(createWorld());
    const moment=pendingLifeMoment(world)!;
    const choice=moment.choices[0]!;
    const before=world.history.length;
    const resolved=resolveLifeMoment(world,choice.id);
    expect(resolved.lifeMoments?.pendingId).toBeNull();
    expect(resolved.history).toHaveLength(before+1);
    expect(resolved.history.at(-1)?.kind).toBe('choice');
    expect(resolved.history.at(-1)?.text).toContain(choice.result);
    expect(() => resolveLifeMoment(resolved, choice.id)).toThrow('No life decision');
    expect(world.lifeMoments?.pendingId).toBe(moment.id);
  });
  it('rejects non-existent choices and has deterministic event selection', () => {
    const seed=createWorld('Alex Morgan');
    const a=ageUp(seed), b=ageUp(seed);
    expect(a).toEqual(b);
    expect(() => resolveLifeMoment(a, '__invalid__')).toThrow('not available');
  });
  it('changes distinct results for at least two different options', () => {
    const w=ageUp(createWorld());
    const m=pendingLifeMoment(w)!;
    const one=resolveLifeMoment(w,m.choices[0]!.id);
    const two=resolveLifeMoment(w,m.choices[1]!.id);
    expect(one).not.toEqual(two);
    expect(one.history.at(-1)?.text).not.toBe(two.history.at(-1)?.text);
  });
  it('maintains schema validity, cooldowns and age across 40 simulated years', () => {
    let w=createWorld('Nora Bell');
    const ids:string[]=[];
    for(let year=0;year<40;year++){
      w=ageUp(w);
      const current=pendingLifeMoment(w);
      if(current){
        ids.push(current.id);
        w=resolveLifeMoment(w,current.choices[year%current.choices.length]!.id);
      }
      expect(WorldSchema.safeParse(w).success).toBe(true);
      expect(w.player.wellbeing).toBeGreaterThanOrEqual(0);
      expect(w.player.money).toBeLessThanOrEqual(100000000);
    }
    expect(ids.length).toBeGreaterThanOrEqual(30);
    expect(w.player.ageDays).toBe(63*365);
  });
  it('contains original contextual scenes with at least two authored outcomes', () => {
    expect(LIFE_MOMENTS.length).toBeGreaterThanOrEqual(12);
    for(const m of LIFE_MOMENTS){
      expect(m.choices.length).toBeGreaterThanOrEqual(2);
      expect(m.situation.length).toBeGreaterThan(55);
      expect(new Set(m.choices.map(c=>c.id)).size).toBe(m.choices.length);
    }
  });
});
