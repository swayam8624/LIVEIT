import { WorldSchema, type World } from '@living/world-schema';
import {
  parseStory,
  EffectSchema,
  type Effect,
  type Story,
} from '@living/story-schema';
/** Validate every effect before producing a new state; input is never mutated. */
export function applyConsequences(
  input: World,
  authored: Story,
  effects: Effect[],
): World {
  const story = parseStory(authored);
  const w = structuredClone(WorldSchema.parse(input));
  if (
    !story.compatibleWorlds.includes(w.worldId) ||
    Math.floor(w.player.ageDays / 365) < story.minAge
  )
    throw new Error('Incompatible timeline');
  for (const raw of effects) {
    const effect = EffectSchema.parse(raw);
    const targets =
      effect.operation === 'add_memory'
        ? story.permissions.memoryTargets
        : story.permissions.relationshipTargets;
    if (
      !targets.includes(effect.target) ||
      !w.relationships.some((r) => r.characterId === effect.target)
    )
      throw new Error('Unauthorized consequence target');
    if (effect.operation === 'adjust_relationship') {
      const r = w.relationships.find((r) => r.characterId === effect.target)!;
      r.trust = Math.min(100, Math.max(0, r.trust + effect.value));
      r.lastContactDay = w.day;
    } else {
      w.memories.push({
        id: `${w.timelineId}:memory:${w.memories.length}`,
        day: w.day,
        subject: effect.target,
        text: effect.text,
        fact: effect.fact,
      });
      if (!w.facts.includes(effect.fact)) w.facts.push(effect.fact);
    }
  }
  return WorldSchema.parse(w);
}
