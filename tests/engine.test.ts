import { describe, it, expect } from 'vitest';
import { createWorld, advanceLife, DISTRICTS, CITY_OPPORTUNITIES, availableCityOpportunities, chooseCareer, visitDistrict, resolveCityOpportunity } from '@living/simulation-core';
import {
  choose,
  startStory,
  currentScene,
  conditionMet,
} from '@living/narrative-core';
import { applyConsequences } from '@living/consequence-engine';
import {
  encodeSave,
  decodeSave,
  loadSave,
  writeSave,
  branchWorld,
  type Save,
} from '@living/save-system';
import { parseStory } from '@living/story-schema';
import { reunion, bookshop } from '@living/content';
const copy = () => structuredClone(reunion);
describe('deterministic life simulation', () => {
  it('creates a valid life and rejects blank names', () => {
    expect(createWorld().player.ageDays).toBe(23 * 365);
    expect(() => createWorld(' ')).toThrow();
  });
  it('produces the same world from identical inputs without mutating the input', () => {
    const initial = createWorld();
    const a = advanceLife(initial, 'work', 7);
    expect(a).toEqual(advanceLife(initial, 'work', 7));
    expect(initial.day).toBe(0);
    expect(a.day).toBe(7);
    expect(a.player.money).toBe(216900);
    expect(a.player.career).toBe('employed');
  });
  it('applies daily costs across long intervals', () => {
    expect(advanceLife(createWorld(), 'rest', 30).player.money).toBe(96000);
  });
  it('keeps bounded stats and ages by elapsed days', () => {
    const w = advanceLife(createWorld(), 'study', 30);
    expect(w.player.skill).toBe(100);
    expect(w.player.ageDays).toBe(23 * 365 + 30);
    expect(advanceLife(createWorld(), 'work', 30).player.wellbeing).toBe(0);
  });
  it('rejects invalid intervals and runtime activity values', () => {
    for (const days of [0, -1, 1.2, 31, NaN])
      expect(() => advanceLife(createWorld(), 'rest', days)).toThrow();
    expect(() => advanceLife(createWorld(), 'invalid' as 'rest')).toThrow();
  });
  it('updates NPC relationships and decays neglected ties on weekly ticks', () => {
    const w = advanceLife(createWorld(), 'socialize', 7);
    expect(w.relationships[1]!.trust).toBe(76);
    expect(w.relationships[0]!.trust).toBe(34);
  });
});
describe('shared narrative consequences', () => {
  it('persists a story choice in the associated life and journal', () => {
    let life = startStory(createWorld(), reunion);
    life = choose(life, reunion, 'apologize');
    expect(life.relationships[0]!.trust).toBe(47);
    expect(life.facts).toContain('apologized');
    life = choose(life, reunion, 'truth');
    expect(life.relationships[0]!.trust).toBe(57);
    expect(life.progress[0]!.completed).toBe(true);
    const saved = decodeSave(
      encodeSave({ version: 1, active: 'life', life, story: null }),
    );
    expect(saved.life).toEqual(life);
    expect(saved.life.memories).toHaveLength(2);
    expect(() => choose(life, reunion, 'truth')).toThrow('complete');
  });
  it('reaches each authored ending and preserves distinct facts', () => {
    for (const [first, second, end] of [
      ['apologize', 'truth', 'reconnected'],
      ['guarded', 'repair', 'slow'],
      ['guarded', 'leave', 'apart'],
    ]) {
      const w = choose(
        choose(createWorld(), reunion, first!),
        reunion,
        second!,
      );
      expect(currentScene(w, reunion).id).toBe(end);
      expect(w.memories.length).toBeGreaterThan(0);
    }
  });
  it('can save and resume in the middle of dialogue', () => {
    const w = choose(createWorld(), reunion, 'listen');
    const save = decodeSave(
      encodeSave({ version: 1, active: 'life', life: w, story: null }),
    );
    expect(currentScene(save.life, reunion).id).toBe('listening');
    expect(choose(save.life, reunion, 'support').progress[0]!.completed).toBe(
      true,
    );
  });
  it('enforces conditional choices at execution, not only in the UI', () => {
    const s = copy();
    s.scenes[0]!.choices[0]!.conditions = [
      { kind: 'trust', target: 'amelia', min: 80 },
    ];
    expect(() => choose(createWorld(), s, 'apologize')).toThrow('unavailable');
    expect(
      conditionMet(createWorld(), {
        kind: 'fact',
        fact: 'university_attended',
      }),
    ).toBe(true);
    expect(
      conditionMet(createWorld(), { kind: 'trust', target: 'missing', min: 0 }),
    ).toBe(false);
  });
  it('rejects invalid and stale choices without changing input', () => {
    const w = choose(createWorld(), reunion, 'listen');
    const before = structuredClone(w);
    expect(() => choose(w, reunion, 'apologize')).toThrow();
    expect(w).toEqual(before);
  });
  it('isolates a standalone story and allows continuing life after its ending', () => {
    const life = createWorld();
    let story = branchWorld(life, 'standalone');
    story = choose(choose(story, reunion, 'apologize'), reunion, 'truth');
    story = advanceLife(story, 'rest');
    expect(life.relationships[0]!.trust).toBe(35);
    expect(story.relationships[0]!.trust).toBe(57);
    expect(story.day).toBe(1);
    expect(life.memories).toHaveLength(0);
    expect(() => branchWorld(life, 'main')).toThrow();
  });
  it('rejects an incompatible protagonist or missing cast', () => {
    const w = createWorld();
    w.player.ageDays = 10 * 365;
    expect(() => startStory(w, reunion)).toThrow('incompatible');
    const noCast = createWorld();
    noCast.relationships = [];
    expect(() => startStory(noCast, reunion)).toThrow('Missing cast');
  });
  it('is atomic when one effect in a transaction is unauthorized', () => {
    const w = createWorld();
    const before = structuredClone(w);
    expect(() =>
      applyConsequences(w, reunion, [
        { operation: 'adjust_relationship', target: 'amelia', value: 10 },
        { operation: 'adjust_relationship', target: 'noah', value: 10 },
      ]),
    ).toThrow('Unauthorized');
    expect(w).toEqual(before);
  });
  it('clamps trust and rejects excessive requested changes', () => {
    const w = createWorld();
    w.relationships[0]!.trust = 99;
    expect(
      applyConsequences(w, reunion, [
        { operation: 'adjust_relationship', target: 'amelia', value: 20 },
      ]).relationships[0]!.trust,
    ).toBe(100);
    expect(() =>
      applyConsequences(w, reunion, [
        { operation: 'adjust_relationship', target: 'amelia', value: 1000 },
      ]),
    ).toThrow();
  });
});
describe('untrusted story validation', () => {
  it('rejects unknown operations and arbitrary code fields', () => {
    const s = copy();
    Object.assign(s.scenes[0]!.choices[0]!.effects[0]!, {
      operation: 'execute',
      code: 'delete save',
    });
    expect(() => parseStory(s)).toThrow();
  });
  it('rejects missing destinations, unreachable nodes, cycles without endings, and duplicate IDs', () => {
    const a = copy();
    a.scenes[0]!.choices[0]!.next = 'missing';
    expect(() => parseStory(a)).toThrow();
    const b = copy();
    b.scenes.push({ ...b.scenes.at(-1)!, id: 'unreachable' });
    expect(() => parseStory(b)).toThrow();
    const c = copy();
    c.scenes[0]!.choices.forEach((choice) => (choice.next = 'arrival'));
    expect(() => parseStory(c)).toThrow();
    const d = copy();
    d.scenes.push(d.scenes[0]!);
    expect(() => parseStory(d)).toThrow();
  });
  it('rejects undeclared targets and graphs with no unconditional fallback', () => {
    const s = copy();
    s.permissions.relationshipTargets = [];
    expect(() => parseStory(s)).toThrow();
    const t = copy();
    t.scenes[0]!.choices.forEach(
      (c) => (c.conditions = [{ kind: 'fact', fact: 'impossible' }]),
    );
    expect(() => parseStory(t)).toThrow();
  });
  it('requires an ending or available choices on every scene', () => {
    const s = copy();
    s.scenes[0]!.choices = [];
    expect(() => parseStory(s)).toThrow();
  });
});
describe('versioned persistence', () => {
  it('round trips through the actual async storage contract', async () => {
    const data = new Map<string, string>();
    const storage = {
      getItem: async (k: string) => data.get(k) ?? null,
      setItem: async (k: string, v: string) => {
        data.set(k, v);
      },
    };
    expect(await loadSave(storage)).toBeNull();
    const s: Save = {
      version: 1,
      active: 'life',
      life: createWorld(),
      story: null,
    };
    await writeSave(storage, s);
    expect(await loadSave(storage)).toEqual(s);
  });
  it('rejects corrupt saves, unsupported versions, missing active timelines, and conflicting identities', () => {
    expect(() => decodeSave('{broken')).toThrow();
    const s = { version: 1, active: 'life', life: createWorld(), story: null };
    expect(() => decodeSave(JSON.stringify({ ...s, version: 2 }))).toThrow();
    expect(() =>
      decodeSave(JSON.stringify({ ...s, active: 'story' })),
    ).toThrow();
    expect(() =>
      decodeSave(JSON.stringify({ ...s, story: createWorld() })),
    ).toThrow();
  });
  it('reports storage failures rather than claiming success', async () => {
    const storage = {
      getItem: async () => null,
      setItem: async () => {
        throw new Error('disk full');
      },
    };
    await expect(
      writeSave(storage, {
        version: 1,
        active: 'life',
        life: createWorld(),
        story: null,
      }),
    ).rejects.toThrow('disk full');
  });
  it('rejects unknown world fields and duplicate character references', () => {
    const w = createWorld();
    w.relationships.push(w.relationships[0]!);
    expect(() =>
      encodeSave({ version: 1, active: 'life', life: w, story: null }),
    ).toThrow();
  });
});

describe('Creator Studio to local player story bridge', () => {
  it('accepts a JSON-exported story and persists its effects in the main life', () => {
    const authored = copy();
    authored.id = 'creator.cafe-encounter';
    authored.title = 'An Evening to Remember';
    authored.scenes[0]!.text = 'You recognize an old friend across the room.';
    const parsed = parseStory(JSON.parse(JSON.stringify(authored)));

    const original = createWorld('Alex Morgan');
    const started = startStory(original, parsed);
    const firstChoice = choose(started, parsed, 'apologize');
    const ending = choose(firstChoice, parsed, 'truth');
    const restored = decodeSave(
      encodeSave({ version: 1, active: 'life', life: ending, story: null }),
    );

    expect(original.relationships[0]!.trust).toBe(35);
    expect(restored.life.relationships[0]!.trust).toBe(57);
    expect(restored.life.progress[0]!.storyId).toBe('creator.cafe-encounter');
    expect(restored.life.progress[0]!.completed).toBe(true);
    expect(restored.life.memories).toHaveLength(2);
  });

  it('does not permit imported stories to execute arbitrary commands or effects', () => {
    const unsafe = {
      ...copy(),
      id: 'creator.unsafe',
      injectedCode: 'process.exit(0)',
    };
    expect(() => parseStory(unsafe)).toThrow();

    const unauthorized = copy();
    unauthorized.id = 'creator.unauthorized';
    unauthorized.scenes[0]!.choices[0]!.effects[0] = {
      operation: 'adjust_relationship',
      target: 'noah',
      value: 20,
    };
    expect(() => parseStory(unauthorized)).toThrow('permissions');
  });
});

describe('imported narrative persistence and compatibility', () => {
  it('loads legacy version-one saves without a narrative ID', () => {
    const legacy = {
      version: 1 as const,
      active: 'life' as const,
      life: createWorld(),
      story: null,
    };
    const restored = decodeSave(JSON.stringify(legacy));
    expect(restored.activeStoryId).toBeUndefined();
    expect(restored).toEqual(legacy);
  });

  it('preserves an imported story identifier and in-progress scene across a full save round trip', () => {
    const imported = copy();
    imported.id = 'creator.a-new-moment';
    const incomplete = choose(createWorld(), imported, 'listen');
    expect(currentScene(incomplete, imported).id).toBe('listening');
    const checkpoint: Save = {
      version: 1,
      active: 'life',
      activeStoryId: imported.id,
      life: incomplete,
      story: null,
    };
    const restored = decodeSave(encodeSave(checkpoint));
    expect(restored.activeStoryId).toBe(imported.id);
    expect(currentScene(restored.life, imported).id).toBe('listening');
    expect(
      choose(restored.life, imported, 'support').relationships[0]?.trust,
    ).toBe(51);
  });

  it('rejects invalid active narrative identifiers', () => {
    const data: Save = {
      version: 1,
      active: 'life',
      life: createWorld(),
      story: null,
    };
    expect(() =>
      decodeSave(JSON.stringify({ ...data, activeStoryId: '' })),
    ).toThrow();
  });
});

describe('Bellweather living city (deterministic open simulation)', () => {
  it('initializes a rich city without breaking legacy save compatibility', () => {
    const fresh = createWorld();
    expect(fresh.city?.district).toBe('riverside');
    expect(fresh.city?.careerPath).toBe('undecided');
    expect(fresh.city?.reputation).toBe(35);
    const legacy = structuredClone(fresh);
    delete legacy.city;
    const restored = decodeSave(encodeSave({
      version: 1, active: 'life', life: legacy, story: null,
    }));
    expect(restored.life.city).toBeUndefined();
    expect(visitDistrict(restored.life, 'market').city?.district).toBe('market');
  });
  it('contains twenty original opportunities, five districts and no duplicated IDs', () => {
    expect(CITY_OPPORTUNITIES.length).toBeGreaterThanOrEqual(20);
    expect(DISTRICTS).toHaveLength(5);
    expect(new Set(CITY_OPPORTUNITIES.map(e => e.id)).size).toBe(CITY_OPPORTUNITIES.length);
    for (const event of CITY_OPPORTUNITIES) {
      expect(event.choices).toHaveLength(2);
      expect(event.choices[0].id).not.toBe(event.choices[1].id);
      expect(event.choices[0].consequence.length).toBeGreaterThan(5);
    }
  });
  it('schedules reproducible events as time advances, without waiting in real time', () => {
    const original = createWorld();
    const first = advanceLife(original, 'study', 3);
    const second = advanceLife(original, 'study', 3);
    expect(first).toEqual(second);
    expect(availableCityOpportunities(first).length).toBeGreaterThan(0);
    expect(original.city?.opportunities).toHaveLength(0);
    expect(first.city?.stress).toBeGreaterThan(original.city!.stress);
  });
  it('validates a choice and records atomic permanent consequences', () => {
    const before = advanceLife(createWorld(), 'rest', 3);
    const next = availableCityOpportunities(before)[0]!;
    expect(next).toBeDefined();
    const after = resolveCityOpportunity(before, next.id, next.choices[0].id);
    expect(after.city?.resolved).toContain(next.id);
    expect(after.facts).toContain(`city:${next.id}:${next.choices[0].id}`);
    expect(after.memories.at(-1)?.subject).toBe('bellweather');
    expect(after.history.at(-1)?.kind).toBe('choice');
    expect(before.city!.resolved).toHaveLength(0);
    expect(() => resolveCityOpportunity(after, next.id, next.choices[0].id)).toThrow();
    expect(() => resolveCityOpportunity(before, next.id, 'execute_code')).toThrow('Choice unavailable');
    expect(() => resolveCityOpportunity(before, 'invented', 'anything')).toThrow();
  });
  it('lets players choose a career field, and prevents accidental rewrites', () => {
    const fresh = createWorld();
    const direction = chooseCareer(fresh, 'technology');
    expect(direction.city?.careerPath).toBe('technology');
    expect(fresh.city?.careerPath).toBe('undecided');
    expect(() => chooseCareer(direction, 'creative')).toThrow('career-transition');
    expect(() => chooseCareer(fresh, 'undecided')).toThrow();
  });
  it('persists an opportunity decision and a named district across JSON saves', () => {
    const original = advanceLife(createWorld(), 'study', 3);
    const event = availableCityOpportunities(original)[0]!;
    const changed = visitDistrict(
      resolveCityOpportunity(original, event.id, event.choices[1].id),
      'university',
    );
    const restored = decodeSave(
      encodeSave({ version: 1, active: 'life', life: changed, story: null }),
    );
    expect(restored.life.city?.district).toBe('university');
    expect(restored.life.city?.resolved).toContain(event.id);
    expect(restored.life.player.money).toBe(changed.player.money);
  });
});

describe('Bookshop chapter and shared life continuity', () => {
  it('provides a valid second playable chapter with three endings', () => {
    expect(bookshop.scenes).toHaveLength(11);
    expect(bookshop.scenes.filter(s => s.ending)).toHaveLength(3);
    expect(bookshop.entry).toBe('doorway');
  });
  it('remembers earlier reconciliation and persists the bookshop outcome', () => {
    const reunited = choose(choose(createWorld(), reunion, 'apologize'), reunion, 'truth');
    const daysLater = advanceLife(reunited, 'rest', 7);
    const opening = startStory(daysLater, bookshop);
    let w = choose(opening, bookshop, 'early');
    w = choose(w, bookshop, 'joke');
    w = choose(w, bookshop, 'after');
    const restored = decodeSave(encodeSave({
      version: 1, active: 'life', life: w, story: null, activeStoryId: bookshop.id,
    }));
    expect(restored.life.progress.find(p => p.storyId === bookshop.id)?.completed).toBe(true);
    expect(restored.life.progress.find(p => p.storyId === reunion.id)?.completed).toBe(true);
    expect(restored.life.facts).toContain('bookshop_early');
    expect(restored.life.facts).toContain('bookshop_afterhours');
    expect(restored.life.relationships[0]!.trust).toBeGreaterThan(daysLater.relationships[0]!.trust);
  });
  it('allows the original standalone story without mutating main life memories', () => {
    const mainLife = createWorld();
    const alone = choose(choose(createWorld('Alex', 'story.bookshop'), bookshop, 'look'), bookshop, 'remember');
    const completed = choose(alone, bookshop, 'goodbye');
    expect(currentScene(completed, bookshop).id).toBe('separate');
    expect(mainLife.memories).toHaveLength(0);
    expect(mainLife.progress).toHaveLength(0);
  });
});

describe('NPC autonomy and career/district modifiers', () => {
  it('advances independent NPC lives with stable goals and accomplishments', () => {
    const initial = createWorld();
    expect(initial.npcLives).toHaveLength(2);
    const after = advanceLife(initial, 'rest', 23);
    const amelia = after.npcLives?.find(n => n.characterId === 'amelia')!;
    const noah = after.npcLives?.find(n => n.characterId === 'noah')!;
    expect(amelia.occupation).toBe('Bookshop owner');
    expect(amelia.milestones).toContain('shop_open');
    expect(noah.occupation).toBe('Café supervisor');
    expect(noah.milestones).toContain('promoted');
    expect(initial.npcLives?.[0]?.milestones).toHaveLength(0);
    expect(after).toEqual(advanceLife(initial, 'rest', 23));
  });
  it('restores NPC state lazily for an older save', () => {
    const oldWorld = createWorld();
    delete oldWorld.npcLives;
    const updated = advanceLife(oldWorld, 'rest', 5);
    expect(updated.npcLives?.find(p => p.characterId === 'noah')?.occupation).toBe('Café assistant');
  });
  it('makes choosing an occupation a genuine economic decision', () => {
    const base = advanceLife(createWorld(), 'work', 8);
    const focused = advanceLife(chooseCareer(createWorld(), 'technology'), 'work', 8);
    expect(focused.player.money).toBeGreaterThan(base.player.money);
    expect(focused.player.career).toBe('employed');
    expect(focused.city?.careerPath).toBe('technology');
  });
  it('makes neighborhood location change skill and wellbeing progression', () => {
    const ordinary = advanceLife(createWorld(), 'study', 4);
    const campus = advanceLife(visitDistrict(createWorld(), 'university'), 'study', 4);
    expect(campus.player.skill).toBe(ordinary.player.skill + 4);
    const rested = advanceLife(visitDistrict(createWorld(), 'gardens'), 'rest', 1);
    expect(rested.player.wellbeing).toBe(84);
  });
});
