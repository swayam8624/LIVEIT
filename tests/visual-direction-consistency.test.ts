import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

const fromRoot = (path: string): string =>
  readFileSync(resolve(process.cwd(), path), 'utf8');

describe('current 100% pixel-only owner direction remains canonical', () => {
  const authorities = [
    'docs/PIXEL_ONLY_DIRECTION_V2.md',
    'docs/UNIFIED_VISUAL_ENGINE_VISION.md',
    'docs/ART_DIRECTION.md',
    'content/production-assets/pixel-v2/required-assets.json',
    'docs/DOCUMENT_INDEX.md',
  ];

  it('keeps the new pixel-only source of truth, active catalog and history', () => {
    for (const file of authorities) expect(existsSync(resolve(process.cwd(), file)), file).toBe(true);
    const index = fromRoot('docs/DOCUMENT_INDEX.md');
    expect(index).toMatch(/PIXEL ART/i);
    expect(index).toMatch(/superseded|retir/i);
    expect(existsSync(resolve(process.cwd(), 'docs/LIVEIT_RENDER_ENGINE_ARCHITECTURE_V1.md'))).toBe(true);
  });

  it('requires the living city and expressive dialogue to be only 2D pixel scenes', () => {
    const agent = fromRoot('AGENTS.md');
    const art = fromRoot('docs/ART_DIRECTION.md');
    const vision = fromRoot('docs/UNIFIED_VISUAL_ENGINE_VISION.md');
    expect(agent).toMatch(/pixel art/i);
    expect(agent).toMatch(/No 3D art/i);
    expect(art).toMatch(/16×16/i);
    expect(art).toMatch(/animated scenes/i);
    expect(vision).toMatch(/100% 2D RETRO PIXEL ART/i);
    expect(vision).toMatch(/mouth\/blink/i);
  });

  it('keeps imported pixels and game audio rights-checked', () => {
    const readme = fromRoot('README.md');
    const agent = fromRoot('AGENTS.md');
    expect(readme).toContain('assets:intake');
    expect(agent).toContain('tools/intake_pixel_assets.py');
    expect(existsSync(resolve(process.cwd(), 'tools/validate_pixel_assets.py'))).toBe(true);
  });

  it('has a real 2D walking stage and a still-authoritative story engine', () => {
    const city = fromRoot('apps/player/src/CityWorld.tsx');
    const town = fromRoot('apps/player/src/PixelTown.tsx');
    const logic = fromRoot('apps/player/src/pixelTownLogic.ts');
    const story = fromRoot('apps/player/src/StoryPlayer.tsx');
    expect(city).toContain('PixelTown');
    expect(town).toContain('AsyncStorage');
    expect(logic).toContain('movePixel');
    expect(logic).toContain('pixelCell');
    expect(story).toContain('currentScene');
    expect(story).not.toContain('selectVisualPresentation');
  });
});
