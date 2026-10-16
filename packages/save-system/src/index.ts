import { z } from 'zod';
import { WorldSchema, type World } from '@living/world-schema';
export const SaveSchema = z
  .object({
    version: z.literal(1),
    active: z.enum(['life', 'story']),
    // Optional for compatibility with existing v1 saves. Identifies the active
    // narrative independently of timeline (official or locally imported).
    activeStoryId: z.string().min(1).max(120).optional(),
    /** Leaves active narrative progress intact, but does not auto-open on reload. */
    sceneDismissed: z.boolean().optional(),
    life: WorldSchema,
    story: WorldSchema.nullable(),
  })
  .strict()
  .superRefine((s, ctx) => {
    if (s.story?.timelineId === s.life.timelineId)
      ctx.addIssue({ code: 'custom', message: 'Timelines must be isolated' });
    if (s.active === 'story' && !s.story)
      ctx.addIssue({
        code: 'custom',
        message: 'Active story timeline is missing',
      });
  });
export type Save = z.infer<typeof SaveSchema>;
export interface SaveStorage {
  getItem(key: string): Promise<string | null>;
  setItem(key: string, value: string): Promise<void>;
}
export const SAVE_KEY = 'living-universe.save.v1';
export function encodeSave(save: Save): string {
  return JSON.stringify(SaveSchema.parse(save));
}
export function decodeSave(text: string): Save {
  return SaveSchema.parse(JSON.parse(text));
}
export async function loadSave(storage: SaveStorage): Promise<Save | null> {
  const text = await storage.getItem(SAVE_KEY);
  return text === null ? null : decodeSave(text);
}
export async function writeSave(
  storage: SaveStorage,
  save: Save,
): Promise<void> {
  await storage.setItem(SAVE_KEY, encodeSave(save));
}
/** Branching copies state but deliberately preserves an independent identity. */
export function branchWorld(world: World, timelineId: string): World {
  if (timelineId === world.timelineId)
    throw new Error('A branch needs its own identity');
  return WorldSchema.parse({ ...structuredClone(world), timelineId });
}
