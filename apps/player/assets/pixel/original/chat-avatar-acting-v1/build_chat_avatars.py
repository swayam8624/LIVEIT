#!/usr/bin/env python3
"""Build original 48px chat-avatar acting frames and integrity metadata."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FRAMES = ROOT / "frames"
IDENTITY_REF = ROOT.parent / "family-portrait-expressions-v1" / "manifest.json"
SIZE = 48
STATES = ("listening", "curious", "concerned", "reassuring", "speaking", "blink")
CHARACTERS = [
    {
        "id": "mara", "name": "Mara", "ageGroup": "adult", "role": "adult parent/caregiver",
        "identity": "short natural curls, rust cardigan, mustard scarf",
        "skin": "#8b4b32", "hair": "#281a1c", "coat": "#b94d32", "accent": "#e0a33e",
        "bg": "#49313d", "outline": "#241923", "hairStyle": "curls",
    },
    {
        "id": "eli", "name": "Eli", "ageGroup": "adult", "role": "adult parent/caregiver",
        "identity": "close-cropped dark hair, round glasses, navy jacket",
        "skin": "#ad7047", "hair": "#211c24", "coat": "#29395d", "accent": "#daa13e",
        "bg": "#293744", "outline": "#191a29", "hairStyle": "close",
    },
    {
        "id": "niko", "name": "Niko", "ageGroup": "school-age", "role": "school-age sibling",
        "identity": "curly ponytail with orange tie, cobalt hoodie",
        "skin": "#a95a36", "hair": "#2a1a20", "coat": "#2f6dcc", "accent": "#ec7d31",
        "bg": "#263b5b", "outline": "#171b2d", "hairStyle": "pony",
    },
    {
        "id": "aunt-sol", "name": "Aunt Sol", "ageGroup": "older-adult", "role": "older relative",
        "identity": "silver braid, plum coat, sage scarf",
        "skin": "#a96645", "hair": "#d5c5b5", "coat": "#713c68", "accent": "#a5b887",
        "bg": "#473247", "outline": "#241d2c", "hairStyle": "braid",
    },
]

STATE_META = {
    "listening": {"label": "Listening", "meaning": "calm attention", "durationMs": None},
    "curious": {"label": "Curious", "meaning": "open question or interest", "durationMs": None},
    "concerned": {"label": "Concerned", "meaning": "gentle worry or empathy", "durationMs": None},
    "reassuring": {"label": "Reassuring", "meaning": "warm support", "durationMs": None},
    "speaking": {"label": "Speaking", "meaning": "mouth-open speech cue", "durationMs": 120},
    "blink": {"label": "Blink", "meaning": "brief closed-eye idle frame", "durationMs": 100},
}


def rgb(hex_color: str) -> tuple[int, int, int, int]:
    return tuple(bytes.fromhex(hex_color.removeprefix("#"))) + (255,)


def box(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], color: str) -> None:
    draw.rectangle(xy, fill=rgb(color))


def frame(character: dict[str, str], state: str) -> Image.Image:
    """Draw a consistent front-facing pixel bust with state-specific facial pixels."""
    im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    outline, skin, hair, coat, accent = (character[k] for k in ("outline", "skin", "hair", "coat", "accent"))

    # Pixel-cut circle, kept inside the cell to leave a transparent safety rim.
    bg_color = character["bg"]
    bg = rgb(bg_color)
    for y, left, right in ((4, 18, 29), (5, 14, 33), (6, 11, 36), (7, 9, 38),
                           (8, 7, 40), (9, 6, 41), (10, 5, 42), (11, 4, 43),
                           (12, 3, 44), (13, 3, 44), (14, 2, 45), (15, 2, 45),
                           (16, 2, 45), (17, 1, 46), (18, 1, 46), (19, 1, 46),
                           (20, 1, 46), (21, 1, 46), (22, 1, 46), (23, 1, 46),
                           (24, 1, 46), (25, 1, 46), (26, 2, 45), (27, 2, 45),
                           (28, 2, 45), (29, 3, 44), (30, 3, 44), (31, 4, 43),
                           (32, 5, 42), (33, 6, 41), (34, 7, 40), (35, 9, 38),
                           (36, 11, 36), (37, 14, 33), (38, 18, 29)):
        d.line((left, y, right, y), fill=bg)

    # Shoulders, neck, face, and hair; proportions remain fixed across the set.
    box(d, (8, 34, 39, 44), outline)
    box(d, (9, 35, 38, 43), coat)
    box(d, (20, 31, 27, 37), outline)
    box(d, (21, 31, 26, 36), skin)
    box(d, (13, 11, 34, 32), outline)
    box(d, (14, 12, 33, 31), skin)
    # ears
    box(d, (11, 20, 14, 25), outline); box(d, (12, 21, 14, 24), skin)
    box(d, (33, 20, 36, 25), outline); box(d, (33, 21, 35, 24), skin)

    style = character["hairStyle"]
    if style == "curls":
        for x, y, w in ((14, 9, 5), (20, 7, 5), (26, 8, 5), (11, 13, 4), (30, 12, 4),
                        (12, 16, 3), (32, 16, 3), (14, 10, 3), (24, 9, 4)):
            box(d, (x, y, x + w - 1, y + 4), hair)
        box(d, (15, 15, 17, 19), hair); box(d, (30, 15, 32, 18), hair)
    elif style == "close":
        box(d, (14, 9, 33, 16), hair)
        box(d, (16, 8, 20, 10), hair); box(d, (24, 8, 29, 10), hair)
    elif style == "pony":
        box(d, (14, 9, 33, 16), hair); box(d, (12, 13, 15, 21), hair)
        box(d, (31, 12, 34, 18), hair); box(d, (32, 17, 37, 22), hair)
        box(d, (35, 17, 37, 18), accent)
    elif style == "braid":
        box(d, (13, 9, 34, 17), hair); box(d, (12, 15, 15, 25), hair)
        for y, x in ((22, 13), (26, 15), (30, 13), (34, 15)):
            box(d, (x, y, x + 3, y + 4), hair)
            box(d, (x + 1, y + 1, x + 2, y + 2), "#eee0c9")
        box(d, (31, 15, 33, 21), hair)

    # State-driven brow, eye, and mouth shape. Child state set stays everyday and safe.
    brow_y = {"listening": 18, "curious": 17, "concerned": 17, "reassuring": 18, "speaking": 18, "blink": 19}[state]
    eye_y = {"listening": 20, "curious": 20, "concerned": 20, "reassuring": 20, "speaking": 20, "blink": 21}[state]
    if state == "concerned":
        box(d, (17, brow_y, 21, brow_y + 1), outline); box(d, (27, brow_y, 31, brow_y + 1), outline)
        # Lift the inner brow pixels to read as sympathetic concern at icon scale.
        box(d, (20, brow_y, 21, brow_y + 1), skin); box(d, (27, brow_y, 28, brow_y + 1), skin)
    elif state == "curious":
        box(d, (17, brow_y, 20, brow_y + 1), outline); box(d, (28, brow_y - 1, 31, brow_y), outline)
    else:
        box(d, (17, brow_y, 21, brow_y + 1), outline); box(d, (27, brow_y, 31, brow_y + 1), outline)
    if state == "blink":
        box(d, (17, eye_y, 21, eye_y + 1), outline); box(d, (27, eye_y, 31, eye_y + 1), outline)
    else:
        box(d, (18, eye_y, 20, eye_y + 3), outline); box(d, (28, eye_y, 30, eye_y + 3), outline)
        box(d, (19, eye_y, 19, eye_y), "#f5e9d2"); box(d, (29, eye_y, 29, eye_y), "#f5e9d2")
    # Small nose highlight keeps the face readable without over-detail.
    box(d, (23, 24, 24, 25), "#ca805b")
    if state == "concerned":
        box(d, (21, 28, 26, 29), outline); box(d, (22, 28, 25, 28), skin)
    elif state == "reassuring":
        box(d, (20, 27, 27, 28), outline); box(d, (21, 27, 26, 27), skin)
        box(d, (16, 26, 18, 27), "#d68168"); box(d, (30, 26, 32, 27), "#d68168")
    elif state == "speaking":
        box(d, (21, 27, 26, 30), outline); box(d, (22, 28, 25, 29), "#b64a4d")
    elif state == "curious":
        box(d, (22, 27, 25, 29), outline); box(d, (23, 27, 24, 27), "#f6d3a1")
    else:
        box(d, (21, 28, 26, 29), outline); box(d, (22, 28, 25, 28), "#d08a70")

    # A stable scarf/shirt accent ties the named identities together visually.
    box(d, (18, 35, 29, 37), accent)
    box(d, (19, 38, 28, 40), coat)
    if character["id"] == "eli":
        # Glasses are identity-defining: blocky rims remain separate from eye pixels.
        box(d, (15, 19, 22, 25), outline); box(d, (26, 19, 33, 25), outline)
        box(d, (16, 20, 21, 24), bg_color); box(d, (27, 20, 32, 24), bg_color)
        if state == "blink":
            box(d, (17, 21, 20, 22), skin); box(d, (28, 21, 31, 22), skin)
        else:
            box(d, (18, 21, 19, 23), outline); box(d, (29, 21, 30, 23), outline)
        box(d, (22, 21, 26, 22), outline)
    return im


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    atlas = Image.new("RGBA", (SIZE * len(STATES), SIZE * len(CHARACTERS)), (0, 0, 0, 0))
    contact = Image.new("RGB", (SIZE * 3 * len(STATES), (SIZE * 3 + 16) * len(CHARACTERS)), "#161f2e")
    font = ImageFont.load_default()
    for row, person in enumerate(CHARACTERS):
        for col, state in enumerate(STATES):
            im = frame(person, state)
            file = FRAMES / f"{person['id']}-{state}-48x48.png"
            im.save(file, optimize=True)
            atlas.alpha_composite(im, (col * SIZE, row * SIZE))
            enlarged = im.resize((SIZE * 3, SIZE * 3), Image.Resampling.NEAREST)
            contact.paste(enlarged, (col * SIZE * 3, row * (SIZE * 3 + 16)), enlarged)
            # Add state label below each preview tile.
            label = state.replace("-", " ")[:11]
            ImageDraw.Draw(contact).text((col * SIZE * 3 + 3, row * (SIZE * 3 + 16) + SIZE * 3 + 1), label, font=font, fill="#f5f2d9")
            rows.append({
                "id": f"liveit.pixel.v2.chat-avatar.{person['id']}.{state}",
                "characterId": person["id"], "characterName": person["name"],
                "ageGroup": person["ageGroup"], "ageSafety": "all-ages-safe",
                "state": state, **STATE_META[state],
                "file": file.relative_to(ROOT).as_posix(),
                "x": col * SIZE, "y": row * SIZE, "width": SIZE, "height": SIZE,
                "pivot": {"x": 24, "y": 42}, "sha256": digest(file),
                "runtimeReady": False,
            })
    atlas_path = ROOT / "chat-avatar-acting-atlas-6x4-48.png"
    contact_path = ROOT / "chat-avatar-acting-preview-3x.png"
    atlas.save(atlas_path, optimize=True)
    contact.save(contact_path, optimize=True)
    provenance = {
        "created": "2026-10-20",
        "method": "Drawn from original geometric pixel primitives in build_chat_avatars.py; no image generation, web assets, source archives, or copied pixels.",
        "identityPaletteReferences": [
            {"file": "../family-portrait-expressions-v1/manifest.json", "sha256": digest(IDENTITY_REF), "role": "text-only character identity and palette reference; not sampled"}
        ],
        "sourceFiles": [{"file": "build_chat_avatars.py", "sha256": digest(ROOT / "build_chat_avatars.py")}],
    }
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    manifest = {
        "schemaVersion": 1,
        "batch": "chat-avatar-acting-v1",
        "assetFamily": "liveit.pixel.v2.chat-avatar.acting.concept",
        "description": "Compact named-character chat portraits with age-safe listening, curious, concerned, reassuring, speaking and blink states.",
        "cell": {"width": SIZE, "height": SIZE, "sampling": "nearest-neighbor", "transparentBackground": True},
        "atlas": {"file": atlas_path.name, "columns": len(STATES), "rows": len(CHARACTERS), "sha256": digest(atlas_path)},
        "preview": {"file": contact_path.name, "scale": 3, "sha256": digest(contact_path)},
        "characters": [
            {k: person[k] for k in ("id", "name", "ageGroup", "role", "identity")}
            for person in CHARACTERS
        ],
        "states": list(STATES),
        "frameCount": len(rows), "frames": rows,
        "provenanceFile": "provenance.json",
        "provenance": provenance,
        "runtimeReady": False,
        "limitations": [
            "Concept sprites need human pixel-art and identity review at target device scale.",
            "No chat component consumes these frames yet; timing values are suggestions only.",
            "Niko's states are ordinary child-safe conversation cues; romance-coded states are intentionally absent.",
        ],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
