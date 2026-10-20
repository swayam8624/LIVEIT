from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).parent
ASSET_ROOT = ROOT.parent
SOURCE_ROOT = ASSET_ROOT / "life-arc-early-cycles-v1"
DIRECTIONS = ["south", "west", "east", "north"]
POSES = ["idle", "interact"]
STAGES = [
    ("infant-crawl", "infant crawl", "tummy-rest", "reach-for-soft-toy"),
    ("toddler-waddle", "toddler waddle", "comfort-clasp", "toddler-wave"),
    ("child-walk", "child", "relaxed-stance", "show-keepsake"),
    ("teen-walk", "teen", "casual-stand", "check-keepsake"),
]

# The source sheets establish identity cues only. Every output silhouette is
# drawn below as new pixel clusters; no source pixels are copied or mirrored.
PALETTE = {
    "outline": (30, 27, 36, 255),
    "hair": (52, 31, 36, 255),
    "hair_hi": (83, 45, 42, 255),
    "skin": (144, 78, 58, 255),
    "skin_hi": (204, 121, 76, 255),
    "skin_shadow": (104, 55, 51, 255),
    "blue": (64, 143, 179, 255),
    "blue_hi": (107, 191, 218, 255),
    "blue_shadow": (37, 84, 117, 255),
    "gold": (235, 191, 83, 255),
    "gold_shadow": (164, 105, 49, 255),
    "pants": (48, 47, 65, 255),
    "pants_hi": (79, 76, 94, 255),
    "shoe": (31, 31, 42, 255),
    "toy": (239, 206, 104, 255),
    "paper": (214, 224, 181, 255),
    "eye": (250, 226, 164, 255),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_frame(stage: str, direction: str, phase: str) -> Path:
    return SOURCE_ROOT / stage / f"{stage}-{direction}-{phase}.png"


def rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: str) -> None:
    draw.rectangle(box, fill=PALETTE[color])


def poly(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], color: str) -> None:
    draw.polygon(points, fill=PALETTE[color])


def pixel(draw: ImageDraw.ImageDraw, x: int, y: int, color: str) -> None:
    rect(draw, (x, y, x, y), color)


def face(draw: ImageDraw.ImageDraw, direction: str, head: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = head
    rect(draw, head, "skin")
    rect(draw, (x0 + 1, y0, x1 - 1, y0 + 1), "skin_hi")
    if direction == "south":
        pixel(draw, x0 + 2, y0 + 3, "eye")
        pixel(draw, x1 - 2, y0 + 3, "eye")
        pixel(draw, x0 + 3, y0 + 5, "outline")
        pixel(draw, x1 - 3, y0 + 5, "outline")
    elif direction == "west":
        rect(draw, (x0 - 1, y0 + 3, x0, y0 + 4), "skin_hi")
        pixel(draw, x0 + 1, y0 + 3, "eye")
        pixel(draw, x0 + 2, y0 + 5, "outline")
    elif direction == "east":
        rect(draw, (x1, y0 + 3, x1 + 1, y0 + 4), "skin_hi")
        pixel(draw, x1 - 1, y0 + 3, "eye")
        pixel(draw, x1 - 2, y0 + 5, "outline")
    else:
        rect(draw, (x0 + 1, y0 + 2, x1 - 1, y0 + 3), "skin_shadow")
        pixel(draw, x0 + 2, y0 + 1, "hair_hi")


def hair(draw: ImageDraw.ImageDraw, direction: str, head: tuple[int, int, int, int]) -> None:
    x0, y0, x1, _ = head
    rect(draw, (x0, y0 - 2, x1, y0 + 1), "hair")
    rect(draw, (x0 + 1, y0 - 3, x1 - 1, y0 - 2), "hair")
    pixel(draw, x0 + 1, y0 - 1, "hair_hi")
    pixel(draw, x1 - 1, y0, "hair_hi")
    if direction == "west":
        rect(draw, (x0 - 1, y0 - 1, x0 + 1, y0 + 3), "hair")
    elif direction == "east":
        rect(draw, (x1 - 1, y0 - 1, x1 + 1, y0 + 3), "hair")
    elif direction == "north":
        rect(draw, (x0 + 1, y0 - 2, x1 - 1, y0), "hair_hi")


def infant(draw: ImageDraw.ImageDraw, direction: str, pose: str) -> None:
    # Low, horizontal crawl silhouette: head and knees keep a clear baby scale.
    if direction == "south":
        head = (8, 6, 15, 12)
        hair(draw, direction, head); face(draw, direction, head)
        poly(draw, [(7, 13), (16, 13), (19, 18), (17, 23), (7, 23), (5, 19)], "blue")
        rect(draw, (8, 15, 14, 20), "blue_hi")
        rect(draw, (5, 20, 9, 23), "skin")
        rect(draw, (15, 20, 19, 23), "skin_shadow")
        if pose == "idle":
            rect(draw, (5, 14, 8, 18), "skin")
            rect(draw, (16, 14, 19, 18), "skin_shadow")
        else:
            rect(draw, (3, 16, 9, 18), "skin_hi")
            rect(draw, (1, 16, 3, 17), "skin")
            rect(draw, (0, 14, 2, 16), "toy")
            pixel(draw, 1, 13, "blue_hi")
    elif direction == "west":
        head = (5, 7, 12, 13)
        hair(draw, direction, head); face(draw, direction, head)
        poly(draw, [(10, 13), (17, 14), (20, 19), (18, 23), (8, 23), (5, 19)], "blue")
        rect(draw, (11, 15, 17, 20), "blue_hi")
        rect(draw, (17, 20, 21, 23), "skin_shadow")
        rect(draw, (8, 20, 12, 23), "skin")
        if pose == "idle":
            rect(draw, (8, 14, 11, 18), "skin")
            rect(draw, (16, 15, 20, 18), "skin_shadow")
        else:
            rect(draw, (4, 16, 10, 18), "skin_hi")
            rect(draw, (1, 16, 4, 17), "skin")
            rect(draw, (0, 14, 2, 16), "toy")
            pixel(draw, 1, 13, "blue_hi")
    elif direction == "east":
        head = (12, 7, 19, 13)
        hair(draw, direction, head); face(draw, direction, head)
        poly(draw, [(7, 14), (14, 13), (19, 18), (16, 23), (6, 23), (4, 19)], "blue")
        rect(draw, (7, 15, 13, 20), "blue_hi")
        rect(draw, (4, 20, 8, 23), "skin_shadow")
        rect(draw, (13, 20, 17, 23), "skin")
        if pose == "idle":
            rect(draw, (5, 15, 9, 18), "skin_shadow")
            rect(draw, (14, 14, 17, 18), "skin")
        else:
            rect(draw, (15, 16, 21, 18), "skin_hi")
            rect(draw, (21, 16, 23, 17), "skin")
            rect(draw, (22, 14, 23, 16), "toy")
            pixel(draw, 22, 13, "blue_hi")
    else:
        head = (8, 6, 15, 12)
        hair(draw, direction, head); face(draw, direction, head)
        poly(draw, [(7, 13), (16, 13), (19, 18), (17, 23), (7, 23), (5, 19)], "blue")
        rect(draw, (8, 15, 14, 20), "blue_shadow")
        rect(draw, (5, 20, 9, 23), "skin")
        rect(draw, (15, 20, 19, 23), "skin_shadow")
        if pose == "idle":
            rect(draw, (5, 14, 8, 18), "skin")
            rect(draw, (16, 14, 19, 18), "skin_shadow")
        else:
            rect(draw, (8, 14, 11, 19), "skin_hi")
            rect(draw, (13, 14, 16, 19), "skin_shadow")
            rect(draw, (11, 18, 13, 20), "toy")


def toddler(draw: ImageDraw.ImageDraw, direction: str, pose: str) -> None:
    specs = {
        "south": ((9, 4, 15, 10), [(7, 11), (17, 11), (18, 19), (16, 23), (8, 23), (6, 19)]),
        "west": ((7, 4, 13, 10), [(10, 11), (17, 12), (18, 21), (9, 23), (6, 19)]),
        "east": ((11, 4, 17, 10), [(7, 12), (14, 11), (18, 19), (15, 23), (7, 22), (5, 18)]),
        "north": ((9, 4, 15, 10), [(7, 11), (17, 11), (18, 20), (16, 23), (8, 23), (6, 20)]),
    }
    head, body = specs[direction]
    hair(draw, direction, head); face(draw, direction, head)
    poly(draw, body, "blue")
    rect(draw, (head[0] + 1, 11, head[2] - 1, 15), "blue_hi")
    # Short legs with oversized toddler shoes.
    rect(draw, (8, 21, 11, 26), "skin")
    rect(draw, (14, 21, 17, 26), "skin_shadow")
    rect(draw, (7, 26, 11, 27), "shoe")
    rect(draw, (14, 26, 18, 27), "shoe")
    if pose == "idle":
        if direction == "south":
            rect(draw, (5, 13, 8, 19), "skin")
            rect(draw, (16, 13, 19, 19), "skin_shadow")
            rect(draw, (9, 17, 15, 19), "gold_shadow")
            rect(draw, (10, 16, 14, 18), "gold")
        elif direction == "west":
            rect(draw, (5, 13, 9, 19), "skin")
            rect(draw, (15, 14, 19, 19), "skin_shadow")
            rect(draw, (7, 17, 12, 19), "gold")
        elif direction == "east":
            rect(draw, (4, 14, 8, 19), "skin_shadow")
            rect(draw, (15, 13, 19, 19), "skin")
            rect(draw, (12, 17, 17, 19), "gold")
        else:
            rect(draw, (6, 14, 10, 19), "skin")
            rect(draw, (14, 14, 18, 19), "skin_shadow")
            rect(draw, (10, 17, 14, 19), "gold_shadow")
    else:
        # One arm lifts in each authored direction, with a distinct comfort/wave hand.
        if direction == "south":
            rect(draw, (4, 11, 8, 15), "skin_hi"); rect(draw, (3, 9, 6, 11), "skin")
            rect(draw, (16, 14, 20, 18), "skin_shadow")
            pixel(draw, 4, 8, "gold")
        elif direction == "west":
            rect(draw, (4, 10, 8, 14), "skin_hi"); rect(draw, (2, 8, 5, 10), "skin")
            rect(draw, (15, 15, 19, 19), "skin_shadow")
            pixel(draw, 3, 7, "gold")
        elif direction == "east":
            rect(draw, (16, 10, 20, 14), "skin_hi"); rect(draw, (19, 8, 22, 10), "skin")
            rect(draw, (4, 15, 8, 19), "skin_shadow")
            pixel(draw, 20, 7, "gold")
        else:
            rect(draw, (6, 10, 10, 14), "skin_hi"); rect(draw, (5, 8, 8, 10), "skin")
            rect(draw, (14, 14, 18, 19), "skin_shadow")
            pixel(draw, 6, 7, "gold")


def child(draw: ImageDraw.ImageDraw, direction: str, pose: str) -> None:
    heads = {"south": (9, 3, 15, 9), "west": (7, 3, 13, 9), "east": (11, 3, 17, 9), "north": (9, 3, 15, 9)}
    head = heads[direction]
    hair(draw, direction, head); face(draw, direction, head)
    rect(draw, (7 if direction != "east" else 6, 10, 17 if direction != "west" else 18, 18), "blue")
    rect(draw, (9, 10, 15, 14), "blue_hi")
    rect(draw, (8, 18, 11, 25), "pants")
    rect(draw, (14, 18, 17, 25), "pants_hi")
    rect(draw, (7, 25, 11, 27), "shoe")
    rect(draw, (14, 25, 18, 27), "shoe")
    if pose == "idle":
        arms = {
            "south": [(5, 11, 8, 18, "skin"), (16, 11, 19, 18, "skin_shadow")],
            "west": [(4, 11, 8, 18, "skin"), (16, 12, 20, 18, "skin_shadow")],
            "east": [(4, 12, 8, 18, "skin_shadow"), (16, 11, 20, 18, "skin")],
            "north": [(5, 12, 8, 18, "skin"), (16, 12, 19, 18, "skin_shadow")],
        }
        for x0, y0, x1, y1, c in arms[direction]:
            rect(draw, (x0, y0, x1, y1), c)
        rect(draw, (10, 16, 14, 18), "gold_shadow")
    else:
        # Keepsake is a deliberately large paper-colored book held outward.
        if direction == "south":
            rect(draw, (4, 11, 8, 16), "skin_hi"); rect(draw, (16, 11, 20, 16), "skin")
            rect(draw, (8, 14, 16, 19), "paper"); rect(draw, (9, 15, 15, 16), "gold")
        elif direction == "west":
            rect(draw, (3, 12, 8, 16), "skin_hi"); rect(draw, (15, 12, 19, 17), "skin_shadow")
            rect(draw, (5, 14, 12, 19), "paper"); rect(draw, (6, 15, 11, 16), "gold")
        elif direction == "east":
            rect(draw, (16, 12, 21, 16), "skin_hi"); rect(draw, (4, 12, 8, 17), "skin_shadow")
            rect(draw, (12, 14, 19, 19), "paper"); rect(draw, (13, 15, 18, 16), "gold")
        else:
            rect(draw, (5, 11, 9, 16), "skin_hi"); rect(draw, (15, 11, 19, 16), "skin")
            rect(draw, (9, 14, 15, 19), "paper"); rect(draw, (10, 15, 14, 16), "gold")


def teen(draw: ImageDraw.ImageDraw, direction: str, pose: str) -> None:
    heads = {"south": (9, 2, 15, 8), "west": (7, 2, 13, 8), "east": (11, 2, 17, 8), "north": (9, 2, 15, 8)}
    head = heads[direction]
    hair(draw, direction, head); face(draw, direction, head)
    torso = {"south": (7, 9, 17, 19), "west": (8, 9, 18, 19), "east": (6, 9, 16, 19), "north": (7, 9, 17, 19)}[direction]
    rect(draw, torso, "blue")
    rect(draw, (torso[0] + 2, 10, torso[2] - 2, 13), "blue_hi")
    rect(draw, (8, 19, 11, 27), "pants")
    rect(draw, (14, 19, 17, 27), "pants_hi")
    rect(draw, (7, 27, 11, 28), "shoe")
    rect(draw, (14, 27, 18, 28), "shoe")
    if pose == "idle":
        if direction == "south":
            rect(draw, (4, 10, 8, 19), "skin")
            rect(draw, (16, 10, 20, 19), "skin_shadow")
            pixel(draw, 7, 18, "gold")
            pixel(draw, 16, 18, "gold_shadow")
        elif direction == "west":
            rect(draw, (4, 11, 8, 19), "skin")
            rect(draw, (17, 11, 21, 19), "skin_shadow")
            pixel(draw, 7, 18, "gold")
        elif direction == "east":
            rect(draw, (3, 11, 7, 19), "skin_shadow")
            rect(draw, (15, 10, 19, 19), "skin")
            pixel(draw, 16, 18, "gold")
        else:
            rect(draw, (4, 11, 8, 19), "skin")
            rect(draw, (16, 11, 20, 19), "skin_shadow")
            pixel(draw, 7, 18, "gold")
    else:
        # The keepsake is held close, offset according to facing direction.
        if direction == "south":
            rect(draw, (7, 12, 11, 20), "skin_hi"); rect(draw, (14, 12, 18, 20), "skin")
            rect(draw, (10, 15, 14, 19), "paper"); rect(draw, (11, 16, 13, 17), "gold")
        elif direction == "west":
            rect(draw, (5, 12, 10, 19), "skin_hi"); rect(draw, (14, 12, 18, 19), "skin_shadow")
            rect(draw, (8, 15, 13, 19), "paper"); rect(draw, (9, 16, 12, 17), "gold")
        elif direction == "east":
            rect(draw, (14, 12, 19, 19), "skin_hi"); rect(draw, (5, 12, 9, 19), "skin_shadow")
            rect(draw, (11, 15, 16, 19), "paper"); rect(draw, (12, 16, 15, 17), "gold")
        else:
            rect(draw, (7, 12, 11, 20), "skin_hi"); rect(draw, (14, 12, 18, 20), "skin")
            rect(draw, (10, 15, 14, 19), "paper"); rect(draw, (11, 16, 13, 17), "gold")


DRAWERS = {"infant-crawl": infant, "toddler-waddle": toddler, "child-walk": child, "teen-walk": teen}


def render(stage: str, direction: str, pose: str) -> Image.Image:
    image = Image.new("RGBA", (24, 32), (0, 0, 0, 0))
    DRAWERS[stage](ImageDraw.Draw(image), direction, pose)
    return image


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    stage_records: list[dict] = []
    combined = Image.new("RGBA", (48, 128 * len(STAGES)), (0, 0, 0, 0))

    for stage_index, (stage, label, idle_cue, interact_cue) in enumerate(STAGES):
        stage_dir = ROOT / "frames" / stage
        stage_dir.mkdir(parents=True, exist_ok=True)
        atlas = Image.new("RGBA", (48, 128), (0, 0, 0, 0))
        stage_frames: list[dict] = []
        for direction_index, direction in enumerate(DIRECTIONS):
            for pose_index, pose in enumerate(POSES):
                source_path = source_frame(stage, direction, "contact-a" if pose == "idle" else "passing-b")
                if not source_path.exists():
                    raise FileNotFoundError(source_path)
                with Image.open(source_path) as source:
                    if source.size != (24, 32):
                        raise ValueError(f"Unexpected source size {source.size}: {source_path}")
                image = render(stage, direction, pose)
                output = stage_dir / f"{stage}-{direction}-{pose}.png"
                image.save(output)
                atlas.alpha_composite(image, (pose_index * 24, direction_index * 32))
                record = {
                    "id": f"{stage}/{direction}/{pose}",
                    "stage": stage,
                    "stageLabel": label,
                    "direction": direction,
                    "pose": pose,
                    "cue": idle_cue if pose == "idle" else interact_cue,
                    "file": str(output.relative_to(ASSET_ROOT)),
                    "sourceFrame": str(source_path.relative_to(ASSET_ROOT)),
                    "sourceFrameSha256": sha256(source_path),
                    "sourceUse": "identity palette and silhouette reference only; output redrawn as new pixel clusters",
                    "size": [24, 32],
                    "pivot": [12, 31],
                    "mode": "RGBA",
                    "sha256": sha256(output),
                    "runtimeReady": False,
                }
                records.append(record)
                stage_frames.append(record)

        atlas_path = ROOT / f"{stage}-idle-interact-atlas.png"
        atlas.save(atlas_path)
        combined.alpha_composite(atlas, (0, stage_index * 128))
        stage_records.append({
            "id": stage,
            "label": label,
            "atlas": atlas_path.name,
            "frameCount": len(stage_frames),
            "frames": stage_frames,
            "runtimeReady": False,
        })

    combined_path = ROOT / "linked-early-poses-v2-atlas-24x32.png"
    combined.save(combined_path)
    preview = combined.resize((combined.width * 4, combined.height * 4), Image.Resampling.NEAREST)
    preview_path = ROOT / "linked-early-poses-v2-preview-4x.png"
    preview.save(preview_path)
    manifest = {
        "schemaVersion": 1,
        "id": "linked-early-poses-v2",
        "status": "original-rights-safe-concept-study",
        "runtimeReady": False,
        "sourceTool": "Pillow deterministic hand-authored pixel-cluster drawing",
        "sourceBatch": "life-arc-early-cycles-v1",
        "identityCues": ["deep-brown skin", "coiled dark hair and recurring facial mark", "sky-blue clothing accents"],
        "frameSize": [24, 32],
        "pivot": [12, 31],
        "directions": DIRECTIONS,
        "poses": POSES,
        "stageCount": len(STAGES),
        "frameCount": len(records),
        "stages": stage_records,
        "combinedAtlas": {"file": combined_path.name, "size": list(combined.size), "mode": "RGBA", "sha256": sha256(combined_path)},
        "preview": {"file": preview_path.name, "size": list(preview.size), "mode": "RGBA", "sha256": sha256(preview_path)},
        "limitations": [
            "These are redrawn concept sprites and do not prove exact saved-person identity continuity across independently generated age sheets.",
            "Every direction has an authored layout; no horizontal mirroring or source-pixel copying is used.",
            "All frames remain concept art pending pixel-artist review, collision/timing authoring, renderer validation, and runtime integration.",
        ],
        "frames": records,
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {len(records)} redrawn linked early-age poses across {len(STAGES)} stages.")


if __name__ == "__main__":
    main()
