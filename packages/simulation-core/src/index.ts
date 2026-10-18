export { buildVisualScene } from './visual-scene';
export type { CastMember } from './visual-scene';
export { generateCityScene, projectCityBlock } from './city-scene';
export type { CityScene, CityBlock } from './city-scene';
export {
  LIFE_MOMENTS,
  pendingLifeMoment,
  scheduleLifeMoment,
  resolveLifeMoment,
} from './moments';
export type { LifeMoment, MomentChoice } from './moments';
export {
  CATALOG,
  portfolio,
  assetValue,
  netWorth,
  buyAsset,
  sellAsset,
  investIndex,
  withdrawIndex,
} from './portfolio';
export type { AssetId } from './portfolio';
export {
  applyForJob,
  attendJobInterview,
  requestPromotion,
  resignFromJob,
  ageUp,
} from './life';
import { initialCityState, tickCity } from './city';
import { initialNPCLives, tickNPCs } from './npc';
export { NPC_BEATS, initialNPCLives } from './npc';
export {
  CITY_OPPORTUNITIES,
  DISTRICTS,
  availableCityOpportunities,
  chooseCareer,
  cityState,
  visitDistrict,
  resolveCityOpportunity,
} from './city';
export type { CityOpportunity, CityChoice } from './city';
import {
  WorldSchema,
  record,
  DEFAULT_APPEARANCE,
  AppearanceSchema,
  type Appearance,
  type World,
  type Character,
} from '@living/world-schema';
/** Creates a reproducible modern-city life. Identity is supplied by the save owner. */
export function createWorld(
  name = 'Alex Morgan',
  timelineId = 'main',
  pronouns: Character['pronouns'] = 'they/them',
  appearance: Appearance = DEFAULT_APPEARANCE,
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
      appearance: AppearanceSchema.parse(appearance),
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
    npcLives: initialNPCLives(),
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
    tickNPCs(w);
    w.player.money -= 2800;
    if (activity === 'work') {
      if (
        !w.city?.employment &&
        w.player.career === 'seeking' &&
        w.player.skill >= 25
      )
        w.player.career = 'employed';
      const careerJob = w.city?.employment;
      // An actual chosen job pays its contract rate; old v1 employment
      // still uses its original wages so legacy playthroughs do not change.
      w.player.money += careerJob
        ? careerJob.stage === 'applied'
          ? 6500
          : Math.round(careerJob.salaryAnnual / 260)
        : w.player.career === 'employed'
          ? 12000
          : 6500;
      w.player.wellbeing -= 4;
      w.player.skill += 1;
      if (careerJob && careerJob.stage !== 'applied')
        careerJob.experience = Math.min(20000, careerJob.experience + 1);
      if (w.player.career === 'employed' && w.city) {
        const bonus = {
          undecided: 0,
          technology: 2200,
          creative: 800,
          business: 2800,
          community: 1200,
        }[w.city.careerPath];
        w.player.money += bonus;
        if (w.city.careerPath === 'business')
          w.city.stress = Math.min(100, w.city.stress + 2);
        if (w.city.careerPath === 'community')
          w.city.connections = Math.min(100, w.city.connections + 1);
      }
      if (w.city?.district === 'market') w.player.money += 1500;
    }
    if (activity === 'study') {
      w.player.skill += w.city?.district === 'university' ? 5 : 4;
      w.player.wellbeing -= 1;
      if (w.city?.district === 'studio')
        w.city.reputation = Math.min(100, w.city.reputation + 1);
    }
    if (activity === 'rest')
      w.player.wellbeing += w.city?.district === 'gardens' ? 12 : 9;
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

/** Re-style an existing character without purchasing clothing or changing stats. */
export function setCharacterAppearance(
  input: World,
  appearance: Appearance,
): World {
  const world = structuredClone(WorldSchema.parse(input));
  world.player.appearance = AppearanceSchema.parse(appearance);
  return WorldSchema.parse(world);
}
