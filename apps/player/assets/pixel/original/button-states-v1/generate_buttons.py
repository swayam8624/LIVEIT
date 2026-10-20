"""Create the original pixel button concept batch with Pillow.

The generator intentionally uses integer rectangles and polygons only.  It is
kept beside the output so the source pixels and the provenance remain
auditable without relying on a third-party art pack.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).parent
OUT = ROOT
BUTTON_W, BUTTON_H = 160, 48
ICON_SIZE = 24
SCALE = 4

PALETTE = {
    "ink": (43, 28, 57, 255),
    "ink_soft": (75, 49, 76, 255),
    "cream": (255, 232, 177, 255),
    "paper": (255, 245, 207, 255),
    "teal": (47, 139, 132, 255),
    "teal_hi": (101, 199, 169, 255),
    "mustard": (218, 164, 57, 255),
    "auburn": (155, 73, 65, 255),
    "coral": (220, 91, 82, 255),
    "slate": (117, 119, 135, 255),
    "slate_hi": (159, 160, 166, 255),
    "shadow": (25, 18, 37, 255),
}

FAMILIES = {
    "primary": {"label": "confirm / continue", "base": "teal", "accent": "teal_hi", "icon": "arrow"},
    "secondary": {"label": "open / inspect", "base": "cream", "accent": "mustard", "icon": "spark"},
    "choice": {"label": "story choice", "base": "mustard", "accent": "cream", "icon": "branch"},
    "phone": {"label": "phone / messages", "base": "auburn", "accent": "coral", "icon": "phone"},
    "danger": {"label": "cancel / leave", "base": "coral", "accent": "cream", "icon": "cross"},
    "utility": {"label": "settings / utility", "base": "ink_soft", "accent": "teal_hi", "icon": "gear"},
}

STATES = ("normal", "focused", "pressed", "disabled")


def rgba(name: str) -> tuple[int, int, int, int]:
    return PALETTE[name]


def stepped_plate(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill, border, state: str) -> None:
    x0, y0, x1, y1 = box
    # A 4px logical border with 4px stepped corners makes the plate safe for
    # nearest-neighbor scale-up and practical nine-slice use.
    outer = [(x0 + 4, y0), (x1 - 4, y0), (x1, y0 + 4), (x1, y1 - 4),
             (x1 - 4, y1), (x0 + 4, y1), (x0, y1 - 4), (x0, y0 + 4)]
    draw.polygon(outer, fill=border)
    inner = [(x0 + 8, y0 + 4), (x1 - 8, y0 + 4), (x1 - 4, y0 + 8),
             (x1 - 4, y1 - 8), (x1 - 8, y1 - 4), (x0 + 8, y1 - 4),
             (x0 + 4, y1 - 8), (x0 + 4, y0 + 8)]
    draw.polygon(inner, fill=fill)
    if state == "focused":
        draw.rectangle((x0 + 8, y0 + 8, x1 - 9, y1 - 9), outline=rgba("paper"), width=2)
        draw.rectangle((x0 + 12, y0 + 12, x1 - 13, y1 - 13), outline=rgba("cream"), width=1)
    elif state == "pressed":
        draw.rectangle((x0 + 8, y1 - 11, x1 - 9, y1 - 7), fill=rgba("shadow"))
        draw.line((x0 + 12, y0 + 7, x1 - 13, y0 + 7), fill=rgba("paper"), width=2)
    elif state == "normal":
        draw.line((x0 + 12, y0 + 7, x1 - 13, y0 + 7), fill=rgba("paper"), width=2)


def draw_icon(draw: ImageDraw.ImageDraw, kind: str, color, state: str) -> None:
    c = color
    if state == "disabled":
        c = rgba("slate_hi")
    # All glyphs stay inside a 24x24 logical cell and use chunky integer pixels.
    if kind == "arrow":
        draw.rectangle((4, 10, 16, 13), fill=c)
        draw.polygon([(13, 5), (20, 11), (13, 18)], fill=c)
    elif kind == "spark":
        draw.rectangle((10, 2, 13, 21), fill=c)
        draw.rectangle((2, 10, 21, 13), fill=c)
        draw.rectangle((7, 7, 16, 16), fill=c)
    elif kind == "branch":
        draw.rectangle((10, 3, 13, 19), fill=c)
        draw.rectangle((4, 3, 13, 6), fill=c)
        draw.rectangle((4, 3, 7, 12), fill=c)
        draw.rectangle((13, 17, 20, 20), fill=c)
        draw.rectangle((17, 13, 20, 20), fill=c)
    elif kind == "phone":
        draw.rectangle((5, 3, 18, 6), fill=c)
        draw.rectangle((3, 6, 7, 18), fill=c)
        draw.rectangle((7, 18, 17, 21), fill=c)
        draw.rectangle((17, 6, 21, 18), fill=c)
        draw.rectangle((8, 7, 16, 16), fill=rgba("ink"))
        draw.rectangle((10, 18, 14, 19), fill=c)
    elif kind == "cross":
        draw.rectangle((4, 10, 20, 13), fill=c)
        draw.rectangle((10, 4, 13, 20), fill=c)
    elif kind == "gear":
        draw.rectangle((8, 3, 15, 20), fill=c)
        draw.rectangle((3, 8, 20, 15), fill=c)
        draw.rectangle((7, 7, 16, 16), fill=c)
        draw.rectangle((10, 10, 13, 13), fill=rgba("ink"))


def make_button(family: str, state: str) -> Image.Image:
    spec = FAMILIES[family]
    image = Image.new("RGBA", (BUTTON_W, BUTTON_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    base = rgba(spec["base"])
    accent = rgba(spec["accent"])
    border = rgba("ink")
    if state == "disabled":
        base, accent, border = rgba("slate"), rgba("slate_hi"), rgba("ink_soft")
    elif state == "pressed":
        base = tuple(max(0, channel - 22) for channel in base[:3]) + (255,)
    stepped_plate(draw, (0, 0, BUTTON_W - 1, BUTTON_H - 1), base, border, state)
    draw_icon(draw, spec["icon"], accent, state)
    # A second, tiny pixel marker hints at the action without rasterizing text.
    draw.rectangle((BUTTON_W - 23, 20, BUTTON_W - 16, 27), fill=accent if state != "disabled" else rgba("slate_hi"))
    draw.rectangle((BUTTON_W - 20, 17, BUTTON_W - 19, 30), fill=accent if state != "disabled" else rgba("slate_hi"))
    return image


def make_icon(family: str, state: str) -> Image.Image:
    spec = FAMILIES[family]
    image = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    draw_icon(ImageDraw.Draw(image), spec["icon"], rgba(spec["accent"]), state)
    return image


def write_manifest() -> None:
    frames = []
    icons = []
    for family, spec in FAMILIES.items():
        for state in STATES:
            frames.append({
                "id": f"{family}-{state}", "file": f"buttons/{family}-{state}.png",
                "family": family, "state": state, "width": BUTTON_W, "height": BUTTON_H,
                "x": 0, "y": 0, "nineSliceInsets": {"left": 8, "top": 8, "right": 8, "bottom": 8},
                "iconFile": f"icons/{family}-{state}.png", "sampling": "nearest", "runtimeReady": False,
            })
            icons.append({
                "id": f"{family}-{state}-icon", "file": f"icons/{family}-{state}.png",
                "family": family, "state": state, "width": ICON_SIZE, "height": ICON_SIZE,
                "sampling": "nearest", "runtimeReady": False,
            })
    manifest = {
        "batch": "button-states-v1", "runtimeReady": False, "pixelArt": True,
        "sampling": "nearest", "buttonSize": [BUTTON_W, BUTTON_H], "iconSize": [ICON_SIZE, ICON_SIZE],
        "nineSliceInsets": {"left": 8, "top": 8, "right": 8, "bottom": 8},
        "states": list(STATES), "families": [{"id": key, **value} for key, value in FAMILIES.items()],
        "frames": frames, "icons": icons,
        "notes": "Source concepts only; no runtime/catalog integration, labels, or accessibility text.",
    }
    (OUT / "frames.json").write_text(json.dumps(manifest, indent=2) + "\n")


def build() -> None:
    (OUT / "buttons").mkdir(exist_ok=True)
    (OUT / "icons").mkdir(exist_ok=True)
    for family in FAMILIES:
        for state in STATES:
            make_button(family, state).save(OUT / "buttons" / f"{family}-{state}.png")
            make_icon(family, state).save(OUT / "icons" / f"{family}-{state}.png")

    # One atlas per family keeps each state aligned for runtime inspection.
    for family in FAMILIES:
        atlas = Image.new("RGBA", (BUTTON_W * 4, BUTTON_H), (0, 0, 0, 0))
        for index, state in enumerate(STATES):
            atlas.alpha_composite(make_button(family, state), (index * BUTTON_W, 0))
        atlas.save(OUT / f"{family}-states-atlas.png")

    montage = Image.new("RGBA", (BUTTON_W * 3 + 24, (BUTTON_H + 16) * len(FAMILIES) // 3 + 16), (28, 20, 40, 255))
    for i, family in enumerate(FAMILIES):
        row, col = divmod(i, 3)
        x, y = 12 + col * BUTTON_W, 8 + row * (BUTTON_H + 16)
        for state_index, state in enumerate(STATES):
            # Fit all four states into each family row while retaining hard edges.
            thumb = make_button(family, state).resize((BUTTON_W // 2, BUTTON_H // 2), Image.Resampling.NEAREST)
            montage.alpha_composite(thumb, (x + (state_index % 2) * (BUTTON_W // 2), y + (state_index // 2) * (BUTTON_H // 2)))
    montage = montage.resize((montage.width * 2, montage.height * 2), Image.Resampling.NEAREST)
    montage.save(OUT / "button-states-preview-2x.png")
    write_manifest()


if __name__ == "__main__":
    build()
