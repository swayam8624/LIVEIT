import { describe, expect, it } from 'vitest';
import { createWorld, performWorldActivity } from '@living/simulation-core';
import { decodeSave, encodeSave } from '@living/save-system';

describe('world-space daily interactions', () => {
  it('market gig pays one £35 shift without skipping a day or aging', () => {
    const start = createWorld();
    const next = performWorldActivity(start, 'gig', 0);
    expect(next.player.money - start.player.money).toBe(3500);
    expect(next.player.skill).toBe(start.player.skill + 1);
    expect(next.player.ageDays).toBe(start.player.ageDays);
    expect(next.day).toBe(start.day);
    expect(start.player.money).toBe(180000);
    expect(() => performWorldActivity(next, 'gig', 0)).toThrow('Already done');
    const secondDay = performWorldActivity(next, 'gig', 1);
    expect(secondDay.player.money).toBe(187000);
  });

  it('coffee and garden activities affect real save state, one action each per day', () => {
    const start = createWorld();
    const coffee = performWorldActivity(start, 'cafe', 0);
    expect(coffee.player.money).toBe(179550);
    expect(coffee.player.wellbeing).toBe(74);
    const garden = performWorldActivity(coffee, 'garden', 0);
    expect(garden.player.wellbeing).toBe(79);
    expect(decodeSave(encodeSave({version:1,active:'life',life:garden,story:null})).life).toEqual(garden);
  });

  it('rejects untrusted input and preserves the previous state', () => {
    const start = createWorld();
    for (const offset of [-1, 30, 0.5, NaN])
      expect(() => performWorldActivity(start, 'gig', offset)).toThrow();
    expect(() => performWorldActivity(start, 'cash_machine' as 'gig', 0)).toThrow();
    expect(start.facts.some(f => f.startsWith('free-life-action:'))).toBe(false);
  });

  it('does not permit coffee when funds are insufficient', () => {
    const start = createWorld();
    start.player.money = 0;
    expect(() => performWorldActivity(start, 'cafe', 0)).toThrow('Not enough cash');
  });
});
