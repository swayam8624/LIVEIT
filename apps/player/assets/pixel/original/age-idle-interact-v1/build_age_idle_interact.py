"""Build the age-arc idle and interact concept frames.

The directional-age-refine-v1 movement studies are the source of the body
silhouettes.  This script makes a separate, reproducible concept pack by
reusing one stable movement frame per direction and adding small, age-aware
pixel clusters for breathing, waving, reading, holding a toy, or using a
cane.  The source pack is never edited and this pack remains outside runtime
intake until an artist and renderer review it.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
SOURCE_ROOT = ROOT.parent / "directional-age-refine-v1"
W, H = 24, 32
STAGES = [
    ("infant-crawl", "infant"),
    ("toddler-waddle", "toddler"),
    ("child-walk", "child"),
    ("teen-walk", "teen"),
    ("adult-walk", "adult"),
    ("elder-woman-walk", "elder-woman"),
    ("elder-man-walk", "elder-man"),
]
DIRECTIONS = ["south", "west", "east", "north"]
POSES = ["idle", "interact"]
SOURCE_PHASE = {"idle": "contact-a", "interact": "passing-b"}
P = {
    "ink": (30, 31, 52, 255),
    "skin": (220, 154, 118, 255),
    "gold": (242, 190, 83, 255),
    "cream": (255, 231, 174, 255),
    "teal": (79, 184, 167, 255),
    "coral": (246, 134, 115, 255),
    "blue": (103, 142, 193, 255),
    "toy": (216, 91, 101, 255),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: str) -> None:
    x0, y0, x1, y1 = box
    draw.rectangle((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)), fill=P[color])


def add_idle(draw: ImageDraw.ImageDraw, stage: str, direction: str) -> str:
    """Draw a quiet, age-specific idle cue and return its cue name."""
    if stage == "infant":
        # A safe tummy-time rest: little blanket edge and a pacifier-like dot.
        rect(draw, (5, 26, 18, 27), "teal")
        rect(draw, (18 if direction != "west" else 5, 20, 19 if direction != "west" else 6, 21), "toy")
        return "tummy-rest"
    if stage == "toddler":
        rect(draw, (9, 23, 10, 25), "gold")
        rect(draw, (10, 24, 12, 25), "gold")
        return "comfort-clasp"
    if stage == "child":
        rect(draw, (16 if direction != "west" else 6, 15, 18 if direction != "west" else 8, 17), "toy")
        return "small-toy-hold"
    if stage == "teen":
        rect(draw, (8, 17, 10, 19), "blue")
        rect(draw, (14, 17, 16, 19), "blue")
        return "backpack-rest"
    if stage == "adult":
        rect(draw, (9, 18, 11, 20), "cream")
        rect(draw, (13, 18, 15, 20), "cream")
        return "hands-rest"
    if stage == "elder-woman":
        rect(draw, (7 if direction != "east" else 15, 19, 9 if direction != "east" else 17, 21), "gold")
        return "shawl-rest"
    rect(draw, (7 if direction != "east" else 15, 19, 8 if direction != "east" else 16, 23), "gold")
    return "cane-rest"


def add_interact(draw: ImageDraw.ImageDraw, stage: str, direction: str) -> str:
    """Draw an age-safe interaction cue that is still readable at 24x32."""
    side = -1 if direction == "west" else 1
    if direction == "north":
        side = 1
    x = 17 if side > 0 else 5
    if stage == "infant":
        # Reaches toward a soft toy, never a grown-up-coded gesture.
        rect(draw, (x, 18, x + side * 2, 19), "skin")
        rect(draw, (x + side * 2, 19, x + side * 4, 20), "toy")
        return "reach-for-toy"
    if stage == "toddler":
        rect(draw, (x, 12, x + side * 2, 15), "skin")
        rect(draw, (x + side * 2, 11, x + side * 3, 12), "gold")
        return "toddler-wave"
    if stage == "child":
        rect(draw, (x, 12, x + side * 2, 16), "skin")
        rect(draw, (x + side * 2, 11, x + side * 4, 15), "toy")
        return "show-toy"
    if stage == "teen":
        rect(draw, (x, 14, x + side * 2, 18), "skin")
        rect(draw, (x + side * 2, 14, x + side * 4, 17), "blue")
        return "offer-phone"
    if stage == "adult":
        rect(draw, (x, 12, x + side * 2, 16), "skin")
        rect(draw, (x + side * 2, 11, x + side * 3, 12), "gold")
        return "friendly-wave"
    if stage == "elder-woman":
        rect(draw, (x, 12, x + side * 2, 16), "skin")
        rect(draw, (x + side * 2, 11, x + side * 4, 13), "cream")
        return "offer-tea"
    rect(draw, (x, 12, x + side * 2, 16), "skin")
    rect(draw, (x + side * 2, 11, x + side * 3, 13), "gold")
    return "cane-greeting"


def make_frame(stage_id: str, stage: str, direction: str, pose: str) -> tuple[Image.Image, str, Path]:
    source_phase = SOURCE_PHASE[pose]
    source_path = SOURCE_ROOT / "frames" / stage_id / f"{stage_id}-{direction}-{source_phase}.png"
    im = Image.open(source_path).convert("RGBA")
    draw = ImageDraw.Draw(im)
    cue = add_idle(draw, stage, direction) if pose == "idle" else add_interact(draw, stage, direction)
    # A single low-alpha-free grounding pixel keeps the two pose families
    # mechanically distinguishable while retaining the source silhouette.
    if pose == "idle":
        rect(draw, (1, 30, 1, 30), "teal")
    else:
        rect(draw, (22, 30, 22, 30), "coral")
    return im, cue, source_path


def main() -> None:
    frames_dir = ROOT / "frames"
    frames_dir.mkdir(exist_ok=True)
    records: list[dict] = []
    source_records: dict[str, dict] = {}
    for stage_id, stage in STAGES:
        stage_dir = frames_dir / stage_id
        stage_dir.mkdir(exist_ok=True)
        atlas = Image.new("RGBA", (W * 2, H * 4), (0, 0, 0, 0))
        for row, direction in enumerate(DIRECTIONS):
            for col, pose in enumerate(POSES):
                im, cue, source_path = make_frame(stage_id, stage, direction, pose)
                filename = f"{stage_id}-{direction}-{pose}.png"
                out = stage_dir / filename
                im.save(out)
                atlas.paste(im, (col * W, row * H))
                # Store a repo-root path so provenance can be resolved directly
                # by asset audits and future import tooling.
                rel_source = source_path.relative_to(ROOT.parents[5])
                source_records[str(out.relative_to(ROOT))] = {
                    "sourceFrame": str(rel_source),
                    "sourceSha256": sha256(source_path),
                }
                records.append({
                    "id": f"{stage_id}/{direction}/{pose}",
                    "stage": stage_id,
                    "direction": direction,
                    "pose": pose,
                    "cue": cue,
                    "file": str(out.relative_to(ROOT)),
                    "sourceFrame": str(rel_source),
                    "x": col * W,
                    "y": row * H,
                    "width": W,
                    "height": H,
                    "pivot": {"x": 12, "y": 31},
                    "sha256": sha256(out),
                    "runtimeReady": False,
                })
        atlas.save(stage_dir / f"{stage_id}-idle-interact-atlas.png")

    # Review sheet: each stage is one 8-frame strip, enlarged with nearest-neighbor.
    preview = Image.new("RGBA", (W * 2 * 4, H * 4 * len(STAGES)), (18, 19, 34, 255))
    for row, (stage_id, _) in enumerate(STAGES):
        atlas = Image.open(frames_dir / stage_id / f"{stage_id}-idle-interact-atlas.png")
        preview.paste(atlas.resize((W * 2 * 4, H * 4), Image.Resampling.NEAREST), (0, row * H * 4))
    preview.save(ROOT / "age-idle-interact-preview-4x.png")

    manifest = {
        "schemaVersion": 1,
        "assetId": "age-idle-interact-v1",
        "status": "original-rights-safe-concept-study",
        "runtimeReady": False,
        "sourceTool": "Pillow deterministic overlays on directional-age-refine-v1 frames",
        "sourceMaster": "directional-age-refine-v1/frames/*",
        "logicalFrame": [W, H],
        "stages": [stage_id for stage_id, _ in STAGES],
        "directions": DIRECTIONS,
        "poses": POSES,
        "frameCount": len(records),
        "sampling": "nearest-neighbor",
        "suggestedDurationMs": {"idle": 520, "interact": 260},
        "frames": records,
        "sourceFrames": source_records,
        "limitations": [
            "These are one-frame pose studies, not animation timing, collision, or interaction logic.",
            "The body silhouettes are reused from directional-age-refine-v1 and require an artist pass for anatomy, clothing continuity, and identity matching.",
            "Infant and toddler gestures are intentionally limited to care-safe play, reaching, and waving cues; no adult-coded content is implied.",
            "No runtime atlas registration or renderer acceptance is implied.",
        ],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
