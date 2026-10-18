import { createHash } from 'node:crypto';
import { describe, expect, it } from 'vitest';
import {
  VisualPackSchema, prepareVisualPackActivation,
  type VisualAssetVerifier,
} from '@living/world-schema';
import core from '../content/visual-packs/core/manifest.json';

const installed = VisualPackSchema.parse(core);
const bytes = new Uint8Array([37, 80, 78, 71, 0, 1, 2, 3]);
const sha256 = (input: Uint8Array) => createHash('sha256').update(input).digest('hex');
const verifier: VisualAssetVerifier = {
  read: async () => bytes,
  sha256: async (value) => sha256(value),
};
function expansion() {
  return {
    schemaVersion: 1,
    id: 'liveit.pack-accessory-demo',
    revision: 1,
    title: 'Independent miniature asset addition',
    style: installed.style,
    minGameVersion: '0.1.0',
    dependencies: [installed.id],
    assets: [{
      id: 'liveit.prop.demo-pendant',
      kind: 'prop',
      tier: 'downloadable',
      revision: 1,
      style: installed.style,
      dependencies: [],
      tags: ['cosmetic'],
      license: {
        spdx: 'MIT',
        author: 'LIVEIT regression fixture',
        source: 'https://github.com/swayam8624/LIVEIT',
      },
      implementation: {
        kind: 'external', path: 'props/demo-pendant.png',
        sha256: sha256(bytes), bytes: bytes.length, format: 'png',
      },
    }],
  };
}
describe('content growth without executable downloaded code', () => {
  it('verifies bytes and atomically prepares the next installed pack graph', async () => {
    const candidate = await prepareVisualPackActivation([installed], [expansion()], verifier);
    expect(candidate.packs).toHaveLength(2);
    expect(candidate.index.has('liveit.rig.prototype')).toBe(true);
    expect(candidate.index.has('liveit.prop.demo-pendant')).toBe(true);
    expect(candidate.newlyVerifiedBytes).toBe(bytes.length);
    expect(installed.assets).toHaveLength(51);
  });
  it('rejects wrong hashes or short bytes without mutating the current catalog', async () => {
    const previous = structuredClone(installed);
    await expect(prepareVisualPackActivation([installed], [expansion()], {
      ...verifier, read: async () => bytes.slice(0, 3),
    })).rejects.toThrow('byte size mismatch');
    await expect(prepareVisualPackActivation([installed], [expansion()], {
      ...verifier, sha256: async () => '0'.repeat(64),
    })).rejects.toThrow('digest mismatch');
    expect(installed).toEqual(previous);
  });
  it('refuses unknown parents and rollback/downgrade installs', async () => {
    const missing = expansion();
    missing.dependencies = ['liveit.pack-not-installed'];
    await expect(prepareVisualPackActivation([installed], [missing], verifier))
      .rejects.toThrow('Missing required visual pack');
    await expect(prepareVisualPackActivation([installed], [installed], verifier))
      .rejects.toThrow('revisions must increase');
    const newer = expansion();
    newer.minGameVersion = '99.0.0';
    await expect(prepareVisualPackActivation([installed], [newer], verifier))
      .rejects.toThrow('newer game version');
  });
});
