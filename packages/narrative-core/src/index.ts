import { WorldSchema, record, type World } from '@living/world-schema';
import { parseStory, type Story, type Condition } from '@living/story-schema';
import { applyConsequences } from '@living/consequence-engine';
export function conditionMet(w: World, c: Condition): boolean {
  return c.kind === 'fact'
    ? w.facts.includes(c.fact)
    : (w.relationships.find((r) => r.characterId === c.target)?.trust ?? -1) >=
        c.min;
}
export function currentScene(w: World, s: Story) {
  const p = w.progress.find((p) => p.storyId === s.id);
  if (p && p.version !== s.version) throw new Error('Story version mismatch');
  const scene = s.scenes.find((n) => n.id === (p?.sceneId ?? s.entry));
  if (!scene) throw new Error('Saved scene is missing');
  return scene;
}
export function startStory(input: World, authored: Story): World {
  const s = parseStory(authored);
  const w = structuredClone(WorldSchema.parse(input));
  if (
    !s.compatibleWorlds.includes(w.worldId) ||
    Math.floor(w.player.ageDays / 365) < s.minAge
  )
    throw new Error('Character is incompatible with this story');
  for (const target of [
    ...s.permissions.relationshipTargets,
    ...s.permissions.memoryTargets,
  ])
    if (!w.relationships.some((r) => r.characterId === target))
      throw new Error(`Missing cast relationship: ${target}`);
  if (!w.progress.some((p) => p.storyId === s.id))
    w.progress.push({
      storyId: s.id,
      version: s.version,
      sceneId: s.entry,
      completed: currentScene(w, s).ending,
      choices: [],
    });
  currentScene(w, s);
  return WorldSchema.parse(w);
}
/** Resolves an available choice once, including effects and progress, as one transaction. */
export function choose(input: World, authored: Story, choiceId: string): World {
  const s = parseStory(authored);
  let w = startStory(input, s);
  const p = w.progress.find((p) => p.storyId === s.id)!;
  if (p.completed) throw new Error('This story is complete');
  const scene = currentScene(w, s);
  const c = scene.choices.find((c) => c.id === choiceId);
  if (!c || !c.conditions.every((condition) => conditionMet(w, condition)))
    throw new Error('Choice is unavailable');
  w = applyConsequences(w, s, c.effects);
  const progress = w.progress.find((p) => p.storyId === s.id)!;
  progress.sceneId = c.next;
  progress.choices.push(`${scene.id}:${c.id}`);
  progress.completed = currentScene(w, s).ending;
  record(w, 'choice', `${s.title}: ${c.label}`);
  return WorldSchema.parse(w);
}
