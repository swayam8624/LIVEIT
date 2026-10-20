#!/usr/bin/env python3
"""Generate original, text-free pixel conversation UI assets.

Every mark is drawn from integer rectangles and polygons with the palette below.
Run with the repository's bundled Pillow runtime:
  python3 generate_assets.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
PALETTE = {
    "clear": (0, 0, 0, 0),
    "ink": (35, 31, 47, 255),
    "ink_soft": (60, 54, 74, 255),
    "paper": (255, 245, 218, 255),
    "paper_hi": (255, 251, 232, 255),
    "paper_shadow": (221, 191, 149, 255),
    "lavender": (165, 144, 206, 255),
    "lavender_hi": (216, 197, 238, 255),
    "teal": (56, 163, 154, 255),
    "teal_hi": (119, 220, 194, 255),
    "rose": (221, 122, 145, 255),
    "rose_hi": (247, 174, 174, 255),
    "gold": (243, 193, 83, 255),
    "muted": (143, 137, 153, 255),
    "disabled": (102, 96, 110, 255),
    "danger": (197, 78, 91, 255),
    "safe": (75, 170, 117, 255),
}

def rgba(name: str):
    return PALETTE[name]

def canvas(w: int, h: int) -> Image.Image:
    return Image.new("RGBA", (w, h), rgba("clear"))

def rect(d: ImageDraw.ImageDraw, xy, fill: str, outline: str | None = None, width: int = 1):
    d.rectangle(xy, fill=rgba(fill), outline=rgba(outline) if outline else None, width=width)

def save(im: Image.Image, rel: str):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)

def checker(im: Image.Image, x0: int, y0: int, x1: int, y1: int, color: str):
    d = ImageDraw.Draw(im)
    for y in range(y0, y1 + 1, 4):
        for x in range(x0, x1 + 1, 4):
            if ((x - x0) // 4 + (y - y0) // 4) % 2 == 0:
                rect(d, (x, y, min(x + 3, x1), min(y + 3, y1)), color)

def slice_panel(w: int, h: int, theme: str, radius: int = 6) -> Image.Image:
    im = canvas(w, h)
    d = ImageDraw.Draw(im)
    fill = "paper" if theme == "incoming" else "lavender" if theme == "outgoing" else "ink_soft"
    hi = "paper_hi" if theme == "incoming" else "lavender_hi" if theme == "outgoing" else "muted"
    shadow = "paper_shadow" if theme == "incoming" else "lavender" if theme == "outgoing" else "ink"
    # Pixel stepped corners, with no antialiasing.
    rect(d, (radius, 0, w - radius - 1, h - 1), fill)
    rect(d, (0, radius, w - 1, h - radius - 1), fill)
    rect(d, (radius // 2, radius // 2, w - radius // 2 - 1, h - radius // 2 - 1), fill)
    rect(d, (radius, 0, w - radius - 1, 2), hi)
    rect(d, (0, radius, 2, h - radius - 1), hi)
    rect(d, (radius, h - 3, w - radius - 1, h - 1), shadow)
    rect(d, (w - 3, radius, w - 1, h - radius - 1), shadow)
    return im

def make_slice_tiles():
    for name, theme in (("incoming", "incoming"), ("outgoing", "outgoing"), ("system", "system"), ("panel", "outgoing")):
        # A 48px source has a 16px border; runtime may repeat the 16px center.
        im = slice_panel(48, 48, theme, 8)
        save(im, f"nine-slice/{name}-slice-48x48.png")

def make_bubble_surfaces():
    for name, theme, tail_side in (("incoming", "incoming", "left"), ("outgoing", "outgoing", "right"), ("system", "system", "none")):
        im = slice_panel(128, 56, theme, 8)
        d = ImageDraw.Draw(im)
        if tail_side == "left":
            rect(d, (0, 40, 7, 47), "paper")
            rect(d, (0, 47, 3, 51), "paper")
            rect(d, (3, 48, 6, 54), "paper_shadow")
        elif tail_side == "right":
            rect(d, (120, 40, 127, 47), "lavender")
            rect(d, (124, 47, 127, 51), "lavender")
            rect(d, (121, 48, 124, 54), "lavender")
        else:
            rect(d, (8, 5, 119, 7), "muted")
            rect(d, (8, 48, 119, 50), "ink")
        save(im, f"surfaces/{name}-bubble-128x56.png")

def make_typing():
    im = canvas(64, 24)
    d = ImageDraw.Draw(im)
    # Three frames, each 20x24, animated by atlas metadata.
    for frame in range(3):
        ox = frame * 21
        rect(d, (ox + 3, 2, ox + 17, 20), "paper")
        for i in range(3):
            yy = 10 + (2 if (i + frame) % 3 == 0 else 0)
            rect(d, (ox + 6 + i * 4, yy, ox + 8 + i * 4, yy + 2), "teal" if i == frame else "lavender")
    save(im, "indicators/typing-dots-3x-21x24-atlas.png")

def make_badges():
    im = canvas(96, 24)
    d = ImageDraw.Draw(im)
    for i, col in enumerate(("rose", "gold", "teal", "muted")):
        ox = i * 24
        rect(d, (ox + 3, 3, ox + 20, 20), col)
        rect(d, (ox + 6, 6, ox + 17, 17), "ink")
        if i == 0:
            rect(d, (ox + 11, 8, ox + 13, 15), col)
            rect(d, (ox + 11, 17, ox + 13, 18), col)
        elif i == 1:
            rect(d, (ox + 9, 11, ox + 14, 13), col)
        elif i == 2:
            rect(d, (ox + 9, 10, ox + 14, 15), col)
        else:
            rect(d, (ox + 9, 10, ox + 14, 15), col)
    save(im, "badges/unread-notification-4x24-atlas.png")

def make_avatar_frames():
    im = canvas(192, 48)
    d = ImageDraw.Draw(im)
    states = (("neutral", "teal", "paper"), ("focus", "gold", "paper_hi"), ("pressed", "rose", "lavender_hi"), ("disabled", "muted", "disabled"))
    for i, (_, border, inner) in enumerate(states):
        ox = i * 48
        rect(d, (ox + 4, 4, ox + 43, 43), border)
        rect(d, (ox + 8, 8, ox + 39, 39), inner)
        rect(d, (ox + 14, 14, ox + 33, 33), "ink_soft" if i != 3 else "ink")
        rect(d, (ox + 18, 18, ox + 20, 20), "paper_hi" if i != 3 else "muted")
        rect(d, (ox + 27, 18, ox + 29, 20), "paper_hi" if i != 3 else "muted")
        rect(d, (ox + 19, 27, ox + 28, 29), "rose" if i != 3 else "disabled")
    save(im, "avatars/avatar-frame-states-4x48-atlas.png")

def make_symbols():
    im = canvas(96, 24)
    d = ImageDraw.Draw(im)
    # consent-safe, muted, blocked, system info symbols; no text.
    for i, col in enumerate(("safe", "muted", "danger", "teal")):
        ox = i * 24
        rect(d, (ox + 4, 4, ox + 19, 19), col)
        if i == 0:  # shield
            d.polygon([(ox + 8, 7), (ox + 16, 7), (ox + 18, 11), (ox + 15, 17), (ox + 12, 19), (ox + 9, 17), (ox + 6, 11)], fill=rgba("paper_hi"))
            rect(d, (ox + 10, 12, ox + 12, 14), col)
            rect(d, (ox + 13, 10, ox + 15, 12), col)
        elif i == 1:  # muted speaker
            rect(d, (ox + 7, 10, ox + 10, 14), "paper_hi")
            d.polygon([(ox + 10, 10), (ox + 15, 7), (ox + 15, 17), (ox + 10, 14)], fill=rgba("paper_hi"))
            rect(d, (ox + 16, 8, ox + 17, 16), col)
        elif i == 2:  # blocked slash
            rect(d, (ox + 6, 11, ox + 17, 13), "paper_hi")
            d.line([(ox + 7, 17), (ox + 17, 7)], fill=rgba("paper_hi"), width=2)
        else:  # info star
            rect(d, (ox + 11, 7, ox + 13, 16), "paper_hi")
            rect(d, (ox + 9, 11, ox + 15, 13), "paper_hi")
            rect(d, (ox + 11, 17, ox + 13, 18), "paper_hi")
    save(im, "symbols/notification-symbols-4x24-atlas.png")

def button_frame(state: str) -> Image.Image:
    im = canvas(32, 32)
    d = ImageDraw.Draw(im)
    border, fill, glyph = {"neutral": ("teal", "ink_soft", "paper_hi"), "focus": ("gold", "ink_soft", "paper_hi"), "pressed": ("rose", "ink", "paper_hi"), "disabled": ("disabled", "ink_soft", "muted")} [state]
    rect(d, (3, 3, 28, 28), border)
    rect(d, (6, 6, 25, 25), fill)
    # Send glyph: a simple arrow/plane made of pixel blocks.
    d.polygon([(10, 15), (22, 10), (18, 21), (15, 17), (10, 18)], fill=rgba(glyph))
    rect(d, (10, 15, 17, 17), glyph)
    return im

def make_controls():
    states = ("neutral", "focus", "pressed", "disabled")
    atlas = canvas(128, 32)
    for i, state in enumerate(states):
        atlas.alpha_composite(button_frame(state), (i * 32, 0))
    save(atlas, "controls/send-button-states-4x32-atlas.png")
    # Compact icon controls retain the same state ordering and dimensions.
    for name, glyph in (("reply", "rose"), ("close", "muted"), ("consent", "safe")):
        atlas = canvas(128, 32)
        for i, state in enumerate(states):
            im = button_frame(state)
            d = ImageDraw.Draw(im)
            col = rgba(glyph if state != "disabled" else "disabled")
            if name == "reply":
                d.line([(20, 11), (12, 16), (20, 21)], fill=col, width=2)
                rect(d, (14, 15, 22, 17), glyph if state != "disabled" else "disabled")
            elif name == "close":
                d.line([(12, 12), (20, 20)], fill=col, width=2)
                d.line([(20, 12), (12, 20)], fill=col, width=2)
            else:
                d.line([(11, 17), (15, 21), (22, 11)], fill=col, width=2)
            atlas.alpha_composite(im, (i * 32, 0))
        save(atlas, f"controls/{name}-button-states-4x32-atlas.png")

def make_preview():
    """Make a nearest-neighbor board for human review; it contains no text."""
    im = canvas(512, 320)
    d = ImageDraw.Draw(im)
    # A muted checkerboard makes transparent edges visible in review.
    for y in range(0, 320, 8):
        for x in range(0, 512, 8):
            rect(d, (x, y, x + 7, y + 7), "ink" if ((x // 8 + y // 8) % 2) else "ink_soft")
    tiles = [
        ("surfaces/incoming-bubble-128x56.png", (16, 16), 2),
        ("surfaces/outgoing-bubble-128x56.png", (272, 16), 2),
        ("surfaces/system-bubble-128x56.png", (16, 144), 2),
        ("avatars/avatar-frame-states-4x48-atlas.png", (272, 128), 2),
        ("controls/send-button-states-4x32-atlas.png", (16, 256), 3),
        ("symbols/notification-symbols-4x24-atlas.png", (272, 240), 3),
    ]
    for rel, pos, scale in tiles:
        src = Image.open(ROOT / rel).convert("RGBA")
        src = src.resize((src.width * scale, src.height * scale), Image.Resampling.NEAREST)
        im.alpha_composite(src, pos)
    save(im, "conversation-ui-preview-2x.png")

def main():
    make_slice_tiles()
    make_bubble_surfaces()
    make_typing()
    make_badges()
    make_avatar_frames()
    make_symbols()
    make_controls()
    make_preview()

    records = []
    for path in sorted(ROOT.rglob("*.png")):
        with Image.open(path) as im:
            records.append({"file": path.relative_to(ROOT).as_posix(), "width": im.width, "height": im.height, "mode": im.mode, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "runtimeReady": False})
    manifest = {
        "schema": "liveit.pixel.conversation-ui.v2",
        "title": "Conversation and social UI sprite kit",
        "runtimeReady": False,
        "license": "CC0-equivalent original procedural artwork by LIVEIT project",
        "sourcePolicy": "No archive, third-party, or reference image bytes used.",
        "textPolicy": "All dynamic text is intentionally excluded from images.",
        "nineSlice": {
            "sourceSize": [48, 48], "insets": {"left": 16, "top": 16, "right": 16, "bottom": 16},
            "centerMode": "repeat", "tileFiles": ["nine-slice/incoming-slice-48x48.png", "nine-slice/outgoing-slice-48x48.png", "nine-slice/system-slice-48x48.png", "nine-slice/panel-slice-48x48.png"]
        },
        "atlasConventions": {"origin": "top-left", "integerPixels": True, "nearestNeighbor": True, "stateOrder": ["neutral", "focus", "pressed", "disabled"]},
        "files": records,
        "runtimeIntegration": "Concept-only package. Requires renderer import, pixel-scale review, and accessibility/state wiring before runtimeReady can change."
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    provenance = {
        "artwork": "Procedural integer-pixel geometry authored for LIVEIT; generated by generate_assets.py.",
        "generator": "generate_assets.py",
        "palette": PALETTE,
        "inputs": [],
        "externalAssets": False,
        "prompts": [],
        "transformations": ["None; all files are direct generator outputs."],
        "reviewNotes": ["No dynamic text in images.", "Nine-slice source tiles use 16px insets.", "All PNGs are RGBA and runtimeReady remains false."]
    }
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(records)} PNGs")

if __name__ == "__main__":
    main()
