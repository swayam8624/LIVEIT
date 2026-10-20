"""Derive transparent NPC walk frames from the preserved original source sheet.

The source sheet is never rewritten. Generated concepts remain runtimeReady=false
until an art pass and engine import review approve them.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageEnhance

ROOT = Path(__file__).parent
SOURCE = ROOT / "npc-archetypes-source.png"
FRAME_SIZE = (96, 128)
# The image generator centered the four poses in a 512 px working column.
# Keep the full 1024x1536 source intact and crop the 128 px cells from x=256.
CELL_W, CELL_H = 128, 128
GRID_X = 256
IDENTITIES = {
    "sari-caregiver": (0, [0, 128, 239, 358]),
    "cane-neighbor": (0, [500, 628, 748, 872]),
    "garden-keeper": (0, [1010, 1168, 1255, 1374]),
}
DIRECTIONS = ("front", "back", "left", "right")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remove_dark_background(cell: Image.Image) -> Image.Image:
    rgba = cell.convert("RGBA")
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            # The generated sheet uses a charcoal studio field. Keep the colored
            # sprite pixels while removing that near-neutral field and its halo.
            chroma = max(r, g, b) - min(r, g, b)
            if max(r, g, b) < 46 and chroma < 14:
                px[x, y] = (r, g, b, 0)
    # Remove disconnected fragments caused by adjacent rows in the generated
    # sheet. Keep the dominant sprite and nearby accessory components (tote,
    # cane, or watering can) while rejecting distant head/foot fragments.
    mask = {(x, y) for y in range(rgba.height) for x in range(rgba.width) if rgba.getpixel((x, y))[3] > 0}
    components = []
    while mask:
        seed = mask.pop()
        stack = [seed]
        component = {seed}
        while stack:
            x, y = stack.pop()
            for nx in range(x - 1, x + 2):
                for ny in range(y - 1, y + 2):
                    if (nx, ny) in mask:
                        mask.remove((nx, ny))
                        component.add((nx, ny))
                        stack.append((nx, ny))
        components.append(component)
    if components:
        main = max(components, key=len)
        min_x, min_y = min(x for x, _ in main), min(y for _, y in main)
        max_x, max_y = max(x for x, _ in main), max(y for _, y in main)
        keep = set(main)
        for component in components:
            if component is main:
                continue
            cmin_x, cmin_y = min(x for x, _ in component), min(y for _, y in component)
            cmax_x, cmax_y = max(x for x, _ in component), max(y for _, y in component)
            gap_x = max(min_x - cmax_x, cmin_x - max_x, 0)
            gap_y = max(min_y - cmax_y, cmin_y - max_y, 0)
            if gap_x <= 24 and gap_y <= 6:
                keep.update(component)
        for y in range(rgba.height):
            for x in range(rgba.width):
                if (x, y) not in keep:
                    r, g, b, _ = rgba.getpixel((x, y))
                    rgba.putpixel((x, y), (r, g, b, 0))
    box = rgba.getbbox()
    if not box:
        return Image.new("RGBA", FRAME_SIZE)
    cropped = rgba.crop(box)
    # Preserve crisp pixel edges while fitting a stable gameplay frame.
    scale = min((FRAME_SIZE[0] - 12) / cropped.width, (FRAME_SIZE[1] - 8) / cropped.height)
    size = (max(1, round(cropped.width * scale)), max(1, round(cropped.height * scale)))
    resized = cropped.resize(size, Image.Resampling.NEAREST)
    out = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
    out.paste(resized, ((FRAME_SIZE[0] - size[0]) // 2, FRAME_SIZE[1] - size[1] - 4), resized)
    return out


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    if source.size != (1024, 1536):
        raise SystemExit(f"unexpected source size {source.size}; expected 1024x1536")
    records = []
    for identity, (_, row_starts) in IDENTITIES.items():
        out_dir = ROOT / identity
        out_dir.mkdir(exist_ok=True)
        frames = []
        for direction_index, direction in enumerate(DIRECTIONS):
            direction_dir = out_dir / direction
            direction_dir.mkdir(exist_ok=True)
            for phase in range(4):
                x = GRID_X + phase * CELL_W
                y = row_starts[direction_index]
                frame = remove_dark_background(source.crop((x, y, x + CELL_W, y + CELL_H)))
                path = direction_dir / f"phase-{phase + 1:02d}.png"
                frame.save(path)
                frames.append({
                    "direction": direction,
                    "phase": phase + 1,
                    "file": str(path.relative_to(out_dir)),
                    "width": FRAME_SIZE[0],
                    "height": FRAME_SIZE[1],
                    "mode": "RGBA",
                    "pivot": {"x": 48, "y": 124},
                    "runtimeReady": False,
                    "sha256": sha256(path),
                })
        atlas = Image.new("RGBA", (FRAME_SIZE[0] * 4, FRAME_SIZE[1] * 4), (0, 0, 0, 0))
        for item in frames:
            direction_index = DIRECTIONS.index(item["direction"])
            phase = item["phase"] - 1
            image = Image.open(out_dir / item["file"])
            atlas.paste(image, (phase * FRAME_SIZE[0], direction_index * FRAME_SIZE[1]), image)
        atlas_path = out_dir / "walk-atlas-4x4.png"
        atlas.save(atlas_path)
        preview = atlas.resize((atlas.width * 2, atlas.height * 2), Image.Resampling.NEAREST)
        preview_path = out_dir / "walk-atlas-preview-2x.png"
        preview.save(preview_path)
        manifest = {
            "id": f"npc-{identity}-walk-v1",
            "character": identity,
            "source": "../npc-archetypes-source.png",
            "frameSize": {"width": FRAME_SIZE[0], "height": FRAME_SIZE[1]},
            "directions": list(DIRECTIONS),
            "phasesPerDirection": 4,
            "frames": frames,
            "atlas": {"file": "walk-atlas-4x4.png", "width": atlas.width, "height": atlas.height, "runtimeReady": False, "sha256": sha256(atlas_path)},
            "preview": {"file": "walk-atlas-preview-2x.png", "scale": 2, "runtimeReady": False, "sha256": sha256(preview_path)},
            "runtimeReady": False,
        }
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        records.append({"identity": identity, "manifest": f"{identity}/manifest.json", "runtimeReady": False})
    (ROOT / "manifest.json").write_text(json.dumps({
        "id": "npc-archetype-walk-v1",
        "kind": "original-pixel-npc-movement-concepts",
        "source": "npc-archetypes-source.png",
        "identities": records,
        "runtimeReady": False,
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
