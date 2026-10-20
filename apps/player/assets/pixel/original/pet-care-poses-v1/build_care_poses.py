"""Derive isolated 96x128 concept frames from the six-pose source sheets."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
POSES = ["idle", "happy", "worried", "sleeping", "care", "recovering"]
BOUNDS = {
    "cat": [0, 350, 740, 1090, 1450, 1800, 2172],
    "dog": [0, 370, 760, 1130, 1470, 1810, 2172],
    "rabbit": [0, 350, 740, 1100, 1450, 1800, 2172],
}


def derive(animal: str) -> None:
    folder = ROOT / animal
    source_path = folder / f"{animal}-care-poses-source.png"
    source = Image.open(source_path).convert("RGBA")
    bounds = BOUNDS[animal]
    out_frames: list[str] = []
    atlas = Image.new("RGBA", (96 * len(POSES), 128), (0, 0, 0, 0))
    for index, pose in enumerate(POSES):
        crop = source.crop((bounds[index], 0, bounds[index + 1], source.height))
        bbox = crop.getchannel("A").getbbox()
        if bbox is None:
            raise RuntimeError(f"{source_path}: pose {pose} has no visible pixels")
        crop = crop.crop(bbox)
        scale = min(88 / crop.width, 112 / crop.height)
        resized = crop.resize((max(1, round(crop.width * scale)), max(1, round(crop.height * scale))), Image.Resampling.NEAREST)
        frame = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
        frame.alpha_composite(resized, ((96 - resized.width) // 2, (128 - resized.height) // 2))
        pixels = frame.load()
        for y in range(frame.height):
            for x in range(frame.width):
                r, g, b, a = pixels[x, y]
                if a <= 8 and max(r, g, b) - min(r, g, b) >= 40:
                    pixels[x, y] = (r, g, b, 0)
        # Decorative hearts/sparkles and crop remnants are tiny disconnected islands;
        # retain only components large enough to be part of the animal silhouette.
        seen: set[tuple[int, int]] = set()
        components: list[list[tuple[int, int]]] = []
        for sy in range(frame.height):
            for sx in range(frame.width):
                if (sx, sy) in seen or pixels[sx, sy][3] == 0:
                    continue
                stack = [(sx, sy)]
                seen.add((sx, sy))
                component: list[tuple[int, int]] = []
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                        if 0 <= nx < frame.width and 0 <= ny < frame.height and (nx, ny) not in seen and pixels[nx, ny][3] > 0:
                            seen.add((nx, ny))
                            stack.append((nx, ny))
                components.append(component)
        if components:
            keep = max(components, key=len)
            keep_set = set(keep)
            for component in components:
                if component is not keep and not any((x, y) in keep_set for x, y in component):
                    for x, y in component:
                        pixels[x, y] = (0, 0, 0, 0)
        name = f"{animal}-{pose}-96x128.png"
        frame.save(folder / "frames" / name)
        atlas.alpha_composite(frame, (index * 96, 0))
        out_frames.append(name)
    atlas.save(folder / f"{animal}-care-poses-atlas-576x128.png")
    atlas.resize((1152, 256), Image.Resampling.NEAREST).save(folder / f"{animal}-care-poses-preview-2x.png")
    (folder / "frames.json").write_text(json.dumps({"animal": animal, "frameSize": [96, 128], "poses": POSES, "frames": out_frames, "runtimeReady": False}, indent=2) + "\n")


if __name__ == "__main__":
    for animal in ("cat", "dog", "rabbit"):
        derive(animal)
