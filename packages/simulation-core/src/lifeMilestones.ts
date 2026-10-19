import { record, type World } from '@living/world-schema';

/** Life milestones are separate from expensive world simulation. A milestone
 * is a *once-only* save transition at a calendar month boundary. Skipping
 * childhood replays the same events in order, so it cannot erase early life.
 *
 * These are authored fictional life events, not medical development claims.
 * Everyone develops differently; the full game will support optional and
 * delayed milestones and different family circumstances.
 */
export type LifeMilestone = Readonly<{
  month: number;
  id: string;
  title: string;
  narration: string;
  skill?: number;
  wellbeing?: number;
  familyTrust?: number;
}>;
export const LIFE_MILESTONES: readonly LifeMilestone[] = [
  {
    month: 1,
    id: 'settling_home',
    title: 'A World of Voices',
    narration:
      'You learn the rhythm of your home. Mara and Eli recognize the sounds that mean you need them.',
    wellbeing: 1,
    familyTrust: 2,
  },
  {
    month: 3,
    id: 'recognizing_faces',
    title: 'Familiar Faces',
    narration:
      'You begin recognizing the people who return to your side each morning.',
    familyTrust: 3,
  },
  {
    month: 6,
    id: 'first_laughter',
    title: 'An Unexpected Laugh',
    narration:
      'A funny sound makes you laugh, then makes everyone else laugh too.',
    wellbeing: 3,
  },
  {
    month: 9,
    id: 'curiosity',
    title: 'A Curious New World',
    narration:
      'The corners of each room become interesting, and you try to reach everything.',
    skill: 1,
  },
  {
    month: 12,
    id: 'first_birthday',
    title: 'Your First Birthday',
    narration:
      'The family gathers for a small cake, a few photographs, and a year of being together.',
    wellbeing: 4,
    familyTrust: 2,
  },
  {
    month: 24,
    id: 'toddler_years',
    title: 'Growing Independence',
    narration:
      'You want to do more things yourself, even when the world feels enormous.',
    skill: 2,
  },
  {
    month: 36,
    id: 'early_questions',
    title: 'Questions About Everything',
    narration:
      'You are full of questions about the people, streets, and sky around you.',
    skill: 2,
  },
  {
    month: 60,
    id: 'first_school',
    title: 'Starting School',
    narration: 'A school bag hangs beside the door, ready for its first day.',
    skill: 2,
    familyTrust: 2,
  },
  {
    month: 72,
    id: 'first_friendships',
    title: 'Finding Your People',
    narration: 'Friendship starts becoming something you can choose and build.',
    wellbeing: 2,
  },
  {
    month: 120,
    id: 'discovering_passions',
    title: 'Discovering Your Interests',
    narration: 'Your hobbies become more than a way to fill a quiet afternoon.',
    skill: 3,
  },
  {
    month: 156,
    id: 'teenage_years',
    title: 'Growing Beyond Childhood',
    narration:
      'School, friendships, and family expectations begin to pull in different directions.',
    skill: 1,
  },
  {
    month: 192,
    id: 'more_independence',
    title: 'Growing Responsibility',
    narration:
      'You are old enough to seek small opportunities, make mistakes, and own their consequences.',
    skill: 2,
  },
  {
    month: 216,
    id: 'legal_adulthood',
    title: 'A New Chapter',
    narration:
      'You turn eighteen. The wider world opens, with work, travel, independence, and adult relationships.',
    wellbeing: 2,
  },
  {
    month: 252,
    id: 'young_adulthood',
    title: 'Your Own Direction',
    narration: 'You begin to define what a successful life means for yourself.',
    skill: 2,
  },
  {
    month: 360,
    id: 'turning_thirty',
    title: 'Another Decade',
    narration: 'At thirty, old plans compete with the life you actually built.',
    wellbeing: 1,
  },
  {
    month: 480,
    id: 'turning_forty',
    title: 'Reconsidering Priorities',
    narration:
      'At forty, some choices have deep roots; others can still change.',
    wellbeing: 1,
  },
  {
    month: 600,
    id: 'turning_fifty',
    title: 'The Weight of Experience',
    narration:
      'You carry memories of victories and wrong turns into another decade.',
    skill: 2,
  },
  {
    month: 780,
    id: 'senior_years',
    title: 'An Older Chapter',
    narration:
      'The world continues to change; you still decide how to spend your years.',
    wellbeing: 1,
  },
  {
    month: 960,
    id: 'turning_eighty',
    title: 'Many Years of Stories',
    narration:
      'Eight decades of people, places, and days have made a life worth remembering.',
    wellbeing: 1,
  },
];

const clamp = (n: number) => Math.max(0, Math.min(100, n));

/** Mutates the *cloned, validated* world owned by the monthly tick only.
 * Never accept a model's generated milestone IDs as authority.
 */
export function applyLifeMilestones(w: World): string[] {
  if (!w.facts.includes('life_origin:born_in_bellweather')) return [];
  const month = Math.floor((w.player.ageDays * 12) / 365);
  const happened: string[] = [];
  for (const entry of LIFE_MILESTONES) {
    if (entry.month > month) continue;
    const marker = 'life.milestone:' + entry.id;
    if (w.facts.includes(marker)) continue;
    w.facts.push(marker);
    w.player.wellbeing = clamp(w.player.wellbeing + (entry.wellbeing ?? 0));
    w.player.skill = clamp(w.player.skill + (entry.skill ?? 0));
    const parent = w.relationships.find((r) => r.characterId === 'parent_mara');
    if (parent && entry.familyTrust) {
      parent.trust = clamp(parent.trust + entry.familyTrust);
      parent.lastContactDay = w.day;
    }
    record(
      w,
      'simulation',
      'LIFE MILESTONE — ' + entry.title + ': ' + entry.narration,
    );
    if (w.memories.length < 9990)
      w.memories.push({
        id: w.timelineId + ':milestone:' + entry.id,
        day: w.day,
        subject: 'player',
        fact: marker,
        text: entry.title + ': ' + entry.narration,
      });
    happened.push(entry.id);
  }
  return happened;
}
