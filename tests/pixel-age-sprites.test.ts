import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { lifeStageOf } from '@living/simulation-core';
import {
  ameliaLifeArcFrame,
  playerLifeArcFrame,
  playerLifeArcLine,
} from '../apps/player/src/pixelAgeStage';
import { DEFAULT_APPEARANCE } from '@living/world-schema';

describe('appearance-gated pixel life arc', () => {
  const matchingAppearance = {
    ...DEFAULT_APPEARANCE,
    skinTone: 'cocoa' as const,
    hair: 'coils' as const,
    hairColor: 'black' as const,
    outfitColor: 'navy' as const,
  };

  it('uses only saved appearance cues and the canonical life stage', () => {
    expect(playerLifeArcLine(undefined)).toBeUndefined();
    expect(playerLifeArcLine(DEFAULT_APPEARANCE)).toBeUndefined();
    expect(playerLifeArcLine(matchingAppearance)).toBe('woman');
    expect(playerLifeArcFrame(lifeStageOf(65 * 365), 'woman', 'up', 3)).toEqual(
      { row: 6, direction: 3, phase: 3 },
    );
  });

  it('maps Amelia adult and senior to her authored age cycles and directions', () => {
    expect(ameliaLifeArcFrame(lifeStageOf(18 * 365), 'right', 5)).toEqual({
      row: 0,
      direction: 2,
      phase: 5,
    });
    expect(ameliaLifeArcFrame(lifeStageOf(65 * 365), 'left', 4)).toEqual({
      row: 8,
      direction: 1,
      phase: 4,
    });
    expect(
      ameliaLifeArcFrame(lifeStageOf(17 * 365), 'down', 4),
    ).toBeUndefined();
  });

  it('uses static Metro atlas paths with manifest frame dimensions and pivots', () => {
    const source = readFileSync(
      resolve(process.cwd(), 'apps/player/src/pixelAgeSprites.ts'),
      'utf8',
    );
    expect(source).not.toMatch(/require\([^'"]*\+/);
    const paths = [
      'linked-life-arc-family-v2/linked-life-arc-family-v2-movement-atlas-24x32.png',
      'named-friend-age-cycles-v1/named-friend-age-cycles-atlas.png',
    ];
    for (const relative of paths) {
      expect(
        existsSync(
          resolve(process.cwd(), 'apps/player/assets/pixel/original', relative),
        ),
      ).toBe(true);
    }
    const manifest = JSON.parse(
      readFileSync(
        resolve(
          process.cwd(),
          'apps/player/assets/pixel/original/linked-life-arc-family-v2/manifest.json',
        ),
        'utf8',
      ),
    ) as { frameSize: number[]; pivot: number[]; runtimeReady: boolean };
    expect(manifest.frameSize).toEqual([24, 32]);
    expect(manifest.pivot).toEqual([12, 31]);
    expect(manifest.runtimeReady).toBe(false);
  });
});
