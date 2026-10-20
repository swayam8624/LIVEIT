"""Deterministically extract the age/identity study into reviewable concept frames.

The two generated source sheets are preserved byte-for-byte in source/. All
derived frames are concept references only and are intentionally marked
runtimeReady=false in manifest.json.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
SRC = ROOT / "source"
IDENTITIES = ROOT / "identities"
WALKS = ROOT / "walk-cycles"
NAMES = ["child-a", "child-b", "teen-a", "teen-b", "adult-a", "adult-b", "elder-a", "elder-b"]


def bounds(total, pieces, index):
    return round(total * index / pieces), round(total * (index + 1) / pieces)


def save_scaled(im, path, size):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.resize(size, Image.Resampling.NEAREST).save(path)


def main():
    lineup = Image.open(SRC / "age-identity-lineup-original.png").convert("RGB")
    walk = Image.open(SRC / "age-identity-walk-original.png").convert("RGB")
    identity_records = []
    walk_records = []

    # The lineup has two columns and four life-stage rows.
    for i, name in enumerate(NAMES):
        row, col = divmod(i, 2)
        x0, x1 = bounds(lineup.width, 2, col)
        y0, y1 = bounds(lineup.height, 4, row)
        cell = lineup.crop((x0, y0, x1, y1))
        out = IDENTITIES / f"{name}-identity-256x192.png"
        save_scaled(cell, out, (256, 192))
        identity_records.append({
            "id": name,
            "stage": name.split("-")[0],
            "file": out.relative_to(ROOT).as_posix(),
            "sourceCrop": {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0},
            "dimensions": [256, 192],
            "mode": "RGB",
            "runtimeReady": False,
        })

    # The movement sheet is two rows by four panels. Each panel contains four
    # horizontal phases. Output 96x128 RGBA frames for later engine review.
    for i, name in enumerate(NAMES):
        row, col = divmod(i, 4)
        px0, px1 = bounds(walk.width, 4, col)
        py0, py1 = bounds(walk.height, 2, row)
        panel = walk.crop((px0, py0, px1, py1))
        phase_dir = WALKS / name
        phase_dir.mkdir(parents=True, exist_ok=True)
        frames = []
        for phase in range(4):
            fx0, fx1 = bounds(panel.width, 4, phase)
            frame = panel.crop((fx0, 0, fx1, panel.height)).convert("RGBA")
            path = phase_dir / f"frame-{phase:02d}.png"
            save_scaled(frame, path, (96, 128))
            frames.append({
                "phase": phase,
                "file": path.relative_to(ROOT).as_posix(),
                "sourceCrop": {"x": px0 + fx0, "y": py0, "width": fx1 - fx0, "height": py1 - py0},
                "dimensions": [96, 128],
                "mode": "RGBA",
                "pivot": {"x": 48, "y": 112},
            })
        atlas = Image.new("RGBA", (96 * 4, 128), (12, 19, 35, 255))
        for phase in range(4):
            atlas.alpha_composite(Image.open(phase_dir / f"frame-{phase:02d}.png"), (phase * 96, 0))
        atlas_path = phase_dir / "walk-atlas-384x128.png"
        atlas.save(atlas_path)
        preview = atlas.resize((384, 512), Image.Resampling.NEAREST)
        preview_path = phase_dir / "walk-preview-4x.png"
        preview.save(preview_path)
        walk_records.append({
            "id": name,
            "stage": name.split("-")[0],
            "directions": ["three-quarter-front"],
            "phaseCount": 4,
            "frames": frames,
            "atlas": atlas_path.relative_to(ROOT).as_posix(),
            "preview": preview_path.relative_to(ROOT).as_posix(),
            "runtimeReady": False,
        })

    # Review montage: each identity is a row of four phases with a stage tint.
    montage = Image.new("RGBA", (4 * 128, 8 * 160), (8, 12, 24, 255))
    draw = ImageDraw.Draw(montage)
    for i, name in enumerate(NAMES):
        y = i * 160
        draw.text((2, y + 130), name, fill=(230, 235, 245, 255))
        for phase in range(4):
            frame = Image.open(WALKS / name / f"frame-{phase:02d}.png").resize((128, 160), Image.Resampling.NEAREST)
            montage.alpha_composite(frame, (phase * 128, y))
    montage.save(ROOT / "age-identity-walk-montage-4x.png")

    manifest = {
        "id": "age-identity-variety-v1",
        "purpose": "Original age and identity variety study with concept walk mini-cycles.",
        "sourceImages": [
            {"file": "source/age-identity-lineup-original.png", "dimensions": [1024, 1536], "mode": "RGB"},
            {"file": "source/age-identity-walk-original.png", "dimensions": [1774, 887], "mode": "RGB"},
        ],
        "identities": identity_records,
        "walkCycles": walk_records,
        "preview": "age-identity-walk-montage-4x.png",
        "runtimeReady": False,
        "license": "Original generated concept art; verify project policy before any runtime admission.",
        "notes": [
            "Eight identities cover child, teen, adult and elder stages with two variants per stage.",
            "Movement extraction is a four-phase three-quarter-front study only; all directions and collision pivots remain unverified.",
            "Derived images retain the source sheet's background and are not transparent production sprites.",
        ],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
