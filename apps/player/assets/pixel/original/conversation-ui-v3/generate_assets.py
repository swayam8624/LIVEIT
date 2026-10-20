#!/usr/bin/env python3
"""Build the original, text-free LIVEIT conversation UI v3 package.

The builder uses only integer Pillow primitives.  It intentionally produces
concept artwork outside the runtime asset intake; every manifest record keeps
runtimeReady false until renderer and accessibility review is complete.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
P = {
    "clear": (0, 0, 0, 0),
    "night": (18, 22, 38, 255),
    "ink": (35, 31, 53, 255),
    "ink2": (49, 48, 76, 255),
    "ink3": (68, 65, 96, 255),
    "cream": (255, 241, 211, 255),
    "cream_hi": (255, 249, 231, 255),
    "cream_shadow": (208, 169, 130, 255),
    "cyan": (69, 203, 193, 255),
    "cyan_hi": (140, 239, 216, 255),
    "violet": (135, 111, 210, 255),
    "violet_hi": (191, 168, 245, 255),
    "coral": (226, 111, 131, 255),
    "coral_hi": (255, 167, 163, 255),
    "amber": (245, 191, 73, 255),
    "mint": (101, 214, 157, 255),
    "muted": (135, 137, 163, 255),
    "muted2": (91, 93, 120, 255),
    "danger": (232, 92, 105, 255),
    "disabled": (85, 87, 108, 255),
}

def c(name: str):
    return P[name]

def im(w: int, h: int) -> Image.Image:
    return Image.new("RGBA", (w, h), c("clear"))

def R(d, box, fill, outline=None, width=1):
    d.rectangle(box, fill=c(fill), outline=c(outline) if outline else None, width=width)

def L(d, points, fill, width=1):
    d.line(points, fill=c(fill), width=width)

def save(x: Image.Image, rel: str):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    x.save(path)

def stepped_panel(w: int, h: int, theme: str, inset: int = 12, tail: str | None = None) -> Image.Image:
    """A crisp panel with a 12px protected border and a repeatable center."""
    x = im(w, h)
    d = ImageDraw.Draw(x)
    themes = {
        "dialogue": ("ink2", "violet", "violet_hi", "ink"),
        "choice": ("night", "cyan", "cyan_hi", "ink"),
        "status": ("ink", "amber", "cream_hi", "ink2"),
        "phone": ("night", "violet", "violet_hi", "ink2"),
        "incoming": ("cream", "cream_hi", "cream_shadow", "ink"),
        "outgoing": ("violet", "violet_hi", "violet", "ink"),
        "system": ("ink3", "muted", "muted", "night"),
    }
    fill, edge, hi, shadow = themes[theme]
    # Main stepped body; corners are deliberately square-pixel stair steps.
    R(d, (inset, 0, w - inset - 1, h - 1), fill)
    R(d, (0, inset, w - 1, h - inset - 1), fill)
    R(d, (4, 4, w - 5, h - 5), fill)
    R(d, (inset, 0, w - inset - 1, 2), hi)
    R(d, (0, inset, 2, h - inset - 1), hi)
    R(d, (inset, h - 3, w - inset - 1, h - 1), shadow)
    R(d, (w - 3, inset, w - 1, h - inset - 1), shadow)
    # Two-pixel corner notches keep the repeat boundary visually legible.
    R(d, (4, 4, 7, 5), edge)
    R(d, (w - 8, 4, w - 5, 5), edge)
    R(d, (4, h - 6, 7, h - 5), shadow)
    R(d, (w - 8, h - 6, w - 5, h - 5), shadow)
    if tail == "left":
        R(d, (0, h - 22, 7, h - 12), fill)
        R(d, (0, h - 11, 3, h - 5), fill)
        R(d, (3, h - 8, 5, h - 3), shadow)
    elif tail == "right":
        R(d, (w - 8, h - 22, w - 1, h - 12), fill)
        R(d, (w - 4, h - 11, w - 1, h - 5), fill)
        R(d, (w - 6, h - 8, w - 4, h - 3), shadow)
    return x

def make_slices():
    for name, theme in (("dialogue", "dialogue"), ("choice", "choice"), ("status", "status"), ("phone", "phone"), ("incoming", "incoming"), ("outgoing", "outgoing"), ("system", "system")):
        save(stepped_panel(64, 64, theme, 12), f"nine-slice/{name}-slice-64x64.png")

def make_bubbles():
    for name, theme, tail in (("incoming", "incoming", "left"), ("outgoing", "outgoing", "right"), ("system", "system", None)):
        x = stepped_panel(160, 64, theme, 12, tail)
        d = ImageDraw.Draw(x)
        # A subtle signal rail gives each surface a distinct visual identity
        # while leaving the center clear for dynamic text.
        rail = "cyan" if name == "incoming" else "coral" if name == "outgoing" else "muted"
        R(d, (16, 11, 20, 15), rail)
        R(d, (16, 17, 18, 21), rail)
        R(d, (24, 11, 28, 13), rail)
        save(x, f"surfaces/{name}-bubble-160x64.png")

def make_choice_status_surfaces():
    for name, theme, w, h in (("choice-idle", "choice", 192, 56), ("choice-focus", "choice", 192, 56), ("choice-pressed", "choice", 192, 56), ("status-saved", "status", 192, 48), ("status-error", "status", 192, 48), ("status-syncing", "status", 192, 48)):
        x = stepped_panel(w, h, theme, 12)
        d = ImageDraw.Draw(x)
        if "focus" in name:
            R(d, (12, 7, w - 13, 9), "amber")
            R(d, (8, 15, 11, h - 16), "amber")
        if "pressed" in name:
            R(d, (16, h - 12, w - 17, h - 9), "coral")
        if name == "status-saved":
            L(d, [(20, 24), (25, 29), (34, 18)], "mint", 3)
        elif name == "status-error":
            R(d, (20, 18, 24, 30), "danger")
            R(d, (20, 34, 24, 37), "danger")
        else:
            R(d, (20, 20, 34, 24), "amber")
            R(d, (25, 16, 29, 28), "amber")
        save(x, f"surfaces/{name}-192x{h}.png")

def make_typing_and_status():
    x = im(72, 24)
    d = ImageDraw.Draw(x)
    for frame in range(3):
        ox = frame * 24
        R(d, (ox + 3, 4, ox + 20, 20), "ink")
        for i in range(3):
            y = 11 - (3 if (i + frame) % 3 == 0 else 0)
            R(d, (ox + 7 + i * 4, y, ox + 9 + i * 4, y + 2), "cyan_hi" if i == frame else "violet_hi")
    save(x, "indicators/typing-dots-3x24x24-atlas.png")
    x = im(96, 24)
    d = ImageDraw.Draw(x)
    for i, kind in enumerate(("online", "away", "busy", "offline")):
        ox = i * 24
        col = {"online": "mint", "away": "amber", "busy": "coral", "offline": "muted"}[kind]
        R(d, (ox + 5, 5, ox + 18, 18), "ink")
        if kind == "online":
            R(d, (ox + 8, 8, ox + 15, 15), col)
        elif kind == "away":
            R(d, (ox + 11, 7, ox + 13, 15), col)
            R(d, (ox + 13, 14, ox + 16, 16), col)
        elif kind == "busy":
            R(d, (ox + 8, 11, ox + 15, 14), col)
        else:
            R(d, (ox + 8, 8, ox + 15, 15), col)
            L(d, [(ox + 8, 8), (ox + 15, 15)], "ink")
    save(x, "indicators/status-4x24-atlas.png")

def make_avatar():
    x = im(192, 48)
    d = ImageDraw.Draw(x)
    for i, (edge, fill) in enumerate((("cyan", "ink2"), ("amber", "ink2"), ("coral", "ink"), ("muted", "night"))):
        ox = i * 48
        R(d, (3, 3, 44, 44), edge)
        R(d, (7, 7, 40, 40), fill)
        # Generic face placeholder, intentionally not a character portrait.
        R(d, (15, 13, 32, 34), "cream" if i < 3 else "muted")
        R(d, (18, 20, 20, 22), "ink")
        R(d, (27, 20, 29, 22), "ink")
        R(d, (21, 28, 26, 30), "coral" if i != 3 else "disabled")
        R(d, (11, 11, 14, 14), edge)
    save(x, "avatars/avatar-frame-4x48-atlas.png")

def icon_button(state: str, action: str) -> Image.Image:
    x = im(32, 32)
    d = ImageDraw.Draw(x)
    border, fill = {"normal": ("cyan", "ink2"), "focus": ("amber", "ink2"), "pressed": ("coral", "ink"), "disabled": ("disabled", "night")}[state]
    glyph = "muted" if state == "disabled" else "cream_hi"
    R(d, (3, 3, 28, 28), border)
    R(d, (6, 6, 25, 25), fill)
    if action == "consent":
        L(d, [(10, 17), (14, 21), (22, 11)], glyph, 2)
    elif action == "report":
        R(d, (11, 9, 20, 21), glyph)
        R(d, (13, 12, 18, 17), fill)
        R(d, (14, 23, 17, 25), glyph)
    elif action == "block":
        R(d, (9, 9, 22, 22), glyph)
        L(d, [(10, 21), (21, 10)], fill, 2)
    elif action == "send":
        d.polygon([(9, 15), (23, 9), (18, 23), (14, 18), (9, 19)], fill=c(glyph))
    elif action == "reply":
        L(d, [(21, 11), (12, 16), (21, 21)], glyph, 2)
        R(d, (14, 15, 23, 17), glyph)
    elif action == "close":
        L(d, [(11, 11), (21, 21)], glyph, 2)
        L(d, [(21, 11), (11, 21)], glyph, 2)
    return x

def make_controls():
    for action in ("consent", "report", "block", "send", "reply", "close"):
        x = im(128, 32)
        for i, state in enumerate(("normal", "focus", "pressed", "disabled")):
            x.alpha_composite(icon_button(state, action), (i * 32, 0))
        save(x, f"controls/{action}-states-4x32-atlas.png")

def make_phone_widgets():
    # Frame with safe inset metadata; all internal regions are text-free.
    x = stepped_panel(176, 240, "phone", 12)
    d = ImageDraw.Draw(x)
    R(d, (16, 15, 159, 27), "violet")
    R(d, (22, 18, 60, 23), "cyan")
    R(d, (145, 18, 153, 23), "amber")
    R(d, (16, 36, 159, 201), "ink")
    for y, col in ((52, "cream"), (85, "violet"), (118, "cream"), (151, "violet")):
        R(d, (26, y, 110, y + 20), col)
        R(d, (118, y + 4, 148, y + 14), "ink3")
    R(d, (16, 212, 159, 224), "violet")
    for ox in (28, 68, 108, 148):
        R(d, (ox - 4, 216, ox + 4, 220), "cyan_hi")
    save(x, "phone/phone-chat-panel-176x240.png")
    # Small text-free widget strip: contact, call, attachment, emoji, more.
    x = im(160, 32)
    d = ImageDraw.Draw(x)
    for i, kind in enumerate(("contact", "call", "attach", "emoji", "more")):
        ox = i * 32
        R(d, (ox + 3, 3, ox + 28, 28), "violet")
        R(d, (ox + 6, 6, ox + 25, 25), "ink2")
        if kind == "contact":
            R(d, (ox + 12, 9, ox + 19, 16), "cyan_hi")
            R(d, (ox + 9, 18, ox + 22, 22), "cyan_hi")
        elif kind == "call":
            L(d, [(ox + 11, 11), (ox + 15, 9), (ox + 21, 16), (ox + 18, 21), (ox + 12, 15), (ox + 11, 11)], "mint", 2)
        elif kind == "attach":
            L(d, [(ox + 19, 10), (ox + 12, 17), (ox + 12, 22), (ox + 17, 24), (ox + 22, 19), (ox + 22, 12)], "amber", 2)
        elif kind == "emoji":
            R(d, (ox + 10, 9, ox + 21, 20), "amber")
            R(d, (ox + 13, 12, ox + 14, 13), "ink")
            R(d, (ox + 18, 12, ox + 19, 13), "ink")
            R(d, (ox + 14, 16, ox + 18, 17), "ink")
        else:
            for yy in (12, 16, 20):
                R(d, (ox + 13, yy, ox + 18, yy + 1), "cyan_hi")
    save(x, "phone/chat-widget-strip-160x32.png")

def make_preview():
    x = im(640, 384)
    d = ImageDraw.Draw(x)
    for y in range(0, 384, 8):
        for xx in range(0, 640, 8):
            R(d, (xx, y, xx + 7, y + 7), "night" if ((xx // 8 + y // 8) % 2) else "ink")
    items = [
        ("surfaces/incoming-bubble-160x64.png", (16, 16), 2),
        ("surfaces/outgoing-bubble-160x64.png", (304, 16), 2),
        ("surfaces/system-bubble-160x64.png", (16, 160), 2),
        ("phone/phone-chat-panel-176x240.png", (432, 104), 1),
        ("controls/consent-states-4x32-atlas.png", (16, 304), 2),
        ("controls/report-states-4x32-atlas.png", (272, 304), 2),
    ]
    for rel, pos, scale in items:
        src = Image.open(ROOT / rel).convert("RGBA")
        src = src.resize((src.width * scale, src.height * scale), Image.Resampling.NEAREST)
        x.alpha_composite(src, pos)
    save(x, "conversation-ui-v3-preview-2x.png")

def build_manifest():
    records = []
    for path in sorted(ROOT.rglob("*.png")):
        with Image.open(path) as x:
            records.append({"file": path.relative_to(ROOT).as_posix(), "width": x.width, "height": x.height, "mode": x.mode, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "runtimeReady": False})
    slices = []
    for name in ("dialogue", "choice", "status", "phone", "incoming", "outgoing", "system"):
        slices.append({"file": f"nine-slice/{name}-slice-64x64.png", "sourceSize": [64, 64], "insets": {"left": 12, "top": 12, "right": 12, "bottom": 12}, "centerMode": "repeat", "borderSafety": {"edgePixelsOpaque": False, "transparentOutsideSource": True, "tail": name in ("incoming", "outgoing")}})
    manifest = {
        "schema": "liveit.pixel.conversation-ui.v3",
        "title": "Premium retro-futurist conversation and social UI sprite kit",
        "runtimeReady": False,
        "license": "CC0-equivalent original procedural artwork by LIVEIT project",
        "sourcePolicy": "No archive, third-party, or reference image bytes used.",
        "textPolicy": "Dynamic dialogue, labels, dates, balances, and accessibility text remain external.",
        "pixelPolicy": {"integerPrimitives": True, "nearestNeighbor": True, "rgba": True, "paletteEntries": len(P)},
        "nineSlice": {"tiles": slices, "safeExpansion": "Repeat only the center region; preserve the 12px perimeter and do not stretch corner pixels."},
        "atlasConventions": {"origin": "top-left", "stateOrder": ["normal", "focus", "pressed", "disabled"], "frameSize": {"controls": [32, 32], "status": [24, 24], "avatar": [48, 48]}},
        "files": records,
        "runtimeIntegration": "Concept-only package. Requires renderer import, nine-slice expansion tests, semantic accessibility wiring, and human visual review before runtimeReady can change."
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    provenance = {
        "artwork": "Procedural integer-pixel geometry authored for LIVEIT; generated by generate_assets.py.",
        "generator": "generate_assets.py",
        "palette": P,
        "inputs": [],
        "externalAssets": False,
        "prompts": [],
        "transformations": ["None; all PNGs are direct generator outputs."],
        "reviewNotes": ["Dynamic text is absent by design.", "Every PNG is RGBA.", "Nine-slice boundaries and transparent margins require renderer review.", "All records remain runtimeReady false."]
    }
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(records)} PNGs")

def main():
    make_slices()
    make_bubbles()
    make_choice_status_surfaces()
    make_typing_and_status()
    make_avatar()
    make_controls()
    make_phone_widgets()
    make_preview()
    build_manifest()

if __name__ == "__main__":
    main()
