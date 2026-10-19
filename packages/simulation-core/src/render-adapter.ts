import {
  DEFAULT_APPEARANCE,
  PixelRenderFrameSchema,
  CinematicRenderFrameSchema,
  type PixelRenderFrame,
  type CinematicRenderFrame,
  type World,
} from '@living/world-schema';
import { buildVisualScene, type CastMember } from './visual-scene';

export type PixelWorldPose = Readonly<{
  x: number;
  y: number;
  facing: 'north' | 'east' | 'south' | 'west';
  tileMap: string;
  spriteAtlas: string;
  cameraX: number;
  cameraY: number;
}>;

/**
 * Builds a *proposed* pixel frame from the actual saved world and a supplied
 * world-nav pose. LIVEIT v1 does not yet persist tile position/collisions!
 *
 * The caller MUST supply a valid navigation pose from the future authoritative
 * world-position subsystem. This function does not invent a spawn or create a
 * collision system. Asset IDs must be resolved by pack manager before display.
 */
export function buildPixelRenderFrame(
  world: World,
  pose: PixelWorldPose,
  sceneRevision: number,
): PixelRenderFrame {
  const ageYears = Math.floor(world.player.ageDays / 365);
  const district = world.city?.district ?? 'riverside';
  return PixelRenderFrameSchema.parse({
    protocolVersion: 1,
    sceneRevision,
    timelineId: world.timelineId,
    gameDay: world.day,
    playerEntityId: world.player.id,
    mode: 'pixel-overworld',
    locationId: 'liveit.location.bellweather-' + district,
    tileSizePx: 16,
    tileMap: pose.tileMap,
    camera: { centerX: pose.cameraX, centerY: pose.cameraY, zoom: 1 },
    ambient: 'day',
    actors: [
      {
        entityId: world.player.id,
        appearance: world.player.appearance ?? DEFAULT_APPEARANCE,
        ageYears,
        position: { x: pose.x, y: pose.y },
        facing: pose.facing,
        animation: 'idle',
        spriteAtlas: pose.spriteAtlas,
      },
    ],
  });
}

/** Cinema and AI characters always share canonical visual-scene identities. */
export function buildCinematicRenderFrame(
  world: World,
  sceneRevision: number,
  view: 'story' | 'chat' = 'story',
  cast: readonly CastMember[] = [],
): CinematicRenderFrame {
  return CinematicRenderFrameSchema.parse({
    protocolVersion: 1,
    sceneRevision,
    timelineId: world.timelineId,
    gameDay: world.day,
    playerEntityId: world.player.id,
    mode: 'cinematic-3d',
    scene: buildVisualScene(world, view, cast),
  });
}
