import { describe, it, expect } from 'vitest';
import {
  createBirthWorld,
  createWorld,
  advanceCalendarMonth,
  skipToAge,
  performSchoolAction,
  applyForJob,
} from '@living/simulation-core';
import { decodeSave, encodeSave } from '@living/save-system';

describe('iteration three: school, household and transitions', () => {
  it('begins with separate parent household budget, while baby owns no cash', () => {
    const born = createBirthWorld('Mia', 'family-1');
    expect(born.player.ageDays).toBe(0);
    expect(born.player.money).toBe(0);
    expect(born.household?.balancePence).toBe(240000);
    expect(born.school?.phase).toBe('not_started');
    const month = advanceCalendarMonth(born);
    expect(month.household?.balancePence).toBe(295000);
    expect(month.household?.lastSettledMonth).toBe(1);
    expect(month.player.money).toBe(0);
    expect(born.household?.balancePence).toBe(240000);
  });
  it('enrolls in primary at age 5, secondary at 13 and finishes at 18', () => {
    const born = createBirthWorld('Eli', 'student-2');
    const primary = skipToAge(born, 5);
    expect(primary.school?.phase).toBe('primary');
    const secondary = skipToAge(primary, 13);
    expect(secondary.school?.phase).toBe('secondary');
    const graduate = skipToAge(secondary, 18);
    expect(graduate.school?.phase).toBe('graduated');
    expect(graduate.school?.graduatedWith).not.toBeNull();
    expect(graduate.facts).toContain('education:school_completed');
  });
  it('school choices change outcomes, relationships and discipline', () => {
    const primary = skipToAge(createBirthWorld('Jules', 'student-3'), 5);
    const studying = performSchoolAction(primary, 'study', 0);
    expect(studying.school?.grade).toBeGreaterThan(primary.school!.grade);
    expect(studying.school?.studySessions).toBe(1);
    expect(() => performSchoolAction(studying, 'study', 0)).toThrow('already');
    const absent = performSchoolAction(studying, 'skip_class', 1);
    expect(absent.school!.discipline).toBeGreaterThan(
      studying.school!.discipline,
    );
    expect(absent.school!.attendance).toBeLessThan(studying.school!.attendance);
    const befriended = performSchoolAction(absent, 'make_friend', 2);
    expect(
      befriended.relationships.some(
        (r) => r.characterId === 'childhood_friend',
      ),
    ).toBe(true);
    expect(
      decodeSave(
        encodeSave({
          version: 1,
          active: 'life',
          life: befriended,
          story: null,
        }),
      ).life,
    ).toEqual(befriended);
  });
  it('prevents under-age employment and school actions beyond graduation', () => {
    const born = createBirthWorld('Alex', 'career-age');
    expect(() => performSchoolAction(born, 'study', 0)).toThrow('ages 5');
    expect(() => applyForJob(born, 'technology')).toThrow('18');
    const graduate = skipToAge(born, 18);
    expect(() => performSchoolAction(graduate, 'study', 0)).toThrow('ages 5');
    const applied = applyForJob(graduate, 'technology');
    expect(applied.city?.employment?.stage).toBe('applied');
  });
  it('legacy adult saves remain readable and do not gain invented childhood savings', () => {
    const legacy = createWorld('Morgan', 'old-save');
    const next = advanceCalendarMonth(legacy);
    expect(next.school).toBeUndefined();
    expect(next.household).toBeUndefined();
    expect(next.player.ageDays).toBeGreaterThan(legacy.player.ageDays);
  });
});
