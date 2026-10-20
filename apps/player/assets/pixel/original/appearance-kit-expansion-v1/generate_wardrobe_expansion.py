"""Generate an original directional wardrobe/accessory expansion.

All pixels are hand-authored Pillow primitives.  The package is a review
artifact: it deliberately does not touch the runtime catalog.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
W, H = 24, 32
PIVOT = [12, 28]
DIRECTIONS = ["south", "west", "east", "north"]
PALETTE = {
    "outline": (33, 28, 42, 255), "ink": (43, 42, 58, 255),
    "olive": (116, 126, 66, 255), "rust": (167, 79, 57, 255),
    "cobalt": (50, 82, 145, 255), "plum": (111, 65, 121, 255),
    "cream": (231, 214, 167, 255), "sky": (96, 166, 177, 255),
    "ochre": (207, 152, 57, 255), "rose": (194, 95, 107, 255),
    "leaf": (61, 130, 92, 255), "leather": (121, 71, 45, 255),
    "silver": (178, 190, 194, 255), "gold": (235, 190, 61, 255),
    "white": (236, 237, 222, 255), "skin": (202, 143, 104, 255),
}

SETS = {
    "hair": {"copper_pixie": ("rust", "ochre"), "lavender_locs": ("plum", "rose"),
             "forest_bun": ("leaf", "olive"), "midnight_ponytail": ("ink", "cobalt"),
             "silver_twists": ("silver", "white"), "sunset_headscarf": ("rose", "ochre")},
    "outerwear": {"olive_parka": ("olive", "cream"), "rust_peacoat": ("rust", "cream"),
                   "cobalt_raincoat": ("cobalt", "sky"), "plum_cardigan": ("plum", "rose"),
                   "cream_shawl": ("cream", "ochre"), "leaf_bomber": ("leaf", "gold")},
    "bottom": {"wide_culottes": ("plum", "rose"), "patched_denim": ("cobalt", "sky"),
                "linen_wrap": ("cream", "ochre"), "utility_shorts": ("olive", "rust")},
    "mobility": {"teal_cane": ("sky", "ink"), "wooden_crutch": ("leather", "ink"),
                 "folding_walker": ("silver", "ink"), "stroller_handle": ("rose", "ink")},
    "seasonal": {"knit_beanie": ("rust", "cream"), "sun_visor": ("ochre", "cream"),
                  "rain_hood": ("cobalt", "sky"), "wool_muffler": ("plum", "rose")},
    "cultural": {"patterned_sash": ("rose", "gold"), "woven_shoulder_cloth": ("leaf", "ochre"),
                 "prayer_beads": ("gold", "plum"), "embroidered_cap": ("cobalt", "gold")},
}


def blank():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)


def box(d, xy, c): d.rectangle(xy, fill=c)
def poly(d, pts, c): d.polygon(pts, fill=c)


def directional_anchor(direction):
    # Distinct coordinates per facing; never derive one facing by mirroring.
    return {"south": (8, 4, 15, 11), "west": (6, 5, 13, 12),
            "east": (11, 5, 18, 12), "north": (8, 3, 15, 10)}[direction]


def layer(kind, name, direction):
    im, d = blank(); a, b = (PALETTE[x] for x in SETS[kind][name])
    x0, y0, x1, y1 = directional_anchor(direction)
    if kind == "hair":
        if name == "copper_pixie":
            box(d, (x0, y0, x1, y0 + 4), a); box(d, (x0 - 1, y0 + 3, x0 + 1, y0 + 8), b)
        elif name == "lavender_locs":
            for x in range(x0, x1 + 1, 3): box(d, (x, y0 + 1, x + 2, y0 + 7), a)
            box(d, (x0 + 2, y0, x1 - 1, y0 + 2), b)
        elif name == "forest_bun":
            box(d, (x0, y0 + 1, x1, y0 + 5), a); box(d, (x0 + 3, y0 - 2, x0 + 6, y0 + 1), b)
            box(d, (x1 - 2, y0 - 1, x1 + 1, y0 + 2), a)
        elif name == "midnight_ponytail":
            box(d, (x0, y0 + 1, x1, y0 + 5), a); box(d, (x1, y0 + 3, x1 + 3, y0 + 9), b)
        elif name == "silver_twists":
            box(d, (x0, y0 + 1, x1, y0 + 4), a)
            for x in (x0, x0 + 3, x1 - 2): box(d, (x, y0 + 3, x + 2, y0 + 8), b)
        else:
            box(d, (x0, y0 + 1, x1, y0 + 5), a); box(d, (x0 + 2, y0, x1 - 2, y0 + 2), b)
            box(d, (x1, y0 + 4, x1 + 2, y0 + 10), a)
    elif kind == "outerwear":
        poly(d, [(x0, 12), (x1, 12), (x1 + 2, 21), (x0 - 2, 21)], a)
        box(d, (x0 + 2, 13, x1 - 2, 20), b)
        if direction == "south": box(d, (11, 13, 12, 20), a)
        elif direction == "west": box(d, (7, 14, 8, 19), b)
        elif direction == "east": box(d, (15, 14, 16, 19), b)
        else: box(d, (x0 + 2, 12, x1 - 2, 14), b)
    elif kind == "bottom":
        if name == "wide_culottes":
            poly(d, [(7, 19), (16, 19), (18, 26), (5, 26)], a)
            if direction == "south": box(d, (11, 20, 12, 25), b)
            elif direction == "west": box(d, (7, 21, 8, 24), b)
            elif direction == "east": box(d, (15, 21, 16, 24), b)
            else: box(d, (9, 19, 14, 20), b)
        elif name == "patched_denim":
            box(d, (7, 19, 16, 25), a)
            if direction == "south": box(d, (8, 21, 9, 22), b); box(d, (14, 23, 15, 24), b)
            elif direction == "west": box(d, (7, 21, 8, 23), b)
            elif direction == "east": box(d, (15, 20, 16, 22), b)
            else: box(d, (10, 19, 13, 20), b)
        elif name == "linen_wrap":
            poly(d, [(7, 19), (16, 19), (17, 26), (6, 26)], a)
            if direction == "south": box(d, (11, 20, 12, 25), b)
            elif direction == "west": box(d, (7, 20, 8, 24), b)
            elif direction == "east": box(d, (15, 20, 16, 24), b)
            else: box(d, (9, 19, 14, 20), b)
        else:
            box(d, (7, 19, 16, 24), a)
            if direction == "south": box(d, (8, 23, 10, 25), b); box(d, (13, 23, 15, 25), b)
            elif direction == "west": box(d, (7, 22, 9, 24), b)
            elif direction == "east": box(d, (14, 22, 16, 24), b)
            else: box(d, (10, 19, 13, 20), b)
    elif kind == "mobility":
        if name == "teal_cane":
            x = 5 if direction in ("west", "north") else 18; box(d, (x, 15, x + 1, 28), a); box(d, (x - 1, 14, x + 2, 16), b)
        elif name == "wooden_crutch":
            x = 5 if direction == "west" else 18; box(d, (x, 13, x + 1, 28), a); box(d, (x - 2, 12, x + 3, 13), b)
        elif name == "folding_walker":
            box(d, (5, 17, 6, 28), a); box(d, (18, 17, 19, 28), a); box(d, (5, 17, 19, 18), b); box(d, (7, 26, 8, 29), b); box(d, (16, 26, 17, 29), b)
        else:
            box(d, (4, 20, 19, 21), a); box(d, (5, 20, 6, 28), b); box(d, (17, 20, 18, 28), b); box(d, (8, 18, 15, 19), a)
        # Small direction-specific hardware glints preserve four authored states
        # even for symmetric accessibility equipment.
        glint = {"south": (10, 22), "west": (8, 20), "east": (15, 20), "north": (12, 18)}[direction]
        box(d, (glint[0], glint[1], glint[0] + 1, glint[1]), b)
    elif kind == "seasonal":
        if name == "knit_beanie": box(d, (x0, y0 - 1, x1, y0 + 3), a); box(d, (x0 + 2, y0 - 2, x1 - 2, y0 - 1), b)
        elif name == "sun_visor": box(d, (x0, y0 + 1, x1, y0 + 2), a); box(d, (x1 - 1, y0 + 2, x1 + 3, y0 + 3), b)
        elif name == "rain_hood": box(d, (x0 - 1, y0, x1 + 1, y0 + 6), a); box(d, (x0, y0 + 5, x1, y0 + 6), b)
        else:
            box(d, (x0 - 1, 11, x1 + 1, 13), a); box(d, (x0, 12, x1, 14), b)
            if direction == "south": box(d, (11, 13, 12, 15), a)
            elif direction == "west": box(d, (x0 - 1, 13, x0, 16), a)
            elif direction == "east": box(d, (x1, 13, x1 + 1, 16), a)
            else: box(d, (x0 + 2, 10, x1 - 2, 11), a)
    else:
        if name == "patterned_sash":
            if direction == "south": box(d, (6, 15, 17, 17), a)
            elif direction == "north": box(d, (7, 14, 16, 16), a)
            elif direction == "west": box(d, (7, 14, 10, 21), a)
            else: box(d, (14, 14, 17, 21), a)
            box(d, (11, 15, 12, 16), b)
        elif name == "woven_shoulder_cloth":
            box(d, (x0 - 1, 12, x0 + 2, 21), a); box(d, (x0, 13, x0 + 1, 18), b)
        elif name == "prayer_beads":
            for x, y in [(9, 14), (11, 15), (13, 14), (10, 17), (12, 18), (14, 17)]: box(d, (x, y, x + 1, y + 1), a)
        else:
            box(d, (x0 + 1, y0, x1 - 1, y0 + 2), a); box(d, (x0 + 3, y0 + 1, x0 + 4, y0 + 1), b)
        marker = {"south": (10, 19), "west": (8, 18), "east": (15, 18), "north": (12, 12)}[direction]
        box(d, (marker[0], marker[1], marker[0], marker[1]), b)
    return im


def base(direction, skin_name="skin"):
    im, d = blank(); x0, y0, x1, y1 = directional_anchor(direction)
    c = PALETTE["skin"]
    box(d, (x0 + 1, y0 + 3, x1 - 1, y0 + 8), c); box(d, (x0 + 3, 11, x1 - 3, 14), c)
    box(d, (5, 14, 7, 20), c); box(d, (17, 14, 19, 20), c)
    box(d, (7, 20, 10, 27), c); box(d, (14, 20, 17, 27), c)
    box(d, (6, 27, 10, 29), PALETTE["outline"]); box(d, (14, 27, 18, 29), PALETTE["outline"])
    if direction == "south": box(d, (9, 7, 9, 7), PALETTE["outline"]); box(d, (14, 7, 14, 7), PALETTE["outline"])
    elif direction == "west": box(d, (7, 8, 7, 8), PALETTE["outline"])
    elif direction == "east": box(d, (16, 8, 16, 8), PALETTE["outline"])
    return im


def compose(direction, hair, outerwear, bottom, accessory, seasonal=None):
    im = base(direction)
    for kind, name in [("bottom", bottom), ("outerwear", outerwear), ("hair", hair), ("cultural", accessory)]: im.alpha_composite(layer(kind, name, direction))
    if seasonal: im.alpha_composite(layer("seasonal", seasonal, direction))
    return im


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    records = []; atlas_cells = []
    for kind, names in SETS.items():
        for name in names:
            for direction in DIRECTIONS:
                path = ROOT / "layers" / direction / kind / f"{name}-24x32.png"; path.parent.mkdir(parents=True, exist_ok=True)
                layer(kind, name, direction).save(path)
                records.append({"id": f"{direction}/{kind}/{name}", "path": str(path.relative_to(ROOT)), "kind": kind, "name": name, "direction": direction, "size": [W, H], "mode": "RGBA", "pivot": PIVOT, "sha256": sha(path), "runtimeReady": False})
    examples = [("dara", "forest_bun", "olive_parka", "patched_denim", "patterned_sash", "knit_beanie"), ("imani", "lavender_locs", "plum_cardigan", "wide_culottes", "woven_shoulder_cloth", "wool_muffler"), ("soren", "midnight_ponytail", "cobalt_raincoat", "utility_shorts", "prayer_beads", "rain_hood")]
    for identity, hair, outer, bottom, acc, seasonal in examples:
        for direction in DIRECTIONS:
            path = ROOT / "composites" / identity / f"{direction}-24x32.png"; path.parent.mkdir(parents=True, exist_ok=True)
            compose(direction, hair, outer, bottom, acc, seasonal).save(path)
            records.append({"id": f"composite/{identity}/{direction}", "path": str(path.relative_to(ROOT)), "kind": "composite", "name": identity, "direction": direction, "size": [W, H], "mode": "RGBA", "pivot": PIVOT, "sha256": sha(path), "runtimeReady": False})
    # 3x contact sheet, with rows of components and composites.
    thumbs = []
    for r in records:
        p = ROOT / r["path"]
        if r["kind"] == "composite" or (r["kind"] in ("hair", "outerwear", "cultural") and r["direction"] == "south"):
            im = Image.open(p).resize((72, 96), Image.Resampling.NEAREST); thumbs.append((r["id"], im))
    cols = 12; rows = (len(thumbs) + cols - 1) // cols; atlas = Image.new("RGBA", (cols * 88, rows * 116), (25, 24, 34, 255)); ad = ImageDraw.Draw(atlas)
    for i, (label, im) in enumerate(thumbs):
        x = (i % cols) * 88 + 8; y = (i // cols) * 116 + 4; atlas.alpha_composite(im, (x, y)); ad.text((x, y + 97), label.split("/")[-1][:13], fill=PALETTE["white"])
    atlas.save(ROOT / "appearance-kit-expansion-preview-3x.png")
    manifest = {"schema": "liveit.pixel.appearance-kit-expansion.v1", "runtimeReady": False, "canvas": {"size": [W, H], "mode": "RGBA", "pivot": PIVOT}, "directions": DIRECTIONS, "layerOrder": ["base", "bottom", "outerwear", "hair", "cultural", "seasonal", "mobility"], "sets": {k: list(v) for k, v in SETS.items()}, "records": records, "contactSheet": {"path": "appearance-kit-expansion-preview-3x.png", "runtimeReady": False}}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    provenance = {"schema": "liveit.pixel.provenance.v1", "package": "appearance-kit-expansion-v1", "source": "generate_wardrobe_expansion.py", "authorship": "Original Pillow primitives and hand-authored palette; no supplied archives, internet images, or third-party pixels used.", "generatedAt": "2026-10-20", "runtimeReady": False, "reviewLimits": ["concept-only", "directional parity and age-safe layering require human art review", "renderer import and device evidence are outstanding"]}
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(f"generated {len(records)} hashed PNG records")


if __name__ == "__main__": main()
