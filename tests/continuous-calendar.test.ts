import { describe, expect, it } from 'vitest';
import { createWorld, advanceCalendarMonth } from '@living/simulation-core';
import { WorldSchema } from '@living/world-schema';
import { encodeSave, decodeSave } from '@living/save-system';

describe('continuous world calendar', () => {
  it('ages exactly one month while preserving identity and the old save schema', () => {
    const original = createWorld('Jordan');
    const month = advanceCalendarMonth(original);
    expect(original.day).toBe(0);
    expect(original.player.ageDays).toBe(23 * 365);
    expect(month.day).toBe(31);
    expect(month.player.ageDays).toBe(23 * 365 + 31);
    expect(month.player.name).toBe('Jordan');
    expect(month.player.wellbeing).toBe(original.player.wellbeing);
    expect(month.player.money).toBe(93200);
    expect(month.relationships[0]!.trust).toBeLessThan(35);
    expect(WorldSchema.parse(month)).toEqual(month);
    const copy = decodeSave(encodeSave({ version: 1, active: 'life', life: month, story: null }));
    expect(copy.life).toEqual(month);
  });

  it('twelve active-play months add up to exactly one birthday', () => {
    let world = createWorld();
    for (let i = 0; i < 12; i++) world = advanceCalendarMonth(world);
    expect(world.player.ageDays).toBe(24 * 365);
    expect(world.day).toBe(365);
  });

  it('is deterministic and does not mutate the input', () => {
    const original = createWorld();
    expect(advanceCalendarMonth(original)).toEqual(advanceCalendarMonth(original));
    expect(original.day).toBe(0);
  });

  it('pays wages only to an employed character during workdays', () => {
    const original = createWorld();
    const employed = {
      ...original,
      player: { ...original.player, career: 'employed' as const },
    };
    const month = advanceCalendarMonth(employed);
    expect(month.player.money).toBeGreaterThan(advanceCalendarMonth(original).player.money);
  });
});
