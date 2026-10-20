#!/usr/bin/env node
/* global __dirname, require */
/* eslint-disable @typescript-eslint/no-require-imports */

/**
 * Build original transparent pixel actor studies for the garden-graduation
 * exclusive scene. Integer primitives keep the batch deterministic and avoid
 * copying pixels from any supplied archive or existing scene image.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { PNG } = require('pngjs');

const ROOT = __dirname;
const FRAME = { width: 48, height: 80 };
const ATLAS = { columns: 12, rows: 3, width: 576, height: 240 };
const PREVIEW_SCALE = 2;
const DIRECTIONS = ['south', 'east', 'north', 'west'];
const P = {
  ink: [31, 27, 48, 255],
  shadow: [53, 42, 65, 255],
  skin: [220, 151, 116, 255],
  skinLight: [247, 190, 145, 255],
  hair: [67, 45, 58, 255],
  hairLight: [106, 68, 69, 255],
  coral: [220, 95, 100, 255],
  coralDark: [151, 63, 78, 255],
  mint: [102, 199, 164, 255],
  mintDark: [61, 126, 116, 255],
  sky: [108, 163, 209, 255],
  lavender: [157, 128, 197, 255],
  gold: [244, 185, 78, 255],
  cream: [255, 231, 174, 255],
  paper: [255, 246, 212, 255],
  wood: [126, 72, 55, 255],
};

function image() {
  const png = new PNG({ width: FRAME.width, height: FRAME.height });
  png.data.fill(0);
  return png;
}
function color(c) {
  return P[c] || c;
}
function set(im, x, y, c) {
  if (x < 0 || y < 0 || x >= im.width || y >= im.height) return;
  const i = (im.width * y + x) << 2;
  const v = color(c);
  im.data[i] = v[0];
  im.data[i + 1] = v[1];
  im.data[i + 2] = v[2];
  im.data[i + 3] = v[3];
}
function rect(im, x0, y0, x1, y1, c) {
  for (let y = y0; y <= y1; y += 1)
    for (let x = x0; x <= x1; x += 1) set(im, x, y, c);
}
function poly(im, points, c) {
  const minY = Math.max(0, Math.min(...points.map((p) => p[1])));
  const maxY = Math.min(im.height - 1, Math.max(...points.map((p) => p[1])));
  for (let y = minY; y <= maxY; y += 1) {
    const xs = [];
    for (let i = 0, j = points.length - 1; i < points.length; j = i++) {
      const [xi, yi] = points[i];
      const [xj, yj] = points[j];
      if (yi > y !== yj > y) xs.push(xi + ((y - yi) * (xj - xi)) / (yj - yi));
    }
    xs.sort((a, b) => a - b);
    for (let i = 0; i + 1 < xs.length; i += 2)
      for (let x = Math.ceil(xs[i]); x <= Math.floor(xs[i + 1]); x += 1)
        set(im, x, y, c);
  }
}
function outlineRect(im, x0, y0, x1, y1, fill) {
  rect(im, x0, y0, x1, y1, 'ink');
  rect(im, x0 + 2, y0 + 2, x1 - 2, y1 - 2, fill);
}
function ground(im) {
  rect(im, 11, 76, 36, 78, 'shadow');
}
function head(im, dir, hair = 'hair') {
  if (dir === 'north') {
    rect(im, 17, 12, 30, 26, hair);
    rect(im, 19, 16, 28, 24, 'hairLight');
    rect(im, 20, 24, 27, 26, 'skin');
  } else if (dir === 'east') {
    rect(im, 18, 12, 31, 26, hair);
    rect(im, 20, 15, 31, 24, 'skin');
    rect(im, 30, 18, 34, 21, 'skinLight');
    rect(im, 20, 13, 29, 16, 'hairLight');
  } else if (dir === 'west') {
    rect(im, 16, 12, 29, 26, hair);
    rect(im, 16, 15, 27, 24, 'skin');
    rect(im, 13, 18, 17, 21, 'skinLight');
    rect(im, 18, 13, 27, 16, 'hairLight');
  } else {
    rect(im, 16, 12, 31, 26, hair);
    rect(im, 19, 15, 28, 24, 'skin');
    rect(im, 20, 19, 21, 20, 'ink');
    rect(im, 26, 19, 27, 20, 'ink');
    rect(im, 21, 22, 26, 23, 'coralDark');
    rect(im, 17, 12, 30, 15, 'hairLight');
  }
}
function legs(im, trousers) {
  rect(im, 20, 57, 26, 75, trousers);
  rect(im, 27, 57, 32, 75, trousers);
  rect(im, 18, 74, 27, 77, 'ink');
  rect(im, 27, 74, 35, 77, 'ink');
}
function torso(im, shirt, robe = false) {
  if (robe)
    poly(
      im,
      [
        [16, 30],
        [31, 30],
        [36, 59],
        [12, 59],
      ],
      shirt,
    );
  else
    poly(
      im,
      [
        [17, 31],
        [30, 31],
        [34, 58],
        [14, 58],
      ],
      shirt,
    );
  rect(im, 18, 39, 29, 42, shirt === 'mint' ? 'mintDark' : 'coralDark');
}
function arms(im, dir, pose, sleeve) {
  if (pose === 'receive-diploma') {
    rect(im, 11, 35, 18, 50, sleeve);
    rect(im, 29, 35, 36, 50, sleeve);
    rect(im, 14, 48, 33, 54, 'skinLight');
  } else if (pose === 'present-diploma') {
    if (dir === 'east') {
      rect(im, 28, 34, 43, 40, sleeve);
      rect(im, 40, 37, 46, 42, 'skinLight');
    } else if (dir === 'west') {
      rect(im, 4, 34, 19, 40, sleeve);
      rect(im, 2, 37, 8, 42, 'skinLight');
    } else {
      rect(im, 11, 35, 18, 49, sleeve);
      rect(im, 29, 35, 36, 49, sleeve);
      rect(im, 14, 47, 34, 53, 'skinLight');
    }
  } else if (pose === 'cheer') {
    rect(im, 10, 29, 16, 46, sleeve);
    rect(im, 30, 28, 36, 45, sleeve);
    rect(im, 8, 25, 14, 32, 'skinLight');
    rect(im, 32, 24, 38, 31, 'skinLight');
  } else if (pose === 'hold-flowers') {
    rect(im, 11, 35, 18, 52, sleeve);
    rect(im, 29, 35, 36, 52, sleeve);
    rect(im, 14, 49, 33, 55, 'skinLight');
  } else {
    rect(im, 11, 35, 17, 53, sleeve);
    rect(im, 29, 35, 35, 53, sleeve);
    rect(im, 13, 50, 18, 56, 'skinLight');
    rect(im, 28, 50, 33, 56, 'skinLight');
  }
}
function diploma(im, dir) {
  if (dir === 'east') outlineRect(im, 37, 38, 46, 47, 'paper');
  else if (dir === 'west') outlineRect(im, 2, 38, 11, 47, 'paper');
  else outlineRect(im, 17, 48, 30, 53, 'paper');
  rect(im, 21, 49, 26, 50, 'gold');
}
function flowers(im) {
  rect(im, 22, 49, 24, 61, 'wood');
  rect(im, 17, 47, 22, 52, 'mint');
  rect(im, 24, 46, 29, 51, 'coral');
  rect(im, 20, 44, 25, 49, 'gold');
}
function makeActor(actor, dir, pose) {
  const im = image();
  ground(im);
  if (actor === 'graduate') {
    head(im, dir, 'hair');
    torso(im, 'sky', true);
    legs(im, 'lavender');
    arms(im, dir, pose, 'sky');
    if (pose === 'receive-diploma') diploma(im, dir);
    if (pose === 'cheer') {
      rect(im, 8, 20, 10, 24, 'gold');
      rect(im, 37, 19, 39, 23, 'gold');
    }
  } else if (actor === 'family-supporter') {
    head(im, dir, 'hairLight');
    torso(im, pose === 'hold-flowers' ? 'coral' : 'mint');
    legs(im, 'coralDark');
    arms(im, dir, pose, 'coral');
    if (pose === 'hold-flowers') flowers(im);
    if (pose === 'cheer') {
      rect(im, 8, 21, 10, 25, 'gold');
      rect(im, 37, 20, 39, 24, 'gold');
    }
  } else {
    head(im, dir, 'hair');
    torso(im, pose === 'present-diploma' ? 'lavender' : 'mint');
    legs(im, 'sky');
    arms(im, dir, pose, 'lavender');
    if (pose === 'present-diploma') diploma(im, dir);
    if (pose === 'cheer') {
      rect(im, 8, 20, 10, 24, 'gold');
      rect(im, 37, 19, 39, 23, 'gold');
    }
  }
  return im;
}
const specs = [
  {
    id: 'graduate',
    label: 'Graduate',
    poses: ['stand', 'receive-diploma', 'cheer'],
  },
  {
    id: 'family-supporter',
    label: 'Family supporter',
    poses: ['stand', 'hold-flowers', 'cheer'],
  },
  {
    id: 'teacher',
    label: 'Teacher',
    poses: ['stand', 'present-diploma', 'cheer'],
  },
];
function ensure(d) {
  fs.mkdirSync(d, { recursive: true });
}
function writePng(png, file) {
  fs.writeFileSync(file, PNG.sync.write(png));
}
function sha(file) {
  return crypto
    .createHash('sha256')
    .update(fs.readFileSync(file))
    .digest('hex');
}
function main() {
  ensure(ROOT);
  const atlas = new PNG({ width: ATLAS.width, height: ATLAS.height });
  atlas.data.fill(0);
  const frames = [];
  let index = 0;
  for (const actor of specs) {
    const dir = path.join(ROOT, actor.id);
    ensure(dir);
    for (const pose of actor.poses)
      for (const direction of DIRECTIONS) {
        const png = makeActor(actor.id, direction, pose);
        const name = `${actor.id}-${pose}-${direction}.png`;
        const file = path.join(dir, name);
        writePng(png, file);
        const col = index % ATLAS.columns;
        const row = Math.floor(index / ATLAS.columns);
        PNG.bitblt(
          png,
          atlas,
          0,
          0,
          FRAME.width,
          FRAME.height,
          col * FRAME.width,
          row * FRAME.height,
        );
        frames.push({
          actor: actor.id,
          pose,
          direction,
          file: `${actor.id}/${name}`,
          atlasCell: { column: col, row },
          width: FRAME.width,
          height: FRAME.height,
          pivot: { x: 24, y: 79, kind: 'bottom-center' },
          actorSafeAnchor: { x: 156, y: 216 },
          runtimeReady: false,
        });
        index += 1;
      }
  }
  const atlasFile = path.join(ROOT, 'graduation-actors-atlas.png');
  writePng(atlas, atlasFile);
  const preview = new PNG({
    width: ATLAS.width * PREVIEW_SCALE,
    height: ATLAS.height * PREVIEW_SCALE,
  });
  preview.data.fill(0);
  for (let y = 0; y < atlas.height; y += 1)
    for (let x = 0; x < atlas.width; x += 1) {
      const i = (atlas.width * y + x) << 2;
      for (let dy = 0; dy < PREVIEW_SCALE; dy += 1)
        for (let dx = 0; dx < PREVIEW_SCALE; dx += 1) {
          const j =
            (preview.width * (y * PREVIEW_SCALE + dy) +
              x * PREVIEW_SCALE +
              dx) <<
            2;
          preview.data[j] = atlas.data[i];
          preview.data[j + 1] = atlas.data[i + 1];
          preview.data[j + 2] = atlas.data[i + 2];
          preview.data[j + 3] = atlas.data[i + 3];
        }
    }
  const previewFile = path.join(ROOT, 'graduation-actors-preview-2x.png');
  writePng(preview, previewFile);
  const files = [
    ...frames.map((f) => f.file),
    'graduation-actors-atlas.png',
    'graduation-actors-preview-2x.png',
  ].sort();
  const manifest = {
    schema: 'liveit.pixel.exclusive-scene-graduation-actors.v1',
    generatedBy: 'build_graduation_actors.js',
    runtimeReady: false,
    conceptQuality:
      'isolated concept studies; requires manual pixel cleanup and compositing review',
    scene: 'garden-graduation',
    canvas: { frame: FRAME, atlas: ATLAS, previewScale: PREVIEW_SCALE },
    directions: DIRECTIONS,
    sceneAnchor: {
      x: 156,
      y: 216,
      pivot: 'bottom-center',
      dialogueSafeRegion: { x: 42, y: 232, width: 236, height: 24 },
    },
    actors: specs.map((a) => ({
      id: a.id,
      label: a.label,
      poses: a.poses,
      runtimeReady: false,
    })),
    frames: frames.map((f) => ({ ...f, sha256: sha(path.join(ROOT, f.file)) })),
    files: files.map((f) => {
      const p = path.join(ROOT, f);
      const img = PNG.sync.read(fs.readFileSync(p));
      return {
        file: f,
        width: img.width,
        height: img.height,
        colorMode: 'RGBA',
        alpha: true,
        sha256: sha(p),
        runtimeReady: false,
      };
    }),
    provenance: {
      authoredInRepo: true,
      thirdPartyAssetsUsed: false,
      suppliedArchivesUsed: false,
      externalReferencesUsed: false,
      sourceReferences: [
        'exclusive-scene-depth-v2/graduation-preview-derived.png',
        'exclusive-scenes-v2/garden-graduation-layout-guide.png',
      ],
      sourceReferencesUse:
        'scene anchor and palette conventions only; no source pixels copied',
      date: '2026-10-20',
    },
  };
  fs.writeFileSync(
    path.join(ROOT, 'manifest.json'),
    `${JSON.stringify(manifest, null, 2)}\n`,
  );
  fs.writeFileSync(
    path.join(ROOT, 'hashes.sha256'),
    `${files.map((f) => `${sha(path.join(ROOT, f))}  ${f}`).join('\n')}\n`,
  );
}
main();
