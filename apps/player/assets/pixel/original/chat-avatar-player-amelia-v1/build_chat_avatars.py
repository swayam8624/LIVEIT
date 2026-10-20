#!/usr/bin/env python3
"""Draw compact player life-stage and Amelia chat avatars from pixel primitives."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FRAME_DIR = ROOT / "frames"
SIZE = 48
STATES = ("listening", "curious", "concerned", "reassuring", "speaking", "blink")
CHARACTERS = [
    {"id": "player-infant", "name": "Player — infant", "role": "player life-stage concept", "ageGroup": "infant", "ageSafe": True, "face": "#f2bb91", "hair": "#9d4b2e", "hairLight": "#c96739", "coat": "#f0dfc2", "accent": "#258f82", "bg": "#365448", "outline": "#342633", "style": "baby", "stageIndex": 0},
    {"id": "player-toddler", "name": "Player — toddler", "role": "player life-stage concept", "ageGroup": "toddler", "ageSafe": True, "face": "#edb38a", "hair": "#99462c", "hairLight": "#c26036", "coat": "#ead9bc", "accent": "#258f82", "bg": "#365448", "outline": "#342633", "style": "toddler", "stageIndex": 1},
    {"id": "player-child", "name": "Player — child", "role": "player life-stage concept", "ageGroup": "child", "ageSafe": True, "face": "#e9ad83", "hair": "#91432b", "hairLight": "#c26437", "coat": "#ddd0b2", "accent": "#258f82", "bg": "#365448", "outline": "#342633", "style": "child", "stageIndex": 2},
    {"id": "player-teen", "name": "Player — teen", "role": "player life-stage concept", "ageGroup": "teen", "ageSafe": True, "face": "#e8ae84", "hair": "#8f4029", "hairLight": "#c36536", "coat": "#d8cfb6", "accent": "#258f82", "bg": "#365448", "outline": "#342633", "style": "teen", "stageIndex": 3},
    {"id": "player-young-adult", "name": "Player — young adult", "role": "player life-stage concept", "ageGroup": "young-adult", "ageSafe": True, "face": "#e7b18b", "hair": "#8d422a", "hairLight": "#c56a38", "coat": "#293c4b", "accent": "#258f82", "bg": "#365448", "outline": "#342633", "style": "young-adult", "stageIndex": 4},
    {"id": "player-midlife", "name": "Player — midlife", "role": "player life-stage concept", "ageGroup": "midlife", "ageSafe": True, "face": "#e2ad87", "hair": "#77402d", "hairLight": "#b96b41", "coat": "#334b48", "accent": "#258f82", "bg": "#365448", "outline": "#342633", "style": "midlife", "stageIndex": 5},
    {"id": "player-elder", "name": "Player — elder", "role": "player life-stage concept", "ageGroup": "elder", "ageSafe": True, "face": "#d9a887", "hair": "#bbb4a6", "hairLight": "#e3d6c2", "coat": "#52605a", "accent": "#258f82", "bg": "#365448", "outline": "#342633", "style": "elder", "stageIndex": 6},
    {"id": "amelia", "name": "Amelia", "role": "adult named character", "ageGroup": "adult", "ageSafe": True, "face": "#e4aa7e", "hair": "#382528", "hairLight": "#714237", "coat": "#efe3cd", "accent": "#288f84", "bg": "#344c55", "outline": "#29202b", "style": "amelia", "stageIndex": None},
]
STATE_META = {
    "listening": {"label": "Listening", "meaning": "calm attention", "durationMs": None},
    "curious": {"label": "Curious", "meaning": "open question or interest", "durationMs": None},
    "concerned": {"label": "Concerned", "meaning": "gentle worry or empathy", "durationMs": None},
    "reassuring": {"label": "Reassuring", "meaning": "warm support", "durationMs": None},
    "speaking": {"label": "Speaking", "meaning": "brief open-mouth speech cue; infant and toddler frames indicate babbling only", "durationMs": 120},
    "blink": {"label": "Blink", "meaning": "brief closed-eye idle frame", "durationMs": 100},
}


def rgba(value: str) -> tuple[int, int, int, int]:
    return tuple(bytes.fromhex(value.removeprefix("#"))) + (255,)


def rect(draw: ImageDraw.ImageDraw, bounds: tuple[int, int, int, int], color: str) -> None:
    draw.rectangle(bounds, fill=rgba(color))


def draw_backdrop(draw: ImageDraw.ImageDraw, color: str) -> None:
    # Identical pixel-circle silhouette across the player's life arc anchors continuity.
    for y, left, right in (
        (4, 18, 29), (5, 14, 33), (6, 11, 36), (7, 9, 38), (8, 7, 40),
        (9, 6, 41), (10, 5, 42), (11, 4, 43), (12, 3, 44), (13, 3, 44),
        (14, 2, 45), (15, 2, 45), (16, 2, 45), (17, 1, 46), (18, 1, 46),
        (19, 1, 46), (20, 1, 46), (21, 1, 46), (22, 1, 46), (23, 1, 46),
        (24, 1, 46), (25, 1, 46), (26, 2, 45), (27, 2, 45), (28, 2, 45),
        (29, 3, 44), (30, 3, 44), (31, 4, 43), (32, 5, 42), (33, 6, 41),
        (34, 7, 40), (35, 9, 38), (36, 11, 36), (37, 14, 33), (38, 18, 29),
    ):
        draw.line((left, y, right, y), fill=rgba(color))


def age_hair(d: ImageDraw.ImageDraw, character: dict, stage: str) -> None:
    hair, light = character["hair"], character["hairLight"]
    if stage == "baby":
        rect(d, (18, 12, 29, 16), hair)
        rect(d, (20, 10, 25, 13), light)
    elif stage == "toddler":
        for x, y, w in ((15, 9, 6), (21, 7, 6), (27, 9, 5), (13, 13, 5), (30, 13, 5)):
            rect(d, (x, y, x + w - 1, y + 4), hair)
        rect(d, (16, 10, 18, 11), light); rect(d, (25, 8, 27, 9), light)
        rect(d, (31, 10, 34, 12), character["accent"])
    elif stage == "child":
        rect(d, (13, 9, 34, 17), hair)
        rect(d, (14, 8, 20, 12), light); rect(d, (23, 8, 31, 11), hair)
        rect(d, (12, 14, 15, 22), hair); rect(d, (32, 14, 35, 19), hair)
        rect(d, (31, 12, 34, 13), character["accent"])
    elif stage == "teen":
        rect(d, (12, 9, 35, 16), hair)
        rect(d, (14, 7, 23, 11), hair); rect(d, (17, 8, 20, 9), light)
        rect(d, (12, 15, 15, 28), hair); rect(d, (32, 15, 35, 25), hair)
        rect(d, (13, 27, 16, 32), hair); rect(d, (33, 24, 35, 28), hair)
        rect(d, (13, 11, 16, 12), character["accent"])
    elif stage in ("young-adult", "midlife"):
        rect(d, (11, 8, 36, 16), hair)
        rect(d, (14, 6, 23, 10), hair); rect(d, (18, 6, 22, 7), light)
        rect(d, (11, 14, 15, 29), hair); rect(d, (33, 14, 37, 29), hair)
        rect(d, (12, 27, 16, 33), hair); rect(d, (33, 26, 36, 33), hair)
        if stage == "midlife":
            rect(d, (13, 15, 14, 20), "#d9b598"); rect(d, (34, 17, 35, 21), "#d9b598")
        rect(d, (14, 11, 17, 12), character["accent"])
    elif stage == "elder":
        rect(d, (11, 8, 36, 16), hair)
        rect(d, (14, 6, 23, 10), hair); rect(d, (18, 6, 22, 7), light)
        rect(d, (11, 14, 15, 29), hair); rect(d, (33, 14, 37, 29), hair)
        rect(d, (12, 27, 16, 33), hair); rect(d, (33, 26, 36, 33), hair)
        rect(d, (13, 13, 15, 16), light); rect(d, (33, 18, 35, 20), light)
    elif stage == "amelia":
        rect(d, (11, 9, 36, 17), hair)
        rect(d, (14, 6, 25, 11), hair); rect(d, (17, 7, 21, 9), light)
        rect(d, (11, 15, 15, 28), hair); rect(d, (33, 15, 37, 27), hair)
        rect(d, (12, 25, 17, 31), hair); rect(d, (32, 24, 36, 29), hair)


def frame(character: dict, state: str) -> Image.Image:
    im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    draw_backdrop(d, character["bg"])
    stage = character["style"]
    outline, skin = character["outline"], character["face"]
    infant = stage == "baby"
    toddler = stage == "toddler"

    # The head scales upward through the early stages; all face features share the same center.
    rect(d, (8, 34, 39, 44), outline)
    rect(d, (9, 35, 38, 43), character["coat"])
    rect(d, (18, 32, 29, 37), outline)
    rect(d, (19, 32, 28, 36), skin)
    if infant:
        rect(d, (13, 10, 34, 32), outline); rect(d, (14, 11, 33, 31), skin)
    elif toddler:
        rect(d, (12, 10, 35, 32), outline); rect(d, (13, 11, 34, 31), skin)
    else:
        rect(d, (13, 10, 34, 32), outline); rect(d, (14, 11, 33, 31), skin)
    rect(d, (11, 20, 14, 25), outline); rect(d, (12, 21, 14, 24), skin)
    rect(d, (33, 20, 36, 25), outline); rect(d, (33, 21, 35, 24), skin)
    age_hair(d, character, stage)

    # Expression features are small but distinct and occupy the same anchors per stage.
    if state == "curious":
        rect(d, (17, 18, 21, 18), outline); rect(d, (27, 16, 31, 17), outline)
    elif state == "concerned":
        rect(d, (17, 17, 21, 18), outline); rect(d, (27, 17, 31, 18), outline)
        rect(d, (20, 17, 21, 18), skin); rect(d, (27, 17, 28, 18), skin)
    elif state == "reassuring":
        rect(d, (17, 19, 21, 19), outline); rect(d, (27, 19, 31, 19), outline)
    else:
        rect(d, (17, 18, 21, 19), outline); rect(d, (27, 18, 31, 19), outline)

    eye_y = 21
    if state == "blink":
        rect(d, (17, eye_y, 21, eye_y + 1), outline); rect(d, (27, eye_y, 31, eye_y + 1), outline)
    else:
        eye_h = 4 if state == "curious" else (2 if state == "concerned" else 3)
        rect(d, (18, eye_y, 20, eye_y + eye_h - 1), outline)
        rect(d, (28, eye_y, 30, eye_y + eye_h - 1), outline)
        rect(d, (19, eye_y, 19, eye_y), "#fff0d6"); rect(d, (29, eye_y, 29, eye_y), "#fff0d6")

    rect(d, (23, 25, 24, 26), "#cb805e")
    if state == "speaking":
        rect(d, (21, 28, 26, 31), outline)
        rect(d, (22, 29, 25, 30), "#b9474e")
        if infant or toddler:
            rect(d, (23, 29, 24, 29), "#f3c5a5")  # soft babble mouth, not implied words
    elif state == "curious":
        rect(d, (22, 28, 25, 30), outline); rect(d, (23, 28, 24, 28), "#f3d7a8")
    elif state == "concerned":
        rect(d, (21, 29, 26, 30), outline); rect(d, (22, 29, 25, 29), skin)
    elif state == "reassuring":
        rect(d, (20, 28, 27, 29), outline); rect(d, (21, 28, 26, 28), skin)
        rect(d, (16, 27, 18, 28), "#d78370"); rect(d, (30, 27, 32, 28), "#d78370")
    else:
        rect(d, (21, 29, 26, 30), outline); rect(d, (22, 29, 25, 29), "#d48e70")

    # Clothing accent changes with age but remains a teal identity thread.
    rect(d, (18, 35, 29, 37), character["accent"])
    if character["id"] == "amelia":
        rect(d, (14, 31, 15, 32), character["accent"])
        rect(d, (33, 31, 34, 32), character["accent"])
    elif stage in ("young-adult", "midlife", "elder"):
        rect(d, (19, 37, 28, 40), character["accent"])
    return im


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    atlas = Image.new("RGBA", (SIZE * len(STATES), SIZE * len(CHARACTERS)), (0, 0, 0, 0))
    rows: list[dict] = []
    for row, person in enumerate(CHARACTERS):
        for col, state in enumerate(STATES):
            im = frame(person, state)
            path = FRAME_DIR / f"{person['id']}-{state}-48x48.png"
            im.save(path, optimize=True)
            atlas.alpha_composite(im, (col * SIZE, row * SIZE))
            rows.append({
                "id": f"liveit.pixel.v2.chat-avatar.{person['id']}.{state}",
                "characterId": person["id"], "characterName": person["name"],
                "role": person["role"], "ageGroup": person["ageGroup"],
                "ageSafety": "all-ages-safe", "playerAgeStageIndex": person["stageIndex"],
                "state": state, **STATE_META[state],
                "file": path.relative_to(ROOT).as_posix(),
                "x": col * SIZE, "y": row * SIZE, "width": SIZE, "height": SIZE,
                "pivot": {"x": 24, "y": 42}, "sha256": sha(path), "runtimeReady": False,
            })

    atlas_path = ROOT / "player-amelia-chat-avatars-atlas-6x8-48.png"
    atlas.save(atlas_path, optimize=True)
    preview_path = ROOT / "player-amelia-chat-avatars-preview-3x.png"
    margin, label_width, scale, row_gap, header = 10, 96, 3, 20, 22
    preview = Image.new("RGB", (margin * 2 + label_width + SIZE * scale * len(STATES), header + len(CHARACTERS) * (SIZE * scale + row_gap)), "#161f2e")
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(preview)
    for col, state in enumerate(STATES):
        x = margin + label_width + col * SIZE * scale + 4
        draw.text((x, 6), state, font=font, fill="#f5f2d9")
    for row, person in enumerate(CHARACTERS):
        y = header + row * (SIZE * scale + row_gap)
        draw.text((margin, y + 54), person["name"].replace("Player — ", "")[:13], font=font, fill="#f5f2d9")
        for col, state in enumerate(STATES):
            path = FRAME_DIR / f"{person['id']}-{state}-48x48.png"
            tile = Image.open(path).convert("RGBA").resize((SIZE * scale, SIZE * scale), Image.Resampling.NEAREST)
            preview.paste(tile, (margin + label_width + col * SIZE * scale, y), tile)
    preview.save(preview_path, optimize=True)

    refs = [
        {"file": "../player-age-arc-v1/frames.json", "path": ROOT.parent / "player-age-arc-v1" / "frames.json", "role": "age-stage and auburn/teal identity concept notes only; pixels not sampled"},
        {"file": "../portrait-acting-v1/amelia/frames.json", "path": ROOT.parent / "portrait-acting-v1" / "amelia" / "frames.json", "role": "adult Amelia hair and cream/teal palette concept notes only; pixels not sampled"},
    ]
    provenance = {
        "created": "2026-10-20",
        "method": "All avatar pixels are drawn from original geometric pixel primitives in build_chat_avatars.py. No reference image pixels, generated images, web assets, source archives, or third-party art are sampled or copied.",
        "identityPaletteReferences": [{"file": r["file"], "sha256": sha(r["path"]), "role": r["role"]} for r in refs],
        "sourceFiles": [{"file": "build_chat_avatars.py", "sha256": sha(ROOT / "build_chat_avatars.py")}],
        "ageSafety": "All states use everyday, non-romantic interaction cues. Infant and toddler speaking frames are mouth-open babble cues only; no words, intimacy, or adult-coded expression is implied.",
        "continuityNote": "The seven player rows represent one auburn-haired/teal-accent concept identity across age stages, not the full player appearance-customization range.",
    }
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    manifest = {
        "schemaVersion": 1, "batch": "chat-avatar-player-amelia-v1",
        "assetFamily": "liveit.pixel.v2.chat-avatar.player-life-arc-and-amelia.concept",
        "description": "Compact chat avatars for one player life arc and adult Amelia, with six age-safe conversation states each.",
        "cell": {"width": SIZE, "height": SIZE, "sampling": "nearest-neighbor", "transparentBackground": True},
        "atlas": {"file": atlas_path.name, "columns": len(STATES), "rows": len(CHARACTERS), "sha256": sha(atlas_path)},
        "preview": {"file": preview_path.name, "scale": scale, "sha256": sha(preview_path)},
        "characters": [{k: p[k] for k in ("id", "name", "role", "ageGroup", "stageIndex")} for p in CHARACTERS],
        "states": list(STATES), "frameCount": len(rows), "frames": rows,
        "provenanceFile": "provenance.json", "provenance": provenance,
        "runtimeReady": False,
        "limitations": [
            "Concept sprites need pixel-art cleanup, identity review, accessibility naming, and target-device scale review.",
            "No chat or dialogue component consumes these frames yet; suggested timings are not runtime behavior.",
            "The chosen player age arc is one concept appearance; it does not cover customizable player identities.",
        ],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
