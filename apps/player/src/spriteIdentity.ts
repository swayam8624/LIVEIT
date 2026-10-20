/**
 * Stable identity-to-art mapping. This module deliberately does not import
 * concept PNGs: all 86 concept packs are still awaiting production approval.
 *
 * A resident's appearance is selected from their world seed and persistent ID,
 * never from camera coordinates, clock time, render count or array position.
 * Save spriteKey when promoting an ambient resident into the narrative roster.
 */
export type ApprovedAmbientSpriteKey = 'pulse:n1' | 'pulse:n2';

export type AmbientSpriteAssignment = Readonly<{
  look: 1 | 2;
  spriteKey: ApprovedAmbientSpriteKey;
}>;

/** FNV-1a over a stable UTF-16 code-unit string, using defined 32-bit overflow. */
export function stableSpriteHash(worldSeed: number, residentId: string): number {
  let hash = 0x811c9dc5;
  const key = String(worldSeed >>> 0) + ':' + residentId;
  for (let i = 0; i < key.length; i++) {
    hash ^= key.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193);
  }
  return hash >>> 0;
}

/**
 * The only eligible visual variants today are the two existing CC0 actors.
 * Expand this allowlist only after pack rights, native-scale visual QA,
 * animation coverage, identity and accessibility approval are recorded.
 */
export function ambientSpriteAssignment(
  worldSeed: number,
  residentId: string,
): AmbientSpriteAssignment {
  const look = (stableSpriteHash(worldSeed, residentId) & 1) === 0 ? 1 : 2;
  return { look, spriteKey: look === 1 ? 'pulse:n1' : 'pulse:n2' };
}
