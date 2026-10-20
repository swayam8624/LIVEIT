#!/usr/bin/env python3
"""Normalize the generated 4x8 walk sheet into fixed RGBA frames."""
from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "young-midlife-cycles-source.png"
ATLAS = ROOT / "young-midlife-cycles-atlas.png"
FRAME_W, FRAME_H = 96, 128
STAGES = ["young-adult-woman", "midlife-adult-woman"]
FACING = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b"]


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
            if (depth, color, comp, filt, interlace) != (8, 6, 0, 0, 0):
                raise ValueError("expected an 8-bit RGBA non-interlaced PNG")
        elif kind == b"IDAT":
            idat.extend(chunk)
        elif kind == b"IEND":
            break
    if width is None or height is None:
        raise ValueError("PNG has no dimensions")
    packed = zlib.decompress(idat)
    stride = width * 4
    rows: list[bytes] = []
    pos = 0
    previous = bytearray(stride)
    for _ in range(height):
        mode = packed[pos]
        pos += 1
        current = bytearray(packed[pos : pos + stride])
        pos += stride
        for i in range(stride):
            left = current[i - 4] if i >= 4 else 0
            up = previous[i]
            up_left = previous[i - 4] if i >= 4 else 0
            if mode == 1:
                current[i] = (current[i] + left) & 255
            elif mode == 2:
                current[i] = (current[i] + up) & 255
            elif mode == 3:
                current[i] = (current[i] + ((left + up) // 2)) & 255
            elif mode == 4:
                estimate = left + up - up_left
                pa, pb, pc = abs(estimate - left), abs(estimate - up), abs(estimate - up_left)
                current[i] = (current[i] + (left if pa <= pb and pa <= pc else up if pb <= pc else up_left)) & 255
            elif mode != 0:
                raise ValueError(f"unsupported PNG filter {mode}")
        rows.append(bytes(current))
        previous = current
    return width, height, b"".join(rows)


def write_png(path: Path, width: int, height: int, pixels: bytes) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    rows = b"".join(b"\x00" + pixels[y * width * 4 : (y + 1) * width * 4] for y in range(height))
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(rows, 9))
        + chunk(b"IEND", b"")
    )


def alpha_bbox(pixels: bytes, width: int, height: int) -> tuple[int, int, int, int] | None:
    points = [(x, y) for y in range(height) for x in range(width) if pixels[(y * width + x) * 4 + 3] > 8]
    if not points:
        return None
    xs, ys = zip(*points)
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def largest_component(pixels: bytes, width: int, height: int) -> tuple[bytes, tuple[int, int, int, int]]:
    active = {y * width + x for y in range(height) for x in range(width) if pixels[(y * width + x) * 4 + 3] > 8}
    best: list[int] = []
    while active:
        start = active.pop()
        stack, group = [start], [start]
        while stack:
            point = stack.pop()
            x, y = point % width, point // width
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                neighbor = ny * width + nx
                if 0 <= nx < width and 0 <= ny < height and neighbor in active:
                    active.remove(neighbor)
                    stack.append(neighbor)
                    group.append(neighbor)
        if len(group) > len(best):
            best = group
    if not best:
        raise ValueError("cell has no connected silhouette")
    mask = bytearray(width * height * 4)
    for point in best:
        source = point * 4
        mask[source : source + 4] = pixels[source : source + 4]
    xs = [point % width for point in best]
    ys = [point // width for point in best]
    return bytes(mask), (min(xs), min(ys), max(xs) + 1, max(ys) + 1)


def crop_cell(pixels: bytes, width: int, height: int, col: int, row: int) -> tuple[bytes, int, int]:
    x0, x1 = round(col * width / 4), round((col + 1) * width / 4)
    # The generator lets a few feet cross row seams; reserve a transparent
    # gutter on both sides before selecting the cell's own silhouette.
    y0, y1 = round(row * height / 8) + 24, round((row + 1) * height / 8) - 12
    cell_w, cell_h = x1 - x0, y1 - y0
    cell = b"".join(pixels[(y0 + y) * width * 4 + x0 * 4 : (y0 + y) * width * 4 + x1 * 4] for y in range(cell_h))
    cell, box = largest_component(cell, cell_w, cell_h)
    bx0, by0, bx1, by1 = box
    pad = 3
    bx0, by0 = max(0, bx0 - pad), max(0, by0 - pad)
    bx1, by1 = min(cell_w, bx1 + pad), min(cell_h, by1 + pad)
    cropped = b"".join(cell[y * cell_w * 4 + bx0 * 4 : y * cell_w * 4 + bx1 * 4] for y in range(by0, by1))
    return cropped, bx1 - bx0, by1 - by0


def normalize(cropped: bytes, src_w: int, src_h: int, target_h: int) -> bytes:
    scale = min((FRAME_W - 8) / src_w, target_h / src_h)
    out_w, out_h = max(1, round(src_w * scale)), max(1, round(src_h * scale))
    ox, oy = (FRAME_W - out_w) // 2, FRAME_H - out_h - 2
    output = bytearray(FRAME_W * FRAME_H * 4)
    for dy in range(out_h):
        sy = min(src_h - 1, int(dy / scale))
        for dx in range(out_w):
            sx = min(src_w - 1, int(dx / scale))
            source = (sy * src_w + sx) * 4
            dest = ((oy + dy) * FRAME_W + ox + dx) * 4
            output[dest : dest + 4] = cropped[source : source + 4]
    # Keep seam residue from touching the top of a normalized frame. The
    # character's hair remains below this small transparent safety gutter.
    for y in range(6):
        output[y * FRAME_W * 4 : (y + 1) * FRAME_W * 4] = b"\x00" * (FRAME_W * 4)
    return bytes(output)


def main() -> None:
    width, height, pixels = read_png(SOURCE)
    if width < 4 or height < 8:
        raise ValueError("source sheet is too small for a 4x8 grid")
    cells: list[tuple[bytes, int, int]] = [crop_cell(pixels, width, height, col, row) for row in range(8) for col in range(4)]
    stage_heights = [min(FRAME_H - 8, max(cells[row * 4 + col][2] for row in range(stage * 4, stage * 4 + 4) for col in range(4))) for stage in range(2)]
    atlas = bytearray(4 * FRAME_W * 8 * FRAME_H * 4)
    metadata = {
        "schemaVersion": 1,
        "runtimeReady": False,
        "sourceMode": "generated-four-phase",
        "sheet": {"columns": 4, "rows": 8, "frameWidth": FRAME_W, "frameHeight": FRAME_H, "sourceWidth": width, "sourceHeight": height},
        "frames": [],
    }
    row_stride = 4 * FRAME_W * 4
    for row in range(8):
        stage_index, facing = row // 4, FACING[row % 4]
        stage = STAGES[stage_index]
        stage_dir = ROOT / stage
        stage_dir.mkdir(exist_ok=True)
        for phase_index, phase in enumerate(PHASES):
            cropped, src_w, src_h = cells[row * 4 + phase_index]
            frame = normalize(cropped, src_w, src_h, stage_heights[stage_index])
            frame_path = stage_dir / f"{stage}-{facing}-{phase}.png"
            write_png(frame_path, FRAME_W, FRAME_H, frame)
            atlas_x, atlas_y = phase_index * FRAME_W, row * FRAME_H
            for y in range(FRAME_H):
                start = (atlas_y + y) * row_stride + atlas_x * 4
                atlas[start : start + FRAME_W * 4] = frame[y * FRAME_W * 4 : (y + 1) * FRAME_W * 4]
            metadata["frames"].append({
                "id": f"{stage}/{facing}/{phase}",
                "stage": stage,
                "facing": facing,
                "phase": phase,
                "file": f"{stage}/{frame_path.name}",
                "atlas": {"x": atlas_x, "y": atlas_y, "width": FRAME_W, "height": FRAME_H},
                "pivot": {"x": 48, "y": 126},
                "runtimeReady": False,
            })
    write_png(ATLAS, 4 * FRAME_W, 8 * FRAME_H, bytes(atlas))
    (ROOT / "frames.json").write_text(json.dumps(metadata, indent=2) + "\n")


if __name__ == "__main__":
    main()
