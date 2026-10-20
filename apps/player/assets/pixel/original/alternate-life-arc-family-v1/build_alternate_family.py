"""Build a distinct, rights-safe secondary life-arc family.

The drawings are deliberately small and procedural: a warm olive complexion,
auburn hair, a mustard scarf, a teal satchel, and a star hair clip persist
through the life arc. Direction views have separate authored geometry rather
than mirroring. This package is a visual concept family and remains runtime
disabled until a human art pass and renderer integration approve it.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parent
SIZE = (24, 32)
PIVOT = (12, 31)
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("contact-a", "passing-a", "contact-b", "passing-b")
POSES = ("idle", "interact")

PALETTE = {
    "skin": (184, 142, 112, 255),
    "skin_hi": (221, 177, 139, 255),
    "skin_shadow": (132, 92, 82, 255),
    "hair": (112, 54, 45, 255),
    "hair_hi": (166, 79, 55, 255),
    "hair_silver": (191, 153, 137, 255),
    "scarf": (222, 163, 52, 255),
    "scarf_shadow": (154, 94, 35, 255),
    "top": (42, 67, 104, 255),
    "top_hi": (61, 104, 138, 255),
    "trouser": (73, 55, 83, 255),
    "shoe": (54, 40, 50, 255),
    "satchel": (38, 133, 128, 255),
    "satchel_hi": (75, 181, 154, 255),
    "clip": (238, 205, 88, 255),
    "outline": (31, 30, 46, 255),
}

STAGES = (
    ("infant-crawl", "Infant crawl", "shared", 0),
    ("toddler-waddle", "Toddler waddle", "shared", 1),
    ("child-walk", "Child walk", "shared", 2),
    ("teen-walk", "Teen walk", "shared", 3),
    ("young-adult-woman", "Young adult woman", "woman", 4),
    ("midlife-woman", "Midlife woman", "woman", 5),
    ("elder-woman", "Elder woman", "woman", 6),
    ("young-adult-man", "Young adult man", "man", 7),
    ("midlife-man", "Midlife man", "man", 8),
    ("elder-man", "Elder man", "man", 9),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clear_generated() -> None:
    for path in OUT.glob("**/*.png"):
        path.unlink()


def stage_profile(index: int, branch: str) -> dict[str, int | bool]:
    # Height and proportions grow gradually. The distinct branch silhouettes
    # are intentionally encoded in the profile rather than copied frames.
    if index == 0:
        return {"head": 6, "body": 5, "leg": 0, "crawl": True, "hair": 2}
    if index == 1:
        return {"head": 6, "body": 7, "leg": 5, "crawl": False, "hair": 3}
    if index == 2:
        return {"head": 6, "body": 9, "leg": 8, "crawl": False, "hair": 4}
    if index == 3:
        return {"head": 6, "body": 10, "leg": 10, "crawl": False, "hair": 5}
    if branch == "woman":
        return {"head": 6, "body": 11, "leg": 12, "crawl": False, "hair": 6 if index == 4 else 5 if index == 5 else 4}
    return {"head": 6, "body": 12, "leg": 12, "crawl": False, "hair": 5 if index == 7 else 4}


def rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: tuple[int, int, int, int]) -> None:
    draw.rectangle(box, fill=fill)


def person(stage: str, branch: str, index: int, direction: str, action: str, phase: int = 0) -> Image.Image:
    profile = stage_profile(index, branch)
    image = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    center = 12
    # Meaningful frame changes: bob, step and hand reach are different for
    # each state; no frame is a byte-identical duplicate of another phase.
    bob = (0, -1, 0, 1)[phase % 4] if action.startswith("move") else (0, 0)
    if isinstance(bob, tuple):
        bob = bob[0]
    step = (-2, 1, 2, -1)[phase % 4]
    if action == "interact":
        bob = -1
    if action == "idle":
        bob = 0
    base = 30 + bob
    head = int(profile["head"])
    body = int(profile["body"])
    leg = int(profile["leg"])
    hair = int(profile["hair"])
    crawl = bool(profile["crawl"])
    elder = index in (6, 9)

    # Independently-authored directional head silhouettes.
    if direction == "south":
        hx0, hx1, hy0 = center - head // 2, center + head // 2 - 1, 8 + bob
        rect(draw, (hx0 - 1, hy0 + 1, hx1 + 1, hy0 + head), PALETTE["outline"])
        rect(draw, (hx0, hy0, hx1, hy0 + head - 1), PALETTE["skin"])
        rect(draw, (hx0 + 1, hy0 + 1, hx1 - 1, hy0 + 2), PALETTE["skin_hi"])
        rect(draw, (hx0, hy0, hx0 + 1, hy0 + hair - 1), PALETTE["hair"])
        rect(draw, (hx1 - 1, hy0, hx1, hy0 + hair - 1), PALETTE["hair_hi"])
        rect(draw, (hx0 + 1, hy0, hx1 - 1, hy0 + 1), PALETTE["hair"])
        if elder:
            rect(draw, (hx0 + 2, hy0, hx0 + 2, hy0 + 2), PALETTE["hair_silver"])
        rect(draw, (hx0 + 1, hy0 + 3, hx0 + 1, hy0 + 3), PALETTE["outline"])
        rect(draw, (hx1 - 1, hy0 + 3, hx1 - 1, hy0 + 3), PALETTE["outline"])
        rect(draw, (hx1 - 2, hy0 - 1, hx1 - 1, hy0), PALETTE["clip"])
    elif direction == "west":
        hx0, hy0 = 8, 8 + bob
        rect(draw, (hx0 - 1, hy0 + 1, hx0 + head, hy0 + head), PALETTE["outline"])
        rect(draw, (hx0, hy0, hx0 + head - 1, hy0 + head - 1), PALETTE["skin"])
        rect(draw, (hx0, hy0, hx0 + 2, hy0 + hair - 1), PALETTE["hair"])
        rect(draw, (hx0 + 1, hy0, hx0 + head - 2, hy0 + 1), PALETTE["hair_hi"])
        rect(draw, (hx0 - 2, hy0 + 3, hx0, hy0 + 4), PALETTE["skin_hi"])
        rect(draw, (hx0 + 1, hy0 + 3, hx0 + 1, hy0 + 3), PALETTE["outline"])
        rect(draw, (hx0 + 1, hy0 - 1, hx0 + 2, hy0), PALETTE["clip"])
    elif direction == "east":
        hx0, hy0 = 10, 8 + bob
        rect(draw, (hx0 - 1, hy0 + 1, hx0 + head, hy0 + head), PALETTE["outline"])
        rect(draw, (hx0, hy0, hx0 + head - 1, hy0 + head - 1), PALETTE["skin"])
        rect(draw, (hx0 + head - 3, hy0, hx0 + head - 1, hy0 + hair - 1), PALETTE["hair_hi"])
        rect(draw, (hx0 + 1, hy0, hx0 + head - 2, hy0 + 1), PALETTE["hair"])
        rect(draw, (hx0 + head - 1, hy0 + 3, hx0 + head + 1, hy0 + 4), PALETTE["skin_hi"])
        rect(draw, (hx0 + head - 2, hy0 + 3, hx0 + head - 2, hy0 + 3), PALETTE["outline"])
        rect(draw, (hx0 + 3, hy0 - 1, hx0 + 4, hy0), PALETTE["clip"])
    else:  # north/back silhouette has a different hair and scarf arrangement.
        hx0, hx1, hy0 = center - head // 2, center + head // 2 - 1, 8 + bob
        rect(draw, (hx0 - 1, hy0 + 1, hx1 + 1, hy0 + head), PALETTE["outline"])
        rect(draw, (hx0, hy0, hx1, hy0 + head - 1), PALETTE["hair"])
        rect(draw, (hx0 + 1, hy0 + 1, hx1 - 1, hy0 + 3), PALETTE["hair_hi"])
        rect(draw, (hx0 + 1, hy0 + 4, hx1 - 1, hy0 + head - 1), PALETTE["hair"])
        if elder:
            rect(draw, (hx1 - 2, hy0 + 1, hx1 - 1, hy0 + 3), PALETTE["hair_silver"])
        rect(draw, (hx0 - 1, hy0 + 1, hx0, hy0 + 2), PALETTE["clip"])

    if crawl:
        y = 20 + bob
        rect(draw, (7, y, 16, y + body - 1), PALETTE["outline"])
        rect(draw, (8, y + 1, 15, y + body - 1), PALETTE["top"])
        rect(draw, (9, y + 1, 14, y + 2), PALETTE["top_hi"])
        arm = 6 + (phase % 3)
        rect(draw, (5, y + 2, 8, y + 3), PALETTE["skin"])
        rect(draw, (15, y + 3, arm + 12, y + 4), PALETTE["skin_shadow"])
        rect(draw, (6, y + 5, 9, y + 6), PALETTE["skin_hi"])
    else:
        torso_y = 14 + bob
        torso_w = 7 if index < 4 else 8 if branch == "woman" else 9
        left, right = center - torso_w // 2, center + torso_w // 2
        rect(draw, (left - 1, torso_y, right + 1, torso_y + body), PALETTE["outline"])
        rect(draw, (left, torso_y + 1, right, torso_y + body - 1), PALETTE["top"])
        rect(draw, (left + 1, torso_y + 1, right - 1, torso_y + 3), PALETTE["top_hi"])
        # Persistent mustard scarf and teal satchel, authored per direction.
        if direction == "south":
            rect(draw, (left, torso_y + 1, right, torso_y + 2), PALETTE["scarf"])
            rect(draw, (right - 1, torso_y + 4, right + 2, torso_y + 7), PALETTE["satchel"])
            rect(draw, (right, torso_y + 4, right + 1, torso_y + 4), PALETTE["satchel_hi"])
        elif direction == "west":
            rect(draw, (left - 1, torso_y + 2, left + 1, torso_y + 5), PALETTE["scarf"])
            rect(draw, (left - 2, torso_y + 5, left, torso_y + 9), PALETTE["satchel"])
        elif direction == "east":
            rect(draw, (right - 1, torso_y + 2, right + 1, torso_y + 5), PALETTE["scarf_shadow"])
            rect(draw, (right, torso_y + 5, right + 2, torso_y + 9), PALETTE["satchel_hi"])
        else:
            rect(draw, (left, torso_y + 1, right, torso_y + 2), PALETTE["scarf_shadow"])
            rect(draw, (left - 1, torso_y + 4, left + 2, torso_y + 8), PALETTE["satchel"])
        # Arms change for movement and reaching states.
        reach = action == "interact"
        if direction in ("south", "north"):
            left_hand = left - (3 if reach else 2) + (step if phase % 2 else 0)
            right_hand = right + (3 if reach else 2) - (step if phase % 2 else 0)
            rect(draw, (left_hand, torso_y + 4, left_hand + 1, torso_y + 8), PALETTE["skin"])
            rect(draw, (right_hand, torso_y + 4, right_hand + 1, torso_y + 8), PALETTE["skin_hi"])
        elif direction == "west":
            rect(draw, (left - (4 if reach else 2), torso_y + 4 + (phase % 2), left, torso_y + 5 + (phase % 2)), PALETTE["skin_hi"])
            rect(draw, (right - 1, torso_y + 5, right + 1, torso_y + 8), PALETTE["skin_shadow"])
        else:
            rect(draw, (right, torso_y + 4 + (phase % 2), right + (4 if reach else 2), torso_y + 5 + (phase % 2)), PALETTE["skin_hi"])
            rect(draw, (left - 1, torso_y + 5, left + 1, torso_y + 8), PALETTE["skin_shadow"])
        leg_y = torso_y + body
        if branch == "woman" and index >= 4:
            rect(draw, (left, leg_y, right, leg_y + leg - 2), PALETTE["trouser"])
        else:
            rect(draw, (left, leg_y, left + 2, leg_y + leg - 2), PALETTE["trouser"])
            rect(draw, (right - 2, leg_y, right, leg_y + leg - 2), PALETTE["trouser"])
        if action.startswith("move"):
            rect(draw, (left - 1 + max(0, step), base - 1, left + 1 + max(0, step), base), PALETTE["shoe"])
            rect(draw, (right - 1 - max(0, -step), base - 1, right + 1 - max(0, -step), base), PALETTE["shoe"])
        else:
            rect(draw, (left - 1, base - 1, left + 2, base), PALETTE["shoe"])
            rect(draw, (right - 1, base - 1, right + 2, base), PALETTE["shoe"])

    # A stable star cue moves from hair to scarf as proportions grow, but
    # remains visible in every branch and never depends on mirroring.
    if index < 4:
        rect(draw, (16, 18 + bob, 17, 19 + bob), PALETTE["clip"])
    else:
        rect(draw, (center - 1, 16 + bob, center, 17 + bob), PALETTE["clip"])
    return image


def save_frame(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=False)


def atlas(images: list[Path], columns: int, path: Path, cell: tuple[int, int] = SIZE) -> tuple[int, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = math.ceil(len(images) / columns)
    output = Image.new("RGBA", (columns * cell[0], rows * cell[1]), (0, 0, 0, 0))
    for i, source_path in enumerate(images):
        with Image.open(source_path) as source:
            output.paste(source.convert("RGBA"), ((i % columns) * cell[0], (i // columns) * cell[1]))
    output.save(path, format="PNG", optimize=False)
    return output.size


def build_preview(records: list[dict[str, Any]], path: Path) -> tuple[int, int]:
    scale, label_w, row_h = 4, 128, 52
    rows = len(STAGES)
    output = Image.new("RGBA", ((label_w + 6 * SIZE[0]) * scale, (30 + rows * row_h) * scale), (24, 29, 42, 255))
    draw = ImageDraw.Draw(output)
    font = ImageFont.load_default()
    draw.text((4 * scale, 6 * scale), "alternate identity | south west east north | 4 move + idle + interact", fill=(235, 240, 249, 255), font=font)
    by_id = {r["id"]: r for r in records}
    for row, (stage_id, label, _, _) in enumerate(STAGES):
        y = 30 + row * row_h
        draw.rectangle((0, y * scale, output.width, (y + row_h - 1) * scale), fill=(29, 36, 54, 255))
        draw.text((4 * scale, (y + 8) * scale), label[:17], fill=(255, 218, 137, 255), font=font)
        samples = [(d, "contact-a") for d in DIRECTIONS] + [("south", p) for p in POSES]
        for col, (direction, state) in enumerate(samples):
            key = f"{stage_id}/{direction}/{state}"
            with Image.open(OUT / by_id[key]["file"]) as source:
                frame = source.convert("RGBA").resize((SIZE[0] * scale, SIZE[1] * scale), Image.Resampling.NEAREST)
            output.alpha_composite(frame, ((label_w + col * SIZE[0]) * scale, (y + 1) * scale))
    output.save(path, format="PNG", optimize=False)
    return output.size


def main() -> None:
    clear_generated()
    records: list[dict[str, Any]] = []
    masters = Image.new("RGBA", (48 * 10, 64), (24, 29, 42, 255))
    for stage_id, label, branch, index in STAGES:
        master = person(stage_id, branch, index, "south", "idle", 0).resize((48, 64), Image.Resampling.NEAREST)
        masters.alpha_composite(master, (index * 48, 0))
        stage_dir = OUT / "frames" / stage_id
        for direction in DIRECTIONS:
            for phase_index, phase in enumerate(PHASES):
                image = person(stage_id, branch, index, direction, "move", phase_index)
                path = stage_dir / f"{stage_id}-{direction}-{phase}.png"
                save_frame(image, path)
                records.append({"id": f"{stage_id}/{direction}/{phase}", "stage": stage_id, "direction": direction, "phase": phase, "file": str(path.relative_to(OUT)).replace("\\", "/"), "size": list(SIZE), "pivot": list(PIVOT), "mirrored": False, "runtimeReady": False})
            for state in POSES:
                image = person(stage_id, branch, index, direction, state, 1 if state == "interact" else 0)
                path = stage_dir / f"{stage_id}-{direction}-{state}.png"
                save_frame(image, path)
                records.append({"id": f"{stage_id}/{direction}/{state}", "stage": stage_id, "direction": direction, "state": state, "file": str(path.relative_to(OUT)).replace("\\", "/"), "size": list(SIZE), "pivot": list(PIVOT), "mirrored": False, "runtimeReady": False})
    master_path = OUT / "alternate-life-arc-stage-masters.png"
    masters.save(master_path, format="PNG", optimize=False)
    movement_paths = [OUT / r["file"] for r in records if "phase" in r]
    pose_paths = [OUT / r["file"] for r in records if "state" in r]
    movement_path = OUT / "alternate-life-arc-movement-atlas-24x32.png"
    pose_path = OUT / "alternate-life-arc-pose-atlas-24x32.png"
    movement_size = atlas(movement_paths, 16, movement_path)
    pose_size = atlas(pose_paths, 8, pose_path)
    preview_path = OUT / "alternate-life-arc-preview-4x.png"
    preview_size = build_preview(records, preview_path)
    stage_atlases: dict[str, dict[str, Any]] = {}
    for stage_id, _, branch, _ in STAGES:
        stage_records = [r for r in records if r["stage"] == stage_id]
        move = [OUT / r["file"] for r in stage_records if "phase" in r]
        pose = [OUT / r["file"] for r in stage_records if "state" in r]
        mp = OUT / "atlases" / f"{stage_id}-movement.png"
        pp = OUT / "atlases" / f"{stage_id}-poses.png"
        ms, ps = atlas(move, 4, mp), atlas(pose, 4, pp)
        stage_atlases[stage_id] = {"branch": branch, "movement": {"file": str(mp.relative_to(OUT)), "size": list(ms), "sha256": sha256(mp)}, "poses": {"file": str(pp.relative_to(OUT)), "size": list(ps), "sha256": sha256(pp)}}
    branch_atlases: dict[str, dict[str, Any]] = {}
    for branch in ("shared", "woman", "man"):
        ids = [s[0] for s in STAGES if s[2] == branch]
        move = [OUT / r["file"] for r in records if r["stage"] in ids and "phase" in r]
        pose = [OUT / r["file"] for r in records if r["stage"] in ids and "state" in r]
        mp = OUT / "atlases" / f"{branch}-movement.png"
        pp = OUT / "atlases" / f"{branch}-poses.png"
        ms, ps = atlas(move, 16, mp), atlas(pose, 8, pp)
        branch_atlases[branch] = {"movement": {"file": str(mp.relative_to(OUT)), "size": list(ms), "sha256": sha256(mp)}, "poses": {"file": str(pp.relative_to(OUT)), "size": list(ps), "sha256": sha256(pp)}}
    manifest = {"schemaVersion": 1, "id": "alternate-life-arc-family-v1", "status": "original-rights-safe-procedural-concept", "runtimeReady": False, "description": "Distinct secondary player family with a continuous auburn-haired, warm-olive identity across ten life stages.", "identity": {"skinTone": "warm olive", "hair": "auburn with silver strands in elder stages", "persistentCues": ["mustard scarf", "teal satchel", "gold star clip"], "outfit": "navy and berry with teal accessory", "distinctFrom": "primary deep-brown, coiled-hair, sky-blue, facial-mark arc"}, "directions": list(DIRECTIONS), "phases": list(PHASES), "poses": list(POSES), "frameSize": list(SIZE), "pivot": list(PIVOT), "coverage": {"stages": len(STAGES), "movementFrames": len(movement_paths), "poseFrames": len(pose_paths), "totalFrames": len(records), "expectedTotal": 240, "directionViewsIndependentlyAuthored": True, "mirroredFrames": 0}, "sourcePolicy": "No supplied ZIP content or third-party art copied. Procedural Pillow drawings are original source art for this concept batch.", "sourcePrompt": "Original pixel-art secondary player family for a top-down ordinary-life simulator: warm olive complexion, auburn hair, mustard scarf, teal satchel, small gold star clip; preserve the cues while changing proportions from infant crawl through toddler, child, teen, young adult, midlife and elder woman/man. Four authored top-down directions, four readable walk phases, idle and reaching interaction, crisp 24x32 RGBA clusters, transparent background, no text, no logos, no mirror flips.", "sourceMaster": {"file": master_path.name, "sha256": sha256(master_path), "size": list(masters.size)}, "outputs": {"movementAtlas": {"file": movement_path.name, "size": list(movement_size), "sha256": sha256(movement_path)}, "poseAtlas": {"file": pose_path.name, "size": list(pose_size), "sha256": sha256(pose_path)}, "preview": {"file": preview_path.name, "size": list(preview_size), "sha256": sha256(preview_path)}, "stageAtlases": stage_atlases, "branchAtlases": branch_atlases}, "records": records, "limitations": ["Concept quality only; small sprites require human pixel cleanup.", "Identity continuity is structurally encoded but needs art-direction review before runtime.", "All frames remain runtimeReady false until renderer integration and in-game review."]}
    with (OUT / "manifest.json").open("w", encoding="utf-8") as stream:
        json.dump(manifest, stream, indent=2)
        stream.write("\n")
    provenance = {"tool": "offline deterministic Pillow builder", "license": "original project-owned concept art", "sourcePrompt": manifest["sourcePrompt"], "externalInputs": [], "generatedOutputs": ["manifest.json", "alternate-life-arc-stage-masters.png", "alternate-life-arc-movement-atlas-24x32.png", "alternate-life-arc-pose-atlas-24x32.png", "alternate-life-arc-preview-4x.png"], "runtimeReady": False}
    with (OUT / "provenance.json").open("w", encoding="utf-8") as stream:
        json.dump(provenance, stream, indent=2)
        stream.write("\n")
    hashes = []
    for path in sorted(OUT.rglob("*")):
        if path.is_file() and path.name not in {"hashes.sha256"}:
            hashes.append(f"{sha256(path)}  {path.relative_to(OUT).as_posix()}")
    (OUT / "hashes.sha256").write_text("\n".join(hashes) + "\n", encoding="utf-8")
    print(json.dumps({"frames": len(records), "movement": len(movement_paths), "poses": len(pose_paths), "master": list(masters.size)}))


if __name__ == "__main__":
    main()
