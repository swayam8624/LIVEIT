import { describe, it, expect } from 'vitest';
import { WorldSchema } from '@living/world-schema';
import {
  createWorld, ageUp, CATALOG, portfolio, netWorth,
  buyAsset, sellAsset, investIndex, withdrawIndex,
} from '@living/simulation-core';

describe('LIVEIT native life: financial actions', () => {
  it('opens the same valid legacy save without adding any required fields', () => {
    const legacy = createWorld();
    delete legacy.portfolio;
    expect(WorldSchema.parse(legacy)).toEqual(legacy);
    expect(portfolio(legacy).indexPence).toBe(0);
    expect(netWorth(legacy)).toBe(legacy.player.money);
  });
  it('buys a bicycle transactionally and prevents duplicate purchases', () => {
    const initial = createWorld();
    const next = buyAsset(initial, 'bicycle');
    expect(initial.portfolio).toBeUndefined();
    expect(initial.player.money).toBe(180000);
    expect(next.player.money).toBe(180000 - CATALOG.bicycle.price);
    expect(next.portfolio?.owned[0]?.id).toBe('bicycle');
    expect(() => buyAsset(next, 'bicycle')).toThrow('already own');
    expect(() => buyAsset(initial, 'townhouse')).toThrow('Not enough');
    expect(next.history.at(-1)?.kind).toBe('choice');
  });
  it('cannot exploit transactions or invest an invalid amount', () => {
    const w = createWorld();
    expect(() => investIndex(w, Number.NaN)).toThrow();
    expect(() => investIndex(w, -100)).toThrow();
    expect(() => investIndex(w, 200000)).toThrow('Not enough');
    expect(() => withdrawIndex(w, 5000)).toThrow('Insufficient');
    expect(() => sellAsset(w, 'car')).toThrow('do not own');
    const after = sellAsset(buyAsset(w, 'bicycle'), 'bicycle');
    expect(after.player.money).toBeLessThan(w.player.money);
    expect(after.portfolio?.owned.length).toBe(0);
  });
  it('adds deterministic index returns exactly once per annual transition', () => {
    const seed = investIndex(createWorld(), 10000);
    const a = ageUp(seed);
    const b = ageUp(seed);
    expect(a).toEqual(b);
    expect(seed.portfolio?.indexPence).toBe(10000);
    expect(a.portfolio?.indexPence).toBe(10800); // year 1 uses 1.08
    expect(a.history.some(x => x.text.includes('simulated market cycle'))).toBe(true);
    expect(a.player.ageDays).toBe(seed.player.ageDays + 365);
  });
  it('retains invested assets through further age-ups and withdrawals', () => {
    const initial = investIndex(createWorld(), 10000);
    const afterYear = ageUp(initial);
    const next = withdrawIndex(afterYear, 5000);
    expect(next.portfolio?.indexPence).toBe(5800);
    expect(next.player.money).toBe(afterYear.player.money + 5000);
    expect(netWorth(next)).toBe(netWorth(afterYear));
  });
  it('holds the purchase in the same validated event-sourced world', () => {
    const world = buyAsset(createWorld(), 'bicycle');
    expect(WorldSchema.parse(world)).toEqual(world);
    expect(world.history.at(-1)?.text).toContain('City bicycle');
    expect(world.portfolio?.owned[0]?.dayBought).toBe(world.day);
  });
});
