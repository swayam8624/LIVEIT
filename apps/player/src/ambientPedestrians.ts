import { CHUNK_SIZE, tileHash, worldCell } from './proceduralWorld';
import type { Facing } from './pixelTownLogic';
import { ambientSpriteAssignment } from './spriteIdentity';
import { residentProfile, type ResidentProfile } from './residentProfiles';

export type AmbientPedestrian = Readonly<{
  id: string;
  x: number;
  y: number;
  look: 1 | 2;
  /** Stable visual key; currently restricted to approved CC0 placeholders. */
  spriteKey: 'pulse:n1' | 'pulse:n2';
  profile: ResidentProfile;
  facing: Facing;
  shift: 'commute' | 'work' | 'leisure' | 'home';
}>;
/** Visual crowd simulation. The 32x32 region owns stable civilian IDs.
 * Their time-dependent routines are generated without server calls or
 * persistent NPC allocations, and are deliberately non-interactive until
 * an individual is promoted into a named, persisted NPC.
 */
export function ambientPedestrians(
  seed: number,
  left: number,
  top: number,
  cols: number,
  rows: number,
  minuteOfDay: number,
): AmbientPedestrian[] {
  if (
    ![left, top, cols, rows, minuteOfDay].every(Number.isFinite) ||
    cols < 1 ||
    rows < 1 ||
    cols * rows > 2500
  )
    return [];
  const hour = Math.floor((((minuteOfDay % 1440) + 1440) % 1440) / 60);
  const shift =
    hour < 6 || hour >= 22
      ? 'home'
      : hour < 9
        ? 'commute'
        : hour < 17
          ? 'work'
          : 'leisure';
  // Most people go home after ten. Peak foot traffic is on commute routes.
  const count = shift === 'home' ? 1 : shift === 'commute' ? 4 : 3;
  const results: AmbientPedestrian[] = [];
  const firstX = Math.floor(left / CHUNK_SIZE),
    lastX = Math.floor((left + cols - 1) / CHUNK_SIZE);
  const firstY = Math.floor(top / CHUNK_SIZE),
    lastY = Math.floor((top + rows - 1) / CHUNK_SIZE);
  for (let cy = firstY; cy <= lastY; cy++)
    for (let cx = firstX; cx <= lastX; cx++) {
      for (let i = 0; i < count; i++) {
        const hash = tileHash(
          seed ^ 0x525449,
          cx * 17 + i * 37,
          cy * 13 + i * 53,
        );
        // Every resident follows a repeatable daily loop on public sidewalks.
        // Use the same global roads as the chunk generator: no seam seams.
        // Generate a deterministic *sidewalk* resident rather than rolling
        // arbitrary solid building tiles. The global grid uses x%16=6/9
        // for publicly walkable pavements across chunk seams.
        const id = seed + ':' + cx + ':' + cy + ':' + i;
        const visual = ambientSpriteAssignment(seed, id);
        // Keep movement entirely inside one 32x32 chunk. The triangle-wave
        // gait reverses gently rather than teleporting from +3 to -3.
        const localX =
          ((hash >>> 9) % 2 === 0 ? 6 : 9) + ((hash >>> 12) % 2) * 16;
        const baseY = 4 + ((hash >>> 7) % (CHUNK_SIZE - 8));
        const x = cx * CHUNK_SIZE + localX;
        const base = cy * CHUNK_SIZE + baseY;
        const cycle = [0, 1, 2, 3, 2, 1, 0, -1, -2, -3, -2, -1] as const;
        const progress = (((minuteOfDay % 1440) + 1440) % 1440) / 12;
        const step = Math.floor(progress);
        const fraction = progress - step;
        // Smoothstep has zero velocity at each waypoint, reducing jitter on
        // slow displays while keeping the position deterministic across saves.
        const blend = fraction * fraction * (3 - 2 * fraction);
        const from = base + cycle[(step + (hash >>> 25)) % cycle.length]!;
        const to = base + cycle[(step + 1 + (hash >>> 25)) % cycle.length]!;
        const traversable =
          !worldCell('street', x, Math.round(from), seed).solid &&
          !worldCell('street', x, Math.round(to), seed).solid;
        const y =
          shift === 'home' || !traversable
            ? base
            : from + (to - from) * blend;
        const facing: Facing =
          shift === 'home' || !traversable || from === to
            ? 'down'
            : to > from
              ? 'down'
              : 'up';
        if (x < left || x >= left + cols || y < top || y >= top + rows)
          continue;
        if (worldCell('street', x, y, seed).solid) continue;
        if (x === 10 && y === 7) continue; // canonical Amelia spawn
        results.push({
          id,
          x,
          y,
          facing,
          look: visual.look,
          spriteKey: visual.spriteKey,
          profile: residentProfile(seed, id, cx * CHUNK_SIZE, cy * CHUNK_SIZE),
          shift,
        });
      }
    }
  return results;
}
