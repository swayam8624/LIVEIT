import { stableSpriteHash } from './spriteIdentity';
import { regionAt, type RegionId } from './worldRegions';

/**
 * Names and small pixel accessories are LIVEIT-authored data. We do not import
 * unapproved generated concepts or third-party fan-game graphics.
 *
 * Assign from the immutable resident ID (not rerenders, time of day or camera)
 * and the immutable home district. The caller should persist this profile if
 * the ambient resident graduates into a named story character.
 */
const FIRST = [
  'Ada', 'Alba', 'Arlo', 'Ash', 'Bea', 'Cam', 'Cleo', 'Devi',
  'Eliot', 'Emi', 'Faye', 'Finn', 'Iris', 'Jules', 'Kai', 'Leah',
  'Leo', 'Mara', 'Milo', 'Nia', 'Noor', 'Owen', 'Rae', 'Ren',
  'Sage', 'Sam', 'Tess', 'Theo', 'Uma', 'Zoe',
] as const;
const LAST = [
  'Arden', 'Bell', 'Brooks', 'Chen', 'Cole', 'Das', 'Evans',
  'Fern', 'Hale', 'Ibarra', 'Jain', 'Kim', 'Lane', 'Moss',
  'Park', 'Quinn', 'Reed', 'Shaw', 'Stone', 'Vale', 'Wells',
] as const;

const OUTFIT_COLORS = [
  '#e9a77c', '#b8c7ec', '#f5d58e', '#b6d8a7',
  '#d5b4d9', '#92c8c1', '#e69ca8', '#b5a387',
] as const;

export type ResidentAccessory = 'none' | 'cap' | 'satchel';
export type ResidentRole =
  | 'student' | 'barista' | 'gardener' | 'artist' | 'mechanic'
  | 'dockworker' | 'shopkeeper' | 'commuter' | 'librarian'
  | 'walker' | 'musician' | 'visitor';

const ROLE_BY_REGION: Record<RegionId, readonly ResidentRole[]> = {
  bellweather: ['shopkeeper', 'barista', 'commuter', 'walker', 'visitor'],
  willowmere: ['student', 'librarian', 'commuter', 'visitor'],
  quayside: ['dockworker', 'shopkeeper', 'commuter', 'visitor'],
  larkspur: ['gardener', 'walker', 'visitor'],
  orchard: ['gardener', 'shopkeeper', 'walker'],
  foundry: ['mechanic', 'artist', 'commuter'],
  tideglass: ['dockworker', 'musician', 'walker', 'visitor'],
  oldtown: ['artist', 'musician', 'shopkeeper', 'visitor'],
  cedarwood: ['gardener', 'walker', 'visitor'],
};

export type ResidentProfile = Readonly<{
  name: string;
  role: ResidentRole;
  homeRegion: RegionId;
  outfitColor: string;
  accessory: ResidentAccessory;
}>;

export function residentProfile(
  seed: number,
  residentId: string,
  homeX: number,
  homeY: number,
): ResidentProfile {
  const hash = stableSpriteHash(seed, residentId);
  const region = regionAt(homeX, homeY);
  const roles = ROLE_BY_REGION[region.id];
  return {
    name: FIRST[hash % FIRST.length] + ' ' + LAST[(hash >>> 9) % LAST.length],
    role: roles[(hash >>> 15) % roles.length]!,
    homeRegion: region.id,
    outfitColor: OUTFIT_COLORS[(hash >>> 4) % OUTFIT_COLORS.length]!,
    accessory: (['none', 'cap', 'satchel'] as const)[(hash >>> 21) % 3]!,
  };
}
