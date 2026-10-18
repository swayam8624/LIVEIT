import { WorldSchema, record, type World } from '@living/world-schema';

/**
 * A deterministic early life-event Director. Authored options change real
 * world state rather than granting generic "choice acknowledged" messages.
 * This content array is deliberately small: broaden with reviewed data packs
 * after the transitions, save semantics and gameplay have proven reliable.
 */
type Effect = {
  money?: number;
  wellbeing?: number;
  skill?: number;
  stress?: number;
  reputation?: number;
  connections?: number;
  trust?: { who: 'amelia' | 'noah'; delta: number };
  fact?: string;
};
export type MomentChoice = {
  id: string;
  text: string;
  result: string;
  effect: Effect;
};
export type LifeMoment = {
  id: string;
  title: string;
  situation: string;
  minAge: number;
  maxAge?: number;
  requires?:
    'job' | 'freelance' | 'low-wellbeing' | 'trusted-friend' | 'skilled';
  choices: readonly MomentChoice[];
};
export const LIFE_MOMENTS: readonly LifeMoment[] = [
  {
    id: 'rent-pressure',
    title: 'The rent is going up',
    situation:
      'Your landlord raises the rent. A cheaper room is available across town, but you would lose your familiar neighborhood.',
    minAge: 18,
    choices: [
      {
        id: 'move',
        text: 'Move to the cheaper room',
        result: 'You traded convenience for savings.',
        effect: { money: 28000, wellbeing: -5, stress: 2 },
      },
      {
        id: 'negotiate',
        text: 'Ask for a fairer deal',
        result: 'You negotiated some breathing room.',
        effect: { skill: 3, reputation: 2, money: -9000 },
      },
      {
        id: 'stay',
        text: 'Stay and pay the increase',
        result: 'Keeping your routine was expensive.',
        effect: { money: -25000, wellbeing: 3 },
      },
    ],
  },
  {
    id: 'noah-emergency',
    title: 'A call after midnight',
    situation:
      'Noah has had a difficult week and needs someone to show up. Tomorrow is an important workday.',
    minAge: 18,
    choices: [
      {
        id: 'visit',
        text: 'Spend the night with Noah',
        result: 'Noah remembers that you came.',
        effect: { trust: { who: 'noah', delta: 14 }, stress: 7, wellbeing: 3 },
      },
      {
        id: 'call',
        text: 'Stay on the phone until morning',
        result: 'A difficult conversation brought you closer.',
        effect: { trust: { who: 'noah', delta: 7 }, wellbeing: -2 },
      },
      {
        id: 'decline',
        text: 'Protect your own time',
        result: 'You got needed rest, but Noah felt alone.',
        effect: { trust: { who: 'noah', delta: -8 }, wellbeing: 4 },
      },
    ],
  },
  {
    id: 'amelia-exhibition',
    title: 'One seat left',
    situation:
      'Amelia invites you to an exhibition that matters deeply to her. You had already planned to take on some extra work.',
    minAge: 18,
    choices: [
      {
        id: 'go',
        text: 'Go and listen',
        result: 'You shared an afternoon that Amelia will remember.',
        effect: {
          trust: { who: 'amelia', delta: 10 },
          money: -3500,
          wellbeing: 5,
        },
      },
      {
        id: 'work',
        text: 'Keep your existing commitment',
        result: 'You earned the fee, but missed something personal.',
        effect: { money: 19000, trust: { who: 'amelia', delta: -5 } },
      },
      {
        id: 'reschedule',
        text: 'Suggest a quieter evening together',
        result: 'Amelia appreciated your honesty.',
        effect: { trust: { who: 'amelia', delta: 4 }, stress: -3 },
      },
    ],
  },
  {
    id: 'missed-invoice',
    title: 'An unpaid invoice',
    situation:
      'A client has delayed payment for weeks. The money would cover your bills; chasing it might cost you future work.',
    minAge: 18,
    requires: 'freelance',
    choices: [
      {
        id: 'push',
        text: 'Demand payment in writing',
        result: 'Your persistence paid off.',
        effect: { money: 28000, reputation: -4, skill: 2 },
      },
      {
        id: 'plan',
        text: 'Negotiate installments',
        result: 'You protected the relationship but waited longer.',
        effect: { money: 12000, reputation: 3 },
      },
      {
        id: 'walk',
        text: 'Write it off and move on',
        result: 'You avoided the conflict, but not the loss.',
        effect: { money: -12000, stress: -4 },
      },
    ],
  },
  {
    id: 'career-mentor',
    title: 'A demanding mentor',
    situation:
      'Someone senior offers to coach you outside work hours. Their advice could change your career trajectory.',
    minAge: 19,
    requires: 'job',
    choices: [
      {
        id: 'accept',
        text: 'Make time for weekly sessions',
        result: 'Your skills grew, at a personal cost.',
        effect: { skill: 12, stress: 8, reputation: 5 },
      },
      {
        id: 'boundaries',
        text: 'Meet occasionally, with boundaries',
        result: 'You learned steadily without giving up your weekends.',
        effect: { skill: 6, stress: 2 },
      },
      {
        id: 'decline',
        text: 'Keep your evenings free',
        result: 'You chose a quieter year.',
        effect: { wellbeing: 8 },
      },
    ],
  },
  {
    id: 'town-vote',
    title: 'The neighborhood vote',
    situation:
      'A local project could bring new jobs but close the riverside garden. Your vote and influence might matter.',
    minAge: 18,
    choices: [
      {
        id: 'garden',
        text: 'Organize for the garden',
        result: 'Neighbors learned your name.',
        effect: { connections: 9, reputation: 6, money: -7000, wellbeing: 3 },
      },
      {
        id: 'jobs',
        text: 'Support the new development',
        result: 'Local employers noticed your involvement.',
        effect: { connections: 7, money: 12000, reputation: -2 },
      },
      {
        id: 'study',
        text: 'Research a compromise',
        result: 'You discovered people on both sides were willing to listen.',
        effect: { skill: 5, connections: 5, stress: 4 },
      },
    ],
  },
  {
    id: 'burnout-signs',
    title: 'You are running on empty',
    situation:
      'Late nights and constant obligations have started to catch up with you. Something has to change.',
    minAge: 18,
    requires: 'low-wellbeing',
    choices: [
      {
        id: 'recover',
        text: 'Take time off and recover',
        result: 'Your mind felt clearer after a genuine rest.',
        effect: { wellbeing: 18, money: -45000, stress: -18 },
      },
      {
        id: 'care',
        text: 'Seek professional support',
        result: 'You received practical support, without any instant miracle.',
        effect: { wellbeing: 11, money: -12000, stress: -13 },
      },
      {
        id: 'ignore',
        text: 'Push through for now',
        result: 'The pressure has not disappeared.',
        effect: { money: 22000, wellbeing: -12, stress: 13 },
      },
    ],
  },
  {
    id: 'learning-opportunity',
    title: 'An unexpected scholarship',
    situation:
      'A community program offers a subsidized course. It could open doors, but the application requires effort.',
    minAge: 18,
    choices: [
      {
        id: 'apply',
        text: 'Apply and commit to the course',
        result: 'Months of study changed what you could attempt next.',
        effect: { skill: 14, stress: 7, money: -5000 },
      },
      {
        id: 'evening',
        text: 'Take the shorter evening course',
        result: 'You made steady progress at your own pace.',
        effect: { skill: 7, wellbeing: -2 },
      },
      {
        id: 'pass',
        text: 'Pass this time',
        result: 'You kept your time free for other priorities.',
        effect: { wellbeing: 4, money: 8000 },
      },
    ],
  },
  {
    id: 'risky-offer',
    title: 'The too-perfect investment',
    situation:
      'An acquaintance promises guaranteed returns. They want money before showing any documents.',
    minAge: 18,
    choices: [
      {
        id: 'verify',
        text: 'Request documents and decline',
        result: 'The acquaintance stopped replying when asked for proof.',
        effect: { skill: 4, reputation: 3 },
      },
      {
        id: 'share',
        text: 'Warn your friends',
        result: 'You helped others avoid a costly mistake.',
        effect: { connections: 5, reputation: 7 },
      },
      {
        id: 'gamble',
        text: 'Risk the money anyway',
        result: 'The promised return never arrived.',
        effect: { money: -60000, stress: 12 },
      },
    ],
  },
  {
    id: 'gallery-audition',
    title: 'An open audition',
    situation:
      'A local arts collective wants fresh performers and designers. The application deadline is tonight.',
    minAge: 18,
    choices: [
      {
        id: 'audition',
        text: 'Show your work',
        result: 'People began recognizing your creative efforts.',
        effect: { skill: 8, reputation: 5, wellbeing: 3, money: -6000 },
      },
      {
        id: 'volunteer',
        text: 'Help backstage',
        result: 'You met people who might change your future.',
        effect: { connections: 10, wellbeing: 4 },
      },
      {
        id: 'observe',
        text: 'Attend as a guest',
        result: 'A memorable evening gave you new ideas.',
        effect: { wellbeing: 5 },
      },
    ],
  },
  {
    id: 'shared-business',
    title: 'A friend wants a partner',
    situation:
      'Someone you know proposes a small neighborhood business. They have energy and ideas, but not much experience.',
    minAge: 21,
    requires: 'skilled',
    choices: [
      {
        id: 'partner',
        text: 'Invest in a trial launch',
        result: 'The pilot sold well, but demanded more time than expected.',
        effect: {
          money: -30000,
          skill: 8,
          connections: 10,
          stress: 8,
          fact: 'explored_small_business',
        },
      },
      {
        id: 'advise',
        text: 'Offer advice without investing',
        result: 'You helped clarify the plan without risking savings.',
        effect: { skill: 4, reputation: 5 },
      },
      {
        id: 'decline',
        text: 'Decline and focus on your current path',
        result: 'You protected your attention and stability.',
        effect: { wellbeing: 6 },
      },
    ],
  },
  {
    id: 'found-letter',
    title: 'A letter you never expected',
    situation:
      'An unsigned envelope contains old photographs of the city, including one from the place you first met Amelia.',
    minAge: 18,
    choices: [
      {
        id: 'share',
        text: 'Show the photographs to Amelia',
        result: 'An old memory opened a new conversation.',
        effect: {
          trust: { who: 'amelia', delta: 10 },
          wellbeing: 5,
          fact: 'shared_old_photographs',
        },
      },
      {
        id: 'archive',
        text: 'Keep them in your personal archive',
        result: 'You kept a fragment of your past.',
        effect: { wellbeing: 4, fact: 'kept_old_photographs' },
      },
      {
        id: 'donate',
        text: 'Donate the photographs to the local archive',
        result: 'A piece of neighborhood history found a home.',
        effect: { reputation: 7, connections: 4 },
      },
    ],
  },
  {
    id: 'unexpected-health',
    title: 'A reminder to take care',
    situation:
      'A community clinic offers a routine checkup. It is not urgent, but you have been putting your own needs last.',
    minAge: 18,
    choices: [
      {
        id: 'check',
        text: 'Book the checkup',
        result: 'You learned more about caring for your health.',
        effect: { wellbeing: 6, money: -7000, stress: -3 },
      },
      {
        id: 'activity',
        text: 'Start a gentle exercise routine',
        result: 'An ordinary habit made everyday life easier.',
        effect: { wellbeing: 8, stress: -4 },
      },
      {
        id: 'wait',
        text: 'Put it off another year',
        result: 'You saved a little money and gained no clarity.',
        effect: { money: 3000, stress: 2 },
      },
    ],
  },
];
const clamp = (value: number, min = 0, max = 100) =>
  Math.max(min, Math.min(max, Math.round(value)));
const momentById = (id: string) => LIFE_MOMENTS.find((m) => m.id === id);
const allowed = (world: World, moment: LifeMoment): boolean => {
  const age = Math.floor(world.player.ageDays / 365);
  if (
    age < moment.minAge ||
    (moment.maxAge !== undefined && age > moment.maxAge)
  )
    return false;
  switch (moment.requires) {
    case 'job':
      return (
        !!world.city?.employment && world.city.employment.stage !== 'applied'
      );
    case 'freelance':
      return (
        !world.city?.employment || world.city.employment.stage === 'applied'
      );
    case 'low-wellbeing':
      return world.player.wellbeing <= 60 || (world.city?.stress ?? 0) >= 60;
    case 'trusted-friend':
      return world.relationships.some((r) => r.trust >= 45);
    case 'skilled':
      return world.player.skill >= 35;
    default:
      return true;
  }
};
/** Called on one annual world update. Never starts an AI request. */
export function scheduleLifeMoment(world: World): void {
  world.lifeMoments ??= { pendingId: null, seen: [] };
  if (world.lifeMoments.pendingId) {
    record(
      world,
      'simulation',
      'An earlier opportunity passed while you moved on with life.',
    );
    world.lifeMoments.pendingId = null;
  }
  const age = Math.floor(world.player.ageDays / 365);
  const eligible = LIFE_MOMENTS.filter(
    (m) =>
      allowed(world, m) &&
      !world.lifeMoments!.seen.some(
        (s) => s.id === m.id && world.day - s.day < 4 * 365,
      ),
  );
  if (eligible.length === 0) return;
  // Stable per-life schedule that differs between identities but replays
  // exactly from the same world state, without Math.random or Date.now.
  const salt = [...world.player.name].reduce((v, c) => v + c.charCodeAt(0), 0);
  const choice = eligible[(salt + age * 17 + world.day) % eligible.length]!;
  world.lifeMoments.pendingId = choice.id;
  world.lifeMoments.seen.push({ id: choice.id, day: world.day });
  world.lifeMoments.seen = world.lifeMoments.seen.slice(-100);
}
export function pendingLifeMoment(world: World): LifeMoment | null {
  return momentById(world.lifeMoments?.pendingId ?? '') ?? null;
}
/** Atomic allow-listed choice resolution against the persisted life state. */
export function resolveLifeMoment(input: World, choiceId: string): World {
  const world = structuredClone(WorldSchema.parse(input));
  const moment = pendingLifeMoment(world);
  if (!moment) throw new Error('No life decision is currently waiting.');
  const choice = moment.choices.find((c) => c.id === choiceId);
  if (!choice)
    throw new Error('This option is not available for this decision.');
  const e = choice.effect;
  if (e.money !== undefined)
    world.player.money = clamp(
      world.player.money + e.money,
      -100_000_000,
      100_000_000,
    );
  if (e.wellbeing !== undefined)
    world.player.wellbeing = clamp(world.player.wellbeing + e.wellbeing);
  if (e.skill !== undefined)
    world.player.skill = clamp(world.player.skill + e.skill);
  if (world.city) {
    if (e.stress !== undefined)
      world.city.stress = clamp(world.city.stress + e.stress);
    if (e.reputation !== undefined)
      world.city.reputation = clamp(world.city.reputation + e.reputation);
    if (e.connections !== undefined)
      world.city.connections = clamp(world.city.connections + e.connections);
  }
  if (e.trust) {
    const friend = world.relationships.find(
      (x) => x.characterId === e.trust!.who,
    );
    if (friend) {
      friend.trust = clamp(friend.trust + e.trust.delta);
      friend.lastContactDay = world.day;
    }
  }
  if (e.fact && !world.facts.includes(e.fact)) world.facts.push(e.fact);
  world.lifeMoments!.pendingId = null;
  record(world, 'choice', `${moment.title}: ${choice.result}`);
  return WorldSchema.parse(world);
}
