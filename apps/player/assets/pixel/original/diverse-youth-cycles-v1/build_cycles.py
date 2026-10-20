#!/usr/bin/env python3
"""Build two original 24x32 four-direction youth walk cycles.

The art is authored as deterministic pixel clusters here.  No supplied ZIP
contents or downloaded art is read by this script.  Each profile has its own
silhouette, palette, hair, and outfit cues; east and west are authored
separately so directional coverage is not a mirrored export.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
W, H = 24, 32
DIRECTIONS = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b"]

PROFILES = {
    "child-mika": {
        "stage": "child",
        "description": "small, springy child with round curls, coral hoodie and teal shoes",
        "skin": (128, 78, 57, 255),
        "skin_hi": (166, 104, 76, 255),
        "hair": (37, 27, 31, 255),
        "hair_hi": (71, 42, 43, 255),
        "top": (210, 86, 91, 255),
        "top_hi": (245, 122, 105, 255),
        "bottom": (218, 166, 62, 255),
        "shoe": (36, 151, 146, 255),
        "shoe_hi": (95, 211, 184, 255),
        "accent": (242, 211, 93, 255),
        "bag": (38, 102, 116, 255),
        "height": 22,
        "head_w": 8,
        "hair_shape": "curls",
        "phase_sway": 0,
    },
    "teen-ravi": {
        "stage": "teen",
        "description": "tall teen with side-swept auburn hair, slate jacket, orange trousers and messenger bag",
        "skin": (177, 119, 83, 255),
        "skin_hi": (215, 153, 109, 255),
        "hair": (93, 47, 37, 255),
        "hair_hi": (155, 77, 49, 255),
        "top": (54, 83, 111, 255),
        "top_hi": (86, 129, 151, 255),
        "bottom": (193, 91, 48, 255),
        "shoe": (43, 48, 63, 255),
        "shoe_hi": (104, 115, 130, 255),
        "accent": (232, 183, 67, 255),
        "bag": (92, 54, 76, 255),
        "height": 26,
        "head_w": 7,
        "hair_shape": "sweep",
        "phase_sway": 1,
    },
}


def rect(d: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color) -> None:
    x0, y0, x1, y1 = box
    d.rectangle((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)), fill=color)


def poly(d: ImageDraw.ImageDraw, points, color) -> None:
    d.polygon(points, fill=color)


def profile_body(profile: dict, direction: str, phase: int) -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    skin, skin_hi = profile["skin"], profile["skin_hi"]
    hair, hair_hi = profile["hair"], profile["hair_hi"]
    top, top_hi = profile["top"], profile["top_hi"]
    bottom, shoe, shoe_hi = profile["bottom"], profile["shoe"], profile["shoe_hi"]
    accent, bag = profile["accent"], profile["bag"]
    tall = profile["stage"] == "teen"
    y0 = 3 if tall else 6
    head_y = y0 + 1
    # A four-frame gait uses opposite foot extension and a small torso sway.
    stride = ((phase + profile["phase_sway"]) % 4)
    # Exaggerated readable gait at 1x: contact frames open the feet, passing
    # frames pull them under the hips and lift one toe.  The arms swing in the
    # opposite phase so the four cells do not read as a static pose.
    gait = [
        (-3, 3, 0, 0, -2, 2),
        (-1, 1, -2, -1, 2, -1),
        (3, -3, 0, 0, 2, -2),
        (1, -1, -1, -2, -2, 1),
    ][stride]
    left_step, right_step, left_lift, right_lift, left_arm, right_arm = gait
    bob = [0, -1, 0, 1][stride] if tall else [0, 0, -1, 0][stride]
    cx = 12 + (1 if direction == "east" else -1 if direction == "west" else 0)

    if direction == "south":
        # Back leg/shadow first makes the front-facing silhouette readable.
        rect(d, (cx - 5 + left_step, 25 + bob + left_lift, cx - 2 + left_step, 29 + bob + left_lift), bottom)
        rect(d, (cx + 2 + right_step, 25 + bob + right_lift, cx + 5 + right_step, 29 + bob + right_lift), bottom)
        rect(d, (cx - 6 + left_step, 29 + bob + left_lift, cx - 1 + left_step, 30 + bob + left_lift), shoe)
        rect(d, (cx + 1 + right_step, 29 + bob + right_lift, cx + 6 + right_step, 30 + bob + right_lift), shoe)
        rect(d, (cx - 6 + left_step, 30 + bob + left_lift, cx - 1 + left_step, 30 + bob + left_lift), shoe_hi)
        rect(d, (cx + 1 + right_step, 30 + bob + right_lift, cx + 6 + right_step, 30 + bob + right_lift), shoe_hi)
        # Hoodie/jacket torso and arms.
        rect(d, (cx - 7, 16 + bob, cx + 6, 25 + bob), top)
        rect(d, (cx - 6, 17 + bob, cx + 5, 19 + bob), top_hi)
        rect(d, (cx - 8, 18 + bob + left_arm, cx - 6, 24 + bob + left_arm), skin)
        rect(d, (cx + 6, 18 + bob + right_arm, cx + 8, 24 + bob + right_arm), skin)
        rect(d, (cx - 8, 23 + bob + left_arm, cx - 6, 25 + bob + left_arm), skin_hi)
        rect(d, (cx + 6, 23 + bob + right_arm, cx + 8, 25 + bob + right_arm), skin_hi)
        # Neck and face.
        rect(d, (cx - 2, 13 + bob, cx + 2, 17 + bob), skin)
        rect(d, (cx - 4, head_y + bob, cx + 4, 14 + bob), skin)
        rect(d, (cx - 3, head_y + bob, cx + 3, head_y + 1 + bob), skin_hi)
        if profile["hair_shape"] == "curls":
            rect(d, (cx - 5, head_y - 1 + bob, cx + 5, head_y + 2 + bob), hair)
            for x, y in ((cx - 6, head_y + 1), (cx + 5, head_y + 2), (cx - 4, head_y - 2), (cx + 2, head_y - 2)):
                rect(d, (x, y + bob, x + 2, y + 2 + bob), hair)
            rect(d, (cx - 3, head_y - 1 + bob, cx + 1, head_y + bob), hair_hi)
        else:
            rect(d, (cx - 4, head_y - 1 + bob, cx + 4, head_y + 2 + bob), hair)
            rect(d, (cx - 3, head_y - 2 + bob, cx + 3, head_y - 1 + bob), hair_hi)
            rect(d, (cx + 2, head_y + bob, cx + 5, head_y + 3 + bob), hair)
        # Face pixels, collar and emblem.
        rect(d, (cx - 3, 10 + bob, cx - 2, 11 + bob), hair)
        rect(d, (cx + 2, 10 + bob, cx + 3, 11 + bob), hair)
        rect(d, (cx - 1, 13 + bob, cx + 1, 13 + bob), skin_hi)
        rect(d, (cx - 1, 16 + bob, cx + 1, 17 + bob), accent)
        if tall:
            rect(d, (cx - 5, 17 + bob, cx - 4, 24 + bob), bag)
            rect(d, (cx + 3, 17 + bob, cx + 4, 18 + bob), accent)
    elif direction == "north":
        rect(d, (cx - 5 + left_step, 25 + bob + left_lift, cx - 2 + left_step, 29 + bob + left_lift), bottom)
        rect(d, (cx + 2 + right_step, 25 + bob + right_lift, cx + 5 + right_step, 29 + bob + right_lift), bottom)
        rect(d, (cx - 6 + left_step, 29 + bob + left_lift, cx - 1 + left_step, 30 + bob + left_lift), shoe)
        rect(d, (cx + 1 + right_step, 29 + bob + right_lift, cx + 6 + right_step, 30 + bob + right_lift), shoe)
        rect(d, (cx - 6 + left_step, 30 + bob + left_lift, cx - 1 + left_step, 30 + bob + left_lift), shoe_hi)
        rect(d, (cx + 1 + right_step, 30 + bob + right_lift, cx + 6 + right_step, 30 + bob + right_lift), shoe_hi)
        rect(d, (cx - 7, 16 + bob, cx + 6, 25 + bob), top)
        rect(d, (cx - 5, 17 + bob, cx + 4, 23 + bob), bag)
        rect(d, (cx - 6, 17 + bob, cx + 5, 18 + bob), top_hi)
        rect(d, (cx - 8, 18 + bob + left_arm, cx - 6, 24 + bob + left_arm), skin)
        rect(d, (cx + 6, 18 + bob + right_arm, cx + 8, 24 + bob + right_arm), skin)
        rect(d, (cx - 2, 13 + bob, cx + 2, 17 + bob), skin)
        rect(d, (cx - 5, head_y + bob, cx + 5, 14 + bob), hair)
        rect(d, (cx - 3, head_y - 1 + bob, cx + 3, head_y + 1 + bob), hair_hi)
        if tall:
            rect(d, (cx + 4, 18 + bob, cx + 5, 22 + bob), accent)
    else:
        # Profiles are authored independently: face projection, one visible arm,
        # bag placement, and asymmetrical foot offsets differ by direction.
        s = 1 if direction == "east" else -1
        front = cx + 5 * s
        back = cx - 5 * s
        rect(d, (cx - 3 + left_step, 25 + bob + left_lift, cx + 1 + left_step, 29 + bob + left_lift), bottom)
        rect(d, (cx - 1 + right_step, 25 + bob + right_lift, cx + 4 + right_step, 29 + bob + right_lift), bottom)
        rect(d, (cx - 4 + left_step, 29 + bob + left_lift, cx + 1 + left_step, 30 + bob + left_lift), shoe)
        rect(d, (cx + 1 + right_step, 29 + bob + right_lift, cx + 6 + right_step, 30 + bob + right_lift), shoe)
        rect(d, (cx - 4 + left_step, 30 + bob + left_lift, cx + 1 + left_step, 30 + bob + left_lift), shoe_hi)
        rect(d, (cx + 1 + right_step, 30 + bob + right_lift, cx + 6 + right_step, 30 + bob + right_lift), shoe_hi)
        rect(d, (cx - 5, 16 + bob, cx + 5, 25 + bob), top)
        rect(d, (cx - 4, 17 + bob, cx + 3, 19 + bob), top_hi)
        rect(d, (front - s, 18 + bob + left_arm, front + s, 24 + bob + left_arm), skin)
        rect(d, (back, 18 + bob + right_arm, back + s, 23 + bob + right_arm), bag if tall else top_hi)
        rect(d, (cx - 2, 13 + bob, cx + 2, 17 + bob), skin)
        rect(d, (cx - 4, head_y + bob, cx + 3, 14 + bob), skin)
        # Projection creates unmistakable left/right authored differences.
        rect(d, (front + s, 9 + bob, front + 3 * s, 11 + bob), skin_hi)
        rect(d, (front + 2 * s, 10 + bob, front + 3 * s, 11 + bob), hair)
        rect(d, (cx - 4, head_y - 1 + bob, cx + 2, head_y + 2 + bob), hair)
        if profile["hair_shape"] == "curls":
            rect(d, (back - s, head_y + 1 + bob, back + s, head_y + 4 + bob), hair)
            rect(d, (cx - 2, head_y - 1 + bob, cx, head_y + bob), hair_hi)
        else:
            rect(d, (back - s, head_y - 1 + bob, back + s, head_y + 2 + bob), hair_hi)
            rect(d, (back - 2 * s, head_y + 1 + bob, back - s, head_y + 5 + bob), hair)
        rect(d, (front + s, 13 + bob, front + 2 * s, 13 + bob), hair)
        if tall:
            rect(d, (back - s, 17 + bob, back, 22 + bob), bag)
            rect(d, (cx + s, 17 + bob, cx + 2 * s, 18 + bob), accent)
        else:
            rect(d, (cx - s, 17 + bob, cx + s, 18 + bob), accent)
    return im


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    (ROOT / "frames").mkdir(exist_ok=True)
    atlas = Image.new("RGBA", (W * 4, H * 8), (0, 0, 0, 0))
    preview = Image.new("RGBA", (W * 4 * 4, H * 8 * 4), (0, 0, 0, 0))
    frame_records = []
    for row, (identity, profile) in enumerate(PROFILES.items()):
        for dir_index, direction in enumerate(DIRECTIONS):
            atlas_row = row * 4 + dir_index
            for phase_index, phase in enumerate(PHASES):
                im = profile_body(profile, direction, phase_index)
                rel = Path("frames") / identity / f"{identity}-{direction}-{phase}.png"
                out = ROOT / rel
                out.parent.mkdir(exist_ok=True)
                im.save(out)
                atlas.paste(im, (phase_index * W, atlas_row * H))
                frame_records.append({
                    "id": f"{identity}/{direction}/{phase}",
                    "identity": identity,
                    "stage": profile["stage"],
                    "direction": direction,
                    "phase": phase,
                    "file": rel.as_posix(),
                    "size": [W, H],
                    "pivot": [12, 31],
                    "runtimeReady": False,
                })
    atlas_path = ROOT / "diverse-youth-cycles-atlas.png"
    atlas.save(atlas_path)
    preview = atlas.resize((atlas.width * 4, atlas.height * 4), Image.Resampling.NEAREST)
    review_bg = Image.new("RGBA", preview.size, (246, 239, 218, 255))
    review_bg.alpha_composite(preview)
    review_bg.save(ROOT / "diverse-youth-cycles-preview-4x.png")
    spec_path = ROOT / "identity-spec.json"
    spec_path.write_text(json.dumps({"schemaVersion": 1, "profiles": PROFILES, "sourcePolicy": "original deterministic pixel clusters; no external art inputs"}, indent=2) + "\n")
    builder_hash = sha(Path(__file__))
    source_hash = sha(spec_path)
    for rec in frame_records:
        rec["sha256"] = sha(ROOT / rec["file"])
        rec["sourceSpec"] = "identity-spec.json"
        rec["sourceSpecSha256"] = source_hash
        rec["builderSha256"] = builder_hash
    manifest = {
        "schemaVersion": 1,
        "assetId": "diverse-youth-cycles-v1",
        "description": "Two original, visually distinct child and teen four-direction four-phase walk cycles.",
        "runtimeReady": False,
        "frameSize": [W, H],
        "pivot": [12, 31],
        "directions": DIRECTIONS,
        "phases": PHASES,
        "identities": [{"id": k, "stage": v["stage"], "description": v["description"], "frameCount": 16, "runtimeReady": False} for k, v in PROFILES.items()],
        "atlas": {"file": atlas_path.name, "size": list(atlas.size), "order": "identity rows, direction rows, phase columns"},
        "preview": "diverse-youth-cycles-preview-4x.png",
        "sourceSpec": {"file": spec_path.name, "sha256": source_hash},
        "builder": {"file": Path(__file__).name, "sha256": builder_hash},
        "frames": frame_records,
        "limitations": ["Concept batch only: needs pixel cleanup, palette lock, collision review, animation timing, and renderer acceptance before integration."],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    provenance = {
        "batch": "diverse-youth-cycles-v1",
        "sourcePolicy": "All pixels are authored by the deterministic local builder; no supplied ZIP or third-party asset was read.",
        "artDirection": "ordinary-life top-down pixel sprites; readable silhouettes at 1x; direction-specific construction; no horizontal mirroring",
        "profiles": {k: {"stage": v["stage"], "silhouette": v["description"], "palette": {p: list(v[p]) for p in ("skin", "hair", "top", "bottom", "shoe", "accent", "bag")}} for k, v in PROFILES.items()},
        "exactGeneration": "python3 build_cycles.py",
        "runtimeReady": False,
    }
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")


if __name__ == "__main__":
    main()
