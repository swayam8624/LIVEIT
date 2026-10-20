"""Build a deterministic, original 24x32 named-character concept batch.

The drawings are deliberately hand-authored primitive pixel clusters. They are
concept exports, not runtime admissions. No external images or archive art are
read by this script.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
W, H = 24, 32
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("contact-a", "passing-a", "contact-b", "passing-b", "idle", "interact")
CATALOG = {
    "amelia": "liveit.prod.v1.pixel.sprite.named.amelia",
    "noah": "liveit.prod.v1.pixel.sprite.named.noah",
    "teacher": "liveit.prod.v1.pixel.sprite.named.teacher",
    "parent-one": "liveit.prod.v1.pixel.sprite.named.parent-one",
    "parent-two": "liveit.prod.v1.pixel.sprite.named.parent-two",
}

# Existing identity cues are intentionally explicit here so later identity QA
# can compare this batch against the older concept packages.
CHARACTERS = {
    "amelia": {
        "name": "Amelia Chen",
        "role": "adult friend",
        "skin": (183, 119, 78, 255), "skin_hi": (215, 153, 103, 255),
        "hair": (45, 28, 30, 255), "hair_hi": (83, 48, 45, 255),
        "top": (240, 225, 194, 255), "bottom": (41, 123, 125, 255),
        "accent": (70, 189, 176, 255), "shoe": (32, 50, 66, 255),
        "prop": "teal satchel", "silhouette": "brunette bob, apron dress",
    },
    "noah": {
        "name": "Noah Bennett",
        "role": "adult friend / café supervisor",
        "skin": (142, 94, 67, 255), "skin_hi": (185, 130, 91, 255),
        "hair": (27, 35, 47, 255), "hair_hi": (57, 71, 88, 255),
        "top": (219, 137, 76, 255), "bottom": (47, 68, 89, 255),
        "accent": (246, 191, 72, 255), "shoe": (38, 39, 49, 255),
        "prop": "apron notebook", "silhouette": "tall lean, rolled sleeves",
    },
    "teacher": {
        "name": "Bellweather teacher",
        "role": "school teacher",
        "skin": (105, 70, 60, 255), "skin_hi": (156, 106, 84, 255),
        "hair": (91, 54, 38, 255), "hair_hi": (137, 85, 56, 255),
        "top": (61, 115, 157, 255), "bottom": (57, 67, 86, 255),
        "accent": (236, 203, 106, 255), "shoe": (44, 43, 52, 255),
        "prop": "lesson pointer", "silhouette": "blue knit sweater, chalk badge",
    },
    "parent-one": {
        "name": "Mara Bellweather",
        "role": "parent / caregiver (canonical Mara)",
        "skin": (92, 54, 45, 255), "skin_hi": (142, 88, 65, 255),
        "hair": (32, 25, 28, 255), "hair_hi": (76, 48, 47, 255),
        "top": (172, 73, 64, 255), "bottom": (74, 91, 83, 255),
        "accent": (226, 170, 55, 255), "shoe": (46, 38, 43, 255),
        "prop": "mustard scarf and tote", "silhouette": "pear shape, short natural curls",
    },
    "parent-two": {
        "name": "Eli Bellweather",
        "role": "parent / caregiver (canonical Eli)",
        "skin": (135, 117, 82, 255), "skin_hi": (187, 161, 109, 255),
        "hair": (35, 32, 28, 255), "hair_hi": (76, 69, 56, 255),
        "top": (39, 62, 91, 255), "bottom": (73, 78, 73, 255),
        "accent": (196, 134, 57, 255), "shoe": (39, 40, 45, 255),
        "prop": "round glasses and work jacket", "silhouette": "tall lean, close-cropped hair",
    },
}


def box(d: ImageDraw.ImageDraw, xy, color):
    d.rectangle(xy, fill=color)


def draw_sprite(key: str, direction: str, phase: str) -> Image.Image:
    c = CHARACTERS[key]
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # Phase cadence: every state changes feet, hem, and one arm cluster.
    phase_i = PHASES.index(phase)
    if phase in ("contact-a", "contact-b"):
        stride = -2 if phase == "contact-a" else 2
        bounce = 0 if phase == "contact-a" else -1
    elif phase in ("passing-a", "passing-b"):
        stride = -1 if phase == "passing-a" else 1
        bounce = -1 if phase == "passing-a" else 0
    else:
        stride, bounce = 0, (0 if phase == "idle" else -1)
    if direction == "west":
        side = -1
    elif direction == "east":
        side = 1
    else:
        side = 0

    # Small grounding mark is part of the sprite, not an external shadow.
    box(d, (7, 30, 10, 31), (*c["shoe"][:3], 220))
    box(d, (13, 30, 16, 31), (*c["shoe"][:3], 220))

    # Legs and footwear are independently placed for each facing.
    if direction in ("south", "north"):
        left_x, right_x = 9 + stride, 14 - stride
        box(d, (left_x, 24 + bounce, left_x + 2, 30), c["bottom"])
        box(d, (right_x, 24 - bounce, right_x + 2, 30), c["bottom"])
        box(d, (left_x - 1, 30, left_x + 2, 31), c["shoe"])
        box(d, (right_x, 30, right_x + 3, 31), c["shoe"])
    else:
        leg_x = 10 + (1 if direction == "east" else -1)
        box(d, (leg_x + stride, 24 + bounce, leg_x + 3 + stride, 30), c["bottom"])
        box(d, (leg_x + 2 - stride, 24 - bounce, leg_x + 5 - stride, 30), c["bottom"])
        box(d, (leg_x - 1 + stride, 30, leg_x + 3 + stride, 31), c["shoe"])
        box(d, (leg_x + 2 - stride, 30, leg_x + 6 - stride, 31), c["shoe"])

    # Torso proportions differ by identity. The teacher's sweater and Mara's
    # cardigan carry the most visual mass; Noah/Eli stay tall and narrow.
    if key == "parent-one":
        torso = (6, 14 + bounce, 17, 25)
    elif key in ("noah", "parent-two"):
        torso = (8, 14 + bounce, 15, 25)
    elif key == "teacher":
        torso = (7, 14 + bounce, 16, 25)
    else:
        torso = (7, 14 + bounce, 16, 25)
    box(d, torso, c["top"])
    box(d, (torso[0] + 1, torso[1] + 2, torso[2] - 1, torso[1] + 3), c["accent"])
    # Hem / jacket contour pixels provide frame-to-frame readable cadence.
    if phase in ("passing-a", "passing-b"):
        box(d, (torso[0] - 1, torso[3] - 1, torso[0], torso[3]), c["top"])
        box(d, (torso[2] + 1, torso[3] - 2, torso[2] + 2, torso[3]), c["top"])
    if key == "parent-one":
        box(d, (5, 16 + bounce, 7, 22), c["top"])
        box(d, (16, 16 + bounce, 18, 22), c["top"])
        box(d, (8, 14 + bounce, 15, 16 + bounce), c["accent"])
        box(d, (7, 13 + bounce, 16, 14 + bounce), c["accent"])
    elif key == "parent-two":
        box(d, (7, 15 + bounce, 8, 22), c["top"])
        box(d, (15, 15 + bounce, 16, 22), c["top"])
        box(d, (11, 15 + bounce, 12, 24), c["accent"])
    elif key == "amelia":
        box(d, (6, 15 + bounce, 7, 22), c["accent"])
        box(d, (16, 15 + bounce, 17, 22), c["accent"])
    elif key == "noah":
        box(d, (7, 15 + bounce, 8, 22), c["top"])
        box(d, (15, 15 + bounce, 16, 22), c["top"])
        box(d, (11, 15 + bounce, 12, 22), c["accent"])
    else:
        box(d, (6, 16 + bounce, 7, 22), c["top"])
        box(d, (16, 16 + bounce, 17, 22), c["top"])

    # Head and hair are directional, with asymmetric ears/accessory pixels.
    if direction == "south":
        box(d, (8, 6 + bounce, 15, 14 + bounce), c["skin"])
        box(d, (9, 7 + bounce, 14, 9 + bounce), c["skin_hi"])
        box(d, (7, 5 + bounce, 16, 8 + bounce), c["hair"])
        box(d, (8, 4 + bounce, 14, 6 + bounce), c["hair"])
        box(d, (7, 7 + bounce, 8, 12 + bounce), c["hair"])
        box(d, (15, 7 + bounce, 16, 11 + bounce), c["hair"])
        # eyes and nose give front-facing readability.
        box(d, (9, 10 + bounce, 9, 10 + bounce), (35, 31, 35, 255))
        box(d, (14, 10 + bounce, 14, 10 + bounce), (35, 31, 35, 255))
        box(d, (11, 12 + bounce, 12, 12 + bounce), c["skin_hi"])
    elif direction == "north":
        box(d, (8, 6 + bounce, 15, 14 + bounce), c["hair"])
        box(d, (9, 8 + bounce, 14, 14 + bounce), c["hair_hi"])
        box(d, (7, 5 + bounce, 16, 9 + bounce), c["hair"])
        box(d, (8, 4 + bounce, 14, 6 + bounce), c["hair"])
        box(d, (7, 8 + bounce, 8, 12 + bounce), c["hair"])
        box(d, (15, 8 + bounce, 16, 12 + bounce), c["hair"])
    else:
        # Side faces intentionally differ by direction; no mirrored source.
        if direction == "west":
            box(d, (7, 6 + bounce, 14, 14 + bounce), c["skin"])
            box(d, (6, 5 + bounce, 12, 8 + bounce), c["hair"])
            box(d, (6, 8 + bounce, 8, 13 + bounce), c["hair"])
            box(d, (7, 10 + bounce, 7, 10 + bounce), (35, 31, 35, 255))
            box(d, (6, 11 + bounce, 6, 12 + bounce), c["skin_hi"])
        else:
            box(d, (9, 6 + bounce, 16, 14 + bounce), c["skin"])
            box(d, (11, 5 + bounce, 17, 8 + bounce), c["hair"])
            box(d, (15, 8 + bounce, 17, 13 + bounce), c["hair"])
            box(d, (16, 10 + bounce, 16, 10 + bounce), (35, 31, 35, 255))
            box(d, (17, 11 + bounce, 17, 12 + bounce), c["skin_hi"])

    # Identity accessories and interaction gesture.
    if key == "amelia":
        box(d, (15 if direction != "west" else 6, 14 + bounce, 17 if direction != "west" else 8, 15 + bounce), c["accent"])
        if direction == "north": box(d, (8, 5 + bounce, 9, 8 + bounce), c["hair_hi"])
    elif key == "noah":
        box(d, (9, 20 + bounce, 10, 21 + bounce), c["accent"])
        if direction == "south": box(d, (9, 9 + bounce, 14, 9 + bounce), c["hair_hi"])
    elif key == "teacher":
        box(d, (14, 16 + bounce, 15, 17 + bounce), c["accent"])
        if direction == "south": box(d, (8, 9 + bounce, 9, 11 + bounce), c["hair_hi"])
    elif key == "parent-one":
        box(d, (15, 16 + bounce, 17, 18 + bounce), c["accent"])
        box(d, (7, 8 + bounce, 8, 10 + bounce), c["hair_hi"])
    elif key == "parent-two":
        if direction == "south":
            box(d, (8, 10 + bounce, 10, 10 + bounce), (217, 216, 185, 255))
            box(d, (13, 10 + bounce, 15, 10 + bounce), (217, 216, 185, 255))
            box(d, (10, 10 + bounce, 13, 10 + bounce), (77, 70, 60, 255))
        box(d, (15, 17 + bounce, 16, 18 + bounce), c["accent"])

    if phase == "interact":
        # Each actor reaches toward a distinct prop, with handedness tied to
        # facing. This is a true pose change, not a one-pixel bob.
        if direction in ("south", "north"):
            hand_x = 17 if direction == "south" else 6
            box(d, (hand_x, 17, min(hand_x + 2, 23), 19), c["skin"])
            box(d, (hand_x + (2 if hand_x < 12 else -2), 16, hand_x + (3 if hand_x < 12 else -1), 17), c["accent"])
        elif direction == "west":
            box(d, (4, 17, 7, 19), c["skin"])
            box(d, (3, 16, 5, 17), c["accent"])
        else:
            box(d, (17, 17, 20, 19), c["skin"])
            box(d, (19, 16, 21, 17), c["accent"])
        if key == "teacher":
            box(d, (18 if direction != "west" else 3, 13, 19 if direction != "west" else 4, 20), c["accent"])
        elif key == "noah":
            box(d, (18 if direction != "west" else 3, 18, 20 if direction != "west" else 5, 20), c["accent"])
        elif key == "parent-one":
            box(d, (18 if direction != "west" else 3, 19, 20 if direction != "west" else 5, 21), c["accent"])

    return im


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "frames").mkdir(exist_ok=True)
    manifest = {
        "batch": "named-characters-batch-v1",
        "direction": "PIXEL-ONLY",
        "runtimeReady": False,
        "frameSize": {"width": W, "height": H},
        "pivot": {"x": 12, "y": 31},
        "directions": list(DIRECTIONS),
        "phases": list(PHASES),
        "characters": [],
        "frames": [],
        "atlases": [],
    }
    sheets = []
    for key, c in CHARACTERS.items():
        cdir = ROOT / "frames" / key
        cdir.mkdir(parents=True, exist_ok=True)
        records = []
        atlas = Image.new("RGBA", (W * 4, H * 6), (0, 0, 0, 0))
        for row, direction in enumerate(DIRECTIONS):
            for col, phase in enumerate(PHASES):
                im = draw_sprite(key, direction, phase)
                out = cdir / f"{key}-{direction}-{phase}.png"
                im.save(out, optimize=False)
                atlas.paste(im, (W * (col % 4), H * (row * 6 // 4 + col // 4)))
                records.append({
                    "id": f"{key}/{direction}/{phase}",
                    "character": key,
                    "displayName": c["name"],
                    "catalogId": CATALOG[key],
                    "direction": direction,
                    "phase": phase,
                    "file": str(out.relative_to(ROOT)),
                    "width": W, "height": H, "mode": "RGBA",
                    "pivot": {"x": 12, "y": 31},
                    "sha256": sha(out),
                    "runtimeReady": False,
                })
        # Recompose a readable 4 columns x 6 rows atlas in phase order.
        atlas = Image.new("RGBA", (W * 6, H * 4), (0, 0, 0, 0))
        for row, direction in enumerate(DIRECTIONS):
            for col, phase in enumerate(PHASES):
                atlas.paste(draw_sprite(key, direction, phase), (W * col, H * row))
        atlas_path = cdir / f"{key}-movement-atlas.png"
        atlas.save(atlas_path, optimize=False)
        preview = atlas.resize((atlas.width * 4, atlas.height * 4), Image.Resampling.NEAREST)
        preview_path = cdir / f"{key}-movement-preview-4x.png"
        preview.save(preview_path, optimize=False)
        manifest["characters"].append({
            "id": key, "displayName": c["name"], "role": c["role"],
            "catalogId": CATALOG[key], "silhouette": c["silhouette"],
            "identityCues": [c["prop"]], "runtimeReady": False,
        })
        manifest["atlases"].append({
            "character": key, "file": str(atlas_path.relative_to(ROOT)),
            "width": atlas.width, "height": atlas.height, "columns": list(PHASES),
            "rows": list(DIRECTIONS), "sha256": sha(atlas_path), "runtimeReady": False,
        })
        manifest["frames"].extend(records)
        sheets.append((key, atlas))

    contact_rows = (len(sheets) + 1) // 2
    contact = Image.new("RGBA", (W * 6 * 2 * 2, H * 4 * 2 * contact_rows), (22, 28, 44, 255))
    cd = ImageDraw.Draw(contact)
    for i, (key, atlas) in enumerate(sheets):
        x = (i % 2) * W * 6 * 2
        y = (i // 2) * H * 4 * 2
        contact.paste(atlas.resize((atlas.width * 2, atlas.height * 2), Image.Resampling.NEAREST), (x, y))
        cd.rectangle((x, y, x + 120, y + 11), fill=(22, 28, 44, 255))
        cd.text((x + 3, y + 1), key, fill=(245, 231, 183, 255))
    contact_path = ROOT / "named-characters-contact-sheet-2x.png"
    contact.save(contact_path, optimize=False)
    manifest["contactSheet"] = {"file": contact_path.name, "sha256": sha(contact_path), "runtimeReady": False}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    provenance = {
        "batch": "named-characters-batch-v1",
        "created": "2026-10-20",
        "method": "deterministic hand-authored Pillow pixel primitives",
        "sourceArchivesUsed": [], "externalImagesUsed": [],
        "license": "original project-owned concept work; no third-party art included",
        "identityReferences": {
            "amelia": "existing amelia-movement-batch-v1 and amelia-portrait.jpg cues only",
            "parent-one": "existing named-family-batch-v1 / family-walk-cycles-v1 Mara cues only",
            "parent-two": "existing named-family-batch-v1 / family-walk-cycles-v1 Eli cues only",
        },
        "prompt": "Original 24x32 RGBA top-down pixel sprite primitives with four independently authored directions and six state poses; no external art references.",
        "runtimeReady": False,
    }
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(manifest['frames'])} frames, {len(manifest['characters'])} characters")


if __name__ == "__main__":
    main()
