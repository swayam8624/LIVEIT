import { describe, expect, it } from 'vitest';
import {
  createBirthWorld, createWorld, advanceCalendarMonth,
  LIFE_MILESTONES, applyLifeMilestones, skipToAge,
} from '@living/simulation-core';
import { encodeSave, decodeSave } from '@living/save-system';

describe('monthly family development and permanent memories', () => {
  it('gives a newborn one stable authored milestone as each month passes', () => {
    let world=createBirthWorld('Jules','family-calendar');
    const initial=world.relationships[0]!.trust;
    world=advanceCalendarMonth(world);
    expect(world.facts).toContain('life.milestone:settling_home');
    expect(world.memories).toHaveLength(1);
    expect(world.relationships[0]!.trust).toBeGreaterThan(initial);
    expect(world.history.some(h=>h.text.includes('A World of Voices'))).toBe(true);
    const second=advanceCalendarMonth(world);
    expect(second.facts.filter(f=>f==='life.milestone:settling_home')).toHaveLength(1);
    expect(second.memories.filter(m=>m.fact==='life.milestone:settling_home')).toHaveLength(1);
  });

  it('preserves guardian bond even without clicking bonding actions every week', () => {
    let world=createBirthWorld('June','guardian-bond');
    const before=world.relationships.find(r=>r.characterId==='parent_eli')!.trust;
    for(let month=0;month<12;month++)world=advanceCalendarMonth(world);
    expect(world.relationships.find(r=>r.characterId==='parent_eli')!.trust).toBe(before);
    expect(world.player.ageDays).toBe(365);
    expect(world.facts).toContain('life.milestone:first_birthday');
  });

  it('does not inject childhood memories into legacy adult saves', () => {
    const adult=createWorld('Morgan','legacy-adult');
    const advanced=advanceCalendarMonth(adult);
    expect(advanced.memories).toHaveLength(0);
    expect(advanced.facts.some(f=>f.startsWith('life.milestone:'))).toBe(false);
    expect(applyLifeMilestones(adult)).toEqual([]);
  });

  it('supports meaningful skip-to-toddler without deleting skipped events', () => {
    const newborn=createBirthWorld('Noah','toddler-transition');
    const toddler=skipToAge(newborn,2);
    expect(toddler.player.ageDays).toBe(730);
    expect(toddler.facts).toContain('life.milestone:first_birthday');
    expect(toddler.facts).toContain('life.milestone:toddler_years');
    expect(toddler.memories.length).toBeGreaterThanOrEqual(6);
    expect(decodeSave(encodeSave({
      version:1,active:'life',life:toddler,story:null,
    })).life).toEqual(toddler);
    expect(newborn.player.ageDays).toBe(0);
  });

  it('has unique milestone months and IDs, no silent scene duplicates', () => {
    expect(new Set(LIFE_MILESTONES.map(m=>m.month)).size).toBe(LIFE_MILESTONES.length);
    expect(new Set(LIFE_MILESTONES.map(m=>m.id)).size).toBe(LIFE_MILESTONES.length);
    expect(LIFE_MILESTONES.every(m=>m.narration.length<290)).toBe(true);
  });
});
