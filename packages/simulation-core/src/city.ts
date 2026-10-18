import {
  CityStateSchema,
  WorldSchema,
  record,
  type CityState,
  type CareerPath,
  type District,
  type World,
} from '@living/world-schema';

/** Pure, reproducible authorable events. No LLMs, clocks or network dependencies. */
export type CityEffect = {
  money?: number;
  wellbeing?: number;
  skill?: number;
  stress?: number;
  reputation?: number;
  connections?: number;
  trust?: { characterId: 'amelia' | 'noah'; amount: number };
};
export type CityChoice = {
  id: string;
  label: string;
  consequence: string;
  effects: CityEffect;
};
export type CityOpportunity = {
  id: string;
  title: string;
  description: string;
  district: District;
  minDay: number;
  minSkill?: number;
  minReputation?: number;
  minConnections?: number;
  requireFact?: string;
  choices: readonly [CityChoice, CityChoice];
};
export const DISTRICTS: ReadonlyArray<{
  id: District;
  title: string;
  tagline: string;
  activities: string;
}> = [
  {
    id: 'riverside',
    title: 'Riverside',
    tagline: 'The past is never quite finished',
    activities: 'Café, friendships, quiet evenings',
  },
  {
    id: 'university',
    title: 'North Campus',
    tagline: 'Where every door needs a key',
    activities: 'Study, workshops, research',
  },
  {
    id: 'market',
    title: 'Old Market',
    tagline: 'Every opportunity has a price',
    activities: 'Jobs, trade, entrepreneurship',
  },
  {
    id: 'studio',
    title: 'The Arts Quarter',
    tagline: 'Make something people remember',
    activities: 'Art, performance, collaboration',
  },
  {
    id: 'gardens',
    title: 'The Commons',
    tagline: 'A city needs more than ambition',
    activities: 'Exercise, volunteering, community',
  },
];

/**
 * Hand-authored open-ended opportunities with balanced and sometimes costly
 * choices. Effects use integer pence, bounded stats and explicit trust targets.
 */
export const CITY_OPPORTUNITIES: readonly CityOpportunity[] = [
  {
    id: 'lost_wallet',
    title: 'The forgotten wallet',
    district: 'market',
    minDay: 2,
    description:
      'A leather wallet lies under a market stall. Inside is enough cash to cover a week of expenses, and an address.',
    choices: [
      {
        id: 'return',
        label: 'Find its owner',
        consequence: 'The owner thanks you. Word gets around the market.',
        effects: { reputation: 6, connections: 3, stress: -2 },
      },
      {
        id: 'keep',
        label: 'Take the cash',
        consequence:
          'Your rent becomes easier. Looking people in the eye does not.',
        effects: { money: 12000, reputation: -8, stress: 6 },
      },
    ],
  },
  {
    id: 'bookshop_posters',
    title: 'Posters in the rain',
    district: 'riverside',
    minDay: 3,
    description:
      'Amelia is hanging posters for a bookshop opening. The sky is turning dark and she has dozens left.',
    choices: [
      {
        id: 'help',
        label: 'Help, even if it takes the evening',
        consequence: 'You both return soaked and laughing.',
        effects: {
          trust: { characterId: 'amelia', amount: 9 },
          stress: -3,
          connections: 2,
        },
      },
      {
        id: 'donate',
        label: 'Pay a printer to handle it',
        consequence:
          'The posters are delivered. Amelia appreciates the gesture, though you barely spoke.',
        effects: {
          money: -5500,
          trust: { characterId: 'amelia', amount: 3 },
          reputation: 1,
        },
      },
    ],
  },
  {
    id: 'campus_workshop',
    title: 'An open workshop',
    district: 'university',
    minDay: 3,
    description:
      'A lecturer invites you to a difficult workshop. You can learn something new, but it means skipping a paid shift.',
    choices: [
      {
        id: 'attend',
        label: 'Take the workshop',
        consequence:
          'The assignment humbles you. You leave knowing more than you arrived with.',
        effects: { skill: 7, money: -3500, stress: 5 },
      },
      {
        id: 'shift',
        label: 'Take the paid shift instead',
        consequence:
          'A practical decision. The workshop will not wait for you.',
        effects: { money: 6000, skill: 1, stress: 1 },
      },
    ],
  },
  {
    id: 'gallery_wall',
    title: 'One empty gallery wall',
    district: 'studio',
    minDay: 4,
    description:
      'A small gallery offers you a chance to show your work, provided you cover the materials yourself.',
    choices: [
      {
        id: 'create',
        label: 'Make something original',
        consequence:
          'Your work attracts a few strangers. One remembers your name.',
        effects: { money: -4500, skill: 4, reputation: 5, connections: 3 },
      },
      {
        id: 'volunteer',
        label: 'Help the gallery instead',
        consequence: 'You meet the people keeping this place alive.',
        effects: { reputation: 3, connections: 5, stress: -3 },
      },
    ],
  },
  {
    id: 'park_cleanup',
    title: 'A park worth keeping',
    district: 'gardens',
    minDay: 4,
    description:
      'The local community is cleaning a neglected public garden. The organizers need extra hands.',
    choices: [
      {
        id: 'join',
        label: 'Spend the morning helping',
        consequence: 'Nobody pays you, but several neighbors now know you.',
        effects: { connections: 6, wellbeing: 4, reputation: 4, money: -700 },
      },
      {
        id: 'donate',
        label: 'Contribute to equipment',
        consequence: 'The volunteers can buy new gloves and tools.',
        effects: { money: -2500, reputation: 3, stress: -1 },
      },
    ],
  },
  {
    id: 'quiet_investor',
    title: 'The quiet investor',
    district: 'market',
    minDay: 6,
    minSkill: 20,
    description:
      'Someone offers to invest in your side project, but wants most of the creative control.',
    choices: [
      {
        id: 'decline',
        label: 'Keep your independence',
        consequence: 'Progress is slower, but the project remains yours.',
        effects: { skill: 3, reputation: 2, stress: 3 },
      },
      {
        id: 'accept',
        label: 'Accept the funding',
        consequence: 'The project accelerates; your freedom becomes smaller.',
        effects: { money: 24000, stress: 9, reputation: -2 },
      },
    ],
  },
  {
    id: 'unpaid_internship',
    title: 'A prestigious offer',
    district: 'market',
    minDay: 7,
    description:
      'A celebrated studio offers an unpaid placement, promising connections but little else.',
    choices: [
      {
        id: 'negotiate',
        label: 'Ask for fair compensation',
        consequence: 'They reluctantly agree to a smaller paid project.',
        effects: { money: 8500, reputation: 3, connections: 2, stress: 3 },
      },
      {
        id: 'decline',
        label: 'Walk away',
        consequence: 'You decide your work is worth something.',
        effects: { reputation: 1, stress: -4 },
      },
    ],
  },
  {
    id: 'friend_in_trouble',
    title: 'A difficult phone call',
    district: 'riverside',
    minDay: 8,
    description:
      'Noah calls just after midnight. He needs help moving out of a difficult living situation.',
    choices: [
      {
        id: 'show_up',
        label: 'Go help him',
        consequence: 'You spend the night carrying boxes. He will remember it.',
        effects: {
          trust: { characterId: 'noah', amount: 12 },
          wellbeing: -4,
          connections: 3,
        },
      },
      {
        id: 'send_cab',
        label: 'Pay for transport',
        consequence: 'He gets home safely. You promise to talk tomorrow.',
        effects: {
          money: -3400,
          trust: { characterId: 'noah', amount: 4 },
          stress: 1,
        },
      },
    ],
  },
  {
    id: 'campus_debate',
    title: 'An argument in public',
    district: 'university',
    minDay: 8,
    description:
      'At a campus debate, someone misrepresents your research. Everyone is listening.',
    choices: [
      {
        id: 'respond',
        label: 'Respond with evidence',
        consequence: 'You win respect from some and hostility from others.',
        effects: { reputation: 5, skill: 2, stress: 7 },
      },
      {
        id: 'disengage',
        label: 'Discuss it privately later',
        consequence:
          'There is no victory on stage, but a serious conversation follows.',
        effects: { connections: 4, stress: -2 },
      },
    ],
  },
  {
    id: 'stolen_credit',
    title: 'Your idea, their presentation',
    district: 'studio',
    minDay: 9,
    description:
      'A collaborator presents your idea as their own. Your work is praised under another name.',
    choices: [
      {
        id: 'confront',
        label: 'Confront them respectfully',
        consequence: 'You regain credit, but the partnership may not survive.',
        effects: { reputation: 5, stress: 8, connections: -3 },
      },
      {
        id: 'document',
        label: 'Record evidence and move on',
        consequence: 'You secure proof and focus on building something better.',
        effects: { skill: 3, stress: 3, reputation: 1 },
      },
    ],
  },
  {
    id: 'late_invoice',
    title: 'The invoice that never arrived',
    district: 'market',
    minDay: 10,
    description:
      'A client refuses to pay. You can chase the money or protect your time.',
    choices: [
      {
        id: 'pursue',
        label: 'Challenge the payment',
        consequence: 'After hard negotiation, most of the invoice is paid.',
        effects: { money: 14000, stress: 8, reputation: 2 },
      },
      {
        id: 'release',
        label: 'Move on to another job',
        consequence: 'The money is gone. Your energy returns.',
        effects: { wellbeing: 4, stress: -5, skill: 1 },
      },
    ],
  },
  {
    id: 'street_performance',
    title: 'An unexpected duet',
    district: 'studio',
    minDay: 11,
    description:
      'A street performer asks you to join in front of a small crowd.',
    choices: [
      {
        id: 'join',
        label: 'Take the stage',
        consequence:
          'You stumble, recover, and win a spontaneous round of applause.',
        effects: { wellbeing: 6, reputation: 3, connections: 4 },
      },
      {
        id: 'watch',
        label: 'Stay and support the performers',
        consequence: 'Sometimes participating means simply showing up.',
        effects: { wellbeing: 3, money: -1200, connections: 2 },
      },
    ],
  },
  {
    id: 'rent_increase',
    title: 'A letter from your landlord',
    district: 'riverside',
    minDay: 12,
    description:
      'Your landlord announces a rent increase. Other tenants are just as worried.',
    choices: [
      {
        id: 'organize',
        label: 'Work with other tenants',
        consequence: 'Together, you negotiate a fairer renewal.',
        effects: { connections: 5, reputation: 3, stress: 7 },
      },
      {
        id: 'pay',
        label: 'Accept the extra cost',
        consequence: 'You keep your apartment and avoid conflict.',
        effects: { money: -13000, stress: 2 },
      },
    ],
  },
  {
    id: 'morning_run',
    title: 'The five-kilometer dare',
    district: 'gardens',
    minDay: 13,
    description:
      'A local running club invites you to a weekend event. You have barely slept all week.',
    choices: [
      {
        id: 'go',
        label: 'Join at your own pace',
        consequence:
          'The air is cold, the city is beautiful, and you finish tired but proud.',
        effects: { wellbeing: 8, stress: -6, connections: 2 },
      },
      {
        id: 'rest',
        label: 'Sleep in and recover',
        consequence: 'You needed the rest more than the applause.',
        effects: { wellbeing: 5, stress: -5 },
      },
    ],
  },
  {
    id: 'mentor_offer',
    title: 'A mentor takes an interest',
    district: 'university',
    minDay: 14,
    minSkill: 28,
    description:
      'A visiting researcher offers an introduction that could change your career.',
    choices: [
      {
        id: 'prepare',
        label: 'Prepare carefully and meet',
        consequence:
          'Your ideas survive difficult questioning. New doors open.',
        effects: { skill: 4, connections: 7, reputation: 3, stress: 4 },
      },
      {
        id: 'delay',
        label: 'Ask for another month',
        consequence:
          'You choose preparation over urgency. The offer remains uncertain.',
        effects: { skill: 3, stress: -3 },
      },
    ],
  },
  {
    id: 'job_interview',
    title: 'An interview across town',
    district: 'market',
    minDay: 16,
    minSkill: 25,
    description:
      'A growing company offers you a difficult interview at short notice.',
    choices: [
      {
        id: 'go',
        label: 'Take your best shot',
        consequence:
          'You make an impression. Even without a guarantee, you build momentum.',
        effects: { reputation: 4, connections: 4, stress: 6 },
      },
      {
        id: 'prepare_more',
        label: 'Ask to reschedule',
        consequence: 'They agree to another date. You have time to improve.',
        effects: { skill: 4, stress: 2 },
      },
    ],
  },
  {
    id: 'bookshop_launch',
    title: 'Opening night',
    district: 'riverside',
    minDay: 18,
    description:
      'Amelia’s bookshop opens tonight. There is a line at the door, and she looks overwhelmed.',
    choices: [
      {
        id: 'stay',
        label: 'Stay late and help close up',
        consequence: 'She introduces you as someone she trusts.',
        effects: {
          trust: { characterId: 'amelia', amount: 10 },
          reputation: 4,
          stress: 1,
        },
      },
      {
        id: 'celebrate',
        label: 'Bring a thoughtful gift',
        consequence: 'She keeps your note beside the register.',
        effects: {
          money: -2500,
          trust: { characterId: 'amelia', amount: 6 },
          wellbeing: 3,
        },
      },
    ],
  },
  {
    id: 'community_budget',
    title: 'The neighborhood budget',
    district: 'gardens',
    minDay: 20,
    minConnections: 8,
    description:
      'Residents vote on how to improve the district. You can advocate for something that matters.',
    choices: [
      {
        id: 'speak',
        label: 'Make a public case',
        consequence: 'Your proposal gains supporters, and critics.',
        effects: { reputation: 7, stress: 6, connections: 3 },
      },
      {
        id: 'organize',
        label: 'Bring people into agreement',
        consequence: 'You build a quieter, more durable coalition.',
        effects: { connections: 8, reputation: 3, stress: 2 },
      },
    ],
  },
  {
    id: 'new_collaboration',
    title: 'The midnight project',
    district: 'studio',
    minDay: 22,
    minConnections: 5,
    description:
      'Two creators invite you to collaborate on a project that may never make money.',
    choices: [
      {
        id: 'commit',
        label: 'Make the project together',
        consequence: 'The work is difficult but your creative world expands.',
        effects: { skill: 5, connections: 6, stress: 6, money: -4000 },
      },
      {
        id: 'advise',
        label: 'Offer advice instead',
        consequence: 'You keep your schedule while maintaining the friendship.',
        effects: { connections: 3, stress: -2 },
      },
    ],
  },
  {
    id: 'old_letter',
    title: 'A letter without a return address',
    district: 'riverside',
    minDay: 24,
    description:
      'An envelope arrives containing a photograph and an unfinished apology.',
    choices: [
      {
        id: 'reply',
        label: 'Write back honestly',
        consequence: 'You make peace with something you cannot change.',
        effects: { wellbeing: 7, stress: -4 },
      },
      {
        id: 'archive',
        label: 'Put it away for now',
        consequence: 'Some questions can wait until you are ready.',
        effects: { wellbeing: 2, stress: -1 },
      },
    ],
  },
] as const;

export function initialCityState(): CityState {
  return CityStateSchema.parse({
    district: 'riverside',
    careerPath: 'undecided',
    reputation: 35,
    stress: 24,
    connections: 12,
    housing: 'shared_flat',
    milestones: [],
    opportunities: [],
    resolved: [],
  });
}
export function cityState(world: World): CityState {
  return world.city ?? initialCityState();
}
const clamp = (n: number) => Math.max(0, Math.min(100, Math.round(n)));
function eligible(w: World, item: CityOpportunity): boolean {
  const city = cityState(w);
  return (
    w.day >= item.minDay &&
    w.player.skill >= (item.minSkill ?? 0) &&
    city.reputation >= (item.minReputation ?? 0) &&
    city.connections >= (item.minConnections ?? 0) &&
    (!item.requireFact || w.facts.includes(item.requireFact)) &&
    !city.resolved.includes(item.id) &&
    !city.opportunities.some((o) => o.id === item.id)
  );
}
/** Called inside an already cloned world as simulated time advances. */
export function tickCity(
  input: World,
  activity: 'work' | 'study' | 'rest' | 'socialize',
): void {
  const c = input.city ?? (input.city = initialCityState());
  c.stress = clamp(
    c.stress +
      (activity === 'work'
        ? 2
        : activity === 'study'
          ? 1
          : activity === 'rest'
            ? -5
            : -2),
  );
  if (activity === 'socialize') c.connections = clamp(c.connections + 1);
  // Do not create hundreds of unplayed events or trigger every day.
  if (input.day % 3 !== 0) return;
  scheduleCityOpportunity(input);
}
/** Schedule a small bounded opportunity pool, also usable by annual ageing. */
export function scheduleCityOpportunity(input: World): void {
  const c = input.city ?? (input.city = initialCityState());
  c.opportunities = c.opportunities.filter((o) => o.expiresDay >= input.day);
  if (c.opportunities.length >= 2) return;
  const available = CITY_OPPORTUNITIES.filter((o) => eligible(input, o));
  if (!available.length) return;
  const index =
    (Math.floor(input.day / 3) + input.player.skill) % available.length;
  const chosen = available[index]!;
  c.opportunities.push({
    id: chosen.id,
    offeredDay: input.day,
    expiresDay: input.day + 14,
  });
  record(
    input,
    'simulation',
    `New opportunity: ${chosen.title}. Visit the city to decide.`,
  );
}
export function availableCityOpportunities(w: World): CityOpportunity[] {
  return cityState(w)
    .opportunities.filter((entry) => entry.expiresDay >= w.day)
    .map((entry) => CITY_OPPORTUNITIES.find((item) => item.id === entry.id))
    .filter((x): x is CityOpportunity => Boolean(x));
}
export function visitDistrict(input: World, district: District): World {
  const w = structuredClone(WorldSchema.parse(input));
  if (!DISTRICTS.some((d) => d.id === district))
    throw new Error('Unknown Bellweather district');
  const c = w.city ?? (w.city = initialCityState());
  c.district = district;
  record(
    w,
    'simulation',
    `Visited ${DISTRICTS.find((d) => d.id === district)!.title}.`,
  );
  return WorldSchema.parse(w);
}
export function chooseCareer(input: World, path: CareerPath): World {
  const w = structuredClone(WorldSchema.parse(input));
  const c = w.city ?? (w.city = initialCityState());
  if (path === 'undecided') throw new Error('Choose a field of work');
  if (c.careerPath !== 'undecided' && c.careerPath !== path)
    throw new Error(
      'Changing career paths requires a later career-transition event',
    );
  c.careerPath = path;
  c.milestones.push(`career:${path}`);
  record(w, 'simulation', `Chose a direction in ${path.replace('_', ' ')}.`);
  return WorldSchema.parse(w);
}
export function resolveCityOpportunity(
  input: World,
  eventId: string,
  choiceId: string,
): World {
  const w = structuredClone(WorldSchema.parse(input));
  const c = w.city ?? (w.city = initialCityState());
  const pending = c.opportunities.find(
    (item) => item.id === eventId && item.expiresDay >= w.day,
  );
  if (!pending) throw new Error('This opportunity is no longer available');
  const event = CITY_OPPORTUNITIES.find((item) => item.id === eventId);
  if (!event) throw new Error('Unknown opportunity');
  const choice = event.choices.find((option) => option.id === choiceId);
  if (!choice) throw new Error('Choice unavailable');
  const e = choice.effects;
  w.player.money = Math.max(
    -100000000,
    Math.min(100000000, w.player.money + (e.money ?? 0)),
  );
  w.player.wellbeing = clamp(w.player.wellbeing + (e.wellbeing ?? 0));
  w.player.skill = clamp(w.player.skill + (e.skill ?? 0));
  c.stress = clamp(c.stress + (e.stress ?? 0));
  c.reputation = clamp(c.reputation + (e.reputation ?? 0));
  c.connections = clamp(c.connections + (e.connections ?? 0));
  if (e.trust) {
    const person = w.relationships.find(
      (r) => r.characterId === e.trust!.characterId,
    );
    if (person) {
      person.trust = clamp(person.trust + e.trust.amount);
      person.lastContactDay = w.day;
    }
  }
  c.opportunities = c.opportunities.filter((x) => x.id !== event.id);
  c.resolved.push(event.id);
  c.milestones.push(`event:${event.id}:${choice.id}`);
  const fact = `city:${event.id}:${choice.id}`;
  if (!w.facts.includes(fact)) w.facts.push(fact);
  record(w, 'choice', `${event.title} — ${choice.consequence}`);
  w.memories.push({
    id: `${w.timelineId}:city-memory:${event.id}`,
    day: w.day,
    subject: 'bellweather',
    text: choice.consequence,
    fact,
  });
  return WorldSchema.parse(w);
}
