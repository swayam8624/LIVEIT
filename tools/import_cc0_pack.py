#!/usr/bin/env python3
"""Safely stage a manually downloaded, individually verified CC0 asset pack.

Usage:
 python3 tools/import_cc0_pack.py kenney-ui ~/Downloads/Kenney_UI.zip --confirm-license

This imports inspected archives into staging, not bundled runtime assets.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets" / "open_source_sources.json"
DEFAULT_OUT = ROOT / "assets" / "third_party"
SAFE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".ogg", ".wav", ".ttf", ".otf", ".txt", ".md", ".json"}
MAX_FILE = 12 * 1024 * 1024
MAX_TOTAL = 85 * 1024 * 1024
MAX_COUNT = 3000

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser(description="Stage a properly licensed game asset pack")
    parser.add_argument("source_id", help="Identifier from assets/open_source_sources.json")
    parser.add_argument("zip_path", type=Path, help="Manually downloaded original ZIP")
    parser.add_argument("--confirm-license", action="store_true",
                        help="Confirm the archive itself includes suitable rights")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    catalog = json.loads(REGISTRY.read_text(encoding="utf-8"))
    sources = {item["id"]: item for item in catalog["entries"]}
    if args.source_id not in sources:
        parser.error(f"Unrecognized source: {args.source_id}")
    if not args.confirm_license:
        parser.error("Inspect the downloaded archive's individual license then pass --confirm-license")
    if not args.zip_path.is_file():
        parser.error(f"Archive not found: {args.zip_path}")
    out = args.output / args.source_id
    if out.exists():
        parser.error(f"Destination already exists; refusing silent overwrite: {out}")
    accepted = []
    total = 0
    with zipfile.ZipFile(args.zip_path) as archive:
        entries = [f for f in archive.infolist() if not f.is_dir()]
        if len(entries) > MAX_COUNT:
            parser.error(f"Archive too large: {len(entries)} entries")
        for info in entries:
            item = PurePosixPath(info.filename.replace("\\", "/"))
            if item.is_absolute() or ".." in item.parts or ":" in item.parts[0]:
                parser.error(f"Unsafe filename: {info.filename}")
            if item.suffix.lower() not in SAFE_EXT:
                continue
            if info.file_size > MAX_FILE or total + info.file_size > MAX_TOTAL:
                parser.error(f"Pack exceeds asset limits at {info.filename}")
            total += info.file_size
            accepted.append((info, item))
        if not accepted:
            parser.error("No suitable safe image/audio/font files found")
        out.mkdir(parents=True)
        records = []
        for info, item in accepted:
            payload = archive.read(info)
            target = out.joinpath(*item.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            records.append({"path": str(item), "bytes": len(payload), "sha256": sha(payload)})
    manifest = {
        "source": sources[args.source_id],
        "archive_name": args.zip_path.name,
        "archive_sha256": sha(args.zip_path.read_bytes()),
        "license_review": "Manually confirmed by the operator",
        "files": records,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Staged {len(records)} files ({total:,} bytes) at {out}")
    print("Review quality, licensing and art direction before using files in game.")

if __name__ == "__main__":
    main()
