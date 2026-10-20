"""Derive transparent, uniformly pivoted prop cells from the original concept sheet.

The source sheet is preserved byte-for-byte under source/. Derived cells remain
concept art and are intentionally marked runtimeReady=false in manifest.json.
"""

from __future__ import annotations

import json
import hashlib
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
SOURCE = ROOT / "source" / "home-props-original.png"
SPRITES = ROOT / "sprites"
CELL = 128
GRID_COLUMNS = 4
GRID_ROWS = 3
MARGIN = 8
MAX_DIM = CELL - (2 * MARGIN)

PROPS = [
    ("bed_single", "single bed with pillow and blanket"),
    ("sofa_two_seat", "two-seat sofa"),
    ("dining_table_two_chairs", "small dining table with two chairs"),
    ("kitchen_counter_sink", "kitchen counter, sink, cabinet and utensils"),
    ("refrigerator_compact", "compact refrigerator"),
    ("bathtub_shower", "bathtub with shower curtain and shower head"),
    ("crib_baby", "baby crib with blanket and toy"),
    ("storage_chest", "wooden storage chest"),
    ("wardrobe_tall", "tall wooden wardrobe"),
    ("floor_lamp", "floor lamp"),
    ("plant_potted", "potted house plant"),
    ("wall_clock", "wall clock"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    SPRITES.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGBA")
    cell_w = source.width // GRID_COLUMNS
    cell_h = source.height // GRID_ROWS
    records = []
    for i, (slug, description) in enumerate(PROPS):
        col, row = i % GRID_COLUMNS, i // GRID_COLUMNS
        crop = source.crop((col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h))
        alpha = crop.getchannel("A")
        bbox = alpha.getbbox()
        if bbox is None:
            raise RuntimeError(f"empty alpha cell for {slug}")
        subject = crop.crop(bbox)
        scale = min(MAX_DIM / subject.width, MAX_DIM / subject.height, 1.0)
        if scale != 1.0:
            subject = subject.resize((round(subject.width * scale), round(subject.height * scale)), Image.Resampling.LANCZOS)
        frame = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
        x = (CELL - subject.width) // 2
        y = CELL - MARGIN - subject.height
        frame.alpha_composite(subject, (x, y))
        path = SPRITES / f"{slug}.png"
        frame.save(path)
        records.append({
            "id": f"world_prop.home.{slug}",
            "slug": slug,
            "description": description,
            "file": f"sprites/{path.name}",
            "size": {"width": CELL, "height": CELL},
            "pivot": {"x": 0.5, "y": 1.0},
            "sourceCell": {"column": col, "row": row, "width": cell_w, "height": cell_h},
            "runtimeReady": False,
        })

    atlas = Image.new("RGBA", (GRID_COLUMNS * CELL, GRID_ROWS * CELL), (0, 0, 0, 0))
    for i, (slug, _) in enumerate(PROPS):
        atlas.alpha_composite(Image.open(SPRITES / f"{slug}.png").convert("RGBA"), ((i % GRID_COLUMNS) * CELL, (i // GRID_COLUMNS) * CELL))
    atlas.save(ROOT / "home-props-atlas-4x3.png")
    preview = atlas.resize((atlas.width * 2, atlas.height * 2), Image.Resampling.NEAREST)
    preview.save(ROOT / "home-props-preview-2x.png")
    manifest = {
        "schema": "liveit.pixel.world-props.v1",
        "batch": "world-props-home-v1",
        "style": "original 2D pixel concept art, warm home interior palette",
        "cell": {"width": CELL, "height": CELL},
        "atlas": "home-props-atlas-4x3.png",
        "preview": "home-props-preview-2x.png",
        "runtimeReady": False,
        "source": "source/home-props-original.png",
        "items": records,
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    provenance = {
        "sourceType": "original generated concept sheet",
        "generator": "OpenAI image generation tool",
        "promptFile": "prompts.md",
        "userSuppliedReferenceArt": False,
        "thirdPartyAssets": False,
        "sourceSha256": sha256(SOURCE),
        "derivation": "12 transparent 128x128 cells cropped from a 4x3 source sheet; subjects bottom-aligned with pivot (0.5, 1.0); nearest-neighbor 2x preview.",
        "limitations": [
            "Generated source is a polished concept sheet, not a final engine-tested sprite pack.",
            "Edges retain some anti-aliased pixels from generation; a pixel-artist cleanup pass is still required.",
            "No collision bounds, tile occupancy, draw order, or interaction metadata has been authored.",
        ],
    }
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")


if __name__ == "__main__":
    main()
