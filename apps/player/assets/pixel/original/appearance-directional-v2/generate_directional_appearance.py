#!/usr/bin/env python3
"""Build a small, original four-direction wardrobe extension.

The coordinate branches are intentionally written per facing.  This keeps
profile hair, shoulder seams, hems, and carried details readable without
mirroring a finished frame.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
SIZE = (24, 32)
PIVOT = [12, 28]
DIRECTIONS = ("south", "west", "east", "north")
LAYER_ORDER = ("skin", "bottom", "top", "shoes", "hair", "accessory")
TRANSPARENT = (0, 0, 0, 0)
INK = (34, 28, 40, 255)
SHADOW = (57, 43, 57, 220)
SKINS = {
    "honey": (208, 139, 91, 255),
    "deep_rose": (116, 67, 61, 255),
}
HAIR = {
    "indigo_bob": ((38, 32, 58, 255), (82, 71, 114, 255)),
    "russet_locs": ((82, 43, 33, 255), (153, 83, 47, 255)),
}
TOPS = {
    "sunset_jacket": ((188, 74, 76, 255), (235, 131, 87, 255)),
    "mint_overall": ((49, 143, 128, 255), (109, 203, 159, 255)),
}
BOTTOM = (55, 65, 101, 255)
BOTTOM_HIGHLIGHT = (86, 97, 139, 255)
SHOE = (49, 39, 52, 255)
ACCENT = (235, 179, 70, 255)


def canvas() -> Image.Image:
    return Image.new("RGBA", SIZE, TRANSPARENT)


def rect(draw: ImageDraw.ImageDraw, box, fill) -> None:
    draw.rectangle(box, fill=fill)


def poly(draw: ImageDraw.ImageDraw, points, fill) -> None:
    draw.polygon(points, fill=fill)


def skin(direction: str, tone) -> Image.Image:
    im, d = canvas(), None
    d = ImageDraw.Draw(im)
    if direction == "south":
        rect(d, (8, 3, 15, 10), tone); rect(d, (6, 6, 17, 8), tone)
        rect(d, (6, 11, 17, 18), tone); rect(d, (8, 18, 10, 25), tone); rect(d, (14, 18, 16, 25), tone)
        rect(d, (9, 7, 9, 7), INK); rect(d, (14, 7, 14, 7), INK); rect(d, (10, 9, 13, 9), (158, 77, 75, 255))
    elif direction == "west":
        rect(d, (7, 3, 14, 10), tone); rect(d, (6, 5, 14, 8), tone); poly(d, ((6, 6), (4, 7), (6, 8)), tone)
        rect(d, (7, 11, 17, 18), tone); rect(d, (9, 18, 11, 25), tone); rect(d, (14, 18, 16, 25), tone)
        rect(d, (7, 7, 7, 7), INK)
    elif direction == "east":
        rect(d, (10, 3, 17, 10), tone); rect(d, (10, 5, 18, 8), tone); poly(d, ((18, 6), (20, 7), (18, 8)), tone)
        rect(d, (7, 11, 17, 18), tone); rect(d, (8, 18, 10, 25), tone); rect(d, (13, 18, 15, 25), tone)
        rect(d, (16, 7, 16, 7), INK)
    else:
        rect(d, (8, 3, 15, 10), tone); rect(d, (6, 6, 17, 8), tone)
        rect(d, (6, 11, 17, 18), tone); rect(d, (8, 18, 10, 25), tone); rect(d, (14, 18, 16, 25), tone)
        rect(d, (10, 5, 13, 5), (227, 174, 136, 255))
    return im


def bottom(direction: str) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    if direction == "west":
        poly(d, ((8, 18), (17, 18), (16, 25), (13, 25), (12, 21), (10, 25), (8, 25)), BOTTOM)
        rect(d, (9, 19, 14, 20), BOTTOM_HIGHLIGHT)
    elif direction == "east":
        poly(d, ((7, 18), (16, 18), (16, 25), (13, 25), (12, 21), (9, 25), (8, 25)), BOTTOM)
        rect(d, (9, 19, 14, 20), BOTTOM_HIGHLIGHT)
    else:
        poly(d, ((7, 18), (17, 18), (16, 25), (13, 25), (12, 21), (11, 25), (8, 25)), BOTTOM)
        rect(d, (8, 19, 15, 20), BOTTOM_HIGHLIGHT if direction == "south" else SHADOW)
    return im


def shoes(direction: str) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    if direction == "west":
        rect(d, (8, 25, 11, 27), SHOE); rect(d, (14, 25, 16, 27), SHOE); rect(d, (6, 27, 11, 28), INK); rect(d, (14, 27, 17, 28), INK)
    elif direction == "east":
        rect(d, (8, 25, 10, 27), SHOE); rect(d, (13, 25, 16, 27), SHOE); rect(d, (7, 27, 10, 28), INK); rect(d, (13, 27, 18, 28), INK)
    else:
        rect(d, (7, 25, 10, 27), SHOE); rect(d, (14, 25, 17, 27), SHOE); rect(d, (6, 27, 10, 28), INK); rect(d, (14, 27, 18, 28), INK)
    return im


def top(direction: str, style: str) -> Image.Image:
    base, light = TOPS[style]
    im = canvas()
    d = ImageDraw.Draw(im)
    if direction == "south":
        poly(d, ((6, 12), (9, 10), (14, 10), (18, 12), (17, 19), (7, 19)), base); rect(d, (8, 12, 15, 13), light)
        rect(d, (7, 14, 7, 17), light); rect(d, (16, 14, 16, 17), light)
        if style == "mint_overall": rect(d, (10, 14, 13, 19), base)
    elif direction == "west":
        poly(d, ((7, 11), (11, 10), (16, 12), (17, 19), (8, 19)), base); rect(d, (8, 12, 13, 13), light); rect(d, (7, 14, 7, 17), light)
        rect(d, (14, 13, 16, 14), light if style == "sunset_jacket" else base)
    elif direction == "east":
        poly(d, ((8, 12), (13, 10), (17, 11), (17, 19), (7, 19)), base); rect(d, (11, 12, 16, 13), light); rect(d, (17, 14, 17, 17), light)
        rect(d, (8, 13, 10, 14), light if style == "sunset_jacket" else base)
    else:
        poly(d, ((6, 12), (9, 10), (14, 10), (18, 12), (17, 19), (7, 19)), base); rect(d, (8, 11, 15, 12), light)
        rect(d, (10, 13, 13, 13), SHADOW); rect(d, (7, 14, 7, 17), light); rect(d, (16, 14, 16, 17), light)
        if style == "mint_overall": rect(d, (10, 14, 13, 19), base)
    return im


def hair(direction: str, style: str) -> Image.Image:
    dark, light = HAIR[style]
    im = canvas()
    d = ImageDraw.Draw(im)
    if style == "indigo_bob":
        if direction == "south":
            rect(d, (7, 3, 16, 6), dark); rect(d, (7, 5, 8, 11), dark); rect(d, (15, 5, 16, 11), dark); rect(d, (8, 2, 10, 3), light); rect(d, (13, 2, 15, 3), light)
        elif direction == "west":
            rect(d, (6, 3, 14, 6), dark); rect(d, (6, 5, 8, 11), dark); rect(d, (13, 4, 14, 8), dark); rect(d, (7, 2, 9, 3), light)
        elif direction == "east":
            rect(d, (10, 3, 18, 6), dark); rect(d, (10, 4, 11, 9), dark); rect(d, (17, 5, 18, 11), dark); rect(d, (15, 2, 17, 3), light)
        else:
            rect(d, (7, 3, 16, 6), dark); rect(d, (7, 5, 8, 10), dark); rect(d, (15, 5, 16, 10), dark); rect(d, (9, 2, 11, 3), light); rect(d, (13, 2, 15, 3), light)
    else:
        if direction == "south":
            rect(d, (7, 3, 16, 6), dark); rect(d, (6, 5, 8, 10), dark); rect(d, (15, 5, 16, 9), dark); rect(d, (6, 9, 7, 15), light); rect(d, (8, 2, 9, 3), light)
        elif direction == "west":
            rect(d, (6, 3, 14, 6), dark); rect(d, (5, 5, 8, 10), dark); rect(d, (5, 9, 6, 15), light); rect(d, (7, 2, 8, 3), light)
        elif direction == "east":
            rect(d, (10, 3, 18, 6), dark); rect(d, (17, 5, 19, 10), dark); rect(d, (18, 9, 19, 15), light); rect(d, (16, 2, 17, 3), light)
        else:
            rect(d, (7, 3, 16, 6), dark); rect(d, (7, 5, 8, 10), dark); rect(d, (15, 5, 16, 10), dark); rect(d, (6, 9, 7, 14), light); rect(d, (16, 9, 17, 14), light); rect(d, (9, 2, 10, 3), light)
    return im


def accessory(direction: str) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    if direction == "west":
        rect(d, (5, 13, 6, 21), ACCENT); rect(d, (5, 19, 8, 22), ACCENT); rect(d, (6, 19, 7, 19), INK)
    elif direction == "east":
        rect(d, (18, 13, 19, 21), ACCENT); rect(d, (16, 19, 19, 22), ACCENT); rect(d, (17, 19, 18, 19), INK)
    else:
        rect(d, (5, 14, 6, 20), ACCENT); rect(d, (4, 19, 7, 22), ACCENT); rect(d, (5, 19, 6, 19), INK)
    return im


def save(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, format="PNG")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compose(direction: str, tone: str, hair_style: str, top_style: str) -> Image.Image:
    out = canvas()
    for part in (skin(direction, SKINS[tone]), bottom(direction), top(direction, top_style), shoes(direction), hair(direction, hair_style), accessory(direction)):
        out = Image.alpha_composite(out, part)
    return out


def build() -> None:
    layers = []
    for direction in DIRECTIONS:
        specs = {
            "skin": [(name, skin(direction, color)) for name, color in SKINS.items()],
            "hair": [(name, hair(direction, name)) for name in HAIR],
            "top": [(name, top(direction, name)) for name in TOPS],
            "bottom": [("indigo_trousers", bottom(direction))],
            "shoes": [("ink_sneakers", shoes(direction))],
            "accessory": [("ochre_satchel", accessory(direction))],
        }
        for kind, entries in specs.items():
            for name, image in entries:
                path = ROOT / "layers" / direction / kind / f"{name}-24x32.png"
                save(image, path)
                layers.append({"id": f"{direction}/{kind}/{name}", "path": str(path.relative_to(ROOT)), "kind": kind, "name": name, "direction": direction, "size": list(SIZE), "mode": "RGBA", "pivot": PIVOT, "sha256": digest(path), "runtimeReady": False})

    identities = (("honey_indigo", "honey", "indigo_bob", "sunset_jacket"), ("deep_russet", "deep_rose", "russet_locs", "mint_overall"))
    composites, atlas_frames = [], []
    for row, (identity, tone, hair_style, top_style) in enumerate(identities):
        for col, direction in enumerate(DIRECTIONS):
            image = compose(direction, tone, hair_style, top_style)
            path = ROOT / "composites" / identity / f"{direction}-24x32.png"
            save(image, path)
            composites.append({"id": f"{identity}/{direction}", "path": str(path.relative_to(ROOT)), "identity": identity, "direction": direction, "layers": [f"{direction}/skin/{tone}", f"{direction}/bottom/indigo_trousers", f"{direction}/top/{top_style}", f"{direction}/shoes/ink_sneakers", f"{direction}/hair/{hair_style}", f"{direction}/accessory/ochre_satchel"], "size": list(SIZE), "mode": "RGBA", "pivot": PIVOT, "sha256": digest(path), "runtimeReady": False})
            atlas_frames.append({"id": f"{identity}/{direction}", "x": col * 96, "y": row * 128, "width": 96, "height": 128, "source": str(path.relative_to(ROOT))})

    atlas = Image.new("RGBA", (len(DIRECTIONS) * 96, len(identities) * 128), (25, 25, 37, 255))
    for frame in atlas_frames:
        image = Image.open(ROOT / frame["source"])
        atlas.alpha_composite(image.resize((96, 128), Image.Resampling.NEAREST), (frame["x"], frame["y"]))
    save(atlas, ROOT / "appearance-directional-v2-atlas-4x.png")
    atlas_meta = {"size": list(atlas.size), "scale": 4, "filter": "nearest", "frames": atlas_frames, "runtimeReady": False}
    (ROOT / "atlas.json").write_text(json.dumps(atlas_meta, indent=2) + "\n", encoding="utf-8")
    manifest = {"schema": "liveit.pixel.appearance-directional.v2", "runtimeReady": False, "canvas": {"size": list(SIZE), "mode": "RGBA", "pivot": PIVOT}, "directions": list(DIRECTIONS), "layerOrder": list(LAYER_ORDER), "layers": layers, "composites": composites, "atlas": {"path": "appearance-directional-v2-atlas-4x.png", "metadata": "atlas.json", "sha256": digest(ROOT / "appearance-directional-v2-atlas-4x.png"), "runtimeReady": False}, "validation": {"directionallyAuthored": True, "noMirrorFlip": True, "source": "generate_directional_appearance.py", "thirdPartyAssets": False, "archiveAssets": False, "aiGeneratedSources": False}}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    provenance = {"batch": "appearance-directional-v2", "created": "2026-10-20", "authoring": "deterministic Pillow drawing primitives in generate_directional_appearance.py", "visualReference": "Existing original LIVEIT appearance-kit layout and palette vocabulary were inspected for compatibility only; no source pixels were copied.", "sourceImages": [], "sourceArchives": [], "thirdPartyAssets": [], "aiGeneration": False, "license": "Original work authored for LIVEIT; no external asset license is inherited.", "directionMethod": "Each cardinal direction has independent hair, torso, and silhouette coordinate branches; west/east are not mirror-flipped.", "runtimeReady": False}
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
