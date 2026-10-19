import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

const source = readFileSync(
  resolve(process.cwd(), 'apps/player/src/pixelArt.ts'),
  'utf8',
);
const entries = [...source.matchAll(/([a-zA-Z0-9_]+): png\('([A-Za-z0-9+/=]+)'\)/g)];

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

describe('bundled user-provided CC0 pixels', () => {
  it('has correctly attributed public-domain source and at least 24 usable frames', () => {
    expect(source).toContain('LICENSE-CC0.txt');
    expect(source).toContain('pulse-everyday-streets-16x16.zip');
    expect(entries.length).toBeGreaterThanOrEqual(24);
  });

  it('every embedded image is a complete 16x16 PNG with correct CRCs', () => {
    const ids = new Set<string>();
    for (const [, name, base64] of entries) {
      if (!name || !base64) throw new Error('Invalid embedded sprite entry');
      expect(ids.has(name)).toBe(false);
      ids.add(name);
      const image = Buffer.from(base64, 'base64');
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
