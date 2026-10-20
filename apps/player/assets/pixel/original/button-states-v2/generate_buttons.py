"""Build the original tactile button-states-v2 concept batch.

Only integer geometry and a fixed local palette are used.  The text-safe
middle of each plate is intentionally empty; the game can place localized
labels at runtime without baking language into the art.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).parent
BUTTON_W, BUTTON_H = 192, 56
ICON_SIZE = 32
INSET = 10
STATES = ("normal", "focused", "pressed", "disabled")

P = {
    "void": (24, 18, 38, 255),
    "ink": (46, 31, 62, 255),
    "ink_hi": (80, 58, 86, 255),
    "teal": (40, 133, 130, 255),
    "teal_hi": (103, 207, 177, 255),
    "blue": (52, 113, 170, 255),
    "blue_hi": (129, 195, 226, 255),
    "gold": (214, 157, 48, 255),
    "gold_hi": (255, 220, 116, 255),
    "coral": (203, 75, 80, 255),
    "coral_hi": (255, 143, 125, 255),
    "plum": (107, 58, 112, 255),
    "plum_hi": (213, 127, 202, 255),
    "slate": (104, 105, 125, 255),
    "slate_hi": (170, 172, 182, 255),
    "paper": (255, 245, 207, 255),
    "shadow": (14, 11, 24, 255),
    "clear": (0, 0, 0, 0),
}

FAMILIES = {
    "primary": {"label": "confirm / continue", "base": "teal", "accent": "teal_hi", "icon": "chevron", "shape": "ribbon"},
    "secondary": {"label": "open / inspect", "base": "blue", "accent": "blue_hi", "icon": "inspect", "shape": "tab"},
    "choice": {"label": "story choice", "base": "gold", "accent": "gold_hi", "icon": "branch", "shape": "diamond"},
    "danger": {"label": "cancel / leave", "base": "coral", "accent": "coral_hi", "icon": "cross", "shape": "notch"},
    "phone": {"label": "phone / messages", "base": "plum", "accent": "plum_hi", "icon": "phone", "shape": "ticket"},
    "utility": {"label": "settings / utility", "base": "ink_hi", "accent": "teal_hi", "icon": "gear", "shape": "square"},
}


def rgba(name: str) -> tuple[int, int, int, int]:
    return P[name]


def shifted(c: tuple[int, int, int, int], amount: int) -> tuple[int, int, int, int]:
    return tuple(max(0, min(255, n + amount)) for n in c[:3]) + (255,)


def stepped_polygon(x0: int, y0: int, x1: int, y1: int, step: int = 6):
    return [(x0 + step, y0), (x1 - step, y0), (x1, y0 + step),
            (x1, y1 - step), (x1 - step, y1), (x0 + step, y1),
            (x0, y1 - step), (x0, y0 + step)]


def plate(draw: ImageDraw.ImageDraw, family: str, state: str) -> None:
    spec = FAMILIES[family]
    base = rgba(spec["base"])
    accent = rgba(spec["accent"])
    if state == "disabled":
        base, accent = rgba("slate"), rgba("slate_hi")
    if state == "pressed":
        base = shifted(base, -24)
    # Shadow is offset so the pressed state can sit visually into the surface.
    shadow_y = 5 if state != "pressed" else 2
    draw.polygon(stepped_polygon(2, shadow_y, BUTTON_W - 2, BUTTON_H + shadow_y - 4, 7), fill=rgba("shadow"))
    border = rgba("void") if state != "focused" else accent
    draw.polygon(stepped_polygon(0, 0, BUTTON_W - 1, BUTTON_H - 5, 7), fill=border)
    draw.polygon(stepped_polygon(5, 5, BUTTON_W - 6, BUTTON_H - 10, 4), fill=base)
    # Crisp top and left bevel; deliberately kept outside the text-safe center.
    bevel = rgba("paper") if state != "disabled" else shifted(accent, -28)
    draw.line((13, 8, BUTTON_W - 14, 8), fill=bevel, width=2)
    draw.line((9, 12, 9, BUTTON_H - 17), fill=bevel, width=2)
    draw.line((13, BUTTON_H - 14, BUTTON_W - 14, BUTTON_H - 14), fill=shifted(rgba("void"), -2), width=2)
    if state == "focused":
        draw.rectangle((INSET, 12, BUTTON_W - INSET - 1, BUTTON_H - 18), outline=rgba("paper"), width=2)
        draw.rectangle((INSET + 4, 16, BUTTON_W - INSET - 5, BUTTON_H - 22), outline=accent, width=1)
    elif state == "pressed":
        draw.line((13, 11, BUTTON_W - 14, 11), fill=shifted(base, 28), width=2)
        draw.line((13, BUTTON_H - 16, BUTTON_W - 14, BUTTON_H - 16), fill=rgba("shadow"), width=2)
    # A family-specific corner marker gives a clear surface silhouette while
    # leaving the central label area empty.
    marker = accent
    if spec["shape"] == "ribbon":
        draw.polygon([(BUTTON_W - 31, 5), (BUTTON_W - 11, 5), (BUTTON_W - 18, 14), (BUTTON_W - 31, 14)], fill=marker)
    elif spec["shape"] == "tab":
        draw.rectangle((BUTTON_W - 27, 5, BUTTON_W - 11, 13), fill=marker)
    elif spec["shape"] == "diamond":
        draw.polygon([(BUTTON_W - 21, 5), (BUTTON_W - 11, 14), (BUTTON_W - 21, 23), (BUTTON_W - 31, 14)], fill=marker)
    elif spec["shape"] == "notch":
        draw.polygon([(BUTTON_W - 31, 5), (BUTTON_W - 11, 5), (BUTTON_W - 11, 14), (BUTTON_W - 22, 14)], fill=marker)
    elif spec["shape"] == "ticket":
        draw.rectangle((BUTTON_W - 30, 6, BUTTON_W - 11, 14), fill=marker)
        draw.rectangle((BUTTON_W - 27, 7, BUTTON_W - 24, 13), fill=base)
    else:
        draw.rectangle((BUTTON_W - 28, 6, BUTTON_W - 12, 14), fill=marker)
    # The 24px-wide center strip is an intentional no-text / no-icon safe zone.
    draw.rectangle((BUTTON_W // 2 - 12, 5, BUTTON_W // 2 + 12, 7), fill=shifted(base, 10))


def icon(draw: ImageDraw.ImageDraw, kind: str, color, state: str) -> None:
    c = rgba("slate_hi") if state == "disabled" else color
    if kind == "chevron":
        draw.rectangle((4, 14, 17, 17), fill=c)
        draw.polygon([(15, 7), (25, 15), (15, 23)], fill=c)
    elif kind == "inspect":
        draw.ellipse((4, 4, 21, 21), outline=c, width=3)
        draw.line((18, 18, 27, 27), fill=c, width=4)
        draw.rectangle((9, 11, 16, 14), fill=c)
    elif kind == "branch":
        draw.rectangle((14, 4, 17, 26), fill=c)
        draw.rectangle((7, 4, 16, 7), fill=c)
        draw.rectangle((7, 4, 10, 15), fill=c)
        draw.rectangle((16, 23, 25, 26), fill=c)
        draw.rectangle((22, 17, 25, 25), fill=c)
        draw.rectangle((7, 13, 16, 16), fill=c)
    elif kind == "cross":
        draw.rectangle((5, 13, 27, 17), fill=c)
        draw.rectangle((13, 5, 17, 25), fill=c)
    elif kind == "phone":
        draw.rectangle((7, 4, 25, 27), fill=c)
        draw.rectangle((10, 8, 22, 22), fill=rgba("ink"))
        draw.rectangle((14, 24, 18, 26), fill=rgba("ink"))
        draw.rectangle((13, 10, 19, 13), fill=c)
        draw.rectangle((11, 15, 21, 18), fill=c)
    elif kind == "gear":
        draw.rectangle((12, 3, 20, 29), fill=c)
        draw.rectangle((3, 12, 29, 20), fill=c)
        draw.rectangle((8, 8, 24, 24), fill=c)
        draw.rectangle((13, 13, 19, 19), fill=rgba("ink"))


def make_button(family: str, state: str) -> Image.Image:
    image = Image.new("RGBA", (BUTTON_W, BUTTON_H), rgba("clear"))
    plate(ImageDraw.Draw(image), family, state)
    return image


def make_icon(family: str, state: str) -> Image.Image:
    image = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), rgba("clear"))
    icon(ImageDraw.Draw(image), FAMILIES[family]["icon"], rgba(FAMILIES[family]["accent"]), state)
    return image


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> None:
    buttons = ROOT / "buttons"
    icons = ROOT / "icons"
    buttons.mkdir(exist_ok=True)
    icons.mkdir(exist_ok=True)
    frames, icon_frames = [], []
    for family in FAMILIES:
        atlas = Image.new("RGBA", (BUTTON_W * 4, BUTTON_H), rgba("clear"))
        for i, state in enumerate(STATES):
            button_path = buttons / f"{family}-{state}.png"
            icon_path = icons / f"{family}-{state}.png"
            make_button(family, state).save(button_path)
            make_icon(family, state).save(icon_path)
            atlas.alpha_composite(Image.open(button_path), (i * BUTTON_W, 0))
            frame = {"id": f"{family}-{state}", "file": f"buttons/{family}-{state}.png", "family": family, "state": state, "width": BUTTON_W, "height": BUTTON_H, "x": 0, "y": 0, "iconFile": f"icons/{family}-{state}.png", "nineSliceInsets": {"left": INSET, "top": INSET, "right": INSET, "bottom": INSET}, "sampling": "nearest", "textSafeRect": [40, 10, 151, 45], "sha256": sha(button_path), "runtimeReady": False}
            frames.append(frame)
            icon_frames.append({"id": f"{family}-{state}-icon", "file": f"icons/{family}-{state}.png", "family": family, "state": state, "width": ICON_SIZE, "height": ICON_SIZE, "sampling": "nearest", "sha256": sha(icon_path), "runtimeReady": False})
        atlas.save(ROOT / f"{family}-states-atlas.png")

    montage = Image.new("RGBA", (BUTTON_W * 2 + 32, (BUTTON_H + 20) * 3 + 24), rgba("void"))
    for i, family in enumerate(FAMILIES):
        row, col = divmod(i, 2)
        x, y = 16 + col * BUTTON_W, 8 + row * (BUTTON_H + 20)
        for j, state in enumerate(STATES):
            thumb = make_button(family, state).resize((BUTTON_W // 2, BUTTON_H // 2), Image.Resampling.NEAREST)
            montage.alpha_composite(thumb, (x + (j % 2) * (BUTTON_W // 2), y + (j // 2) * (BUTTON_H // 2)))
    montage.resize((montage.width * 2, montage.height * 2), Image.Resampling.NEAREST).save(ROOT / "button-states-preview-2x.png")

    manifest = {"batch": "button-states-v2", "runtimeReady": False, "pixelArt": True, "sampling": "nearest", "buttonSize": [BUTTON_W, BUTTON_H], "iconSize": [ICON_SIZE, ICON_SIZE], "nineSliceInsets": {"left": INSET, "top": INSET, "right": INSET, "bottom": INSET}, "states": list(STATES), "families": [{"id": key, **spec} for key, spec in FAMILIES.items()], "frames": frames, "icons": icon_frames, "source": "generate_buttons.py", "notes": "Original concept plates with empty text-safe center; runtime labels and accessibility text remain external."}
    (ROOT / "frames.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    build()
