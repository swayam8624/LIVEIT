import { z } from 'zod';
import { AppearanceSchema } from './appearance';
import { VisualSceneSchema } from './visual-assets';

/**
 * Renderer ABI intent, not an active native module. Both the pixel world and
 * the 3D cinematic stage receive immutable, validated snapshots; gameplay
 * events travel in the opposite direction as untrusted player intents.
 */
const ResourceId = z.string().regex(/^[a-z][a-z0-9_-]*(?:[./][a-z0-9_-]+)+$/);
const WorldStamp = {
  protocolVersion: z.literal(1),
  sceneRevision: z.number().int().nonnegative(),
  timelineId: z.string().min(1).max(120),
  gameDay: z.number().int().nonnegative(),
  playerEntityId: z.string().min(1).max(120),
};
const PixelActorSchema = z
  .object({
    entityId: z.string().min(1).max(120),
    appearance: AppearanceSchema,
    ageYears: z.number().int().min(0).max(125),
    position: z
      .object({
        x: z.number().finite(),
        y: z.number().finite(),
      })
      .strict(),
    facing: z.enum(['north', 'east', 'south', 'west']),
    animation: z.enum(['idle', 'walk', 'interact']),
    spriteAtlas: ResourceId,
  })
  .strict();

export const PixelRenderFrameSchema = z
  .object({
    ...WorldStamp,
    mode: z.literal('pixel-overworld'),
    locationId: ResourceId,
    tileSizePx: z.literal(16),
    camera: z
      .object({
        centerX: z.number().finite(),
        centerY: z.number().finite(),
        zoom: z.number().finite().min(0.5).max(4),
      })
      .strict(),
    tileMap: ResourceId,
    actors: z.array(PixelActorSchema).min(1).max(500),
    ambient: z.enum(['dawn', 'day', 'dusk', 'night']),
  })
  .strict()
  .superRefine((frame, ctx) => {
    const ids = frame.actors.map((actor) => actor.entityId);
    if (!ids.includes(frame.playerEntityId)) {
      ctx.addIssue({
        code: 'custom',
        message: 'Player actor missing from pixel scene',
        path: ['actors'],
      });
    }
    if (new Set(ids).size !== ids.length) {
      ctx.addIssue({
        code: 'custom',
        message: 'Duplicate pixel entity identity',
        path: ['actors'],
      });
    }
  });

export const CinematicRenderFrameSchema = z
  .object({
    ...WorldStamp,
    mode: z.literal('cinematic-3d'),
    scene: VisualSceneSchema,
  })
  .strict()
  .superRefine((frame, ctx) => {
    if (frame.scene.day !== frame.gameDay) {
      ctx.addIssue({
        code: 'custom',
        message: 'Cinematic day differs from saved world',
        path: ['scene', 'day'],
      });
    }
    const ids = frame.scene.actors.map((actor) => actor.entityId);
    if (!ids.includes(frame.playerEntityId)) {
      ctx.addIssue({
        code: 'custom',
        message: 'Player actor missing from cinematic scene',
        path: ['scene', 'actors'],
      });
    }
    if (new Set(ids).size !== ids.length) {
      ctx.addIssue({
        code: 'custom',
        message: 'Duplicate cinematic entity identity',
        path: ['scene', 'actors'],
      });
    }
  });

export const GameRenderFrameSchema = z.union([
  PixelRenderFrameSchema,
  CinematicRenderFrameSchema,
]);
export type GameRenderFrame = z.infer<typeof GameRenderFrameSchema>;
export type PixelRenderFrame = z.infer<typeof PixelRenderFrameSchema>;
export type CinematicRenderFrame = z.infer<typeof CinematicRenderFrameSchema>;

/**
 * The native renderer emits only *intent*. The TypeScript domain reducer
 * validates range, collision, available choices, costs and consequences.
 * A renderer is never authorized to update a world by itself.
 */
export const RenderUserIntentSchema = z.discriminatedUnion('kind', [
  z
    .object({
      kind: z.literal('walk'),
      sceneRevision: z.number().int().nonnegative(),
      playerEntityId: z.string().min(1).max(120),
      dx: z.number().int().min(-1).max(1),
      dy: z.number().int().min(-1).max(1),
      inputSequence: z.number().int().nonnegative(),
    })
    .strict()
    .refine((value) => Math.abs(value.dx) + Math.abs(value.dy) === 1, {
      message: 'A single walking intent moves exactly one cardinal direction',
    }),
  z
    .object({
      kind: z.literal('interact'),
      sceneRevision: z.number().int().nonnegative(),
      playerEntityId: z.string().min(1).max(120),
      targetEntityId: z.string().min(1).max(120),
      inputSequence: z.number().int().nonnegative(),
    })
    .strict(),
  z
    .object({
      kind: z.literal('choose'),
      sceneRevision: z.number().int().nonnegative(),
      playerEntityId: z.string().min(1).max(120),
      choiceId: z.string().min(1).max(120),
      inputSequence: z.number().int().nonnegative(),
    })
    .strict(),
]);
export type RenderUserIntent = z.infer<typeof RenderUserIntentSchema>;

/** Pure, GPU-agnostic integer viewport plan, not a Vulkan image allocation. */
export function planPixelViewport(
  deviceWidthPx: number,
  deviceHeightPx: number,
  baselineWidth = 320,
  baselineHeight = 256,
): Readonly<{
  integerScale: number;
  presentationWidthPx: number;
  presentationHeightPx: number;
  visibleWorldWidthPx: number;
  visibleWorldHeightPx: number;
  cropOrExtend: 'crop' | 'extend' | 'baseline';
}> {
  const dimensions = [
    deviceWidthPx,
    deviceHeightPx,
    baselineWidth,
    baselineHeight,
  ];
  if (dimensions.some((value) => !Number.isSafeInteger(value) || value <= 0)) {
    throw new RangeError(
      'Pixel viewport dimensions must be positive safe integers',
    );
  }
  if (
    deviceWidthPx > 16384 ||
    deviceHeightPx > 16384 ||
    baselineWidth > 4096 ||
    baselineHeight > 4096
  ) {
    throw new RangeError('Pixel viewport exceeds safe GPU dimensions');
  }
  const fit = Math.floor(
    Math.min(deviceWidthPx / baselineWidth, deviceHeightPx / baselineHeight),
  );
  const integerScale = Math.max(1, fit);
  // Present integer-sized logical pixel quad(s) only; no bilinear smearing.
  const presentationWidthPx =
    Math.floor(deviceWidthPx / integerScale) * integerScale;
  const presentationHeightPx =
    Math.floor(deviceHeightPx / integerScale) * integerScale;
  const visibleWorldWidthPx = presentationWidthPx / integerScale;
  const visibleWorldHeightPx = presentationHeightPx / integerScale;
  const cropOrExtend =
    visibleWorldWidthPx < baselineWidth || visibleWorldHeightPx < baselineHeight
      ? 'crop'
      : visibleWorldWidthPx > baselineWidth ||
          visibleWorldHeightPx > baselineHeight
        ? 'extend'
        : 'baseline';
  return {
    integerScale,
    presentationWidthPx,
    presentationHeightPx,
    visibleWorldWidthPx,
    visibleWorldHeightPx,
    cropOrExtend,
  };
}

/** Validate a native event against the currently presented snapshot, not state alone. */
export function isFreshRendererIntent(
  frame: GameRenderFrame,
  event: RenderUserIntent,
): boolean {
  return (
    frame.sceneRevision === event.sceneRevision &&
    frame.playerEntityId === event.playerEntityId &&
    !(event.kind === 'walk' && frame.mode !== 'pixel-overworld')
  );
}

/**
 * UI outcome is a receipt rather than an automatic "success animation":
 * only display committed if the save coordinator has confirmed persistence.
 */
export const OutcomeReceiptSchema = z
  .object({
    eventId: z.string().min(1).max(150),
    timelineId: z.string().min(1).max(120),
    sceneRevision: z.number().int().nonnegative(),
    status: z.enum(['pending', 'committed', 'failed']),
    category: z.enum([
      'story',
      'relationship',
      'career',
      'money',
      'life',
      'world',
    ]),
    caption: z.string().min(1).max(180),
    deltas: z
      .array(
        z
          .object({
            label: z.string().min(1).max(64),
            amount: z.number().finite(),
            unit: z.enum(['pence', 'points', 'days']),
          })
          .strict(),
      )
      .max(12),
    haptic: z.enum(['none', 'selection', 'confirmation', 'warning']),
  })
  .strict()
  .superRefine((receipt, ctx) => {
    if (receipt.status !== 'committed' && receipt.haptic === 'confirmation') {
      ctx.addIssue({
        code: 'custom',
        path: ['haptic'],
        message: 'Cannot claim confirmation before authoritative persistence',
      });
    }
  });
export type OutcomeReceipt = z.infer<typeof OutcomeReceiptSchema>;

// Render scale budgets are rendering intent, not real-device benchmark results.
export const RenderQualitySchema = z
  .object({
    preset: z.enum(['battery', 'balanced', 'quality']),
    maxFps: z.union([z.literal(30), z.literal(60)]),
    cinematicResolutionScale: z.number().min(0.5).max(1),
    reduceMotion: z.boolean(),
    hapticStrength: z.enum(['off', 'subtle', 'full']),
  })
  .strict();
export type RenderQuality = z.infer<typeof RenderQualitySchema>;
