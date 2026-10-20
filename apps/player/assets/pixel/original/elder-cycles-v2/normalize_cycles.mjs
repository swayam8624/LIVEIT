/* global URL */
import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

const root = path.dirname(new URL(import.meta.url).pathname);
const directions = ['south', 'west', 'east', 'north'];
const phases = ['contact-a', 'passing-a', 'contact-b', 'passing-b'];
const frameWidth = 96;
const frameHeight = 128;

for (const stage of ['elder-woman', 'elder-man']) {
  const stageRoot = path.join(root, stage);
  const sourcePath = path.join(stageRoot, `${stage}-cycles-source.png`);
  const source = await sharp(sourcePath).metadata();
  if (!source.width || !source.height)
    throw new Error(`Unreadable source: ${sourcePath}`);
  const cellSourceWidth = source.width / 4;
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
  if (rowBounds.length !== 4)
    throw new Error(
      `Expected four occupied row bands in ${sourcePath}, got ${rowBounds.length}`,
    );
  const frames = [];
  await fs.mkdir(path.join(stageRoot, 'frames'), { recursive: true });

  for (let row = 0; row < 4; row += 1) {
    for (let column = 0; column < 4; column += 1) {
      const left = Math.round(column * cellSourceWidth);
      const right = Math.round((column + 1) * cellSourceWidth);
      const [top, bottom] = rowBounds[row];
      const direction = directions[row];
      const phase = phases[column];
      const id = `${stage}-${direction}-${phase}`;
      const file = `frames/${id}.png`;
      const trimmed = await sharp(sourcePath)
        .extract({ left, top, width: right - left, height: bottom - top })
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
        .toFile(path.join(stageRoot, file));
      frames.push({
        id,
        stage,
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

  const atlas = sharp({
    create: {
      width: frameWidth * 4,
      height: frameHeight * 4,
      channels: 4,
      background: { r: 0, g: 0, b: 0, alpha: 0 },
    },
  });
  await atlas
    .composite(
      frames.map((frame) => ({
        input: path.join(stageRoot, frame.file),
        left: frame.x,
        top: frame.y,
      })),
    )
    .png()
    .toFile(path.join(stageRoot, `${stage}-cycles-atlas.png`));
  await sharp(path.join(stageRoot, `${stage}-cycles-atlas.png`))
    .resize({ width: 1536, height: 2048, kernel: 'nearest' })
    .png()
    .toFile(path.join(stageRoot, `${stage}-cycles-preview-4x.png`));
  await fs.writeFile(
    path.join(stageRoot, 'frames.json'),
    `${JSON.stringify(
      {
        schemaVersion: 1,
        assetId: `${stage}-cycles-v2`,
        source: `${stage}-cycles-source.png`,
        atlas: {
          file: `${stage}-cycles-atlas.png`,
          width: 384,
          height: 512,
          columns: 4,
          rows: 4,
          cellWidth: 96,
          cellHeight: 128,
          order:
            'phase columns contact-a/passing-a/contact-b/passing-b; direction rows south/west/east/north',
        },
        frames,
        runtimeReady: false,
        limitations: [
          'Source is AI-generated concept art, not runtime-approved art.',
          'Colored edge artifacts, phase timing, collision boxes, palette cleanup, and renderer sampling remain open.',
        ],
      },
      null,
      2,
    )}\n`,
  );
}
