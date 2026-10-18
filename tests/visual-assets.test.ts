import { describe, expect, it } from 'vitest';
import { createWorld, buildVisualScene, setCharacterAppearance } from '@living/simulation-core';
import {
  DEFAULT_APPEARANCE, VisualSceneSchema, VisualPackSchema,
  indexVisualAssets, type VisualPack,
} from '@living/world-schema';
// Vitest resolves JSON as build-time content; no HTTP or bundled image downloads.
import coreVisuals from '../content/visual-packs/core/manifest.json';

describe('growing visual pack system', () => {
  const pack = VisualPackSchema.parse(coreVisuals);

  it('loads all shader-backed visual assets as one validated graph', () => {
    const lookup = indexVisualAssets([pack]);
    expect(pack.assets.length).toBeGreaterThan(45);
    expect(lookup.get('liveit.rig.prototype')?.kind).toBe('rig');
    expect(lookup.get('liveit.expression.crying')?.implementation.kind).toBe('procedural');
    expect(lookup.get('liveit.outfit.palette-teal')?.implementation.kind).toBe('procedural');
  });

  it('rejects duplicate, missing, circular and untrusted asset paths', () => {
    const duplicate = structuredClone(pack);
    duplicate.assets.push({ ...duplicate.assets[0]! });
    expect(VisualPackSchema.safeParse(duplicate).success).toBe(false);
    const missing = structuredClone(pack);
    missing.assets[2]!.dependencies = ['liveit.material.nonexistent'];
    expect(VisualPackSchema.safeParse(missing).success).toBe(false);
    const cycle = structuredClone(pack);
    cycle.assets[0]!.dependencies = ['liveit.shader.actors'];
    cycle.assets[1]!.dependencies = ['liveit.shader.city'];
    expect(VisualPackSchema.safeParse(cycle).success).toBe(false);
    const unsafe = structuredClone(pack) as VisualPack;
    unsafe.assets[0]!.implementation = {
      kind: 'external', path: '../escape.png', sha256: '0'.repeat(64),
      bytes: 100, format: 'png',
    };
    expect(VisualPackSchema.safeParse(unsafe).success).toBe(false);
    expect(() => indexVisualAssets([pack, pack])).toThrow('Duplicate installed asset');
  });

  it('keeps old saved appearance consistent in city, story and AI portrait scenes', () => {
    const world = setCharacterAppearance(createWorld(), {
      ...DEFAULT_APPEARANCE,
      skinTone: 'umber',
      hairColor: 'blue',
      hair: 'long',
      outfitColor: 'rose',
    });
    const city = buildVisualScene(world, 'city');
    const story = buildVisualScene(world, 'story');
    const chat = buildVisualScene(world, 'chat');
    for (const scene of [city, story, chat]) {
      expect(VisualSceneSchema.safeParse(scene).success).toBe(true);
      expect(scene.actors[0]!.appearance).toEqual(world.player.appearance);
      expect(scene.actors[0]!.entityId).toBe(world.player.id);
      expect(scene.day).toBe(world.day);
    }
    expect(city.camera.preset).toBe('isometric');
    expect(story.camera.preset).toBe('conversation');
    expect(chat.camera.preset).toBe('portrait');
  });

  it('requires explicit distinct persisted NPC identity, never invents a cast', () => {
    const world = createWorld();
    expect(buildVisualScene(world, 'chat').actors).toHaveLength(1);
    const cast = [{
      entityId: 'npc-amelia',
      appearance: DEFAULT_APPEARANCE,
      ageYears: 24,
      expression: 'happy' as const,
    }];
    expect(buildVisualScene(world, 'story', cast).actors[1]!.entityId).toBe('npc-amelia');
    expect(() => buildVisualScene(world, 'story', [...cast, ...cast])).toThrow();
    expect(() => buildVisualScene(world, 'story', [{
      ...cast[0]!, entityId: world.player.id,
    }])).toThrow();
  });
});
