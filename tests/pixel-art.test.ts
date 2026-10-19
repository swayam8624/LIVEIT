import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

const directory = 'apps/player/assets/pixel/pulse';
const source = readFileSync(
  resolve(process.cwd(), 'apps/player/src/pixelArt.ts'),
  'utf8',
);
const entries = [
  ...source.matchAll(
    /([a-zA-Z0-9_]+):\s*require\(\s*'\.\.\/assets\/pixel\/pulse\/([a-zA-Z0-9_]+)\.png'\s*\)/g,
  ),
];

const baseSprites = entries.filter((entry) => !entry[1]?.endsWith('_sheet'));
const walkSheets = entries.filter((entry) => entry[1]?.endsWith('_sheet'));

function crc32(bytes: Buffer): number {
  let n = 0xffffffff;
  for (const byte of bytes) {
    n ^= byte;
    for (let bit = 0; bit < 8; bit++) {
      n = n & 1 ? (n >>> 1) ^ 0xedb88320 : n >>> 1;
    }
  }
  return (n ^ 0xffffffff) >>> 0;
}

describe('native-bundled Pulse CC0 pixel art', () => {
  it('has original source provenance, uses static native resources and bundles 24 sprites', () => {
    const provenance = readFileSync(
      resolve(process.cwd(), directory, 'README.md'),
      'utf8',
    );
    expect(provenance).toContain('CC0');
    expect(provenance).toContain('edfaygo.itch.io/pulse-everyday-streets-1616');
    expect(source).not.toContain('data:image/png;base64,');
    expect(baseSprites.length).toBe(24);
    expect(walkSheets.length).toBe(4);
  });

  it('bundles four 64x16 CC0 animation sheets for 4-frame motion', () => {
    for (const match of walkSheets) {
      const path = resolve(process.cwd(), directory, match[2] + '.png');
      expect(existsSync(path)).toBe(true);
      const image = readFileSync(path);
      expect(image.readUInt32BE(16)).toBe(64);
      expect(image.readUInt32BE(20)).toBe(16);
    }
  });

  it('ships actual 16x16 PNG files with valid chunk CRCs, not placeholder URIs', () => {
    const ids = new Set<string>();
    for (const match of baseSprites) {
      const name = match[1];
      const file = match[2];
      if (!name || !file) throw new Error('Invalid sprite source declaration');
      expect(name).toBe(file);
      expect(ids.has(name)).toBe(false);
      ids.add(name);
      const path = resolve(process.cwd(), directory, file + '.png');
      expect(existsSync(path), path).toBe(true);
      const image = readFileSync(path);
      expect(image.subarray(0, 8)).toEqual(
        Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]),
      );
      expect(image.readUInt32BE(16)).toBe(16);
      expect(image.readUInt32BE(20)).toBe(16);
      let offset = 8;
      let ended = false;
      while (offset < image.length) {
        const length = image.readUInt32BE(offset);
        const chunkEnd = offset + 12 + length;
        expect(chunkEnd).toBeLessThanOrEqual(image.length);
        const type = image.toString('ascii', offset + 4, offset + 8);
        expect(crc32(image.subarray(offset + 4, offset + 8 + length))).toBe(
          image.readUInt32BE(offset + 8 + length),
        );
        offset = chunkEnd;
        if (type === 'IEND') {
          ended = true;
          break;
        }
      }
      expect(ended).toBe(true);
      expect(offset).toBe(image.length);
    }
  });
});
