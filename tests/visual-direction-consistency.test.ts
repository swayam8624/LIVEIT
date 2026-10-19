import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

const fromRoot = (path: string): string =>
  readFileSync(resolve(process.cwd(), path), 'utf8');

describe('hybrid visual doctrine stays consistent across the repository', () => {
  const authorities = [
    'docs/LIVEIT_GRAPHICS_DESIGN_SPEC_V1.md',
    'docs/LIVEIT_SCREEN_MODE_BLUEPRINT_V1.md',
    'docs/LIVEIT_RENDER_ENGINE_ARCHITECTURE_V1.md',
    'docs/UNIFIED_VISUAL_ENGINE_VISION.md',
    'docs/ART_DIRECTION.md',
    'docs/HYBRID_RENDER_IMPLEMENTATION_PLAN.md',
    'docs/DOCUMENT_INDEX.md',
  ];

  it('keeps all three source-of-truth specs and their index available', () => {
    for (const file of authorities) {
      expect(existsSync(resolve(process.cwd(), file)), file).toBe(true);
    }
    const index = fromRoot('docs/DOCUMENT_INDEX.md');
    expect(index).toContain('GDS-001');
    expect(index).toContain('GDS-002');
    expect(index).toContain('ENG-003');
    expect(index).toMatch(/top-down pixel overworld/i);
  });

  it('designates pixel free-roam, true 3D cinematics and tactile HUD in mission and art', () => {
    const agent = fromRoot('AGENTS.md');
    const art = fromRoot('docs/ART_DIRECTION.md');
    const vision = fromRoot('docs/UNIFIED_VISUAL_ENGINE_VISION.md');
    expect(agent).toMatch(/top-down pixel gameplay/i);
    expect(agent).toMatch(/rigged 3D/i);
    expect(art).toMatch(/16×16 logical/i);
    expect(art).toMatch(/3D geometry/i);
    expect(vision).toMatch(/top-down pixel/i);
    expect(vision).toMatch(/TACTILE UI/i);
  });

  it('clearly distinguishes current illustrated map from a walkable pixel world', () => {
    const readme = fromRoot('README.md');
    const status = fromRoot('docs/BUILD_STATUS.md');
    const historical = fromRoot('docs/VULKAN_CITY_RENDERING.md');
    expect(readme).toMatch(/district selector/i);
    expect(readme).toMatch(/not\*\* exist in the phone player yet/i);
    expect(status).toMatch(/native view/i);
    expect(status).toMatch(/DISTRICT PREVIEW/);
    expect(historical).toMatch(/ARCHIVED TECHNICAL SLICE/);
  });

  it('retains working fallback UI and checks that native GPU rendering is opt-in only', () => {
    const city = fromRoot('apps/player/src/CityWorld.tsx');
    const story = fromRoot('apps/player/src/StoryPlayer.tsx');
    const policy = fromRoot('apps/player/src/visualPresentation.ts');
    expect(city).toContain('BELLWEATHER / DISTRICT PREVIEW');
    expect(story).toContain('selectVisualPresentation');
    expect(policy).toContain("state: 'unavailable'");
    expect(policy).toContain("backend: 'android-vulkan' | 'ios-moltenvk'");
  });
});
