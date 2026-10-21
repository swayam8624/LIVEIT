import { describe, expect, it } from 'vitest';
import { ambientPedestrians } from './ambientPedestrians';
import { worldCell, validInfinitePosition } from './proceduralWorld';
import { residentProfile } from './residentProfiles';
import { residentObservation } from './residentDialogue';
import { regionActivityZone, regionArrival, regionAt, WORLD_REGIONS } from './worldRegions';

describe('original LIVEIT regional transport', () => {
  it('has nine distinct, named locations in one coordinate space', () => {
    expect(new Set(WORLD_REGIONS.map((r) => r.id)).size).toBe(9);
    for (const region of WORLD_REGIONS)
      expect(regionAt(region.x, region.y).id).toBe(region.id);
  });

  it('maps real game activities appropriately for distant districts', () => {
    expect(regionActivityZone('foundry')).toBe('market');
    expect(regionActivityZone('quayside')).toBe('market');
    expect(regionActivityZone('cedarwood')).toBe('garden');
    expect(regionActivityZone('willowmere')).toBe('street');
  });

  it('never delivers a character inside a wall or another canonical NPC', () => {
    for (const seed of [0, 17, 0xffffffff]) {
      for (const region of WORLD_REGIONS) {
        const arrival = regionArrival(region.id, seed);
        expect(regionAt(arrival.x, arrival.y).id).toBe(region.id);
        expect(validInfinitePosition(arrival, seed)).toBe(true);
        expect(worldCell('street', arrival.x, arrival.y, seed).solid).toBe(false);
      }
    }
  });
});

describe('deterministic resident identities and continuous movements', () => {
  it('assigns profile from stable resident identity, not time or viewport', () => {
    const a = residentProfile(19, '19:0:0:2', 0, 0);
    const b = residentProfile(19, '19:0:0:2', 0, 0);
    expect(b).toEqual(a);
    expect(a.name.split(' ').length).toBe(2);
    expect(['none', 'cap', 'satchel']).toContain(a.accessory);
  });

  it('offers reproducible, offline regional dialogue without a model', () => {
    const profile = residentProfile(33, '33:10:10:1', 320, 320);
    const first = residentObservation(profile, '33:10:10:1', 12);
    expect(first).toBe(residentObservation(profile, '33:10:10:1', 12));
    expect(first.length).toBeGreaterThan(12);
  });

  it('repeats the same resident state at the same simulated minute', () => {
    const first = ambientPedestrians(23, 0, 0, 32, 32, 620);
    const repeated = ambientPedestrians(23, 0, 0, 32, 32, 620);
    expect(repeated).toEqual(first);
    for (const r of first) {
      expect(r.profile.name).toBeTruthy();
      expect(worldCell('street', r.x, Math.round(r.y), 23).solid).toBe(false);
    }
  });

  it('uses a continuous path rather than clock-dependent random rerolls', () => {
    const a = ambientPedestrians(101, 320, 320, 32, 32, 640);
    const b = ambientPedestrians(101, 320, 320, 32, 32, 641);
    const matching = b.filter((person) => a.some((other) => other.id === person.id));
    for (const newer of matching) {
      const older = a.find((person) => person.id === newer.id)!;
      expect(newer.profile).toEqual(older.profile);
      expect(newer.spriteKey).toBe(older.spriteKey);
      expect(Math.hypot(newer.x - older.x, newer.y - older.y)).toBeLessThanOrEqual(1);
    }
  });

  it('does not use render discovery order to assign appearances', () => {
    const wide = ambientPedestrians(19, -8, -8, 48, 48, 850);
    const narrow = ambientPedestrians(19, 0, 0, 32, 32, 850);
    for (const resident of narrow) {
      const match = wide.find((person) => person.id === resident.id);
      expect(match?.profile).toEqual(resident.profile);
      expect(match?.spriteKey).toBe(resident.spriteKey);
    }
  });
});
