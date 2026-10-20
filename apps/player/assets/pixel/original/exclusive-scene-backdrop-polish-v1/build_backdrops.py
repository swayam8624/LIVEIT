from pathlib import Path
from PIL import Image
import json, hashlib

ROOT = Path(__file__).parent
SOURCE = ROOT / "source"
EXPORTS = ROOT / "exports"
EXPORTS.mkdir(exist_ok=True)

records = []
for source in sorted(SOURCE.glob("*.png")):
    image = Image.open(source).convert("RGB")
    width, height = image.size
    target_ratio = 5 / 4
    if width / height > target_ratio:
        new_width = round(height * target_ratio)
        left = (width - new_width) // 2
        image = image.crop((left, 0, left + new_width, height))
    else:
        new_height = round(width / target_ratio)
        top = (height - new_height) // 2
        image = image.crop((0, top, width, top + new_height))

    scene = source.stem.replace("-original", "")
    logical = image.resize((160, 128), Image.Resampling.LANCZOS)
    logical = logical.quantize(colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    pixel_path = EXPORTS / f"{scene}-pixel-320x256.png"
    logical.resize((320, 256), Image.Resampling.NEAREST).save(pixel_path, optimize=True)
    records.append({"id": f"{scene}.pixel-32-color", "scene": scene, "role": "pixel-cluster-background-study", "file": str(pixel_path.relative_to(ROOT)), "width": 320, "height": 256, "mode": "RGB", "colors": 32, "sampling": "160x128 quantized, 2x nearest-neighbor", "sha256": hashlib.sha256(pixel_path.read_bytes()).hexdigest(), "runtimeReady": False})

    detail = image.resize((320, 256), Image.Resampling.LANCZOS)
    detail = detail.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    detail_path = EXPORTS / f"{scene}-detail-320x256.png"
    detail.save(detail_path, optimize=True)
    records.append({"id": f"{scene}.detail-64-color", "scene": scene, "role": "detailed-background-concept", "file": str(detail_path.relative_to(ROOT)), "width": 320, "height": 256, "mode": "RGB", "colors": 64, "sampling": "Lanczos resize, no-dither 64-color palette", "sha256": hashlib.sha256(detail_path.read_bytes()).hexdigest(), "runtimeReady": False})

sources = []
for source in sorted(SOURCE.glob("*.png")):
    with Image.open(source) as image:
        sources.append({"file": str(source.relative_to(ROOT)), "dimensions": list(image.size), "mode": image.mode, "sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
manifest = {"schemaVersion": 1, "batch": "exclusive-scene-backdrop-polish-v1", "runtimeReady": False, "sources": sources, "records": records, "limitations": ["Generated background studies are detailed and softly textured compared with small-cluster character sprites.", "Pixel exports reduce detail to a 160x128 logical plate and 32 colors; assess at actual game scale.", "These are standalone background alternatives, not walkable maps, not depth layers, and not integrated with the separate scene layer batch."]}
(ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
