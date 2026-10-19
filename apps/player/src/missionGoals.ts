/**
 * One save timeline, unlimited user-authored goals, no AI authority.
 *
 * NPC language models can suggest mission descriptions but completion is
 * performed only by whitelisted, replayable gameplay events below.
 */
export const MISSION_GOALS = [
  { id: 'cafe', label: 'Enter the café', hint: 'Walk through the café door' },
  { id: 'meet', label: 'Talk to Amelia', hint: 'Stand near Amelia and talk' },
  { id: 'garden', label: 'Explore the garden', hint: 'Visit Bellweather garden' },
  { id: 'work', label: 'Talk about work', hint: 'Ask Amelia about work or jobs' },
  { id: 'month', label: 'Live another month', hint: 'Keep playing until a month passes' },
  { id: 'personal', label: 'Personal objective', hint: 'Mark completed yourself' },
] as const;

export type MissionGoal = (typeof MISSION_GOALS)[number]['id'];
export type MissionEvent = Exclude<MissionGoal, 'personal'>;
export type LifeMission = Readonly<{
  id: string;
  title: string;
  description: string;
  createdAge: number;
  expiresAge?: number;
  goal?: MissionGoal;
  completed: boolean;
  completedAge?: number;
}>;

/** Strictly read local sidecar content without importing unknown machine data. */
export function parseMissions(input: unknown): LifeMission[] {
  if (!Array.isArray(input)) return [];
  return input.filter((value): value is LifeMission => {
    if (!value || typeof value !== 'object') return false;
    const m = value as Partial<LifeMission>;
    return typeof m.id === 'string' && m.id.length <= 120 &&
      typeof m.title === 'string' && m.title.length > 0 && m.title.length <= 80 &&
      typeof m.description === 'string' && m.description.length <= 500 &&
      Number.isSafeInteger(m.createdAge) && m.createdAge! >= 0 &&
      (m.expiresAge === undefined ||
        (Number.isSafeInteger(m.expiresAge) && m.expiresAge >= 0)) &&
      (m.goal === undefined || MISSION_GOALS.some(g => g.id === m.goal)) &&
      typeof m.completed === 'boolean' &&
      (m.completedAge === undefined ||
        (Number.isSafeInteger(m.completedAge) && m.completedAge >= 0));
  }).slice(-500);
}

export function missionExpired(m: LifeMission, ageMonths: number): boolean {
  return !m.completed && m.expiresAge !== undefined && ageMonths >= m.expiresAge;
}

/** A transcript is never a transaction; only committed world events count. */
export function resolveMissionEvent(
  missions: readonly LifeMission[], event: MissionEvent, ageMonths: number,
): { missions: LifeMission[]; newlyCompleted: LifeMission[] } {
  const completed: LifeMission[] = [];
  const output = missions.map(m => {
    if (m.completed || missionExpired(m, ageMonths) || m.goal !== event) return m;
    const next = { ...m, completed: true, completedAge: ageMonths };
    completed.push(next);
    return next;
  });
  return { missions: output, newlyCompleted: completed };
}

/**
 * Do not make an algorithm invent hidden quest goals from arbitrary prose.
 * The user chooses the gameplay objective explicitly. Manual objectives
 * remain possible, with completion visible and controlled by the player.
 */
export function newMission(
  id: string, title: string, description: string, goal: MissionGoal,
  ageMonths: number, throughAge?: number | null,
): LifeMission {
  const clean = title.trim().slice(0, 80);
  if (!clean) throw new Error('A mission must have a title.');
  if (!Number.isSafeInteger(ageMonths) || ageMonths < 0) throw new Error('Invalid age');
  const birthday = (Math.floor(ageMonths / 12) + 1) * 12;
  return {
    id,
    title: clean,
    description: description.trim().slice(0, 500),
    createdAge: ageMonths,
    // The user can choose an extended age-bound mission.
    expiresAge: throughAge === null ? undefined :
      (throughAge !== undefined && throughAge * 12 > ageMonths ? throughAge * 12 : birthday),
    goal,
    completed: false,
  };
}
