import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

const read = (path: string): string => readFileSync(resolve(process.cwd(), path), 'utf8');

describe('live player is pixels, not 3D or photographic story art', () => {
  it('renders the original pixel stage rather than an image-backed scene', () => {
    const game = read('apps/player/src/GameStage.tsx');
    expect(game).toContain('<PixelStoryBackdrop');
    expect(game).not.toContain('cafe-dusk.jpg');
    const scene = read('apps/player/src/PixelStoryBackdrop.tsx');
    expect(scene).toContain('pixelArt.plant');
    expect(scene).not.toContain('ImageBackground');
  });

  it('renders appearance-aware 2D pixel busts and never story JPEG actors', () => {
    const story = read('apps/player/src/StoryPlayer.tsx');
    expect(story).toContain('<PixelPortrait');
    expect(story).not.toContain('amelia-portrait.jpg');
    const person = read('apps/player/src/PixelPortrait.tsx');
    expect(person).toContain('SKIN_COLORS');
    expect(person).toContain('HAIR_COLORS');
    expect(person).toContain('OUTFIT_COLORS');
  });

  it('uses native bundled NPC sprite in the life and relationships UI', () => {
    const app = read('apps/player/App.tsx');
    expect(app).toContain('pixelArt.n2_down');
    expect(app).not.toContain("require('./assets/amelia-portrait.jpg')");
    const town = read('apps/player/src/PixelTown.tsx');
    expect(town).toContain("actorArt(");
    expect(town).toContain("window.addEventListener('keydown', handleKey)");
  });
});
