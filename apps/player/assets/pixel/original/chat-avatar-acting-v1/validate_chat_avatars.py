#!/usr/bin/env python3
"""Validate the generated chat-avatar acting batch and recorded hashes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
EXPECTED_CHARACTERS = {"mara", "eli", "niko", "aunt-sol"}
EXPECTED_STATES = {"listening", "curious", "concerned", "reassuring", "speaking", "blink"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text())
    assert manifest["runtimeReady"] is False
    assert manifest["frameCount"] == 24
    assert set(manifest["states"]) == EXPECTED_STATES
    assert {item["id"] for item in manifest["characters"]} == EXPECTED_CHARACTERS
    assert len(manifest["frames"]) == 24

    seen: set[tuple[str, str]] = set()
    for item in manifest["frames"]:
        key = (item["characterId"], item["state"])
        assert key not in seen, f"duplicate frame mapping: {key}"
        seen.add(key)
        assert item["characterId"] in EXPECTED_CHARACTERS
        assert item["state"] in EXPECTED_STATES
        assert item["ageSafety"] == "all-ages-safe"
        assert item["runtimeReady"] is False
        path = ROOT / item["file"]
        assert sha256(path) == item["sha256"], f"hash mismatch: {path}"
        with Image.open(path) as image:
            assert image.size == (48, 48) and image.mode == "RGBA", f"bad frame: {path}"
            x, y = item["x"], item["y"]
            with Image.open(ROOT / manifest["atlas"]["file"]) as atlas:
                assert atlas.crop((x, y, x + 48, y + 48)).tobytes() == image.tobytes(), f"atlas mismatch: {key}"
    assert len(seen) == len(EXPECTED_CHARACTERS) * len(EXPECTED_STATES)

    for record in (manifest["atlas"], manifest["preview"]):
        path = ROOT / record["file"]
        assert sha256(path) == record["sha256"], f"hash mismatch: {path}"
    with Image.open(ROOT / manifest["atlas"]["file"]) as atlas:
        assert atlas.size == (288, 192) and atlas.mode == "RGBA"
    with Image.open(ROOT / manifest["preview"]["file"]) as preview:
        assert preview.size == (864, 640) and preview.mode == "RGB"

    provenance = json.loads((ROOT / manifest["provenanceFile"]).read_text())
    for record in provenance["sourceFiles"] + provenance["identityPaletteReferences"]:
        assert sha256((ROOT / record["file"]).resolve()) == record["sha256"], f"hash mismatch: {record['file']}"
    print("chat-avatar-acting-v1: 24 frames, 4 identities × 6 states, atlas/preview/provenance hashes valid; runtimeReady=false")


if __name__ == "__main__":
    main()
