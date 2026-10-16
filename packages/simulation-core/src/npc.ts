import { record, type NPCLife, type World } from '@living/world-schema';

/**
 * Sparse off-screen character beats. NPCs continue living even when the
 * player doesn't open a scene. No continuous loop, cloud LLM, or per-second
 * simulation is needed. The same day/state always yields the same history.
 */
export function initialNPCLives(): NPCLife[] {
  return [
    { characterId: 'amelia', occupation: 'Bookseller', currentGoal: 'Prepare a welcoming neighborhood bookshop', mood: 'anxious', milestones: [] },
    { characterId: 'noah', occupation: 'Hospitality temp', currentGoal: 'Find steady work and an apartment', mood: 'hopeful', milestones: [] },
  ];
}

type NPCBeat = {
  day: number;
  who: 'amelia' | 'noah';
  occupation: string;
  goal: string;
  mood: NPCLife['mood'];
  milestone: string;
  notice: string;
};
export const NPC_BEATS: readonly NPCBeat[] = [
  { day: 5, who: 'noah', occupation: 'Café assistant', goal: 'Learn enough to keep a regular position', mood: 'busy', milestone: 'first_shift', notice: 'Noah started a regular shift at the market café.' },
  { day: 9, who: 'amelia', occupation: 'Independent bookseller', goal: 'Finish decorating the storefront', mood: 'hopeful', milestone: 'lease_signed', notice: 'Amelia signed the lease for her first bookshop.' },
  { day: 13, who: 'noah', occupation: 'Café assistant', goal: 'Save enough for a deposit', mood: 'restless', milestone: 'flat_search', notice: 'Noah is looking for a better apartment.' },
  { day: 18, who: 'amelia', occupation: 'Bookshop owner', goal: 'Survive opening night', mood: 'anxious', milestone: 'shop_open', notice: 'The lights came on at Amelia’s bookshop for opening night.' },
  { day: 23, who: 'noah', occupation: 'Café supervisor', goal: 'Build a stable career', mood: 'hopeful', milestone: 'promoted', notice: 'Noah took on responsibility for the café’s evening team.' },
  { day: 27, who: 'amelia', occupation: 'Bookshop owner', goal: 'Keep the shop running beyond its first month', mood: 'busy', milestone: 'first_month', notice: 'Amelia is learning what running a bookshop really costs.' },
  { day: 35, who: 'noah', occupation: 'Café supervisor', goal: 'Move into a new apartment', mood: 'content', milestone: 'new_flat', notice: 'Noah finally found a place to call his own.' },
  { day: 42, who: 'amelia', occupation: 'Bookshop owner', goal: 'Create a community reading evening', mood: 'content', milestone: 'reading_night', notice: 'Amelia’s bookshop hosted its first community reading.' },
  { day: 56, who: 'noah', occupation: 'Café supervisor', goal: 'Apply to hospitality school', mood: 'hopeful', milestone: 'night_classes', notice: 'Noah enrolled in evening hospitality classes.' },
  { day: 70, who: 'amelia', occupation: 'Bookshop owner', goal: 'Publish a local writers’ anthology', mood: 'hopeful', milestone: 'anthology', notice: 'Amelia is collecting stories for an anthology of Bellweather writers.' },
];

/** Mutates the simulation's already-cloned world; bounded, event-driven state. */
export function tickNPCs(world: World): void {
  const people = world.npcLives ?? (world.npcLives = initialNPCLives());
  const beat = NPC_BEATS.find(item => item.day === world.day);
  if (!beat) return;
  const person = people.find(item => item.characterId === beat.who);
  if (!person || person.milestones.includes(beat.milestone)) return;
  person.occupation = beat.occupation;
  person.currentGoal = beat.goal;
  person.mood = beat.mood;
  person.milestones.push(beat.milestone);
  record(world, 'simulation', beat.notice);
}
