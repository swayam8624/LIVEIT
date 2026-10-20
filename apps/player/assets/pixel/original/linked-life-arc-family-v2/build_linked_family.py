"""Build the linked life-arc aggregate from existing transparent source frames.

This package is an index and review atlas. It does not redraw or vendor source
frames; every frame record points at the original pack and records both file
and source-manifest hashes. The generated atlases are deterministic derived
outputs and remain runtime-disabled until a human approves the identity and
pixel cleanup.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


ORIGINAL = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
SIZE = (24, 32)
PIVOT = (12, 31)
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("contact-a", "passing-a", "contact-b", "passing-b")
POSES = ("idle", "interact")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def rel(path: Path) -> str:
    return Path(os.path.relpath(path, OUT)).as_posix()


def source_manifest(package: str) -> tuple[Path, dict[str, Any], str]:
    path = ORIGINAL / package / "manifest.json"
    return path, read_json(path), sha256(path)


PACKAGES: dict[str, tuple[Path, dict[str, Any], str]] = {
    package: source_manifest(package)
    for package in (
        "linked-life-arc-family-v1",
        "linked-early-poses-v1",
        "life-arc-later-poses-v1",
        "linked-elder-poses-v1",
        "linked-male-adult-cycles-v1",
    )
}


STAGE_PLAN = (
    # stage, display label, movement source package, movement stage, pose source package, pose stage
    ("infant-crawl", "Infant crawl", "linked-life-arc-family-v1", "infant-crawl", "linked-early-poses-v1", "infant-crawl"),
    ("toddler-waddle", "Toddler waddle", "linked-life-arc-family-v1", "toddler-waddle", "linked-early-poses-v1", "toddler-waddle"),
    ("child-walk", "Child walk", "linked-life-arc-family-v1", "child-walk", "linked-early-poses-v1", "child-walk"),
    ("teen-walk", "Teen walk", "linked-life-arc-family-v1", "teen-walk", "linked-early-poses-v1", "teen-walk"),
    ("young-adult-woman", "Young adult woman", "linked-life-arc-family-v1", "young-adult-woman", "life-arc-later-poses-v1", "young-adult-woman"),
    ("midlife-woman", "Midlife woman", "linked-life-arc-family-v1", "midlife-woman", "life-arc-later-poses-v1", "midlife-woman"),
    ("elder-woman", "Elder woman", "linked-life-arc-family-v1", "elder-woman", "linked-elder-poses-v1", "elder-woman"),
    ("young-adult-man", "Young adult man", "linked-male-adult-cycles-v1", "young-adult-man", "linked-male-adult-cycles-v1", "young-adult-man"),
    ("midlife-man", "Midlife man", "linked-male-adult-cycles-v1", "midlife-man", "linked-male-adult-cycles-v1", "midlife-man"),
    ("elder-man", "Elder man", "linked-life-arc-family-v1", "elder-man", "linked-elder-poses-v1", "elder-man"),
)


def stage_from(manifest: dict[str, Any], stage_id: str) -> dict[str, Any]:
    for stage in manifest.get("stages", []):
        if isinstance(stage, dict) and stage.get("id") == stage_id:
            return stage
        if isinstance(stage, str) and stage == stage_id:
            # Compact pose packages keep the stage IDs at the top level and
            # store all pose records in one flat ``frames`` list.
            return {
                "id": stage_id,
                "frames": [record for record in manifest.get("frames", []) if record.get("stage") == stage_id],
            }
    raise KeyError(f"missing stage {stage_id}")


def resolved_frame(package: str, record: dict[str, Any]) -> tuple[Path, str, str]:
    manifest_path, _, manifest_hash = PACKAGES[package]
    package_root = manifest_path.parent
    frame_path = package_root / record["file"]
    # Some aggregate source manifests intentionally store paths relative to
    # the original asset root, while package-local manifests use their folder.
    if not frame_path.is_file():
        frame_path = ORIGINAL / record["file"]
    if not frame_path.is_file():
        raise FileNotFoundError(frame_path)
    actual = sha256(frame_path)
    expected = record.get("sha256")
    if expected and actual != expected:
        raise ValueError(f"hash mismatch for {frame_path}: {actual} != {expected}")
    return frame_path, manifest_hash, actual


def movement_record(package: str, stage: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    path, manifest_hash, actual = resolved_frame(package, record)
    if tuple(record.get("size", SIZE)) != SIZE or tuple(record.get("pivot", PIVOT)) != PIVOT:
        raise ValueError(f"incompatible movement frame metadata: {record.get('id')}")
    return {
        "id": record["id"],
        "stage": record["stage"],
        "direction": record["direction"],
        "phase": record["phase"],
        "file": rel(path),
        "sourcePackage": package,
        "sourceManifest": rel(PACKAGES[package][0]),
        "sourceManifestSha256": manifest_hash,
        "sourceFileSha256": actual,
        "size": list(SIZE),
        "pivot": list(PIVOT),
        "mirrored": False,
        "runtimeReady": False,
    }


def pose_record(package: str, stage: dict[str, Any], record: dict[str, Any], aggregate_stage: str) -> dict[str, Any]:
    path, manifest_hash, actual = resolved_frame(package, record)
    state = record.get("state", record.get("pose"))
    if state not in POSES:
        raise ValueError(f"unsupported pose state {state!r} in {record.get('id')}")
    if tuple(record.get("size", SIZE)) != SIZE or tuple(record.get("pivot", PIVOT)) != PIVOT:
        raise ValueError(f"incompatible pose frame metadata: {record.get('id')}")
    return {
        "id": f"{aggregate_stage}/{record['direction']}/{state}",
        "stage": aggregate_stage,
        "direction": record["direction"],
        "state": state,
        "file": rel(path),
        "sourcePackage": package,
        "sourceManifest": rel(PACKAGES[package][0]),
        "sourceManifestSha256": manifest_hash,
        "sourceFileSha256": actual,
        "size": list(SIZE),
        "pivot": list(PIVOT),
        "mirrored": bool(record.get("mirrored", False)),
        "runtimeReady": False,
    }


def atlas(images: list[tuple[str, Path]], columns: int, path: Path) -> tuple[int, int]:
    rows = (len(images) + columns - 1) // columns
    output = Image.new("RGBA", (columns * SIZE[0], rows * SIZE[1]), (0, 0, 0, 0))
    for index, (_, image_path) in enumerate(images):
        with Image.open(image_path) as source:
            frame = source.convert("RGBA")
        if frame.size != SIZE:
            raise ValueError(f"unexpected frame size {frame.size} for {image_path}")
        output.paste(frame, ((index % columns) * SIZE[0], (index // columns) * SIZE[1]))
    output.save(path, format="PNG", optimize=False)
    return output.size


def preview(stages: list[dict[str, Any]], path: Path) -> tuple[int, int]:
    scale = 4
    label_w = 112
    cell_w = SIZE[0]
    cols = 6
    row_h = SIZE[1] + 14
    header_h = 26
    output = Image.new("RGBA", ((label_w + cols * cell_w) * scale, (header_h + len(stages) * row_h) * scale), (24, 29, 42, 255))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    def text(x: int, y: int, value: str, fill: tuple[int, int, int, int] = (235, 240, 249, 255)) -> None:
        draw.text((x * scale, y * scale), value, fill=fill, font=font)
    text(4, 5, "movement: south west east north | poses: idle interact")
    for row, stage in enumerate(stages):
        y = header_h + row * row_h
        draw.rectangle((0, y * scale, output.width, (y + row_h - 1) * scale), fill=(29, 36, 54, 255))
        text(4, y + 4, stage["label"][:16], (255, 218, 137, 255))
        movement_by = {(r["direction"], r["phase"]): r for r in stage["movementFrames"]}
        pose_by = {(r["direction"], r["state"]): r for r in stage["poseFrames"]}
        samples = [(d, "contact-a") for d in DIRECTIONS] + [("south", p) for p in POSES]
        for col, (direction, state) in enumerate(samples):
            record = movement_by.get((direction, state)) or pose_by[(direction, state)]
            with Image.open(OUT / record["file"]) as source:
                frame = source.convert("RGBA").resize((cell_w * scale, SIZE[1] * scale), Image.Resampling.NEAREST)
            x = label_w + col * cell_w
            output.alpha_composite(frame, (x * scale, (y + 1) * scale))
    output.save(path, format="PNG", optimize=False)
    return output.size


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    stages: list[dict[str, Any]] = []
    movement_images: list[tuple[str, Path]] = []
    pose_images: list[tuple[str, Path]] = []
    for aggregate_id, label, movement_package, movement_id, pose_package, pose_id in STAGE_PLAN:
        movement_stage = stage_from(PACKAGES[movement_package][1], movement_id)
        pose_stage = stage_from(PACKAGES[pose_package][1], pose_id)
        moves = [movement_record(movement_package, movement_stage, record) for record in movement_stage["frames"]]
        moves.sort(key=lambda r: (DIRECTIONS.index(r["direction"]), PHASES.index(r["phase"])))
        # The compact pose packages use ``frames``; the male cycle package
        # stores movement in ``frames`` and its idle/interact records in
        # ``poseFrames``.
        pose_records = pose_stage.get("poseFrames") or pose_stage.get("frames", [])
        poses = [pose_record(pose_package, pose_stage, record, aggregate_id) for record in pose_records]
        poses.sort(key=lambda r: (DIRECTIONS.index(r["direction"]), POSES.index(r["state"])))
        if len(moves) != 16 or len(poses) != 8:
            raise ValueError(f"coverage failed for {aggregate_id}: {len(moves)} movement / {len(poses)} poses")
        for direction in DIRECTIONS:
            if [r["direction"] for r in moves].count(direction) != 4 or [r["direction"] for r in poses].count(direction) != 2:
                raise ValueError(f"direction coverage failed for {aggregate_id}")
        if any(r["mirrored"] for r in moves + poses):
            raise ValueError(f"mirrored source record found for {aggregate_id}")
        stage = {
            "id": aggregate_id,
            "label": label,
            "movementFrames": moves,
            "poseFrames": poses,
            "movementFrameCount": len(moves),
            "poseFrameCount": len(poses),
            "runtimeReady": False,
        }
        stages.append(stage)
        movement_images.extend((r["id"], OUT / r["file"]) for r in moves)
        pose_images.extend((r["id"], OUT / r["file"]) for r in poses)

    movement_path = OUT / "linked-life-arc-family-v2-movement-atlas-24x32.png"
    pose_path = OUT / "linked-life-arc-family-v2-pose-atlas-24x32.png"
    preview_path = OUT / "linked-life-arc-family-v2-preview-4x.png"
    movement_size = atlas(movement_images, 16, movement_path)
    pose_size = atlas(pose_images, 8, pose_path)
    preview_size = preview(stages, preview_path)
    output_hashes = {
        "movementAtlas": {"file": movement_path.name, "size": list(movement_size), "sha256": sha256(movement_path)},
        "poseAtlas": {"file": pose_path.name, "size": list(pose_size), "sha256": sha256(pose_path)},
        "preview": {"file": preview_path.name, "size": list(preview_size), "sha256": sha256(preview_path)},
    }
    for stage in stages:
        for record in stage["movementFrames"]:
            record["derivedOutput"] = movement_path.name
            record["derivedOutputSha256"] = output_hashes["movementAtlas"]["sha256"]
        for record in stage["poseFrames"]:
            record["derivedOutput"] = pose_path.name
            record["derivedOutputSha256"] = output_hashes["poseAtlas"]["sha256"]

    manifest = {
        "schemaVersion": 1,
        "id": "linked-life-arc-family-v2",
        "status": "original-rights-safe-derived-aggregate",
        "runtimeReady": False,
        "description": "Aggregate review package for one shared early-age arc with woman and man adult/elder branches.",
        "identityContinuity": "separately generated source branches; human identity reconciliation is still required before runtime integration",
        "ageBranches": {
            "sharedEarly": ["infant-crawl", "toddler-waddle", "child-walk", "teen-walk"],
            "woman": ["young-adult-woman", "midlife-woman", "elder-woman"],
            "man": ["young-adult-man", "midlife-man", "elder-man"],
        },
        "directions": list(DIRECTIONS),
        "phases": list(PHASES),
        "poses": list(POSES),
        "frameSize": list(SIZE),
        "pivot": list(PIVOT),
        "nonMirroringAssumption": {
            "value": True,
            "evidence": "Every source record used here declares mirrored=false or omits mirroring; directions are sourced as authored south/west/east/north frames. Pixel-level artist review is still required.",
        },
        "sourceManifests": [
            {"package": package, "file": rel(path), "sha256": manifest_hash}
            for package, (path, _, manifest_hash) in PACKAGES.items()
        ],
        "outputs": output_hashes,
        "stages": stages,
        "movementFrameCount": sum(s["movementFrameCount"] for s in stages),
        "poseFrameCount": sum(s["poseFrameCount"] for s in stages),
        "limitations": [
            "This aggregate references existing transparent concept frames and does not claim a final artist-redrawn sheet.",
            "The woman and man branches were generated separately; exact facial, hair and outfit continuity needs human reconciliation.",
            "Atlases are derived review outputs and are not admitted to runtime asset intake.",
        ],
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"built {manifest['movementFrameCount']} movement + {manifest['poseFrameCount']} pose frames")
    print(f"movement atlas {movement_size} sha256={output_hashes['movementAtlas']['sha256']}")
    print(f"pose atlas {pose_size} sha256={output_hashes['poseAtlas']['sha256']}")
    print(f"preview {preview_size} sha256={output_hashes['preview']['sha256']}")


if __name__ == "__main__":
    main()
