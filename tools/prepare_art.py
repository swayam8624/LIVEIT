#!/usr/bin/env python3
"""Prepare original, licensed LIVEIT scene and portrait artwork for mobile and web.

Requires Pillow: python -m pip install Pillow
Usage:
  python tools/prepare_art.py --cafe /path/cafe.png --amelia /path/amelia.png

This deliberately does not synthesize poses, claim rights, or turn flattened
images into animation rigs. It creates repeatable, optimized first-stage assets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageOps

OUT = Path(__file__).resolve().parents[1] / "apps" / "player" / "assets"


def sha256(path: Path) -> str:
    """Return a provenance checksum for the exact source file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(src: Path, target: Path, max_width: int, quality: int) -> dict:
    """Crop without distortion, flatten transparent art, then optimize JPEG."""
    if not src.is_file():
        raise FileNotFoundError(f"Asset source not found: {src}")
    with Image.open(src) as opened:
        # Respect EXIF rotation, and refuse unexpectedly tiny art.
        image = ImageOps.exif_transpose(opened).convert("RGBA")
        width, height = image.size
        if width < 320 or height < 200:
            raise ValueError(f"Source too small for a production scene: {src} ({width}×{height})")
        new_width = min(max_width, width)
        new_height = round(height * new_width / width)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        base = Image.new("RGB", image.size, "#111827")
        base.paste(image, mask=image.getchannel("A"))
        target.parent.mkdir(parents=True, exist_ok=True)
        base.save(target, "JPEG", optimize=True, progressive=True, quality=quality)
    return {
        "source": str(src.resolve()),
        "source_sha256": sha256(src),
        "source_dimensions": [width, height],
        "output": str(target.relative_to(OUT.parents[2])),
        "output_sha256": sha256(target),
        "output_dimensions": [new_width, new_height],
        "bytes": target.stat().st_size,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare LIVEIT game artwork")
    parser.add_argument("--cafe", type=Path, required=True, help="Original cafe concept image")
    parser.add_argument("--amelia", type=Path, required=True, help="Original portrait image")
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--confirm-rights", action="store_true",
                        help="Confirm you have permission to include both images")
    args = parser.parse_args()
    if not args.confirm_rights:
        parser.error("Add --confirm-rights after checking the image sources and usage permissions.")
    dest = args.output
    results = [
        prepare(args.cafe, dest / "cafe-dusk.jpg", max_width=1600, quality=84),
        prepare(args.amelia, dest / "amelia-portrait.jpg", max_width=800, quality=85),
    ]
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "generator": "tools/prepare_art.py",
        "rights_review": "Manually acknowledged by the operator; retain independent evidence.",
        "assets": results,
    }
    (dest / "art-provenance.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    for item in results:
        print(f"Prepared {item['output']}: {item['bytes']:,} bytes")
    print(f"Provenance manifest: {dest / 'art-provenance.json'}")


if __name__ == "__main__":
    main()
