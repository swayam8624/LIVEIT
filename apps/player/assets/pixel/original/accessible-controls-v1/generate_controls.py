#!/usr/bin/env python3
"""Generate original text-free pixel controls with deterministic Pillow primitives."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
CELL = (64, 48)
INK = (43, 32, 55, 255)
PAPER = (247, 231, 192, 255)
TEAL = (63, 158, 145, 255)
TEAL_HI = (137, 217, 190, 255)
GOLD = (230, 183, 83, 255)
CORAL = (220, 111, 101, 255)
PLUM = (117, 79, 117, 255)
SLATE = (105, 105, 119, 255)
FAINT = (171, 162, 150, 255)
TRANSPARENT = (0, 0, 0, 0)

# States have distinct visual meaning per widget.  Focus is a visible frame,
# not a substitute for the platform's semantic accessibility focus indicator.
FAMILIES = [
    ("checkbox", "choice", ["unchecked", "checked", "focused", "disabled", "error"]),
    ("switch", "setting", ["off", "on", "focused", "disabled", "loading"]),
    ("radio", "choice", ["unselected", "selected", "focused", "disabled", "error"]),
    ("slider", "setting", ["normal", "focused", "pressed", "disabled", "error"]),
    ("tab", "navigation", ["idle", "selected", "focused", "disabled", "loading"]),
    ("segment", "navigation", ["idle", "selected", "focused", "disabled"]),
    ("disclosure", "navigation", ["closed", "open", "focused", "disabled", "error"]),
    ("settings-key", "setting", ["normal", "selected", "focused", "disabled", "loading", "error"]),
    ("phone-key", "phone", ["normal", "selected", "focused", "disabled", "loading", "error"]),
    ("map-key", "navigation", ["normal", "selected", "focused", "disabled", "loading", "error"]),
]


def box(draw, xy, fill, outline=INK, width=2):
    draw.rectangle(xy, fill=fill, outline=outline, width=width)


def focus(draw):
    # Broken-corner gold brackets remain visible around the widget silhouette.
    c = GOLD
    for x, y, sx, sy in [(5, 5, 1, 1), (58, 5, -1, 1), (5, 42, 1, -1), (58, 42, -1, -1)]:
        draw.rectangle((min(x, x + sx * 6), min(y, y + sy * 2), max(x, x + sx * 6), max(y, y + sy * 2)), fill=c)
        draw.rectangle((min(x, x + sx * 2), min(y, y + sy * 6), max(x, x + sx * 2), max(y, y + sy * 6)), fill=c)


def spinner(draw, cx=32, cy=24):
    for i, (dx, dy) in enumerate([(0, -9), (6, -6), (9, 0), (6, 6), (0, 9), (-6, 6), (-9, 0), (-6, -6)]):
        col = TEAL_HI if i < 3 else TEAL
        draw.rectangle((cx + dx - 1, cy + dy - 1, cx + dx + 1, cy + dy + 1), fill=col)


def symbol(draw, family, state):
    col = SLATE if state == "disabled" else (CORAL if state == "error" else TEAL)
    if family == "checkbox":
        box(draw, (19, 11, 44, 36), PAPER if state != "disabled" else FAINT, col, 3)
        if state == "checked":
            draw.line((24, 24, 29, 29, 39, 17), fill=INK, width=4)
            draw.point((40, 17), fill=INK)
        elif state == "error":
            draw.rectangle((29, 17, 33, 27), fill=CORAL)
            draw.rectangle((29, 30, 33, 34), fill=CORAL)
    elif family == "switch":
        box(draw, (13, 14, 50, 33), SLATE if state == "disabled" else (TEAL if state == "on" else PLUM), col, 2)
        x = 39 if state == "on" else 23
        draw.rectangle((x - 6, 17, x + 3, 30), fill=PAPER, outline=INK, width=2)
        if state == "loading":
            spinner(draw, 32, 24)
    elif family == "radio":
        draw.ellipse((20, 10, 44, 34), fill=PAPER if state != "disabled" else FAINT, outline=col, width=3)
        if state == "selected":
            draw.rectangle((27, 17, 37, 27), fill=INK)
        elif state == "error":
            draw.rectangle((29, 15, 35, 30), fill=CORAL)
            draw.rectangle((24, 20, 40, 25), fill=CORAL)
    elif family == "slider":
        draw.rectangle((13, 22, 50, 26), fill=FAINT)
        draw.rectangle((13, 22, 34, 26), fill=SLATE if state == "disabled" else TEAL)
        x = 34 if state != "error" else 46
        draw.rectangle((x - 5, 15, x + 5, 33), fill=PAPER, outline=CORAL if state == "error" else col, width=3)
        if state == "pressed":
            draw.rectangle((x - 2, 18, x + 2, 30), fill=GOLD)
    elif family == "tab":
        box(draw, (12, 12, 51, 34), PLUM if state == "disabled" else (TEAL if state == "selected" else PAPER), col, 2)
        draw.rectangle((18, 18, 45, 20), fill=INK if state != "disabled" else FAINT)
        draw.rectangle((18, 24, 37, 26), fill=INK if state != "disabled" else FAINT)
        if state == "selected":
            draw.rectangle((18, 31, 45, 34), fill=GOLD)
        if state == "loading":
            spinner(draw, 32, 24)
    elif family == "segment":
        box(draw, (10, 15, 53, 32), PAPER if state != "disabled" else FAINT, col, 2)
        draw.rectangle((11, 16, 31, 31), fill=TEAL if state == "selected" else PAPER)
        draw.line((32, 16, 32, 31), fill=INK, width=2)
        draw.rectangle((17, 22, 25, 25), fill=INK)
        draw.rectangle((38, 22, 46, 25), fill=INK)
    elif family == "disclosure":
        box(draw, (17, 9, 47, 38), PAPER if state != "disabled" else FAINT, col, 2)
        if state == "open":
            draw.polygon([(24, 18), (40, 18), (32, 29)], fill=INK)
        else:
            draw.polygon([(25, 15), (38, 24), (25, 33)], fill=INK)
        if state == "error":
            draw.rectangle((43, 7, 48, 12), fill=CORAL)
    elif family in ("settings-key", "phone-key", "map-key"):
        box(draw, (16, 8, 48, 40), PLUM if state == "disabled" else PAPER, col, 2)
        if family == "phone-key":
            phone_color = SLATE if state == "disabled" else INK
            draw.line((24, 14, 27, 11, 32, 17, 29, 20, 34, 27, 37, 24, 43, 29, 40, 33), fill=phone_color, width=4)
            draw.line((24, 14, 21, 19, 23, 24, 29, 30, 34, 33, 40, 33), fill=phone_color, width=3)
        elif family == "map-key":
            draw.polygon([(21, 14), (29, 11), (37, 14), (43, 11), (43, 32), (36, 35), (29, 32), (21, 35)], fill=TEAL if state != "disabled" else SLATE, outline=INK)
            draw.line((29, 12, 29, 32), fill=INK, width=2)
            draw.line((37, 14, 37, 34), fill=INK, width=2)
            draw.ellipse((32, 17, 36, 21), fill=GOLD)
        else:
            cog = SLATE if state == "disabled" else TEAL
            draw.ellipse((25, 15, 39, 29), fill=cog, outline=INK, width=2)
            draw.ellipse((29, 19, 35, 25), fill=PAPER)
            for x, y in [(30, 11), (30, 29), (21, 20), (39, 20)]:
                draw.rectangle((x, y, x + 4, y + 4), fill=cog)
        if state == "loading":
            spinner(draw, 32, 24)
        elif state == "error":
            draw.rectangle((30, 14, 34, 27), fill=CORAL)
            draw.rectangle((30, 31, 34, 35), fill=CORAL)


def render(family, state):
    im = Image.new("RGBA", CELL, TRANSPARENT)
    d = ImageDraw.Draw(im)
    symbol(d, family, state)
    if state == "focused":
        focus(d)
    return im


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    (ROOT / "controls").mkdir(exist_ok=True)
    records = []
    tiles = []
    for family, category, states in FAMILIES:
        row = []
        for state in states:
            im = render(family, state)
            rel = f"controls/{family}-{state}.png"
            target = ROOT / rel
            im.save(target, optimize=True)
            records.append({
                "id": f"accessible-{family}-{state}", "family": family,
                "category": category, "state": state, "file": rel,
                "width": CELL[0], "height": CELL[1], "mode": "RGBA",
                "sha256": digest(target), "sampling": "nearest",
                "runtimeReady": False,
                "labelPolicy": "Render localized visible label and accessible name as real text outside the image."
            })
            row.append(im)
        tiles.append((family, row))

    manifest = {
        "batch": "accessible-controls-v1", "runtimeReady": False,
        "pixelArt": True, "sampling": "nearest", "cellSize": list(CELL),
        "families": [{"id": f, "category": c, "states": s} for f, c, s in FAMILIES],
        "frames": records,
        "accessibility": {
            "dynamicText": True,
            "visibleFocus": "Gold corner brackets are a visual concept and do not replace platform focus semantics.",
            "disabled": "Disabled appearance must be paired with real disabled semantics and an explanation where needed.",
            "contrast": "Color, shape, and state marks are redundant cues; contrast acceptance remains untested."
        },
        "notes": "Concept art only. PNG state glyphs do not implement control behavior, labels, focus order, input method support, or accessibility APIs."
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    # Labeled preview board is review-only; labels live in preview metadata here,
    # never in individual runtime-style sprites.
    cols = 6
    rows = sum((len(s) + cols - 1) // cols for _, _, s in FAMILIES)
    board = Image.new("RGBA", (cols * 80, rows * 68), (35, 29, 47, 255))
    bd = ImageDraw.Draw(board)
    # Use a built-in bitmap font only on the review sheet, not delivered controls.
    try:
        from PIL import ImageFont
        font = ImageFont.load_default()
    except Exception:
        font = None
    y = 0
    for family, row in tiles:
        for idx, im in enumerate(row):
            x = (idx % cols) * 80
            yy = y + (idx // cols) * 68
            board.alpha_composite(im, (x + 8, yy + 2))
            if font:
                bd.text((x + 3, yy + 51), FAMILIES[[f for f, _, _ in FAMILIES].index(family)][2][idx][:9], fill=PAPER, font=font)
        y += ((len(row) + cols - 1) // cols) * 68
    board = board.resize((board.width * 3, board.height * 3), Image.Resampling.NEAREST)
    board.save(ROOT / "accessible-controls-preview-3x.png", optimize=True)

    pngs = [p for p in ROOT.rglob("*.png")]
    provenance = {
        "batch": "accessible-controls-v1",
        "created": "2026-10-20",
        "method": "Original integer-coordinate Pillow drawing primitives from generate_controls.py; no image generation model, downloaded or supplied art, third-party glyphs, logos, or external fonts used.",
        "rights": "Original locally authored concept artwork; no third-party source material or license is claimed.",
        "runtimeReady": False,
        "files": [{"file": p.relative_to(ROOT).as_posix(), "width": Image.open(p).width, "height": Image.open(p).height, "mode": Image.open(p).mode, "sha256": digest(p)} for p in sorted(pngs)]
    }
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")


if __name__ == "__main__":
    main()
