#!/usr/bin/env node
/* global __dirname, require */
/* eslint-disable @typescript-eslint/no-require-imports */

/**
 * Build original, transparent pixel actor staging studies for the existing
 * new-parenthood and elder-legacy scene concepts. The renderer is deliberately
 * small and deterministic: integer rectangles/polygons, no fonts, no external
 * images and no resampling. Existing scene art is used only for palette and
 * staging reference; this batch does not read or rewrite it.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { PNG } = require('pngjs');

const ROOT = __dirname;
const FRAME = { width: 48, height: 80 };
const ATLAS = { columns: 8, rows: 6, width: 384, height: 480 };
const PREVIEW_SCALE = 2;

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

function rgba(color) {
  return P[color] || color;
}
function set(im, x, y, color) {
  if (x < 0 || y < 0 || x >= im.width || y >= im.height) return;
  const i = (im.width * y + x) << 2;
  const c = rgba(color);
  im.data[i] = c[0];
  im.data[i + 1] = c[1];
  im.data[i + 2] = c[2];
  im.data[i + 3] = c[3];
}
function rect(im, x0, y0, x1, y1, color) {
  for (let y = y0; y <= y1; y += 1)
    for (let x = x0; x <= x1; x += 1) set(im, x, y, color);
}
function poly(im, points, color) {
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
        set(im, x, y, color);
  }
}
function outlineRect(im, x0, y0, x1, y1, fill, outline = 'ink') {
  rect(im, x0, y0, x1, y1, outline);
  rect(im, x0 + 2, y0 + 2, x1 - 2, y1 - 2, fill);
}

function head(im, dir, hair = 'hair') {
  if (dir === 'north') {
    rect(im, 17, 12, 30, 25, hair);
    rect(im, 19, 16, 28, 24, P.hairLight);
    rect(im, 20, 24, 27, 26, 'skin');
  } else if (dir === 'east') {
    rect(im, 18, 12, 31, 26, hair);
    rect(im, 20, 15, 31, 24, 'skin');
    rect(im, 30, 18, 34, 21, 'skinLight');
    rect(im, 20, 13, 29, 16, P.hairLight);
  } else if (dir === 'west') {
    rect(im, 16, 12, 29, 26, hair);
    rect(im, 16, 15, 27, 24, 'skin');
    rect(im, 13, 18, 17, 21, 'skinLight');
    rect(im, 18, 13, 27, 16, P.hairLight);
  } else {
    rect(im, 16, 12, 31, 26, hair);
    rect(im, 19, 15, 28, 24, 'skin');
    rect(im, 20, 19, 21, 20, 'ink');
    rect(im, 26, 19, 27, 20, 'ink');
    rect(im, 21, 22, 26, 23, 'coralDark');
    rect(im, 17, 12, 30, 15, P.hairLight);
  }
}
function ground(im) {
  rect(im, 12, 76, 35, 78, 'shadow');
}
function legs(im, stance = 'neutral', trousers = 'coralDark') {
  if (stance === 'wide') {
    rect(im, 17, 57, 23, 74, trousers);
    rect(im, 27, 57, 33, 74, trousers);
    rect(im, 14, 74, 24, 77, 'ink');
    rect(im, 27, 74, 37, 77, 'ink');
  } else {
    rect(im, 20, 57, 26, 75, trousers);
    rect(im, 27, 57, 32, 75, trousers);
    rect(im, 18, 74, 27, 77, 'ink');
    rect(im, 27, 74, 35, 77, 'ink');
  }
}
function torso(im, shirt = 'coral', stance = 'neutral') {
  if (stance === 'seated') {
    rect(im, 15, 38, 33, 55, shirt);
    rect(im, 13, 52, 34, 61, shirt);
  } else {
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
    rect(im, 18, 34, 29, 39, shirt);
  }
  rect(im, 18, 40, 29, 42, shirt === 'mint' ? 'mintDark' : 'coralDark');
}
function arms(im, dir, pose, sleeve = 'coral') {
  if (pose === 'hold-baby') {
    rect(im, 11, 35, 17, 52, sleeve);
    rect(im, 29, 35, 35, 52, sleeve);
    rect(im, 14, 48, 33, 54, 'skinLight');
  } else if (pose === 'reach') {
    if (dir === 'east') {
      rect(im, 28, 34, 43, 40, sleeve);
      rect(im, 40, 37, 46, 42, 'skinLight');
    } else if (dir === 'west') {
      rect(im, 4, 34, 19, 40, sleeve);
      rect(im, 2, 37, 8, 42, 'skinLight');
    } else {
      rect(im, 12, 35, 18, 51, sleeve);
      rect(im, 29, 35, 35, 51, sleeve);
      rect(im, 15, 49, 33, 54, 'skinLight');
    }
  } else if (pose === 'soothe') {
    rect(im, 11, 33, 18, 50, sleeve);
    rect(im, 29, 34, 36, 50, sleeve);
    rect(im, 13, 46, 20, 53, 'skinLight');
    rect(im, 27, 46, 34, 53, 'skinLight');
  } else if (pose === 'album') {
    rect(im, 10, 38, 17, 54, sleeve);
    rect(im, 28, 37, 35, 52, sleeve);
    rect(im, 14, 49, 32, 56, 'skinLight');
  } else if (pose === 'cane') {
    rect(im, 28, 34, 35, 59, sleeve);
    rect(im, 32, 56, 36, 74, 'wood');
    rect(im, 31, 72, 39, 75, 'wood');
  } else {
    rect(im, 11, 35, 17, 53, sleeve);
    rect(im, 29, 35, 35, 53, sleeve);
    rect(im, 13, 50, 18, 56, 'skinLight');
    rect(im, 28, 50, 33, 56, 'skinLight');
  }
}
function baby(im) {
  outlineRect(im, 13, 45, 34, 59, 'lavender');
  rect(im, 17, 43, 28, 49, 'skinLight');
  rect(im, 19, 45, 20, 46, 'ink');
  rect(im, 25, 45, 26, 46, 'ink');
}

function makeActor(actor, dir, pose) {
  const im = image();
  ground(im);
  if (actor === 'parent-primary') {
    head(im, dir);
    torso(
      im,
      pose === 'hold-baby' ? 'mint' : 'coral',
      pose === 'crouch' ? 'seated' : 'neutral',
    );
    legs(im, pose === 'crouch' ? 'wide' : 'neutral', 'sky');
    arms(im, dir, pose, pose === 'hold-baby' ? 'mint' : 'coral');
    if (pose === 'hold-baby') baby(im);
  } else if (actor === 'parent-secondary') {
    head(im, dir, 'hairLight');
    torso(im, pose === 'present-card' ? 'lavender' : 'sky');
    legs(im, 'neutral', 'coralDark');
    arms(
      im,
      dir,
      pose === 'present-card'
        ? 'reach'
        : pose === 'soothe'
          ? 'soothe'
          : 'neutral',
      'sky',
    );
    if (pose === 'present-card') outlineRect(im, 35, 40, 45, 49, 'paper');
  } else if (actor === 'elder-primary') {
    head(im, dir, 'hairLight');
    torso(im, pose === 'seated-memory' ? 'seated' : 'mint');
    legs(im, pose === 'seated-memory' ? 'wide' : 'neutral', 'lavender');
    arms(
      im,
      dir,
      pose === 'cane-rest'
        ? 'cane'
        : pose === 'seated-memory'
          ? 'album'
          : 'neutral',
      'mint',
    );
    if (pose === 'seated-memory') outlineRect(im, 10, 44, 22, 53, 'wood');
    rect(im, 15, 29, 31, 31, 'cream');
  } else {
    head(im, dir);
    torso(im, pose === 'offer-letter' ? 'coral' : 'sky');
    legs(im, pose === 'kneel-album' ? 'wide' : 'neutral', 'coralDark');
    arms(
      im,
      dir,
      pose === 'kneel-album'
        ? 'album'
        : pose === 'offer-letter'
          ? 'reach'
          : 'neutral',
      'coral',
    );
    if (pose === 'offer-letter') outlineRect(im, 36, 39, 46, 47, 'paper');
  }
  return im;
}

const specs = [
  {
    scene: 'new-parenthood',
    anchor: { x: 126, y: 216 },
    actors: [
      {
        id: 'parent-primary',
        label: 'Parent primary',
        poses: ['stand', 'hold-baby', 'reach'],
      },
      {
        id: 'parent-secondary',
        label: 'Parent secondary',
        poses: ['stand', 'soothe', 'present-card'],
      },
    ],
  },
  {
    scene: 'elder-legacy',
    anchor: { x: 126, y: 216 },
    actors: [
      {
        id: 'elder-primary',
        label: 'Elder primary',
        poses: ['stand', 'seated-memory', 'cane-rest'],
      },
      {
        id: 'legacy-listener',
        label: 'Legacy listener',
        poses: ['stand', 'kneel-album', 'offer-letter'],
      },
    ],
  },
];
const directions = ['south', 'east', 'north', 'west'];

function writePng(png, file) {
  fs.writeFileSync(file, PNG.sync.write(png));
}
function sha(file) {
  return crypto
    .createHash('sha256')
    .update(fs.readFileSync(file))
    .digest('hex');
}
function ensure(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function main() {
  ensure(ROOT);
  const frameRecords = [];
  const atlas = new PNG({ width: ATLAS.width, height: ATLAS.height });
  atlas.data.fill(0);
  let atlasIndex = 0;
  for (const scene of specs) {
    const sceneDir = path.join(ROOT, scene.scene);
    ensure(sceneDir);
    for (const actor of scene.actors) {
      const actorDir = path.join(sceneDir, actor.id);
      ensure(actorDir);
      for (const pose of actor.poses)
        for (const direction of directions) {
          const png = makeActor(actor.id, direction, pose);
          const fileName = `${actor.id}-${pose}-${direction}.png`;
          const file = path.join(actorDir, fileName);
          writePng(png, file);
          const col = atlasIndex % ATLAS.columns;
          const row = Math.floor(atlasIndex / ATLAS.columns);
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
          frameRecords.push({
            scene: scene.scene,
            actor: actor.id,
            pose,
            direction,
            file: `${scene.scene}/${actor.id}/${fileName}`,
            atlasCell: { column: col, row },
            width: FRAME.width,
            height: FRAME.height,
            pivot: { x: 24, y: 79, kind: 'bottom-center' },
            actorSafeAnchor: scene.anchor,
            runtimeReady: false,
          });
          atlasIndex += 1;
        }
    }
  }
  const atlasFile = path.join(ROOT, 'actor-staging-atlas.png');
  writePng(atlas, atlasFile);
  const preview = new PNG({
    width: ATLAS.width * PREVIEW_SCALE,
    height: ATLAS.height * PREVIEW_SCALE,
  });
  preview.data.fill(0);
  PNG.bitblt(atlas, preview, 0, 0, atlas.width, atlas.height, 0, 0);
  for (let y = 0; y < atlas.height; y += 1)
    for (let x = 0; x < atlas.width; x += 1) {
      const i = (atlas.width * y + x) << 2;
      const c = [
        atlas.data[i],
        atlas.data[i + 1],
        atlas.data[i + 2],
        atlas.data[i + 3],
      ];
      for (let dy = 0; dy < PREVIEW_SCALE; dy += 1)
        for (let dx = 0; dx < PREVIEW_SCALE; dx += 1) {
          const j =
            (preview.width * (y * PREVIEW_SCALE + dy) +
              x * PREVIEW_SCALE +
              dx) <<
            2;
          preview.data[j] = c[0];
          preview.data[j + 1] = c[1];
          preview.data[j + 2] = c[2];
          preview.data[j + 3] = c[3];
        }
    }
  const previewFile = path.join(ROOT, 'actor-staging-preview-2x.png');
  writePng(preview, previewFile);
  const files = [
    ...frameRecords.map((r) => r.file),
    'actor-staging-atlas.png',
    'actor-staging-preview-2x.png',
  ].sort();
  const manifest = {
    schema: 'liveit.pixel.exclusive-scene-actor-staging.v1',
    generatedBy: 'build_actor_staging.js',
    runtimeReady: false,
    conceptQuality:
      'isolated concept studies; requires manual pixel cleanup and compositing review',
    canvas: { frame: FRAME, atlas: ATLAS, previewScale: PREVIEW_SCALE },
    directions,
    sceneAnchors: Object.fromEntries(
      specs.map((s) => [
        s.scene,
        {
          anchor: s.anchor,
          pivot: 'bottom-center',
          dialogueSafeRegion: { x: 42, y: 232, width: 236, height: 24 },
        },
      ]),
    ),
    actors: specs.flatMap((s) =>
      s.actors.map((a) => ({
        scene: s.scene,
        id: a.id,
        label: a.label,
        poses: a.poses,
        runtimeReady: false,
      })),
    ),
    frames: frameRecords.map((r) => ({
      ...r,
      sha256: sha(path.join(ROOT, r.file)),
    })),
    files: files.map((f) => {
      const p = path.join(ROOT, f);
      const pImg = PNG.sync.read(fs.readFileSync(p));
      return {
        file: f,
        width: pImg.width,
        height: pImg.height,
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
      sourceReferences: ['exclusive-scene-depth-v2', 'exclusive-scenes-v1'],
      sourceReferencesUse:
        'palette and staging conventions only; no source pixels copied',
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
