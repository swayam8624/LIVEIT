import { describe, expect, it } from 'vitest';
import {
  DAILY_ACTIVITIES, activitiesForAge, dailyActivitiesUsed, performDailyActivity,
  createBirthWorld, createWorld, actOnRelationship,
} from '@living/simulation-core';
import { encodeSave, decodeSave } from '@living/save-system';

describe('daily Free Life activities', () => {
  it('exposes 31 unique activities across meaningful life categories', () => {
    expect(DAILY_ACTIVITIES).toHaveLength(31);
    expect(new Set(DAILY_ACTIVITIES.map(a=>a.id)).size).toBe(31);
    expect(new Set(DAILY_ACTIVITIES.map(a=>a.group)).size).toBeGreaterThanOrEqual(8);
  });

  it('begins with safe infant activities and no access to paid adult jobs', () => {
    const born=createBirthWorld('Elena','activities-born');
    const ids=activitiesForAge(born.player.ageDays).map(a=>a.id);
    expect(ids).toContain('family_cuddle');
    expect(ids).not.toContain('freelance');
    expect(ids).not.toContain('date_night');
    const next=performDailyActivity(born,'family_cuddle',0,'street');
    expect(next.player.money).toBe(0);
    expect(next.player.wellbeing).toBe(90);
    expect(next.relationships[0]!.trust).toBe(90);
    expect(next.history.at(-1)?.text).toContain('Cuddle');
    expect(born.player.wellbeing).toBe(85);
    expect(()=>performDailyActivity(born,'freelance',0,'market')).toThrow(/age/);
  });

  it('respects physical location and prevents replaying a completed action', () => {
    const w=createWorld();
    expect(()=>performDailyActivity(w,'concert',0,'street')).toThrow(/Travel/);
    const trip=performDailyActivity(w,'concert',0,'market');
    expect(trip.player.money).toBe(w.player.money-4000);
    expect(trip.player.wellbeing).toBe(80);
    expect(()=>performDailyActivity(trip,'concert',0,'market')).toThrow(/already/);
    expect(decodeSave(encodeSave({version:1,active:'life',life:trip,story:null})).life).toEqual(trip);
  });

  it('allows four activities per simulated day, resets next day, no money exploits', () => {
    const w=createWorld();
    const day0=performDailyActivity(w,'freelance',0,'street');
    const day1=performDailyActivity(day0,'library',0,'street');
    const day2=performDailyActivity(day1,'cook',0,'street');
    const day3=performDailyActivity(day2,'call_family',0,'street');
    expect(dailyActivitiesUsed(day3,0)).toBe(4);
    expect(()=>performDailyActivity(day3,'draw',0,'street')).toThrow(/four activities/);
    expect(dailyActivitiesUsed(day3,1)).toBe(0);
    const after=performDailyActivity(day3,'draw',1,'street');
    expect(dailyActivitiesUsed(after,1)).toBe(1);
    expect(after.player.money).toBe(w.player.money+8500);
  });

  it('friends and parents are persistent relationships rather than transient UI counts', () => {
    const w=createBirthWorld('Noor');
    w.player.ageDays=6*365;
    const friend=performDailyActivity(w,'meet_classmate',0,'street');
    expect(friend.relationships.find(r=>r.characterId==='childhood_friend')?.trust).toBe(41);
    expect(friend.relationships.find(r=>r.characterId==='childhood_friend')?.lastContactDay).toBe(0);
    expect(friend.player.wellbeing).toBe(88);
  });

  it('protects adult dating against unsupported partnership and insufficent funds', () => {
    const w=createWorld();
    expect(()=>performDailyActivity(w,'date_night',0,'cafe')).toThrow(/partnership/);
    w.player.money=200;
    expect(()=>performDailyActivity(w,'concert',0,'market')).toThrow(/afford/);
    w.player.money=180000;
    let courting=w;
    for(let i=0;i<3;i++) courting=actOnRelationship(courting,'befriend',i);
    courting=actOnRelationship(courting,'ask_date',3);
    const outing=performDailyActivity(courting,'date_night',3,'cafe');
    expect(outing.relationships.find(r=>r.characterId==='amelia')!.trust)
      .toBeGreaterThan(courting.relationships.find(r=>r.characterId==='amelia')!.trust);
  });

  it('never runs malformed IDs, regions or day offsets', () => {
    const w=createWorld();
    expect(()=>performDailyActivity(w,'spoof-money' as 'freelance',0,'market')).toThrow(/Unknown/);
    expect(()=>performDailyActivity(w,'freelance',31,'market')).toThrow(/offset/);
    expect(()=>performDailyActivity(w,'football',0,'market')).toThrow(/Travel/);
  });
});
