"""Build the isolated linked elder idle/interact concept batch.

The source batch is kept outside this folder and is never modified. Every
direction is authored from its matching source frame; this builder does not
mirror a frame to synthesize another direction.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).parent
SOURCE_ROOT = ROOT.parent / "life-arc-later-cycles-v1"
SOURCE_FRAME_ROOT = SOURCE_ROOT / "frames"
SIZE = (24, 32)
PIVOT = (12, 31)
DIRECTIONS = ("south", "west", "east", "north")
STAGES = ("elder-woman", "elder-man")
STATES = ("idle", "interact")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_frame(stage: str, direction: str, phase: str) -> Path:
    return SOURCE_FRAME_ROOT / stage / f"{stage}-{direction}-{phase}.png"


def pick_colors(image: Image.Image) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
    """Select the linked sky-blue and warm ochre colors from this frame."""

    colors = Counter(pixel for pixel in image.convert("RGBA").getdata() if pixel[3] > 0)
    blue = [
        (count, pixel)
        for pixel, count in colors.items()
        if pixel[2] > pixel[0] + 16 and pixel[2] >= pixel[1] and sum(pixel[:3]) > 100
    ]
    ochre = [
        (count, pixel)
        for pixel, count in colors.items()
        if pixel[0] > pixel[2] + 20 and pixel[1] > pixel[2] + 10 and sum(pixel[:3]) > 100
    ]
    return (
        max(blue, default=(0, (43, 111, 151, 255)))[1],
        max(ochre, default=(0, (190, 105, 34, 255)))[1],
    )


def grounded_idle(base: Image.Image) -> Image.Image:
    """Keep the original contact silhouette and preserve its bottom pivot."""

    # Copying the matching contact frame retains the source's independently
    # authored direction and grounded feet. No directional mirroring occurs.
    return base.convert("RGBA").copy()


def interaction_pose(
    base: Image.Image,
    stage: str,
    direction: str,
    blue: tuple[int, int, int, int],
    ochre: tuple[int, int, int, int],
) -> Image.Image:
    """Add a small, accessible greeting or steadying cue per direction."""

    result = base.convert("RGBA").copy()
    # These are hand-authored coordinates for each facing. They deliberately
    # differ by direction instead of deriving one pose by flipping another.
    anchors = {
        "south": (16, 16),
        "west": (5, 17),
        "east": (18, 17),
        "north": (8, 16),
    }
    x, y = anchors[direction]
    if stage == "elder-woman":
        # A two-pixel open-hand wave, kept close to the shoulder and inside
        # the silhouette. The warm pixel gives the hand a source-palette cue.
        offsets = {
            "south": ((0, 0, blue), (1, -1, blue), (1, 0, ochre)),
            "west": ((0, 0, blue), (-1, -1, blue), (0, -1, ochre)),
            "east": ((0, 0, blue), (1, -1, blue), (1, 0, ochre)),
            "north": ((0, 0, blue), (-1, -1, blue), (-1, 0, ochre)),
        }[direction]
        adaptation = "direction-authored open-hand wave cue"
    else:
        # A short blue shaft and warm grip read as a steadying cane / hello
        # gesture. Placement changes with facing and never uses a mirror.
        offsets = {
            "south": ((0, 0, blue), (0, 1, blue), (1, 0, ochre)),
            "west": ((0, 0, blue), (-1, 1, blue), (-1, 0, ochre)),
            "east": ((0, 0, blue), (1, 1, blue), (1, 0, ochre)),
            "north": ((0, 0, blue), (0, 1, blue), (-1, 0, ochre)),
        }[direction]
        adaptation = "direction-authored steadying-cane greeting cue"
    for dx, dy, color in offsets:
        px, py = x + dx, y + dy
        if 0 <= px < SIZE[0] and 0 <= py < SIZE[1]:
            result.putpixel((px, py), color)
    result.info["adaptation"] = adaptation
    return result


def main() -> None:
    frame_root = ROOT / "frames"
    frame_root.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    source_records: dict[str, dict[str, object]] = {}

    for stage in STAGES:
        stage_dir = frame_root / stage
        stage_dir.mkdir(parents=True, exist_ok=True)
        atlas = Image.new("RGBA", (SIZE[0] * 8, SIZE[1]), (0, 0, 0, 0))
        for direction_index, direction in enumerate(DIRECTIONS):
            idle_source = source_frame(stage, direction, "contact-a")
            interact_source = source_frame(stage, direction, "passing-a")
            with Image.open(idle_source).convert("RGBA") as idle_base, Image.open(interact_source).convert("RGBA") as interact_base:
                if idle_base.size != SIZE or interact_base.size != SIZE:
                    raise ValueError(f"Unexpected source size for {stage}/{direction}")
                blue, ochre = pick_colors(interact_base)
                variants = (
                    ("idle", grounded_idle(idle_base), idle_source, "matching contact frame"),
                    (
                        "interact",
                        interaction_pose(interact_base, stage, direction, blue, ochre),
                        interact_source,
                        "direction-authored greeting cue",
                    ),
                )
            for state_index, (state, frame, source_path, adaptation) in enumerate(variants):
                filename = f"{stage}-{direction}-{state}.png"
                frame_path = stage_dir / filename
                frame.save(frame_path)
                atlas_x = (direction_index * 2 + state_index) * SIZE[0]
                atlas.alpha_composite(frame, (atlas_x, 0))
                source_key = str(source_path.relative_to(SOURCE_ROOT))
                source_records[source_key] = {
                    "file": f"../life-arc-later-cycles-v1/{source_key}",
                    "sha256": sha256(source_path),
                    "size": list(Image.open(source_path).size),
                    "mode": "RGBA",
                }
                records.append(
                    {
                        "id": f"{stage}/{direction}/{state}",
                        "stage": stage,
                        "direction": direction,
                        "state": state,
                        "file": f"frames/{stage}/{filename}",
                        "sha256": sha256(frame_path),
                        "sourceFrame": f"../life-arc-later-cycles-v1/{source_key}",
                        "sourceFrameSha256": sha256(source_path),
                        "sourceSheet": f"../life-arc-later-cycles-v1/frames/{stage}/{stage}-atlas.png",
                        "sourceSheetSha256": sha256(SOURCE_FRAME_ROOT / stage / f"{stage}-atlas.png"),
                        "atlas": {
                            "file": f"frames/{stage}/{stage}-atlas.png",
                            "x": atlas_x,
                            "y": 0,
                            "width": SIZE[0],
                            "height": SIZE[1],
                        },
                        "pivot": list(PIVOT),
                        "size": list(SIZE),
                        "mode": "RGBA",
                        "mirrored": False,
                        "runtimeReady": False,
                        "adaptation": adaptation,
                    }
                )
        atlas_path = stage_dir / f"{stage}-atlas.png"
        atlas.save(atlas_path)

    combined = Image.new("RGBA", (SIZE[0] * 8, SIZE[1] * len(STAGES)), (0, 0, 0, 0))
    for stage_index, stage in enumerate(STAGES):
        stage_atlas = Image.open(frame_root / stage / f"{stage}-atlas.png").convert("RGBA")
        combined.alpha_composite(stage_atlas, (0, stage_index * SIZE[1]))
    combined_path = ROOT / "linked-elder-poses-atlas.png"
    combined.save(combined_path)
    preview = combined.resize((combined.width * 6, combined.height * 6), Image.Resampling.NEAREST)
    preview_path = ROOT / "linked-elder-poses-preview-6x.png"
    preview.save(preview_path)

    manifest = {
        "schemaVersion": 1,
        "id": "linked-elder-poses-v1",
        "description": "Concept-only linked elder woman and elder man idle/interact pose studies with care-safe greeting cues.",
        "logicalFrameSize": list(SIZE),
        "pivot": list(PIVOT),
        "stages": list(STAGES),
        "directions": list(DIRECTIONS),
        "states": list(STATES),
        "frameCount": len(records),
        "runtimeReady": False,
        "conceptOnly": True,
        "sourcePolicy": "Only local original elder frames from life-arc-later-cycles-v1 were used; no ZIP or external asset was used.",
        "identityCues": [
            "silver-white elder hair against the linked deep-brown skin palette",
            "recurring sky-blue clothing accent",
            "warm ochre accessory and hand cues sampled from each source frame",
        ],
        "interactionPolicy": "Care-safe accessible greeting studies: open-hand wave for elder woman; steadying cane/hello cue for elder man.",
        "linkedFamilyReferences": [
            {
                "file": f"../linked-life-arc-family-v1/harmonized-32-color/{stage}-atlas.png",
                "sha256": sha256(ROOT.parent / "linked-life-arc-family-v1" / "harmonized-32-color" / f"{stage}-atlas.png"),
                "size": [96, 128],
                "mode": "RGBA",
                "purpose": "palette and elder identity cue comparison only",
            }
            for stage in STAGES
        ],
        "sources": list(source_records.values()),
        "frames": records,
        "atlases": [
            {"file": f"frames/{stage}/{stage}-atlas.png", "size": [SIZE[0] * 8, SIZE[1]], "mode": "RGBA", "sha256": sha256(frame_root / stage / f"{stage}-atlas.png")} for stage in STAGES
        ],
        "combinedAtlas": {"file": combined_path.name, "size": list(combined.size), "mode": "RGBA", "sha256": sha256(combined_path)},
        "preview": {"file": preview_path.name, "size": list(preview.size), "mode": "RGBA", "sha256": sha256(preview_path)},
        "limitations": [
            "These are concept-only adaptations over linked elder source frames, not final pixel-artist redraws.",
            "A human pixel artist must reconcile hands, cane/wave readability, clothing folds, face continuity, and timing before runtime use.",
            "Collision boxes, renderer sampling, save continuity, accessibility review, and gameplay integration remain unverified.",
        ],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
