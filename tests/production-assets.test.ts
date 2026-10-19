import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { validateProductionCatalog } from '../tools/validate-production-assets.mjs';

const directory = resolve(process.cwd(), 'content/production-assets/v1');
const read = (file: string) =>
  JSON.parse(readFileSync(resolve(directory, file), 'utf8')) as {
    entries: Array<Record<string, unknown>>;
  };

describe('LIVEIT production asset inventory — exact aspirational vs shipped boundary', () => {
  const result = validateProductionCatalog();

  it('validates all 1481 planned entries, production priorities and zero completed art', () => {
    expect(result.planned).toBe(1481);
    expect(result.released).toBe(0);
    expect(result.existingPrototypeImages).toBe(28);
    expect(result.tinyPreviews).toBe(2);
    expect(Object.values(result.priorities).reduce((a, b) => a + b, 0)).toBe(1481);
  });

  it('requires individually named 400 rig pieces, not palette-color-only variants', () => {
    const rig = read('characters-3d.json').entries.filter(
      (entry) => entry.category === 'character-rig-part',
    );
    expect(rig.length).toBe(400);
    expect(new Set(rig.map((entry) => entry.id)).size).toBe(400);
    expect(rig.every((entry) => entry.expectedDistinctGeometry === true)).toBe(true);
    expect(rig.some((entry) => entry.status !== 'planned')).toBe(false);
  });

  it('specifies 200 district-specific cinematic sets with actual 3D geometry requirements', () => {
    const sets = read('locations-3d.json').entries.filter(
      (entry) => entry.category === 'cinematic-location',
    );
    const counts = new Map<string, number>();
    for (const scene of sets) {
      const district = scene.district as string;
      counts.set(district, (counts.get(district) ?? 0) + 1);
      expect(scene.expectedDistinctLayout).toBe(true);
      expect(scene.requirements).toMatchObject({
        actual3DGeometryRequired: true,
        npcSpawnMarkers: true,
        returnPortal: true,
      });
    }
    expect(counts.size).toBe(5);
    expect([...counts.values()]).toEqual([40, 40, 40, 40, 40]);
  });

  it('keeps sharp top-down pixel tiles and sprite family requirements explicit', () => {
    const entries = read('pixel-world.json').entries;
    const tiles = entries.filter((entry) => entry.category === 'pixel-tile');
    const families = entries.filter(
      (entry) => entry.category === 'pixel-sprite-family',
    );
    expect(tiles.length).toBe(302);
    expect(families.length).toBe(55);
    expect(tiles.every((entry) => entry.tileSizePx === 16)).toBe(true);
    expect(families.every((entry) => Number(entry.framesRequired) >= 12)).toBe(true);
  });

  it('requires real 3D acting expressions, camera shots and non-executable downloadable shaders', () => {
    const characters = read('characters-3d.json').entries;
    const visuals = read('hud-audio-fx.json').entries;
    expect(characters.filter((entry) => entry.category === 'facial-expression')).toHaveLength(12);
    expect(visuals.filter((entry) => entry.category === 'camera')).toHaveLength(30);
    expect(
      visuals.filter((entry) => entry.category === 'shader').every(
        (entry) => entry.implementationType === 'precompiled-app-only',
      ),
    ).toBe(true);
  });

  it('prevents the existing prototype catalog from being mistaken for completed 3D art', () => {
    const audit = JSON.parse(
      readFileSync(resolve(directory, 'existing-repo-audit.json'), 'utf8'),
    );
    expect(audit.counts.pinnedKenneyCC0Pngs).toBe(28);
    expect(audit.counts.shaderBackedProceduralMetadata).toBe(51);
    expect(audit.counts.realProductionRigged3DCharacters).toBe(0);
    expect(audit.counts.realProductionTopDownTileAtlas).toBe(0);
    expect(audit.counts.realProduction3DCinematicSets).toBe(0);
  });
});
