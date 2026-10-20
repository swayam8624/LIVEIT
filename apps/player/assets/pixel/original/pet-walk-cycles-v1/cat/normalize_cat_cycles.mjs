/* global URL */
import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

const root = path.dirname(new URL(import.meta.url).pathname);
const sourcePath = path.join(root, 'cat-walk-cycles-source.png');
const directions = ['south', 'west', 'east', 'north'];
const phases = ['contact-a', 'passing-a', 'contact-b', 'passing-b'];
const frameWidth = 96;
const frameHeight = 128;
const contentWidth = 88;
const contentHeight = 120;

const source = await sharp(sourcePath).metadata();
if (!source.width || !source.height || !source.hasAlpha) {
  throw new Error('Cat source must be a readable RGBA PNG.');
}
const { data, info } = await sharp(sourcePath)
  .ensureAlpha()
  .raw()
  .toBuffer({ resolveWithObject: true });

const occupiedRows = [];
for (let y = 0; y < info.height; y += 1) {
  let occupied = false;
  for (let x = 0; x < info.width; x += 1) {
    if (data[(y * info.width + x) * 4 + 3] > 10) {
      occupied = true;
      break;
    }
  }
  if (occupied) occupiedRows.push(y);
}

const rowBounds = [];
let rowStart = occupiedRows[0];
let previous = occupiedRows[0];
for (const y of occupiedRows.slice(1)) {
  if (y > previous + 1) {
    rowBounds.push([rowStart, previous + 1]);
    rowStart = y;
  }
  previous = y;
}
rowBounds.push([rowStart, previous + 1]);
if (rowBounds.length !== 4) {
  throw new Error(`Expected four occupied row bands, got ${rowBounds.length}.`);
}

const cellSourceWidth = info.width / 4;
const frames = [];
const framesRoot = path.join(root, 'frames');
await fs.mkdir(framesRoot, { recursive: true });

for (let row = 0; row < 4; row += 1) {
  for (let column = 0; column < 4; column += 1) {
    const left = Math.round(column * cellSourceWidth);
    const right = Math.round((column + 1) * cellSourceWidth);
    const [top, bottom] = rowBounds[row];
    const direction = directions[row];
    const phase = phases[column];
    const id = `cat-${direction}-${phase}`;
    const file = `frames/${id}.png`;
    const trimmed = await sharp(sourcePath)
      .extract({ left, top, width: right - left, height: bottom - top })
      .resize({
        width: contentWidth,
        height: contentHeight,
        fit: 'fill',
        kernel: 'nearest',
      })
      .png()
      .toBuffer();
    await sharp({
      create: {
        width: frameWidth,
        height: frameHeight,
        channels: 4,
        background: { r: 0, g: 0, b: 0, alpha: 0 },
      },
    })
      .composite([{ input: trimmed, left: 4, top: 4 }])
      .png()
      .toFile(path.join(root, file));
    frames.push({
      id,
      direction,
      phase,
      file,
      x: column * frameWidth,
      y: row * frameHeight,
      width: frameWidth,
      height: frameHeight,
      pivot: { x: 48, y: 124 },
      runtimeReady: false,
      limitations: [
        'AI-generated movement concept; requires pixel cleanup, timing, collision-box review, and renderer validation.',
      ],
    });
  }
}

await sharp({
  create: {
    width: frameWidth * 4,
    height: frameHeight * 4,
    channels: 4,
    background: { r: 0, g: 0, b: 0, alpha: 0 },
  },
})
  .composite(
    frames.map((frame) => ({
      input: path.join(root, frame.file),
      left: frame.x,
      top: frame.y,
    })),
  )
  .png()
  .toFile(path.join(root, 'cat-walk-cycles-atlas.png'));

await sharp(path.join(root, 'cat-walk-cycles-atlas.png'))
  .resize({ width: 1536, height: 2048, kernel: 'nearest' })
  .png()
  .toFile(path.join(root, 'cat-walk-cycles-preview-4x.png'));

const manifest = {
  schemaVersion: 1,
  assetId: 'liveit.pixel.pet.cat.walk-cycles.v1',
  source: 'cat-walk-cycles-source.png',
  atlas: {
    file: 'cat-walk-cycles-atlas.png',
    width: 384,
    height: 512,
    columns: 4,
    rows: 4,
    cellWidth: frameWidth,
    cellHeight: frameHeight,
    order:
      'phase columns contact-a/passing-a/contact-b/passing-b; direction rows south/west/east/north',
  },
  sampling: 'nearest-neighbor',
  frames,
  runtimeReady: false,
  limitations: [
    'Source is AI-generated concept art, not runtime-approved art.',
    'Colored edge artifacts, phase timing, collision boxes, palette cleanup, and renderer sampling remain open.',
  ],
};
await fs.writeFile(
  path.join(root, 'frames.json'),
  `${JSON.stringify(manifest, null, 2)}\n`,
);
await fs.writeFile(
  path.join(root, 'manifest.json'),
  `${JSON.stringify({ ...manifest, manifest: 'frames.json' }, null, 2)}\n`,
);
