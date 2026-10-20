#!/usr/bin/env python3
"""Create the original HUD panel source batch with only the Python standard library.

The output is intentionally deterministic: every panel is assembled from integer
pixel rectangles and a small fixed palette.  This keeps the source auditable on
machines without an image authoring package installed.
"""

from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path


OUT = Path(__file__).parent
SCALE = 1
P = {
    "transparent": (0, 0, 0, 0),
    "plum": (43, 27, 55, 255),
    "plum_dark": (28, 18, 38, 255),
    "ink": (72, 44, 69, 255),
    "cream": (247, 222, 164, 255),
    "cream_hi": (255, 239, 193, 255),
    "teal": (70, 139, 135, 255),
    "teal_dark": (39, 91, 97, 255),
    "gold": (225, 166, 70, 255),
    "coral": (202, 88, 91, 255),
    "slate": (116, 123, 137, 255),
    "slate_dark": (79, 84, 101, 255),
    "mint": (150, 208, 169, 255),
}


class Canvas:
    def __init__(self, w: int, h: int):
        self.w, self.h = w, h
        self.px = [[P["transparent"] for _ in range(w)] for _ in range(h)]

    def rect(self, x0, y0, x1, y1, color):
        color = P[color] if isinstance(color, str) else color
        for y in range(max(0, y0), min(self.h, y1)):
            for x in range(max(0, x0), min(self.w, x1)):
                self.px[y][x] = color

    def line(self, points, color):
        color = P[color] if isinstance(color, str) else color
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            if x0 == x1:
                self.rect(x0, min(y0, y1), x0 + 1, max(y0, y1) + 1, color)
            elif y0 == y1:
                self.rect(min(x0, x1), y0, max(x0, x1) + 1, y0 + 1, color)


def png_bytes(c: Canvas) -> bytes:
    raw = b"".join(b"\x00" + b"".join(bytes(px) for px in row) for row in c.px)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", c.w, c.h, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")


def save(c, name):
    (OUT / name).write_bytes(png_bytes(c))


def panel(w, h, fill="cream", accent="teal", corner=8, trim=True):
    c = Canvas(w, h)
    c.rect(0, 0, w, h, "plum_dark")
    c.rect(2, 2, w - 2, h - 2, "plum")
    c.rect(4, 4, w - 4, h - 4, fill)
    c.rect(6, 6, w - 6, h - 6, fill)
    c.rect(4, 4, w - 4, 7, accent)
    c.rect(4, h - 7, w - 4, h - 4, accent)
    c.rect(4, 7, 7, h - 7, accent)
    c.rect(w - 7, 7, w - 4, h - 7, accent)
    if trim:
        c.rect(8, 8, w - 8, 10, "cream_hi" if fill == "cream" else "teal")
        c.rect(8, h - 10, w - 8, h - 8, "ink")
    # Four pixel corner brackets make the stretch-safe border legible.
    for x, y, sx, sy in ((8, 8, 1, 1), (w - 8, 8, -1, 1), (8, h - 8, 1, -1), (w - 8, h - 8, -1, -1)):
        c.rect(x, y, x + 3 * sx, y + sy, "gold")
        c.rect(x, y, x + sx, y + 3 * sy, "gold")
    return c


def dialogue():
    c = panel(320, 128, "cream", "teal")
    c.rect(18, 22, 74, 26, "teal_dark")
    c.rect(22, 26, 70, 30, "gold")
    c.rect(18, 36, 302, 38, "cream_hi")
    c.rect(18, 44, 296, 46, "cream_hi")
    c.rect(18, 52, 264, 54, "cream_hi")
    c.rect(18, 64, 128, 68, "teal")
    c.rect(152, 64, 280, 68, "teal")
    c.rect(18, 74, 104, 78, "ink")
    c.rect(138, 74, 276, 78, "ink")
    c.rect(18, 88, 60, 92, "coral")
    c.rect(84, 88, 138, 92, "gold")
    c.rect(144, 88, 222, 92, "teal_dark")
    return c


def choice(state):
    colors = {"idle": ("cream", "teal"), "selected": ("cream_hi", "gold"), "armed": ("teal", "cream_hi"), "saving": ("cream", "gold"), "committed": ("mint", "teal_dark"), "error": ("cream", "coral")}
    fill, accent = colors[state]
    c = panel(288, 72, fill, accent, trim=False)
    c.rect(18, 18, 26, 54, accent)
    c.rect(32, 18, 36, 54, "plum")
    c.rect(52, 20, 208, 24, "cream_hi" if fill != "teal" else "teal_dark")
    c.rect(52, 30, 228, 34, "cream_hi" if fill != "teal" else "teal_dark")
    c.rect(52, 44, 154, 48, "ink" if fill != "teal" else "cream")
    if state in {"saving", "committed"}:
        c.rect(236, 18, 246, 28, "gold")
        c.rect(240, 22, 250, 38, "gold")
        c.rect(244, 32, 250, 48, "teal_dark")
    if state == "error":
        c.rect(236, 18, 246, 22, "coral")
        c.rect(240, 26, 242, 44, "coral")
        c.rect(240, 48, 242, 50, "coral")
    return c


def receipt(state):
    c = panel(320, 64, "cream", "mint" if state == "saved" else "coral", trim=False)
    c.rect(18, 17, 42, 41, "mint" if state == "saved" else "coral")
    if state == "saved":
        c.line([(22, 29), (28, 35), (38, 23)], "plum_dark")
    else:
        c.rect(29, 21, 32, 34, "cream_hi")
        c.rect(29, 37, 32, 39, "cream_hi")
    c.rect(56, 18, 204, 22, "cream_hi")
    c.rect(56, 28, 286, 32, "cream_hi")
    c.rect(56, 40, 174, 44, "ink")
    return c


def phone_shell():
    c = panel(256, 384, "teal_dark", "gold")
    c.rect(20, 28, 236, 58, "plum_dark")
    c.rect(28, 38, 196, 48, "gold")
    c.rect(20, 70, 236, 354, "cream")
    c.rect(28, 80, 228, 96, "teal")
    for y in (112, 176, 240, 304):
        c.rect(28, y, 228, y + 4, "ink")
    for x in (28, 92, 156, 220):
        c.rect(x, 344, x + 4, 376, "teal_dark")
    c.rect(110, 16, 146, 20, "plum_dark")
    return c


def phone_view(kind):
    c = panel(224, 320, "cream", "teal" if kind in {"chat", "contacts"} else "gold")
    c.rect(16, 18, 208, 42, "plum_dark")
    c.rect(26, 28, 114, 32, "gold")
    c.rect(176, 26, 192, 34, "teal")
    if kind == "chat":
        for y, x1, x2, col in ((72, 34, 148, "teal"), (108, 72, 194, "gold"), (144, 34, 162, "teal"), (180, 86, 194, "gold"), (216, 34, 132, "teal")):
            c.rect(x1, y, x2, y + 24, col)
            c.rect(x1 + 6, y + 8, min(x2 - 6, x1 + 52), y + 12, "cream_hi" if col == "teal" else "plum")
    elif kind == "contacts":
        for y in (76, 136, 196, 256):
            c.rect(28, y, 62, y + 32, "coral")
            c.rect(74, y + 4, 178, y + 10, "teal_dark")
            c.rect(74, y + 18, 144, y + 24, "ink")
    elif kind == "memory":
        for y, col in ((78, "gold"), (130, "teal"), (182, "coral"), (234, "gold")):
            c.rect(30, y, 50, y + 32, col)
            c.rect(64, y + 5, 196, y + 11, "teal_dark")
            c.rect(64, y + 19, 172, y + 25, "ink")
    else:
        for y in (82, 132, 182, 232):
            c.rect(30, y, 76, y + 18, "teal_dark")
            c.rect(120, y + 2, 196, y + 16, "plum")
            c.rect(200, y + 2, 216, y + 16, "gold")
    return c


def main():
    specs = [
        ("dialogue-window", dialogue(), {"left": 8, "top": 8, "right": 8, "bottom": 8}, "dialogue"),
        *[(f"choice-card-{s}", choice(s), {"left": 8, "top": 8, "right": 8, "bottom": 8}, "choice") for s in ("idle", "selected", "armed", "saving", "committed", "error")],
        ("status-receipt-saved", receipt("saved"), {"left": 8, "top": 8, "right": 8, "bottom": 8}, "status-receipt"),
        ("status-receipt-error", receipt("error"), {"left": 8, "top": 8, "right": 8, "bottom": 8}, "status-receipt"),
        ("phone-shell", phone_shell(), {"left": 10, "top": 10, "right": 10, "bottom": 10}, "phone"),
        *[(f"phone-{k}", phone_view(k), {"left": 8, "top": 8, "right": 8, "bottom": 8}, "phone-view") for k in ("chat", "contacts", "memory", "settings")],
    ]
    gap = 16
    cols = 3
    rows = (len(specs) + cols - 1) // cols
    cell_w, cell_h = 352, 432
    atlas = Canvas(cols * cell_w, rows * cell_h)
    frames = []
    for i, (ident, image, insets, category) in enumerate(specs):
        save(image, f"{ident}.png")
        x, y = (i % cols) * cell_w + gap, (i // cols) * cell_h + gap
        for yy, row in enumerate(image.px):
            for xx, pixel in enumerate(row):
                if pixel[3]:
                    atlas.px[y + yy][x + xx] = pixel
        record = {"id": ident, "x": x, "y": y, "w": image.w, "h": image.h, "category": category, "nineSliceInsets": insets, "sampling": "nearest"}
        if ident.startswith("choice-card-"):
            record["state"] = ident.removeprefix("choice-card-")
        elif ident.startswith("status-receipt-"):
            record["state"] = ident.removeprefix("status-receipt-")
        elif ident.startswith("phone-") and ident != "phone-shell":
            record["view"] = ident.removeprefix("phone-")
        frames.append(record)
    save(atlas, "hud-panels-atlas-v1.png")
    preview = Canvas(atlas.w * 2, atlas.h * 2)
    for yy, row in enumerate(atlas.px):
        for xx, pixel in enumerate(row):
            preview.px[yy * 2][xx * 2] = pixel
            preview.px[yy * 2][xx * 2 + 1] = pixel
            preview.px[yy * 2 + 1][xx * 2] = pixel
            preview.px[yy * 2 + 1][xx * 2 + 1] = pixel
    save(preview, "hud-panels-preview-2x.png")
    meta = {"atlas": "hud-panels-atlas-v1.png", "width": atlas.w, "height": atlas.h, "pixelArt": True, "sampling": "nearest", "frames": frames}
    (OUT / "frames.json").write_text(json.dumps(meta, indent=2) + "\n")


if __name__ == "__main__":
    main()
