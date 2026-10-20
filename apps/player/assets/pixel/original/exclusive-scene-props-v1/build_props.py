from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
SIZE = 64
PIVOT = [32, 60]
SCENE_ORDER = ["graduation", "new-parenthood", "elder-legacy"]

PALETTE = {
    "ink": (39, 31, 49, 255),
    "shadow": (79, 52, 70, 255),
    "wood": (126, 75, 53, 255),
    "wood_hi": (190, 119, 69, 255),
    "gold": (244, 193, 85, 255),
    "cream": (255, 231, 177, 255),
    "paper": (247, 239, 208, 255),
    "red": (203, 74, 74, 255),
    "rose": (232, 126, 139, 255),
    "mint": (101, 190, 153, 255),
    "teal": (59, 141, 157, 255),
    "blue": (76, 116, 189, 255),
    "lavender": (143, 115, 190, 255),
    "brown": (105, 65, 48, 255),
    "white": (255, 255, 239, 255),
    "skin": (224, 154, 115, 255),
    "leaf": (76, 132, 71, 255),
    "glass": (173, 218, 224, 255),
}


def rgba(name: str):
    return PALETTE[name]


def base() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    return image, ImageDraw.Draw(image)


def shadow(draw: ImageDraw.ImageDraw, box=(19, 56, 45, 60)):
    draw.rectangle(box, fill=rgba("shadow"))
    draw.rectangle((box[0] + 3, box[1], box[2] - 3, box[3] - 1), fill=rgba("ink"))


def graduation(kind: str) -> Image.Image:
    im, d = base()
    shadow(d)
    if kind == "ceremony-sign":
        d.rectangle((30, 10, 33, 57), fill=rgba("wood")); d.rectangle((31, 10, 32, 57), fill=rgba("wood_hi"))
        d.polygon([(10, 9), (53, 9), (50, 29), (13, 29)], fill=rgba("ink"))
        d.polygon([(13, 12), (50, 12), (48, 26), (15, 26)], fill=rgba("gold"))
        d.rectangle((20, 17, 43, 20), fill=rgba("red")); d.rectangle((24, 21, 39, 23), fill=rgba("cream"))
    elif kind == "folding-chair":
        d.line((15, 19, 48, 19), fill=rgba("ink"), width=4); d.rectangle((16, 16, 47, 23), fill=rgba("blue"))
        d.line((17, 22, 22, 56), fill=rgba("ink"), width=4); d.line((46, 22, 40, 56), fill=rgba("ink"), width=4)
        d.line((22, 34, 42, 34), fill=rgba("teal"), width=3)
    elif kind == "honor-cord":
        d.arc((18, 16, 46, 50), 15, 170, fill=rgba("gold"), width=4); d.arc((20, 18, 44, 48), 10, 168, fill=rgba("red"), width=2)
        d.rectangle((18, 43, 22, 57), fill=rgba("gold")); d.rectangle((42, 43, 46, 57), fill=rgba("gold"))
        d.polygon([(17, 55), (23, 55), (20, 60)], fill=rgba("red")); d.polygon([(41, 55), (47, 55), (44, 60)], fill=rgba("red"))
    elif kind == "confetti-popper":
        d.polygon([(14, 16), (49, 26), (40, 51), (10, 37)], fill=rgba("ink"))
        d.polygon([(17, 19), (46, 28), (38, 47), (14, 36)], fill=rgba("lavender"))
        for x, y, c in [(23, 25, "gold"), (32, 28, "mint"), (38, 34, "red"), (24, 35, "cream"), (34, 40, "teal")]:
            d.rectangle((x, y, x + 4, y + 4), fill=rgba(c))
        d.rectangle((39, 47, 44, 55), fill=rgba("wood"))
    elif kind == "diploma-tube":
        d.rectangle((10, 24, 52, 40), fill=rgba("ink")); d.rectangle((12, 26, 50, 38), fill=rgba("red")); d.rectangle((16, 24, 20, 40), fill=rgba("gold")); d.rectangle((42, 24, 46, 40), fill=rgba("gold"))
        d.ellipse((8, 24, 18, 40), fill=rgba("gold")); d.ellipse((46, 24, 54, 40), fill=rgba("cream")); d.rectangle((29, 39, 34, 55), fill=rgba("wood")); d.rectangle((25, 53, 38, 57), fill=rgba("wood_hi"))
    else:  # flower wreath
        d.ellipse((13, 13, 51, 49), outline=rgba("leaf"), width=5); d.ellipse((20, 20, 44, 42), fill=(0, 0, 0, 0), outline=rgba("ink"), width=2)
        for x, y, c in [(16, 16, "rose"), (43, 18, "gold"), (17, 38, "cream"), (44, 37, "red"), (28, 12, "lavender")]:
            d.rectangle((x - 3, y - 3, x + 3, y + 3), fill=rgba(c)); d.rectangle((x - 1, y - 5, x + 1, y + 5), fill=rgba(c))
    return im


def parenthood(kind: str) -> Image.Image:
    im, d = base(); shadow(d)
    if kind == "folded-blanket":
        d.polygon([(10, 27), (50, 21), (55, 45), (15, 51)], fill=rgba("ink")); d.polygon([(14, 29), (47, 24), (51, 42), (18, 47)], fill=rgba("teal")); d.line((14, 35, 50, 30), fill=rgba("cream"), width=3); d.line((17, 42, 51, 37), fill=rgba("mint"), width=3)
    elif kind == "feeding-bottle":
        d.rectangle((22, 22, 42, 49), fill=rgba("ink")); d.rectangle((25, 25, 39, 46), fill=rgba("glass")); d.rectangle((21, 17, 43, 24), fill=rgba("rose")); d.rectangle((27, 11, 37, 18), fill=rgba("ink")); d.rectangle((29, 10, 35, 15), fill=rgba("cream")); d.line((31, 29, 31, 43), fill=rgba("white"), width=2)
    elif kind == "lullaby-mobile":
        d.line((31, 9, 31, 54), fill=rgba("ink"), width=3); d.line((18, 20, 45, 20), fill=rgba("ink"), width=3); d.line((18, 20, 18, 32), fill=rgba("teal"), width=2); d.line((31, 20, 31, 35), fill=rgba("rose"), width=2); d.line((44, 20, 44, 30), fill=rgba("gold"), width=2)
        d.polygon([(12, 31), (24, 31), (18, 41)], fill=rgba("teal")); d.polygon([(25, 34), (37, 34), (31, 44)], fill=rgba("rose")); d.ellipse((39, 29, 49, 39), fill=rgba("gold"))
    elif kind == "toy-blocks":
        for box, c, letter in [((11, 31, 30, 51), "red", "A"), ((29, 25, 48, 45), "gold", "B"), ((24, 42, 43, 60), "mint", "C")]:
            d.rectangle(box, fill=rgba("ink")); d.rectangle((box[0] + 3, box[1] + 3, box[2] - 3, box[3] - 3), fill=rgba(c)); d.rectangle((box[0] + 7, box[1] + 8, box[0] + 11, box[1] + 12), fill=rgba("cream"))
    elif kind == "footprint-card":
        d.rectangle((14, 12, 50, 53), fill=rgba("ink")); d.rectangle((17, 15, 47, 50), fill=rgba("paper")); d.rectangle((22, 22, 29, 38), fill=rgba("rose")); d.ellipse((21, 17, 30, 27), fill=rgba("rose")); d.rectangle((34, 22, 41, 38), fill=rgba("teal")); d.ellipse((33, 17, 42, 27), fill=rgba("teal")); d.rectangle((23, 42, 41, 45), fill=rgba("gold"))
    else:  # night lamp
        d.rectangle((27, 29, 37, 56), fill=rgba("ink")); d.rectangle((30, 32, 34, 54), fill=rgba("gold")); d.polygon([(17, 26), (47, 26), (41, 12), (23, 12)], fill=rgba("ink")); d.polygon([(21, 24), (43, 24), (39, 15), (25, 15)], fill=rgba("cream")); d.rectangle((28, 56, 38, 59), fill=rgba("wood"))
    return im


def legacy(kind: str) -> Image.Image:
    im, d = base(); shadow(d)
    if kind == "framed-photo":
        d.rectangle((10, 10, 54, 48), fill=rgba("ink")); d.rectangle((14, 14, 50, 44), fill=rgba("wood_hi")); d.rectangle((18, 18, 46, 40), fill=rgba("teal")); d.rectangle((18, 31, 46, 40), fill=rgba("leaf")); d.ellipse((26, 21, 35, 30), fill=rgba("skin")); d.polygon([(24, 39), (29, 29), (39, 39)], fill=rgba("lavender")); d.rectangle((25, 48, 39, 56), fill=rgba("wood"))
    elif kind == "tea-tray":
        d.ellipse((9, 28, 55, 51), fill=rgba("ink")); d.ellipse((13, 30, 51, 47), fill=rgba("wood_hi")); d.rectangle((22, 21, 37, 39), fill=rgba("ink")); d.rectangle((25, 24, 34, 36), fill=rgba("cream")); d.arc((32, 25, 42, 35), 270, 90, fill=rgba("ink"), width=3); d.rectangle((39, 25, 45, 31), fill=rgba("paper")); d.rectangle((18, 47, 23, 54), fill=rgba("wood")); d.rectangle((41, 47, 46, 54), fill=rgba("wood"))
    elif kind == "knitting-basket":
        d.polygon([(12, 28), (51, 28), (45, 53), (18, 53)], fill=rgba("ink")); d.polygon([(16, 31), (47, 31), (42, 49), (21, 49)], fill=rgba("rose")); d.arc((17, 16, 47, 38), 180, 360, fill=rgba("ink"), width=4); d.line((26, 19, 20, 8), fill=rgba("gold"), width=3); d.line((37, 19, 45, 9), fill=rgba("gold"), width=3); d.rectangle((23, 35, 41, 39), fill=rgba("lavender"))
    elif kind == "birthday-cake":
        d.rectangle((11, 30, 53, 52), fill=rgba("ink")); d.rectangle((14, 33, 50, 48), fill=rgba("cream")); d.rectangle((16, 38, 48, 42), fill=rgba("rose")); d.rectangle((19, 24, 23, 32), fill=rgba("gold")); d.rectangle((31, 20, 35, 32), fill=rgba("gold")); d.rectangle((41, 25, 45, 32), fill=rgba("gold")); d.rectangle((20, 20, 22, 24), fill=rgba("red")); d.rectangle((32, 16, 34, 20), fill=rgba("red")); d.rectangle((42, 21, 44, 25), fill=rgba("red")); d.rectangle((19, 50, 45, 55), fill=rgba("wood"))
    elif kind == "reading-glasses":
        d.ellipse((12, 26, 30, 43), outline=rgba("ink"), width=4); d.ellipse((34, 26, 52, 43), outline=rgba("ink"), width=4); d.line((30, 33, 34, 33), fill=rgba("ink"), width=3); d.line((12, 30, 6, 25), fill=rgba("ink"), width=3); d.line((52, 30, 58, 25), fill=rgba("ink"), width=3); d.rectangle((17, 31, 25, 37), fill=rgba("glass")); d.rectangle((39, 31, 47, 37), fill=rgba("glass"))
    else:  # keepsake box
        d.rectangle((10, 28, 54, 52), fill=rgba("ink")); d.rectangle((14, 32, 50, 48), fill=rgba("wood_hi")); d.rectangle((10, 23, 54, 34), fill=rgba("ink")); d.rectangle((14, 26, 50, 31), fill=rgba("wood")); d.rectangle((29, 27, 35, 34), fill=rgba("gold")); d.rectangle((30, 43, 34, 48), fill=rgba("gold"))
    return im


PROPS = {
    "graduation": ["ceremony-sign", "folding-chair", "honor-cord", "confetti-popper", "diploma-tube", "flower-wreath"],
    "new-parenthood": ["folded-blanket", "feeding-bottle", "lullaby-mobile", "toy-blocks", "footprint-card", "night-lamp"],
    "elder-legacy": ["framed-photo", "tea-tray", "knitting-basket", "birthday-cake", "reading-glasses", "keepsake-box"],
}


def make_atlas(scene: str, names: list[str], out: Path):
    atlas = Image.new("RGBA", (SIZE * 3, SIZE * 2), (0, 0, 0, 0))
    for i, name in enumerate(names):
        maker = graduation if scene == "graduation" else parenthood if scene == "new-parenthood" else legacy
        atlas.paste(maker(name), ((i % 3) * SIZE, (i // 3) * SIZE))
    atlas.save(out)


def composite(scene: str, names: list[str], out: Path):
    im = Image.new("RGBA", (192, 128), (28, 34, 51, 255))
    d = ImageDraw.Draw(im)
    ground = {"graduation": (65, 102, 75, 255), "new-parenthood": (78, 67, 91, 255), "elder-legacy": (92, 72, 57, 255)}[scene]
    d.rectangle((0, 74, 191, 127), fill=ground); d.rectangle((0, 70, 191, 75), fill=rgba("ink"))
    maker = graduation if scene == "graduation" else parenthood if scene == "new-parenthood" else legacy
    positions = [(14, 46), (67, 46), (120, 46), (39, 72), (92, 72), (145, 72)]
    for name, (x, y) in zip(names, positions):
        im.alpha_composite(maker(name), (x, y))
    im.save(out)


def main():
    files = []
    manifest = {
        "schema": "liveit.pixel.exclusive-scene-props.v1",
        "generatedBy": "build_props.py",
        "canvas": {"size": [SIZE, SIZE], "mode": "RGBA", "scale": "1x", "pivot": PIVOT, "pivotMeaning": "bottom-center ground contact"},
        "runtimeReady": False,
        "scenes": [],
        "files": [],
    }
    for scene in SCENE_ORDER:
        scene_dir = ROOT / scene / "props"
        scene_dir.mkdir(parents=True, exist_ok=True)
        entries = []
        for index, name in enumerate(PROPS[scene]):
            out = scene_dir / f"{name}.png"
            maker = graduation if scene == "graduation" else parenthood if scene == "new-parenthood" else legacy
            maker(name).save(out)
            rel = out.relative_to(ROOT).as_posix()
            entries.append({"id": name, "path": rel, "size": [SIZE, SIZE], "pivot": PIVOT, "objectBounds": [6, 8, 58, 60], "drawDepth": round(0.42 + index * 0.015, 3), "interactive": True, "runtimeReady": False})
            files.append(out)
        atlas = scene_dir / f"{scene}-props-atlas.png"; preview = ROOT / f"{scene}-props-preview.png"
        make_atlas(scene, PROPS[scene], atlas); composite(scene, PROPS[scene], preview)
        files.extend([atlas, preview])
        manifest["scenes"].append({"id": scene, "props": entries, "atlas": atlas.relative_to(ROOT).as_posix(), "preview": preview.relative_to(ROOT).as_posix(), "runtimeReady": False})
    for path in sorted(files):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        with Image.open(path) as im:
            manifest["files"].append({"path": path.relative_to(ROOT).as_posix(), "sha256": digest, "size": list(im.size), "mode": im.mode})
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (ROOT / "provenance.json").write_text(json.dumps({"source": "original deterministic Pillow pixel construction", "thirdPartyAssets": [], "sourceArchivesUsed": [], "prompts": [], "license": "Original work for LIVEIT; review project licensing before commercial release", "runtimeReady": False}, indent=2) + "\n")


if __name__ == "__main__":
    main()
