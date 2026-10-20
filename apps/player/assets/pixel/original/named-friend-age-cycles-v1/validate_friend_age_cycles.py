#!/usr/bin/env python3
"""Validate friend age-cycle coverage, PNGs, lineage, and byte uniqueness."""
import hashlib
import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT.parent
DIRECTIONS = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b", "idle", "interact"]
EXPECTED = {"amelia": ["adult", "midlife", "elder"], "noah": ["adult", "midlife", "elder"]}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_png(path, expected=(24, 32)):
    data = path.read_bytes()
    assert data.startswith(b"\x89PNG\r\n\x1a\n"), f"bad PNG signature: {path}"
    width, height, depth, color = struct.unpack(">2I2B", data[16:26])
    assert (width, height, depth, color) == (*expected, 8, 6), f"expected {expected[0]}x{expected[1]} RGBA: {path}"
    position, compressed = 8, []
    while position < len(data):
        size = struct.unpack(">I", data[position:position + 4])[0]
        kind = data[position + 4:position + 8]
        payload = data[position + 8:position + 8 + size]
        crc = struct.unpack(">I", data[position + 8 + size:position + 12 + size])[0]
        assert zlib.crc32(kind + payload) & 0xFFFFFFFF == crc, f"bad PNG chunk CRC: {path}"
        if kind == b"IDAT":
            compressed.append(payload)
        position += size + 12
        if kind == b"IEND":
            break
    raw = zlib.decompress(b"".join(compressed))
    stride = width * 4 + 1
    assert len(raw) == height * stride, f"bad pixel payload: {path}"
    assert all(raw[y * stride] == 0 for y in range(height)), f"unexpected PNG row filter: {path}"
    alpha = [raw[y * stride + 1 + x * 4 + 3] for y in range(height) for x in range(width)]
    assert any(alpha) and not all(alpha), f"empty/opaque canvas: {path}"
    return raw


def existing_hashes(relative_dir, skip=None):
    result = set()
    for path in (ORIGINAL / relative_dir).rglob("*.png"):
        if skip and path.resolve() == skip.resolve():
            continue
        result.add(digest(path))
    return result


def main():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    assert manifest["batch"] == "named-friend-age-cycles-v1"
    assert manifest["runtimeReady"] is False
    assert manifest["ageTransitions"] == EXPECTED
    assert manifest["frameSize"] == {"width": 24, "height": 32}
    assert manifest["pivot"] == {"x": 12, "y": 31}
    assert manifest["directions"] == DIRECTIONS and manifest["phases"] == PHASES
    assert len(manifest["frames"]) == 6 * 24
    provenance_path = ROOT / "provenance.json"
    assert manifest["provenanceSha256"] == digest(provenance_path)
    provenance = json.loads(provenance_path.read_text())
    assert provenance["batch"] == manifest["batch"]
    assert provenance["sourceLineage"] == manifest["identityLineage"]

    base_manifest_path = ORIGINAL / "named-characters-batch-v1" / "manifest.json"
    base_manifest = json.loads(base_manifest_path.read_text())
    blocked = set()
    for base_pack in ORIGINAL.glob("named-characters-batch-v*"):
        if base_pack.is_dir():
            blocked |= existing_hashes(base_pack.relative_to(ORIGINAL))
    for family_pack in ("named-family-age-cycles-v1", "named-family-age-cycles-v2"):
        blocked |= existing_hashes(Path(family_pack))
    seen_files, seen_hashes, groups = set(), set(), {}
    for frame in manifest["frames"]:
        assert frame["runtimeReady"] is False and frame["pivot"] == manifest["pivot"]
        assert frame["width"] == 24 and frame["height"] == 32 and frame["mode"] == "RGBA"
        assert frame["direction"] in DIRECTIONS and frame["phase"] in PHASES
        path = ROOT / frame["file"]
        assert frame["file"] not in seen_files and path.is_file(), f"duplicate/missing file: {path}"
        seen_files.add(frame["file"])
        inspect_png(path)
        value = digest(path)
        assert value == frame["sha256"], f"frame hash mismatch: {path}"
        assert value not in seen_hashes, f"repeated frame bytes in pack: {path}"
        assert value not in blocked, f"frame duplicates source/base/family-age bytes: {path}"
        seen_hashes.add(value)
        groups.setdefault((frame["character"], frame["ageStage"]), []).append(frame)

    for character, ages in EXPECTED.items():
        for age in ages:
            group = groups[(character, age)]
            assert len(group) == 24
            assert {frame["direction"] for frame in group} == set(DIRECTIONS)
            assert {frame["phase"] for frame in group} == set(PHASES)
    assert len(groups) == 6

    lineage = manifest["identityLineage"]
    for character in EXPECTED:
        source_record = next(row for row in base_manifest["characters"] if row["id"] == character)
        record = lineage[character]
        assert record["manifestSha256"] == digest(base_manifest_path)
        assert record["catalogId"] == source_record["catalogId"]
        assert record["identityCues"] == source_record["identityCues"]
        assert record["silhouette"] == source_record["silhouette"]
        assert set(record["sourceFrameHashes"]).issubset(blocked)

    for output in manifest["outputs"].values():
        path = ROOT / output["file"]
        expected = (output["width"], output["height"])
        inspect_png(path, expected)
        assert digest(path) == output["sha256"], f"output hash mismatch: {path}"
    print("PASS: 6 identity-stage cycles, 144 distinct frames, complete 4-direction × 6-phase coverage, stable 24x32 RGBA pivots, source/family hash disjointness, atlas/contact sheet integrity; runtimeReady=false")


if __name__ == "__main__":
    main()
