"""Build original 24x32 crowd movement concepts.

The drawings in this file are deliberately authored as pixel clusters rather
than traced or transformed from an external sprite sheet.  Re-running the
builder produces byte-stable PNGs, atlases, previews and manifests.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
SIZE = (24, 32)
# Keep the original source-folder names so existing PNG paths and hashes stay
# stable. Manifests expose the catalog's cardinal direction contract below.
SOURCE_DIRECTIONS = ("front", "back", "left", "right")
CARDINAL_BY_SOURCE = {"front": "south", "back": "north", "left": "west", "right": "east"}
CARDINAL_DIRECTIONS = tuple(CARDINAL_BY_SOURCE[name] for name in SOURCE_DIRECTIONS)
PHASES = ("walk-a", "walk-b", "idle")
PIVOT = {"x": 12, "y": 31}

# Palette and silhouette choices are intentionally distinct for crowd readability.
ROLES = {
    "runner": {"skin": "#b86f52", "hair": "#2a1b25", "top": "#e45258", "bottom": "#303c6e", "accent": "#f3c45d", "prop": "headband"},
    "tourist": {"skin": "#d59672", "hair": "#563b2c", "top": "#f4d77b", "bottom": "#4d8b88", "accent": "#d86d50", "prop": "camera"},
    "mechanic": {"skin": "#9c624c", "hair": "#211d25", "top": "#3e6d82", "bottom": "#2d3942", "accent": "#e5a84b", "prop": "wrench"},
    "artist": {"skin": "#c47d63", "hair": "#7a3f35", "top": "#a6578d", "bottom": "#3a3657", "accent": "#71c4a8", "prop": "palette"},
    "filmmaker": {"skin": "#8d5b4a", "hair": "#1c2025", "top": "#4e5c8a", "bottom": "#33313f", "accent": "#e1b55d", "prop": "camera"},
    "athlete": {"skin": "#a9674d", "hair": "#33231e", "top": "#55a4c7", "bottom": "#d75b63", "accent": "#f0dc84", "prop": "ball"},
    "shopper": {"skin": "#d69a79", "hair": "#49322c", "top": "#cf7697", "bottom": "#536e9e", "accent": "#e9b35e", "prop": "bag"},
    "barista": {"skin": "#bb765b", "hair": "#2d2327", "top": "#e9e1d3", "bottom": "#6b4f63", "accent": "#bd5c54", "prop": "cup"},
    "pet-walker": {"skin": "#9a6654", "hair": "#30252d", "top": "#7ab38b", "bottom": "#394b5d", "accent": "#e3a85b", "prop": "leash"},
    "market-vendor": {"skin": "#c17b58", "hair": "#4d3025", "top": "#e48555", "bottom": "#5a4353", "accent": "#f4d573", "prop": "basket"},
}

CATALOG_IDS = {role: f"liveit.prod.v1.pixel.sprite.crowd.{role}" for role in ROLES}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rect(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill: str) -> None:
    draw.rectangle(xy, fill=fill)


def draw_character(role: str, direction: str, phase: str) -> Image.Image:
    c = ROLES[role]
    image = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(image)

    # A one-pixel ground contact keeps every role on the same bottom pivot.
    if phase == "walk-a":
        leg_offsets = (-1, 1)
        arm_offsets = (1, -1)
    elif phase == "walk-b":
        leg_offsets = (1, -1)
        arm_offsets = (-1, 1)
    else:
        leg_offsets = (0, 0)
        arm_offsets = (0, 0)

    # Hair and head are independently authored for each cardinal view.
    if direction == "front":
        rect(d, (8, 4, 15, 10), c["skin"])
        rect(d, (7, 3, 16, 6), c["hair"])
        rect(d, (7, 5, 8, 8), c["hair"])
        rect(d, (15, 5, 16, 8), c["hair"])
        rect(d, (9, 7, 9, 7), "#20202b")
        rect(d, (14, 7, 14, 7), "#20202b")
    elif direction == "back":
        rect(d, (8, 4, 15, 10), c["hair"])
        rect(d, (9, 9, 14, 11), c["skin"])
        rect(d, (7, 3, 16, 6), c["hair"])
    elif direction == "left":
        rect(d, (7, 4, 14, 10), c["skin"])
        rect(d, (6, 3, 12, 7), c["hair"])
        rect(d, (6, 6, 8, 9), c["hair"])
        rect(d, (7, 7, 7, 7), "#20202b")
        rect(d, (5, 8, 7, 9), c["skin"])
    else:
        rect(d, (9, 4, 16, 10), c["skin"])
        rect(d, (12, 3, 17, 7), c["hair"])
        rect(d, (15, 6, 17, 9), c["hair"])
        rect(d, (16, 7, 16, 7), "#20202b")
        rect(d, (16, 8, 18, 9), c["skin"])

    # Role-specific head silhouette cues.
    if role == "runner":
        rect(d, (7, 3, 16, 3), c["accent"])
    elif role == "tourist":
        rect(d, (6, 2, 17, 3), c["accent"])
        rect(d, (8, 3, 15, 3), c["accent"])
    elif role == "artist":
        rect(d, (6, 3, 7, 5), c["accent"])
    elif role == "barista":
        rect(d, (7, 2, 16, 3), c["accent"])
        rect(d, (9, 1, 14, 2), c["accent"])

    # Torso and arms vary by direction, but use the same 24x32 logical scale.
    if direction in ("front", "back"):
        rect(d, (8, 11, 15, 21), c["top"])
        rect(d, (7, 12 + arm_offsets[0], 8, 20 + arm_offsets[0]), c["skin"])
        rect(d, (15, 12 + arm_offsets[1], 16, 20 + arm_offsets[1]), c["skin"])
        rect(d, (9, 20, 14, 22), c["bottom"])
    elif direction == "left":
        rect(d, (7, 11, 14, 21), c["top"])
        rect(d, (6, 13 + arm_offsets[0], 7, 20 + arm_offsets[0]), c["skin"])
        rect(d, (14, 12 + arm_offsets[1], 15, 19 + arm_offsets[1]), c["skin"])
        rect(d, (8, 20, 13, 22), c["bottom"])
    else:
        rect(d, (9, 11, 16, 21), c["top"])
        rect(d, (8, 12 + arm_offsets[0], 9, 19 + arm_offsets[0]), c["skin"])
        rect(d, (16, 13 + arm_offsets[1], 17, 20 + arm_offsets[1]), c["skin"])
        rect(d, (10, 20, 15, 22), c["bottom"])

    # Clothing details make the archetypes distinguishable at small scale.
    if role == "mechanic":
        rect(d, (10, 12, 10, 20), c["accent"])
        rect(d, (13, 12, 13, 20), c["accent"])
    elif role == "barista":
        rect(d, (11, 12, 12, 19), c["accent"])
    elif role == "athlete":
        rect(d, (10, 12, 13, 12), c["accent"])
    elif role == "market-vendor":
        rect(d, (8, 19, 15, 20), c["accent"])
    elif role == "tourist":
        rect(d, (9, 14, 14, 15), c["accent"])

    # Legs have deliberately different phase positions; no frame is mirrored.
    left_x, right_x = 9 + leg_offsets[0], 13 + leg_offsets[1]
    rect(d, (left_x, 22, left_x + 2, 29), c["bottom"])
    rect(d, (right_x, 22, right_x + 2, 29), c["bottom"])
    rect(d, (left_x - 1, 29, left_x + 2, 30), "#22283c")
    rect(d, (right_x - 1, 29, right_x + 2, 30), "#22283c")
    rect(d, (left_x, 30, left_x + 2, 31), "#20202b")
    rect(d, (right_x, 30, right_x + 2, 31), "#20202b")

    # Held objects are role-specific and directional, using asymmetric placement.
    prop_x = {"front": 17, "back": 16, "left": 4, "right": 18}[direction]
    prop_y = 16 + (1 if phase == "walk-b" else 0)
    if c["prop"] == "headband":
        pass
    elif c["prop"] == "camera":
        rect(d, (prop_x, prop_y, prop_x + 2, prop_y + 2), "#252c3b")
        rect(d, (prop_x + 1, prop_y - 1, prop_x + 1, prop_y), c["accent"])
    elif c["prop"] == "wrench":
        rect(d, (prop_x, prop_y - 2, prop_x, prop_y + 3), c["accent"])
        rect(d, (prop_x - 1, prop_y - 2, prop_x + 1, prop_y - 1), c["accent"])
    elif c["prop"] == "palette":
        rect(d, (prop_x, prop_y, prop_x + 3, prop_y + 2), c["accent"])
        rect(d, (prop_x + 1, prop_y, prop_x + 1, prop_y), c["top"])
    elif c["prop"] == "ball":
        rect(d, (prop_x, prop_y, prop_x + 2, prop_y + 2), c["accent"])
        rect(d, (prop_x + 1, prop_y + 1, prop_x + 1, prop_y + 1), c["top"])
    elif c["prop"] == "bag":
        rect(d, (prop_x, prop_y, prop_x + 3, prop_y + 3), c["accent"])
        rect(d, (prop_x + 1, prop_y - 1, prop_x + 2, prop_y - 1), c["accent"])
    elif c["prop"] == "cup":
        rect(d, (prop_x, prop_y, prop_x + 2, prop_y + 2), c["accent"])
        rect(d, (prop_x + 3, prop_y + 1, prop_x + 3, prop_y + 2), c["accent"])
    elif c["prop"] == "leash":
        rect(d, (prop_x, prop_y, prop_x, prop_y + 6), c["accent"])
        rect(d, (prop_x + 1, prop_y + 6, prop_x + 3, prop_y + 8), c["accent"])
        rect(d, (prop_x + 2, prop_y + 8, prop_x + 4, prop_y + 9), c["top"])
    elif c["prop"] == "basket":
        rect(d, (prop_x, prop_y, prop_x + 3, prop_y + 3), c["accent"])
        rect(d, (prop_x, prop_y - 1, prop_x + 3, prop_y - 1), c["accent"])

    # Keep edges crisp and ensure alpha is binary for nearest-neighbour import.
    alpha = image.getchannel("A").point(lambda value: 255 if value else 0)
    image.putalpha(alpha)
    return image


def write_atlas(frames: list[tuple[str, str, Path]], out: Path) -> tuple[Path, Path]:
    atlas = Image.new("RGBA", (SIZE[0] * 3, SIZE[1] * 4), (0, 0, 0, 0))
    for direction, phase, path in frames:
        atlas.paste(Image.open(path), (PHASES.index(phase) * SIZE[0], SOURCE_DIRECTIONS.index(direction) * SIZE[1]))
    atlas_path = out / "movement-atlas-3x4.png"
    atlas.save(atlas_path)
    preview_path = out / "movement-preview-6x.png"
    atlas.resize((atlas.width * 6, atlas.height * 6), Image.Resampling.NEAREST).save(preview_path)
    return atlas_path, preview_path


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    all_records: list[dict] = []
    contact = Image.new("RGBA", (SIZE[0] * 3 * len(ROLES), SIZE[1] * 4), (0, 0, 0, 0))
    for role, colors in ROLES.items():
        role_dir = ROOT / role
        role_dir.mkdir(exist_ok=True)
        frames: list[tuple[str, str, Path]] = []
        records = []
        for direction in SOURCE_DIRECTIONS:
            (role_dir / direction).mkdir(exist_ok=True)
            for phase in PHASES:
                path = role_dir / direction / f"{phase}.png"
                draw_character(role, direction, phase).save(path)
                frames.append((direction, phase, path))
                records.append({
                    "direction": CARDINAL_BY_SOURCE[direction],
                    "sourceDirection": direction,
                    "phase": phase,
                    "file": str(path.relative_to(role_dir)),
                    "width": SIZE[0],
                    "height": SIZE[1],
                    "mode": "RGBA",
                    "pivot": PIVOT,
                    "runtimeReady": False,
                    "sha256": sha256(path),
                })
        atlas_path, preview_path = write_atlas(frames, role_dir)
        # Place each role's atlas into the combined contact sheet.
        contact.paste(Image.open(atlas_path), ((list(ROLES).index(role) * 3 * SIZE[0]), 0))
        manifest = {
            "id": f"crowd-archetypes-batch-v2.{role}",
            "catalogId": CATALOG_IDS[role],
            "role": role,
            "frameSize": {"width": SIZE[0], "height": SIZE[1]},
            "directions": list(CARDINAL_DIRECTIONS),
            "directionConvention": "north=back, east=right, south=front, west=left; sourceDirection preserves the legacy folder name",
            "phases": list(PHASES),
            "frames": records,
            "atlas": {"file": atlas_path.name, "width": SIZE[0] * 3, "height": SIZE[1] * 4, "columns": list(PHASES), "rows": list(CARDINAL_DIRECTIONS), "runtimeReady": False, "sha256": sha256(atlas_path)},
            "preview": {"file": preview_path.name, "scale": 6, "runtimeReady": False, "sha256": sha256(preview_path)},
            "runtimeReady": False,
        }
        (role_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        all_records.append({"role": role, "catalogId": CATALOG_IDS[role], "manifest": str((role_dir / "manifest.json").relative_to(ROOT)), "frameCount": len(records), "runtimeReady": False})

    # Add compact labels so the review sheet communicates role columns and
    # cardinal atlas rows without changing any role frame or atlas bytes.
    labels = ("runner", "tourist", "mechanic", "artist", "film", "athlete", "shopper", "barista", "pet", "vendor")
    labeled = Image.new("RGBA", (contact.width + 28, contact.height + 10), (16, 20, 30, 255))
    labeled.alpha_composite(contact, (28, 10))
    label_draw = ImageDraw.Draw(labeled)
    for index, label in enumerate(labels):
        label_draw.text((28 + index * SIZE[0] * 3 + 2, 1), label, fill="#e8e1c8")
    for index, label in enumerate(("S", "N", "W", "E")):
        label_draw.text((9, 10 + index * SIZE[1] + 10), label, fill="#e8e1c8")
    contact_path = ROOT / "crowd-archetypes-contact-sheet.png"
    labeled.resize((labeled.width * 2, labeled.height * 2), Image.Resampling.NEAREST).save(contact_path)
    manifest = {
        "id": "crowd-archetypes-batch-v2",
        "kind": "original-pixel-crowd-movement-concepts",
        "frameSize": {"width": SIZE[0], "height": SIZE[1]},
        "directions": list(CARDINAL_DIRECTIONS),
        "directionConvention": "north=back, east=right, south=front, west=left; PNG folders retain legacy source names",
        "phases": list(PHASES),
        "roles": all_records,
        "contactSheet": {"file": contact_path.name, "scale": 2, "labels": {"roles": list(ROLES), "rows": list(CARDINAL_DIRECTIONS)}, "runtimeReady": False, "sha256": sha256(contact_path)},
        "provenance": "All pixels are deterministic original drawings authored in build_crowd_archetypes.py; no supplied archive or internet asset was used.",
        "runtimeReady": False,
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (ROOT / "provenance.json").write_text(json.dumps({
        "sourceType": "original-authored-pixel-clusters",
        "builder": "build_crowd_archetypes.py",
        "builderSha256": sha256(ROOT / "build_crowd_archetypes.py"),
        "directionConvention": {"north": "back", "east": "right", "south": "front", "west": "left"},
        "externalAssets": [],
        "license": "Original work; no third-party source pixels incorporated.",
        "runtimeReady": False,
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
