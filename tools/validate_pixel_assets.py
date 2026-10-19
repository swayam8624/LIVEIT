#!/usr/bin/env python3
"""Validate only legitimately imported pixel-world / dialogue / UI / audio resources."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORTED = ROOT / "assets" / "imported"
ALLOWED = {".png", ".ase", ".aseprite", ".tmx", ".tsx", ".json", ".wav", ".ogg", ".mp3", ".m4a", ".flac", ".ttf", ".otf", ".txt", ".md"}
RIGHTS = {"CC0-1.0", "CC-BY-4.0", "CC-BY-3.0", "MIT", "OFL-1.1"}

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = {"packs": 0, "files": 0, "audio": 0, "pixelOrUI": 0, "fonts": 0, "bytes": 0, "issues": []}
    if IMPORTED.exists():
        for pack in sorted(IMPORTED.iterdir()):
            if pack.is_symlink() or not pack.is_dir():
                report["issues"].append("Unexpected non-directory/symlink: " + pack.name)
                continue
            manifest = pack / "SOURCE.json"
            if not manifest.is_file():
                report["issues"].append("Missing SOURCE.json: " + pack.name)
                continue
            try:
                receipt = json.loads(manifest.read_text())
            except (ValueError, OSError):
                report["issues"].append("Malformed SOURCE.json: " + pack.name)
                continue
            if receipt.get("license_id") not in RIGHTS or not receipt.get("public_repo_redistribution_approved"):
                report["issues"].append("Missing permitted-license assertion: " + pack.name)
            if not receipt.get("license_evidence_url", "").startswith("https://") or not receipt.get("source_url", "").startswith("https://"):
                report["issues"].append("Missing actual license/source link: " + pack.name)
            if not receipt.get("creator"):
                report["issues"].append("Missing creator: " + pack.name)
            paths = set()
            for item in receipt.get("imported_files", []):
                rel = item.get("path", "")
                source = pack / rel
                if not rel or rel.startswith("/") or ".." in Path(rel).parts or "\\" in rel or rel in paths:
                    report["issues"].append("Untrusted/duplicate recorded path: " + str(rel))
                    continue
                paths.add(rel)
                if source.is_symlink() or not source.is_file() or not source.resolve().is_relative_to(pack.resolve()):
                    report["issues"].append("Missing/unsafe media: " + str(source))
                    continue
                ext = source.suffix.lower()
                if ext not in ALLOWED:
                    report["issues"].append("Unexpected file extension (3D/executable forbidden): " + str(source))
                if source.stat().st_size != item.get("bytes") or sha256(source) != item.get("sha256"):
                    report["issues"].append("File size/digest mismatch: " + str(source))
                report["files"] += 1
                report["bytes"] += source.stat().st_size
                if ext in {".wav", ".ogg", ".mp3", ".m4a", ".flac"}:
                    report["audio"] += 1
                elif ext in {".ttf", ".otf"}:
                    report["fonts"] += 1
                else:
                    report["pixelOrUI"] += 1
            report["packs"] += 1
            if not paths:
                report["issues"].append("Pack has no approved compatible media: " + pack.name)
            for path in pack.rglob("*"):
                if path.is_symlink():
                    report["issues"].append("Symlink in public pack: " + str(path))
                elif path.is_file() and path.name != "SOURCE.json" and path.relative_to(pack).as_posix() not in paths and not path.relative_to(pack).parts[0] == "licenses":
                    report["issues"].append("Untracked file in pack: " + str(path))
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("Pixel-only asset import: %d packs, %d files (%d audio, %d pixel/UI, %d fonts), %d bytes, %d issues" %
              (report["packs"], report["files"], report["audio"], report["pixelOrUI"], report["fonts"], report["bytes"], len(report["issues"])))
        for issue in report["issues"]:
            print("ERROR", issue)
    return 1 if report["issues"] else 0

if __name__ == "__main__":
    sys.exit(main())
