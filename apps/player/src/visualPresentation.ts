import type { GameRenderFrame } from '@living/world-schema';

/**
 * Step 4 compatibility gate: LIVEIT currently has no embedded native Vulkan
 * surface module. An offscreen PPM or successful bundling is NOT proof that a
 * GPU renderer is mounted on the user's screen.
 *
 * Keep an actual usable illustrated fallback until the Expo native view
 * reports a matching mode, active surface generation, and ready assets.
 */
export type VisualCapability = Readonly<
  | { state: 'unavailable'; reason: string }
  | {
      state: 'ready';
      backend: 'android-vulkan' | 'ios-moltenvk';
      generation: number;
      supportedModes: readonly GameRenderFrame['mode'][];
      assetsReady: boolean;
    }
>;

export type VisualPresentation = Readonly<{
  mode: GameRenderFrame['mode'];
  renderer: 'native-vulkan' | 'illustrated-fallback';
  status: 'ready' | 'fallback';
  accessibilityLabel: string;
  fallbackReason?: string;
}>;

/** This constant must only be replaced by live native module capability data. */
export const CURRENT_VISUAL_CAPABILITY: VisualCapability = {
  state: 'unavailable',
  reason: 'Native Vulkan/MoltenVK view is not yet integrated',
};

export function selectVisualPresentation(
  mode: GameRenderFrame['mode'],
  capability: VisualCapability,
): VisualPresentation {
  const actualSurface =
    capability.state === 'ready' &&
    Number.isSafeInteger(capability.generation) &&
    capability.generation > 0 &&
    capability.assetsReady &&
    capability.supportedModes.includes(mode);

  if (actualSurface) {
    return {
      mode,
      renderer: 'native-vulkan',
      status: 'ready',
      accessibilityLabel:
        mode === 'pixel-overworld'
          ? 'Pixel-crisp GPU overworld with accessible controls'
          : 'Animated GPU cinematic stage with accessible dialogue',
    };
  }

  return {
    mode,
    renderer: 'illustrated-fallback',
    status: 'fallback',
    accessibilityLabel:
      mode === 'pixel-overworld'
        ? 'Illustrated district-selection preview, not a walkable pixel world'
        : 'Illustrated story stage, not live rigged 3D',
    fallbackReason:
      capability.state === 'unavailable'
        ? capability.reason
        : !capability.supportedModes.includes(mode)
          ? 'Native renderer does not support the requested visual mode'
          : !capability.assetsReady
            ? 'Required visual assets not yet available'
            : 'Native render surface is not currently mounted',
  };
}
