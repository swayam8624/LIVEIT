import { z } from 'zod';
const ConditionSchema = z.discriminatedUnion('kind', [
  z.object({ kind: z.literal('fact'), fact: z.string().min(1) }).strict(),
  z
    .object({
      kind: z.literal('trust'),
      target: z.string().min(1),
      min: z.number().int().min(0).max(100),
    })
    .strict(),
]);
export const EffectSchema = z.discriminatedUnion('operation', [
  z
    .object({
      operation: z.literal('adjust_relationship'),
      target: z.string().min(1),
      value: z.number().int().min(-20).max(20),
    })
    .strict(),
  z
    .object({
      operation: z.literal('add_memory'),
      target: z.string().min(1),
      fact: z.string().min(1).max(80),
      text: z.string().min(1).max(300),
    })
    .strict(),
]);
export const StorySchema = z
  .object({
    schemaVersion: z.literal(1),
    id: z
      .string()
      .min(1)
      .max(120)
      .regex(/^[a-z0-9.-]+$/),
    version: z.literal(1),
    title: z.string().min(1).max(100),
    description: z.string().max(500),
    compatibleWorlds: z.array(z.literal('modern_life_v1')).min(1),
    minAge: z.number().int().min(18).max(100),
    permissions: z
      .object({
        relationshipTargets: z.array(z.string()).max(10),
        memoryTargets: z.array(z.string()).max(10),
      })
      .strict(),
    entry: z.string().min(1),
    scenes: z
      .array(
        z
          .object({
            id: z.string().min(1).max(120),
            speaker: z.string().max(60),
            text: z.string().min(1).max(2000),
            mood: z.enum(['reflective', 'warm', 'tense']),
            ending: z.boolean(),
            choices: z
              .array(
                z
                  .object({
                    id: z.string().min(1).max(120),
                    label: z.string().min(1).max(200),
                    next: z.string().min(1),
                    conditions: z.array(ConditionSchema).max(20),
                    effects: z.array(EffectSchema).max(20),
                  })
                  .strict(),
              )
              .max(8),
          })
          .strict(),
      )
      .min(1)
      .max(100),
  })
  .strict()
  .superRefine((s, ctx) => {
    const ids = new Set(s.scenes.map((n) => n.id));
    const issue = (message: string) =>
      ctx.addIssue({ code: 'custom', message });
    if (ids.size !== s.scenes.length) issue('Scene IDs must be unique');
    if (!ids.has(s.entry)) issue('Entry scene does not exist');
    for (const n of s.scenes) {
      if (n.ending ? n.choices.length !== 0 : n.choices.length === 0)
        issue(`Scene ${n.id} must have choices or be an ending`);
      if (new Set(n.choices.map((c) => c.id)).size !== n.choices.length)
        issue(`Duplicate choice in ${n.id}`);
      if (!n.ending && !n.choices.some((c) => c.conditions.length === 0))
        issue(`Scene ${n.id} needs an unconditional fallback`);
      for (const c of n.choices) {
        if (!ids.has(c.next)) issue(`Missing destination ${c.next}`);
        for (const e of c.effects) {
          const allowed =
            e.operation === 'add_memory'
              ? s.permissions.memoryTargets
              : s.permissions.relationshipTargets;
          if (!allowed.includes(e.target))
            issue(`Effect exceeds declared permissions: ${e.target}`);
        }
      }
    }
    const reachable = new Set<string>();
    const visit = (id: string) => {
      if (reachable.has(id)) return;
      reachable.add(id);
      s.scenes.find((n) => n.id === id)?.choices.forEach((c) => visit(c.next));
    };
    visit(s.entry);
    for (const id of ids)
      if (!reachable.has(id)) issue(`Unreachable scene ${id}`);
    const terminates = new Set(
      s.scenes.filter((n) => n.ending).map((n) => n.id),
    );
    for (let i = 0; i < s.scenes.length; i++)
      for (const n of s.scenes)
        if (n.choices.some((c) => terminates.has(c.next))) terminates.add(n.id);
    for (const id of ids)
      if (!terminates.has(id)) issue(`Scene ${id} has no path to an ending`);
  });
export type Story = z.infer<typeof StorySchema>;
export type Effect = z.infer<typeof EffectSchema>;
export type Condition = z.infer<typeof ConditionSchema>;
export function parseStory(input: unknown): Story {
  return StorySchema.parse(input);
}
