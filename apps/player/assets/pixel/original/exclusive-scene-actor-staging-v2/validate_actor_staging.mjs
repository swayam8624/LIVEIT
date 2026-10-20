#!/usr/bin/env node
/* global console, process */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(ROOT, '../../../../../../');
const manifest = JSON.parse(
  fs.readFileSync(path.join(ROOT, 'manifest.json'), 'utf8'),
);
const errors = [];
const require = (ok, message) => {
  if (!ok) errors.push(message);
};
const sha = (f) =>
  crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
require(manifest.runtimeReady ===
  false, 'batch must remain runtimeReady:false');
require(manifest.scenes.length === 4, 'expected exactly four scenes');
require(manifest.frames.length === 96, 'expected 96 directional body frames');
require(manifest.busts.length === 32, 'expected 32 directional bust portraits');
require(manifest.scenes.every(
  (s) =>
    s.runtimeReady === false && s.actors.every((a) => a.runtimeReady === false),
), 'scene and actor runtime gates must remain false');
const entries = new Map(manifest.files.map((f) => [f.file, f]));
for (const file of manifest.files) {
  const full = path.join(ROOT, file.file);
  require(fs.existsSync(full), `missing ${file.file}`);
  if (!fs.existsSync(full)) continue;
  require(sha(full) === file.sha256, `SHA-256 mismatch: ${file.file}`);
  const p = PNG.sync.read(fs.readFileSync(full));
  require(p.width === file.width &&
    p.height === file.height, `dimension mismatch: ${file.file}`);
  require(file.colorMode === 'RGBA' &&
    file.alpha === true, `expected RGBA with alpha: ${file.file}`);
  if (
    file.file.startsWith('frames/') ||
    file.file.startsWith('portraits/') ||
    file.file.startsWith('overlays/')
  ) {
    require(file.alphaMode === 'binary', `alpha must be binary: ${file.file}`);
    require(file.paletteColors <=
      manifest.paletteLimit, `palette exceeds ${manifest.paletteLimit} colors: ${file.file}`);
    let transparentRgb = false,
      intermediateAlpha = false;
    for (let i = 0; i < p.data.length; i += 4) {
      const a = p.data[i + 3];
      if (a !== 0 && a !== 255) intermediateAlpha = true;
      if (a === 0 && (p.data[i] || p.data[i + 1] || p.data[i + 2]))
        transparentRgb = true;
    }
    require(!intermediateAlpha, `intermediate alpha found: ${file.file}`);
    require(!transparentRgb, `transparent pixels carry unstable RGB: ${file.file}`);
  }
}
for (const s of manifest.scenes) {
  const safe = s.actorSafeRegion,
    dialog = s.dialogueSafeRegion;
  for (const placement of s.placements) {
    const top = placement.anchor.y - manifest.canvas.bodyFrame.height + 1;
    require(placement.anchor.x >= safe.x &&
      placement.anchor.x <=
        safe.x +
          safe.width, `${s.id}/${placement.actor}: anchor outside actor-safe x bounds`);
    require(top >= safe.y &&
      placement.anchor.y <=
        safe.y +
          safe.height, `${s.id}/${placement.actor}: body frame outside actor-safe y bounds`);
    require(placement.anchor.y <
      dialog.y, `${s.id}/${placement.actor}: body intersects dialogue-safe region`);
  }
  const overlay = s.foregroundOverlays[0],
    entry = entries.get(overlay.file);
  require(!!entry &&
    entry.width === 320 &&
    entry.height === 256, `${s.id}: expected 320x256 foreground overlay`);
  require(overlay.zOrder ===
    'foreground-over-actors', `${s.id}: missing foreground z-order`);
  if (entry) {
    const p = PNG.sync.read(fs.readFileSync(path.join(ROOT, overlay.file)));
    let overlapsDialogue = false;
    for (let y = dialog.y; y < dialog.y + dialog.height; y++)
      for (let x = dialog.x; x < dialog.x + dialog.width; x++)
        if (p.data[(y * p.width + x) * 4 + 3]) overlapsDialogue = true;
    require(!overlapsDialogue, `${s.id}: foreground overlay intrudes into dialogue-safe region`);
  }
}
const varietyRoot = path.join(
  REPO,
  'apps/player/assets/pixel/original/exclusive-scenes-variety-v1',
);
for (const ref of manifest.backdropReferences) {
  const f = path.join(varietyRoot, ref.file);
  require(fs.existsSync(f), `missing protected backdrop ${ref.file}`);
  if (fs.existsSync(f))
    require(sha(f) === ref.sha256, `protected backdrop changed: ${ref.file}`);
}
const hashesPath = path.join(ROOT, 'hashes.sha256');
const hashes = fs
  .readFileSync(hashesPath, 'utf8')
  .trim()
  .split('\n')
  .map((line) => line.trim())
  .sort();
const expected = manifest.files.map((x) => `${x.sha256}  ${x.file}`).sort();
require(JSON.stringify(hashes) ===
  JSON.stringify(expected), 'hashes.sha256 does not match manifest');
if (errors.length) {
  for (const e of errors) console.error(`FAIL ${e}`);
  process.exitCode = 1;
} else
  console.log(
    `PASS: ${manifest.scenes.length} scenes, ${manifest.frames.length} body frames, ${manifest.busts.length} bust portraits, ${manifest.files.length} hashed images; binary alpha, palette limits, placements, and protected backdrop hashes verified.`,
  );
