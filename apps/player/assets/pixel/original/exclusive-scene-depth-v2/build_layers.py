#!/usr/bin/env python3
"""Build original, rights-safe 2D pixel scene layers and verification metadata.

The artwork is authored with Pillow primitives at a 160x128 design grid and
exported with nearest-neighbour scaling.  This intentionally keeps the source
recipe in the package and leaves every compositing layer independently usable.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
GRID = (160, 128)
OUT = (320, 256)
SOURCE = (640, 512)

PALETTE = {
    "ink": (31, 27, 48, 255),
    "ink2": (53, 42, 65, 255),
    "cream": (255, 231, 174, 255),
    "gold": (244, 185, 78, 255),
    "coral": (220, 95, 100, 255),
    "mint": (102, 199, 164, 255),
    "sky": (108, 163, 209, 255),
    "lavender": (157, 128, 197, 255),
    "paper": (255, 246, 212, 255),
    "wood": (126, 72, 55, 255),
}


def rgba(color):
    if isinstance(color, str):
        color = PALETTE[color]
    return color if len(color) == 4 else (*color, 255)


def scene_dir(slug: str) -> Path:
    path = ROOT / slug
    path.mkdir(parents=True, exist_ok=True)
    (path / "items").mkdir(exist_ok=True)
    return path


def make_layer() -> Image.Image:
    return Image.new("RGBA", GRID, (0, 0, 0, 0))


def rect(draw: ImageDraw.ImageDraw, box, fill, outline=None, width=1):
    draw.rectangle(box, fill=rgba(fill), outline=rgba(outline) if outline else None, width=width)


def text(draw: ImageDraw.ImageDraw, xy, value, fill="cream"):
    # Pillow's default bitmap font is deliberately used so the source is deterministic.
    draw.text(xy, value, fill=rgba(PALETTE[fill] if isinstance(fill, str) and fill in PALETTE else fill))


def save_grid(image: Image.Image, path: Path, mode: str = "RGBA"):
    image = image.convert(mode)
    image.resize(OUT, Image.Resampling.NEAREST).save(path)


def save_source(image: Image.Image, path: Path):
    image.convert("RGB").resize(SOURCE, Image.Resampling.NEAREST).save(path)


def add_stars(draw, color, count=24, y_max=80):
    for i in range(count):
        x = (i * 37 + 11) % 158
        y = (i * 19 + 7) % y_max
        rect(draw, (x, y, x + (i % 2), y + (i % 2)), color)


def graduation_layers():
    slug = "graduation"
    path = scene_dir(slug)
    bg = make_layer(); d = ImageDraw.Draw(bg)
    rect(d, (0, 0, 159, 127), (42, 56, 101, 255))
    rect(d, (0, 0, 159, 82), (65, 92, 150, 255))
    add_stars(d, "cream", 34, 70)
    # sunset stripe and school roof silhouette
    rect(d, (0, 71, 159, 83), (227, 142, 98, 255))
    rect(d, (0, 84, 159, 127), (38, 39, 63, 255))
    rect(d, (12, 72, 148, 89), (52, 47, 72, 255))
    rect(d, (20, 65, 140, 73), (43, 39, 66, 255))
    rect(d, (30, 89, 48, 127), (60, 53, 79, 255)); rect(d, (112, 89, 130, 127), (60, 53, 79, 255))
    rect(d, (75, 54, 84, 69), (45, 39, 67, 255)); rect(d, (67, 57, 92, 62), "gold")
    text(d, (58, 91), "★  OPEN  SKY  ★", "cream")
    mid = make_layer(); d = ImageDraw.Draw(mid)
    # stage riser, benches, banners, diploma table
    rect(d, (18, 79, 141, 91), (91, 53, 59, 255), "ink")
    rect(d, (23, 91, 136, 97), (126, 72, 55, 255), "ink")
    rect(d, (35, 62, 44, 80), (220, 95, 100, 255), "ink")
    rect(d, (116, 62, 125, 80), (102, 199, 164, 255), "ink")
    rect(d, (36, 62, 44, 65), "gold"); rect(d, (117, 62, 125, 65), "gold")
    rect(d, (10, 98, 149, 103), (47, 40, 61, 255))
    for x in (18, 43, 68, 93, 118, 143):
        rect(d, (x, 103, x + 12, 106), (80, 62, 77, 255))
    rect(d, (128, 86, 141, 96), "gold", "ink")
    text(d, (129, 87), "D", "ink")
    fg = make_layer(); d = ImageDraw.Draw(fg)
    # cinematic curtains and corner foliage frame; central actor lane stays open
    rect(d, (0, 0, 14, 127), (70, 34, 59, 245), "ink")
    rect(d, (146, 0, 159, 127), (70, 34, 59, 245), "ink")
    for x in (3, 8, 151, 156):
        rect(d, (x, 0, x + 2, 127), (108, 46, 68, 220))
    for x, y in ((16, 109), (19, 113), (140, 110), (136, 115)):
        rect(d, (x, y, x + 9, y + 7), "mint", "ink")
        rect(d, (x + 4, y - 4, x + 6, y + 1), "wood")
    rect(d, (14, 0, 146, 4), "gold", "ink")
    # items: diploma, cap, bouquet, medal
    items = {
        "diploma-scroll": ((255, 246, 212, 255), (220, 95, 100, 255)),
        "graduation-cap": ((36, 31, 57, 255), (244, 185, 78, 255)),
        "wildflower-bouquet": ((102, 199, 164, 255), (220, 95, 100, 255)),
        "class-medal": ((244, 185, 78, 255), (220, 95, 100, 255)),
    }
    for name, (primary, accent) in items.items():
        im = make_layer(); q = ImageDraw.Draw(im)
        if name == "diploma-scroll":
            rect(q, (20, 31, 130, 93), primary, "ink"); rect(q, (29, 42, 119, 46), accent); rect(q, (29, 55, 97, 58), "lavender"); rect(q, (29, 66, 109, 69), "sky"); rect(q, (104, 74, 120, 86), "gold", "ink")
        elif name == "graduation-cap":
            rect(q, (27, 60, 133, 71), primary, "ink"); rect(q, (50, 43, 110, 61), primary, "ink"); rect(q, (78, 68, 84, 93), accent, "ink"); rect(q, (83, 88, 102, 93), accent, "ink")
        elif name == "wildflower-bouquet":
            rect(q, (76, 60, 84, 108), "mint", "ink"); rect(q, (53, 47, 107, 78), primary, "ink"); rect(q, (41, 52, 63, 73), accent, "ink"); rect(q, (94, 42, 118, 65), "lavender", "ink")
        else:
            rect(q, (72, 45, 89, 73), accent, "ink"); rect(q, (59, 74, 102, 82), primary, "ink"); rect(q, (75, 82, 84, 103), accent, "ink")
        save_grid(im, path / "items" / f"{name}.png")
    return slug, bg, mid, fg, (42, 20, 118, 107)


def parenthood_layers():
    slug = "new-parenthood"
    path = scene_dir(slug)
    bg = make_layer(); d = ImageDraw.Draw(bg)
    rect(d, (0, 0, 159, 127), (61, 92, 115, 255)); rect(d, (0, 78, 159, 127), (194, 149, 117, 255))
    rect(d, (0, 73, 159, 80), (238, 194, 148, 255)); rect(d, (11, 17, 59, 68), (255, 246, 212, 255), "ink")
    rect(d, (16, 22, 54, 62), (108, 163, 209, 255)); rect(d, (28, 22, 31, 62), "cream"); rect(d, (16, 39, 54, 42), "cream")
    rect(d, (96, 18, 143, 61), (255, 231, 174, 255), "ink"); rect(d, (101, 23, 138, 55), (157, 128, 197, 255))
    rect(d, (18, 66, 145, 73), (126, 72, 55, 255), "ink"); text(d, (67, 42), "HOME", "ink")
    mid = make_layer(); d = ImageDraw.Draw(mid)
    rect(d, (47, 69, 112, 105), (244, 222, 187, 255), "ink")
    rect(d, (51, 64, 108, 74), (255, 246, 212, 255), "ink")
    rect(d, (53, 76, 106, 98), (102, 199, 164, 255), "ink")
    rect(d, (57, 80, 102, 95), (84, 139, 120, 255))
    rect(d, (8, 93, 38, 119), (126, 72, 55, 255), "ink"); rect(d, (11, 88, 35, 97), (220, 95, 100, 255), "ink")
    rect(d, (120, 82, 151, 121), (126, 72, 55, 255), "ink"); rect(d, (125, 75, 146, 86), (244, 185, 78, 255), "ink")
    fg = make_layer(); d = ImageDraw.Draw(fg)
    rect(d, (0, 113, 159, 127), (72, 52, 67, 245), "ink")
    for x in (5, 149):
        rect(d, (x, 31, x + 8, 117), (220, 95, 100, 180), "ink")
        rect(d, (x - 3, 25, x + 11, 34), (244, 185, 78, 210), "ink")
    rect(d, (16, 0, 144, 4), "mint", "ink")
    items = {
        "swaddled-baby": "baby", "family-photo": "photo", "keepsake-rattle": "rattle", "welcome-home-card": "card"
    }
    for name, kind in items.items():
        im = make_layer(); q = ImageDraw.Draw(im)
        if kind == "baby":
            rect(q, (42, 46, 118, 100), (255, 246, 212, 255), "ink"); rect(q, (52, 56, 108, 91), (157, 128, 197, 255), "ink"); rect(q, (67, 48, 91, 67), (244, 185, 78, 255), "ink"); rect(q, (72, 53, 76, 57), "ink"); rect(q, (84, 53, 88, 57), "ink")
        elif kind == "photo":
            rect(q, (35, 29, 125, 105), "wood", "ink"); rect(q, (43, 37, 117, 95), (108, 163, 209, 255), "ink"); rect(q, (56, 54, 67, 76), "coral", "ink"); rect(q, (74, 49, 85, 76), "mint", "ink"); rect(q, (91, 55, 103, 76), "lavender", "ink")
        elif kind == "rattle":
            rect(q, (72, 58, 88, 75), "gold", "ink"); rect(q, (77, 72, 83, 104), "wood", "ink"); rect(q, (67, 53, 93, 67), "gold", "ink")
        else:
            rect(q, (26, 34, 134, 99), "paper", "ink"); rect(q, (38, 48, 122, 53), "coral"); rect(q, (38, 61, 109, 64), "sky"); rect(q, (38, 74, 97, 77), "mint"); rect(q, (100, 79, 123, 91), "gold", "ink")
        save_grid(im, path / "items" / f"{name}.png")
    return slug, bg, mid, fg, (38, 24, 123, 109)


def legacy_layers():
    slug = "elder-legacy"
    path = scene_dir(slug)
    bg = make_layer(); d = ImageDraw.Draw(bg)
    rect(d, (0, 0, 159, 127), (39, 55, 79, 255)); rect(d, (0, 70, 159, 127), (64, 51, 63, 255))
    add_stars(d, "gold", 30, 69); rect(d, (16, 20, 144, 27), "wood", "ink"); rect(d, (19, 28, 141, 67), (90, 77, 102, 255), "ink")
    for x in range(25, 138, 18):
        rect(d, (x, 33, x + 12, 58), (157, 128, 197, 255), "ink"); rect(d, (x + 3, 38, x + 9, 47), "gold")
    rect(d, (0, 65, 159, 71), (244, 185, 78, 255)); text(d, (54, 76), "THE  LONG  VIEW", "cream")
    mid = make_layer(); d = ImageDraw.Draw(mid)
    rect(d, (22, 83, 138, 103), (126, 72, 55, 255), "ink"); rect(d, (28, 78, 132, 86), (244, 185, 78, 255), "ink")
    for x in (34, 59, 84, 109):
        rect(d, (x, 85, x + 15, 101), (220, 95, 100, 255), "ink")
        rect(d, (x + 4, 88, x + 11, 95), (255, 231, 174, 255))
    rect(d, (65, 102, 96, 121), (90, 77, 102, 255), "ink"); rect(d, (72, 106, 89, 116), "mint", "ink")
    fg = make_layer(); d = ImageDraw.Draw(fg)
    rect(d, (0, 0, 12, 127), (27, 29, 53, 245), "ink"); rect(d, (148, 0, 159, 127), (27, 29, 53, 245), "ink")
    for x in (3, 7, 151, 155): rect(d, (x, 0, x + 2, 127), (70, 62, 83, 220))
    rect(d, (12, 0, 148, 4), "gold", "ink"); rect(d, (13, 112, 147, 127), (42, 37, 58, 235), "ink")
    items = {"memory-album": "album", "garden-seed-packet": "seed", "old-key": "key", "legacy-letter": "letter"}
    for name, kind in items.items():
        im = make_layer(); q = ImageDraw.Draw(im)
        if kind == "album":
            rect(q, (31, 24, 129, 106), (66, 45, 74, 255), "ink"); rect(q, (41, 34, 119, 96), (108, 163, 209, 255), "ink"); rect(q, (51, 48, 69, 81), "coral", "ink"); rect(q, (72, 43, 90, 81), "mint", "ink"); rect(q, (95, 51, 111, 81), "lavender", "ink"); rect(q, (48, 87, 111, 91), "gold")
        elif kind == "seed":
            rect(q, (48, 29, 112, 103), "mint", "ink"); rect(q, (57, 39, 103, 54), "gold", "ink"); text(q, (61, 61), "GROW", "ink"); rect(q, (66, 79, 94, 92), "wood", "ink")
        elif kind == "key":
            rect(q, (46, 65, 105, 74), "gold", "ink"); rect(q, (92, 50, 112, 88), "gold", "ink"); rect(q, (104, 52, 118, 61), "gold", "ink"); rect(q, (53, 62, 61, 77), "gold", "ink")
        else:
            rect(q, (29, 32, 131, 101), "paper", "ink"); rect(q, (42, 48, 112, 52), "coral"); rect(q, (42, 62, 121, 65), "sky"); rect(q, (42, 76, 103, 79), "lavender"); rect(q, (103, 84, 121, 92), "gold", "ink")
        save_grid(im, path / "items" / f"{name}.png")
    return slug, bg, mid, fg, (43, 19, 117, 108)


def guide_image(box):
    im = make_layer(); d = ImageDraw.Draw(im)
    # guide overlay is intentionally transparent outside the placement rectangles.
    x0, y0, x1, y1 = box
    for x in range(x0, x1 + 1, 5):
        rect(d, (x, y0, min(x + 2, x1), y0 + 1), (102, 199, 164, 210))
        rect(d, (x, y1, min(x + 2, x1), y1 + 1), (102, 199, 164, 210))
    for y in range(y0, y1 + 1, 5):
        rect(d, (x0, y, x0 + 1, min(y + 2, y1)), (102, 199, 164, 210))
        rect(d, (x1, y, x1 + 1, min(y + 2, y1)), (102, 199, 164, 210))
    text(d, (x0 + 2, y0 + 3), "ACTOR SAFE", "mint")
    return im


def compose(slug: str, layers: Iterable[Image.Image]):
    canvas = Image.new("RGBA", GRID, (0, 0, 0, 0))
    for layer in layers:
        canvas.alpha_composite(layer)
    save_grid(canvas, ROOT / f"{slug}-preview-derived.png")


def main():
    specs = [graduation_layers(), parenthood_layers(), legacy_layers()]
    records = []
    for slug, bg, mid, fg, box in specs:
        path = scene_dir(slug)
        save_source(bg, path / f"{slug}-background-source.png")
        save_source(mid, path / f"{slug}-midground-source.png")
        save_source(fg, path / f"{slug}-foreground-source.png")
        save_grid(bg, path / f"{slug}-background-plate.png", "RGB")
        save_grid(mid, path / f"{slug}-midground-set-dressing.png")
        save_grid(fg, path / f"{slug}-foreground-frame.png")
        guide = guide_image(box)
        save_grid(guide, path / f"{slug}-actor-safe-guide.png")
        compose(slug, [bg, mid, fg])
        records.append({
            "id": slug,
            "layers": [
                f"{slug}/{slug}-background-plate.png",
                f"{slug}/{slug}-midground-set-dressing.png",
                f"{slug}/{slug}-foreground-frame.png",
                f"{slug}/{slug}-actor-safe-guide.png",
            ],
            "items": sorted(str(p.relative_to(ROOT)) for p in (path / "items").glob("*.png")),
            "actorSafeRectGrid": list(box),
            "preview": f"{slug}-preview-derived.png",
            "runtimeReady": False,
        })
    all_paths = sorted(p for p in ROOT.rglob("*.png") if p.name != "manifest.json")
    files = []
    for p in all_paths:
        with p.open("rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        image = Image.open(p)
        files.append({
            "path": str(p.relative_to(ROOT)),
            "sha256": digest,
            "size": list(image.size),
            "mode": image.mode,
            "role": "derived-preview" if "preview-derived" in p.name else ("source-original" if "-source" in p.name else "layer-or-item"),
        })
    (ROOT / "manifest.json").write_text(json.dumps({
        "schema": "liveit.pixel.exclusive-scene-depth.v2",
        "generatedBy": "build_layers.py",
        "sourceGrid": list(GRID),
        "exportSize": list(OUT),
        "sourceSize": list(SOURCE),
        "scenes": records,
        "files": files,
        "runtimeReady": False,
    }, indent=2) + "\n", encoding="utf-8")
    (ROOT / "provenance.json").write_text(json.dumps({
        "license": "Original procedural artwork authored for LIVEIT; no third-party imagery or archive assets used.",
        "authoring": "Pillow primitives on a deterministic 160x128 pixel grid, nearest-neighbour exports.",
        "sourceOfTruth": "build_layers.py and prompts.md",
        "derivation": "Source plates are 640x512 RGB snapshots; runtime candidates are 320x256 layers. Derived previews composite layers only and are not runtime candidates.",
        "runtimeReady": False,
        "limitations": ["Actor sprites are not included; guides reserve a central lane for later placement.", "Layer palette and silhouettes need art-direction review at phone size.", "Scene files are concept studies and have not been admitted to the runtime asset catalog."],
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
