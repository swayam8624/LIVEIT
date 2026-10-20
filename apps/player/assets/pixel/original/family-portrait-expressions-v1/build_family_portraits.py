#!/usr/bin/env python3
"""Build rights-safe named-family portrait expression concepts.

The art is authored from simple pixel primitives at 48x48 and enlarged with
nearest-neighbour sampling.  No third-party images are read by this builder.
The local named-family concept board is recorded as an identity reference only.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
SCALE = 2
BASE = 48
SIZE = BASE * SCALE
EMOTIONS = [
    "neutral",
    "happy",
    "sad",
    "angry",
    "shocked",
    "scared",
    "smug",
    "crying",
    "embarrassed",
    "tired",
    "thoughtful",
    "speaking",
]

CHARACTERS = {
    "mara": {
        "displayName": "Mara",
        "stableId": "parent_mara",
        "role": "adult parent/caregiver",
        "skin": "#8b4b32",
        "skin_shadow": "#603022",
        "hair": "#281a1c",
        "hair_hi": "#4b2c25",
        "coat": "#b94d32",
        "coat_shadow": "#7b3028",
        "accent": "#e0a33e",
        "shirt": "#f2e0c2",
        "outline": "#241923",
        "identity": ["short natural curls", "mustard scarf", "rust cardigan"],
        "hairStyle": "curls",
    },
    "eli": {
        "displayName": "Eli",
        "stableId": "parent_eli",
        "role": "adult parent/caregiver",
        "skin": "#ad7047",
        "skin_shadow": "#744329",
        "hair": "#211c24",
        "hair_hi": "#3c3340",
        "coat": "#29395d",
        "coat_shadow": "#1d2846",
        "accent": "#daa13e",
        "shirt": "#e0a538",
        "outline": "#191a29",
        "identity": ["close-cropped dark hair", "round glasses", "navy work jacket"],
        "hairStyle": "close-crop",
    },
    "niko": {
        "displayName": "Niko",
        "stableId": "sibling_niko",
        "role": "school-age sibling",
        "skin": "#a95a36",
        "skin_shadow": "#723723",
        "hair": "#2a1a20",
        "hair_hi": "#4d2c2b",
        "coat": "#2f6dcc",
        "coat_shadow": "#214587",
        "accent": "#ec7d31",
        "shirt": "#dce9f4",
        "outline": "#171b2d",
        "identity": ["curly ponytail", "cobalt hoodie", "orange hair tie"],
        "hairStyle": "ponytail",
    },
    "aunt-sol": {
        "displayName": "Aunt Sol",
        "stableId": "relative_aunt_sol",
        "role": "older relative",
        "skin": "#a96645",
        "skin_shadow": "#70412f",
        "hair": "#d5c5b5",
        "hair_hi": "#f0e2d0",
        "coat": "#713c68",
        "coat_shadow": "#4a294e",
        "accent": "#a5b887",
        "shirt": "#f1e2c9",
        "outline": "#241d2c",
        "identity": ["silver braid", "plum coat", "sage scarf"],
        "hairStyle": "braid",
    },
}


def hexrgb(value: str) -> tuple[int, int, int]:
    return tuple(int(value[i : i + 2], 16) for i in (1, 3, 5))


def rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: str) -> None:
    draw.rectangle(box, fill=hexrgb(color))


def ellipse(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: str) -> None:
    draw.ellipse(box, fill=hexrgb(color))


def line(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], color: str, width: int = 1) -> None:
    draw.line(points, fill=hexrgb(color), width=width)


def draw_hair(draw: ImageDraw.ImageDraw, c: dict, style: str) -> None:
    if style == "curls":
        for x, y, r in [(15, 12, 4), (19, 8, 4), (24, 7, 4), (29, 8, 4), (34, 12, 4), (14, 17, 3), (34, 17, 3)]:
            ellipse(draw, (x - r, y - r, x + r, y + r), c["hair"])
        for x, y in [(17, 10), (23, 7), (29, 9), (14, 16), (34, 15)]:
            rect(draw, (x, y, x + 2, y + 2), c["hair_hi"])
    elif style == "close-crop":
        rect(draw, (16, 7, 32, 17), c["hair"])
        rect(draw, (18, 6, 30, 9), c["hair_hi"])
        rect(draw, (15, 10, 17, 17), c["hair"])
        rect(draw, (31, 10, 33, 17), c["hair"])
    elif style == "ponytail":
        ellipse(draw, (8, 7, 19, 20), c["hair"])
        ellipse(draw, (11, 5, 22, 16), c["hair"])
        ellipse(draw, (15, 3, 25, 14), c["hair"])
        rect(draw, (20, 5, 22, 8), c["accent"])
        rect(draw, (16, 8, 31, 17), c["hair"])
        rect(draw, (18, 7, 29, 9), c["hair_hi"])
    else:  # silver braid
        rect(draw, (16, 7, 32, 17), c["hair"])
        for y, x in [(13, 13), (17, 12), (21, 13), (25, 12), (29, 13)]:
            ellipse(draw, (x - 2, y - 3, x + 3, y + 3), c["hair"])
            rect(draw, (x, y - 2, x + 2, y), c["hair_hi"])
        rect(draw, (16, 8, 31, 10), c["hair_hi"])


def draw_face(draw: ImageDraw.ImageDraw, c: dict, emotion: str) -> None:
    # Eyes and brows are deliberately pixel-sized and remain readable at 2x.
    eye = hexrgb(c["outline"])
    white = (248, 239, 211)
    if emotion == "tired":
        line(draw, [(18, 20), (21, 20)], c["outline"], 1)
        line(draw, [(27, 20), (30, 20)], c["outline"], 1)
    elif emotion == "shocked":
        ellipse(draw, (18, 18, 22, 23), "#f8efd3")
        ellipse(draw, (26, 18, 30, 23), "#f8efd3")
        rect(draw, (20, 20, 21, 22), c["outline"])
        rect(draw, (27, 20, 28, 22), c["outline"])
        line(draw, [(18, 17), (21, 16)], c["outline"], 1)
        line(draw, [(27, 16), (30, 17)], c["outline"], 1)
    elif emotion == "scared":
        ellipse(draw, (18, 19, 22, 23), "#f8efd3")
        ellipse(draw, (26, 19, 30, 23), "#f8efd3")
        rect(draw, (20, 21, 21, 22), c["outline"])
        rect(draw, (27, 21, 28, 22), c["outline"])
        line(draw, [(18, 17), (21, 18)], c["outline"], 1)
        line(draw, [(27, 18), (30, 17)], c["outline"], 1)
    else:
        rect(draw, (18, 19, 21, 21), "#f8efd3")
        rect(draw, (27, 19, 30, 21), "#f8efd3")
        rect(draw, (20, 20, 21, 21), c["outline"])
        rect(draw, (27, 20, 28, 21), c["outline"])
        if emotion == "angry":
            line(draw, [(17, 17), (21, 19)], c["outline"], 1)
            line(draw, [(27, 19), (31, 17)], c["outline"], 1)
        elif emotion == "thoughtful":
            line(draw, [(17, 18), (21, 17)], c["outline"], 1)
            line(draw, [(27, 17), (31, 18)], c["outline"], 1)
        elif emotion == "tired":
            line(draw, [(17, 18), (21, 18)], c["outline"], 1)
            line(draw, [(27, 18), (31, 18)], c["outline"], 1)
    if emotion == "embarrassed":
        rect(draw, (15, 23, 18, 24), "#d8786b")
        rect(draw, (30, 23, 33, 24), "#d8786b")
    if emotion in {"sad", "crying"}:
        rect(draw, (20, 23, 21, 25), "#63a9c2")
        rect(draw, (28, 23, 29, 25), "#63a9c2")
    if emotion == "happy":
        line(draw, [(20, 25), (22, 26), (27, 26), (29, 25)], c["outline"], 1)
    elif emotion == "sad":
        line(draw, [(21, 27), (24, 26), (27, 27)], c["outline"], 1)
    elif emotion == "angry":
        line(draw, [(21, 26), (24, 25), (27, 26)], c["outline"], 1)
    elif emotion == "shocked" or emotion == "scared":
        ellipse(draw, (22, 24, 26, 28), c["outline"])
    elif emotion == "crying":
        line(draw, [(21, 26), (24, 25), (27, 26)], c["outline"], 1)
        rect(draw, (18, 26, 19, 28), "#63a9c2")
        rect(draw, (30, 26, 31, 28), "#63a9c2")
    elif emotion == "embarrassed":
        line(draw, [(21, 26), (24, 25), (27, 26)], c["outline"], 1)
    elif emotion == "tired":
        line(draw, [(21, 26), (27, 26)], c["outline"], 1)
    elif emotion == "thoughtful":
        line(draw, [(22, 26), (25, 25), (27, 25)], c["outline"], 1)
    elif emotion == "speaking":
        rect(draw, (22, 25, 26, 27), c["outline"])
        rect(draw, (23, 25, 25, 25), c["shirt"])
    elif emotion == "smug":
        line(draw, [(21, 25), (25, 26), (28, 24)], c["outline"], 1)
    else:
        line(draw, [(22, 26), (26, 26)], c["outline"], 1)


def draw_character(character: str, emotion: str) -> Image.Image:
    c = CHARACTERS[character]
    im = Image.new("RGBA", (BASE, BASE), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # shoulders / clothing bust
    ellipse(d, (6, 28, 42, 58), c["outline"])
    ellipse(d, (8, 29, 40, 58), c["coat"])
    rect(d, (19, 27, 29, 35), c["skin"])
    rect(d, (20, 31, 28, 37), c["skin_shadow"])
    if character == "mara":
        rect(d, (17, 31, 20, 43), c["shirt"])
        rect(d, (28, 31, 31, 43), c["shirt"])
        rect(d, (21, 31, 27, 38), c["accent"])
        rect(d, (22, 37, 26, 42), c["accent"])
    elif character == "eli":
        rect(d, (20, 32, 28, 45), c["shirt"])
        rect(d, (18, 32, 20, 45), c["coat_shadow"])
        rect(d, (28, 32, 30, 45), c["coat_shadow"])
        rect(d, (23, 36, 25, 39), c["accent"])
    elif character == "niko":
        rect(d, (18, 31, 30, 46), c["coat"])
        line(d, [(22, 34), (24, 38), (26, 34)], c["shirt"], 1)
        rect(d, (20, 43, 21, 45), c["accent"])
        rect(d, (27, 43, 28, 45), c["accent"])
    else:
        rect(d, (19, 31, 29, 46), c["shirt"])
        rect(d, (16, 33, 19, 44), c["coat_shadow"])
        rect(d, (29, 33, 32, 44), c["coat_shadow"])
        line(d, [(27, 32), (31, 42)], c["accent"], 2)
    # head and face; retain the same silhouette while changing only acting marks.
    ellipse(d, (14, 10, 34, 33), c["outline"])
    ellipse(d, (15, 11, 33, 32), c["skin"])
    draw_hair(d, c, c["hairStyle"])
    if character == "eli":
        # glasses stay part of Eli's identity on every expression.
        d.rectangle((16, 18, 23, 23), outline=hexrgb(c["outline"]), width=1)
        d.rectangle((25, 18, 32, 23), outline=hexrgb(c["outline"]), width=1)
        line(d, [(23, 20), (25, 20)], c["outline"], 1)
    if character == "aunt-sol":
        rect(d, (31, 18, 33, 27), c["hair"])
        rect(d, (32, 26, 34, 28), c["hair_hi"])
    draw_face(d, c, emotion)
    # Tiny identity anchors, placed after the face so they read at thumbnail size.
    if character == "mara":
        rect(d, (12, 28, 14, 31), c["accent"])
    if character == "niko":
        rect(d, (33, 29, 35, 31), c["accent"])
    if character == "aunt-sol":
        rect(d, (29, 29, 31, 31), "#dbb33f")
    return im.resize((SIZE, SIZE), Image.Resampling.NEAREST)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    frames_root = ROOT / "frames"
    frames_root.mkdir(parents=True, exist_ok=True)
    records = []
    atlas = Image.new("RGBA", (SIZE * len(EMOTIONS), SIZE * len(CHARACTERS)), (0, 0, 0, 0))
    for row, (character, c) in enumerate(CHARACTERS.items()):
        char_dir = frames_root / character
        char_dir.mkdir(parents=True, exist_ok=True)
        for col, emotion in enumerate(EMOTIONS):
            path = char_dir / f"{character}-{emotion}-96x96.png"
            draw_character(character, emotion).save(path)
            atlas.alpha_composite(Image.open(path), (col * SIZE, row * SIZE))
            records.append({
                "id": f"{c['stableId']}/{emotion}",
                "character": c["stableId"],
                "displayName": c["displayName"],
                "emotion": emotion,
                "file": str(path.relative_to(ROOT)),
                "width": SIZE,
                "height": SIZE,
                "pivot": {"x": 48, "y": 92},
                "runtimeReady": False,
            })
    atlas_path = ROOT / "family-portrait-expressions-atlas-12x4-96x96.png"
    atlas.save(atlas_path)
    manifest = {
        "schemaVersion": 1,
        "batch": "family-portrait-expressions-v1",
        "direction": "PIXEL-ONLY",
        "runtimeReady": False,
        "frameSize": [SIZE, SIZE],
        "pivot": {"x": 48, "y": 92},
        "characters": [
            {
                "id": c["stableId"],
                "name": c["displayName"],
                "role": c["role"],
                "identity": c["identity"],
                "palette": {k: c[k] for k in ("skin", "hair", "coat", "accent", "outline")},
                "runtimeReady": False,
            }
            for c in CHARACTERS.values()
        ],
        "emotions": EMOTIONS,
        "atlas": {"file": atlas_path.name, "columns": EMOTIONS, "rows": [c["stableId"] for c in CHARACTERS.values()]},
        "sourceReferences": [
            {
                "file": "../named-family-batch-v1/named-family-portraits-concept-master.png",
                "purpose": "local original identity and palette study only; not sampled into output",
                "sha256": sha256(ROOT.parent / "named-family-batch-v1" / "named-family-portraits-concept-master.png"),
            },
            {
                "file": "../named-family-batch-v1/characters.json",
                "purpose": "stable character IDs and identity notes only",
                "sha256": sha256(ROOT.parent / "named-family-batch-v1" / "characters.json"),
            },
        ],
        "frames": records,
        "sha256": {"atlas": sha256(atlas_path), "frames": {}},
    }
    for record in records:
        path = ROOT / record["file"]
        manifest["sha256"]["frames"][record["file"]] = sha256(path)
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    # Rebuild a 2x contact sheet from the exact outputs, preserving nearest-neighbour pixels.
    contact = atlas.resize((atlas.width * 2, atlas.height * 2), Image.Resampling.NEAREST)
    contact.save(ROOT / "family-portrait-expressions-contact-2x.png")


if __name__ == "__main__":
    main()
