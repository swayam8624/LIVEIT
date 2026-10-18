import { z } from 'zod';
import { AppearanceSchema } from './appearance';

/**
 * Versioned, renderer-neutral visual resources. All player and NPC cosmetics
 * remain independent of stats, and installed packs are validated as a graph.
 */
const ResourceId = z.string().regex(/^[a-z][a-z0-9_-]*(?:[./][a-z0-9_-]+)+$/);
const Digest = z.string().regex(/^[0-9a-f]{64}$/);
const SafeRelativePath = z
  .string()
  .min(1)
  .max(250)
  .regex(/^[a-zA-Z0-9_./-]+$/)
  .refine(
    (value) => !value.startsWith('/') && !value.split('/').includes('..'),
    'Unsafe asset path',
  );

export const VisualAssetKindSchema = z.enum([
  'rig',
  'rig-part',
  'outfit',
  'prop',
  'architecture',
  'location',
  'material',
  'shader',
  'vfx',
  'animation',
  'background',
  'audio',
]);
export const VisualAssetSchema = z
  .object({
    id: ResourceId,
    kind: VisualAssetKindSchema,
    tier: z.enum(['core', 'downloadable']),
    revision: z.number().int().positive(),
    dependencies: z.array(ResourceId).max(64).default([]),
    style: z.string().min(1),
    slot: z.string().optional(),
    tags: z.array(z.string().min(1)).max(32).default([]),
    license: z
      .object({
        spdx: z.string().min(1),
        author: z.string().min(1),
        source: z.string().min(1),
        attribution: z.string().optional(),
      })
      .strict(),
    implementation: z.discriminatedUnion('kind', [
      z
        .object({
          kind: z.literal('procedural'),
          shader: ResourceId.optional(),
          parameters: z.record(
            z.string(),
            z.union([z.number().finite(), z.string(), z.boolean()]),
          ),
        })
        .strict(),
      z
        .object({
          kind: z.literal('external'),
          path: SafeRelativePath,
          sha256: Digest,
          bytes: z.number().int().positive(),
          format: z.enum(['png', 'webp', 'ktx2', 'glb', 'ogg', 'wav', 'spv']),
        })
        .strict(),
    ]),
  })
  .strict();
export type VisualAsset = z.infer<typeof VisualAssetSchema>;

export const VisualPackSchema = z
  .object({
    schemaVersion: z.literal(1),
    id: ResourceId,
    revision: z.number().int().positive(),
    title: z.string().min(1),
    style: z.string().min(1),
    minGameVersion: z.string().regex(/^\d+\.\d+\.\d+$/),
    dependencies: z.array(ResourceId).default([]),
    assets: z.array(VisualAssetSchema).min(1).max(5000),
  })
  .strict()
  .superRefine((pack, ctx) => {
    const ids = new Set<string>();
    for (const [index, asset] of pack.assets.entries()) {
      if (ids.has(asset.id))
        ctx.addIssue({
          code: 'custom',
          path: ['assets', index, 'id'],
          message: 'Duplicate asset id',
        });
      ids.add(asset.id);
    }
    const edges = new Map<string, string[]>();
    for (const [index, asset] of pack.assets.entries()) {
      if (
        asset.kind !== 'shader' &&
        asset.implementation.kind === 'procedural' &&
        !asset.implementation.shader
      ) {
        ctx.addIssue({
          code: 'custom',
          path: ['assets', index, 'implementation', 'shader'],
          message: 'Procedural resource needs a shader',
        });
      }
      const refs = [...asset.dependencies];
      if (asset.implementation.kind === 'procedural' && asset.implementation.shader)
        refs.push(asset.implementation.shader);
      for (const ref of refs) {
        if (!ids.has(ref) && !pack.dependencies.includes(ref))
          ctx.addIssue({
            code: 'custom',
            path: ['assets', index, 'dependencies'],
            message: 'Undeclared resource ' + ref,
          });
      }
      edges.set(
        asset.id,
        refs.filter((ref) => ids.has(ref)),
      );
    }
    const visiting = new Set<string>();
    const visited = new Set<string>();
    function hasCycle(id: string): boolean {
      if (visiting.has(id)) return true;
      if (visited.has(id)) return false;
      visiting.add(id);
      for (const dep of edges.get(id) ?? []) {
        if (hasCycle(dep)) return true;
      }
      visiting.delete(id);
      visited.add(id);
      return false;
    }
    if ([...edges.keys()].some((id) => hasCycle(id)))
      ctx.addIssue({
        code: 'custom',
        path: ['assets'],
        message: 'Visual asset dependency cycle',
      });
  });
export type VisualPack = z.infer<typeof VisualPackSchema>;

export const VisualActorSchema = z
  .object({
    entityId: z.string().min(1),
    rig: ResourceId,
    appearance: AppearanceSchema,
    worldPosition: z.tuple([
      z.number().finite(),
      z.number().finite(),
      z.number().finite(),
    ]),
    facing: z.number().finite(),
    expression: z.enum([
      'neutral',
      'happy',
      'sad',
      'angry',
      'flirty',
      'shocked',
      'scared',
      'smug',
      'crying',
      'embarrassed',
      'tired',
      'thoughtful',
    ]),
    animation: ResourceId,
    ageYears: z.number().int().min(0).max(125),
  })
  .strict();
export const VisualSceneSchema = z
  .object({
    id: ResourceId,
    location: ResourceId,
    day: z.number().int().nonnegative(),
    camera: z
      .object({
        preset: z.enum(['isometric', 'portrait', 'conversation', 'cinematic']),
        orbit: z.number().finite(),
        zoom: z.number().min(0.5).max(4),
      })
      .strict(),
    lighting: z
      .object({
        timeOfDay: z.enum(['dawn', 'day', 'dusk', 'night']),
        weather: z.enum(['clear', 'rain', 'snow', 'fog']),
        lifeStage: z.enum(['child', 'teen', 'young-adult', 'midlife', 'elder']),
      })
      .strict(),
    actors: z.array(VisualActorSchema).max(32),
    props: z
      .array(
        z
          .object({
            assetId: ResourceId,
            worldPosition: z.tuple([
              z.number().finite(),
              z.number().finite(),
              z.number().finite(),
            ]),
            rotation: z.number().finite(),
            scale: z.number().positive().max(100),
          })
          .strict(),
      )
      .max(4096),
  })
  .strict();
export type VisualScene = z.infer<typeof VisualSceneSchema>;

/** Reject broken or duplicated installed content, not just malformed JSON. */
export function indexVisualAssets(
  packs: readonly VisualPack[],
): Map<string, VisualAsset> {
  const index = new Map<string, VisualAsset>();
  for (const pack of packs) {
    for (const asset of pack.assets) {
      if (index.has(asset.id))
        throw new Error('Duplicate installed asset: ' + asset.id);
      index.set(asset.id, asset);
    }
  }
  for (const asset of index.values()) {
    for (const dependency of [
      ...asset.dependencies,
      ...(asset.implementation.kind === 'procedural' &&
      asset.implementation.shader
        ? [asset.implementation.shader]
        : []),
    ]) {
      if (!index.has(dependency))
        throw new Error('Missing installed asset: ' + dependency);
    }
  }
  return index;
}
