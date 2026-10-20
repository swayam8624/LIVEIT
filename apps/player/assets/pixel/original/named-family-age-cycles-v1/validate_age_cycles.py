#!/usr/bin/env python3
"""Validate age-cycle frame coverage, PNG structure, unique motion and catalog lineage."""
import hashlib
import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def inspect_png(path):
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"): raise ValueError(f"bad PNG signature: {path}")
    width, height, depth, color = struct.unpack(">2I2B", data[16:26])
    if (width, height, depth, color) != (24, 32, 8, 6): raise ValueError(f"expected 24x32 RGBA: {path}")
    pos, parts = 8, []
    while pos < len(data):
        n = struct.unpack(">I", data[pos:pos+4])[0]
        kind, payload = data[pos+4:pos+8], data[pos+8:pos+8+n]
        crc = struct.unpack(">I", data[pos+8+n:pos+12+n])[0]
        if zlib.crc32(kind + payload) & 0xffffffff != crc: raise ValueError(f"bad chunk CRC: {path}")
        if kind == b"IDAT": parts.append(payload)
        pos += n + 12
        if kind == b"IEND": break
    raw = zlib.decompress(b"".join(parts))
    if len(raw) != 32 * (1 + 24 * 4): raise ValueError(f"bad RGBA pixel payload: {path}")
    if any(raw[y * 97] != 0 for y in range(32)): raise ValueError(f"unsupported PNG row filter: {path}")
    alpha = [raw[y*97+1+x*4+3] for y in range(32) for x in range(24)]
    if not any(alpha) or all(alpha): raise ValueError(f"empty or opaque canvas: {path}")

def main():
    m = json.loads((ROOT / "manifest.json").read_text())
    assert m["runtimeReady"] is False
    assert m["frameSize"] == {"width":24,"height":32} and m["pivot"] == {"x":12,"y":31}
    assert len(m["frames"]) == 9 * 24
    expected = {"mara":["adult","midlife","elder"],"eli":["adult","midlife","elder"],"niko":["child","teen","young-adult"]}
    assert m["ageTransitions"] == expected
    refs, hashes = set(), set()
    for f in m["frames"]:
        assert f["runtimeReady"] is False and f["pivot"] == {"x":12,"y":31}
        p = ROOT / f["file"]
        assert f["file"] not in refs and p.is_file(); refs.add(f["file"])
        inspect_png(p)
        h = digest(p)
        assert h == f["sha256"] and h not in hashes, f"missing uniqueness or digest mismatch: {p}"
        hashes.add(h)
    groups = {}
    for f in m["frames"]: groups.setdefault((f["character"],f["ageStage"]),[]).append(f)
    for group, frames in groups.items():
        assert len(frames) == 24 and len({f["direction"] for f in frames}) == 4 and len({f["phase"] for f in frames}) == 6
    for output in m["outputs"].values():
        p = ROOT / output["file"]
        assert p.is_file() and digest(p) == output["sha256"]
    print(f"PASS: {len(groups)} identity-stage cycles, {len(refs)} unique valid 24x32 RGBA frames, 4 facings × 6 phases, stable pivots, verified atlas/contact sheet hashes; runtimeReady=false")

if __name__ == "__main__": main()
