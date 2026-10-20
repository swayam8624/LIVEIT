#!/usr/bin/env python3
"""Build original named NPC movement studies for the five P0 catalog roles.

Every cluster is authored with integer Pillow primitives.  Cardinal views are
separate recipes rather than transformed copies, so later cleanup can preserve
direction-specific clothing and prop placement.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
SIZE = (24, 32)
PIVOT = {"x": 12, "y": 31}
DIRECTIONS = ("south", "west", "east", "north")
WALK_PHASES = ("contact-a", "passing-a", "contact-b", "passing-b")
STATES = WALK_PHASES + ("idle", "interact")

ROLES = {
    "boss": {
        "catalogId": "liveit.prod.v1.pixel.sprite.named.boss",
        "label": "boss",
        "skin": (176, 112, 83, 255), "hair": (44, 34, 38, 255),
        "shirt": (53, 67, 97, 255), "pants": (35, 42, 59, 255),
        "accent": (224, 176, 77, 255), "trim": (143, 175, 191, 255),
        "prop": "clipboard", "shape": "broad",
        "description": "Broad-shouldered director in a cobalt blazer with a gold pin and clipboard.",
    },
    "coworker": {
        "catalogId": "liveit.prod.v1.pixel.sprite.named.coworker",
        "label": "coworker",
        "skin": (214, 151, 111, 255), "hair": (80, 52, 43, 255),
        "shirt": (60, 132, 122, 255), "pants": (63, 69, 79, 255),
        "accent": (238, 198, 98, 255), "trim": (239, 225, 187, 255),
        "prop": "badge", "shape": "lean",
        "description": "Lean teammate in a teal overshirt with a lanyard badge and rolled notebook.",
    },
    "friend-one": {
        "catalogId": "liveit.prod.v1.pixel.sprite.named.friend-one",
        "label": "friend one",
        "skin": (119, 81, 70, 255), "hair": (33, 39, 53, 255),
        "shirt": (180, 92, 117, 255), "pants": (46, 58, 86, 255),
        "accent": (248, 178, 106, 255), "trim": (151, 211, 188, 255),
        "prop": "mug", "shape": "compact",
        "description": "Compact friend in a rose hoodie, striped trousers, and a bright takeaway mug.",
    },
    "friend-two": {
        "catalogId": "liveit.prod.v1.pixel.sprite.named.friend-two",
        "label": "friend two",
        "skin": (192, 137, 95, 255), "hair": (121, 70, 48, 255),
        "shirt": (76, 113, 157, 255), "pants": (91, 61, 79, 255),
        "accent": (231, 127, 79, 255), "trim": (247, 218, 131, 255),
        "prop": "phone", "shape": "tall",
        "description": "Tall friend in a blue jacket with warm auburn curls and a coral phone.",
    },
    "neighbor": {
        "catalogId": "liveit.prod.v1.pixel.sprite.named.neighbor",
        "label": "neighbor",
        "skin": (152, 101, 78, 255), "hair": (63, 50, 44, 255),
        "shirt": (89, 139, 99, 255), "pants": (66, 74, 61, 255),
        "accent": (216, 166, 76, 255), "trim": (188, 214, 172, 255),
        "prop": "plant", "shape": "round",
        "description": "Round-shouldered neighbor in a moss cardigan carrying a terracotta plant.",
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def box(draw: ImageDraw.ImageDraw, coords, color):
    draw.rectangle(tuple(int(v) for v in coords), fill=color)


def phase_step(phase: str) -> int:
    return {"contact-a": -1, "passing-a": 0, "contact-b": 1, "passing-b": 0, "idle": 0, "interact": 0}[phase]


def leg_offsets(phase: str) -> tuple[int, int]:
    """Return a distinct planted-leg silhouette for each gait moment."""
    return {
        "contact-a": (1, -1),
        "passing-a": (-1, 1),
        "contact-b": (-1, 1),
        "passing-b": (1, -1),
        # Idle keeps both feet level on the shared baseline.
        "idle": (1, 1),
        "interact": (0, 0),
    }[phase]


def draw_body(draw: ImageDraw.ImageDraw, role: dict, direction: str, phase: str):
    skin, hair, shirt, pants = role["skin"], role["hair"], role["shirt"], role["pants"]
    step = phase_step(phase)
    # Independent cardinal silhouettes.  These coordinates intentionally do
    # not derive one view from another or use image mirroring.
    if direction == "south":
        head = (8, 4 + step, 15, 10 + step)
        box(draw, head, skin); box(draw, (8, 4 + step, 15, 6 + step), hair)
        if role["shape"] == "tall": box(draw, (9, 4 + step, 16, 5 + step), hair)
        if role["shape"] == "round": box(draw, (7, 6 + step, 16, 9 + step), hair)
        torso = (7, 10 + step, 16, 19 + step)
        if role["shape"] == "lean": torso = (8, 10 + step, 15, 19 + step)
        if role["shape"] == "compact": torso = (7, 10 + step, 16, 18 + step)
        box(draw, torso, shirt)
        box(draw, (6, 11 + step, 7, 17 + step), skin); box(draw, (16, 11 + step, 17, 17 + step), skin)
        leg_y = 20 + step
        left, right = leg_offsets(phase)
        box(draw, (8, leg_y, 10, 29 + left), pants); box(draw, (13, leg_y, 15, 29 + right), pants)
        box(draw, (7, 29 + left, 10, 30 + left), hair); box(draw, (13, 29 + right, 16, 30 + right), hair)
        box(draw, (10, 7 + step, 11, 8 + step), role["trim"]); box(draw, (12, 7 + step, 13, 8 + step), role["trim"])
    elif direction == "west":
        box(draw, (7, 4 + step, 14, 10 + step), skin); box(draw, (6, 4 + step, 11, 7 + step), hair)
        if role["shape"] == "tall": box(draw, (7, 3 + step, 13, 5 + step), hair)
        if role["shape"] == "round": box(draw, (6, 7 + step, 10, 9 + step), hair)
        box(draw, (7, 10 + step, 14, 19 + step), shirt)
        box(draw, (6, 12 + step, 7, 18 + step), skin); box(draw, (4, 13 + step, 6, 16 + step), skin)
        leg_y = 20 + step
        left, right = leg_offsets(phase)
        box(draw, (7, leg_y, 9, 29 + left), pants); box(draw, (11, leg_y, 13, 29 + right), pants)
        box(draw, (6, 29 + left, 9, 30 + left), hair); box(draw, (11, 29 + right, 14, 30 + right), hair)
        box(draw, (7, 7 + step, 8, 8 + step), role["trim"])
    elif direction == "east":
        box(draw, (10, 4 + step, 17, 10 + step), skin); box(draw, (14, 4 + step, 19, 7 + step), hair)
        if role["shape"] == "tall": box(draw, (12, 3 + step, 18, 5 + step), hair)
        if role["shape"] == "round": box(draw, (15, 7 + step, 19, 9 + step), hair)
        box(draw, (10, 10 + step, 17, 19 + step), shirt)
        box(draw, (17, 12 + step, 18, 18 + step), skin); box(draw, (18, 13 + step, 20, 16 + step), skin)
        leg_y = 20 + step
        left, right = leg_offsets(phase)
        box(draw, (10, leg_y, 12, 29 + left), pants); box(draw, (14, leg_y, 16, 29 + right), pants)
        box(draw, (9, 29 + left, 12, 30 + left), hair); box(draw, (14, 29 + right, 17, 30 + right), hair)
        box(draw, (16, 7 + step, 17, 8 + step), role["trim"])
    else:  # north
        box(draw, (8, 4 + step, 15, 10 + step), hair); box(draw, (7, 5 + step, 16, 7 + step), hair)
        if role["shape"] == "tall": box(draw, (9, 3 + step, 16, 5 + step), hair)
        if role["shape"] == "round": box(draw, (7, 7 + step, 16, 10 + step), hair)
        box(draw, (7, 10 + step, 16, 19 + step), shirt)
        box(draw, (6, 12 + step, 7, 18 + step), role["trim"]); box(draw, (16, 12 + step, 17, 18 + step), role["trim"])
        leg_y = 20 + step
        left, right = leg_offsets(phase)
        box(draw, (8, leg_y, 10, 29 + left), pants); box(draw, (13, leg_y, 15, 29 + right), pants)
        box(draw, (7, 29 + left, 10, 30 + left), hair); box(draw, (13, 29 + right, 16, 30 + right), hair)


def draw_prop(draw: ImageDraw.ImageDraw, role: dict, direction: str, phase: str):
    accent, trim = role["accent"], role["trim"]
    interact = phase == "interact"
    if role["prop"] == "clipboard":
        if direction == "south": box(draw, (16 if not interact else 14, 14, 20 if not interact else 19, 21), accent); box(draw, (17, 15, 19, 16), trim)
        elif direction == "north": box(draw, (3 if not interact else 5, 14, 7 if not interact else 10, 21), accent); box(draw, (4, 15, 6, 16), trim)
        elif direction == "west": box(draw, (3, 14, 7 if not interact else 10, 20), accent); box(draw, (4, 15, 6, 16), trim)
        else: box(draw, (17 if not interact else 14, 14, 21 if not interact else 19, 20), accent); box(draw, (18, 15, 20, 16), trim)
    elif role["prop"] == "badge":
        if direction in ("south", "north"): box(draw, (10, 11, 13, 15), accent); box(draw, (11, 12, 12, 13), trim)
        elif direction == "west": box(draw, (7, 11, 10, 15), accent); box(draw, (8, 12, 9, 13), trim)
        else: box(draw, (14, 11, 17, 15), accent); box(draw, (15, 12, 16, 13), trim)
        if interact:
            box(draw, (3 if direction in ("south", "west") else 18, 16, 6 if direction in ("south", "west") else 21, 21), trim)
    elif role["prop"] == "mug":
        x = 3 if direction in ("south", "west") else 18
        y = 14 if not interact else 11
        box(draw, (x, y, x + 3, y + 4), accent); box(draw, (x + 3, y + 1, x + 4, y + 3), trim)
    elif role["prop"] == "phone":
        x = 3 if direction in ("south", "west") else 18
        y = 15 if not interact else 10
        box(draw, (x, y, x + 2, y + 5), accent); box(draw, (x, y + 1, x + 2, y + 2), trim)
    elif role["prop"] == "plant":
        x = 3 if direction in ("south", "west") else 18
        y = 18 if not interact else 14
        box(draw, (x, y, x + 4, y + 4), accent); box(draw, (x + 1, y - 3, x + 2, y), trim)
        box(draw, (x - 1, y - 4, x + 1, y - 2), trim); box(draw, (x + 2, y - 5, x + 4, y - 3), trim)


def draw_frame(role_key: str, direction: str, phase: str) -> Image.Image:
    image = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    role = ROLES[role_key]
    draw_body(draw, role, direction, phase)
    # Role-specific silhouette accents remain direction-aware and bounded.
    if role_key == "boss":
        if direction == "south": box(draw, (7, 9, 16, 11), role["accent"])
        elif direction == "north": box(draw, (7, 9, 16, 11), role["trim"])
        elif direction == "west": box(draw, (7, 9, 14, 11), role["accent"])
        else: box(draw, (10, 9, 17, 11), role["accent"])
    elif role_key == "coworker":
        box(draw, (10, 10, 13, 12), role["trim"])
    elif role_key == "friend-one":
        if direction in ("south", "north"): box(draw, (7, 9, 16, 11), role["shirt"])
        else: box(draw, (7, 9, 14 if direction == "west" else 17, 11), role["shirt"])
    elif role_key == "friend-two":
        if direction == "south": box(draw, (7, 5, 8, 8), role["accent"]); box(draw, (15, 5, 16, 8), role["accent"])
        elif direction == "west": box(draw, (6, 5, 8, 8), role["accent"])
        elif direction == "east": box(draw, (17, 5, 19, 8), role["accent"])
    else:
        if direction in ("south", "north"): box(draw, (7, 10, 16, 12), role["trim"])
        elif direction == "west": box(draw, (7, 10, 14, 12), role["trim"])
        else: box(draw, (10, 10, 17, 12), role["trim"])
    draw_prop(draw, role, direction, phase)
    return image


def validate_distinct_cycles(frames_root: Path) -> None:
    """Reject byte-identical walk/idle frames within any directional cycle."""
    checked = (*WALK_PHASES, "idle")
    for role_key in ROLES:
        for direction in DIRECTIONS:
            paths = [frames_root / role_key / f"{role_key}-{direction}-{phase}.png" for phase in checked]
            digests = [sha(path) for path in paths]
            if len(set(digests)) != len(checked):
                duplicates = sorted({digest for digest in digests if digests.count(digest) > 1})
                details = [f"{phase}={digest}" for phase, digest in zip(checked, digests) if digest in duplicates]
                raise ValueError(f"Duplicate locomotion phase bytes in {role_key}/{direction}: {', '.join(details)}")


def build() -> None:
    frames_root = ROOT / "frames"
    all_records, role_summaries = [], []
    for role_key, role in ROLES.items():
        role_root = frames_root / role_key
        role_root.mkdir(parents=True, exist_ok=True)
        atlas = Image.new("RGBA", (SIZE[0] * 6, SIZE[1] * 4), (0, 0, 0, 0))
        records = []
        for row, direction in enumerate(DIRECTIONS):
            for col, phase in enumerate(STATES):
                frame = draw_frame(role_key, direction, phase)
                path = role_root / f"{role_key}-{direction}-{phase}.png"
                frame.save(path, "PNG", optimize=False)
                atlas.alpha_composite(frame, (col * SIZE[0], row * SIZE[1]))
                record = {
                    "id": f"{role_key}/{direction}/{phase}", "role": role_key,
                    "catalogId": role["catalogId"], "direction": direction,
                    "phase": phase, "state": "walk" if phase in WALK_PHASES else phase,
                    "file": str(path.relative_to(ROOT)), "width": 24, "height": 32,
                    "mode": "RGBA", "pivot": PIVOT, "sha256": sha(path),
                    "runtimeReady": False,
                }
                records.append(record); all_records.append(record)
        atlas_path = role_root / "movement-atlas-4x6.png"
        atlas.save(atlas_path, "PNG", optimize=False)
        preview_path = role_root / "movement-atlas-preview-4x.png"
        atlas.resize((atlas.width * 4, atlas.height * 4), Image.Resampling.NEAREST).save(preview_path, "PNG", optimize=False)
        role_manifest = {
            "id": f"named-{role_key}-movement-v3", "role": role_key,
            "label": role["label"], "catalogId": role["catalogId"],
            "description": role["description"], "directions": list(DIRECTIONS),
            "states": list(STATES), "walkPhases": list(WALK_PHASES),
            "frameSize": {"width": 24, "height": 32}, "pivot": PIVOT,
            "frames": records,
            "atlas": {"file": str(atlas_path.relative_to(ROOT)), "width": atlas.width,
                      "height": atlas.height, "sha256": sha(atlas_path), "runtimeReady": False},
            "preview": {"file": str(preview_path.relative_to(ROOT)), "scale": 4,
                        "sha256": sha(preview_path), "runtimeReady": False},
            "runtimeReady": False,
        }
        (role_root / "manifest.json").write_text(json.dumps(role_manifest, indent=2) + "\n", encoding="utf-8")
        role_summaries.append({"role": role_key, "label": role["label"], "catalogId": role["catalogId"],
                               "manifest": str((role_root / "manifest.json").relative_to(ROOT)),
                               "frameCount": len(records), "runtimeReady": False})

    validate_distinct_cycles(frames_root)

    contact = Image.new("RGBA", (SIZE[0] * 6 * 3, SIZE[1] * 4 * 2), (10, 16, 25, 255))
    for i, role_key in enumerate(ROLES):
        atlas = Image.open(frames_root / role_key / "movement-atlas-4x6.png")
        contact.alpha_composite(atlas, ((i % 3) * atlas.width, (i // 3) * atlas.height))
    contact_path = ROOT / "named-characters-batch-v3-contact-sheet.png"
    contact.save(contact_path, "PNG", optimize=False)
    contact_preview = ROOT / "named-characters-batch-v3-contact-sheet-preview-2x.png"
    contact.resize((contact.width * 2, contact.height * 2), Image.Resampling.NEAREST).save(contact_preview, "PNG", optimize=False)
    provenance = {
        "batch": "named-characters-batch-v3", "created": "2026-10-20",
        "method": "Original deterministic pixel clusters authored in Pillow primitives; no supplied ZIP, downloaded art, model output, or third-party raster was sampled.",
        "canvas": {"width": 24, "height": 32, "mode": "RGBA", "pivot": PIVOT},
        "style": "24x32 nearest-neighbor pixel clusters, transparent backgrounds, independent cardinal recipes, six states per direction.",
        "rights": "No third-party source content. Project-owned derivative studies pending art direction, pixel cleanup, and import QA.",
    }
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "id": "named-characters-batch-v3", "kind": "original-pixel-named-character-movement-concepts",
        "catalogGroup": "named", "roles": role_summaries, "frameCount": len(all_records),
        "directions": list(DIRECTIONS), "states": list(STATES), "walkPhases": list(WALK_PHASES),
        "frameSize": {"width": 24, "height": 32}, "pivot": PIVOT,
        "contactSheet": {"file": contact_path.name, "width": contact.width, "height": contact.height,
                         "sha256": sha(contact_path), "runtimeReady": False},
        "contactPreview": {"file": contact_preview.name, "scale": 2, "sha256": sha(contact_preview), "runtimeReady": False},
        "runtimeReady": False,
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    hash_lines = []
    for path in sorted(ROOT.rglob("*.png")):
        hash_lines.append(f"{sha(path)}  {path.relative_to(ROOT)}")
    (ROOT / "hashes.sha256").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
