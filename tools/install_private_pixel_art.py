#!/usr/bin/env python3
"""Install owner-downloaded, noncommercial Modern Interiors sprites LOCALLY.

Never downloads, commits or redistributes third-party artwork. The public
LIVEIT branch uses CC0 sprites by default. This optional overlay reads the
owner's own ZIP, installs only two necessary sprites and patches pixelArt.ts
in the local checkout to make them statically bundleable on iOS/Android/Web.

Run:
  python3 tools/install_private_pixel_art.py --source ~/Downloads
  npm run web -w @living/player -- --clear

License: "Modern tiles_Free/LICENSE.txt" explicitly permits non-commercial
use but does NOT grant commercial distribution. You remain responsible for
your own rights and must not commit or publish the installed artwork.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import zipfile

SPRITES = {
    "Adam_run_16x16.png": "player_modern",
    "Amelia_idle_anim_16x16.png": "npc_modern",
}
SHEET_ROOT = "Modern tiles_Free/Characters_free/"
MARKER = "  // BEGIN LOCAL NONCOMMERCIAL ART (DO NOT COMMIT)"
END_MARKER = "  // END LOCAL NONCOMMERCIAL ART"


def run() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path.home() / "Downloads")
    parser.add_argument("--repo", type=Path,
                        default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    source = args.source.expanduser()
    repo = args.repo.expanduser()
    files = sorted(source.glob("Modern_Interiors_Free_v2.2*.zip"))
    if not files:
        print(f"No Modern_Interiors_Free_v2.2*.zip in {source}")
        return 2

    source_zip = files[-1]
    output = repo / "apps/player/assets/private/modern"
    artfile = repo / "apps/player/src/pixelArt.ts"
    if not artfile.is_file():
        print(f"Not a LIVEIT checkout: {artfile}")
        return 2

    with zipfile.ZipFile(source_zip) as archive:
        names = set(archive.namelist())
        license_path = "Modern tiles_Free/LICENSE.txt"
        if license_path not in names:
            print("Missing license file: refusing to import unknown pack.")
            return 2
        license = archive.read(license_path).decode("utf8", errors="replace")
        if "NON COMMERCIAL" not in license.upper():
            print("Unexpected license; review source pack manually.")
            return 2
        missing = [SHEET_ROOT + filename for filename in SPRITES
                   if SHEET_ROOT + filename not in names]
        if missing:
            print("Source ZIP is missing expected sprites:", missing)
            return 2
        output.mkdir(parents=True, exist_ok=True)
        for filename in SPRITES:
            (output / filename).write_bytes(archive.read(SHEET_ROOT + filename))

    original = artfile.read_text(encoding="utf8")
    if MARKER not in original:
        lines = [MARKER]
        for filename, key in SPRITES.items():
            lines.append(
                f"  {key}: require('../assets/private/modern/{filename}'),")
        lines.append(END_MARKER)
        original = original.replace("export const pixelArt = {",
                                    "export const pixelArt = {\n" +
                                    "\n".join(lines), 1)
        artfile.write_text(original, encoding="utf8")

    print("Local-only modern character walk and NPC sprites installed.")
    print("LICENSE: noncommercial only. Do not commit or redistribute artwork.")
    print("Restart Metro using --clear.")
    print("Before pushing: git status --short, omit pixelArt.ts and private assets.")
    return 0


if __name__ == "__main__":
    sys.exit(run())
