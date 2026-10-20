#!/usr/bin/env python3
"""Build the original crowd-archetypes movement batch v3.

This builder is intentionally dependency-light and deterministic.  Every
cluster is authored here with Pillow primitives; no archive, downloaded art,
model output, or mirrored image is read by the build.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
FRAME_SIZE = (24, 32)
PIVOT = (12, 31)
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("walk-a", "walk-b", "idle")

ROLES = {
    "security-guard": {
        "catalog": "liveit.prod.v1.pixel.sprite.crowd.security-guard", "label": "security guard",
        "skin": (181, 123, 91, 255), "hair": (43, 36, 39, 255), "top": (45, 67, 91, 255),
        "bottom": (31, 43, 59, 255), "accent": (239, 190, 65, 255), "prop": "guard",
        "description": "broad navy security uniform, cap, badge and shoulder radio",
    },
    "historian": {
        "catalog": "liveit.prod.v1.pixel.sprite.crowd.historian", "label": "historian",
        "skin": (137, 91, 72, 255), "hair": (77, 54, 53, 255), "top": (117, 82, 111, 255),
        "bottom": (65, 57, 76, 255), "accent": (216, 174, 102, 255), "prop": "scroll",
        "description": "long plum cardigan, round glasses, and a rolled archive scroll",
    },
    "park-cleaner": {
        "catalog": "liveit.prod.v1.pixel.sprite.crowd.park-cleaner", "label": "park cleaner",
        "skin": (197, 145, 106, 255), "hair": (56, 45, 42, 255), "top": (73, 145, 104, 255),
        "bottom": (57, 70, 68, 255), "accent": (236, 205, 87, 255), "prop": "broom",
        "description": "lime safety vest, utility belt, and long park broom",
    },
    "nurse": {
        "catalog": "liveit.prod.v1.pixel.sprite.crowd.nurse", "label": "nurse",
        "skin": (224, 166, 133, 255), "hair": (52, 42, 54, 255), "top": (106, 177, 184, 255),
        "bottom": (71, 118, 133, 255), "accent": (243, 238, 226, 255), "prop": "medical",
        "description": "teal scrubs, white badge, and compact medical shoulder bag",
    },
    "caregiver": {
        "catalog": "liveit.prod.v1.pixel.sprite.crowd.caregiver", "label": "caregiver",
        "skin": (110, 78, 68, 255), "hair": (31, 34, 42, 255), "top": (203, 118, 135, 255),
        "bottom": (68, 61, 80, 255), "accent": (249, 213, 149, 255), "prop": "tote",
        "description": "rose apron, soft scarf, and roomy care tote with hand wipes",
    },
    "gardener": {
        "catalog": "liveit.prod.v1.pixel.sprite.crowd.gardener", "label": "gardener",
        "skin": (170, 115, 83, 255), "hair": (77, 56, 39, 255), "top": (78, 135, 95, 255),
        "bottom": (76, 83, 61, 255), "accent": (228, 163, 74, 255), "prop": "watering",
        "description": "wide sun hat, green work shirt, gloves, and watering can",
    },
    "teacher": {
        "catalog": "liveit.prod.v1.pixel.sprite.crowd.teacher", "label": "teacher",
        "skin": (206, 151, 116, 255), "hair": (118, 67, 48, 255), "top": (72, 104, 161, 255),
        "bottom": (56, 63, 93, 255), "accent": (241, 204, 87, 255), "prop": "pointer",
        "description": "blue knit sweater, chalk badge, satchel, and lesson pointer",
    },
    "parent-with-stroller": {
        "catalog": "liveit.prod.v1.pixel.sprite.crowd.parent-with-stroller", "label": "parent with stroller",
        "skin": (186, 127, 101, 255), "hair": (42, 43, 51, 255), "top": (156, 91, 137, 255),
        "bottom": (55, 57, 81, 255), "accent": (111, 194, 187, 255), "prop": "stroller",
        "description": "lilac jacket with a joined four-view stroller and visible hood",
    },
    "child-playground": {
        "catalog": "liveit.prod.v1.pixel.sprite.crowd.child-playground", "label": "child playground",
        "skin": (222, 163, 123, 255), "hair": (83, 53, 39, 255), "top": (241, 124, 72, 255),
        "bottom": (55, 121, 139, 255), "accent": (242, 207, 73, 255), "prop": "ball",
        "description": "small orange hoodie, bright trainers, and a bouncing playground ball",
    },
    "elder-walker": {
        "catalog": "liveit.prod.v1.pixel.sprite.crowd.elder-walker", "label": "elder walker",
        "skin": (193, 151, 126, 255), "hair": (175, 177, 181, 255), "top": (119, 104, 138, 255),
        "bottom": (80, 82, 101, 255), "accent": (198, 186, 154, 255), "prop": "cane",
        "description": "gentle hunched gait, silver hair, cardigan, and stable walking cane",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rect(draw: ImageDraw.ImageDraw, box, color) -> None:
    x0, y0, x1, y1 = box
    draw.rectangle((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)), fill=color)


def draw_prop(draw: ImageDraw.ImageDraw, role: dict, direction: str, phase: str, y: int) -> None:
    """Draw each prop from its own cardinal recipe; never mirror a frame."""
    p, a = role["prop"], role["accent"]
    step = -1 if phase == "walk-a" else 1 if phase == "walk-b" else 0
    if p == "guard":
        # Cap and shoulder radio make the silhouette readable from every side.
        if direction == "south": rect(draw, (7, y, 16, y + 2), a); rect(draw, (4, y + 11, 6, y + 14), a)
        elif direction == "north": rect(draw, (8, y, 16, y + 2), a); rect(draw, (18, y + 11, 20, y + 14), a)
        elif direction == "west": rect(draw, (5, y + 1, 10, y + 3), a); rect(draw, (3, y + 12, 5, y + 15), a)
        else: rect(draw, (14, y + 1, 19, y + 3), a); rect(draw, (19, y + 12, 21, y + 15), a)
        rect(draw, (10, y + 7, 12, y + 9), a)
    elif p == "scroll":
        if direction == "south": rect(draw, (17, y + 14 + step, 20, y + 20 + step), a); rect(draw, (18, y + 13 + step, 19, y + 14 + step), a)
        elif direction == "north": rect(draw, (3, y + 14 - step, 6, y + 20 - step), a); rect(draw, (4, y + 13 - step, 5, y + 14 - step), a)
        elif direction == "west": rect(draw, (2, y + 14, 6, y + 19), a)
        else: rect(draw, (18, y + 14, 22, y + 19), a)
        # Round glasses/reading glint, authored per view.
        if direction == "south": rect(draw, (8, y + 5, 9, y + 6), a); rect(draw, (14, y + 5, 15, y + 6), a)
        elif direction == "west": rect(draw, (7, y + 4, 8, y + 5), a)
        elif direction == "east": rect(draw, (15, y + 4, 16, y + 5), a)
    elif p == "broom":
        if direction == "south": rect(draw, (18, y + 10 + step, 19, 28), a); rect(draw, (16, y + 26, 21, 29), a)
        elif direction == "north": rect(draw, (4, y + 10 - step, 5, 28), a); rect(draw, (2, y + 26, 7, 29), a)
        elif direction == "west": rect(draw, (3, y + 9, 4, 28), a); rect(draw, (1, y + 26, 6, 29), a)
        else: rect(draw, (20, y + 9, 21, 28), a); rect(draw, (18, y + 26, 23, 29), a)
        rect(draw, (8, y + 12, 15, y + 13), a)
    elif p == "medical":
        x = 3 if direction in ("south", "west") else 18
        rect(draw, (x, y + 16, x + 4, y + 21), a); rect(draw, (x + 1, y + 14, x + 3, y + 16), a)
        rect(draw, (10, y + 8, 12, y + 10), a)
    elif p == "tote":
        x = 2 if direction in ("south", "west") else 18
        rect(draw, (x, y + 16, x + 4, y + 22), a); rect(draw, (x + 1, y + 14, x + 3, y + 16), a)
        rect(draw, (10, y + 6, 11, y + 8), a)
    elif p == "watering":
        if direction == "south": rect(draw, (17, y + 15 + step, 21, y + 20 + step), a); rect(draw, (20, y + 16 + step, 22, y + 17 + step), a)
        elif direction == "north": rect(draw, (2, y + 15 - step, 6, y + 20 - step), a); rect(draw, (1, y + 16 - step, 3, y + 17 - step), a)
        elif direction == "west": rect(draw, (2, y + 15, 6, y + 20), a); rect(draw, (1, y + 16, 3, y + 17), a)
        else: rect(draw, (18, y + 15, 22, y + 20), a); rect(draw, (21, y + 16, 23, y + 17), a)
        # Wide hat brim is intentionally asymmetrical by view.
        if direction == "south": rect(draw, (6, y, 17, y + 1), a)
        elif direction == "north": rect(draw, (7, y, 17, y + 1), a)
        elif direction == "west": rect(draw, (5, y + 1, 11, y + 2), a)
        else: rect(draw, (13, y + 1, 19, y + 2), a)
    elif p == "pointer":
        if direction == "south": rect(draw, (18, y + 11 + step, 19, y + 23 + step), a)
        elif direction == "north": rect(draw, (4, y + 11 - step, 5, y + 23 - step), a)
        elif direction == "west": rect(draw, (3, y + 11, 4, y + 24), a)
        else: rect(draw, (20, y + 11, 21, y + 24), a)
        rect(draw, (9, y + 6, 10, y + 7), a)
    elif p == "stroller":
        # Chassis, hood and both wheels remain connected to the parent in all views.
        if direction == "south":
            rect(draw, (15, y + 13, 20, y + 23), a); rect(draw, (14, y + 12, 20, y + 14), a)
            rect(draw, (17, y + 23, 19, y + 28), (44, 61, 75, 255)); rect(draw, (15, 27, 17, 29), a); rect(draw, (19, 27, 21, 29), a)
        elif direction == "north":
            rect(draw, (4, y + 13, 9, y + 23), a); rect(draw, (4, y + 12, 10, y + 14), a)
            rect(draw, (5, y + 23, 7, y + 28), (44, 61, 75, 255)); rect(draw, (3, 27, 5, 29), a); rect(draw, (7, 27, 9, 29), a)
        elif direction == "west":
            rect(draw, (2, y + 14, 8, y + 22), a); rect(draw, (2, y + 12, 8, y + 14), a)
            rect(draw, (6, y + 21, 9, y + 27), (44, 61, 75, 255)); rect(draw, (2, 27, 5, 29), a); rect(draw, (7, 27, 10, 29), a)
        else:
            rect(draw, (16, y + 14, 22, y + 22), a); rect(draw, (16, y + 12, 22, y + 14), a)
            rect(draw, (15, y + 21, 18, y + 27), (44, 61, 75, 255)); rect(draw, (14, 27, 17, 29), a); rect(draw, (19, 27, 22, 29), a)
        rect(draw, (10, y + 10, 11, y + 13), a)
    elif p == "ball":
        x = 3 if direction in ("south", "west") else 18
        rect(draw, (x, y + 20 + step, x + 3, y + 23 + step), a)
        rect(draw, (x + 1, y + 20 + step, x + 2, y + 20 + step), role["top"])
    elif p == "cane":
        # A stable cane is present in every view; the elder's torso is separately hunched.
        if direction == "south": rect(draw, (18, y + 10, 19, 28), a); rect(draw, (17, y + 9, 19, y + 10), a); rect(draw, (16, 28, 21, 29), a)
        elif direction == "north": rect(draw, (4, y + 10, 5, 28), a); rect(draw, (4, y + 9, 6, y + 10), a); rect(draw, (2, 28, 7, 29), a)
        elif direction == "west": rect(draw, (3, y + 10, 4, 28), a); rect(draw, (3, y + 9, 5, y + 10), a); rect(draw, (1, 28, 6, 29), a)
        else: rect(draw, (20, y + 10, 21, 28), a); rect(draw, (19, y + 9, 21, y + 10), a); rect(draw, (18, 28, 23, 29), a)


def draw_frame(role_key: str, direction: str, phase: str) -> Image.Image:
    role = ROLES[role_key]
    image = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    step = -1 if phase == "walk-a" else 1 if phase == "walk-b" else 0
    # Elder and child have intentionally different posture/scale.
    y = 5 + step
    if role_key == "child-playground": y = 8 + step
    if role_key == "elder-walker": y = 6 + step
    skin, hair, top, bottom, accent = role["skin"], role["hair"], role["top"], role["bottom"], role["accent"]
    if role_key == "elder-walker":
        head_h, torso_h = 6, 9
    elif role_key == "child-playground":
        head_h, torso_h = 5, 7
    else:
        head_h, torso_h = 6, 9
    # Four cardinal recipes share only the palette; their outlines and feature
    # placement are written independently to avoid accidental mirrored frames.
    if direction == "south":
        rect(draw, (8, y, 15, y + head_h), skin); rect(draw, (7, y, 16, y + 2), hair)
        rect(draw, (9, y + head_h - 1, 14, y + head_h + torso_h), top)
        rect(draw, (8, y + 7, 9, y + 11), skin); rect(draw, (14, y + 7, 15, y + 11), skin)
        leg_y = y + head_h + torso_h
        rect(draw, (9, leg_y, 11, leg_y + 10 + (1 if phase == "walk-a" else 0)), bottom); rect(draw, (12, leg_y, 14, leg_y + 10 + (-1 if phase == "walk-b" else 0)), bottom)
        rect(draw, (8, leg_y + 10 + (1 if phase == "walk-a" else 0), 11, leg_y + 11 + (1 if phase == "walk-a" else 0)), hair)
        rect(draw, (12, leg_y + 10 + (-1 if phase == "walk-b" else 0), 15, leg_y + 11 + (-1 if phase == "walk-b" else 0)), hair)
        rect(draw, (8, y + 6, 9, y + 7), accent); rect(draw, (14, y + 6, 15, y + 7), accent)
    elif direction == "north":
        rect(draw, (8, y, 15, y + head_h), hair); rect(draw, (7, y + 1, 16, y + 3), hair)
        rect(draw, (9, y + head_h - 1, 14, y + head_h + torso_h), top); rect(draw, (8, y + 7, 9, y + 11), accent); rect(draw, (14, y + 7, 15, y + 11), accent)
        leg_y = y + head_h + torso_h
        rect(draw, (9, leg_y, 11, leg_y + 10 + (1 if phase == "walk-b" else 0)), bottom); rect(draw, (12, leg_y, 14, leg_y + 10 + (-1 if phase == "walk-a" else 0)), bottom)
    elif direction == "west":
        rect(draw, (8, y, 14, y + head_h), skin); rect(draw, (6, y + 1, 10, y + 4), hair); rect(draw, (8, y + 3, 9, y + 4), accent)
        rect(draw, (8, y + head_h - 1, 13, y + head_h + torso_h), top); rect(draw, (7, y + 8, 8, y + 12), skin); rect(draw, (5, y + 9, 7, y + 10), skin)
        leg_y = y + head_h + torso_h
        rect(draw, (8, leg_y, 10, leg_y + 10 + (1 if phase == "walk-a" else 0)), bottom); rect(draw, (11, leg_y, 13, leg_y + 10 + (-1 if phase == "walk-b" else 0)), bottom)
    else:
        rect(draw, (10, y, 16, y + head_h), skin); rect(draw, (14, y + 1, 18, y + 4), hair); rect(draw, (16, y + 3, 17, y + 4), accent)
        rect(draw, (10, y + head_h - 1, 15, y + head_h + torso_h), top); rect(draw, (15, y + 8, 16, y + 12), skin); rect(draw, (16, y + 9, 18, y + 10), skin)
        leg_y = y + head_h + torso_h
        rect(draw, (10, leg_y, 12, leg_y + 10 + (-1 if phase == "walk-a" else 0)), bottom); rect(draw, (13, leg_y, 15, leg_y + 10 + (1 if phase == "walk-b" else 0)), bottom)
    # Specific silhouettes add role variety without changing the shared pivot.
    if role_key == "security-guard":
        if direction in ("south", "north"): rect(draw, (7, y + 7, 16, y + 10), top)
        else: rect(draw, (7, y + 7, 14, y + 10), top)
    elif role_key == "historian":
        rect(draw, (9, y + 13, 14, y + 15), accent)
    elif role_key == "nurse":
        rect(draw, (10, y + 8, 12, y + 10), accent)
    elif role_key == "caregiver":
        rect(draw, (8, y + 12, 15, y + 14), accent)
    elif role_key == "teacher":
        rect(draw, (8, y + 13, 9, y + 16), accent)
    elif role_key == "elder-walker":
        # A lower shoulder and forward head make a stable, gentle gait readable.
        rect(draw, (9, y + 4, 14, y + 6), hair)
        if direction == "west": rect(draw, (8, y + 7, 13, y + 10), top)
        elif direction == "east": rect(draw, (10, y + 7, 15, y + 10), top)
    draw_prop(draw, role, direction, phase, y)
    rect(draw, (5, 30, 18, 31), (24, 30, 39, 125))
    return image


def build() -> None:
    frames_root = ROOT / "frames"
    all_records = []
    role_summaries = []
    for role_key, role in ROLES.items():
        role_dir = frames_root / role_key
        role_dir.mkdir(parents=True, exist_ok=True)
        atlas = Image.new("RGBA", (FRAME_SIZE[0] * 3, FRAME_SIZE[1] * 4), (0, 0, 0, 0))
        records = []
        for row, direction in enumerate(DIRECTIONS):
            for col, phase in enumerate(PHASES):
                frame = draw_frame(role_key, direction, phase)
                path = role_dir / f"{role_key}-{direction}-{phase}.png"
                frame.save(path, "PNG", optimize=False)
                atlas.alpha_composite(frame, (col * FRAME_SIZE[0], row * FRAME_SIZE[1]))
                record = {
                    "id": f"{role_key}/{direction}/{phase}", "role": role_key, "catalogId": role["catalog"],
                    "direction": direction, "phase": phase, "file": str(path.relative_to(ROOT)),
                    "width": 24, "height": 32, "mode": "RGBA", "pivot": {"x": 12, "y": 31},
                    "sha256": sha256(path), "runtimeReady": False,
                }
                records.append(record); all_records.append(record)
        atlas_path = role_dir / "movement-atlas-3x4.png"
        atlas.save(atlas_path, "PNG", optimize=False)
        preview_path = role_dir / "movement-atlas-preview-6x.png"
        atlas.resize((atlas.width * 6, atlas.height * 6), Image.Resampling.NEAREST).save(preview_path, "PNG", optimize=False)
        role_manifest = {
            "id": f"crowd-{role_key}-movement-v3", "role": role_key, "label": role["label"],
            "catalogId": role["catalog"], "description": role["description"], "directions": list(DIRECTIONS), "phases": list(PHASES),
            "frameSize": {"width": 24, "height": 32}, "pivot": {"x": 12, "y": 31}, "frames": records,
            "atlas": {"file": str(atlas_path.relative_to(ROOT)), "width": atlas.width, "height": atlas.height, "sha256": sha256(atlas_path), "runtimeReady": False},
            "preview": {"file": str(preview_path.relative_to(ROOT)), "scale": 6, "sha256": sha256(preview_path), "runtimeReady": False}, "runtimeReady": False,
        }
        (role_dir / "manifest.json").write_text(json.dumps(role_manifest, indent=2) + "\n", encoding="utf-8")
        role_summaries.append({"role": role_key, "catalogId": role["catalog"], "manifest": str((role_dir / "manifest.json").relative_to(ROOT)), "frameCount": len(records), "runtimeReady": False})

    contact = Image.new("RGBA", (FRAME_SIZE[0] * 3 * 5, FRAME_SIZE[1] * 4 * 2), (9, 14, 24, 255))
    for index, role_key in enumerate(ROLES):
        atlas = Image.open(frames_root / role_key / "movement-atlas-3x4.png")
        contact.alpha_composite(atlas, ((index % 5) * atlas.width, (index // 5) * atlas.height))
    contact_path = ROOT / "crowd-archetypes-batch-v3-contact-sheet.png"
    contact.save(contact_path, "PNG", optimize=False)
    contact_preview = ROOT / "crowd-archetypes-batch-v3-contact-sheet-preview-2x.png"
    contact.resize((contact.width * 2, contact.height * 2), Image.Resampling.NEAREST).save(contact_preview, "PNG", optimize=False)
    provenance = {
        "batch": "crowd-archetypes-batch-v3", "created": "2026-10-20",
        "method": "Original deterministic pixel clusters authored in Pillow primitives. No supplied ZIP, downloaded art, external raster, or model image was sampled.",
        "canvas": {"width": 24, "height": 32, "mode": "RGBA", "pivot": {"x": 12, "y": 31}},
        "style": "24x32 nearest-neighbor pixel clusters with transparent backgrounds and independently authored cardinal views.",
        "rights": "No third-party source content. Project-owned derivative studies pending art direction and import QA.",
    }
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    root_manifest = {
        "id": "crowd-archetypes-batch-v3", "kind": "original-pixel-crowd-movement-concepts", "catalogGroup": "crowd",
        "roles": role_summaries, "frameCount": len(all_records), "directions": list(DIRECTIONS), "phases": list(PHASES),
        "frameSize": {"width": 24, "height": 32}, "pivot": {"x": 12, "y": 31},
        "contactSheet": {"file": contact_path.name, "width": contact.width, "height": contact.height, "sha256": sha256(contact_path), "runtimeReady": False},
        "contactPreview": {"file": contact_preview.name, "scale": 2, "sha256": sha256(contact_preview), "runtimeReady": False},
        "runtimeReady": False,
    }
    (ROOT / "manifest.json").write_text(json.dumps(root_manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
