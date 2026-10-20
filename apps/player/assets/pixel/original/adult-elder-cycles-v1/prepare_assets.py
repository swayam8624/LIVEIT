#!/usr/bin/env python3
"""Crop the generated 4x16 sheet into normalized 96x128 RGBA frames."""
from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "adult-elder-cycles-source.png"
ATLAS = ROOT / "adult-elder-cycles-atlas.png"
FRAME_W, FRAME_H = 96, 128
STAGES = ["young-adult-woman", "midlife-adult-woman", "elder-woman", "elder-man"]
FACING = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b"]
# The generator kept the four columns visually regular but placed broad side
# silhouettes across nominal equal-cell seams. These boundaries retain complete
# silhouettes before normalization.


def read_png(path: Path) -> tuple[int, int, bytes]:
    raw = path.read_bytes()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    pos = 8
    idat = bytearray()
    width = height = None
    while pos < len(raw):
        n = struct.unpack(">I", raw[pos : pos + 4])[0]
        kind = raw[pos + 4 : pos + 8]
        chunk = raw[pos + 8 : pos + 8 + n]
        pos += n + 12
        if kind == b"IHDR":
            width, height, depth, color, comp, filt, interlace = struct.unpack(">IIBBBBB", chunk)
            assert depth == 8 and color == 6 and comp == filt == interlace == 0
        elif kind == b"IDAT":
            idat.extend(chunk)
        elif kind == b"IEND":
            break
    assert width and height
    packed = zlib.decompress(idat)
    stride = width * 4
    rows: list[bytes] = []
    p = 0
    prev = bytearray(stride)
    for _ in range(height):
        mode = packed[p]
        p += 1
        cur = bytearray(packed[p : p + stride])
        p += stride
        for i in range(stride):
            left = cur[i - 4] if i >= 4 else 0
            up = prev[i]
            up_left = prev[i - 4] if i >= 4 else 0
            if mode == 1:
                cur[i] = (cur[i] + left) & 255
            elif mode == 2:
                cur[i] = (cur[i] + up) & 255
            elif mode == 3:
                cur[i] = (cur[i] + ((left + up) // 2)) & 255
            elif mode == 4:
                estimate = left + up - up_left
                pa, pb, pc = abs(estimate - left), abs(estimate - up), abs(estimate - up_left)
                cur[i] = (cur[i] + (left if pa <= pb and pa <= pc else up if pb <= pc else up_left)) & 255
            elif mode != 0:
                raise ValueError(f"unsupported PNG filter {mode}")
        rows.append(bytes(cur))
        prev = cur
    return width, height, b"".join(rows)


def write_png(path: Path, width: int, height: int, pixels: bytes) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    rows = b"".join(b"\x00" + pixels[y * width * 4 : (y + 1) * width * 4] for y in range(height))
    out = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b"")
    path.write_bytes(out)


def alpha_bbox(pixels: bytes, width: int, height: int) -> tuple[int, int, int, int] | None:
    points = [(x, y) for y in range(height) for x in range(width) if pixels[(y * width + x) * 4 + 3] > 8]
    if not points:
        return None
    xs, ys = zip(*points)
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def largest_component_bbox(pixels: bytes, width: int, height: int) -> tuple[int, int, int, int] | None:
    """Ignore stray neighboring-cell pixels when the generator crosses a seam."""
    active = {y * width + x for y in range(height) for x in range(width) if pixels[(y * width + x) * 4 + 3] > 8}
    best: list[int] = []
    while active:
        start = active.pop()
        stack, group = [start], [start]
        while stack:
            point = stack.pop()
            x, y = point % width, point // width
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                n = ny * width + nx
                if 0 <= nx < width and 0 <= ny < height and n in active:
                    active.remove(n)
                    stack.append(n)
                    group.append(n)
        if len(group) > len(best):
            best = group
    if not best:
        return None
    xs = [point % width for point in best]
    ys = [point // width for point in best]
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def row_component_runs(pixels: bytes, width: int, y0: int, height: int) -> list[tuple[int, int]]:
    """Find the four actual silhouette spans in a source row."""
    active = []
    for x in range(width):
        if any(pixels[((y0 + y) * width + x) * 4 + 3] > 8 for y in range(height)):
            active.append(x)
    runs: list[list[int]] = []
    for x in active:
        if not runs or x > runs[-1][-1] + 1:
            runs.append([x])
        else:
            runs[-1].append(x)
    if len(runs) != 4:
        raise ValueError(f"expected four separated source silhouettes, found {len(runs)}")
    return [(run[0], run[-1] + 1) for run in runs]


def normalize(cell: bytes, cell_w: int, cell_h: int, target_h: int) -> bytes:
    box = largest_component_bbox(cell, cell_w, cell_h) or alpha_bbox(cell, cell_w, cell_h)
    if box is None:
        return bytes(FRAME_W * FRAME_H * 4)
    x0, y0, x1, y1 = box
    # Keep a small transparent margin and preserve the entire silhouette.
    pad = 4
    x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(cell_w, x1 + pad), min(cell_h, y1 + pad)
    src_w, src_h = x1 - x0, y1 - y0
    # Use one stage-wide height so a generated phase with a smaller silhouette
    # cannot collapse into a tiny frame beside its siblings.
    scale = min((FRAME_W - 8) / src_w, target_h / src_h)
    out_w, out_h = max(1, round(src_w * scale)), max(1, round(src_h * scale))
    ox, oy = (FRAME_W - out_w) // 2, FRAME_H - out_h - 2
    out = bytearray(FRAME_W * FRAME_H * 4)
    for dy in range(out_h):
        sy = min(src_h - 1, int(dy / scale))
        for dx in range(out_w):
            sx = min(src_w - 1, int(dx / scale))
            src = ((y0 + sy) * cell_w + x0 + sx) * 4
            dst = ((oy + dy) * FRAME_W + ox + dx) * 4
            out[dst : dst + 4] = cell[src : src + 4]
    return bytes(out)


def main() -> None:
    width, height, pixels = read_png(SOURCE)
    source_row_h = height // 16
    # Generated rows touch at their seams. Skip the upper seam pixels, which
    # otherwise belong to the preceding row's feet or accessories.
    row_inset = 12
    cell_h = source_row_h - row_inset
    atlas = bytearray(4 * FRAME_W * 16 * FRAME_H * 4)
    metadata = {"schemaVersion": 1, "runtimeReady": False, "sheet": {"columns": 4, "rows": 16, "frameWidth": FRAME_W, "frameHeight": FRAME_H, "sourceWidth": width, "sourceHeight": height}, "frames": []}
    # Establish a shared silhouette height per stage from all 16 source cells.
    stage_heights: dict[str, int] = {}
    for stage_index, stage in enumerate(STAGES):
        heights = []
        for row in range(stage_index * 4, stage_index * 4 + 4):
            for col in range(4):
                cx0, cx1 = row_component_runs(pixels, width, row * source_row_h, source_row_h)[col]
                cw = cx1 - cx0
                cell = b"".join(pixels[(row * source_row_h + row_inset + y) * width * 4 + cx0 * 4 : (row * source_row_h + row_inset + y) * width * 4 + cx1 * 4] for y in range(cell_h))
                box = largest_component_bbox(cell, cw, cell_h) or alpha_bbox(cell, cw, cell_h)
                if box:
                    heights.append(box[3] - box[1])
        stage_heights[stage] = min(FRAME_H - 8, max(heights, default=FRAME_H - 12))
    for row in range(16):
        stage = STAGES[row // 4]
        facing = FACING[row % 4]
        for phase in range(4):
            cx0, cx1 = row_component_runs(pixels, width, row * source_row_h, source_row_h)[phase]
            cell_w = cx1 - cx0
            cell = bytearray()
            for y in range(cell_h):
                cell.extend(pixels[(row * source_row_h + row_inset + y) * width * 4 + cx0 * 4 : (row * source_row_h + row_inset + y) * width * 4 + cx1 * 4])
            frame = normalize(bytes(cell), cell_w, cell_h, stage_heights[stage])
            x = phase * FRAME_W
            y = row * FRAME_H
            for yy in range(FRAME_H):
                atlas[(y + yy) * 4 * FRAME_W * 4 + x * 4 : (y + yy) * 4 * FRAME_W * 4 + x * 4 + FRAME_W * 4] = frame[yy * FRAME_W * 4 : (yy + 1) * FRAME_W * 4]
            stage_dir = ROOT / stage
            stage_dir.mkdir(exist_ok=True)
            filename = f"{stage}-{facing}-{PHASES[phase]}.png"
            write_png(stage_dir / filename, FRAME_W, FRAME_H, frame)
            metadata["frames"].append({"id": f"{stage}/{facing}/{PHASES[phase]}", "stage": stage, "facing": facing, "phase": PHASES[phase], "file": f"{stage}/{filename}", "atlas": {"x": x, "y": y, "width": FRAME_W, "height": FRAME_H}, "pivot": {"x": 48, "y": 126}, "runtimeReady": False})
    stage_stride = 4 * FRAME_H * (4 * FRAME_W * 4)
    for stage_index, stage in enumerate(STAGES):
        start = stage_index * stage_stride
        write_png(ROOT / stage / f"{stage}-cycle-atlas.png", 4 * FRAME_W, 4 * FRAME_H, bytes(atlas[start : start + stage_stride]))
    write_png(ATLAS, 4 * FRAME_W, 16 * FRAME_H, bytes(atlas))
    (ROOT / "frames.json").write_text(json.dumps(metadata, indent=2) + "\n")


if __name__ == "__main__":
    main()
