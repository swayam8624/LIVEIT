"""Build an optional shared-palette rendition without altering source frames."""
from pathlib import Path
from PIL import Image
import json, hashlib

ROOT = Path(__file__).parent
ASSET_ROOT = ROOT.parent
manifest = json.loads((ROOT / "manifest.json").read_text())
output_root = ROOT / "harmonized-32-color"
output_root.mkdir(exist_ok=True)

# Build one palette from all visible colors across every stage.
visible_rows = []
frame_records = [frame for stage in manifest["stages"] for frame in stage["frames"]]
for record in frame_records:
    source = ASSET_ROOT / record["file"]
    rgba = Image.open(source).convert("RGBA")
    rgb = rgba.convert("RGB")
    alpha = rgba.getchannel("A")
    pixels = rgb.load()
    alpha_pixels = alpha.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            if alpha_pixels[x, y] > 0:
                visible_rows.append(pixels[x, y])

sample = Image.new("RGB", (max(1, len(visible_rows)), 1))
sample.putdata(visible_rows)
palette_image = sample.quantize(colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
palette_rgb = palette_image.convert("RGB")
palette_path = output_root / "shared-palette-swatch.png"
palette_rgb.save(palette_path)

stage_records = []
combined = Image.new("RGBA", (96, 128 * len(manifest["stages"])), (0, 0, 0, 0))
for stage_index, stage in enumerate(manifest["stages"]):
    atlas = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    frames = []
    for frame in stage["frames"]:
        source = ASSET_ROOT / frame["file"]
        rgba = Image.open(source).convert("RGBA")
        alpha = rgba.getchannel("A")
        indexed = rgba.convert("RGB").quantize(palette=palette_image, dither=Image.Dither.NONE)
        recolored = indexed.convert("RGB").convert("RGBA")
        recolored.putalpha(alpha)
        out = output_root / "frames" / stage["id"] / Path(frame["file"]).name
        out.parent.mkdir(parents=True, exist_ok=True)
        recolored.save(out)
        atlas.alpha_composite(recolored, ((manifest["phases"].index(frame["phase"])) * 24, (manifest["directions"].index(frame["direction"])) * 32))
        frames.append({"file": str(out.relative_to(ROOT)), "sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "source": frame["file"], "sourceSha256": frame["sha256"]})
    atlas_path = output_root / f"{stage['id']}-atlas.png"
    atlas.save(atlas_path)
    combined.alpha_composite(atlas, (0, stage_index * 128))
    stage_records.append({"id": stage["id"], "atlas": str(atlas_path.relative_to(ROOT)), "frames": frames})

combined_path = output_root / "linked-life-arc-atlas.png"
combined.save(combined_path)
preview_path = output_root / "linked-life-arc-preview-4x.png"
combined.resize((combined.width * 4, combined.height * 4), Image.Resampling.NEAREST).save(preview_path)

result = {
    "schemaVersion": 1,
    "id": "linked-life-arc-shared-palette-v1",
    "parentManifest": "../manifest.json",
    "paletteColors": 32,
    "dither": "none",
    "runtimeReady": False,
    "stages": stage_records,
    "atlas": {"file": str(combined_path.relative_to(ROOT)), "size": list(combined.size), "mode": "RGBA", "sha256": hashlib.sha256(combined_path.read_bytes()).hexdigest()},
    "preview": {"file": str(preview_path.relative_to(ROOT)), "size": list(Image.open(preview_path).size), "mode": "RGBA", "sha256": hashlib.sha256(preview_path.read_bytes()).hexdigest()},
    "limitations": ["One global palette may blur differences in skin tones, outfits, and age-specific cues.", "Palette reduction is an optional comparison, not an approved replacement for manual art direction.", "Identity continuity still requires human review across the independently generated source sheets."],
}
(output_root / "manifest.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"Built shared-palette atlas for {len(stage_records)} stages using 32 colors.")
