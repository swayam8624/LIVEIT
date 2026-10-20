#!/usr/bin/env python3
"""Build LIVEIT's original 24x32 directional appearance starter.

Every facing is drawn from its own pixel primitives.  No image is mirrored or
sampled from the existing south-facing appearance study.
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

SKIN = {
    "porcelain": (245, 202, 169, 255),
    "copper": (191, 117, 73, 255),
    "umber": (119, 70, 47, 255),
    "deep": (77, 45, 39, 255),
}
HAIR = {
    "coiled": ((38, 25, 29, 255), (76, 45, 41, 255)),
    "silver_coiled": ((167, 182, 184, 255), (92, 111, 114, 255)),
    "cropped": ((30, 29, 43, 255), (62, 57, 74, 255)),
    "braided": ((91, 51, 34, 255), (142, 80, 42, 255)),
}

TEAL = (37, 133, 128, 255)
TEAL_LIGHT = (73, 180, 164, 255)
OCHRE = (206, 143, 48, 255)
OCHRE_DARK = (126, 79, 37, 255)
INK = (36, 29, 42, 255)
SHADOW = (61, 45, 57, 220)
TRANSPARENT = (0, 0, 0, 0)


def canvas() -> Image.Image:
    return Image.new("RGBA", SIZE, TRANSPARENT)


def rect(d: ImageDraw.ImageDraw, box, fill):
    d.rectangle(box, fill=fill)


def poly(d: ImageDraw.ImageDraw, points, fill):
    d.polygon(points, fill=fill)


def skin_layer(direction: str, tone: tuple[int, int, int, int]) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    # Head and exposed lower body are deliberately distinct by facing.
    if direction == "south":
        rect(d, (8, 3, 15, 10), tone)
        rect(d, (7, 5, 16, 8), tone)
        rect(d, (6, 11, 17, 18), tone)
        rect(d, (8, 18, 10, 25), tone)
        rect(d, (14, 18, 16, 25), tone)
        rect(d, (7, 13, 8, 16), tone)
        rect(d, (16, 13, 17, 16), tone)
        rect(d, (9, 7, 9, 7), INK)
        rect(d, (14, 7, 14, 7), INK)
        rect(d, (10, 9, 13, 9), (160, 78, 75, 255))
    elif direction == "west":
        rect(d, (7, 3, 14, 10), tone)
        rect(d, (6, 5, 14, 8), tone)
        poly(d, [(6, 6), (4, 7), (6, 8)], tone)
        rect(d, (7, 11, 17, 18), tone)
        rect(d, (9, 18, 11, 25), tone)
        rect(d, (14, 18, 16, 25), tone)
        rect(d, (6, 13, 7, 16), tone)
        rect(d, (16, 13, 17, 16), tone)
        rect(d, (7, 7, 7, 7), INK)
    elif direction == "east":
        rect(d, (10, 3, 17, 10), tone)
        rect(d, (10, 5, 18, 8), tone)
        poly(d, [(18, 6), (20, 7), (18, 8)], tone)
        rect(d, (7, 11, 17, 18), tone)
        rect(d, (8, 18, 10, 25), tone)
        rect(d, (13, 18, 15, 25), tone)
        rect(d, (7, 13, 8, 16), tone)
        rect(d, (17, 13, 18, 16), tone)
        rect(d, (16, 7, 16, 7), INK)
    else:  # north
        rect(d, (8, 3, 15, 10), tone)
        rect(d, (7, 5, 16, 8), tone)
        rect(d, (6, 11, 17, 18), tone)
        rect(d, (8, 18, 10, 25), tone)
        rect(d, (14, 18, 16, 25), tone)
        rect(d, (7, 13, 8, 16), tone)
        rect(d, (16, 13, 17, 16), tone)
        rect(d, (10, 5, 13, 5), (235, 186, 151, 255))
    return im


def top_layer(direction: str) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    if direction == "south":
        poly(d, [(6, 12), (9, 10), (14, 10), (18, 12), (17, 19), (7, 19)], TEAL)
        rect(d, (8, 12, 15, 13), TEAL_LIGHT)
        rect(d, (7, 14, 7, 17), TEAL_LIGHT)
        rect(d, (16, 14, 16, 17), TEAL_LIGHT)
    elif direction == "west":
        poly(d, [(7, 11), (11, 10), (16, 12), (17, 19), (8, 19)], TEAL)
        rect(d, (8, 12, 13, 13), TEAL_LIGHT)
        rect(d, (7, 14, 7, 17), TEAL_LIGHT)
    elif direction == "east":
        poly(d, [(8, 12), (13, 10), (17, 11), (17, 19), (7, 19)], TEAL)
        rect(d, (11, 12, 16, 13), TEAL_LIGHT)
        rect(d, (17, 14, 17, 17), TEAL_LIGHT)
    else:
        poly(d, [(6, 12), (9, 10), (14, 10), (18, 12), (17, 19), (7, 19)], TEAL)
        rect(d, (8, 11, 15, 12), TEAL_LIGHT)
        rect(d, (10, 13, 13, 13), (28, 105, 103, 255))
        rect(d, (7, 14, 7, 17), TEAL_LIGHT)
        rect(d, (16, 14, 16, 17), TEAL_LIGHT)
    return im


def bottom_layer(direction: str) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    if direction == "south":
        poly(d, [(7, 18), (17, 18), (16, 25), (13, 25), (12, 21), (11, 25), (8, 25)], OCHRE)
        rect(d, (8, 19, 15, 20), (231, 171, 66, 255))
    elif direction == "north":
        poly(d, [(7, 18), (17, 18), (16, 25), (13, 25), (12, 21), (11, 25), (8, 25)], OCHRE)
        rect(d, (8, 19, 15, 19), OCHRE_DARK)
        rect(d, (9, 20, 15, 20), (231, 171, 66, 255))
        rect(d, (13, 21, 15, 23), (176, 111, 39, 255))
    elif direction == "west":
        poly(d, [(8, 18), (17, 18), (16, 25), (13, 25), (12, 21), (10, 25), (8, 25)], OCHRE)
        rect(d, (9, 19, 15, 20), (231, 171, 66, 255))
    else:
        poly(d, [(7, 18), (16, 18), (16, 25), (13, 25), (12, 21), (9, 25), (8, 25)], OCHRE)
        rect(d, (8, 19, 14, 20), (231, 171, 66, 255))
    return im


def shoes_layer(direction: str) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    if direction == "south":
        rect(d, (7, 25, 10, 27), OCHRE_DARK)
        rect(d, (14, 25, 17, 27), OCHRE_DARK)
        rect(d, (6, 27, 10, 28), INK)
        rect(d, (14, 27, 18, 28), INK)
    elif direction == "north":
        rect(d, (8, 25, 10, 28), OCHRE_DARK)
        rect(d, (14, 25, 16, 28), OCHRE_DARK)
        rect(d, (7, 28, 10, 28), INK)
        rect(d, (14, 28, 17, 28), INK)
    elif direction == "west":
        rect(d, (8, 25, 11, 27), OCHRE_DARK)
        rect(d, (14, 25, 16, 27), OCHRE_DARK)
        rect(d, (6, 27, 11, 28), INK)
        rect(d, (14, 27, 17, 28), INK)
    else:
        rect(d, (8, 25, 10, 27), OCHRE_DARK)
        rect(d, (13, 25, 16, 27), OCHRE_DARK)
        rect(d, (7, 27, 10, 28), INK)
        rect(d, (13, 27, 18, 28), INK)
    return im


def hair_layer(direction: str, style: str) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    dark, highlight = HAIR[style]
    if direction == "south":
        rect(d, (7, 3, 16, 6), dark)
        rect(d, (8, 2, 11, 3), dark)
        rect(d, (13, 2, 15, 3), dark)
        rect(d, (7, 5, 8, 10), dark)
        rect(d, (15, 5, 16, 9), dark)
        if style in ("coiled", "silver_coiled"):
            rect(d, (6, 3, 7, 5), highlight)
            rect(d, (16, 3, 17, 5), highlight)
            rect(d, (8, 2, 9, 2), highlight)
            rect(d, (14, 2, 15, 2), highlight)
        elif style == "cropped":
            rect(d, (9, 3, 13, 3), highlight)
        else:
            rect(d, (6, 8, 7, 12), dark)
            rect(d, (5, 10, 6, 14), highlight)
    elif direction == "west":
        rect(d, (6, 3, 14, 6), dark)
        rect(d, (6, 5, 8, 10), dark)
        rect(d, (13, 4, 14, 8), dark)
        if style in ("coiled", "silver_coiled"):
            rect(d, (5, 3, 6, 5), highlight)
            rect(d, (7, 2, 8, 2), highlight)
            rect(d, (12, 2, 13, 2), highlight)
        elif style == "cropped":
            rect(d, (8, 3, 11, 3), highlight)
        else:
            rect(d, (5, 8, 6, 13), dark)
            rect(d, (4, 11, 5, 15), highlight)
    elif direction == "east":
        rect(d, (10, 3, 18, 6), dark)
        rect(d, (10, 4, 11, 8), dark)
        rect(d, (17, 5, 18, 10), dark)
        if style in ("coiled", "silver_coiled"):
            rect(d, (18, 3, 19, 5), highlight)
            rect(d, (11, 2, 12, 2), highlight)
            rect(d, (16, 2, 17, 2), highlight)
        elif style == "cropped":
            rect(d, (13, 3, 16, 3), highlight)
        else:
            rect(d, (18, 8, 19, 13), dark)
            rect(d, (19, 11, 20, 15), highlight)
    else:
        rect(d, (7, 3, 16, 6), dark)
        rect(d, (7, 5, 8, 10), dark)
        rect(d, (15, 5, 16, 10), dark)
        rect(d, (8, 2, 10, 3), dark)
        rect(d, (13, 2, 15, 3), dark)
        if style in ("coiled", "silver_coiled"):
            rect(d, (6, 3, 7, 5), highlight)
            rect(d, (16, 3, 17, 5), highlight)
            rect(d, (9, 2, 9, 2), highlight)
            rect(d, (14, 2, 14, 2), highlight)
        elif style == "cropped":
            rect(d, (10, 3, 13, 3), highlight)
        else:
            rect(d, (6, 8, 7, 13), dark)
            rect(d, (16, 8, 17, 13), highlight)
    return im


def accessory_layer(direction: str, accessory: str) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    if accessory == "scarf":
        if direction == "south":
            rect(d, (8, 10, 15, 11), OCHRE_DARK); rect(d, (14, 11, 16, 15), OCHRE)
        elif direction == "west":
            rect(d, (8, 10, 14, 11), OCHRE_DARK); rect(d, (7, 11, 9, 15), OCHRE)
        elif direction == "east":
            rect(d, (10, 10, 16, 11), OCHRE_DARK); rect(d, (15, 11, 18, 15), OCHRE)
        else:
            rect(d, (8, 10, 15, 11), OCHRE_DARK); rect(d, (9, 11, 11, 15), OCHRE)
    elif accessory == "satchel":
        if direction == "south":
            rect(d, (5, 14, 7, 20), OCHRE_DARK); rect(d, (4, 19, 7, 22), OCHRE)
            rect(d, (5, 19, 6, 19), TEAL_LIGHT)
        elif direction == "west":
            rect(d, (5, 13, 7, 20), OCHRE_DARK); rect(d, (4, 19, 7, 22), OCHRE)
            rect(d, (5, 19, 6, 19), TEAL_LIGHT)
        elif direction == "east":
            rect(d, (17, 13, 19, 20), OCHRE_DARK); rect(d, (17, 19, 20, 22), OCHRE)
            rect(d, (18, 19, 19, 19), TEAL_LIGHT)
        else:
            rect(d, (16, 14, 18, 21), OCHRE_DARK); rect(d, (16, 20, 19, 22), OCHRE)
            rect(d, (17, 20, 18, 20), TEAL_LIGHT)
    else:  # cane
        if direction == "south":
            rect(d, (19, 14, 20, 28), OCHRE_DARK); rect(d, (18, 14, 20, 15), OCHRE)
        elif direction == "north":
            rect(d, (18, 14, 19, 28), OCHRE_DARK); rect(d, (17, 14, 19, 15), OCHRE)
            rect(d, (18, 18, 19, 18), (236, 173, 67, 255))
        elif direction == "west":
            rect(d, (18, 14, 19, 28), OCHRE_DARK); rect(d, (17, 14, 19, 15), OCHRE)
        else:
            rect(d, (20, 14, 21, 28), OCHRE_DARK); rect(d, (19, 14, 21, 15), OCHRE)
    return im


def save(im: Image.Image, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict:
    layer_records = []
    for direction in DIRECTIONS:
        layer_specs = {
            "skin": [(name, skin_layer(direction, color)) for name, color in SKIN.items()],
            "hair": [(name, hair_layer(direction, name)) for name in HAIR],
            "top": [("teal", top_layer(direction))],
            "bottom": [("ochre", bottom_layer(direction))],
            "shoes": [("ochre_boots", shoes_layer(direction))],
            "accessory": [(name, accessory_layer(direction, name)) for name in ("scarf", "satchel", "cane")],
        }
        for kind, entries in layer_specs.items():
            for name, im in entries:
                path = ROOT / "layers" / direction / kind / f"{name}-24x32.png"
                save(im, path)
                layer_records.append({
                    "id": f"{direction}/{kind}/{name}",
                    "path": str(path.relative_to(ROOT)),
                    "kind": kind,
                    "name": name,
                    "direction": direction,
                    "size": list(im.size),
                    "mode": im.mode,
                    "pivot": PIVOT,
                    "sha256": sha(path),
                    "runtimeReady": False,
                })

    identities = (
        ("porcelain_coiled", "porcelain", "coiled", "scarf"),
        ("copper_silver", "copper", "silver_coiled", "satchel"),
        ("umber_cropped", "umber", "cropped", "cane"),
        ("deep_braided", "deep", "braided", "scarf"),
    )
    composite_records = []
    previews = []
    for identity, tone, hair, accessory in identities:
        for direction in DIRECTIONS:
            parts = [
                skin_layer(direction, SKIN[tone]),
                bottom_layer(direction),
                top_layer(direction),
                shoes_layer(direction),
                hair_layer(direction, hair),
                accessory_layer(direction, accessory),
            ]
            out = canvas()
            for part in parts:
                out = Image.alpha_composite(out, part)
            path = ROOT / "composites" / identity / f"{direction}-24x32.png"
            save(out, path)
            composite_records.append({
                "id": f"{identity}/{direction}",
                "path": str(path.relative_to(ROOT)),
                "identity": identity,
                "direction": direction,
                "layers": [f"{direction}/skin/{tone}", f"{direction}/bottom/ochre", f"{direction}/top/teal", f"{direction}/shoes/ochre_boots", f"{direction}/hair/{hair}", f"{direction}/accessory/{accessory}"],
                "size": list(out.size),
                "mode": out.mode,
                "pivot": PIVOT,
                "sha256": sha(path),
                "runtimeReady": False,
            })
            previews.append((identity, direction, out))

    preview = Image.new("RGBA", (len(DIRECTIONS) * 24 * 4, len(identities) * 32 * 4), (24, 24, 34, 255))
    for row, identity in enumerate(identities):
        ident = identity[0]
        for col, direction in enumerate(DIRECTIONS):
            out = next(im for name, facing, im in previews if name == ident and facing == direction)
            preview.alpha_composite(out.resize((96, 128), Image.Resampling.NEAREST), (col * 96, row * 128))
    save(preview, ROOT / "appearance-directional-preview-4x.png")

    manifest = {
        "schema": "liveit.pixel.appearance-directional.v1",
        "runtimeReady": False,
        "canvas": {"size": list(SIZE), "mode": "RGBA", "pivot": PIVOT},
        "directions": list(DIRECTIONS),
        "layerOrder": list(LAYER_ORDER),
        "layers": layer_records,
        "composites": composite_records,
        "validation": {
            "directionallyAuthored": True,
            "source": "generate_directional_appearance.py",
            "thirdPartyAssets": False,
            "archiveAssets": False,
            "aiGeneratedSources": False,
        },
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    provenance = {
        "source": "Deterministic Pillow pixel primitives in generate_directional_appearance.py",
        "license": "Original work authored for LIVEIT; no third-party or archive pixels used",
        "referenceOnly": "appearance-kit-v1 was inspected for frame and pivot conventions only; no pixels were copied or modified",
        "generatedAt": "reproducible local build; see file hashes in manifest.json",
        "directionMethod": "south, west, east, and north each have independent coordinate branches; no flip or transform is used",
        "occlusionOrder": list(LAYER_ORDER),
        "runtimeReady": False,
    }
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    result = build()
    print(f"built {len(result['layers'])} layers and {len(result['composites'])} composites")
