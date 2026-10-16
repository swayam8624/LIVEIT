#!/usr/bin/env python3
"""Install the original LIVEIT art pack into the Expo player's bundled assets.

Usage:
  python3 -m pip install Pillow
  python3 tools/install_concept_art.py ~/Downloads/LIVEIT_Original_Concept_Art_Pack_v1.zip --confirm-rights

The source ZIP stays untouched. Only recognized image filenames are read.
The resulting JPEGs remain offline assets; the UI never depends on a live AI API.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "apps" / "player" / "assets"
SOURCE_IMAGES = {
    "bellweather_cafe_concept_1672x941.png": ("cafe-dusk.jpg", 1600, 84),
    "amelia_character_portrait_326x380.png": ("amelia-portrait.jpg", 652, 85),
}
MAX_SOURCE_BYTES = 10 * 1024 * 1024


def digest(data: bytes) -> str:
    """Hash the exact source image bytes for attribution and reproducibility."""
    return hashlib.sha256(data).hexdigest()


def convert(image_data: bytes, out: Path, max_width: int, quality: int) -> dict:
    """Respect EXIF orientation, flatten transparency, and resize without warping."""
    with Image.open(io.BytesIO(image_data)) as loaded:
        image = ImageOps.exif_transpose(loaded).convert("RGBA")
        original_size = list(image.size)
        if image.width < 320 or image.height < 200:
            raise ValueError(f"Artwork is too small: {original_size}")
        if image.width > max_width:
            new_height = round(image.height * max_width / image.width)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        background = Image.new("RGB", image.size, (16, 23, 35))
        background.paste(image, mask=image.getchannel("A"))
        out.parent.mkdir(parents=True, exist_ok=True)
        background.save(out, "JPEG", optimize=True, progressive=True, quality=quality)
        return {
            "original_dimensions": original_size,
            "export_dimensions": list(background.size),
            "export_sha256": digest(out.read_bytes()),
            "export_bytes": out.stat().st_size,
        }


def main() -> None:
    p = argparse.ArgumentParser(description="Install LIVEIT offline original concept artwork")
    p.add_argument("pack", type=Path, help="Original ChatGPT concept-art ZIP")
    p.add_argument("--confirm-rights", action="store_true",
                   help="Explicitly confirm the planned commercial usage is permitted")
    p.add_argument("--output", type=Path, default=OUTPUT_DIR)
    args = p.parse_args()
    if not args.confirm_rights:
        p.error("Review image terms and pass --confirm-rights to continue.")
    if not args.pack.is_file():
        p.error(f"Cannot find {args.pack}")
    records = []
    try:
        with ZipFile(args.pack) as archive:
            for source, (target, width, quality) in SOURCE_IMAGES.items():
                file_info = archive.getinfo(source)
                if file_info.file_size > MAX_SOURCE_BYTES:
                    raise ValueError(f"Source image too large: {source}")
                raw = archive.read(file_info)
                export = args.output / target
                meta = convert(raw, export, width, quality)
                records.append({
                    "source": source,
                    "source_sha256": digest(raw),
                    "export": str(export),
                    **meta,
                })
                print(f"Installed: {export} ({meta['export_bytes']:,} bytes)")
    except (KeyError, BadZipFile) as exc:
        p.error(f"Invalid LIVEIT art ZIP: {exc}")
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "pack_sha256": digest(args.pack.read_bytes()),
        "license_review": "Operator confirmed; keep independent documentation of rights.",
        "assets": records,
    }
    manifest_path = args.output / "art-provenance.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest: {manifest_path}")
    print("Run npm run check and npm run build:player, then visually review the assets.")


if __name__ == "__main__":
    main()
