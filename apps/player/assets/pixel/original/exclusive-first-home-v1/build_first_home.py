from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent
SOURCE = ROOT / "first-home-generated-master.png"
SIZE = (320, 256)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_palette_study(image: Image.Image, colors: int, path: Path) -> None:
    reduced = image.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    reduced.convert("RGB").save(path, optimize=True)


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    logical = source.resize(SIZE, Image.Resampling.LANCZOS)

    palette_files = []
    for count in (32, 64):
        path = ROOT / f"first-home-{count}c-320x256.png"
        save_palette_study(logical, count, path)
        palette_files.append(path)

    guide = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(guide)
    # Proposed character-safe floor zone: inset from furniture and scene edges.
    draw.rectangle((87, 130, 235, 213), outline=(80, 245, 210, 210), width=1)
    draw.text((90, 132), "ACTOR SAFE", fill=(80, 245, 210, 230), font=ImageFont.load_default())
    # Dialogue zone is below the play floor and can be replaced by runtime UI.
    draw.rectangle((0, 222, 319, 255), outline=(115, 170, 255, 220), width=1)
    draw.text((5, 226), "DIALOGUE BAND", fill=(145, 190, 255, 235), font=ImageFont.load_default())
    guide_path = ROOT / "first-home-layout-guide.png"
    guide.save(guide_path, optimize=True)

    preview = Image.new("RGB", (SIZE[0] * 4, (SIZE[1] + 20) * 2), (24, 27, 40))
    font = ImageFont.load_default()
    for index, (path, label) in enumerate(zip(palette_files, ("32-COLOR STUDY", "64-COLOR STUDY"))):
        x = index * SIZE[0] * 2
        preview.paste(Image.open(path).resize(SIZE, Image.Resampling.NEAREST).resize((SIZE[0] * 2, SIZE[1] * 2), Image.Resampling.NEAREST), (x, 40))
        ImageDraw.Draw(preview).text((x + 8, 8), label, fill=(238, 220, 177), font=font)
    preview_path = ROOT / "first-home-preview-2x.png"
    preview.save(preview_path, optimize=True)

    outputs = [*palette_files, guide_path, preview_path]
    manifest = {
        "schemaVersion": 1,
        "id": "exclusive-first-home-v1",
        "runtimeReady": False,
        "source": {
            "file": SOURCE.name,
            "size": list(source.size),
            "mode": "RGB",
            "sha256": sha256(SOURCE),
        },
        "logicalSize": list(SIZE),
        "scene": "first apartment / moving day",
        "actorSafeZone": [87, 130, 235, 213],
        "dialogueSafeZone": [0, 222, 319, 255],
        "limitations": [
            "Flattened backdrop concept; no composable depth layers.",
            "Staging guide is not a collision or portal map.",
            "Pixel-like generated texture needs human cleanup against actor clusters.",
        ],
        "outputs": [
            {"file": path.name, "size": list(Image.open(path).size), "mode": Image.open(path).mode, "sha256": sha256(path), "runtimeReady": False}
            for path in outputs
        ],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    provenance_path = ROOT / "provenance.json"
    provenance = json.loads(provenance_path.read_text())
    provenance["sourceSha256"] = sha256(SOURCE)
    provenance["outputs"] = [{"file": path.name, "sha256": sha256(path)} for path in outputs]
    provenance_path.write_text(json.dumps(provenance, indent=2) + "\n")


if __name__ == "__main__":
    main()
