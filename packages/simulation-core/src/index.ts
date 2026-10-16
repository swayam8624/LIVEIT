import { initialCityState, tickCity } from './city';
export { CITY_OPPORTUNITIES, DISTRICTS, availableCityOpportunities, chooseCareer, cityState, visitDistrict, resolveCityOpportunity } from './city';
export type { CityOpportunity, CityChoice } from './city';
import {
  WorldSchema,
  record,
  type World,
  type Character,
} from '@living/world-schema';
/** Creates a reproducible modern-city life. Identity is supplied by the save owner. */
export function createWorld(
  name = 'Alex Morgan',
  timelineId = 'main',
  pronouns: Character['pronouns'] = 'they/them',
): World {
  return WorldSchema.parse({
    schemaVersion: 1,
    timelineId,
    worldId: 'modern_life_v1',
    day: 0,
    player: {
      id: 'player',
      name,
      pronouns,
      ageDays: 23 * 365,
      wellbeing: 72,
      skill: 20,
      career: 'seeking',
      money: 180000,
    },
    relationships: [
      { characterId: 'amelia', trust: 35, lastContactDay: 0 },
      { characterId: 'noah', trust: 55, lastContactDay: 0 },
    ],
    memories: [],
    history: [
      {
        id: `${timelineId}:event:0`,
        day: 0,
        kind: 'creation',
        text: 'A new apartment. A new city. A chance to begin again.',
      },
    ],
    facts: ['university_attended'],
    progress: [],
    city: initialCityState(),
  });
}
export type Activity = 'work' | 'study' | 'rest' | 'socialize';
/** One meaningful activity per day; routine costs are automatic. Money uses integer cents. */
export function advanceLife(input: World, activity: Activity, days = 1): World {
  if (!['work', 'study', 'rest', 'socialize'].includes(activity))
    throw new Error('Unknown activity');
  if (!Number.isInteger(days) || days < 1 || days > 30)
    throw new Error('Advance between 1 and 30 days');
  const w = structuredClone(WorldSchema.parse(input));
  for (let i = 0; i < days; i++) {
    w.day++;
    w.player.ageDays++;
    tickCity(w, activity);
    w.player.money -= 2800;
    if (activity === 'work') {
      if (w.player.career === 'seeking' && w.player.skill >= 25)
        w.player.career = 'employed';
      w.player.money += w.player.career === 'employed' ? 12000 : 6500;
      w.player.wellbeing -= 4;
      w.player.skill += 1;
    }
    if (activity === 'study') {
      w.player.skill += 4;
      w.player.wellbeing -= 1;
    }
    if (activity === 'rest') w.player.wellbeing += 9;
    if (activity === 'socialize') {
      w.player.wellbeing += 5;
      const friend = w.relationships.find((r) => r.characterId === 'noah');
      if (friend) {
        friend.trust = Math.min(100, friend.trust + 3);
        friend.lastContactDay = w.day;
      }
    }
    w.player.wellbeing = Math.max(0, Math.min(100, w.player.wellbeing));
    w.player.skill = Math.min(100, w.player.skill);
    if (w.day % 7 === 0) {
      for (const r of w.relationships)
        if (w.day - r.lastContactDay >= 7) r.trust = Math.max(0, r.trust - 1);
      record(
        w,
        'simulation',
        'A week in Bellweather. Untended friendships feel a little more distant.',
      );
    }
  }
  record(
    w,
    'simulation',
    `${days} ${days === 1 ? 'day' : 'days'} spent ${activity === 'work' ? 'working' : activity === 'study' ? 'learning' : activity === 'rest' ? 'resting' : 'with Noah'}. Daily living costs: £28.`,
  );
  return WorldSchema.parse(w);
}
