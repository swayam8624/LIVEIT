import { WorldSchema, record, type World } from '@living/world-schema';

/**
 * Everyday actions are deterministic, age-gated transactions against the
 * canonical World save. They never rely on a language model to grant rewards.
 * Money is stored in *pence*, never floating-point pounds.
 *
 * An activity is accessible only in its physical zone (or "anywhere") and
 * players get at most four activities per simulated day. This prevents
 * repeatedly tapping a free-money button thousands of times while standing
 * still, without reducing meaningful choices to an annual BitLife-style click.
 */
export type ActivityZone = 'street' | 'market' | 'garden' | 'cafe';
type Group =
  | 'Family'
  | 'Learning'
  | 'Friends'
  | 'Fitness'
  | 'Creative'
  | 'Career'
  | 'Wellbeing'
  | 'Leisure';
type Relation = 'parent_mara' | 'parent_eli' | 'childhood_friend' | 'amelia';
export type DailyActivity = Readonly<{
  id: string;
  label: string;
  description: string;
  group: Group;
  icon: string;
  minYears: number;
  maxYears?: number;
  zone?: ActivityZone;
  cost?: number;
  earnings?: number;
  wellbeing?: number;
  skill?: number;
  stress?: number;
  reputation?: number;
  trustTarget?: Relation;
  trust?: number;
  requiresEmployment?: boolean;
  requiresPartner?: boolean;
}>;

/** Original activities with meaningful skill, finances, relationship effects. */
export const DAILY_ACTIVITIES = [
  {
    id: 'family_cuddle',
    label: 'Cuddle with a parent',
    description: 'Feel safe, heard and loved.',
    icon: '♥',
    group: 'Family',
    minYears: 0,
    maxYears: 3,
    wellbeing: 5,
    trustTarget: 'parent_mara',
    trust: 4,
  },
  {
    id: 'soft_blocks',
    label: 'Play with soft blocks',
    description: 'Experiment with shapes and movement.',
    icon: '▣',
    group: 'Learning',
    minYears: 0,
    maxYears: 4,
    skill: 1,
    wellbeing: 2,
  },
  {
    id: 'bedtime_story',
    label: 'Listen to a bedtime story',
    description: 'A quiet story with a familiar voice.',
    icon: '☾',
    group: 'Family',
    minYears: 0,
    maxYears: 13,
    skill: 1,
    trustTarget: 'parent_eli',
    trust: 3,
    wellbeing: 3,
  },
  {
    id: 'toddler_paint',
    label: 'Finger-paint',
    description: 'Make a magnificent mess.',
    icon: '✎',
    group: 'Creative',
    minYears: 2,
    maxYears: 6,
    skill: 2,
    wellbeing: 3,
  },
  {
    id: 'meet_classmate',
    label: 'Make a new friend',
    description: 'Introduce yourself and listen.',
    icon: '☺',
    group: 'Friends',
    minYears: 3,
    maxYears: 18,
    wellbeing: 3,
    trustTarget: 'childhood_friend',
    trust: 6,
  },
  {
    id: 'playground',
    label: 'Play in the park',
    description: 'Climb and explore under the trees.',
    icon: '♣',
    group: 'Fitness',
    minYears: 3,
    maxYears: 18,
    zone: 'garden',
    wellbeing: 5,
    skill: 1,
  },
  {
    id: 'homework',
    label: 'Finish homework',
    description: 'Your effort today helps your future self.',
    icon: '✎',
    group: 'Learning',
    minYears: 5,
    maxYears: 19,
    skill: 4,
    wellbeing: -2,
  },
  {
    id: 'library',
    label: 'Read a book',
    description: 'Get lost in a whole other world.',
    icon: '▤',
    group: 'Learning',
    minYears: 5,
    skill: 3,
    wellbeing: 2,
  },
  {
    id: 'football',
    label: 'Play football',
    description: 'A game on the garden pitch.',
    icon: '⚽',
    group: 'Fitness',
    minYears: 6,
    zone: 'garden',
    skill: 2,
    wellbeing: 3,
  },
  {
    id: 'draw',
    label: 'Draw or paint',
    description: 'Develop your own visual language.',
    icon: '✎',
    group: 'Creative',
    minYears: 6,
    skill: 2,
    wellbeing: 4,
  },
  {
    id: 'gardening',
    label: 'Grow something',
    description: 'Care for plants in the public garden.',
    icon: '☘',
    group: 'Wellbeing',
    minYears: 7,
    zone: 'garden',
    skill: 1,
    wellbeing: 4,
  },
  {
    id: 'museum',
    label: 'Visit the local museum',
    description: 'Learn about the city you live in.',
    icon: '⌂',
    group: 'Learning',
    minYears: 7,
    zone: 'market',
    cost: 0,
    skill: 3,
  },
  {
    id: 'music',
    label: 'Practise an instrument',
    description: 'Work patiently at a new piece.',
    icon: '♫',
    group: 'Creative',
    minYears: 8,
    skill: 3,
    wellbeing: 2,
  },
  {
    id: 'science_club',
    label: 'Join a science club',
    description: 'Build something with curious people.',
    icon: '⚙',
    group: 'Learning',
    minYears: 10,
    maxYears: 22,
    skill: 4,
    wellbeing: 1,
  },
  {
    id: 'cook',
    label: 'Cook a meal',
    description: 'Learn a practical skill and eat together.',
    icon: '♨',
    group: 'Family',
    minYears: 10,
    wellbeing: 3,
    skill: 2,
  },
  {
    id: 'volunteer',
    label: 'Community volunteering',
    description: 'Make your neighborhood better.',
    icon: '♡',
    group: 'Friends',
    minYears: 12,
    zone: 'garden',
    wellbeing: 3,
    reputation: 3,
    trustTarget: 'childhood_friend',
    trust: 1,
  },
  {
    id: 'hangout',
    label: 'Spend time with friends',
    description: 'Friendships are more than a progress meter.',
    icon: '☻',
    group: 'Friends',
    minYears: 12,
    wellbeing: 5,
    trustTarget: 'childhood_friend',
    trust: 4,
  },
  {
    id: 'movie',
    label: 'Go to the cinema',
    description: 'A night at the pictures.',
    icon: '▶',
    group: 'Leisure',
    minYears: 13,
    zone: 'market',
    cost: 900,
    wellbeing: 5,
  },
  {
    id: 'shopping',
    label: 'Go shopping',
    description: 'Buy something useful at the market.',
    icon: '▤',
    group: 'Leisure',
    minYears: 13,
    zone: 'market',
    cost: 1200,
    wellbeing: 2,
  },
  {
    id: 'part_time',
    label: 'Part-time market shift',
    description: 'Earn wages after school.',
    icon: '£',
    group: 'Career',
    minYears: 16,
    zone: 'market',
    earnings: 4000,
    skill: 2,
    stress: 3,
    wellbeing: -2,
  },
  {
    id: 'exercise',
    label: 'Workout session',
    description: 'Build strength without extremes.',
    icon: '◆',
    group: 'Fitness',
    minYears: 16,
    zone: 'garden',
    skill: 1,
    wellbeing: 5,
  },
  {
    id: 'cafe_break',
    label: 'Coffee with a friend',
    description: 'Catch up over a quiet drink.',
    icon: '☕',
    group: 'Friends',
    minYears: 16,
    zone: 'cafe',
    cost: 650,
    wellbeing: 3,
    trustTarget: 'childhood_friend',
    trust: 3,
  },
  {
    id: 'therapy',
    label: 'Talk to a counselor',
    description: 'Make room for what is difficult.',
    icon: '♥',
    group: 'Wellbeing',
    minYears: 16,
    zone: 'market',
    cost: 1800,
    wellbeing: 8,
    stress: -10,
  },
  {
    id: 'internship',
    label: 'Work an internship',
    description: 'Learn from a team and earn some cash.',
    icon: '⌘',
    group: 'Career',
    minYears: 18,
    zone: 'market',
    earnings: 6200,
    skill: 4,
    stress: 4,
  },
  {
    id: 'freelance',
    label: 'Freelance assignment',
    description: 'Complete paid work on your own terms.',
    icon: '⌁',
    group: 'Career',
    minYears: 18,
    earnings: 8500,
    skill: 3,
    wellbeing: -2,
    stress: 5,
  },
  {
    id: 'office',
    label: 'Office work shift',
    description: 'Contribute at your current job.',
    icon: '▥',
    group: 'Career',
    minYears: 18,
    zone: 'market',
    requiresEmployment: true,
    earnings: 11000,
    stress: 4,
    skill: 1,
  },
  {
    id: 'restaurant',
    label: 'Dine out',
    description: 'Try the chef’s seasonal special.',
    icon: '♨',
    group: 'Leisure',
    minYears: 18,
    zone: 'market',
    cost: 2400,
    wellbeing: 6,
  },
  {
    id: 'date_night',
    label: 'Dinner date',
    description: 'Take time for your relationship.',
    icon: '♥',
    group: 'Friends',
    minYears: 18,
    zone: 'cafe',
    cost: 2600,
    wellbeing: 5,
    requiresPartner: true,
    trustTarget: 'amelia',
    trust: 4,
  },
  {
    id: 'concert',
    label: 'Attend a concert',
    description: 'A brilliant evening of live music.',
    icon: '♫',
    group: 'Leisure',
    minYears: 18,
    zone: 'market',
    cost: 4000,
    wellbeing: 8,
  },
  {
    id: 'weekend_trip',
    label: 'Weekend adventure',
    description: 'Explore a neighboring city.',
    icon: '✈',
    group: 'Leisure',
    minYears: 18,
    zone: 'market',
    cost: 16000,
    wellbeing: 9,
    skill: 1,
  },
  {
    id: 'call_family',
    label: 'Call family',
    description: 'Remember the people who raised you.',
    icon: '♡',
    group: 'Family',
    minYears: 18,
    wellbeing: 3,
    trustTarget: 'parent_mara',
    trust: 5,
  },
] as const satisfies readonly DailyActivity[];

export type DailyActivityId = (typeof DAILY_ACTIVITIES)[number]['id'];
const byId = new Map<string, DailyActivity>(
  DAILY_ACTIVITIES.map((item) => [item.id, item]),
);
const clamp100 = (n: number) => Math.max(0, Math.min(100, n));
const prefix = (day: number) => 'daily-life:' + day + ':';

export function activitiesForAge(
  ageDays: number,
  zone?: ActivityZone,
): Array<DailyActivity & { id: DailyActivityId }> {
  const years = ageDays / 365;
  // Widen the literal object union to the documented optional-property
  // contract, while preserving the exact union of valid activity IDs.
  const catalog: readonly DailyActivity[] = DAILY_ACTIVITIES;
  return catalog.filter(
    (a) =>
      years >= a.minYears &&
      (a.maxYears === undefined || years < a.maxYears) &&
      (!zone || !a.zone || a.zone === zone),
  ) as Array<DailyActivity & { id: DailyActivityId }>;
}
export function dailyActivitiesUsed(w: World, dayOffset: number): number {
  const marker = prefix(w.day + dayOffset);
  return w.facts.filter((f) => f.startsWith(marker)).length;
}
export function performDailyActivity(
  input: World,
  id: DailyActivityId,
  offset: number,
  zone: ActivityZone,
): World {
  const w = structuredClone(WorldSchema.parse(input));
  if (!Number.isSafeInteger(offset) || offset < 0 || offset > 29)
    throw Error('Invalid in-game day offset.');
  const def = byId.get(id);
  if (!def) throw Error('Unknown activity. Nothing changed.');
  const years = (w.player.ageDays + offset) / 365;
  if (
    years < def.minYears ||
    (def.maxYears !== undefined && years >= def.maxYears)
  )
    throw Error('This activity is not available at your current age.');
  if (def.zone && def.zone !== zone)
    throw Error('Travel to the ' + def.zone + ' before doing this activity.');
  const serial = w.day + offset;
  const marker = prefix(serial) + id;
  if (w.facts.includes(marker))
    throw Error('You already did this activity today.');
  if (dailyActivitiesUsed(w, offset) >= 4)
    throw Error(
      'You are tired after four activities today. Explore or let the clock advance.',
    );
  if (def.requiresEmployment && w.player.career !== 'employed')
    throw Error('You need an employed career before working an office shift.');
  if (
    def.requiresPartner &&
    !['dating', 'engaged', 'married'].some((status) =>
      w.facts.includes('life_relationship:amelia:' + status),
    )
  )
    throw Error(
      'A dinner date requires an existing consenting adult partnership.',
    );
  if ((def.cost ?? 0) > w.player.money && years >= 18)
    throw Error('You cannot afford this activity yet.');
  // Children participate in community-funded/family-paid activities without
  // generating negative personal debt. Household economy is a later system.
  const paid = years >= 18 ? (def.cost ?? 0) : 0;
  w.player.money = Math.max(
    -100000000,
    Math.min(100000000, w.player.money - paid + (def.earnings ?? 0)),
  );
  w.player.wellbeing = clamp100(w.player.wellbeing + (def.wellbeing ?? 0));
  w.player.skill = clamp100(w.player.skill + (def.skill ?? 0));
  if (w.city) {
    w.city.stress = clamp100(w.city.stress + (def.stress ?? 0));
    w.city.reputation = clamp100(w.city.reputation + (def.reputation ?? 0));
  }
  if (def.trustTarget) {
    let r = w.relationships.find((r) => r.characterId === def.trustTarget);
    if (!r) {
      r = { characterId: def.trustTarget, trust: 35, lastContactDay: serial };
      w.relationships.push(r);
    }
    r.trust = clamp100(r.trust + (def.trust ?? 0));
    r.lastContactDay = serial;
  }
  if (w.facts.length > 9400) {
    // Recycle obsolete cooldown markers, never remove story/family facts.
    w.facts = w.facts.filter((f) => !f.startsWith('daily-life:')).slice(-9000);
  }
  w.facts.push(marker);
  record(w, 'simulation', def.label + '. ' + def.description);
  const event = w.history[w.history.length - 1];
  if (event) event.day = serial;
  return WorldSchema.parse(w);
}
