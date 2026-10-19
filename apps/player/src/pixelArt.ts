import type { ImageSourcePropType } from 'react-native';

/**
 * Actual 16x16 CC0 PNG assets bundled statically by Metro.
 * Source: https://edfaygo.itch.io/pulse-everyday-streets-1616
 * Publisher: Pulse Everyday Streets 16x16, LICENSE-CC0.txt.
 * Authored files and license details in ../assets/pixel/pulse/README.md.
 * Static require() is necessary for Android/iOS/Web offline image bundling.
 */
/* eslint-disable @typescript-eslint/no-require-imports */
export const pixelArt = {
  grass: require('../assets/pixel/pulse/grass.png'),
  walk: require('../assets/pixel/pulse/walk.png'),
  road: require('../assets/pixel/pulse/road.png'),
  floor: require('../assets/pixel/pulse/floor.png'),
  carpet: require('../assets/pixel/pulse/carpet.png'),
  crosswalk: require('../assets/pixel/pulse/crosswalk.png'),
  tree: require('../assets/pixel/pulse/tree.png'),
  door: require('../assets/pixel/pulse/door.png'),
  window: require('../assets/pixel/pulse/window.png'),
  bench: require('../assets/pixel/pulse/bench.png'),
  chair: require('../assets/pixel/pulse/chair.png'),
  table: require('../assets/pixel/pulse/table.png'),
  plant: require('../assets/pixel/pulse/plant.png'),
  shelf: require('../assets/pixel/pulse/shelf.png'),
  bush: require('../assets/pixel/pulse/bush.png'),
  lamp: require('../assets/pixel/pulse/lamp.png'),
  n1_down: require('../assets/pixel/pulse/n1_down.png'),
  n1_up: require('../assets/pixel/pulse/n1_up.png'),
  n1_left: require('../assets/pixel/pulse/n1_left.png'),
  n1_right: require('../assets/pixel/pulse/n1_right.png'),
  n2_down: require('../assets/pixel/pulse/n2_down.png'),
  n2_up: require('../assets/pixel/pulse/n2_up.png'),
  n2_left: require('../assets/pixel/pulse/n2_left.png'),
  n2_right: require('../assets/pixel/pulse/n2_right.png'),
} as const satisfies Record<string, ImageSourcePropType>;
/* eslint-enable @typescript-eslint/no-require-imports */

export type PixelArtKey = keyof typeof pixelArt;

export function actorArt(
  kind: 1 | 2,
  facing: 'up' | 'down' | 'left' | 'right',
): ImageSourcePropType {
  return pixelArt[('n' + kind + '_' + facing) as PixelArtKey];
}
