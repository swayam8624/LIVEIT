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
    ("child-walk", "child", "small-toy-hold", "show-toy"),
    ("teen-walk", "teen", "casual-stand", "check-keepsake"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_frame(stage: str, direction: str, phase: str) -> Path:
    return SOURCE_ROOT / stage / f"{stage}-{direction}-{phase}.png"


def idle_frame(source: Image.Image) -> Image.Image:
    # A one-pixel breathing lift keeps the source silhouette intact while
    # making the pose distinct from the walking contact frame.
    out = Image.new("RGBA", source.size, (0, 0, 0, 0))
    out.alpha_composite(source, (0, -1))
    return out


def interact_frame(source: Image.Image, direction: str, stage: str) -> Image.Image:
    out = source.copy()
    draw = ImageDraw.Draw(out)
    # Small, direction-specific pixel clusters communicate a reachable,
    # care-safe interaction. They are deliberately independent of mirroring.
    anchors = {
        "south": (12, 21),
        "west": (7, 21),
        "east": (16, 21),
        "north": (12, 19),
    }
    x, y = anchors[direction]
    if stage == "infant-crawl":
        # Soft toy: pale yellow center with a sky-blue edge.
        draw.point((x, y), fill=(246, 211, 112, 255))
        draw.point((x + 1, y), fill=(246, 211, 112, 255))
        draw.point((x, y + 1), fill=(112, 190, 226, 255))
    elif stage == "toddler-waddle":
        # Gentle wave/comfort cue: a warm mitten-sized pixel cluster.
        draw.point((x, y), fill=(231, 160, 95, 255))
        draw.point((x, y - 1), fill=(246, 194, 114, 255))
    elif stage == "child-walk":
        # Small keepsake/book held toward the viewer.
        draw.point((x, y), fill=(246, 211, 112, 255))
        draw.point((x + 1, y), fill=(246, 211, 112, 255))
        draw.point((x, y + 1), fill=(63, 156, 190, 255))
    else:
        # A tiny blue keepsake/phone glint, kept close to the body.
        draw.point((x, y), fill=(112, 190, 226, 255))
        draw.point((x + 1, y), fill=(63, 156, 190, 255))
    return out


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    records = []
    stage_records = []
    combined = Image.new("RGBA", (48, 128 * len(STAGES)), (0, 0, 0, 0))

    for stage_index, (stage, label, idle_cue, interact_cue) in enumerate(STAGES):
        stage_dir = ROOT / "frames" / stage
        stage_dir.mkdir(parents=True, exist_ok=True)
        atlas = Image.new("RGBA", (48, 128), (0, 0, 0, 0))
        stage_frames = []
        for direction_index, direction in enumerate(DIRECTIONS):
            idle_source = source_frame(stage, direction, "contact-a")
            interact_source = source_frame(stage, direction, "passing-b")
            for pose in POSES:
                source_path = idle_source if pose == "idle" else interact_source
                with Image.open(source_path).convert("RGBA") as source:
                    if source.size != (24, 32):
                        raise ValueError(f"Unexpected source size {source.size}: {source_path}")
                    image = idle_frame(source) if pose == "idle" else interact_frame(source, direction, stage)
                output = stage_dir / f"{stage}-{direction}-{pose}.png"
                image.save(output)
                x = POSES.index(pose) * 24
                y = direction_index * 32
                atlas.alpha_composite(image, (x, y))
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
                    "size": [24, 32],
                    "pivot": [12, 31],
                    "sha256": sha256(output),
                    "runtimeReady": False,
                }
                records.append(record)
                stage_frames.append(record)

        atlas_path = ROOT / f"{stage}-idle-interact-atlas.png"
        atlas.save(atlas_path)
        combined.alpha_composite(atlas, (0, stage_index * 128))
        stage_records.append(
            {
                "id": stage,
                "label": label,
                "atlas": atlas_path.name,
                "frameCount": len(stage_frames),
                "frames": stage_frames,
                "runtimeReady": False,
            }
        )

    combined_path = ROOT / "linked-early-poses-atlas-24x32.png"
    combined.save(combined_path)
    preview_path = ROOT / "linked-early-poses-preview-4x.png"
    combined.resize((combined.width * 4, combined.height * 4), Image.Resampling.NEAREST).save(preview_path)

    manifest = {
        "schemaVersion": 1,
        "id": "linked-early-poses-v1",
        "status": "original-rights-safe-concept-study",
        "runtimeReady": False,
        "sourceTool": "Pillow deterministic pose derivation from linked-life-arc-family-v1 early directional frames",
        "sourceBatch": "life-arc-early-cycles-v1",
        "identityCues": [
            "deep-brown skin",
            "coiled dark hair and recurring facial mark",
            "sky-blue clothing accents",
        ],
        "frameSize": [24, 32],
        "pivot": [12, 31],
        "directions": DIRECTIONS,
        "poses": POSES,
        "stageCount": len(STAGES),
        "frameCount": len(records),
        "stages": stage_records,
        "combinedAtlas": {
            "file": combined_path.name,
            "size": list(combined.size),
            "mode": "RGBA",
            "sha256": sha256(combined_path),
        },
        "preview": {
            "file": preview_path.name,
            "size": list(combined.resize((combined.width * 4, combined.height * 4), Image.Resampling.NEAREST).size),
            "mode": "RGBA",
            "sha256": sha256(preview_path),
        },
        "limitations": [
            "These poses extend the linked movement studies and do not prove frame-perfect identity continuity across independently generated age sheets.",
            "Directions are authored from their corresponding source frame; no horizontal mirroring is used.",
            "All frames remain concept art pending pixel-artist review, collision/timing authoring, renderer validation, and runtime integration.",
        ],
        "frames": records,
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {len(records)} linked early-age idle/interact frames across {len(STAGES)} stages.")


if __name__ == "__main__":
    main()
