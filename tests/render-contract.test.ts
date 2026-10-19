import { describe, expect, it } from 'vitest';
import {
  createWorld,
  setCharacterAppearance,
  buildPixelRenderFrame,
  buildCinematicRenderFrame,
} from '@living/simulation-core';
import {
  DEFAULT_APPEARANCE,
  GameRenderFrameSchema,
  RenderUserIntentSchema,
  OutcomeReceiptSchema,
  planPixelViewport,
  isFreshRendererIntent,
  type PixelRenderFrame,
} from '@living/world-schema';

const pose = {
  x: 8,
  y: 8,
  facing: 'south' as const,
  tileMap: 'liveit.tilemap.bellweather-market',
  spriteAtlas: 'liveit.atlas.player-core',
  cameraX: 8,
  cameraY: 8,
};

describe('hybrid LIVEIT rendering contract (no active native view yet)', () => {
  it('makes pixel and 3D frames share one saved identity and its appearance', () => {
    const world = setCharacterAppearance(createWorld(), {
      ...DEFAULT_APPEARANCE,
      hairColor: 'blue',
      skinTone: 'umber',
      outfitColor: 'rose',
    });
    const pixel = buildPixelRenderFrame(world, pose, 17);
    const threeD = buildCinematicRenderFrame(world, 17);
    const chat = buildCinematicRenderFrame(world, 17, 'chat');

    for (const frame of [pixel, threeD, chat]) {
      expect(GameRenderFrameSchema.safeParse(frame).success).toBe(true);
      expect(frame.playerEntityId).toBe(world.player.id);
      expect(frame.timelineId).toBe(world.timelineId);
      expect(frame.gameDay).toBe(world.day);
    }
    expect(pixel.actors[0]!.appearance).toEqual(threeD.scene.actors[0]!.appearance);
    expect(pixel.actors[0]!.appearance).toEqual(chat.scene.actors[0]!.appearance);
    expect(pixel.actors[0]!.ageYears).toBe(threeD.scene.actors[0]!.ageYears);
    expect(pixel.actors[0]!.spriteAtlas).toBe(pose.spriteAtlas);
    expect(pose.x).toBe(8); // immutable presentation adapter
  });

  it('does not fabricate persisted tile position on its own', () => {
    const world = createWorld();
    const other = buildPixelRenderFrame(world, { ...pose, x: 51, y: -3 }, 1);
    expect(other.actors[0]!.position).toEqual({ x: 51, y: -3 });
    expect(world.city).not.toHaveProperty('position');
    expect(() => buildPixelRenderFrame(world, { ...pose, x: NaN }, 1)).toThrow();
  });

  it('rejects missing player, duplicate actor and invalid scene day', () => {
    const world = createWorld();
    const pixel = buildPixelRenderFrame(world, pose, 3);
    const missing: PixelRenderFrame = {
      ...pixel, playerEntityId: 'different-entity',
    };
    expect(GameRenderFrameSchema.safeParse(missing).success).toBe(false);
    const duplicated = { ...pixel, actors: [...pixel.actors, pixel.actors[0]!] };
    expect(GameRenderFrameSchema.safeParse(duplicated).success).toBe(false);
    const cinema = buildCinematicRenderFrame(world, 3);
    expect(GameRenderFrameSchema.safeParse({
      ...cinema, gameDay: world.day + 1,
    }).success).toBe(false);
  });

  it('only recognizes current scene-revision input from the correct player', () => {
    const world = createWorld();
    const frame = buildPixelRenderFrame(world, pose, 13);
    const cmd = RenderUserIntentSchema.parse({
      kind: 'walk',
      sceneRevision: 13,
      playerEntityId: world.player.id,
      dx: 1,
      dy: 0,
      inputSequence: 8,
    });
    expect(isFreshRendererIntent(frame, cmd)).toBe(true);
    expect(isFreshRendererIntent({ ...frame, sceneRevision: 14 }, cmd)).toBe(false);
    expect(isFreshRendererIntent(buildCinematicRenderFrame(world, 13), cmd)).toBe(false);
    expect(RenderUserIntentSchema.safeParse({ ...cmd, dx: 1, dy: 1 }).success).toBe(false);
    expect(RenderUserIntentSchema.safeParse({ ...cmd, dx: 0, dy: 0 }).success).toBe(false);
  });

  it('plans integer-scale nearest-neighbor viewport sizing and safe narrow crops', () => {
    expect(planPixelViewport(960, 768)).toEqual({
      integerScale: 3,
      presentationWidthPx: 960,
      presentationHeightPx: 768,
      visibleWorldWidthPx: 320,
      visibleWorldHeightPx: 256,
      cropOrExtend: 'baseline',
    });
    const portrait = planPixelViewport(1170, 2040);
    expect(portrait.integerScale).toBe(3);
    expect(portrait.presentationWidthPx % portrait.integerScale).toBe(0);
    expect(portrait.visibleWorldHeightPx).toBeGreaterThan(256);
    expect(planPixelViewport(240, 200).cropOrExtend).toBe('crop');
    expect(() => planPixelViewport(0, 300)).toThrow(RangeError);
    expect(() => planPixelViewport(NaN, 300)).toThrow(RangeError);
  });

  it('never emits a confirmation haptic for pending or failed receipt', () => {
    const base = {
      eventId: 'main:event:2',
      timelineId: 'main',
      sceneRevision: 12,
      status: 'pending' as const,
      category: 'relationship' as const,
      caption: 'Amelia: Trust +9',
      deltas: [{ label: 'Trust', amount: 9, unit: 'points' as const }],
      haptic: 'none' as const,
    };
    expect(OutcomeReceiptSchema.safeParse(base).success).toBe(true);
    expect(OutcomeReceiptSchema.safeParse({
      ...base, haptic: 'confirmation',
    }).success).toBe(false);
    expect(OutcomeReceiptSchema.safeParse({
      ...base, status: 'failed', haptic: 'confirmation',
    }).success).toBe(false);
    expect(OutcomeReceiptSchema.safeParse({
      ...base, status: 'committed', haptic: 'confirmation',
    }).success).toBe(true);
  });
});
