/* global URL */
import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

const root = path.dirname(new URL(import.meta.url).pathname);
const sourcePath = path.join(root, 'child-teen-cycles-source.png');
const meta = await sharp(sourcePath).metadata();
const directions = ['south', 'west', 'east', 'north'];
const stages = ['child', 'teen'];
const phases = ['phase-01', 'phase-02', 'phase-03', 'phase-04'];
const cellWidth = meta.width / 4;
// The generator preserved the requested order but left unequal transparent
// gutters between the child and teen bands. These measured boundaries keep
// neighboring silhouettes out of each normalized frame.
const rowBoundaries = [0, 247, 438, 627, 830, 1070, 1311, 1541, 1774];
const frameWidth = 96;
const frameHeight = 128;
const frames = [];

await fs.mkdir(path.join(root, 'frames'), { recursive: true });

for (let row = 0; row < 8; row += 1) {
  const stage = stages[Math.floor(row / 4)];
  const direction = directions[row % 4];
  for (let phase = 0; phase < 4; phase += 1) {
    const left = Math.round(phase * cellWidth);
    const top = rowBoundaries[row];
    const width = Math.round((phase + 1) * cellWidth) - left;
    const height = rowBoundaries[row + 1] - top;
    const name = `${stage}-${direction}-${phases[phase]}`;
    const framePath = path.join(root, 'frames', `${name}.png`);
    const trimmed = await sharp(sourcePath)
      .extract({ left, top, width, height })
      .resize({ width: 88, height: 120, fit: 'fill', kernel: 'nearest' })
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
      .toFile(framePath);
    frames.push({
      stage,
      direction,
      phase: phase + 1,
      file: `frames/${name}.png`,
      x: phase * frameWidth,
      y: row * frameHeight,
      width: frameWidth,
      height: frameHeight,
      pivot: { x: 48, y: 124 },
      runtimeReady: false,
      limitations: [
        'AI-generated directional movement concept; requires pixel cleanup, collision-box review, and renderer validation.',
      ],
    });
  }
}

const atlas = sharp({
  create: {
    width: frameWidth * 4,
    height: frameHeight * 8,
    channels: 4,
    background: { r: 0, g: 0, b: 0, alpha: 0 },
  },
});
await atlas
  .composite(
    frames.map((frame) => ({
      input: path.join(root, frame.file),
      left: frame.x,
      top: frame.y,
    })),
  )
  .png()
  .toFile(path.join(root, 'child-teen-cycles-atlas.png'));
await sharp(path.join(root, 'child-teen-cycles-atlas.png'))
  .resize({ width: 1536, height: 4096, kernel: 'nearest' })
  .png()
  .toFile(path.join(root, 'child-teen-cycles-preview-4x.png'));
await fs.writeFile(
  path.join(root, 'frames.json'),
  `${JSON.stringify({ schemaVersion: 1, assetId: 'child-teen-cycles-v1', source: 'child-teen-cycles-source.png', atlas: { file: 'child-teen-cycles-atlas.png', width: 384, height: 1024, columns: 4, rows: 8, cellWidth: 96, cellHeight: 128, order: 'phase columns; child south/west/east/north rows then teen south/west/east/north rows' }, frames, runtimeReady: false }, null, 2)}\n`,
);
