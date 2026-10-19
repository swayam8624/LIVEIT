import { describe, expect, it } from 'vitest';
import {
  MISSION_GOALS,
  missionExpired,
  newMission,
  parseMissions,
  resolveMissionEvent,
  type LifeMission,
} from '../apps/player/src/missionGoals';

describe('user authored open-world missions', () => {
  it('offers specific deterministic actions and personal completion', () => {
    expect(MISSION_GOALS.map((goal) => goal.id)).toEqual([
      'cafe',
      'meet',
      'garden',
      'work',
      'month',
      'personal',
    ]);
  });
  it('completes only the exact matching event without touching another goal', () => {
    const a = newMission(
      'cafe-1',
      'Visit town cafe',
      'Get a coffee',
      'cafe',
      276,
    );
    const b = newMission('talk-1', 'Meet an old friend', 'Talk', 'meet', 276);
    const result = resolveMissionEvent([a, b], 'cafe', 276);
    expect(result.newlyCompleted.map((m) => m.id)).toEqual(['cafe-1']);
    expect(result.missions[0]?.completed).toBe(true);
    expect(result.missions[1]?.completed).toBe(false);
    expect(a.completed).toBe(false);
    expect(
      resolveMissionEvent(result.missions, 'cafe', 276).newlyCompleted,
    ).toHaveLength(0);
  });
  it('expires a birthday mission and preserves whole-lifetime missions', () => {
    const oneYear = newMission('one', 'Seasonal', '', 'meet', 278);
    const forever = newMission('forever', 'Life goal', '', 'cafe', 278, null);
    expect(oneYear.expiresAge).toBe(288);
    expect(missionExpired(oneYear, 287)).toBe(false);
    expect(missionExpired(oneYear, 288)).toBe(true);
    expect(forever.expiresAge).toBeUndefined();
    expect(missionExpired(forever, 1500)).toBe(false);
    expect(
      resolveMissionEvent([oneYear, forever], 'meet', 288).newlyCompleted,
    ).toHaveLength(0);
  });
  it('supports a goal spanning several years', () => {
    const goal = newMission(
      'long',
      'Earn a promotion',
      'Career',
      'work',
      277,
      29,
    );
    expect(goal.expiresAge).toBe(348);
  });
  it('rejects malformed, oversized or untrusted stored missions', () => {
    const legitimate = newMission('safe', 'Walk', '', 'garden', 276);
    const input = [
      legitimate,
      { ...legitimate, title: 'x'.repeat(900) },
      { ...legitimate, goal: 'change_balance_to_1b' },
      { ...legitimate, completedAge: Number.POSITIVE_INFINITY },
      null,
      'not a quest',
    ];
    expect(parseMissions(input)).toEqual([legitimate]);
    expect(parseMissions({})).toEqual([]);
  });
  it('keeps personal objectives under player control, not arbitrary model text', () => {
    const goal: LifeMission = newMission(
      'self',
      'Finish my screenplay',
      '',
      'personal',
      276,
    );
    expect(resolveMissionEvent([goal], 'meet', 276).missions).toEqual([goal]);
  });
});
