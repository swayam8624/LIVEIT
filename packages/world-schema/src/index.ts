import { z } from 'zod';
export const CharacterSchema = z
  .object({
    id: z.string().min(1),
    name: z.string().trim().min(1).max(40),
    pronouns: z.enum(['they/them', 'she/her', 'he/him']),
    ageDays: z.number().int().nonnegative(),
    wellbeing: z.number().int().min(0).max(100),
    skill: z.number().int().min(0).max(100),
    career: z.enum(['seeking', 'employed']),
    money: z.number().int().min(-100000000).max(100000000),
  })
  .strict();
export const RelationshipSchema = z
  .object({
    characterId: z.string().min(1),
    trust: z.number().int().min(0).max(100),
    lastContactDay: z.number().int().nonnegative(),
  })
  .strict();
export const MemorySchema = z
  .object({
    id: z.string(),
    day: z.number().int().nonnegative(),
    subject: z.string(),
    text: z.string().max(300),
    fact: z.string().min(1),
  })
  .strict();
export const EventSchema = z
  .object({
    id: z.string(),
    day: z.number().int().nonnegative(),
    kind: z.enum(['creation', 'simulation', 'choice']),
    text: z.string().max(500),
  })
  .strict();
export const ProgressSchema = z
  .object({
    storyId: z.string(),
    version: z.literal(1),
    sceneId: z.string(),
    completed: z.boolean(),
    choices: z.array(z.string()).max(1000),
  })
  .strict();
export const WorldSchema = z
  .object({
    schemaVersion: z.literal(1),
    timelineId: z.string().min(1),
    worldId: z.literal('modern_life_v1'),
    day: z.number().int().nonnegative(),
    player: CharacterSchema,
    relationships: z.array(RelationshipSchema).max(100),
    memories: z.array(MemorySchema).max(10000),
    history: z.array(EventSchema).max(20000),
    facts: z.array(z.string()).max(10000),
    progress: z.array(ProgressSchema).max(100),
  })
  .strict()
  .superRefine((w, ctx) => {
    if (
      new Set(w.relationships.map((r) => r.characterId)).size !==
      w.relationships.length
    )
      ctx.addIssue({
        code: 'custom',
        message: 'Duplicate relationship identity',
      });
    if (new Set(w.progress.map((p) => p.storyId)).size !== w.progress.length)
      ctx.addIssue({ code: 'custom', message: 'Duplicate story progress' });
  });
export type Character = z.infer<typeof CharacterSchema>;
export type World = z.infer<typeof WorldSchema>;
export function record(
  world: World,
  kind: World['history'][number]['kind'],
  text: string,
): void {
  world.history.push({
    id: `${world.timelineId}:event:${world.history.length}`,
    day: world.day,
    kind,
    text,
  });
}
