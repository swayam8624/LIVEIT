#!/usr/bin/env python3
"""Validate player/Amelia compact chat-avatar coverage and recorded hashes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
EXPECTED_STAGES = (
    "player-infant", "player-toddler", "player-child", "player-teen",
    "player-young-adult", "player-midlife", "player-elder", "amelia",
)
EXPECTED_STATES = {"listening", "curious", "concerned", "reassuring", "speaking", "blink"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text())
    assert manifest["runtimeReady"] is False
    assert manifest["frameCount"] == 48 and len(manifest["frames"]) == 48
    assert tuple(person["id"] for person in manifest["characters"]) == EXPECTED_STAGES
    assert set(manifest["states"]) == EXPECTED_STATES

    seen: set[tuple[str, str]] = set()
    hashes: set[str] = set()
    with Image.open(ROOT / manifest["atlas"]["file"]) as atlas:
        assert atlas.size == (288, 384) and atlas.mode == "RGBA"
        for item in manifest["frames"]:
            key = (item["characterId"], item["state"])
            assert key not in seen, f"duplicate mapping: {key}"
            seen.add(key)
            assert item["ageSafety"] == "all-ages-safe"
            assert item["runtimeReady"] is False
            path = ROOT / item["file"]
            actual = sha256(path)
            assert actual == item["sha256"], f"hash mismatch: {path}"
            assert actual not in hashes, f"duplicate sprite bytes: {key}"
            hashes.add(actual)
            with Image.open(path) as frame:
                assert frame.size == (48, 48) and frame.mode == "RGBA", f"bad frame: {path}"
                x, y = item["x"], item["y"]
                assert atlas.crop((x, y, x + 48, y + 48)).tobytes() == frame.tobytes(), f"atlas mismatch: {key}"
    assert len(seen) == 48 and len(hashes) == 48
    assert {(r["characterId"], r["state"]) for r in manifest["frames"] if r["characterId"] in {"player-infant", "player-toddler"} and r["state"] == "speaking"} == {
        ("player-infant", "speaking"), ("player-toddler", "speaking")
    }

    for record in (manifest["atlas"], manifest["preview"]):
        path = ROOT / record["file"]
        assert sha256(path) == record["sha256"], f"hash mismatch: {path}"
    with Image.open(ROOT / manifest["preview"]["file"]) as preview:
        assert preview.size == (980, 1334) and preview.mode == "RGB"

    provenance = json.loads((ROOT / manifest["provenanceFile"]).read_text())
    for record in provenance["sourceFiles"] + provenance["identityPaletteReferences"]:
        assert sha256((ROOT / record["file"]).resolve()) == record["sha256"], f"reference/source hash mismatch: {record['file']}"
    print("chat-avatar-player-amelia-v1: 48 unique frames, 8 identities/stages × 6 states, atlas/preview/provenance hashes valid; runtimeReady=false")


if __name__ == "__main__":
    main()
