"""Build five original Bellweather named-role movement concept families.

The builder is deterministic and intentionally uses only local Pillow pixel
primitives.  It creates 24 independently drawn 24x32 RGBA frames per role:
four directions, four gait phases, idle, and a role-specific interaction.
These are isolated concept exports; they are not runtime admissions.
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
    "shopkeeper": "liveit.prod.v1.pixel.sprite.named.shopkeeper",
    "nurse": "liveit.prod.v1.pixel.sprite.named.nurse",
    "physician": "liveit.prod.v1.pixel.sprite.named.physician",
    "transit-worker": "liveit.prod.v1.pixel.sprite.named.transit-worker",
    "cafe-owner": "liveit.prod.v1.pixel.sprite.named.cafe-owner",
}

ROLES = {
    "shopkeeper": {
        "displayName": "Bellweather shopkeeper", "role": "market shopkeeper",
        "silhouette": "wide apron, rolled sleeves, neat side braid",
        "identityCues": ["red market sash", "small produce basket"],
        "skin": (177, 116, 78, 255), "skin_hi": (226, 161, 106, 255),
        "hair": (45, 29, 29, 255), "hair_hi": (104, 59, 44, 255),
        "top": (216, 219, 177, 255), "bottom": (73, 91, 73, 255),
        "accent": (190, 65, 58, 255), "prop": (215, 166, 67, 255),
        "shoe": (46, 41, 47, 255), "body": "wide", "interact": "basket",
    },
    "nurse": {
        "displayName": "Bellweather nurse", "role": "community clinic nurse",
        "silhouette": "compact scrub tunic, cropped curls, shoulder satchel",
        "identityCues": ["mint cross badge", "lavender care satchel"],
        "skin": (110, 72, 60, 255), "skin_hi": (164, 111, 84, 255),
        "hair": (39, 29, 35, 255), "hair_hi": (91, 59, 65, 255),
        "top": (119, 190, 177, 255), "bottom": (45, 78, 86, 255),
        "accent": (238, 221, 176, 255), "prop": (183, 133, 192, 255),
        "shoe": (37, 55, 64, 255), "body": "compact", "interact": "clipboard",
    },
    "physician": {
        "displayName": "Bellweather physician", "role": "neighborhood physician",
        "silhouette": "tall white coat, dark curls, stethoscope loop",
        "identityCues": ["coral stethoscope", "teal pen light"],
        "skin": (202, 145, 107, 255), "skin_hi": (238, 184, 135, 255),
        "hair": (32, 37, 47, 255), "hair_hi": (73, 80, 96, 255),
        "top": (224, 237, 225, 255), "bottom": (59, 70, 88, 255),
        "accent": (220, 92, 91, 255), "prop": (71, 171, 164, 255),
        "shoe": (41, 47, 58, 255), "body": "tall", "interact": "stethoscope",
    },
    "transit-worker": {
        "displayName": "Bellweather transit worker", "role": "tram and bus operator",
        "silhouette": "broad safety jacket, cap, utility belt",
        "identityCues": ["amber reflective bands", "blue route flag"],
        "skin": (119, 81, 67, 255), "skin_hi": (172, 121, 92, 255),
        "hair": (36, 34, 31, 255), "hair_hi": (83, 68, 55, 255),
        "top": (44, 83, 101, 255), "bottom": (48, 53, 63, 255),
        "accent": (237, 178, 67, 255), "prop": (75, 147, 190, 255),
        "shoe": (37, 40, 48, 255), "body": "broad", "interact": "flag",
    },
    "cafe-owner": {
        "displayName": "Bellweather cafe owner", "role": "corner cafe owner",
        "silhouette": "rounded apron, wavy bun, coffee towel at hip",
        "identityCues": ["plum apron", "cream mug and towel"],
        "skin": (144, 101, 82, 255), "skin_hi": (198, 148, 111, 255),
        "hair": (72, 43, 34, 255), "hair_hi": (132, 77, 50, 255),
        "top": (244, 212, 169, 255), "bottom": (71, 57, 82, 255),
        "accent": (132, 74, 122, 255), "prop": (223, 190, 124, 255),
        "shoe": (52, 42, 50, 255), "body": "round", "interact": "mug",
    },
}


def rect(d: ImageDraw.ImageDraw, xy, color):
    d.rectangle(xy, fill=color)


def phase_motion(phase: str) -> tuple[int, int]:
    if phase == "contact-a": return -2, 0
    if phase == "passing-a": return -1, -1
    if phase == "contact-b": return 2, 0
    if phase == "passing-b": return 1, -1
    if phase == "interact": return 0, -1
    return 0, 0


def draw_head(d, c, direction, y):
    skin, hi, hair, hair_hi = c["skin"], c["skin_hi"], c["hair"], c["hair_hi"]
    if direction == "south":
        rect(d, (8, y + 5, 15, y + 13), skin); rect(d, (9, y + 6, 14, y + 8), hi)
        rect(d, (7, y + 3, 16, y + 6), hair); rect(d, (8, y + 2, 14, y + 4), hair)
        rect(d, (7, y + 6, 8, y + 11), hair); rect(d, (15, y + 6, 16, y + 10), hair)
        rect(d, (9, y + 9, 9, y + 9), (27, 31, 34, 255)); rect(d, (14, y + 9, 14, y + 9), (27, 31, 34, 255))
    elif direction == "north":
        rect(d, (8, y + 4, 15, y + 13), hair); rect(d, (9, y + 7, 14, y + 13), hair_hi)
        rect(d, (7, y + 4, 16, y + 7), hair); rect(d, (8, y + 2, 14, y + 4), hair)
        rect(d, (7, y + 7, 8, y + 11), hair); rect(d, (15, y + 7, 16, y + 11), hair)
    elif direction == "west":
        rect(d, (7, y + 5, 14, y + 13), skin); rect(d, (6, y + 3, 12, y + 6), hair)
        rect(d, (6, y + 6, 8, y + 12), hair); rect(d, (7, y + 9, 7, y + 9), (27, 31, 34, 255))
        rect(d, (6, y + 10, 6, y + 11), hi); rect(d, (12, y + 7, 14, y + 8), hair_hi)
    else:
        rect(d, (9, y + 5, 16, y + 13), skin); rect(d, (11, y + 3, 17, y + 6), hair)
        rect(d, (15, y + 6, 17, y + 12), hair); rect(d, (16, y + 9, 16, y + 9), (27, 31, 34, 255))
        rect(d, (17, y + 10, 17, y + 11), hi); rect(d, (9, y + 7, 11, y + 8), hair_hi)


def draw_sprite(key: str, direction: str, phase: str) -> Image.Image:
    c = ROLES[key]; im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    stride, bounce = phase_motion(phase)
    body = c["body"]
    # Feet and legs. Directions have their own placements; no mirrored image is used.
    if direction in ("south", "north"):
        lx, rx = 9 + stride, 14 - stride
        rect(d, (lx, 24 + bounce, lx + 2, 30), c["bottom"]); rect(d, (rx, 24 - bounce, rx + 2, 30), c["bottom"])
        rect(d, (lx - 1, 30, lx + 2, 31), c["shoe"]); rect(d, (rx, 30, rx + 3, 31), c["shoe"])
    else:
        x = 10 + (1 if direction == "east" else -1)
        rect(d, (x + stride, 24 + bounce, x + 3 + stride, 30), c["bottom"])
        rect(d, (x + 2 - stride, 24 - bounce, x + 5 - stride, 30), c["bottom"])
        rect(d, (x - 1 + stride, 30, x + 3 + stride, 31), c["shoe"])
        rect(d, (x + 2 - stride, 30, x + 6 - stride, 31), c["shoe"])
    # Role-specific torso mass and hem movement.
    if body == "wide": torso = (6, 14 + bounce, 17, 25)
    elif body == "compact": torso = (7, 14 + bounce, 16, 25)
    elif body == "tall": torso = (8, 13 + bounce, 15, 25)
    elif body == "broad": torso = (6, 14 + bounce, 17, 25)
    else: torso = (6, 14 + bounce, 17, 25)
    rect(d, torso, c["top"]); rect(d, (torso[0] + 1, torso[1] + 2, torso[2] - 1, torso[1] + 3), c["accent"])
    if phase in ("passing-a", "passing-b"):
        rect(d, (torso[0] - 1, torso[3] - 1, torso[0], torso[3]), c["top"])
        rect(d, (torso[2] + 1, torso[3] - 2, torso[2] + 2, torso[3]), c["top"])
    # Signature outfit clusters.
    if key == "shopkeeper":
        rect(d, (7, 15 + bounce, 8, 23), c["top"]); rect(d, (15, 15 + bounce, 16, 23), c["top"])
        rect(d, (8, 14 + bounce, 15, 16 + bounce), c["accent"]); rect(d, (6, 19 + bounce, 7, 20 + bounce), c["prop"])
    elif key == "nurse":
        rect(d, (7, 16 + bounce, 8, 22), c["top"]); rect(d, (15, 16 + bounce, 16, 22), c["top"])
        rect(d, (11, 16 + bounce, 12, 19 + bounce), c["accent"]); rect(d, (10, 17 + bounce, 13, 18 + bounce), c["accent"])
    elif key == "physician":
        rect(d, (7, 15 + bounce, 8, 23), c["top"]); rect(d, (15, 15 + bounce, 16, 23), c["top"])
        rect(d, (11, 15 + bounce, 12, 24), c["accent"]); rect(d, (12, 19 + bounce, 14, 20 + bounce), c["prop"])
    elif key == "transit-worker":
        rect(d, (6, 15 + bounce, 7, 22), c["top"]); rect(d, (16, 15 + bounce, 17, 22), c["top"])
        rect(d, (6, 20 + bounce, 17, 21 + bounce), c["accent"]); rect(d, (8, 23 + bounce, 9, 24 + bounce), c["prop"])
    else:
        rect(d, (6, 16 + bounce, 7, 23), c["top"]); rect(d, (16, 16 + bounce, 17, 23), c["top"])
        rect(d, (8, 14 + bounce, 15, 16 + bounce), c["accent"]); rect(d, (15, 21 + bounce, 17, 22 + bounce), c["prop"])
    draw_head(d, c, direction, bounce)
    # Direction-dependent accessory pixels keep views independently authored.
    if key == "shopkeeper":
        if direction == "west": rect(d, (5, 5 + bounce, 7, 11 + bounce), c["hair_hi"])
        elif direction == "east": rect(d, (16, 5 + bounce, 18, 11 + bounce), c["hair_hi"])
        elif direction == "south": rect(d, (15, 4 + bounce, 17, 8 + bounce), c["hair_hi"])
        else: rect(d, (7, 4 + bounce, 9, 9 + bounce), c["hair_hi"])
    elif key == "nurse":
        rect(d, (8 if direction != "east" else 15, 4 + bounce, 9 if direction != "east" else 16, 5 + bounce), c["accent"])
    elif key == "physician":
        if direction == "south": rect(d, (8, 10 + bounce, 9, 11 + bounce), c["prop"]); rect(d, (14, 10 + bounce, 15, 11 + bounce), c["prop"])
        elif direction == "west": rect(d, (6, 8 + bounce, 7, 10 + bounce), c["prop"])
        elif direction == "east": rect(d, (16, 8 + bounce, 17, 10 + bounce), c["prop"])
    elif key == "transit-worker":
        if direction == "south": rect(d, (7, 2 + bounce, 16, 4 + bounce), c["accent"]); rect(d, (8, 4 + bounce, 15, 5 + bounce), c["hair"])
        elif direction == "north": rect(d, (7, 2 + bounce, 16, 4 + bounce), c["accent"])
        elif direction == "west": rect(d, (6, 3 + bounce, 11, 5 + bounce), c["accent"])
        else: rect(d, (13, 3 + bounce, 18, 5 + bounce), c["accent"])
    else:
        if direction == "south": rect(d, (9, 2 + bounce, 14, 4 + bounce), c["hair_hi"]); rect(d, (7, 5 + bounce, 8, 8 + bounce), c["hair"])
        elif direction == "north": rect(d, (9, 2 + bounce, 14, 4 + bounce), c["hair_hi"])
    # True interaction pose, with role prop held within the 24x32 frame.
    if phase == "interact":
        if direction == "south": hx, py = 17, 17
        elif direction == "north": hx, py = 6, 17
        elif direction == "west": hx, py = 4, 17
        else: hx, py = 18, 17
        rect(d, (hx, py, hx + 2, py + 2), c["skin"])
        if c["interact"] == "basket": rect(d, (hx + (-2 if hx > 12 else 2), py - 2, hx + (2 if hx > 12 else 6), py), c["prop"])
        elif c["interact"] == "clipboard": rect(d, (hx + (-2 if hx > 12 else 2), py - 3, hx + (1 if hx > 12 else 5), py + 1), c["prop"])
        elif c["interact"] == "stethoscope":
            rect(d, (hx + (-2 if hx > 12 else 2), py - 2, hx + (1 if hx > 12 else 5), py - 1), c["prop"])
            rect(d, (hx + (-1 if hx > 12 else 3), py - 1, hx + (0 if hx > 12 else 4), py + 1), c["prop"])
        elif c["interact"] == "flag": rect(d, (hx + (-1 if hx > 12 else 2), py - 6, hx + (0 if hx > 12 else 3), py + 1), c["prop"])
        else: rect(d, (hx + (-2 if hx > 12 else 2), py - 3, hx + (1 if hx > 12 else 5), py - 1), c["prop"])
    return im


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True); (ROOT / "frames").mkdir(exist_ok=True)
    manifest = {"batch": "named-characters-batch-v4", "direction": "PIXEL-ONLY", "runtimeReady": False,
                "frameSize": {"width": W, "height": H}, "pivot": {"x": 12, "y": 31},
                "directions": list(DIRECTIONS), "phases": list(PHASES), "characters": [], "frames": [], "atlases": []}
    contact = Image.new("RGBA", (W * 6, H * 5), (24, 31, 40, 255))
    for row, (key, c) in enumerate(ROLES.items()):
        cdir = ROOT / "frames" / key; cdir.mkdir(parents=True, exist_ok=True)
        manifest["characters"].append({"id": key, "displayName": c["displayName"], "role": c["role"], "catalogId": CATALOG[key], "silhouette": c["silhouette"], "identityCues": c["identityCues"], "runtimeReady": False})
        atlas = Image.new("RGBA", (W * 6, H * 4), (0, 0, 0, 0))
        for di, direction in enumerate(DIRECTIONS):
            for pi, phase in enumerate(PHASES):
                im = draw_sprite(key, direction, phase)
                fn = f"{key}-{direction}-{phase}.png"; fp = cdir / fn; im.save(fp)
                manifest["frames"].append({"id": f"{key}/{direction}/{phase}", "character": key, "catalogId": CATALOG[key], "direction": direction, "phase": phase, "file": f"frames/{key}/{fn}", "width": W, "height": H, "mode": "RGBA", "pivot": {"x": 12, "y": 31}, "sha256": digest(fp), "runtimeReady": False})
                atlas.paste(im, (pi * W, di * H), im); contact.paste(im.resize((W * 2, H * 2), Image.Resampling.NEAREST), (pi * W * 2, row * H * 2), im.resize((W * 2, H * 2), Image.Resampling.NEAREST))
        ap = cdir / f"{key}-movement-atlas.png"; atlas.save(ap); manifest["atlases"].append({"character": key, "file": f"frames/{key}/{ap.name}", "width": 144, "height": 128, "sha256": digest(ap), "runtimeReady": False})
        preview = atlas.resize((576, 512), Image.Resampling.NEAREST); pp = cdir / f"{key}-movement-preview-4x.png"; preview.save(pp); manifest["atlases"].append({"character": key, "file": f"frames/{key}/{pp.name}", "width": 576, "height": 512, "sha256": digest(pp), "runtimeReady": False})
    cp = ROOT / "named-characters-batch-v4-contact-sheet-2x.png"; contact.save(cp); manifest["atlases"].append({"file": cp.name, "width": contact.width, "height": contact.height, "sha256": digest(cp), "runtimeReady": False})
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (ROOT / "provenance.json").write_text(json.dumps({"batch": "named-characters-batch-v4", "created": "2026-10-20", "method": "deterministic hand-authored Pillow pixel primitives", "sourceArchivesUsed": [], "externalImagesUsed": [], "license": "original project-owned concept work; no third-party art included", "catalogSource": "content/production-assets/v1/pixel-world.json exact named sprite records", "runtimeReady": False}, indent=2) + "\n")


if __name__ == "__main__": main()
