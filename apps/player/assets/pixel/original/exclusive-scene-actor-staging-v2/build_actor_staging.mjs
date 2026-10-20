#!/usr/bin/env node
// Deterministic original pixel actor and foreground-overlay concepts for four
// exclusive scene backdrops. Uses integer primitives only; no source image is
// sampled, edited, or copied into the authored assets.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';
import prettier from 'prettier';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(ROOT, '../../../../../../');
const VARIETY = path.join(
  REPO,
  'apps/player/assets/pixel/original/exclusive-scenes-variety-v1',
);
const BODY = { width: 48, height: 80 };
const BUST = { width: 64, height: 64 };
const SCENE = { width: 320, height: 256 };
const dirs = ['south', 'east', 'north', 'west'];

const palettes = {
  diner: {
    ink: '#211d35',
    shadow: '#392b43',
    skin: '#d99173',
    light: '#f2b28c',
    hair: '#433141',
    hairHi: '#79505a',
    shirt: '#dd6465',
    trim: '#a64258',
    pants: '#386a87',
    accent: '#f2b94e',
    cream: '#fff0c8',
    wood: '#794b3b',
    paper: '#fff6d9',
    green: '#5eaa82',
  },
  bus: {
    ink: '#1d2035',
    shadow: '#30394d',
    skin: '#9d634f',
    light: '#d18c69',
    hair: '#302d42',
    hairHi: '#5a5267',
    shirt: '#54899a',
    trim: '#365d72',
    pants: '#44435e',
    accent: '#e5a66f',
    cream: '#e4dfcf',
    wood: '#765b58',
    paper: '#d6dde1',
    green: '#6d958b',
  },
  harvest: {
    ink: '#292239',
    shadow: '#493347',
    skin: '#c47e61',
    light: '#efb18a',
    hair: '#3d2c36',
    hairHi: '#765147',
    shirt: '#739b62',
    trim: '#496c50',
    pants: '#56485f',
    accent: '#e2a548',
    cream: '#fae3b1',
    wood: '#82543e',
    paper: '#f4dfbf',
    green: '#8bae5b',
  },
  apartment: {
    ink: '#29253b',
    shadow: '#484054',
    skin: '#d6a17f',
    light: '#f3c39b',
    hair: '#393044',
    hairHi: '#66505b',
    shirt: '#87769c',
    trim: '#5e526f',
    pants: '#456d76',
    accent: '#db987a',
    cream: '#fae8cb',
    wood: '#795949',
    paper: '#fff1d6',
    green: '#71997c',
  },
};
const scenes = [
  {
    id: 'first-paycheck-diner',
    short: 'diner',
    actors: [
      {
        id: 'mika-first-shift',
        name: 'Mika, first-shift worker',
        skin: 'skin',
        hair: 'hair',
        hairStyle: 'curls',
        top: 'shirt',
        bottom: 'pants',
        role: 'young worker',
        poses: ['seated-counting', 'stand-proud', 'offer-coffee'],
        prompt:
          'Original young diner worker with short swept dark curls, coral work shirt, teal trousers, warm tired eyes; expressive grounded pixel bust and relaxed working-class body language.',
      },
      {
        id: 'ren-night-cook',
        name: 'Ren, night cook',
        skin: 'light',
        hair: 'hairHi',
        hairStyle: 'close-crop',
        top: 'pants',
        bottom: 'trim',
        role: 'older coworker',
        poses: ['lean-counter', 'raise-mug', 'quiet-congratulation'],
        prompt:
          'Original older diner cook with close-cropped silver-brown hair, deep blue apron over a pale shirt, kind lined face; sturdy shoulders and understated supportive gestures.',
      },
    ],
    anchors: [
      { x: 108, y: 211 },
      { x: 213, y: 211 },
    ],
    dialogue: { x: 42, y: 232, width: 236, height: 24 },
    safe: { x: 42, y: 48, width: 236, height: 164 },
    props: ['diner-stool-and-mug-overlay.png'],
  },
  {
    id: 'reconciliation-bus-stop',
    short: 'bus',
    actors: [
      {
        id: 'asha-returning-friend',
        name: 'Asha, returning friend',
        skin: 'light',
        hair: 'hair',
        hairStyle: 'tied-low',
        top: 'shirt',
        bottom: 'pants',
        role: 'returning friend',
        poses: ['umbrella-lowered', 'apology-open-hand', 'reach-tentative'],
        prompt:
          'Original returning friend in a muted teal raincoat with long dark hair tied low, rain-speckled but not wet-rendered; careful remorseful eyes and hesitant open-hand gesture.',
      },
      {
        id: 'jules-waiting-friend',
        name: 'Jules, waiting friend',
        skin: 'skin',
        hair: 'hairHi',
        hairStyle: 'cropped',
        top: 'trim',
        bottom: 'pants',
        role: 'waiting friend',
        poses: ['hands-in-pockets', 'listen-soften', 'offer-paper-cup'],
        prompt:
          'Original friend who waited through the rain, auburn cropped hair, plum scarf and slate coat, guarded expression softening into cautious welcome; avoid melodramatic tears.',
      },
    ],
    anchors: [
      { x: 105, y: 211 },
      { x: 215, y: 211 },
    ],
    dialogue: { x: 42, y: 232, width: 236, height: 24 },
    safe: { x: 52, y: 76, width: 216, height: 136 },
    props: ['bus-stop-puddle-paper-cup-overlay.png'],
  },
  {
    id: 'harvest-table-garden',
    short: 'harvest',
    actors: [
      {
        id: 'noor-garden-host',
        name: 'Noor, garden host',
        skin: 'skin',
        hair: 'hairHi',
        hairStyle: 'headwrap',
        top: 'green',
        bottom: 'pants',
        role: 'garden host',
        poses: ['pass-bowl', 'welcome-wave', 'lift-toast'],
        prompt:
          'Original middle-aged garden host with a salt-and-pepper headwrap, leaf-green cardigan, bright attentive face and generous open posture.',
      },
      {
        id: 'eli-neighbor',
        name: 'Eli, garden neighbor',
        skin: 'light',
        hair: 'hair',
        hairStyle: 'locs',
        top: 'accent',
        bottom: 'trim',
        role: 'neighbor',
        poses: ['carry-produce', 'laugh-shoulders', 'share-bread'],
        prompt:
          'Original young adult neighbor with warm brown locs gathered back, amber overshirt and dark plum trousers; joyful but natural smile, carrying the shared meal.',
      },
    ],
    anchors: [
      { x: 105, y: 211 },
      { x: 215, y: 211 },
    ],
    dialogue: { x: 42, y: 232, width: 236, height: 24 },
    safe: { x: 42, y: 52, width: 236, height: 160 },
    props: ['garden-crate-and-leaves-overlay.png'],
  },
  {
    id: 'fresh-start-apartment',
    short: 'apartment',
    actors: [
      {
        id: 'sam-new-tenant',
        name: 'Sam, new tenant',
        skin: 'light',
        hair: 'hair',
        hairStyle: 'bob',
        top: 'shirt',
        bottom: 'pants',
        role: 'new tenant',
        poses: ['unpack-box', 'hold-key-to-light', 'water-first-plant'],
        prompt:
          'Original newly single tenant with soft black bob, lavender sweater and teal trousers; calm agency replacing sadness, expressive brows and practical gentle posture.',
      },
      {
        id: 'bea-neighbor',
        name: 'Bea, neighbor',
        skin: 'skin',
        hair: 'hairHi',
        hairStyle: 'texture',
        top: 'green',
        bottom: 'trim',
        role: 'neighbor',
        poses: ['knock-gently', 'offer-plant', 'sit-near-window'],
        prompt:
          'Original friendly neighbor with short textured copper hair, muted sage cardigan and plum skirt; quiet welcoming expression, hands offering a small plant.',
      },
    ],
    anchors: [
      { x: 106, y: 211 },
      { x: 214, y: 211 },
    ],
    dialogue: { x: 42, y: 232, width: 236, height: 24 },
    safe: { x: 52, y: 56, width: 216, height: 156 },
    props: ['apartment-box-and-plant-overlay.png'],
  },
];

const rgba = (hex) => [
  ...hex
    .slice(1)
    .match(/../g)
    .map((v) => parseInt(v, 16)),
  255,
];
const mk = ({ width, height }) => {
  const p = new PNG({ width, height });
  p.data.fill(0);
  return p;
};
function px(im, x, y, color) {
  if (x < 0 || y < 0 || x >= im.width || y >= im.height) return;
  const i = (im.width * y + x) * 4,
    c = typeof color === 'string' ? rgba(color) : color;
  im.data[i] = c[0];
  im.data[i + 1] = c[1];
  im.data[i + 2] = c[2];
  im.data[i + 3] = c[3] ?? 255;
}
function rect(im, x0, y0, x1, y1, c) {
  for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) px(im, x, y, c);
}
function ell(im, cx, cy, rx, ry, c) {
  for (let y = -ry; y <= ry; y++)
    for (let x = -rx; x <= rx; x++)
      if (x * x * ry * ry + y * y * rx * rx <= rx * rx * ry * ry)
        px(im, cx + x, cy + y, c);
}
function poly(im, points, c) {
  const ys = points.map((p) => p[1]);
  for (let y = Math.min(...ys); y <= Math.max(...ys); y++) {
    const xs = [];
    for (let i = 0, j = points.length - 1; i < points.length; j = i++) {
      const [x1, y1] = points[i],
        [x2, y2] = points[j];
      if (y1 > y !== y2 > y) xs.push(x1 + ((y - y1) * (x2 - x1)) / (y2 - y1));
    }
    xs.sort((a, b) => a - b);
    for (let i = 0; i + 1 < xs.length; i += 2)
      for (let x = Math.ceil(xs[i]); x <= Math.floor(xs[i + 1]); x++)
        px(im, x, y, c);
  }
}
function actorPixels(im, pal, actor, pose, dir, bust = false) {
  const cx = bust ? 32 : 24,
    headY = bust ? 8 : 9;
  if (!bust) ell(im, cx, 77, 13, 2, pal.shadow);
  // Character-specific hair mass and face, with four readable orientations.
  ell(im, cx, headY + 7, bust ? 15 : 9, bust ? 15 : 10, pal[actor.hair]);
  const hairHi = pal[actor.hairHi || actor.hair];
  if (actor.hairStyle === 'curls' || actor.hairStyle === 'texture') {
    for (const [x, y, r] of [
      [-7, 0, 3],
      [-2, -2, 3],
      [4, -1, 3],
      [8, 2, 2],
    ])
      ell(im, cx + x, headY + y, r, r, hairHi);
  }
  if (actor.hairStyle === 'close-crop')
    rect(im, cx - 7, headY - 2, cx + 7, headY + 3, hairHi);
  if (actor.hairStyle === 'tied-low') {
    rect(im, cx - 9, headY + 2, cx - 6, headY + 16, pal[actor.hair]);
    ell(im, cx - 8, headY + 17, 3, 3, hairHi);
  }
  if (actor.hairStyle === 'cropped')
    rect(im, cx - 9, headY + 1, cx - 5, headY + 10, hairHi);
  if (actor.hairStyle === 'headwrap') {
    rect(im, cx - 9, headY + 1, cx + 9, headY + 4, pal.accent);
    rect(im, cx - 8, headY + 5, cx + 8, headY + 6, hairHi);
  }
  if (actor.hairStyle === 'locs') {
    for (const x of [-7, -3, 2, 6])
      rect(im, cx + x, headY + 2, cx + x + 1, headY + 13, pal[actor.hair]);
  }
  if (actor.hairStyle === 'bob') {
    rect(im, cx - 10, headY + 2, cx - 8, headY + 19, pal[actor.hair]);
    rect(im, cx + 8, headY + 2, cx + 10, headY + 19, pal[actor.hair]);
  }
  if (dir === 'north') rect(im, cx - 7, headY + 1, cx + 7, headY + 14, hairHi);
  else {
    ell(im, cx, headY + 9, bust ? 10 : 6, bust ? 10 : 7, pal[actor.skin]);
    if (dir === 'east')
      rect(im, cx + 4, headY + 8, cx + 10, headY + 10, pal[actor.skin]);
    if (dir === 'west')
      rect(im, cx - 10, headY + 8, cx - 4, headY + 10, pal[actor.skin]);
    rect(
      im,
      cx - (bust ? 8 : 5),
      headY - 3,
      cx + (bust ? 8 : 5),
      headY + 1,
      hairHi,
    );
    if (dir === 'south') {
      rect(im, cx - 4, headY + 8, cx - 3, headY + 9, pal.ink);
      rect(im, cx + 3, headY + 8, cx + 4, headY + 9, pal.ink);
      rect(im, cx - 2, headY + 12, cx + 2, headY + 12, pal.trim);
    }
    if (dir === 'east') rect(im, cx + 5, headY + 8, cx + 6, headY + 9, pal.ink);
    if (dir === 'west') rect(im, cx - 6, headY + 8, cx - 5, headY + 9, pal.ink);
  }
  const top = bust ? 25 : 27,
    bot = bust ? 63 : 56;
  if (bust) {
    poly(
      im,
      [
        [cx - 23, 63],
        [cx - 19, top + 7],
        [cx - 10, top],
        [cx + 10, top],
        [cx + 19, top + 7],
        [cx + 23, 63],
      ],
      pal[actor.top],
    );
    rect(im, cx - 4, top + 9, cx + 4, top + 14, pal[actor.skin]);
  } else {
    poly(
      im,
      [
        [cx - 8, top],
        [cx + 8, top],
        [cx + 12, bot],
        [cx - 12, bot],
      ],
      pal[actor.top],
    );
    if (pose === 'seated-counting' || pose === 'sit-near-window') {
      rect(im, cx - 14, 48, cx + 14, 54, pal[actor.top]);
      rect(im, cx - 12, 56, cx - 6, 70, pal[actor.bottom]);
      rect(im, cx + 5, 56, cx + 11, 70, pal[actor.bottom]);
    } else {
      rect(im, cx - 8, bot, cx - 2, 73, pal[actor.bottom]);
      rect(im, cx + 2, bot, cx + 8, 73, pal[actor.bottom]);
      rect(im, cx - 10, 73, cx - 1, 76, pal.ink);
      rect(im, cx + 2, 73, cx + 11, 76, pal.ink);
    }
    // Silhouette-changing gestures, all contained inside the 48x80 cell.
    const hand = pal.light;
    if (
      /offer|pass|share|reach|toast|cup|plant|key|wave|carry|box/.test(pose)
    ) {
      rect(im, cx + 7, 34, cx + 17, 38, pal[actor.top]);
      rect(im, cx + 15, 35, cx + 20, 39, hand);
    } else if (/knock|apology/.test(pose)) {
      rect(im, cx + 7, 32, cx + 13, 43, pal[actor.top]);
      rect(im, cx + 11, 31, cx + 16, 35, hand);
    } else {
      rect(im, cx - 13, 33, cx - 8, 48, pal[actor.top]);
      rect(im, cx + 8, 33, cx + 13, 48, pal[actor.top]);
      rect(im, cx - 14, 46, cx - 9, 50, hand);
      rect(im, cx + 9, 46, cx + 14, 50, hand);
    }
    if (
      pose === 'offer-coffee' ||
      pose === 'raise-mug' ||
      pose === 'offer-paper-cup'
    ) {
      rect(im, cx + 17, 32, cx + 21, 35, pal.cream);
      rect(im, cx + 18, 31, cx + 20, 31, pal.accent);
    }
    if (pose === 'hold-key-to-light') {
      rect(im, cx + 17, 33, cx + 20, 36, pal.accent);
      px(im, cx + 21, 32, pal.accent);
    }
    if (pose === 'umbrella-lowered') {
      rect(im, cx - 17, 28, cx - 16, 67, pal.wood);
      ell(im, cx - 16, 29, 8, 4, pal[actor.top]);
    }
    if (pose === 'carry-produce' || pose === 'unpack-box') {
      rect(im, cx + 14, 42, cx + 22, 49, pal.wood);
      rect(im, cx + 16, 40, cx + 18, 42, pal.green);
    }
  }
  if (bust && dir === 'south') {
    rect(im, cx - 6, headY + 8, cx - 4, headY + 10, pal.ink);
    rect(im, cx + 4, headY + 8, cx + 6, headY + 10, pal.ink);
  }
}
function makeBody(scene, actor, pose, dir) {
  const p = mk(BODY);
  actorPixels(p, palettes[scene.short], actor, pose, dir);
  return p;
}
function makeBust(scene, actor, dir) {
  const p = mk(BUST);
  actorPixels(p, palettes[scene.short], actor, 'portrait', dir, true);
  return p;
}
function makeProp(scene) {
  const p = mk(SCENE),
    pal = palettes[scene.short];
  if (scene.short === 'diner') {
    rect(p, 16, 207, 61, 212, pal.wood);
    rect(p, 21, 212, 25, 229, pal.wood);
    rect(p, 52, 212, 56, 229, pal.wood);
    rect(p, 83, 217, 96, 219, pal.ink);
    rect(p, 87, 214, 92, 217, pal.cream);
    rect(p, 87, 213, 92, 213, pal.accent);
  }
  if (scene.short === 'bus') {
    poly(
      p,
      [
        [12, 222],
        [35, 218],
        [53, 223],
        [42, 227],
        [19, 227],
      ],
      pal.shadow,
    );
    rect(p, 68, 218, 74, 224, pal.paper);
    rect(p, 71, 216, 76, 218, pal.accent);
    rect(p, 72, 214, 76, 216, pal.cream);
  }
  if (scene.short === 'harvest') {
    rect(p, 14, 217, 46, 229, pal.wood);
    rect(p, 18, 214, 39, 217, pal.accent);
    rect(p, 22, 210, 27, 214, pal.green);
    ell(p, 27, 210, 3, 2, pal.accent);
    rect(p, 55, 225, 64, 230, pal.green);
    rect(p, 59, 219, 60, 226, pal.green);
  }
  if (scene.short === 'apartment') {
    rect(p, 12, 214, 48, 230, pal.wood);
    rect(p, 16, 210, 44, 214, pal.paper);
    rect(p, 79, 223, 91, 230, pal.wood);
    rect(p, 84, 216, 86, 225, pal.green);
    ell(p, 82, 216, 4, 4, pal.green);
    ell(p, 89, 218, 4, 3, pal.accent);
  }
  return p;
}
function write(file, p) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, PNG.sync.write(p));
}
function sha(file) {
  return crypto
    .createHash('sha256')
    .update(fs.readFileSync(file))
    .digest('hex');
}
function alphaAndPalette(p) {
  const colors = new Set();
  let binary = true,
    transparent = 0;
  for (let i = 0; i < p.data.length; i += 4) {
    const a = p.data[i + 3];
    if (a === 0) {
      transparent++;
      if (p.data[i] || p.data[i + 1] || p.data[i + 2])
        throw Error('nonzero RGB under transparent pixel');
    } else if (a !== 255) binary = false;
    colors.add(`${p.data[i]},${p.data[i + 1]},${p.data[i + 2]},${a}`);
  }
  return { binary, transparent, colors: colors.size };
}
function blit(src, dst, dx, dy) {
  for (let y = 0; y < src.height; y++)
    for (let x = 0; x < src.width; x++) {
      const i = (y * src.width + x) * 4,
        a = src.data[i + 3];
      if (!a) continue;
      const tx = dx + x,
        ty = dy + y;
      if (tx < 0 || ty < 0 || tx >= dst.width || ty >= dst.height) continue;
      const j = (ty * dst.width + tx) * 4;
      const da = dst.data[j + 3] / 255,
        sa = a / 255,
        out = sa + da * (1 - sa);
      for (let c = 0; c < 3; c++)
        dst.data[j + c] = Math.round(
          (src.data[i + c] * sa + dst.data[j + c] * da * (1 - sa)) / out,
        );
      dst.data[j + 3] = Math.round(out * 255);
    }
}
function nearest2(src) {
  const dst = mk({ width: src.width * 2, height: src.height * 2 });
  for (let y = 0; y < src.height; y++)
    for (let x = 0; x < src.width; x++) {
      const i = (y * src.width + x) * 4;
      for (let yy = 0; yy < 2; yy++)
        for (let xx = 0; xx < 2; xx++) {
          const j = ((y * 2 + yy) * dst.width + x * 2 + xx) * 4;
          src.data.copy(dst.data, j, i, i + 4);
        }
    }
  return dst;
}
async function build() {
  const frames = [],
    busts = [],
    files = [],
    fileInfo = [];
  const varietyManifest = JSON.parse(
    fs.readFileSync(path.join(VARIETY, 'manifest.json'), 'utf8'),
  );
  const backdropReferences = varietyManifest.scenes.map((s) => ({
    scene: s.id,
    file: s.files.find((x) => x.role === '32-color-320x256-concept').file,
    sha256: s.files.find((x) => x.role === '32-color-320x256-concept').sha256,
    runtimeReady: false,
  }));
  for (const s of scenes) {
    s.actors.forEach((a, ai) => {
      for (const pose of a.poses)
        for (const dir of dirs) {
          const rel = `frames/${s.id}/${a.id}/${pose}-${dir}.png`,
            p = makeBody(s, a, pose, dir),
            f = path.join(ROOT, rel);
          write(f, p);
          frames.push({
            scene: s.id,
            actor: a.id,
            pose,
            direction: dir,
            file: rel,
            width: BODY.width,
            height: BODY.height,
            pivot: { x: 24, y: 79, kind: 'bottom-center' },
            anchor: s.anchors[ai],
            runtimeReady: false,
          });
          files.push(rel);
        }
      for (const dir of dirs) {
        const rel = `portraits/${s.id}/${a.id}-bust-${dir}.png`,
          p = makeBust(s, a, dir),
          f = path.join(ROOT, rel);
        write(f, p);
        busts.push({
          scene: s.id,
          actor: a.id,
          direction: dir,
          file: rel,
          width: BUST.width,
          height: BUST.height,
          pivot: { x: 32, y: 63, kind: 'bottom-center' },
          runtimeReady: false,
        });
        files.push(rel);
      }
    });
    const rel = `overlays/${s.id}/${s.props[0]}`,
      p = makeProp(s),
      f = path.join(ROOT, rel);
    write(f, p);
    files.push(rel);
  }
  const atlas = mk({
    width: BODY.width * 8,
    height: BODY.height * Math.ceil(frames.length / 8),
  });
  frames.forEach((r, i) =>
    PNG.bitblt(
      PNG.sync.read(fs.readFileSync(path.join(ROOT, r.file))),
      atlas,
      0,
      0,
      BODY.width,
      BODY.height,
      (i % 8) * BODY.width,
      Math.floor(i / 8) * BODY.height,
    ),
  );
  write(path.join(ROOT, 'actor-staging-atlas.png'), atlas);
  files.push('actor-staging-atlas.png');
  const bustColumns = 8;
  const bustAtlas = mk({
    width: BUST.width * bustColumns,
    height: BUST.height * Math.ceil(busts.length / bustColumns),
  });
  busts.forEach((r, i) =>
    PNG.bitblt(
      PNG.sync.read(fs.readFileSync(path.join(ROOT, r.file))),
      bustAtlas,
      0,
      0,
      BUST.width,
      BUST.height,
      (i % bustColumns) * BUST.width,
      Math.floor(i / bustColumns) * BUST.height,
    ),
  );
  write(path.join(ROOT, 'portrait-atlas.png'), bustAtlas);
  files.push('portrait-atlas.png');
  // Review composite only: reads concept exports as a backdrop, then layers
  // staged actors and the separately-authored low foreground props.
  const board = mk({ width: SCENE.width * 4, height: SCENE.height * 4 });
  scenes.forEach((s, si) => {
    const bg = PNG.sync.read(
      fs.readFileSync(path.join(VARIETY, 'scenes', `${s.id}-32c-320x256.png`)),
    );
    const panel = mk(SCENE);
    blit(bg, panel, 0, 0);
    s.actors.forEach((a, ai) => {
      const f = path.join(
        ROOT,
        `frames/${s.id}/${a.id}/${a.poses[0]}-south.png`,
      );
      blit(
        PNG.sync.read(fs.readFileSync(f)),
        panel,
        s.anchors[ai].x - 24,
        s.anchors[ai].y - 79,
      );
    });
    blit(
      PNG.sync.read(
        fs.readFileSync(path.join(ROOT, `overlays/${s.id}/${s.props[0]}`)),
      ),
      panel,
      0,
      0,
    );
    const scaled = nearest2(panel);
    const ox = (si % 2) * 640,
      oy = Math.floor(si / 2) * 512;
    PNG.bitblt(scaled, board, 0, 0, scaled.width, scaled.height, ox, oy);
  });
  write(path.join(ROOT, 'actor-staging-review-2x.png'), board);
  files.push('actor-staging-review-2x.png');
  for (const file of files) {
    const p = PNG.sync.read(fs.readFileSync(path.join(ROOT, file))),
      v = alphaAndPalette(p);
    fileInfo.push({
      file,
      width: p.width,
      height: p.height,
      colorMode: 'RGBA',
      alpha: true,
      alphaMode: v.binary ? 'binary' : 'UNEXPECTED',
      transparentPixels: v.transparent,
      paletteColors: v.colors,
      sha256: sha(path.join(ROOT, file)),
      runtimeReady: false,
    });
  }
  const manifest = {
    schema: 'liveit.pixel.exclusive-scene-actor-staging.v2',
    batch: 'exclusive-scene-actor-staging-v2',
    generatedBy: 'build_actor_staging.mjs',
    canvas: { scene: SCENE, bodyFrame: BODY, portraitFrame: BUST },
    paletteLimit: 32,
    runtimeReady: false,
    backdropReferences,
    scenes: scenes.map((s) => ({
      id: s.id,
      actors: s.actors.map((a) => ({
        id: a.id,
        name: a.name,
        role: a.role,
        poses: a.poses,
        portraitDirections: dirs,
        runtimeReady: false,
      })),
      actorSafeRegion: s.safe,
      dialogueSafeRegion: s.dialogue,
      placements: s.actors.map((a, i) => ({
        actor: a.id,
        anchor: s.anchors[i],
        pivot: 'bottom-center',
        zOrder: 'actors',
        runtimeReady: false,
      })),
      foregroundOverlays: [
        {
          file: `overlays/${s.id}/${s.props[0]}`,
          placement: { x: 0, y: 0 },
          zOrder: 'foreground-over-actors',
          dialogueSafeRegion: s.dialogue,
          runtimeReady: false,
        },
      ],
      runtimeReady: false,
    })),
    directions: dirs,
    frames,
    busts,
    files: fileInfo,
    previews: [
      {
        file: 'actor-staging-review-2x.png',
        role: 'backdrop-composite-review-only',
        width: 1280,
        height: 1024,
        panelArrangement: '2x2',
        runtimeReady: false,
      },
    ],
    provenance: {
      authoredInRepo: true,
      method:
        'deterministic integer pixel primitives; source images are not sampled into authored sprites',
      sourceConventions: [
        'exclusive-scenes-variety-v1 scene ids, actor-safe regions, dialogue-safe regions, palette mood only',
        'exclusive-scene-actor-staging-v1 RGBA and bottom-centre pivot convention',
      ],
      promptRecord: 'prompts.md',
      thirdPartyAssetsUsed: false,
      suppliedArchivesUsed: false,
      downloadedAssetsUsed: false,
      externalReferencesUsed: false,
      date: '2026-10-20',
    },
  };
  const formattedManifest = await prettier.format(JSON.stringify(manifest), {
    parser: 'json',
  });
  fs.writeFileSync(path.join(ROOT, 'manifest.json'), formattedManifest);
  fs.writeFileSync(
    path.join(ROOT, 'hashes.sha256'),
    fileInfo
      .map((x) => `${x.sha256}  ${x.file}`)
      .sort()
      .join('\n') + '\n',
  );
}
await build();
