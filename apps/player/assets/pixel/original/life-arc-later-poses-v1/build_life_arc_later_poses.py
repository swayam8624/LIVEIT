"""Build later-life idle and everyday-interaction pose studies.

This is a deterministic adaptation pass over the already-derived 24x32 frames
in ``life-arc-later-cycles-v1``. It deliberately leaves the source batch
untouched and keeps every output outside the runtime intake path.
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
FRAME_ROOT = ROOT / "frames"
SIZE = (24, 32)
PIVOT = (12, 31)
DIRECTIONS = ("south", "west", "east", "north")
STAGES = ("young-adult-woman", "midlife-woman")
STATES = ("idle", "interact")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_frame(stage: str, direction: str, phase: str) -> Path:
    return SOURCE_FRAME_ROOT / stage / f"{stage}-{direction}-{phase}.png"


def pick_palette(image: Image.Image) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
    """Pick two source colors for tiny interaction accents, reproducibly."""

    colors = Counter(pixel for pixel in image.convert("RGBA").getdata() if pixel[3] > 0)
    sky = [
        (count, pixel)
        for pixel, count in colors.items()
        if pixel[2] >= pixel[1] and pixel[2] > pixel[0] + 10 and sum(pixel[:3]) > 120
    ]
    ochre = [
        (count, pixel)
        for pixel, count in colors.items()
        if pixel[0] > pixel[1] + 20 and pixel[1] > pixel[2] + 8 and sum(pixel[:3]) > 120
    ]
    sky_color = max(sky, default=(0, (38, 114, 151, 255)))[1]
    ochre_color = max(ochre, default=(0, (188, 101, 35, 255)))[1]
    return sky_color, ochre_color


def idle_pose(base: Image.Image) -> Image.Image:
    """Create a grounded idle hold with a one-pixel upper-body settling bob."""

    result = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    # Keep the feet and bottom-center pivot fixed while settling the upper
    # silhouette. This is a pose study, not an anatomy redraw.
    result.alpha_composite(base.crop((0, 0, SIZE[0], 1)), (0, 0))
    result.alpha_composite(base.crop((0, 1, SIZE[0], 24)), (0, 0))
    result.alpha_composite(base.crop((0, 24, SIZE[0], SIZE[1])), (0, 24))
    return result


def interact_pose(base: Image.Image, direction: str, sky: tuple[int, int, int, int], ochre: tuple[int, int, int, int]) -> Image.Image:
    """Add a tiny non-romantic greeting/inspection cue to a walk-derived hold."""

    result = base.copy().convert("RGBA")
    # A two-pixel sky-blue phone/notebook cue is kept inside the 24x32 frame.
    # Direction-specific placement makes it read as a held object rather than
    # a UI mark. The ochre pixel is a hand/wrist highlight sampled from the
    # same source palette.
    anchors = {
        "south": (16, 18),
        "west": (5, 18),
        "east": (18, 18),
        "north": (7, 18),
    }
    x, y = anchors[direction]
    if direction in ("west", "north"):
        pixels = ((x, y, sky), (x + 1, y, sky), (x + 1, y + 1, ochre))
    else:
        pixels = ((x, y, sky), (x - 1, y, sky), (x - 1, y + 1, ochre))
    for px, py, color in pixels:
        if 0 <= px < SIZE[0] and 0 <= py < SIZE[1]:
            result.putpixel((px, py), color)
    return result


def main() -> None:
    FRAME_ROOT.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    source_records: list[dict[str, object]] = []
    for stage in STAGES:
        stage_dir = FRAME_ROOT / stage
        stage_dir.mkdir(parents=True, exist_ok=True)
        stage_source_files: set[str] = set()
        atlas = Image.new("RGBA", (SIZE[0] * 8, SIZE[1]), (0, 0, 0, 0))
        for direction_index, direction in enumerate(DIRECTIONS):
            idle_source = source_frame(stage, direction, "contact-a")
            interact_source = source_frame(stage, direction, "passing-a")
            idle_base = Image.open(idle_source).convert("RGBA")
            interact_base = Image.open(interact_source).convert("RGBA")
            sky, ochre = pick_palette(interact_base)
            for state_index, (state, base, source_path) in enumerate(
                (("idle", idle_base, idle_source), ("interact", interact_base, interact_source))
            ):
                frame = idle_pose(base) if state == "idle" else interact_pose(base, direction, sky, ochre)
                filename = f"{stage}-{direction}-{state}.png"
                frame_path = stage_dir / filename
                frame.save(frame_path)
                atlas.alpha_composite(frame, ((direction_index * 2 + state_index) * SIZE[0], 0))
                stage_source_files.add(str(source_path.relative_to(SOURCE_ROOT)))
                records.append(
                    {
                        "id": f"{stage}/{direction}/{state}",
                        "stage": stage,
                        "direction": direction,
                        "state": state,
                        "file": f"frames/{stage}/{filename}",
                        "sha256": sha256(frame_path),
                        "atlas": {
                            "file": f"frames/{stage}/{stage}-atlas.png",
                            "x": (direction_index * 2 + state_index) * SIZE[0],
                            "y": 0,
                            "width": SIZE[0],
                            "height": SIZE[1],
                        },
                        "pivot": list(PIVOT),
                        "size": list(SIZE),
                        "mode": "RGBA",
                        "runtimeReady": False,
                        "sourceBatch": "../life-arc-later-cycles-v1",
                        "sourceFrame": str(source_path.relative_to(SOURCE_ROOT)),
                        "adaptation": "upper-body settling bob" if state == "idle" else "directional held-object cue",
                    }
                )
        atlas.save(stage_dir / f"{stage}-atlas.png")
        for source_name in sorted(stage_source_files):
            source_path = SOURCE_ROOT / source_name
            image = Image.open(source_path).convert("RGBA")
            source_records.append(
                {
                    "file": f"../life-arc-later-cycles-v1/{source_name}",
                    "sha256": sha256(source_path),
                    "size": list(image.size),
                    "mode": image.mode,
                }
            )

    combined = Image.new("RGBA", (SIZE[0] * 8, SIZE[1] * 2), (0, 0, 0, 0))
    for index, stage in enumerate(STAGES):
        combined.alpha_composite(Image.open(FRAME_ROOT / stage / f"{stage}-atlas.png").convert("RGBA"), (0, index * SIZE[1]))
    combined.save(ROOT / "life-arc-later-poses-atlas.png")
    combined.resize((combined.width * 4, combined.height * 4), Image.Resampling.NEAREST).save(ROOT / "life-arc-later-poses-preview-4x.png")

    manifest = {
        "schemaVersion": 1,
        "id": "life-arc-later-poses-v1",
        "description": "Young-adult and midlife woman idle and everyday-interaction pose studies derived from the linked later-life walk frames.",
        "logicalFrameSize": list(SIZE),
        "pivot": list(PIVOT),
        "stages": list(STAGES),
        "directions": list(DIRECTIONS),
        "states": list(STATES),
        "runtimeReady": False,
        "sourcePolicy": "Only local derived frames under ../life-arc-later-cycles-v1/frames were used as visual references.",
        "sources": source_records,
        "frames": records,
        "limitations": [
            "These are deterministic stylized adaptations, not genuinely redrawn anatomy.",
            "Idle uses a one-pixel upper-body settling bob while retaining the source feet and pivot.",
            "Interact adds a tiny held-object/greeting cue using colors sampled from the same source frame.",
            "Human pixel-cluster cleanup, identity continuity review, renderer sampling, collision review, and gameplay integration remain pending.",
        ],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
