import { createWorld, advanceCalendarMonth } from './index';
import { initialHousehold, initialSchool } from './familySchool';
import {
  WorldSchema,
  record,
  type World,
  type Appearance,
  DEFAULT_APPEARANCE,
} from '@living/world-schema';
type Pronouns = World['player']['pronouns'];
export type LifeStage =
  'infant' | 'toddler' | 'child' | 'teen' | 'adult' | 'senior';
/** Age is stored in days; no legacy save format change. */
export function lifeStageOf(ageDays: number): LifeStage {
  if (!Number.isSafeInteger(ageDays) || ageDays < 0) throw Error('Invalid age');
  const age = ageDays / 365;
  if (age < 2) return 'infant';
  if (age < 5) return 'toddler';
  if (age < 13) return 'child';
  if (age < 18) return 'teen';
  if (age < 65) return 'adult';
  return 'senior';
}
/**
 * New protagonists begin literally at birth, within a family.
 * createWorld remains the legacy adult factory for existing tests/saves;
 * only "Begin New Life" uses this birth-origin constructor.
 */
export function createBirthWorld(
  name: string,
  timelineId = 'main',
  pronouns: Pronouns = 'they/them',
  appearance: Appearance = DEFAULT_APPEARANCE,
): World {
  const w = createWorld(name, timelineId, pronouns, appearance);
  w.player.ageDays = 0;
  w.player.skill = 0;
  w.player.money = 0; // Household money will be modeled separately.
  w.player.career = 'seeking';
  w.player.wellbeing = 85;
  w.relationships = [
    { characterId: 'parent_mara', trust: 86, lastContactDay: 0 },
    { characterId: 'parent_eli', trust: 78, lastContactDay: 0 },
  ];
  w.facts = ['life_origin:born_in_bellweather', 'life_stage:infant'];
  w.household = initialHousehold();
  w.school = initialSchool();
  w.history = [];
  record(
    w,
    'creation',
    name + ' was born in Bellweather. Their life begins at day zero.',
  );
  return WorldSchema.parse(w);
}
export type ChildhoodActivity =
  'bond' | 'play' | 'learn' | 'rest' | 'study' | 'make_friend';
/** Child actions are event- and age-gated, persistent, and cannot mint wages. */
export function performChildhoodActivity(
  input: World,
  activity: ChildhoodActivity,
  offset: number,
): World {
  const w = structuredClone(WorldSchema.parse(input));
  const age = w.player.ageDays / 365;
  if (age >= 18) throw Error('Use adult activities after turning 18.');
  if (!Number.isSafeInteger(offset) || offset < 0 || offset > 29)
    throw Error('Invalid day within simulated month.');
  if (
    !['bond', 'play', 'learn', 'rest', 'study', 'make_friend'].includes(
      activity,
    )
  )
    throw Error('Unknown childhood activity.');
  if (age < 2 && !['bond', 'rest', 'play'].includes(activity))
    throw Error('Not old enough for this activity yet.');
  if (age < 5 && activity === 'study') throw Error('School starts later.');
  if (age < 5 && activity === 'make_friend')
    throw Error('Friendships unlock with preschool.');
  const marker = 'child_act:' + (w.day + offset) + ':' + activity;
  if (w.facts.includes(marker)) throw Error('You already did that today.');
  if (w.facts.length > 9500)
    w.facts = w.facts.filter((x) => !x.startsWith('child_act:')).slice(-9000);
  const clamp = (x: number) => Math.min(100, Math.max(0, x));
  if (activity === 'bond') {
    const parent = w.relationships.find((r) => r.characterId === 'parent_mara');
    if (parent) {
      parent.trust = clamp(parent.trust + 3);
      parent.lastContactDay = w.day + offset;
    }
    w.player.wellbeing = clamp(w.player.wellbeing + 4);
  } else if (activity === 'play') {
    w.player.wellbeing = clamp(w.player.wellbeing + 2);
    w.player.skill = clamp(w.player.skill + 1);
  } else if (activity === 'rest') {
    w.player.wellbeing = clamp(w.player.wellbeing + 5);
  } else if (activity === 'learn' || activity === 'study') {
    w.player.skill = clamp(w.player.skill + (activity === 'study' ? 3 : 2));
  } else {
    const friend = w.relationships.find(
      (r) => r.characterId === 'childhood_friend',
    );
    if (friend) {
      friend.trust = clamp(friend.trust + 3);
      friend.lastContactDay = w.day + offset;
    } else
      w.relationships.push({
        characterId: 'childhood_friend',
        trust: 45,
        lastContactDay: w.day + offset,
      });
    w.player.wellbeing = clamp(w.player.wellbeing + 2);
  }
  w.facts.push(marker);
  record(
    w,
    'simulation',
    'Childhood: ' + activity.replace('_', ' ') + ' in Bellweather.',
  );
  return WorldSchema.parse(w);
}
/** Optional explicit childhood skip, never the hidden default time progression. */
export function skipToAge(input: World, targetYears: 2 | 5 | 13 | 18): World {
  let w = WorldSchema.parse(input);
  if (w.player.ageDays / 365 >= targetYears)
    throw Error('Cannot skip backwards.');
  while (w.player.ageDays < targetYears * 365) w = advanceCalendarMonth(w);
  return w;
}
