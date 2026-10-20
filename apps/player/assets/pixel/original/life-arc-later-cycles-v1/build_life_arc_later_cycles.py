"""Extract and normalize the four generated 4x4 walk sheets.

The generated sheets are retained unchanged in ``sources/``.  This script is
the deterministic, nearest-neighbour extraction step used for review frames;
it does not change the source art or promote anything to runtime use.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).parent
SOURCE_DIR = ROOT / "sources"
FRAME_DIR = ROOT / "frames"
TARGET_SIZE = (24, 32)
PIVOT = (12, 31)
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("contact-a", "passing-a", "contact-b", "passing-b")
STAGES = (
    ("young-adult-woman", "young-adult-woman-source.png"),
    ("midlife-woman", "midlife-woman-source.png"),
    ("elder-woman", "elder-woman-source.png"),
    ("elder-man", "elder-man-source.png"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def crop_and_normalize(sheet: Image.Image, row: int, column: int) -> Image.Image:
    width, height = sheet.size
    left = column * width // 4
    top = row * height // 4
    right = (column + 1) * width // 4
    bottom = (row + 1) * height // 4
    cell = sheet.crop((left, top, right, bottom)).convert("RGBA")

    # Ignore faint anti-aliased/fringe pixels when determining the silhouette;
    # retain only a binary alpha in the derived review frame.
    alpha = cell.getchannel("A").point(lambda value: 255 if value >= 16 else 0)
    bbox = alpha.getbbox()
    result = Image.new("RGBA", TARGET_SIZE, (0, 0, 0, 0))
    if bbox is None:
        return result

    content = cell.crop(bbox).convert("RGBA")
    content.putalpha(alpha.crop(bbox))
    max_width, max_height = 22, 30
    scale = min(max_width / content.width, max_height / content.height, 1.0)
    resized = content.resize(
        (max(1, round(content.width * scale)), max(1, round(content.height * scale))),
        Image.Resampling.NEAREST,
    )
    x = (TARGET_SIZE[0] - resized.width) // 2
    y = TARGET_SIZE[1] - resized.height
    result.alpha_composite(resized, (x, y))
    return result


def main() -> None:
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    source_records: list[dict[str, object]] = []
    for stage, source_name in STAGES:
        source_path = SOURCE_DIR / source_name
        source = Image.open(source_path).convert("RGBA")
        source_records.append(
            {
                "stage": stage,
                "file": f"sources/{source_name}",
                "sha256": sha256(source_path),
                "size": list(source.size),
                "mode": source.mode,
            }
        )
        stage_dir = FRAME_DIR / stage
        stage_dir.mkdir(parents=True, exist_ok=True)
        atlas = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
        for row, direction in enumerate(DIRECTIONS):
            for column, phase in enumerate(PHASES):
                frame = crop_and_normalize(source, row, column)
                filename = f"{stage}-{direction}-{phase}.png"
                frame_path = stage_dir / filename
                frame.save(frame_path)
                atlas.alpha_composite(frame, (column * 24, row * 32))
                records.append(
                    {
                        "id": f"{stage}/{direction}/{phase}",
                        "stage": stage,
                        "direction": direction,
                        "phase": phase,
                        "file": f"frames/{stage}/{filename}",
                        "sha256": sha256(frame_path),
                        "atlas": {
                            "file": f"frames/{stage}/{stage}-atlas.png",
                            "x": column * 24,
                            "y": row * 32,
                            "width": 24,
                            "height": 32,
                        },
                        "pivot": list(PIVOT),
                        "size": list(TARGET_SIZE),
                        "mode": "RGBA",
                        "runtimeReady": False,
                        "sourceSheet": f"sources/{source_name}",
                        "sourceCell": {"column": column, "row": row},
                    }
                )
        atlas.save(stage_dir / f"{stage}-atlas.png")

    # One review atlas: stages are stacked vertically, each stage is a 4x4
    # atlas.  It is intentionally a derived preview, not an intake asset.
    combined = Image.new("RGBA", (96, 512), (0, 0, 0, 0))
    for stage_index, (stage, _) in enumerate(STAGES):
        atlas = Image.open(FRAME_DIR / stage / f"{stage}-atlas.png").convert("RGBA")
        combined.alpha_composite(atlas, (0, stage_index * 128))
    combined.save(ROOT / "life-arc-later-cycles-atlas.png")
    combined.resize((384, 2048), Image.Resampling.NEAREST).save(
        ROOT / "life-arc-later-cycles-preview-4x.png"
    )

    manifest = {
        "schemaVersion": 1,
        "id": "life-arc-later-cycles-v1",
        "description": "Four later-life identity stages, four cardinal directions, and four walk phases.",
        "logicalFrameSize": list(TARGET_SIZE),
        "pivot": list(PIVOT),
        "directions": list(DIRECTIONS),
        "phases": list(PHASES),
        "stages": [stage for stage, _ in STAGES],
        "runtimeReady": False,
        "sources": source_records,
        "frames": records,
        "limitations": [
            "Generated identity and motion require a human pixel-art cleanup pass.",
            "Reference matching is approximate; visual identity continuity is not proven.",
            "Derived frames use thresholded alpha and nearest-neighbour scaling.",
            "Renderer sampling, collision boxes, and gameplay integration are not verified.",
        ],
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
