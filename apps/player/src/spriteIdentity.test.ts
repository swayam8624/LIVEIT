import { describe, expect, it } from 'vitest';
import { ambientSpriteAssignment, stableSpriteHash } from './spriteIdentity';

describe('stable ambient sprite identity', () => {
  it('returns identical appearances across rerenders, reloads and discovery order', () => {
    const resident = '17:2:-1:3';
    const first = ambientSpriteAssignment(17, resident);
    expect(ambientSpriteAssignment(17, resident)).toEqual(first);
    expect(ambientSpriteAssignment(17, resident)).toEqual(first);
    expect(first.spriteKey).toBe(first.look === 1 ? 'pulse:n1' : 'pulse:n2');
  });

  it('only selects the currently approved static CC0 fallback family', () => {
    for (let seed = -10; seed < 10; seed++) {
      for (let resident = 0; resident < 50; resident++) {
        const assignment = ambientSpriteAssignment(seed, 'resident:' + resident);
        expect(['pulse:n1', 'pulse:n2']).toContain(assignment.spriteKey);
        expect([1, 2]).toContain(assignment.look);
      }
    }
  });

  it('normalizes the world seed into a defined 32-bit value', () => {
    expect(stableSpriteHash(-1, 'a')).toBe(stableSpriteHash(0xffffffff, 'a'));
    expect(stableSpriteHash(2 ** 32 + 7, 'b')).toBe(stableSpriteHash(7, 'b'));
  });

  it('is insensitive to UI order and simulated time', () => {
    const ids = ['4:1:2:0', '4:1:2:1', '4:1:2:2'];
    const first = new Map(ids.map((id) => [id, ambientSpriteAssignment(4, id)]));
    for (const id of [...ids].reverse())
      expect(ambientSpriteAssignment(4, id)).toEqual(first.get(id));
  });
});
