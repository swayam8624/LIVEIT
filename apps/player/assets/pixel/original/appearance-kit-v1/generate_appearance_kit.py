"""Build an original, deterministic 24x32 modular pixel appearance kit.

The output is intentionally concept-only.  All pixels are authored here with
Pillow primitives; there are no downloaded or third-party source images.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).parent
W, H = 24, 32
PIVOT = [12, 28]


def canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def rect(d: ImageDraw.ImageDraw, xy, color):
    d.rectangle(xy, fill=color)


def poly(d: ImageDraw.ImageDraw, points, color):
    d.polygon(points, fill=color)


def save(im: Image.Image, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


SKIN = {
    "warm_light": (241, 191, 146, 255),
    "golden": (209, 145, 94, 255),
    "deep_brown": (118, 69, 46, 255),
    "rose_brown": (170, 103, 80, 255),
}

HAIR = {
    "auburn_bob": ((118, 48, 38, 255), (75, 30, 30, 255)),
    "coil_crown": ((54, 31, 28, 255), (31, 20, 24, 255)),
    "silver_crop": ((184, 194, 199, 255), (104, 117, 127, 255)),
    "teal_headwrap": ((32, 121, 126, 255), (19, 72, 81, 255)),
    "dark_curls": ((42, 29, 34, 255), (20, 18, 25, 255)),
    "long_braid": ((128, 75, 45, 255), (76, 43, 36, 255)),
}

TOPS = {
    "cream_blouse": ((239, 224, 185, 255), (182, 153, 116, 255)),
    "teal_hoodie": ((37, 113, 119, 255), (21, 66, 76, 255)),
    "coral_cardigan": ((200, 83, 78, 255), (130, 46, 54, 255)),
    "mustard_sweater": ((217, 157, 53, 255), (143, 94, 30, 255)),
    "violet_tunic": ((111, 76, 145, 255), (67, 43, 96, 255)),
    "navy_overall": ((42, 66, 104, 255), (25, 39, 68, 255)),
}

BOTTOMS = {
    "teal_skirt": ((30, 99, 99, 255), (18, 58, 68, 255)),
    "indigo_trousers": ((42, 55, 107, 255), (24, 30, 66, 255)),
    "rust_shorts": ((155, 70, 48, 255), (95, 38, 34, 255)),
    "olive_pants": ((87, 105, 57, 255), (49, 65, 43, 255)),
    "plum_skirt": ((105, 50, 93, 255), (61, 29, 61, 255)),
}

SHOES = {
    "brown_boots": ((108, 62, 40, 255), (61, 35, 31, 255)),
    "white_sneakers": ((221, 224, 211, 255), (120, 132, 139, 255)),
    "red_flats": ((173, 52, 55, 255), (91, 29, 39, 255)),
    "teal_sandals": ((41, 135, 133, 255), (22, 75, 81, 255)),
}

ACCESSORIES = {
    "ochre_satchel": "satchel",
    "teal_scarf": "scarf",
    "round_glasses": "glasses",
    "sun_hat": "hat",
    "walking_cane": "cane",
    "hair_ribbon": "ribbon",
    "silver_earrings": "earrings",
    "birthmark": "birthmark",
}


def skin_layer(tone):
    im, d = canvas()
    c = SKIN[tone]
    shadow = tuple(max(0, x - 35) for x in c[:3]) + (255,)
    # Head, neck, hands, and lower legs.  Clothing layers cover the middle.
    rect(d, (8, 4, 15, 11), c)
    rect(d, (9, 3, 14, 4), c)
    rect(d, (10, 11, 13, 14), c)
    rect(d, (5, 13, 7, 20), c)
    rect(d, (16, 13, 18, 20), c)
    rect(d, (6, 20, 9, 26), c)
    rect(d, (14, 20, 17, 26), c)
    rect(d, (6, 26, 9, 28), shadow)
    rect(d, (14, 26, 17, 28), shadow)
    # Tiny facial pixels keep the mask readable without implying a fixed identity.
    eye = tuple(max(0, x - 70) for x in c[:3]) + (255,)
    rect(d, (9, 7, 9, 7), eye)
    rect(d, (14, 7, 14, 7), eye)
    return im


def hair_layer(kind):
    im, d = canvas()
    c, s = HAIR[kind]
    if kind == "auburn_bob":
        rect(d, (7, 3, 16, 10), c); rect(d, (6, 6, 8, 13), c); rect(d, (15, 6, 17, 13), c)
        rect(d, (8, 2, 14, 3), s); rect(d, (7, 9, 8, 11), s)
    elif kind == "coil_crown":
        for x, y in [(7, 4), (9, 2), (12, 2), (15, 4), (7, 7), (16, 7)]:
            rect(d, (x, y, x + 2, y + 3), c)
        rect(d, (8, 3, 15, 5), s)
    elif kind == "silver_crop":
        rect(d, (7, 3, 16, 7), c); rect(d, (8, 2, 14, 3), s); rect(d, (7, 6, 8, 9), c); rect(d, (15, 6, 16, 9), c)
    elif kind == "teal_headwrap":
        rect(d, (7, 3, 16, 7), c); rect(d, (8, 2, 14, 3), c); rect(d, (15, 4, 17, 9), s); rect(d, (6, 5, 8, 8), s)
    elif kind == "dark_curls":
        for x, y in [(7, 4), (9, 2), (12, 2), (15, 3), (6, 7), (16, 7), (7, 9), (16, 9)]:
            rect(d, (x, y, x + 2, y + 2), c)
        rect(d, (9, 3, 14, 5), s)
    elif kind == "long_braid":
        rect(d, (7, 3, 16, 8), c); rect(d, (8, 2, 14, 3), s)
        rect(d, (15, 7, 17, 18), c); rect(d, (16, 17, 18, 20), s)
        rect(d, (7, 7, 8, 10), s)
    return im


def top_layer(kind):
    im, d = canvas(); c, s = TOPS[kind]
    poly(d, [(8, 12), (15, 12), (17, 20), (6, 20)], c)
    rect(d, (7, 14, 16, 19), c)
    rect(d, (8, 12, 9, 14), s); rect(d, (14, 12, 15, 14), s)
    rect(d, (5, 14, 7, 17), c); rect(d, (16, 14, 18, 17), c)
    if kind == "cream_blouse":
        rect(d, (10, 13, 13, 14), (121, 92, 77, 255)); rect(d, (11, 15, 12, 19), s)
    elif kind == "teal_hoodie":
        rect(d, (9, 12, 14, 13), s); rect(d, (11, 17, 12, 19), s)
    elif kind == "coral_cardigan":
        rect(d, (11, 13, 12, 19), s); rect(d, (8, 13, 9, 19), c); rect(d, (14, 13, 15, 19), c)
    elif kind == "mustard_sweater":
        rect(d, (9, 14, 14, 15), s); rect(d, (10, 17, 13, 17), s)
    elif kind == "violet_tunic":
        rect(d, (8, 19, 15, 21), c)
    elif kind == "navy_overall":
        rect(d, (8, 12, 9, 15), s); rect(d, (14, 12, 15, 15), s); rect(d, (10, 16, 13, 17), s)
    return im


def bottom_layer(kind):
    im, d = canvas(); c, s = BOTTOMS[kind]
    if "skirt" in kind:
        poly(d, [(7, 19), (16, 19), (18, 26), (5, 26)], c)
        rect(d, (6, 20, 17, 21), s)
    elif "shorts" in kind:
        rect(d, (7, 19, 16, 23), c); rect(d, (7, 22, 10, 24), s); rect(d, (13, 22, 16, 24), s)
    else:
        rect(d, (7, 19, 16, 24), c); rect(d, (7, 23, 10, 26), c); rect(d, (13, 23, 16, 26), c)
        rect(d, (8, 20, 8, 24), s); rect(d, (15, 20, 15, 24), s)
    return im


def shoes_layer(kind):
    im, d = canvas(); c, s = SHOES[kind]
    rect(d, (5, 26, 10, 29), c); rect(d, (13, 26, 18, 29), c)
    rect(d, (5, 28, 10, 29), s); rect(d, (13, 28, 18, 29), s)
    if kind == "white_sneakers":
        rect(d, (6, 26, 9, 26), (248, 245, 224, 255)); rect(d, (14, 26, 17, 26), (248, 245, 224, 255))
    return im


def accessory_layer(kind):
    im, d = canvas()
    if kind == "ochre_satchel":
        rect(d, (3, 17, 6, 22), (178, 119, 40, 255)); rect(d, (4, 16, 15, 17), (178, 119, 40, 255)); rect(d, (3, 20, 6, 23), (116, 68, 35, 255))
    elif kind == "teal_scarf":
        rect(d, (8, 11, 15, 13), (31, 137, 139, 255)); rect(d, (14, 12, 16, 18), (21, 98, 109, 255))
    elif kind == "round_glasses":
        rect(d, (8, 6, 10, 8), (38, 39, 50, 255)); rect(d, (13, 6, 15, 8), (38, 39, 50, 255)); rect(d, (10, 7, 13, 7), (38, 39, 50, 255))
    elif kind == "sun_hat":
        rect(d, (5, 2, 18, 3), (205, 151, 70, 255)); rect(d, (8, 0, 15, 2), (227, 181, 88, 255)); rect(d, (9, 3, 14, 3), (160, 98, 45, 255))
    elif kind == "walking_cane":
        rect(d, (18, 13, 19, 28), (115, 75, 49, 255)); rect(d, (17, 12, 19, 13), (115, 75, 49, 255))
    elif kind == "hair_ribbon":
        rect(d, (15, 4, 17, 5), (228, 84, 100, 255)); rect(d, (17, 4, 18, 6), (228, 84, 100, 255))
    elif kind == "silver_earrings":
        rect(d, (7, 8, 7, 9), (226, 213, 156, 255)); rect(d, (16, 8, 16, 9), (226, 213, 156, 255))
    elif kind == "birthmark":
        rect(d, (14, 8, 14, 9), (134, 68, 77, 255))
    return im


def composite(skin, hair, top, bottom, shoes, accessory):
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for layer in (skin, bottom, top, shoes, hair, accessory):
        out.alpha_composite(layer)
    return out


def main():
    layers = {}
    for name in SKIN:
        layers[f"skin/{name}"] = skin_layer(name)
    for name in HAIR:
        layers[f"hair/{name}"] = hair_layer(name)
    for name in TOPS:
        layers[f"tops/{name}"] = top_layer(name)
    for name in BOTTOMS:
        layers[f"bottoms/{name}"] = bottom_layer(name)
    for name in SHOES:
        layers[f"shoes/{name}"] = shoes_layer(name)
    for name in ACCESSORIES:
        layers[f"accessories/{name}"] = accessory_layer(name)

    records = []
    for key, im in layers.items():
        group, name = key.split("/")
        path = ROOT / "layers" / group / f"{name}-24x32.png"
        save(im, path)
        records.append({
            "id": f"appearance.{group}.{name}",
            "group": group,
            "name": name,
            "file": path.relative_to(ROOT).as_posix(),
            "width": W,
            "height": H,
            "mode": "RGBA",
            "pivot": PIVOT,
            "runtimeReady": False,
            "notes": "Original deterministic layer concept; verify palette and occlusion in renderer.",
        })

    examples = [
        ("warm-courier", "warm_light", "auburn_bob", "cream_blouse", "teal_skirt", "brown_boots", "ochre_satchel"),
        ("golden-student", "golden", "dark_curls", "teal_hoodie", "indigo_trousers", "white_sneakers", "round_glasses"),
        ("deep-gardener", "deep_brown", "coil_crown", "mustard_sweater", "olive_pants", "teal_sandals", "sun_hat"),
        ("rose-elder", "rose_brown", "silver_crop", "violet_tunic", "plum_skirt", "red_flats", "walking_cane"),
        ("wrap-artist", "deep_brown", "teal_headwrap", "coral_cardigan", "rust_shorts", "teal_sandals", "teal_scarf"),
        ("braided-parent", "golden", "long_braid", "navy_overall", "indigo_trousers", "brown_boots", "hair_ribbon"),
        ("silver-portrait", "warm_light", "silver_crop", "cream_blouse", "indigo_trousers", "white_sneakers", "silver_earrings"),
        ("birthmark-artist", "rose_brown", "dark_curls", "violet_tunic", "teal_skirt", "red_flats", "birthmark"),
    ]
    example_records = []
    for ex in examples:
        name, sk, ha, to, bo, sh, ac = ex
        im = composite(layers[f"skin/{sk}"], layers[f"hair/{ha}"], layers[f"tops/{to}"], layers[f"bottoms/{bo}"], layers[f"shoes/{sh}"], layers[f"accessories/{ac}"])
        path = ROOT / "composites" / f"{name}-24x32.png"
        save(im, path)
        example_records.append({
            "id": f"appearance.composite.{name}",
            "file": path.relative_to(ROOT).as_posix(),
            "width": W,
            "height": H,
            "mode": "RGBA",
            "pivot": PIVOT,
            "layers": [f"appearance.skin.{sk}", f"appearance.bottoms.{bo}", f"appearance.tops.{to}", f"appearance.shoes.{sh}", f"appearance.hair.{ha}", f"appearance.accessories.{ac}"],
            "runtimeReady": False,
            "notes": "Composite proof only; not an integrated player identity.",
        })

    # 8 columns x 2 rows at 4x size, nearest-neighbor for review.
    preview = Image.new("RGBA", (W * 4 * 8, H * 4 * 2), (18, 24, 35, 255))
    for i, record in enumerate(example_records):
        im = Image.open(ROOT / record["file"])
        preview.alpha_composite(im.resize((W * 4, H * 4), Image.Resampling.NEAREST), (i % 8 * W * 4, i // 8 * H * 4))
    save(preview, ROOT / "appearance-composites-preview-4x.png")

    manifest = {
        "schema": "liveit.pixel.appearance-kit.v1",
        "generatedBy": "generate_appearance_kit.py",
        "logicalFrame": {"width": W, "height": H, "pivot": PIVOT, "mode": "RGBA"},
        "layerOrder": ["skin", "bottoms", "tops", "shoes", "hair", "accessories"],
        "occlusionPolicy": "Later layers may cover earlier pixels; each file keeps transparent pixels outside its own silhouette.",
        "runtimeReady": False,
        "assets": records,
        "composites": example_records,
        "limitations": [
            "Static south-facing concept layers only; no four-direction or walk-phase variants.",
            "24x32 is a compositing study and has not been imported into the player renderer.",
            "Some accessory silhouettes intentionally overlap the canonical 24x32 frame and need renderer review.",
        ],
    }
    for record in records + example_records:
        p = ROOT / record["file"]
        record["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
