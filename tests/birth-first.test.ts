import { describe, expect, it } from 'vitest';
import { createBirthWorld, lifeStageOf, performChildhoodActivity, performWorldActivity, advanceCalendarMonth } from '@living/simulation-core';
import { encodeSave, decodeSave } from '@living/save-system';
describe('birth-first life', () => {
  it('starts at age zero with guardians, and persists the birth save', () => {
    const born=createBirthWorld('Robin','born-1');
    expect(born.player.ageDays).toBe(0);
    expect(born.player.money).toBe(0);
    expect(born.relationships.map(r=>r.characterId)).toEqual(['parent_mara','parent_eli']);
    expect(decodeSave(encodeSave({version:1,active:'life',life:born,story:null})).life).toEqual(born);
  });
  it('ages in calendar months without charging babies adult living expenses', () => {
    const baby=createBirthWorld('Morgan','born-2');
    const next=advanceCalendarMonth(baby);
    expect(next.player.ageDays).toBe(31);
    expect(next.player.money).toBe(0);
    expect(lifeStageOf(next.player.ageDays)).toBe('infant');
    expect(baby.player.ageDays).toBe(0);
  });
  it('allows infant bonding and forbids adult work / school', () => {
    const w=createBirthWorld('Ari');
    const bonded=performChildhoodActivity(w,'bond',0);
    expect(bonded.relationships[0]!.trust).toBeGreaterThan(w.relationships[0]!.trust);
    expect(()=>performChildhoodActivity(bonded,'bond',0)).toThrow();
    expect(()=>performChildhoodActivity(w,'study',0)).toThrow('old enough');
    expect(()=>performWorldActivity(w,'gig',0)).toThrow('locked');
  });
  it('enforces life stages on stage boundaries', () => {
    expect(lifeStageOf(0)).toBe('infant');
    expect(lifeStageOf(2*365)).toBe('toddler');
    expect(lifeStageOf(5*365)).toBe('child');
    expect(lifeStageOf(13*365)).toBe('teen');
    expect(lifeStageOf(18*365)).toBe('adult');
    expect(lifeStageOf(65*365)).toBe('senior');
  });
});
