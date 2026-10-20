"""Build a small, deterministic pixel-cluster locomotion study.

This is intentionally hand-authored with Pillow primitives: each facing is
drawn independently so it cannot accidentally become a rotated single pose.
The resulting PNGs are concept studies and stay outside runtime intake.
"""

from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
W, H = 24, 32
STAGES = [
    ("infant-crawl", "infant", "crawl"),
    ("toddler-waddle", "toddler", "waddle"),
    ("child-walk", "child", "walk"),
    ("teen-walk", "teen", "walk"),
    ("adult-walk", "adult", "walk"),
    ("elder-woman-walk", "elder-woman", "walk"),
    ("elder-man-walk", "elder-man", "walk"),
]
DIRECTIONS = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b"]

P = {
    "outline": (30, 31, 52, 255), "shadow": (58, 51, 78, 255),
    "skin": (220, 154, 118, 255), "skin_hi": (247, 194, 148, 255),
    "hair": (62, 42, 57, 255), "hair_hi": (104, 61, 64, 255),
    "teal": (42, 129, 133, 255), "teal_hi": (79, 184, 167, 255),
    "coral": (216, 91, 101, 255), "coral_hi": (246, 134, 115, 255),
    "gold": (242, 190, 83, 255), "cream": (255, 231, 174, 255),
    "blue": (61, 93, 151, 255), "blue_hi": (103, 142, 193, 255),
    "white": (255, 244, 207, 255),
}

def px(d, box, color):
    x0, y0, x1, y1 = box
    d.rectangle((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)), fill=P[color])

def phase_offsets(phase: int):
    # Contact phases stretch one leg; passing phases tuck the legs under.
    return [(-2, 1), (1, 0), (2, -1), (-1, 0)][phase]

def draw_head(d, direction, stage, top, x=12):
    # Direction-specific head construction: faces, profiles, and backs differ.
    if stage == "infant":
        r = 4
    elif stage in ("toddler", "child"):
        r = 4
    else:
        r = 4
    if direction == "south":
        px(d, (x-r, top, x+r, top+2*r+1), "outline")
        px(d, (x-r+1, top+1, x+r-1, top+2*r), "skin")
        px(d, (x-r+1, top+1, x+r-1, top+2), "hair")
        if stage not in ("infant",):
            px(d, (x-2, top+4, x-1, top+4), "outline")
            px(d, (x+2, top+4, x+3, top+4), "outline")
            px(d, (x-1, top+6, x+1, top+6), "coral")
    elif direction in ("west", "east"):
        sign = -1 if direction == "west" else 1
        px(d, (x-3, top, x+3, top+8), "outline")
        px(d, (x-2, top+1, x+2, top+7), "skin")
        px(d, (x-2, top+1, x+2, top+2), "hair")
        nose_x = x + sign*3
        px(d, (nose_x, top+4, nose_x+sign, top+5), "skin_hi")
        px(d, (x+sign, top+4, x+sign+1, top+4), "outline")
    else:
        px(d, (x-r, top, x+r, top+2*r+1), "outline")
        px(d, (x-r+1, top+1, x+r-1, top+2*r), "hair")
        px(d, (x-2, top+2, x+2, top+3), "hair_hi")
    # Signature age details.
    if stage == "elder-woman":
        if direction == "south": px(d, (x+3, top+1, x+5, top+7), "cream")
        elif direction == "north": px(d, (x-5, top+1, x+5, top+3), "cream")
    if stage == "elder-man":
        px(d, (x-4, top, x+4, top+1), "blue")
        if direction == "west": px(d, (x-4, top+2, x-3, top+4), "blue_hi")
        if direction == "east": px(d, (x+3, top+2, x+4, top+4), "blue_hi")

def draw_person(stage, direction, phase):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    off_x, off_y = phase_offsets(phase)
    cx = 12
    if stage == "infant":
        # Low four-point crawl silhouette with independently drawn face/profile/back.
        top = 9
        draw_head(d, direction, stage, top, 14 if direction == "west" else 10 if direction == "east" else 12)
        px(d, (7, 16, 18, 22), "outline")
        px(d, (8, 17, 17, 21), "coral")
        px(d, (9, 18, 16, 20), "coral_hi")
        if direction == "north": px(d, (9, 17, 16, 18), "teal")
        arm = -1 if phase % 2 == 0 else 1
        px(d, (6+arm, 19, 8+arm, 24), "outline"); px(d, (7+arm, 20, 8+arm, 23), "skin")
        px(d, (16-arm, 19, 18-arm, 24), "outline"); px(d, (17-arm, 20, 18-arm, 23), "skin")
        px(d, (7+off_x, 22+off_y, 11+off_x, 26+off_y), "outline"); px(d, (8+off_x, 23+off_y, 10+off_x, 25+off_y), "skin")
        px(d, (13-off_x, 22-off_y, 17-off_x, 26-off_y), "outline"); px(d, (14-off_x, 23-off_y, 16-off_x, 25-off_y), "skin")
        px(d, (6, 26, 18, 27), "shadow")
        px(d, (4+phase, 28, 5+phase, 28), "teal_hi")
        return im
    tops = {"toddler": 4, "child": 3, "teen": 2, "adult": 2, "elder-woman": 2, "elder-man": 2}
    top = tops[stage]
    draw_head(d, direction, stage, top, cx)
    # Torso silhouette and age-specific proportions.
    body_top = top + 8
    body_bottom = {"toddler": 22, "child": 22, "teen": 22, "adult": 22, "elder-woman": 23, "elder-man": 23}[stage]
    left, right = ({"toddler": (8,16), "child": (8,16), "teen": (8,16), "adult": (7,17), "elder-woman": (7,17), "elder-man": (7,17)})[stage]
    px(d, (left-1, body_top, right+1, body_bottom), "outline")
    outfit = "teal" if stage in ("toddler", "adult", "elder-man") else "coral" if stage in ("child", "elder-woman") else "blue"
    outfit_hi = outfit + "_hi"
    px(d, (left, body_top+1, right, body_bottom-1), outfit)
    px(d, (left+2, body_top+2, right-2, body_top+4), outfit_hi)
    if stage == "elder-woman":
        px(d, (left-2, body_top+5, left, body_bottom-1), "cream")
        px(d, (right, body_top+5, right+2, body_bottom-1), "cream")
    if stage == "elder-man": px(d, (left+2, body_top+5, right-2, body_top+6), "cream")
    # Side-facing torsos expose a shoulder and one arm; backs show a collar.
    if direction == "north": px(d, (left+3, body_top+1, right-3, body_top+2), "hair_hi")
    if direction in ("west", "east"):
        s = -1 if direction == "west" else 1
        px(d, (cx+s*7, body_top+3, cx+s*9, body_bottom-2), "outline")
        px(d, (cx+s*8, body_top+4, cx+s*9, body_bottom-3), "skin")
    else:
        arm = -1 if phase % 2 == 0 else 1
        px(d, (left-3, body_top+3, left, body_top+10), "outline"); px(d, (left-2, body_top+4, left, body_top+9), "skin")
        px(d, (right, body_top+3, right+3, body_top+10), "outline"); px(d, (right+1, body_top+4, right+2, body_top+9), "skin")
        px(d, (left-3+arm, body_top+9, left-1+arm, body_top+10), "skin_hi")
    # Legs are drawn as two separate clusters with phase-specific gait.
    leg_top = body_bottom
    leg_a = off_x
    leg_b = -off_x
    px(d, (cx-4+leg_a, leg_top, cx-1+leg_a, 29), "outline")
    px(d, (cx-3+leg_a, leg_top+1, cx-2+leg_a, 28), "blue" if stage != "elder-woman" else "coral")
    px(d, (cx+1+leg_b, leg_top, cx+4+leg_b, 29), "outline")
    px(d, (cx+2+leg_b, leg_top+1, cx+3+leg_b, 28), "blue" if stage != "elder-woman" else "coral")
    px(d, (cx-5+leg_a, 29, cx-1+leg_a, 30), "outline")
    px(d, (cx+1+leg_b, 29, cx+5+leg_b, 30), "outline")
    if stage == "elder-man":
        cane_x = cx + (6 if direction != "west" else -6)
        px(d, (cane_x, 19, cane_x, 30), "gold")
        px(d, (cane_x-1, 18, cane_x+1, 19), "gold")
    # A tiny phase marker keeps frames mechanically distinct while remaining artful.
    px(d, (2 + phase*2, 31, 2 + phase*2, 31), "teal_hi")
    return im

def main():
    (ROOT / "frames").mkdir(exist_ok=True)
    source = Image.new("RGBA", (W * len(PHASES), H * len(STAGES)), (18, 19, 34, 255))
    frames = []
    for row, (stage_id, stage, locomotion) in enumerate(STAGES):
        stage_dir = ROOT / "frames" / stage_id
        stage_dir.mkdir(exist_ok=True)
        atlas = Image.new("RGBA", (W*4, H*4), (0, 0, 0, 0))
        for direction_row, direction in enumerate(DIRECTIONS):
            for phase_col, phase_name in enumerate(PHASES):
                im = draw_person(stage, direction, phase_col)
                name = f"{stage_id}-{direction}-{phase_name}.png"
                im.save(stage_dir / name)
                atlas.paste(im, (phase_col*W, direction_row*H))
                source.paste(im, (phase_col*W, (row)*H))
                frames.append({
                    "id": f"{stage_id}/{direction}/{phase_name}",
                    "stage": stage_id, "direction": direction, "phase": phase_name,
                    "file": f"frames/{stage_id}/{name}", "x": phase_col*W,
                    "y": direction_row*H, "width": W, "height": H,
                    "pivot": {"x": 12, "y": 31}, "runtimeReady": False,
                })
        atlas.save(stage_dir / f"{stage_id}-atlas.png")
    source.save(ROOT / "directional-age-refine-source.png")
    # 4x nearest preview, arranged as seven stage strips (each strip is a 4x4 atlas).
    preview = Image.new("RGBA", (W*4*4, H*4*len(STAGES)), (18, 19, 34, 255))
    for row, (stage_id, _, _) in enumerate(STAGES):
        im = Image.open(ROOT / "frames" / stage_id / f"{stage_id}-atlas.png")
        preview.paste(im.resize((W*4*4, H*4*4), Image.Resampling.NEAREST), (0, row*H*4*4))
    preview.save(ROOT / "directional-age-refine-preview-4x.png")
    manifest = {
        "schemaVersion": 1, "assetId": "directional-age-refine-v1",
        "status": "original-hand-authored-pixel-cluster-study", "runtimeReady": False,
        "sourceTool": "Pillow deterministic hand-authored primitives",
        "sourceMaster": "directional-age-refine-source.png", "logicalFrame": [W, H],
        "directions": DIRECTIONS, "phases": PHASES,
        "sampling": "nearest-neighbor", "suggestedDurationMs": 140,
        "palette": {k: list(v[:3]) for k, v in P.items()}, "frameCount": len(frames),
        "frames": frames,
        "limitations": [
            "A small logical resolution study; anatomy, hair and clothing need artist review before integration.",
            "The infant uses a crawl silhouette and the elder-man cane is a concept accessory, not collision data.",
            "No runtime atlas registration, collision box, or renderer acceptance is implied.",
        ],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
