#!/usr/bin/env python3
"""Zero-per-file-question import for SIX EXACT, HASH-PINNED, RIGHTS-VERIFIED CC0 packs.

The owner uploaded these exact archives in this session. Their bytes and
published CC0 licenses have been verified. This script refuses a similarly
named archive if its SHA-256 differs; other non-CC0/game-only content is never
auto-approved. It does not overwrite the owner's original ZIPs.

Example:
    python3 tools/import_known_cc0_packs.py --source "$HOME/Downloads" --apply
    python3 tools/validate_pixel_assets.py
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import intake_pixel_assets as intake

PACKS = {
    "pulse-everyday-streets-16x16.zip": (
        "2344a15e223a77a466a11f0661001a7822fc5648d738e2d04117c9964c321fb4",
        "Pulse Games",
        "https://edfaygo.itch.io/pulse-everyday-streets-1616",
        "https://edfaygo.itch.io/pulse-everyday-streets-1616",
        "LICENSE-CC0.txt",
    ),
    "kenney_pixel-ui-pack.zip": (
        "b76f2f60f2be76eb8e66511038fa4d48faec11e638316fa37d06084878cdf0c7",
        "Kenney",
        "https://kenney.nl/assets/pixel-ui-pack",
        "https://kenney.nl/support",
        "License.txt",
    ),
    "kenney_ui-audio.zip": (
        "946fc23a63d535d693eb31b2eabb80c8c28d6351e2186b344ceb71b2cb1d5eb6",
        "Kenney",
        "https://kenney.nl/assets/ui-audio",
        "https://kenney.nl/support",
        "License.txt",
    ),
    "kenney_music-jingles.zip": (
        "b729ba57959bd58793d2c5cafa348aaf2655d354f3da35ec4729e03ec77197b8",
        "Kenney",
        "https://kenney.nl/assets/music-jingles",
        "https://kenney.nl/support",
        "License.txt",
    ),
    "kenney_ui-pack.zip": (
        "a8a14a234911eb648c062622915c93e79e94e97cb7f9f375a70f6617f1174318",
        "Kenney",
        "https://kenney.nl/assets/ui-pack",
        "https://kenney.nl/support",
        "License.txt",
    ),
    "Owlish Media Sound Effects.zip": (
        "57d7059fe2c0ea5f47c7554ace22a538ea22ab40bfc0906b71aa259afffd3d18",
        "OwlishMedia",
        "https://opengameart.org/content/sound-effects-pack",
        "https://opengameart.org/content/sound-effects-pack",
        None,  # Public publisher page explicitly labels this exact ZIP CC0.
    ),
}

def collect(source: Path) -> tuple[list[dict], list[str]]:
    matches: list[dict] = []
    issues: list[str] = []
    source = source.expanduser().resolve()
    if not source.is_dir():
        raise SystemExit("Download directory does not exist: " + str(source))
    for name, (pinned, creator, source_url, rights_url, license_name) in PACKS.items():
        found = [p for p in source.rglob(name) if p.is_file() and not p.is_symlink()]
        if not found:
            issues.append("NOT FOUND: " + name)
            continue
        valid = [p for p in found if intake.sha256(p) == pinned]
        if not valid:
            issues.append("DIGEST MISMATCH: " + name + " (not automatically approved)")
            continue
        archive = sorted(valid, key=lambda p: len(p.parts))[0]
        scan = intake.scan_archive(archive)
        if scan["issues"]:
            issues.append("UNSAFE ARCHIVE: " + name + ": " + ", ".join(scan["issues"]))
            continue
        # Confirm the matching archive still contains the claimed license text.
        if license_name:
            import zipfile
            with zipfile.ZipFile(archive) as zipped:
                try:
                    license_bytes = zipped.read(license_name)
                    if b"CC0" not in license_bytes and b"Creative Commons Zero" not in license_bytes:
                        raise ValueError("archive license does not establish CC0")
                except (KeyError, ValueError):
                    issues.append("MISSING/INVALID EMBEDDED LICENSE: " + name)
                    continue
        matches.append({
            "path": str(archive),
            "name": archive.name,
            "sha256": pinned,
            "bytes": archive.stat().st_size,
            "kind": "zip",
            "contents": scan["counts"],
            "issues": [],
            "approved": True,
            "redistribute_public": True,
            "license_id": "CC0-1.0",
            "source_url": source_url,
            "license_evidence_url": rights_url,
            "creator": creator,
            "notes": "Exact user-provided SHA-256 and publisher CC0 proof; do not apply this approval to other ZIPs.",
        })
    return matches, issues


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(Path.home() / "Downloads"))
    parser.add_argument("--apply", action="store_true", help="Import the selected verified CC0 packs without per-file prompts")
    args = parser.parse_args()
    matches, issues = collect(Path(args.source))
    print("PINNED CC0 PACKS: %d/%d" % (len(matches), len(PACKS)))
    for item in matches:
        print("OK:", item["name"], item["contents"])
    for issue in issues:
        print("REVIEW:", issue)
    if not args.apply:
        print("Dry run: no data imported. Use --apply when you're satisfied.")
        return
    if not matches:
        raise SystemExit("No matching CC0 packs, nothing to import.")
    intake.PRIVATE.mkdir(parents=True, exist_ok=True)
    if intake.REVIEWS.exists():
        existing = intake.load()
        # The 953-item all-Downloads report may include sensitive unrelated
        # files. Preserve it locally but never publish or auto-approve it.
        backup = intake.PRIVATE / "reviews.all-downloads.backup.json"
        if not backup.exists() and any(record["name"] not in PACKS for record in existing.get("files", [])):
            shutil.copy2(intake.REVIEWS, backup)
    intake.save({
        "schemaVersion": 1,
        "scannedFrom": str(Path(args.source).resolve()),
        "selected": "exact hash-pinned CC0 LIVEIT user assets",
        "notes": "Only the listed six CC0 archives have been auto-approved; all other user files remain untouched.",
        "files": matches,
    })
    intake.import_approved()
    print("DONE. Run: python3 tools/validate_pixel_assets.py")
    print("Then inspect: git status --short && du -sh assets/imported")
    print("Only commit/push after reviewing actual files and GitHub's size limits.")

if __name__ == "__main__":
    main()
