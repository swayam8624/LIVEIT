#!/usr/bin/env python3
"""Fallback builder using clean directional concept poses when the source grid drifts."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).parent
CONCEPT = ROOT.parent / "age-direction-concept-batch-v1"
sys.path.insert(0, str(ROOT))
import prepare_assets as io  # noqa: E402

STAGES = {
    "young-adult-woman": "young-adult-woman",
    "midlife-adult-woman": "midlife-woman",
    "elder-woman": "elder-woman",
    "elder-man": "elder-man",
}
FACING = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b"]
SHIFT = [(0, 0), (-1, 1), (1, 0), (0, -1)]


def shift(frame: bytes, dx: int, dy: int) -> bytes:
    out = bytearray(io.FRAME_W * io.FRAME_H * 4)
    for y in range(io.FRAME_H):
        sy = y - dy
        if not 0 <= sy < io.FRAME_H:
            continue
        for x in range(io.FRAME_W):
            sx = x - dx
            if 0 <= sx < io.FRAME_W:
                out[(y * io.FRAME_W + x) * 4 : (y * io.FRAME_W + x + 1) * 4] = frame[(sy * io.FRAME_W + sx) * 4 : (sy * io.FRAME_W + sx + 1) * 4]
    return bytes(out)


def main() -> None:
    atlas = bytearray(4 * io.FRAME_W * 16 * io.FRAME_H * 4)
    metadata = {"schemaVersion": 1, "runtimeReady": False, "sourceMode": "clean-directional-concept-fallback", "sheet": {"columns": 4, "rows": 16, "frameWidth": io.FRAME_W, "frameHeight": io.FRAME_H}, "frames": []}
    for stage_index, (stage, concept_stage) in enumerate(STAGES.items()):
        stage_atlas = bytearray(4 * io.FRAME_W * 4 * io.FRAME_H * 4)
        for facing_index, facing in enumerate(FACING):
            source = CONCEPT / concept_stage / f"{concept_stage}-{facing}-idle.png"
            width, height, base = io.read_png(source)
            if (width, height) != (io.FRAME_W, io.FRAME_H):
                raise ValueError(f"unexpected concept frame size: {source} = {width}x{height}")
            for phase_index, phase in enumerate(PHASES):
                frame = shift(base, *SHIFT[phase_index])
                frame_dir = ROOT / stage
                frame_dir.mkdir(exist_ok=True)
                filename = f"{stage}-{facing}-{phase}.png"
                io.write_png(frame_dir / filename, io.FRAME_W, io.FRAME_H, frame)
                atlas_x = phase_index * io.FRAME_W
                atlas_y = (stage_index * 4 + facing_index) * io.FRAME_H
                stage_y = facing_index * io.FRAME_H
                row_stride = 4 * io.FRAME_W * 4
                atlas[atlas_y * row_stride + atlas_x * 4 : atlas_y * row_stride + (atlas_x + io.FRAME_W) * 4] = frame[: io.FRAME_W * 4]
                for y in range(io.FRAME_H):
                    atlas[(atlas_y + y) * row_stride + atlas_x * 4 : (atlas_y + y) * row_stride + (atlas_x + io.FRAME_W) * 4] = frame[y * io.FRAME_W * 4 : (y + 1) * io.FRAME_W * 4]
                    stage_atlas[(stage_y + y) * row_stride + atlas_x * 4 : (stage_y + y) * row_stride + (atlas_x + io.FRAME_W) * 4] = frame[y * io.FRAME_W * 4 : (y + 1) * io.FRAME_W * 4]
                metadata["frames"].append({"id": f"{stage}/{facing}/{phase}", "stage": stage, "facing": facing, "phase": phase, "file": f"{stage}/{filename}", "atlas": {"x": atlas_x, "y": atlas_y, "width": io.FRAME_W, "height": io.FRAME_H}, "pivot": {"x": 48, "y": 126}, "runtimeReady": False})
        io.write_png(ROOT / stage / f"{stage}-cycle-atlas.png", 4 * io.FRAME_W, 4 * io.FRAME_H, bytes(stage_atlas))
    io.write_png(ROOT / "adult-elder-cycles-atlas.png", 4 * io.FRAME_W, 16 * io.FRAME_H, bytes(atlas))
    (ROOT / "frames.json").write_text(json.dumps(metadata, indent=2) + "\n")


if __name__ == "__main__":
    main()
