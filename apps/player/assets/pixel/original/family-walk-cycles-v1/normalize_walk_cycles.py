#!/usr/bin/env python3
"""Normalize generated 4x4 family walk-cycle sheets into 96x128 frames."""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
DIRECTIONS = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b"]
W, H = 96, 128


def process(name: str, source: Path, character: dict) -> None:
    out = ROOT / name
    out.mkdir(parents=True, exist_ok=True)
    image = Image.open(source).convert("RGBA")
    sw, sh = image.size
    frames = []
    atlas = Image.new("RGBA", (W * 4, H * 4), (0, 0, 0, 0))
    for row, direction in enumerate(DIRECTIONS):
        for col, phase in enumerate(PHASES):
            # Generated source is a clean equal 4x4 layout. Rounding keeps all
            # source pixels assigned exactly once when dimensions are odd.
            x0, x1 = round(col * sw / 4), round((col + 1) * sw / 4)
            y0, y1 = round(row * sh / 4), round((row + 1) * sh / 4)
            cell = image.crop((x0, y0, x1, y1))
            cell.thumbnail((W, H), Image.Resampling.LANCZOS)
            frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            px = (W - cell.width) // 2
            py = H - cell.height
            frame.alpha_composite(cell, (px, py))
            path = out / f"{direction}_{phase}.png"
            frame.save(path)
            atlas.alpha_composite(frame, (col * W, row * H))
            frames.append({
                "id": f"{character['id']}_{direction}_{phase}",
                "direction": direction,
                "phase": phase,
                "path": str(path.relative_to(ROOT.parent.parent.parent.parent)),
                "width": W,
                "height": H,
                "pivot": {"x": 48, "y": 124},
                "runtimeReady": False,
            })
    atlas_path = out / "atlas.png"
    atlas.save(atlas_path)
    preview = atlas.resize((atlas.width * 3, atlas.height * 3), Image.Resampling.NEAREST)
    preview.save(out / "preview-nearest.png")
    manifest = {
        "batch": "family-walk-cycles-v1",
        "character": character,
        "source": str(source),
        "sourceDimensions": {"width": sw, "height": sh},
        "grid": {"columns": 4, "rows": 4, "directions": DIRECTIONS, "phases": PHASES},
        "frameDimensions": {"width": W, "height": H},
        "atlas": str(atlas_path.relative_to(ROOT.parent.parent.parent.parent)),
        "runtimeReady": False,
        "frames": frames,
    }
    (out / "frames.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    process("niko", Path("/tmp/niko_walk_source.png"), {
        "id": "sibling_niko", "name": "Niko", "ageStage": "child",
        "identity": ["curly ponytail", "cobalt hoodie", "orange sneakers", "backpack"],
    })
    process("aunt-sol", Path("/tmp/sol_walk_source.png"), {
        "id": "relative_aunt_sol", "name": "Aunt Sol", "ageStage": "senior",
        "identity": ["silver braid", "sage walking cane", "plum coat", "crossbody pouch"],
    })
