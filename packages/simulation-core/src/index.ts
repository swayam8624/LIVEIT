import { settleHouseholdAndSchoolMonth } from './familySchool';
export {
  initialHousehold,
  initialSchool,
  performSchoolAction,
} from './familySchool';
export type { SchoolAction } from './familySchool';
export {
  SOCIAL_NPCS,
  canTalkTo,
  buildNPCSystemPrompt,
  recordNPCConversation,
} from './npcMemory';
export type { SocialNPC } from './npcMemory';
import { applyLifeMilestones } from './lifeMilestones';
export { applyLifeMilestones, LIFE_MILESTONES } from './lifeMilestones';
export type { LifeMilestone } from './lifeMilestones';
export {
  DAILY_ACTIVITIES,
  activitiesForAge,
  dailyActivitiesUsed,
  performDailyActivity,
} from './dailyActivities';
export type {
  DailyActivity,
  DailyActivityId,
  ActivityZone,
} from './dailyActivities';
export { actOnRelationship, relationshipStatus } from './relationshipLife';
export type {
  RelationshipAction,
  RelationshipStatus,
} from './relationshipLife';
export {
  createBirthWorld,
  lifeStageOf,
  performChildhoodActivity,
  skipToAge,
} from './birthLife';
export type { ChildhoodActivity, LifeStage } from './birthLife';
export {
  buildPixelRenderFrame,
  buildCinematicRenderFrame,
} from './render-adapter';
export type { PixelWorldPose } from './render-adapter';
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

/**
 * Advance one calendar month without pretending the player spent 30 days
 * resting, studying or socializing. Salary is paid on approximately 22
 * workdays, bills accrue daily, passive NPC lives tick, and neglected
 * relationships change gradually. One call = 30 simulated days.
 *
 * The UI triggers this only after 60 actual active gameplay minutes. The
 * elapsed fraction is persisted separately so old v1 saves do not break.
 */
export function advanceCalendarMonth(input: World): World {
  const w = structuredClone(WorldSchema.parse(input));
  // Align month boundaries to the existing 365-day age model. Exactly
  // twelve hourly month ticks equal one birthday, despite 30/31-day months.
  const monthIndex = Math.floor((w.player.ageDays * 12) / 365);
  const days = Math.ceil(((monthIndex + 1) * 365) / 12) - w.player.ageDays;
  for (let i = 0; i < days; i++) {
    w.day += 1;
    w.player.ageDays += 1;
    tickNPCs(w);
    const workday = w.day % 7 < 5;
    if (workday && w.player.career === 'employed') {
      const contract = w.city?.employment;
      w.player.money +=
        contract && contract.stage !== 'applied'
          ? Math.round(contract.salaryAnnual / 260)
          : 12000;
    }
    // A newborn/child does not personally pay the household bills. Adult
    // expenses start at 18; guardian finances will be a separate family ledger.
    if (w.player.ageDays >= 18 * 365) {
      w.player.money = Math.max(
        -100000000,
        Math.min(100000000, w.player.money - 2800),
      );
    }
    if (w.day % 7 === 0) {
      for (const relation of w.relationships)
        if (
          !relation.characterId.startsWith('parent_') &&
          w.player.ageDays >= 5 * 365 &&
          w.day - relation.lastContactDay >= 7
        )
          relation.trust = Math.max(0, relation.trust - 1);
    }
  }
  const birthday = w.player.ageDays % 365 === 0;
  if (birthday && w.player.ageDays <= 18 * 365) {
    const years = w.player.ageDays / 365;
    record(
      w,
      'simulation',
      'Birthday! ' + w.player.name + ' turns ' + years + '.',
    );
    if (years === 5) w.facts.push('school:primary_started');
    if (years === 13) {
      w.facts.push('school:secondary_started');
      if (!w.relationships.some((r) => r.characterId === 'amelia'))
        w.relationships.push({
          characterId: 'amelia',
          trust: 35,
          lastContactDay: w.day,
        });
      if (!w.relationships.some((r) => r.characterId === 'noah'))
        w.relationships.push({
          characterId: 'noah',
          trust: 55,
          lastContactDay: w.day,
        });
    }
    if (years === 18) w.facts.push('life_stage:adult');
  }
  settleHouseholdAndSchoolMonth(w);
  applyLifeMilestones(w);
  record(
    w,
    'simulation',
    'A month passes in Bellweather. Your life continues while the town changes around you.',
  );
  return WorldSchema.parse(w);
}

export type WorldActivity = 'cafe' | 'gig' | 'garden';

/**
 * A free-roam action belongs to an in-game *day*, not a year-advancing
 * dashboard shortcut. The walk clock owns time. The action cannot repeatedly
 * mint money by tapping the same button dozens of times each simulated day.
 *
 * The marker is authoritative and travels with the existing strict v1 save.
 * NPC model responses cannot call this API: actions require a real UI tap.
 */
export function performWorldActivity(
  input: World,
  activity: WorldActivity,
  dayOffset: number,
): World {
  if (!['cafe', 'gig', 'garden'].includes(activity))
    throw new Error('Invalid world action');
  if (!Number.isInteger(dayOffset) || dayOffset < 0 || dayOffset > 29)
    throw new Error('Invalid simulated day');

  const w = structuredClone(WorldSchema.parse(input));
  if (w.player.ageDays < 16 * 365)
    throw new Error(
      'Work, purchases, and adult-world activities are locked until an age-appropriate stage.',
    );
  const serialDay = w.day + dayOffset;
  const marker = 'free-life-action:' + serialDay + ':' + activity;
  if (w.facts.includes(marker))
    throw new Error('Already done today. Explore something else!');
  if (w.facts.length >= 9900) {
    // Preserve story facts and memories; only old activity cooldown markers
    // are recyclable once the campaign becomes multi-decade-long.
    w.facts = w.facts
      .filter((f) => !f.startsWith('free-life-action:'))
      .slice(-9000);
  }
  if (activity === 'cafe') {
    if (w.player.money < 450)
      throw new Error('Not enough cash for a café visit.');
    w.player.money -= 450;
    w.player.wellbeing = Math.min(100, w.player.wellbeing + 2);
    record(
      w,
      'simulation',
      'Bought coffee and took a quiet break at the Bellweather café.',
    );
  } else if (activity === 'gig') {
    w.player.money = Math.min(100000000, w.player.money + 3500);
    w.player.skill = Math.min(100, w.player.skill + 1);
    w.player.wellbeing = Math.max(0, w.player.wellbeing - 2);
    record(w, 'simulation', 'Completed a short market gig and earned £35.');
  } else {
    w.player.wellbeing = Math.min(100, w.player.wellbeing + 5);
    record(
      w,
      'simulation',
      'Spent the afternoon resting in Bellweather gardens.',
    );
  }
  w.facts.push(marker);
  return WorldSchema.parse(w);
}
