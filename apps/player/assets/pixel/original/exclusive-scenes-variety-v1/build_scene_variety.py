#!/usr/bin/env python3
"""Build concept-resolution exports, layout guides, preview sheet, and hash manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "sources"
SCENE_DIR = ROOT / "scenes"
GUIDE_DIR = ROOT / "guides"
PREVIEW_DIR = ROOT / "previews"
SIZE = (320, 256)

SCENES = [
    {
        "id": "first-paycheck-diner",
        "title": "First paycheck, after closing",
        "source": "first-paycheck-diner-source.png",
        "concept": "first-paycheck-diner-32c-320x256.png",
        "guide": "first-paycheck-diner-layout-guide.png",
        "mood": "earned relief and quiet pride",
        "dialogueSafeRegion": {"x": 42, "y": 232, "width": 236, "height": 24},
        "actorSafeRegion": {"x": 42, "y": 48, "width": 236, "height": 164},
    },
    {
        "id": "reconciliation-bus-stop",
        "title": "A difficult reunion after rain",
        "source": "reconciliation-bus-stop-source.png",
        "concept": "reconciliation-bus-stop-32c-320x256.png",
        "guide": "reconciliation-bus-stop-layout-guide.png",
        "mood": "uncertainty, apology, and cautious hope",
        "dialogueSafeRegion": {"x": 42, "y": 232, "width": 236, "height": 24},
        "actorSafeRegion": {"x": 52, "y": 76, "width": 216, "height": 136},
    },
    {
        "id": "harvest-table-garden",
        "title": "A shared harvest table",
        "source": "harvest-table-garden-source.png",
        "concept": "harvest-table-garden-32c-320x256.png",
        "guide": "harvest-table-garden-layout-guide.png",
        "mood": "belonging, generosity, and celebration",
        "dialogueSafeRegion": {"x": 42, "y": 232, "width": 236, "height": 24},
        "actorSafeRegion": {"x": 42, "y": 52, "width": 236, "height": 160},
    },
    {
        "id": "fresh-start-apartment",
        "title": "Room to begin again",
        "source": "fresh-start-apartment-source.png",
        "concept": "fresh-start-apartment-32c-320x256.png",
        "guide": "fresh-start-apartment-layout-guide.png",
        "mood": "grief settling into agency and possibility",
        "dialogueSafeRegion": {"x": 42, "y": 232, "width": 236, "height": 24},
        "actorSafeRegion": {"x": 52, "y": 56, "width": 216, "height": 156},
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path, role: str) -> dict[str, object]:
    with Image.open(path) as image:
        width, height = image.size
        has_alpha = "A" in image.getbands()
        color_mode = image.mode
    return {
        "file": str(path.relative_to(ROOT)),
        "role": role,
        "width": width,
        "height": height,
        "colorMode": color_mode,
        "alpha": has_alpha,
        "sha256": sha256(path),
        "runtimeReady": False,
    }


def main() -> None:
    for directory in (SCENE_DIR, GUIDE_DIR, PREVIEW_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    records = []
    preview_images: list[tuple[dict[str, object], Image.Image]] = []
    for scene in SCENES:
        source_path = SOURCE_DIR / str(scene["source"])
        with Image.open(source_path) as source_image:
            source = source_image.convert("RGB")
            concept = source.resize(SIZE, Image.Resampling.LANCZOS).quantize(
                colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE
            )
            concept_path = SCENE_DIR / str(scene["concept"])
            concept.save(concept_path, optimize=True)
            concept_rgb = concept.convert("RGB")

        guide = Image.new("RGBA", SIZE, (0, 0, 0, 0))
        draw = ImageDraw.Draw(guide)
        actor = scene["actorSafeRegion"]
        draw.rectangle(
            (
                actor["x"],
                actor["y"],
                actor["x"] + actor["width"] - 1,
                actor["y"] + actor["height"] - 1,
            ),
            outline=(75, 235, 240, 230),
            width=2,
        )
        safe = scene["dialogueSafeRegion"]
        draw.rectangle(
            (
                safe["x"],
                safe["y"],
                safe["x"] + safe["width"] - 1,
                safe["y"] + safe["height"] - 1,
            ),
            fill=(244, 186, 66, 76),
            outline=(255, 211, 104, 245),
            width=2,
        )
        guide_path = GUIDE_DIR / str(scene["guide"])
        guide.save(guide_path, optimize=True)

        preview = Image.alpha_composite(concept_rgb.convert("RGBA"), guide).convert("RGB")
        preview_images.append((scene, preview.resize((640, 512), Image.Resampling.NEAREST)))
        records.append(
            {
                **scene,
                "sourceOutput": file_record(source_path, "preserved-source-output"),
                "files": [
                    file_record(concept_path, "32-color-320x256-concept"),
                    file_record(guide_path, "transparent-actor-and-dialogue-layout-guide"),
                ],
                "runtimeReady": False,
            }
        )

    contact = Image.new("RGB", (1280, 1120), (19, 24, 42))
    draw = ImageDraw.Draw(contact)
    font = ImageFont.load_default()
    positions = [(0, 0), (640, 0), (0, 560), (640, 560)]
    for (scene, preview), (x, y) in zip(preview_images, positions):
        draw.rectangle((x, y, x + 639, y + 47), fill=(19, 24, 42))
        draw.text((x + 12, y + 12), str(scene["title"]), font=font, fill=(255, 239, 206))
        draw.text((x + 12, y + 30), str(scene["mood"]), font=font, fill=(160, 207, 211))
        contact.paste(preview, (x, y + 48))
    preview_path = PREVIEW_DIR / "exclusive-scenes-variety-review-2x.png"
    contact.save(preview_path, optimize=True)

    manifest = {
        "batch": "exclusive-scenes-variety-v1",
        "canvas": {"width": SIZE[0], "height": SIZE[1]},
        "paletteLimit": 32,
        "runtimeReady": False,
        "sourceOutputs": {
            "preservedUnmodified": True,
            "files": [
                file_record(SOURCE_DIR / str(scene["source"]), "preserved-source-output")
                for scene in SCENES
            ],
        },
        "scenes": records,
        "previews": [file_record(preview_path, "nearest-neighbor-2x-contact-sheet-with-layout-guides")],
        "provenance": {
            "tool": "built-in image generator",
            "date": "2026-10-20",
            "sourceOutputsCopiedWithoutPixelEdits": True,
            "thirdPartyAssetsUsed": False,
            "suppliedArchivesUsed": False,
            "externalReferencesUsed": False,
            "promptRecord": "prompts.md",
            "normalizationScript": "build_scene_variety.py",
            "conceptPolicy": "Each preserved source is resized to 320x256 with Lanczos resampling and quantized to 32 colors without dithering. Preview contact sheet is 2x nearest-neighbor with staging guides overlaid.",
        },
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
