import { describe, expect, it } from 'vitest';
import { generateCityScene, projectCityBlock } from '../packages/simulation-core/src/city-scene';

describe('seeded 3D Bellweather city scenes', () => {
  it('produces an identical scene for an identical seed, without RNG globals', () => {
    const first = generateCityScene(42);
    expect(generateCityScene(42)).toEqual(first);
    expect(generateCityScene(43)).not.toEqual(first);
    expect(first.blocks.length).toBeGreaterThan(35);
    expect(first.blocks.length).toBeLessThanOrEqual(64);
    expect(new Set(first.blocks.map((block) => block.id)).size).toBe(first.blocks.length);
    expect(new Set(first.blocks.map((block) => block.district)).size).toBe(5);
  });

  it('keeps road axes clear and every building inside its own street cell', () => {
    const scene = generateCityScene(1001);
    for (const block of scene.blocks) {
      expect(block.x).not.toBe(0);
      expect(block.z).not.toBe(0);
      expect(block.width).toBeGreaterThan(0);
      expect(block.depth).toBeGreaterThan(0);
      expect(block.width).toBeLessThan(9);
      expect(block.depth).toBeLessThan(9);
      expect(block.height).toBeGreaterThanOrEqual(3);
      expect(Math.abs(block.x)).toBeLessThan(scene.worldRadius);
      expect(Math.abs(block.z)).toBeLessThan(scene.worldRadius);
    }
  });

  it('projects the model deterministically and reacts to camera zoom', () => {
    const block = generateCityScene().blocks[0]!;
    const atOne = projectCityBlock(block, 390, 405);
    const atTwo = projectCityBlock(block, 390, 405, 1.2);
    expect(atOne).toEqual(projectCityBlock(block, 390, 405));
    expect(atTwo.left).not.toBe(atOne.left);
    expect(atTwo.top).not.toBe(atOne.top);
    expect(() => projectCityBlock(block, 0, 100)).toThrow(RangeError);
    expect(() => projectCityBlock(block, 390, 405, -1)).toThrow(RangeError);
  });

  it('rejects non-reproducible seeds', () => {
    expect(() => generateCityScene(-1)).toThrow(RangeError);
    expect(() => generateCityScene(4294967296)).toThrow(RangeError);
    expect(() => generateCityScene(Infinity)).toThrow(RangeError);
  });
});
