#!/usr/bin/env python3
"""Package the generated dog sheet without resampling source pixels softly."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "dog-walk-cycles-source.png"
DIRECTIONS = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b"]
FRAME_W, FRAME_H = 96, 128
PIVOT = {"x": 48, "y": 124}


def normalize_cell(cell: Image.Image) -> Image.Image:
    """Fit the opaque dog to a stable frame using nearest-neighbor only."""
    alpha = cell.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        return Image.new("RGBA", (FRAME_W, FRAME_H), (0, 0, 0, 0))
    subject = cell.crop(bbox)
    scale = min(88 / subject.width, 120 / subject.height, 1.0)
    size = (max(1, round(subject.width * scale)), max(1, round(subject.height * scale)))
    subject = subject.resize(size, Image.Resampling.NEAREST)
    # The generator occasionally emits isolated chroma-key red/green/blue
    # fringe pixels. Remove only those primary-color halos in derivatives;
    # the exact generated source remains unchanged on disk.
    pixels = subject.load()
    for y in range(subject.height):
        for x in range(subject.width):
            r, g, b, a = pixels[x, y]
            if a and ((r > 220 and g < 70 and b < 70) or
                      (g > 180 and r < 80 and b < 80) or
                      (b > 180 and r < 80 and g < 80)):
                pixels[x, y] = (0, 0, 0, 0)
    frame = Image.new("RGBA", (FRAME_W, FRAME_H), (0, 0, 0, 0))
    frame.alpha_composite(subject, ((FRAME_W - subject.width) // 2, PIVOT["y"] - subject.height))
    return frame


def main() -> None:
    source = Image.open(SOURCE).convert("RGBA")
    sw, sh = source.size
    out = ROOT / "frames"
    out.mkdir(exist_ok=True)
    atlas = Image.new("RGBA", (FRAME_W * 4, FRAME_H * 4), (0, 0, 0, 0))
    records = []
    for row, direction in enumerate(DIRECTIONS):
        for col, phase in enumerate(PHASES):
            x0, x1 = round(col * sw / 4), round((col + 1) * sw / 4)
            y0, y1 = round(row * sh / 4), round((row + 1) * sh / 4)
            frame = normalize_cell(source.crop((x0, y0, x1, y1)))
            filename = f"dog-{direction}-{phase}.png"
            frame.save(out / filename)
            atlas.alpha_composite(frame, (col * FRAME_W, row * FRAME_H))
            records.append({
                "id": f"dog/{direction}/{phase}",
                "character": "Dog companion",
                "facing": direction,
                "phase": phase,
                "file": f"frames/{filename}",
                "atlas": {"x": col * FRAME_W, "y": row * FRAME_H, "width": FRAME_W, "height": FRAME_H},
                "pivot": PIVOT,
                "runtimeReady": False,
            })
    atlas.save(ROOT / "dog-walk-cycles-atlas.png")
    atlas.resize((atlas.width * 2, atlas.height * 2), Image.Resampling.NEAREST).save(ROOT / "dog-walk-cycles-preview-2x.png")
    manifest = {
        "schemaVersion": 1,
        "batch": "pet-walk-cycles-v1",
        "runtimeReady": False,
        "source": "dog-walk-cycles-source.png",
        "sourceMode": "generated-four-direction-four-phase",
        "sheet": {"columns": 4, "rows": 4, "frameWidth": FRAME_W, "frameHeight": FRAME_H,
                   "sourceWidth": sw, "sourceHeight": sh},
        "directions": DIRECTIONS,
        "phases": PHASES,
        "character": {"id": "pet_dog_companion", "name": "Dog companion", "species": "mixed-breed dog",
                      "identity": ["cream coat", "caramel patches", "floppy ears", "short tail", "plum harness"]},
        "atlas": "dog-walk-cycles-atlas.png",
        "preview": "dog-walk-cycles-preview-2x.png",
        "frames": records,
    }
    (ROOT / "frames.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
