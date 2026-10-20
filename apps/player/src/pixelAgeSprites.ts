import type { ImageSourcePropType } from 'react-native';
import type { LifeStage } from '@living/simulation-core';
import type { Appearance } from '@living/world-schema';
import {
  ameliaLifeArcFrame,
  playerLifeArcFrame,
  playerLifeArcLine,
} from './pixelAgeStage';

/* eslint-disable @typescript-eslint/no-require-imports */
export const playerLifeArcAtlas =
  require('../assets/pixel/original/linked-life-arc-family-v2/linked-life-arc-family-v2-movement-atlas-24x32.png') as ImageSourcePropType;
export const ameliaLifeArcAtlas =
  require('../assets/pixel/original/named-friend-age-cycles-v1/named-friend-age-cycles-atlas.png') as ImageSourcePropType;
/* eslint-enable @typescript-eslint/no-require-imports */

export function playerLifeArcSelection(
  appearance: Appearance | undefined,
  stage: LifeStage,
) {
  const line = playerLifeArcLine(appearance);
  return line ? { line, stage, atlas: playerLifeArcAtlas } : undefined;
}

export function playerLifeArcCell(
  appearance: Appearance | undefined,
  stage: LifeStage,
  direction: 'down' | 'left' | 'right' | 'up',
  phase: number,
) {
  const line = playerLifeArcLine(appearance);
  return line ? playerLifeArcFrame(stage, line, direction, phase) : undefined;
}

export function ameliaLifeArcCell(
  stage: LifeStage,
  direction: 'down' | 'left' | 'right' | 'up',
  phase: number,
) {
  return ameliaLifeArcFrame(stage, direction, phase);
}
