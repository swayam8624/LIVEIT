#!/usr/bin/env python3
"""Validate named-family v2 frame coverage, hashes, PNGs and phase uniqueness."""
import hashlib
import json
import struct
import zlib
from pathlib import Path
ROOT = Path(__file__).resolve().parent
DIRECTIONS = {"south", "west", "east", "north"}
PHASES = {"contact-a", "passing-a", "contact-b", "passing-b", "idle", "interact"}
EXPECTED = {"nora": ["adult", "midlife", "elder"], "tavi": ["toddler", "child", "teen", "young-adult"]}

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def inspect_png(path):
    data=path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"): raise ValueError(f"bad PNG signature: {path}")
    width,height,depth,color=struct.unpack(">2I2B",data[16:26])
    if (width,height,depth,color)!=(24,32,8,6): raise ValueError(f"expected 24x32 RGBA: {path}")
    pos,parts=8,[]
    while pos<len(data):
        n=struct.unpack(">I",data[pos:pos+4])[0]; kind=data[pos+4:pos+8]; payload=data[pos+8:pos+8+n]
        crc=struct.unpack(">I",data[pos+8+n:pos+12+n])[0]
        if zlib.crc32(kind+payload)&0xffffffff!=crc: raise ValueError(f"bad chunk CRC: {path}")
        if kind==b"IDAT": parts.append(payload)
        pos+=n+12
        if kind==b"IEND": break
    raw=zlib.decompress(b"".join(parts))
    if len(raw)!=32*(1+24*4): raise ValueError(f"bad RGBA payload: {path}")
    if any(raw[y*97]!=0 for y in range(32)): raise ValueError(f"unsupported row filter: {path}")
    alpha=[raw[y*97+1+x*4+3] for y in range(32) for x in range(24)]
    if not any(alpha) or all(alpha): raise ValueError(f"empty or opaque canvas: {path}")

def main():
    m=json.loads((ROOT/"manifest.json").read_text())
    assert m["runtimeReady"] is False
    assert m["batch"]=="named-family-age-cycles-v2"
    assert m["ageTransitions"]==EXPECTED
    assert m["frameSize"]=={"width":24,"height":32} and m["pivot"]=={"x":12,"y":31}
    assert len(m["frames"])==len(sum(EXPECTED.values(),[]))*24
    refs=set(); all_hashes=set(); groups={}
    for f in m["frames"]:
        assert f["runtimeReady"] is False and f["pivot"]=={"x":12,"y":31}
        path=ROOT/f["file"]
        assert f["file"] not in refs and path.is_file(); refs.add(f["file"])
        inspect_png(path)
        actual=digest(path)
        assert actual==f["sha256"],f"digest mismatch: {path}"
        assert actual not in all_hashes,f"duplicate image bytes across batch: {path}"
        all_hashes.add(actual)
        groups.setdefault((f["character"],f["ageStage"]),[]).append(f)
    expected_groups={(ident,age) for ident,ages in EXPECTED.items() for age in ages}
    assert set(groups)==expected_groups
    for key,frames in groups.items():
        assert len(frames)==24,f"wrong frame count: {key}"
        cells={(f["direction"],f["phase"]) for f in frames}
        assert cells=={(d,p) for d in DIRECTIONS for p in PHASES},f"missing direction/phase: {key}"
        # Reject identical frames across different phases within a direction cycle.
        for direction in DIRECTIONS:
            same_direction=[f for f in frames if f["direction"]==direction]
            phase_hashes={f["phase"]:f["sha256"] for f in same_direction}
            assert len(phase_hashes)==6,f"duplicate or missing phase: {key}/{direction}"
            assert len(set(phase_hashes.values()))==6,f"duplicate phase image bytes within cycle: {key}/{direction}"
        # Also require all 24 authored cells in an age cycle to be distinct.
        assert len({f["sha256"] for f in frames})==24,f"duplicate frame within cycle: {key}"
    prior=ROOT.parent/"named-family-age-cycles-v1"/"frames"
    prior_hashes={digest(path) for path in prior.rglob("*.png")}
    assert not all_hashes.intersection(prior_hashes), "frame bytes duplicate prior Mara/Eli/Niko pack"
    for output in m["outputs"].values():
        path=ROOT/output["file"]
        assert path.is_file() and digest(path)==output["sha256"]
    lineage=m["sourceLineage"]
    source=ROOT.parent/"named-characters-batch-v2"/"manifest.json"
    assert digest(source)==lineage["sourceFiles"][0]["sha256"]
    print(f"PASS: {len(groups)} named age-stage cycles, {len(refs)} unique 24x32 RGBA frames, 4 directions × 6 unique phases per cycle, stable pivot, verified source lineage and atlas/contact sheet hashes; runtimeReady=false")
if __name__=="__main__": main()
