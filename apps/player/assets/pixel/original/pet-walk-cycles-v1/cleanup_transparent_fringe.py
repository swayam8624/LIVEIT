"""Remove only low-alpha saturated fringe pixels from derived pet frames.

The AI-generated source sheets remain untouched. The 1/255-through-8/255
alpha range is below any authored opaque pixel in these sprite concepts; the
filter only clears those pixels when they are strongly chromatic.
"""
from pathlib import Path
import json
from PIL import Image

ROOT = Path(__file__).parent
SPECIES = ("cat", "dog", "rabbit")


def clean_frame(path: Path) -> int:
    image = Image.open(path).convert("RGBA")
    pixels = image.load()
    removed = 0
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = pixels[x, y]
            if alpha <= 8 and max(red, green, blue) - min(red, green, blue) >= 40:
                pixels[x, y] = (0, 0, 0, 0)
                removed += 1
    image.save(path)
    return removed


def rebuild(species: str) -> int:
    folder = ROOT / species
    manifest_path = folder / "frames.json"
    manifest = json.loads(manifest_path.read_text())
    atlas = Image.new("RGBA", (384, 512), (0, 0, 0, 0))
    removed = 0
    for frame in manifest["frames"]:
        frame_path = folder / frame["file"]
        removed += clean_frame(frame_path)
        x = frame.get("x", frame.get("atlas", {}).get("x"))
        y = frame.get("y", frame.get("atlas", {}).get("y"))
        if x is None or y is None:
            raise ValueError(f"Missing atlas coordinates: {frame_path}")
        atlas.alpha_composite(Image.open(frame_path).convert("RGBA"), (x, y))
    atlas_spec = manifest.get("atlas")
    atlas_name = atlas_spec["file"] if isinstance(atlas_spec, dict) else atlas_spec or "atlas.png"
    atlas_path = folder / atlas_name
    atlas.save(atlas_path)
    preview_path = next(folder.glob("*preview*.png"))
    old_preview = Image.open(preview_path)
    scale_x = old_preview.width // 384
    scale_y = old_preview.height // 512
    if scale_x != scale_y:
        raise ValueError(f"Nonuniform preview scale: {preview_path}")
    atlas.resize((384 * scale_x, 512 * scale_y), Image.Resampling.NEAREST).save(preview_path)
    return removed


if __name__ == "__main__":
    counts = {species: rebuild(species) for species in SPECIES}
    print("Cleared saturated edge pixels with alpha <= 8 from derived frames:")
    for species, count in counts.items():
        print(f"{species}: {count}")
    print("Source sheets were not changed.")
