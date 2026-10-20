from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
W = H = 32
PALETTE = {
    "ink": (35, 28, 52, 255),
    "deep": (54, 44, 78, 255),
    "cream": (255, 241, 197, 255),
    "paper": (255, 249, 226, 255),
    "coral": (232, 93, 104, 255),
    "gold": (246, 193, 81, 255),
    "mint": (103, 210, 174, 255),
    "sky": (95, 175, 235, 255),
    "lilac": (175, 127, 225, 255),
    "brown": (122, 76, 65, 255),
    "hair": (43, 35, 58, 255),
    "skin": (245, 181, 145, 255),
    "skin2": (195, 116, 91, 255),
    "rose": (247, 151, 163, 255),
    "white": (255, 255, 255, 255),
}

CHARACTERS = {
    "mara": ("skin", "hair", "coral"),
    "eli": ("skin2", "hair", "sky"),
    "niko": ("skin", "brown", "gold"),
    "aunt-sol": ("skin2", "hair", "mint"),
    "player": ("skin", "deep", "lilac"),
    "amelia": ("skin2", "brown", "rose"),
}
REACTIONS = ["heart", "laugh", "surprise", "comfort", "thinking", "celebrate", "wave", "thanks", "apology", "consent"]


def px(d: ImageDraw.ImageDraw, box, color):
    d.rectangle(box, fill=PALETTE[color] if isinstance(color, str) else color)


def face(name: str, reaction: str) -> Image.Image:
    skin, hair, accent = CHARACTERS[name]
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # soft sticker shadow and tiny starlets
    px(d, (4, 27, 27, 29), "deep")
    px(d, (5, 28, 26, 30), (54, 44, 78, 120))
    # body / head cluster
    px(d, (9, 18, 22, 26), accent)
    px(d, (7, 11, 24, 20), skin)
    px(d, (8, 8, 23, 13), hair)
    px(d, (10, 6, 13, 11), hair)
    px(d, (20, 7, 23, 12), hair)
    px(d, (11, 14, 12, 15), "ink")
    px(d, (19, 14, 20, 15), "ink")
    px(d, (14, 17, 17, 17), "coral" if reaction in ("apology", "comfort") else "ink")
    # identity cue: asymmetrical brow/ear pin
    px(d, (6, 14, 7, 16), accent)
    if name in ("niko", "amelia"):
        px(d, (21, 9, 22, 10), "gold")
    # reaction-specific hand/prop / facial pixels
    if reaction == "heart":
        px(d, (24, 7, 25, 8), "coral"); px(d, (27, 8, 28, 9), "coral"); px(d, (25, 9, 27, 10), "coral")
    elif reaction == "laugh":
        px(d, (14, 16, 17, 18), "ink"); px(d, (13, 15, 18, 15), "cream"); px(d, (25, 11, 27, 12), "gold")
    elif reaction == "surprise":
        px(d, (14, 16, 16, 18), "ink"); px(d, (25, 8, 26, 9), "gold"); px(d, (27, 10, 28, 11), "gold")
    elif reaction == "comfort":
        px(d, (4, 13, 7, 20), "mint"); px(d, (5, 11, 6, 14), "mint"); px(d, (24, 17, 28, 19), "mint")
    elif reaction == "thinking":
        px(d, (24, 18, 27, 20), skin); px(d, (25, 16, 27, 18), skin); px(d, (25, 6, 26, 7), "sky")
    elif reaction == "celebrate":
        px(d, (4, 10, 6, 15), accent); px(d, (26, 9, 28, 14), accent)
        px(d, (3, 7, 4, 8), "gold"); px(d, (28, 6, 29, 7), "gold")
    elif reaction == "wave":
        px(d, (25, 12, 28, 17), skin); px(d, (27, 9, 28, 12), skin); px(d, (25, 8, 26, 12), skin)
    elif reaction == "thanks":
        px(d, (5, 18, 8, 21), "cream"); px(d, (24, 18, 27, 21), "cream"); px(d, (14, 7, 16, 7), "gold")
    elif reaction == "apology":
        px(d, (12, 14, 13, 15), "ink"); px(d, (18, 14, 19, 15), "ink"); px(d, (14, 18, 17, 18), "coral")
        px(d, (24, 7, 25, 9), "sky")
    elif reaction == "consent":
        # split consent mark keeps words external: clear yes/no symbol only
        px(d, (4, 7, 7, 8), "mint"); px(d, (5, 6, 6, 9), "mint")
        px(d, (26, 22, 28, 23), "coral"); px(d, (25, 23, 29, 24), "coral")
    return im


def atlas(images, cols, cell=(W, H), scale=1):
    cw, ch = cell
    out = Image.new("RGBA", (cw * cols * scale, ch * ((len(images) + cols - 1) // cols) * scale), (0, 0, 0, 0))
    for i, im in enumerate(images):
        x = (i % cols) * cw * scale
        y = (i // cols) * ch * scale
        out.paste(im.resize((cw * scale, ch * scale), Image.Resampling.NEAREST), (x, y))
    return out


def status_icon(kind: str) -> Image.Image:
    im = Image.new("RGBA", (24, 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == "online":
        px(d, (7, 7, 16, 16), "mint"); px(d, (10, 10, 13, 13), "cream")
    elif kind == "offline":
        px(d, (7, 7, 16, 16), "deep"); px(d, (10, 10, 13, 13), "paper")
    elif kind == "typing":
        for x in (7, 11, 15): px(d, (x, 11, x + 1, 12), "sky")
    elif kind == "unread":
        px(d, (7, 6, 16, 16), "coral"); px(d, (11, 8, 12, 13), "paper"); px(d, (11, 15, 12, 15), "paper")
    elif kind == "saved":
        px(d, (7, 6, 16, 17), "gold"); px(d, (9, 8, 14, 13), "paper"); px(d, (9, 14, 14, 15), "deep")
    elif kind == "error":
        px(d, (7, 7, 16, 16), "coral"); px(d, (9, 9, 14, 14), "paper"); px(d, (11, 8, 12, 15), "coral")
    elif kind == "muted":
        px(d, (6, 10, 13, 14), "deep"); px(d, (13, 7, 14, 16), "deep"); px(d, (7, 17, 17, 18), "coral")
    return im


def badge(state: str) -> Image.Image:
    im = Image.new("RGBA", (40, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = {"default": "lilac", "favorite": "gold", "verified": "mint", "muted": "coral"}[state]
    for p in [(4, 4, 35, 5), (4, 34, 35, 35), (4, 5, 5, 34), (34, 5, 35, 34)]: px(d, p, c)
    px(d, (8, 8, 31, 31), "deep")
    if state == "favorite":
        px(d, (17, 13, 22, 18), "gold"); px(d, (15, 15, 24, 21), "gold")
    elif state == "verified":
        px(d, (14, 19, 18, 23), "mint"); px(d, (17, 16, 25, 21), "mint")
    elif state == "muted":
        px(d, (13, 13, 25, 25), "coral"); px(d, (15, 15, 23, 23), "deep")
    return im


def tail(kind: str) -> Image.Image:
    im = Image.new("RGBA", (20, 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    color = {"incoming": "sky", "outgoing": "lilac", "system": "deep"}[kind]
    if kind == "incoming":
        px(d, (2, 2, 14, 9), color); px(d, (2, 8, 8, 11), color); px(d, (2, 10, 5, 12), color)
    elif kind == "outgoing":
        px(d, (5, 2, 17, 9), color); px(d, (12, 8, 17, 11), color); px(d, (15, 10, 17, 12), color)
    else:
        px(d, (4, 2, 16, 9), color); px(d, (7, 8, 13, 11), color)
    return im


def write_png(path: Path, image: Image.Image):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG", optimize=False)


def main():
    files = []
    for character in CHARACTERS:
        imgs = [face(character, reaction) for reaction in REACTIONS]
        path = ROOT / "reactions" / f"{character}-reactions-10x32-atlas.png"
        write_png(path, atlas(imgs, 10)); files.append((path, 320, 32, "reactions", character))
    statuses = ["online", "offline", "typing", "unread", "saved", "error", "muted"]
    sp = ROOT / "contact-status" / "contact-status-7x24-atlas.png"; write_png(sp, atlas([status_icon(x) for x in statuses], 7, (24, 24))); files.append((sp, 168, 24, "status", "contact"))
    for kind in ("incoming", "outgoing", "system"):
        p = ROOT / "bubble-tails" / f"{kind}-tail-20x14.png"; write_png(p, tail(kind)); files.append((p, 20, 14, "tail", kind))
    states = ["default", "favorite", "verified", "muted"]
    bp = ROOT / "avatar-badges" / "avatar-badge-4x40-atlas.png"; write_png(bp, atlas([badge(x) for x in states], 4, (40, 40))); files.append((bp, 160, 40, "badge", "avatar"))
    preview = Image.new("RGBA", (640, 360), (27, 24, 45, 255)); d = ImageDraw.Draw(preview)
    preview.paste(atlas([face("mara", x) for x in REACTIONS], 10, scale=3), (12, 12), atlas([face("mara", x) for x in REACTIONS], 10, scale=3))
    preview.paste(atlas([face("eli", x) for x in REACTIONS], 10, scale=3), (12, 120), atlas([face("eli", x) for x in REACTIONS], 10, scale=3))
    preview.paste(atlas([status_icon(x) for x in statuses], 7, (24, 24), scale=3), (12, 228), atlas([status_icon(x) for x in statuses], 7, (24, 24), scale=3))
    preview.paste(atlas([tail(x) for x in ("incoming", "outgoing", "system")], 3, (20, 14), scale=4), (300, 250), atlas([tail(x) for x in ("incoming", "outgoing", "system")], 3, (20, 14), scale=4))
    pp = ROOT / "chat-reaction-icons-v1-preview-3x.png"; write_png(pp, preview); files.append((pp, 640, 360, "preview", "preview"))
    manifest = {
        "schema": "liveit.pixel.chat-reaction-icons.v1",
        "title": "Original character reaction stickers and compact chat status symbols",
        "runtimeReady": False,
        "license": "CC0-equivalent original procedural artwork by LIVEIT project",
        "sourcePolicy": "No archive, third-party, or reference image bytes used; all pixels authored by deterministic Pillow primitives.",
        "textPolicy": "Dynamic names, message text, timestamps, and accessibility labels remain external.",
        "pixelPolicy": {"integerPrimitives": True, "nearestNeighbor": True, "rgba": True, "paletteEntries": len(PALETTE)},
        "reactionOrder": REACTIONS,
        "statusOrder": statuses,
        "badgeOrder": states,
        "files": [],
        "runtimeIntegration": "Concept-only package. Requires renderer import, pixel-scale review, accessibility/state wiring, and character identity QA before runtimeReady can change."
    }
    for path, width, height, family, name in files:
        manifest["files"].append({"file": str(path.relative_to(ROOT)), "width": width, "height": height, "mode": "RGBA", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "family": family, "name": name, "runtimeReady": False})
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    provenance = {"generator": "generate_assets.py", "generatorVersion": "1.0", "createdUtc": "2026-10-20T00:00:00Z", "prompt": "Original crisp pixel reaction stickers for six LIVEIT social characters, plus text-free chat status symbols, compact tails, and avatar badge frames.", "negativePrompt": "No third-party sprites, no archive asset bytes, no logos, no readable text, no anti-aliased edges, no mirrored character art.", "sourceBytes": [], "files": [{"file": x[0].relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(x[0].read_bytes()).hexdigest()} for x in files]}
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    (ROOT / "README.md").write_text("""# Chat reaction icons v1\n\nOriginal, deterministic pixel clusters for expressive chat and social feedback. Six character identities each receive ten age-safe sticker reactions: heart, laugh, surprise, comfort, thinking, celebrate, wave, thanks, apology, and consent. The consent frame contains only affirmative/negative symbols; labels and accessibility text stay external.\n\nThe contact-status atlas adds online, offline, typing, unread, saved, error, and muted symbols. Bubble tails and avatar badge frames are separate transparent primitives so the chat renderer can compose them without embedding text.\n\nAll files are concept-only (`runtimeReady: false`) until imported into the renderer, reviewed at the game's pixel scale, and wired to accessible labels and state behavior. No downloaded or third-party asset bytes were used. See `manifest.json` and `provenance.json` for exact hashes and generation record.\n""")


if __name__ == "__main__":
    main()
