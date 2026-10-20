#!/usr/bin/env python3
"""Check generated control PNGs against their manifest and provenance hashes."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
manifest = json.loads((ROOT / "manifest.json").read_text())
provenance = json.loads((ROOT / "provenance.json").read_text())
recorded = {item["file"]: item for item in provenance["files"]}
errors = []
for frame in manifest["frames"]:
    path = ROOT / frame["file"]
    if not path.is_file():
        errors.append(f"missing: {frame['file']}")
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with Image.open(path) as image:
        if image.size != (frame["width"], frame["height"]):
            errors.append(f"dimensions: {frame['file']} has {image.size}")
        if image.mode != frame["mode"]:
            errors.append(f"mode: {frame['file']} has {image.mode}")
    if digest != frame["sha256"]:
        errors.append(f"manifest hash mismatch: {frame['file']}")
    if frame["file"] not in recorded or digest != recorded[frame["file"]]["sha256"]:
        errors.append(f"provenance hash mismatch: {frame['file']}")

for rel, record in recorded.items():
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"provenance file missing: {rel}")
        continue
    with Image.open(path) as image:
        if image.size != (record["width"], record["height"]):
            errors.append(f"provenance dimensions: {rel} has {image.size}")
        if image.mode != record["mode"]:
            errors.append(f"provenance mode: {rel} has {image.mode}")
    if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
        errors.append(f"provenance hash mismatch: {rel}")

preview = ROOT / "accessible-controls-preview-3x.png"

if errors:
    raise SystemExit("Validation failed:\n" + "\n".join(errors))
print(f"Validated {len(manifest['frames'])} control PNGs: dimensions, RGBA mode, manifest hashes, provenance hashes OK.")
with Image.open(preview) as image:
    print(f"Validated preview: {image.size[0]}x{image.size[1]} {image.mode}.")
