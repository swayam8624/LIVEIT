"""Deterministically extract 4x4 concept sheets into 24x32 pixel frames.

Source sheets are preserved byte-for-byte. Each source is divided into its
four equal rows and columns, then resized with nearest-neighbour sampling to
24x32. The output order is south, west, east, north by row and
contact-a, passing-a, contact-b, passing-b by column.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).parent
STAGES = {
    "infant-crawl": "infant-crawl/infant-crawl-source.png",
    "toddler-waddle": "toddler-waddle/toddler-waddle-source.png",
    "child-walk": "child-walk/child-walk-source.png",
    "teen-walk": "teen-walk/teen-walk-source.png",
}
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("contact-a", "passing-a", "contact-b", "passing-b")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    all_frames: list[dict[str, object]] = []
    for stage, source_rel in STAGES.items():
        stage_dir = ROOT / stage
        source = stage_dir / Path(source_rel).name
        image = Image.open(source).convert("RGBA")
        width, height = image.size
        atlas = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
        records: list[dict[str, object]] = []
        for row, direction in enumerate(DIRECTIONS):
            for col, phase in enumerate(PHASES):
                left = round(col * width / 4)
                top = round(row * height / 4)
                right = round((col + 1) * width / 4)
                bottom = round((row + 1) * height / 4)
                frame = image.crop((left, top, right, bottom)).resize((24, 32), Image.Resampling.NEAREST)
                name = f"{stage}-{direction}-{phase}.png"
                path = stage_dir / name
                frame.save(path)
                atlas.paste(frame, (col * 24, row * 32))
                record = {
                    "file": name,
                    "stage": stage,
                    "direction": direction,
                    "phase": phase,
                    "frameSize": {"width": 24, "height": 32},
                    "pivot": {"x": 12, "y": 31},
                    "sourceCell": {"row": row, "column": col},
                    "runtimeReady": False,
                    "notes": "Derived nearest-neighbor crop from the preserved ImageGen source sheet; concept-only until pixel cleanup and renderer review.",
                }
                records.append(record)
                all_frames.append({"stage": stage, **record})
        atlas_path = stage_dir / f"{stage}-atlas-24x32.png"
        atlas.save(atlas_path)
        preview = atlas.resize((384, 512), Image.Resampling.NEAREST)
        preview.save(stage_dir / f"{stage}-preview-4x.png")
        manifest = {
            "schema": "liveit.pixel.sprite-batch.v1",
            "batch": f"life-arc-early-cycles-v1/{stage}",
            "source": {"file": source.name, "sha256": sha256(source), "size": {"width": width, "height": height}, "mode": "RGBA"},
            "grid": {"rows": list(DIRECTIONS), "columns": list(PHASES), "cellSize": {"width": 24, "height": 32}},
            "pivot": {"x": 12, "y": 31},
            "frames": records,
            "runtimeReady": False,
        }
        (stage_dir / "frames.json").write_text(json.dumps(manifest, indent=2) + "\n")

    combined = Image.new("RGBA", (384, 512), (0, 0, 0, 0))
    for idx, stage in enumerate(STAGES):
        atlas = Image.open(ROOT / stage / f"{stage}-atlas-24x32.png").convert("RGBA").resize((192, 256), Image.Resampling.NEAREST)
        combined.paste(atlas, ((idx % 2) * 192, (idx // 2) * 256))
    combined.save(ROOT / "life-arc-early-cycles-preview-2x.png")
    (ROOT / "frames.json").write_text(json.dumps({
        "schema": "liveit.pixel.sprite-batch.v1",
        "batch": "life-arc-early-cycles-v1",
        "stages": list(STAGES),
        "directions": list(DIRECTIONS),
        "phases": list(PHASES),
        "frameSize": {"width": 24, "height": 32},
        "pivot": {"x": 12, "y": 31},
        "frameCount": len(all_frames),
        "frames": all_frames,
        "runtimeReady": False,
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
