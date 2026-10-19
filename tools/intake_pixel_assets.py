#!/usr/bin/env python3
"""LIVEIT pixel-only import: inspect ZIP/audio/image downloads, review rights, stage safe playable media.

Uses Python 3 standard library. Raw ZIP archives remain at their original locations.
Never marks asset-catalog items complete, never claims licenses were independently verified.
Commands:
  python3 tools/intake_pixel_assets.py --source "$HOME/Downloads" --scan
  python3 tools/intake_pixel_assets.py --review
  python3 tools/intake_pixel_assets.py --import-approved
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import stat
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "assets" / "local-intake"
REVIEWS = PRIVATE / "reviews.json"
PUBLIC = ROOT / "assets" / "imported"
MEDIA_EXT = {".png", ".ase", ".aseprite", ".tmx", ".tsx", ".json", ".wav", ".ogg", ".mp3", ".m4a", ".flac", ".ttf", ".otf"}
AUDIO_EXT = {".wav", ".ogg", ".mp3", ".m4a", ".flac"}
ART_EXT = {".png", ".ase", ".aseprite", ".tmx", ".tsx", ".json"}
FONT_EXT = {".ttf", ".otf"}
SCAN_EXT = MEDIA_EXT | {".zip"}
LICENSES = {"CC0-1.0", "CC-BY-4.0", "CC-BY-3.0", "MIT", "OFL-1.1"}
MAX_FILES = 4500
MAX_FILE = 45 * 1024 * 1024
MAX_ARCHIVE_TOTAL = 500 * 1024 * 1024
MAX_SOURCE_ARCHIVE = 2 * 1024 * 1024 * 1024
MAX_RATIO = 500
IGNORED_DIRS = {"node_modules", ".git", ".next", "dist", "build", ".venv", "venv", "__MACOSX"}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def save(obj: dict) -> None:
    PRIVATE.mkdir(parents=True, exist_ok=True)
    tmp = REVIEWS.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(REVIEWS)

def load() -> dict:
    if not REVIEWS.is_file():
        raise SystemExit("Run --scan first. No reviews.json available.")
    return json.loads(REVIEWS.read_text(encoding="utf-8"))

def safe_path(raw: str) -> Path | None:
    if "\x00" in raw or "\\" in raw or raw.startswith("/") or re.match(r"^[a-zA-Z]:", raw):
        return None
    parts = PurePosixPath(raw).parts
    if not parts or any(part in ("", ".", "..") for part in parts):
        return None
    if len(parts) > 20 or len(raw) > 350:
        return None
    return Path(*parts)

def media_group(ext: str) -> str:
    if ext in AUDIO_EXT:
        return "audio"
    if ext in FONT_EXT:
        return "fonts"
    return "pixel"

def scan_archive(path: Path) -> dict:
    kinds = {"pixel": 0, "audio": 0, "fonts": 0, "unsupported": 0}
    issues = []
    try:
        with zipfile.ZipFile(path) as zf:
            members = zf.infolist()
            if len(members) > MAX_FILES:
                issues.append("too many files")
            total = sum(m.file_size for m in members if not m.is_dir())
            if total > MAX_ARCHIVE_TOTAL:
                issues.append("archive uncompressed size exceeds 500 MiB")
            for member in members:
                if member.is_dir():
                    continue
                p = safe_path(member.filename)
                unix_mode = member.external_attr >> 16
                if p is None or stat.S_ISLNK(unix_mode) or member.flag_bits & 1:
                    issues.append("unsafe path/symlink/encrypted member")
                    continue
                if member.file_size > MAX_FILE:
                    issues.append("oversized extracted file")
                    continue
                if member.file_size > 1024 * 1024 and member.compress_size > 0 and member.file_size / member.compress_size > MAX_RATIO:
                    issues.append("suspicious compression ratio")
                    continue
                ext = p.suffix.lower()
                if ext in MEDIA_EXT:
                    kinds[media_group(ext)] += 1
                else:
                    kinds["unsupported"] += 1
    except (zipfile.BadZipFile, OSError, RuntimeError, ValueError) as exc:
        issues.append("not a readable ZIP: " + str(exc)[:120])
    return {"counts": kinds, "issues": sorted(set(issues))}

def scan(source: Path) -> None:
    source = source.expanduser().resolve()
    if not source.is_dir():
        raise SystemExit("Source folder missing: " + str(source))
    existing = {}
    if REVIEWS.is_file():
        for record in load().get("files", []):
            existing[record["sha256"]] = record
    candidates = []
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.is_symlink() or any(n in IGNORED_DIRS for n in path.relative_to(source).parts):
            continue
        if path.suffix.lower() not in SCAN_EXT:
            continue
        size = path.stat().st_size
        if size > MAX_SOURCE_ARCHIVE:
            print("SKIP over-2GiB source:", path)
            continue
        digest = sha256(path)
        previous = existing.get(digest, {})
        details = scan_archive(path) if path.suffix.lower() == ".zip" else {
            "counts": {media_group(path.suffix.lower()): 1}, "issues": []}
        candidates.append({
            "path": str(path), "name": path.name, "sha256": digest,
            "bytes": size, "kind": path.suffix.lower().lstrip("."),
            "contents": details["counts"], "issues": details["issues"],
            "approved": previous.get("approved", False),
            "redistribute_public": previous.get("redistribute_public", False),
            "license_id": previous.get("license_id", "UNVERIFIED"),
            "license_evidence_url": previous.get("license_evidence_url", ""),
            "source_url": previous.get("source_url", ""),
            "creator": previous.get("creator", ""),
            "notes": previous.get("notes", ""),
        })
    save({"schemaVersion": 1, "scannedFrom": str(source), "scannedAt": datetime.now(timezone.utc).isoformat(),
          "important": "No detected file is automatically legal for a public repo. Review before import.",
          "files": candidates})
    print("Found", len(candidates), "ZIP/audio/art files.")
    for record in candidates:
        flags = " BLOCKED:" + ",".join(record["issues"]) if record["issues"] else ""
        print(("APPROVED" if record["approved"] else "REVIEW"), record["name"],
              "%.1fMB" % (record["bytes"]/1024/1024), record["contents"], flags)
    print("Review file:", REVIEWS)
    print("Next: python3 tools/intake_pixel_assets.py --review")

def review() -> None:
    report = load()
    items = report["files"]
    print("Only approve a pack for PUBLIC GitHub if you personally checked its exact license.")
    print("Acceptable IDs:", ", ".join(sorted(LICENSES)))
    print("Never approve Mixamo/Quaternius/Sonniss/CraftPix raw files without verified permissions.")
    for i, entry in enumerate(items, 1):
        if entry["approved"]:
            print("[%d/%d] Already approved: %s" % (i, len(items), entry["name"]))
            continue
        if entry["issues"]:
            print("[%d/%d] Unsafe/oversize, skip: %s %s" % (i, len(items), entry["name"], entry["issues"]))
            continue
        print("\n[%d/%d] %s — %s" % (i, len(items), entry["name"], entry["contents"]))
        action = input("Rights allow raw/public repo redistribution? (y/N/q): ").strip().lower()
        if action == "q":
            break
        if action != "y":
            continue
        license_id = input("Exact license (CC0-1.0 / CC-BY-4.0 / MIT / OFL-1.1 etc): ").strip()
        if license_id not in LICENSES:
            print("Unsupported/unverified license; remain unapproved.")
            continue
        creator = input("Actual publisher/creator: ").strip()
        origin = input("Original product/asset URL (https://...): ").strip()
        evidence = input("Official exact-license evidence URL (https://...): ").strip()
        if not creator or not origin.startswith("https://") or not evidence.startswith("https://"):
            print("Source creator or provenance URL missing; remain unapproved.")
            continue
        entry.update({"approved": True, "redistribute_public": True, "license_id": license_id,
                      "creator": creator, "source_url": origin, "license_evidence_url": evidence})
        save(report)
    save(report)
    print("Rights review saved to", REVIEWS)

def extract_one(input_stream, target: Path, max_size: int) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with target.open("wb") as f:
        while True:
            data = input_stream.read(min(1024 * 1024, max_size + 1 - written))
            if not data:
                break
            written += len(data)
            if written > max_size:
                raise ValueError("extracted file exceeded maximum")
            f.write(data)

def derive_audio(source: Path, target: Path) -> Path:
    if source.suffix.lower() in {".m4a", ".mp3"}:
        return source
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        out = target.with_suffix(".m4a")
        run = subprocess.run([ffmpeg, "-hide_banner", "-nostdin", "-loglevel", "error", "-y", "-i", str(source),
            "-vn", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2", str(out)],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=75)
        if run.returncode == 0 and out.is_file() and out.stat().st_size > 0:
            source.unlink()
            return out
        print("WARNING conversion failed, retained original audio:", source.name)
    else:
        print("WARNING ffmpeg unavailable; kept original audio:", source.name,
              "(OGG/FLAC may require game playback decoder on iOS)")
    return source

def import_approved() -> None:
    report = load()
    total = 0
    output_list = []
    for record in report["files"]:
        if not record["approved"] or not record["redistribute_public"]:
            continue
        if record["issues"]:
            print("SKIP unsafe source:", record["name"], record["issues"])
            continue
        if record["license_id"] not in LICENSES or not record["creator"] or not record["source_url"].startswith("https://") or not record["license_evidence_url"].startswith("https://"):
            print("SKIP missing verified rights declaration:", record["name"])
            continue
        original = Path(record["path"])
        if not original.is_file() or original.is_symlink() or sha256(original) != record["sha256"]:
            print("SKIP source changed or missing:", record["name"])
            continue
        slug = re.sub(r"[^a-z0-9-]+", "-", original.stem.lower()).strip("-")[:65] or "pack"
        dest = PUBLIC / (slug + "-" + record["sha256"][:12])
        if dest.exists():
            print("ALREADY EXISTS (no overwrite):", dest)
            continue
        temp = PUBLIC / ("." + slug + "-" + record["sha256"][:12] + "-tmp")
        if temp.exists():
            raise SystemExit("Unexpected previous staging directory: " + str(temp))
        temp.mkdir(parents=True)
        imported = []
        try:
            if record["kind"] == "zip":
                with zipfile.ZipFile(original) as zf:
                    members = zf.infolist()
                    if len(members) > MAX_FILES or sum(m.file_size for m in members if not m.is_dir()) > MAX_ARCHIVE_TOTAL:
                        raise ValueError("unsafe archive dimensions")
                    seen = set()
                    for member in members:
                        if member.is_dir():
                            continue
                        rel = safe_path(member.filename)
                        if rel is None:
                            raise ValueError("zip-slip member")
                        unix_mode = member.external_attr >> 16
                        if stat.S_ISLNK(unix_mode) or member.flag_bits & 1:
                            raise ValueError("symlink/encrypted member")
                        lower = rel.as_posix().lower()
                        ext = rel.suffix.lower()
                        is_license = rel.name.lower().startswith(("license", "licence", "copying", "attribution", "credits")) and ext in {".md", ".txt"}
                        if ext not in MEDIA_EXT and not is_license:
                            continue
                        if member.file_size > MAX_FILE or (member.file_size > 1024 * 1024 and member.compress_size and member.file_size / member.compress_size > MAX_RATIO):
                            raise ValueError("oversized/zip-bomb member")
                        # Sanitize macOS case-insensitive path collisions.
                        target_rel = Path("licenses" if is_license else media_group(ext)) / rel
                        key = target_rel.as_posix().lower()
                        if key in seen:
                            print("SKIP duplicate case-insensitive path:", member.filename)
                            continue
                        seen.add(key)
                        target = temp / target_rel
                        with zf.open(member) as incoming:
                            extract_one(incoming, target, MAX_FILE)
                        if not is_license and ext in AUDIO_EXT:
                            target = derive_audio(target, target)
                        imported.append({"path": str(target.relative_to(temp)), "bytes": target.stat().st_size,
                                         "sha256": sha256(target), "source_member": member.filename})
            else:
                ext = original.suffix.lower()
                target = temp / media_group(ext) / original.name
                with original.open("rb") as incoming:
                    extract_one(incoming, target, MAX_FILE)
                if ext in AUDIO_EXT:
                    target = derive_audio(target, target)
                imported.append({"path": str(target.relative_to(temp)), "bytes": target.stat().st_size,
                                 "sha256": sha256(target), "source_member": original.name})
            if not imported:
                print("SKIP no compatible pixel/audio files:", record["name"])
                shutil.rmtree(temp)
                continue
            source_receipt = {
                "source_file": record["name"], "source_archive_sha256": record["sha256"],
                "source_url": record["source_url"], "creator": record["creator"],
                "license_id": record["license_id"], "license_evidence_url": record["license_evidence_url"],
                "rights_reviewed_by": "user-supplied declaration, independently verify for shipping",
                "public_repo_redistribution_approved": True,
                "imported_at": datetime.now(timezone.utc).isoformat(),
                "imported_files": imported,
                "important": "Imported sources are not automatically complete/QA-passed LIVEIT production assets.",
            }
            (temp / "SOURCE.json").write_text(json.dumps(source_receipt, indent=2) + "\n", encoding="utf-8")
            temp.rename(dest)
            print("IMPORTED", record["name"], "→", str(dest.relative_to(ROOT)), len(imported), "files")
            total += len(imported)
            output_list.append(str(dest.relative_to(ROOT)))
        except (OSError, ValueError, zipfile.BadZipFile, subprocess.TimeoutExpired) as exc:
            if temp.exists():
                shutil.rmtree(temp)
            print("FAILED", record["name"], ":", str(exc))
    print("\nImported", total, "approved media files from", len(output_list), "sources.")
    print("Review: git status --short assets/imported && du -sh assets/imported")
    print("Only then stage: git add assets/imported")
    print("Do not stage assets/local-intake/ or original unreviewed ZIP archives.")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(Path.home() / "Downloads"))
    flags = parser.add_mutually_exclusive_group(required=True)
    flags.add_argument("--scan", action="store_true")
    flags.add_argument("--review", action="store_true")
    flags.add_argument("--import-approved", action="store_true")
    opt = parser.parse_args()
    if opt.scan:
        scan(Path(opt.source))
    elif opt.review:
        review()
    else:
        import_approved()

if __name__ == "__main__":
    main()
