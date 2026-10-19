import { describe, expect, it } from 'vitest';
import {
  CURRENT_VISUAL_CAPABILITY,
  selectVisualPresentation,
  type VisualCapability,
} from '../apps/player/src/visualPresentation';

describe('LIVEIT hybrid runtime graphics fallback policy', () => {
  it('never equates an uninstalled native module with real pixel free roaming', () => {
    const result = selectVisualPresentation(
      'pixel-overworld',
      CURRENT_VISUAL_CAPABILITY,
    );
    expect(result.renderer).toBe('illustrated-fallback');
    expect(result.status).toBe('fallback');
    expect(result.accessibilityLabel).toMatch(/not a walkable pixel world/);
  });

  it('describes fallback story illustrations as not live rigged 3D', () => {
    const result = selectVisualPresentation(
      'cinematic-3d',
      CURRENT_VISUAL_CAPABILITY,
    );
    expect(result.renderer).toBe('illustrated-fallback');
    expect(result.accessibilityLabel).toMatch(/not live rigged 3D/);
  });

  const surface = {
    state: 'ready',
    backend: 'android-vulkan',
    generation: 12,
    supportedModes: ['pixel-overworld', 'cinematic-3d'],
    assetsReady: true,
  } as const satisfies VisualCapability;

  it('requires an active generation, supported mode and verified asset readiness', () => {
    expect(
      selectVisualPresentation('pixel-overworld', surface).renderer,
    ).toBe('native-vulkan');
    expect(
      selectVisualPresentation('cinematic-3d', surface).renderer,
    ).toBe('native-vulkan');
    expect(
      selectVisualPresentation('cinematic-3d', {
        ...surface,
        assetsReady: false,
      }).renderer,
    ).toBe('illustrated-fallback');
    expect(
      selectVisualPresentation('pixel-overworld', {
        ...surface,
        supportedModes: ['cinematic-3d'],
      }).renderer,
    ).toBe('illustrated-fallback');
    expect(
      selectVisualPresentation('pixel-overworld', {
        ...surface,
        generation: 0,
      }).renderer,
    ).toBe('illustrated-fallback');
    expect(
      selectVisualPresentation('pixel-overworld', {
        ...surface,
        generation: Number.NaN,
      }).renderer,
    ).toBe('illustrated-fallback');
  });

  it('reports verified iOS and Android backends only when renderer is ready', () => {
    const ios: VisualCapability = {
      ...surface,
      backend: 'ios-moltenvk',
    };
    expect(
      selectVisualPresentation('cinematic-3d', ios).status,
    ).toBe('ready');
    expect(
      selectVisualPresentation('cinematic-3d', {
        state: 'unavailable',
        reason: 'GPU device lost',
      }).fallbackReason,
    ).toBe('GPU device lost');
  });
});
