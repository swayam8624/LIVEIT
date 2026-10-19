#!/usr/bin/env node
/**
 * LIVEIT production content inventory validator (no third-party dependencies).
 * This validates planned asset metadata and basic release gates, NOT rights in
 * third-party files or actual on-device artistic quality. Those require review.
 */
import { readFileSync, existsSync, statSync } from 'node:fs';
import { dirname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const DIR = resolve(ROOT, 'content/production-assets/v1');
const read = (path) => JSON.parse(readFileSync(resolve(DIR, path), 'utf8'));
const fail = (message) => { throw new Error('Asset catalog invalid: ' + message); };
const validId = /^liveit\.prod\.v1\.[a-z][a-z0-9-]*(?:\.[a-z0-9-]+)+$/;
const validPath = (value) => {
  if (typeof value !== 'string' || !value || value.includes('\\') ||
      value.startsWith('/') || value.includes('\0') ||
      value.split('/').includes('..') || value.split('/').includes('.')) return false;
  const normalized = resolve(ROOT, value);
  return normalized.startsWith(ROOT + sep);
};
const statuses = new Set(['planned', 'sourced', 'in-production', 'qa-passed', 'released']);
const waves = new Set(['P0', 'P1', 'P2']);
const sha256Pattern = /^[a-f0-9]{64}$/;
const countItems = (items, key) => items.reduce((acc, x) => {
  acc[x[key]] = (acc[x[key]] ?? 0) + 1;
  return acc;
}, {});
const assert = (condition, message) => { if (!condition) fail(message); };

export function validateProductionCatalog() {
  const index = read('catalog-index.json');
  assert(index.schemaVersion === 1 && index.catalogId === 'liveit.production.v1', 'index/version');
  assert(Array.isArray(index.sourceFiles) && index.sourceFiles.length === 4, 'expected 4 inventory files');
  const assets = [];
  for (const name of index.sourceFiles) {
    assert(/^[a-z0-9-]+\.json$/.test(name), 'untrusted filename ' + name);
    const file = read(name);
    assert(file.schemaVersion === 1 && Array.isArray(file.entries), 'invalid entries in ' + name);
    assert(file.entries.length === index.sourceFileCounts[name], 'index count mismatch for ' + name);
    for (const asset of file.entries) assets.push(asset);
  }
  assert(index.itemsPlanned === assets.length, 'planned total mismatch');
  assert(assets.length === 1481, 'unexpected drift from Step 5 baseline; intentionally update index and test together');
  const ids = new Set();
  const pairs = new Set();
  const seenFiles = new Map();
  let released = 0;
  for (const asset of assets) {
    assert(typeof asset.id === 'string' && validId.test(asset.id), 'invalid ID ' + asset.id);
    assert(!ids.has(asset.id), 'duplicate asset ' + asset.id);
    ids.add(asset.id);
    assert(typeof asset.label === 'string' && asset.label.trim().length > 1, 'missing label ' + asset.id);
    assert(typeof asset.category === 'string' && asset.category.length > 1, 'missing category ' + asset.id);
    assert(waves.has(asset.productionWave), 'unknown production priority ' + asset.id);
    assert(statuses.has(asset.status), 'unknown production status ' + asset.id);
    assert(Array.isArray(asset.qa) && asset.qa.length >= 1, 'missing QA protocol ' + asset.id);
    const semantic = asset.category + ':' + (asset.slot || asset.district || asset.group || '') + ':' + asset.label.toLowerCase();
    assert(!pairs.has(semantic), 'duplicated semantic work item ' + semantic);
    pairs.add(semantic);
    const planned = asset.status === 'planned';
    if (planned) {
      assert(asset.assetFile == null && asset.sourceFile == null && asset.sha256 == null,
        'unproduced record cannot claim a file/hash: ' + asset.id);
      assert(asset.creator == null && asset.licenseEvidence == null,
        'unproduced record cannot claim source rights: ' + asset.id);
    } else {
      assert(typeof asset.creator === 'string' && asset.creator.trim().length > 1,
        'creator missing on sourced asset: ' + asset.id);
      assert(typeof asset.licenseEvidence === 'string' && asset.licenseEvidence.trim().length > 3,
        'license missing on sourced asset: ' + asset.id);
      assert(typeof asset.sourceFile === 'string' && validPath(asset.sourceFile),
        'source file path invalid: ' + asset.id);
      if (asset.status === 'qa-passed' || asset.status === 'released') {
        assert(typeof asset.assetFile === 'string' && validPath(asset.assetFile), 'runtime path invalid: ' + asset.id);
        assert(sha256Pattern.test(asset.sha256), 'missing verified SHA-256: ' + asset.id);
        assert(Array.isArray(asset.qaEvidence) && asset.qaEvidence.length > 0,
          'missing QA evidence: ' + asset.id);
        for (const path of [asset.sourceFile, asset.assetFile, ...asset.qaEvidence]) {
          assert(validPath(path) && existsSync(resolve(ROOT, path)),
            'missing artifact/evidence ' + asset.id + ':' + path);
          assert(statSync(resolve(ROOT, path)).isFile(),
            'expected file ' + asset.id + ':' + path);
        }
        const old = seenFiles.get(asset.assetFile);
        assert(!old || old === asset.id, 'two IDs claim the same unique binary ' + asset.assetFile);
        seenFiles.set(asset.assetFile, asset.id);
      }
    }
    if (asset.status === 'released') released++;
  }
  const categories = countItems(assets, 'category');
  const priorities = countItems(assets, 'productionWave');
  assert(JSON.stringify(categories) === JSON.stringify(index.categoryTargets),
    'category count changed without index update');
  assert(JSON.stringify(priorities) === JSON.stringify(index.productionWaves),
    'production wave counts changed without index update');
  assert(released === index.itemsReleased, 'released count mismatch');
  assert(categories['character-rig-part'] === index.milestoneGoals.customizationParts,
    '400-part goal lost');
  assert(categories['cinematic-location'] === index.milestoneGoals.distinctCinematicLocations,
    '200-location goal lost');
  assert(categories['facial-expression'] === index.milestoneGoals.cinematicExpressions,
    'expression names lost');
  assert(categories.camera === index.milestoneGoals.cinematicCameraPresets,
    'cinematic camera goal lost');
  assert(categories['pixel-sprite-family'] >= index.milestoneGoals.minimumPixelActorFamilies,
    'sprite population planning regressed');

  const audit = read('existing-repo-audit.json');
  assert(audit.existing.length === 28 && audit.preview.length === 2, 'source asset baseline changed');
  const existingPaths = new Set();
  for (const item of [...audit.existing, ...audit.preview]) {
    assert(validPath(item.path) && existsSync(resolve(ROOT, item.path)),
      'missing declared existing repository asset ' + item.path);
    assert(!existingPaths.has(item.path), 'duplicate existing source path');
    existingPaths.add(item.path);
  }
  for (const item of audit.existing) {
    assert(item.license === 'CC0-1.0' && /^[a-f0-9]{40}$/.test(item.gitBlobSha1),
      'pinned Kenney provenance missing ' + item.path);
    assert(item.status === 'existing-prototype', 'do not claim Kenney image is final art');
  }
  assert(audit.proceduralMetadata.count ===
    JSON.parse(readFileSync(resolve(ROOT, audit.proceduralMetadata.manifest), 'utf8')).assets.length,
    'historical procedural recipe count changed');
  assert(released === 0, 'unexpected release count: inspect full art/QA before accepting a release');
  return { planned: assets.length, released, categories, priorities, existingPrototypeImages: audit.existing.length, tinyPreviews: audit.preview.length };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const result = validateProductionCatalog();
    process.stdout.write(JSON.stringify(result, null, process.argv.includes('--json') ? 2 : 0) + '\n');
  } catch (error) {
    process.stderr.write(String(error) + '\n');
    process.exitCode = 1;
  }
}
