#!/usr/bin/env python3
"""Build the linked male young-adult and midlife movement concept batch."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "source"
FRAME_SIZE = (24, 32)
PIVOT = (12, 31)
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("contact-a", "passing-a", "contact-b", "passing-b")
POSE_STATES = ("idle", "interact")
STAGES = (
    ("young-adult-man", "young adult man", "young-adult-man-source.png"),
    ("midlife-man", "midlife man", "midlife-man-source.png"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def frame_from_source(source: Image.Image, col: int, row: int) -> Image.Image:
    """Extract one generated grid cell and normalize it to a 24x32 sprite."""
    left = source.width * col // 4
    right = source.width * (col + 1) // 4
    top = source.height * row // 4
    bottom = source.height * (row + 1) // 4
    cell = source.crop((left, top, right, bottom)).convert("RGBA")
    alpha = cell.getchannel("A")
    bbox = alpha.getbbox()
    out = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
    if bbox is None:
        return out
    subject = cell.crop(bbox)
    # Leave a one-pixel safety margin for the 24x32 runtime cell.
    scale = min(22 / subject.width, 30 / subject.height)
    size = (max(1, round(subject.width * scale)), max(1, round(subject.height * scale)))
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    # Reduce the generated sheet to a compact game palette and hard alpha edges.
    rgb = subject.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT).convert("RGBA")
    a = subject.getchannel("A").resize(size, Image.Resampling.LANCZOS).point(lambda p: 255 if p >= 128 else 0)
    rgb.putalpha(a)
    x = (FRAME_SIZE[0] - size[0]) // 2
    y = FRAME_SIZE[1] - size[1] - 1
    out.alpha_composite(rgb, (x, y))
    return out


def frame_from_pose_source(source: Image.Image, col: int, row: int) -> Image.Image:
    """Extract one 4x2 idle/interact source cell and normalize it to a 24x32 sprite."""
    left = source.width * col // 4
    right = source.width * (col + 1) // 4
    top = source.height * row // 2
    bottom = source.height * (row + 1) // 2
    cell = source.crop((left, top, right, bottom)).convert("RGBA")
    alpha = cell.getchannel("A")
    bbox = alpha.getbbox()
    out = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
    if bbox is None:
        return out
    subject = cell.crop(bbox)
    scale = min(22 / subject.width, 30 / subject.height)
    size = (max(1, round(subject.width * scale)), max(1, round(subject.height * scale)))
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    rgb = subject.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT).convert("RGBA")
    a = subject.getchannel("A").resize(size, Image.Resampling.LANCZOS).point(lambda p: 255 if p >= 128 else 0)
    rgb.putalpha(a)
    x = (FRAME_SIZE[0] - size[0]) // 2
    y = FRAME_SIZE[1] - size[1] - 1
    out.alpha_composite(rgb, (x, y))
    return out


def write_stage(stage_id: str, label: str, source_name: str) -> list[dict]:
    source_path = SOURCE_DIR / source_name
    source = Image.open(source_path).convert("RGBA")
    stage_dir = ROOT / "frames" / stage_id
    stage_dir.mkdir(parents=True, exist_ok=True)
    frames: list[dict] = []
    atlas = Image.new("RGBA", (FRAME_SIZE[0] * 4, FRAME_SIZE[1] * 4), (0, 0, 0, 0))
    for row, direction in enumerate(DIRECTIONS):
        for col, phase in enumerate(PHASES):
            frame = frame_from_source(source, col, row)
            filename = f"{stage_id}-{direction}-{phase}.png"
            path = stage_dir / filename
            frame.save(path, "PNG", optimize=False)
            atlas.alpha_composite(frame, (col * FRAME_SIZE[0], row * FRAME_SIZE[1]))
            frames.append(
                {
                    "id": f"{stage_id}/{direction}/{phase}",
                    "stage": stage_id,
                    "stageLabel": label,
                    "direction": direction,
                    "phase": phase,
                    "file": f"frames/{stage_id}/{filename}",
                    "size": list(FRAME_SIZE),
                    "pivot": list(PIVOT),
                    "sha256": sha256(path),
                    "sourceSheet": f"source/{source_name}",
                    "sourceSheetSha256": sha256(source_path),
                    "runtimeReady": False,
                }
            )
    atlas.save(ROOT / f"{stage_id}-atlas-4x4.png", "PNG", optimize=False)
    return frames


def write_pose_stage(stage_id: str, label: str, source_name: str) -> list[dict]:
    source_path = SOURCE_DIR / source_name
    source = Image.open(source_path).convert("RGBA")
    stage_dir = ROOT / "frames" / stage_id
    stage_dir.mkdir(parents=True, exist_ok=True)
    frames: list[dict] = []
    atlas = Image.new("RGBA", (FRAME_SIZE[0] * 4, FRAME_SIZE[1] * 2), (0, 0, 0, 0))
    for row, state in enumerate(POSE_STATES):
        for col, direction in enumerate(DIRECTIONS):
            frame = frame_from_pose_source(source, col, row)
            filename = f"{stage_id}-{direction}-{state}.png"
            path = stage_dir / filename
            frame.save(path, "PNG", optimize=False)
            atlas.alpha_composite(frame, (col * FRAME_SIZE[0], row * FRAME_SIZE[1]))
            frames.append(
                {
                    "id": f"{stage_id}/{direction}/{state}",
                    "stage": stage_id,
                    "stageLabel": label,
                    "direction": direction,
                    "state": state,
                    "file": f"frames/{stage_id}/{filename}",
                    "size": list(FRAME_SIZE),
                    "pivot": list(PIVOT),
                    "sha256": sha256(path),
                    "sourceSheet": f"source/{source_name}",
                    "sourceSheetSha256": sha256(source_path),
                    "runtimeReady": False,
                }
            )
    atlas.save(ROOT / f"{stage_id}-idle-interact-atlas-4x2.png", "PNG", optimize=False)
    return frames


def main() -> None:
    all_frames: list[dict] = []
    all_pose_frames: list[dict] = []
    stage_entries: list[dict] = []
    stage_blocks: list[Image.Image] = []
    for stage_id, label, source_name in STAGES:
        frames = write_stage(stage_id, label, source_name)
        pose_source_name = f"{stage_id}-idle-interact-source.png"
        pose_frames = write_pose_stage(stage_id, label, pose_source_name)
        all_frames.extend(frames)
        all_pose_frames.extend(pose_frames)
        movement_atlas = Image.open(ROOT / f"{stage_id}-atlas-4x4.png").convert("RGBA")
        pose_atlas = Image.open(ROOT / f"{stage_id}-idle-interact-atlas-4x2.png").convert("RGBA")
        block = Image.new("RGBA", (FRAME_SIZE[0] * 4, FRAME_SIZE[1] * 6), (0, 0, 0, 0))
        block.alpha_composite(movement_atlas, (0, 0))
        block.alpha_composite(pose_atlas, (0, FRAME_SIZE[1] * 4))
        block.save(ROOT / f"{stage_id}-atlas-4x6.png", "PNG", optimize=False)
        stage_entries.append(
            {
                "id": stage_id,
                "label": label,
                "continuityRole": "linked-player-adult-branch",
                "sourceSheet": f"source/{source_name}",
                "sourceSheetSha256": sha256(SOURCE_DIR / source_name),
                "atlas": f"{stage_id}-atlas-4x4.png",
                "frameCount": len(frames),
                "frames": frames,
                "poseStates": list(POSE_STATES),
                "poseSourceSheet": f"source/{pose_source_name}",
                "poseSourceSheetSha256": sha256(SOURCE_DIR / pose_source_name),
                "poseFrameCount": len(pose_frames),
                "poseFrames": pose_frames,
                "poseAtlas": f"{stage_id}-idle-interact-atlas-4x2.png",
                "combinedAtlas": f"{stage_id}-atlas-4x6.png",
                "runtimeReady": False,
            }
        )
        stage_blocks.append(Image.open(ROOT / f"{stage_id}-atlas-4x6.png").convert("RGBA"))

    combined = Image.new("RGBA", (FRAME_SIZE[0] * 8, FRAME_SIZE[1] * 6), (0, 0, 0, 0))
    combined.alpha_composite(stage_blocks[0], (0, 0))
    combined.alpha_composite(stage_blocks[1], (FRAME_SIZE[0] * 4, 0))
    combined.save(ROOT / "linked-male-adult-cycles-atlas-24x32.png", "PNG", optimize=False)
    preview = combined.resize((combined.width * 4, combined.height * 4), Image.Resampling.NEAREST)
    preview.save(ROOT / "linked-male-adult-cycles-preview-4x.png", "PNG", optimize=False)

    manifest = {
        "schemaVersion": 1,
        "id": "linked-male-adult-cycles-v1",
        "runtimeReady": False,
        "identityCues": [
            "deep-brown skin",
            "short coiled dark hair, with silver strands beginning at midlife",
            "recurring sky-blue clothing accent and teal wrist band",
            "small crescent facial mark retained from young adult through elder-man guidance",
        ],
        "directions": list(DIRECTIONS),
        "phases": list(PHASES),
        "frameSize": list(FRAME_SIZE),
        "pivot": list(PIVOT),
        "stages": stage_entries,
        "elderManContinuityGuidance": {
            "referenceBatch": "linked-life-arc-family-v1",
            "referenceAtlas": "../linked-life-arc-family-v1/elder-man-atlas-4x4.png",
            "poseBatch": "../linked-elder-poses-v1",
            "notes": [
                "Keep the same deep-brown skin, crescent facial mark, and blue/teal accents.",
                "Transition the short coils to visibly silver-white coils while keeping the silhouette recognizable.",
                "Use a relaxed, slightly stooped posture and slower stride for the elder presentation.",
            ],
        },
        "sourceSheets": [
            {"file": f"source/{name}", "sha256": sha256(SOURCE_DIR / name)}
            for _, _, name in STAGES
        ]
        + [
            {
                "file": f"source/{stage_id}-idle-interact-source.png",
                "sha256": sha256(SOURCE_DIR / f"{stage_id}-idle-interact-source.png"),
            }
            for stage_id, _, _ in STAGES
        ],
        "promptFiles": [
            f"source/{stage_id}-idle-interact-prompt.txt" for stage_id, _, _ in STAGES
        ],
        "derivedOutputs": [
            {"file": f"{stage_id}-atlas-4x4.png", "sha256": sha256(ROOT / f"{stage_id}-atlas-4x4.png")} for stage_id, _, _ in STAGES
        ]
        + [
            {"file": f"{stage_id}-idle-interact-atlas-4x2.png", "sha256": sha256(ROOT / f"{stage_id}-idle-interact-atlas-4x2.png")} for stage_id, _, _ in STAGES
        ]
        + [
            {"file": f"{stage_id}-atlas-4x6.png", "sha256": sha256(ROOT / f"{stage_id}-atlas-4x6.png")} for stage_id, _, _ in STAGES
        ]
        + [
            {"file": "linked-male-adult-cycles-atlas-24x32.png", "sha256": sha256(ROOT / "linked-male-adult-cycles-atlas-24x32.png")},
            {"file": "linked-male-adult-cycles-preview-4x.png", "sha256": sha256(ROOT / "linked-male-adult-cycles-preview-4x.png")},
        ],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
