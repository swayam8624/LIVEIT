"""Build deterministic, original age-stage derivatives for six named actors.

The adult base designs are project-owned concept sprites from the named-role
packs. This builder reads only those local concept PNGs; it never reads the
provided ZIP archives or third-party art. Output remains concept-only.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT.parent
SOURCES = {
    "teacher": ASSET_ROOT / "named-characters-batch-v1" / "frames" / "teacher",
    "shopkeeper": ASSET_ROOT / "named-characters-batch-v4" / "frames" / "shopkeeper",
    "nurse": ASSET_ROOT / "named-characters-batch-v4" / "frames" / "nurse",
    "physician": ASSET_ROOT / "named-characters-batch-v4" / "frames" / "physician",
    "transit-worker": ASSET_ROOT / "named-characters-batch-v4" / "frames" / "transit-worker",
    "cafe-owner": ASSET_ROOT / "named-characters-batch-v4" / "frames" / "cafe-owner",
    "grandparent": ASSET_ROOT / "named-characters-batch-v2" / "frames" / "grandparent",
    "mentor": ASSET_ROOT / "named-characters-batch-v2" / "frames" / "mentor",
    "boss": ASSET_ROOT / "named-characters-batch-v3" / "frames" / "boss",
    "coworker": ASSET_ROOT / "named-characters-batch-v3" / "frames" / "coworker",
    "friend-one": ASSET_ROOT / "named-characters-batch-v3" / "frames" / "friend-one",
    "friend-two": ASSET_ROOT / "named-characters-batch-v3" / "frames" / "friend-two",
    "neighbor": ASSET_ROOT / "named-characters-batch-v3" / "frames" / "neighbor",
}
NAMES = {
    "teacher": "Bellweather teacher",
    "shopkeeper": "Bellweather shopkeeper",
    "nurse": "Bellweather nurse",
    "physician": "Bellweather physician",
    "transit-worker": "Bellweather transit worker",
    "cafe-owner": "Bellweather cafe owner",
    "grandparent": "Dadi",
    "mentor": "Ishan",
    "boss": "Bellweather boss",
    "coworker": "Bellweather coworker",
    "friend-one": "Bellweather friend one",
    "friend-two": "Bellweather friend two",
    "neighbor": "Bellweather neighbor",
}
STAGES = ("toddler", "child", "teen", "adult", "midlife", "elder")
ACTOR_STAGES = {
    "teacher": STAGES,
    "shopkeeper": STAGES,
    "nurse": STAGES,
    "physician": STAGES,
    "transit-worker": STAGES,
    "cafe-owner": STAGES,
    # These roles have established older ages or adult responsibilities. Their
    # own identity art supplies the source for every derivative stage.
    "grandparent": ("adult", "midlife", "elder"),
    "mentor": ("adult", "midlife", "elder"),
    "boss": ("adult", "midlife", "elder"),
    "coworker": ("adult", "midlife", "elder"),
    "friend-one": ("child", "teen", "adult", "midlife", "elder"),
    "friend-two": ("child", "teen", "adult", "midlife", "elder"),
    "neighbor": ("adult", "midlife", "elder"),
}
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("contact-a", "passing-a", "contact-b", "passing-b", "idle", "interact")
PIVOT = {"x": 12, "y": 31}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def age_frame(source: Image.Image, stage: str, direction: str, phase: str) -> Image.Image:
    """Apply a stable age silhouette while retaining the source costume cues."""
    scales = {
        "toddler": (0.66, 0.79),
        "child": (0.78, 0.88),
        "teen": (0.91, 0.94),
        "adult": (1.00, 1.00),
        "midlife": (0.99, 0.99),
        "elder": (0.96, 0.96),
    }
    width_scale, height_scale = scales[stage]
    # Keep a transparent cell and preserve bottom-center foot placement.
    bounds = source.getbbox()
    if bounds:
        crop = source.crop(bounds)
        size = (max(1, round(crop.width * width_scale)), max(1, round(crop.height * height_scale)))
        crop = crop.resize(size, Image.Resampling.NEAREST)
        result = Image.new("RGBA", (24, 32), (0, 0, 0, 0))
        x = (24 - crop.width) // 2
        y = 31 - crop.height
        result.alpha_composite(crop, (x, y))
    else:
        result = Image.new("RGBA", (24, 32), (0, 0, 0, 0))

    # Midlife and elder hair shifts are restricted to the upper hair mass.
    # This keeps skin and role props intact while making age readable at 1x.
    if stage in ("midlife", "elder"):
        pix = result.load()
        gray = (164, 168, 163, 255) if stage == "midlife" else (202, 205, 196, 255)
        for y in range(5, 10):
            for x in range(6, 18):
                r, g, b, a = pix[x, y]
                if a and max(r, g, b) < 150 and abs(r - g) < 50:
                    # Scattered, fixed streaks; elder has a stronger crown.
                    if (x + y) % (5 if stage == "midlife" else 3) == 0:
                        pix[x, y] = gray

    # Elder posture cue: a quiet forward shoulder pixel and optional cane.
    # The cane is attached at the hand side, without moving the shared pivot.
    if stage == "elder":
        draw = ImageDraw.Draw(result)
        draw.point((14 if direction in ("south", "east") else 9, 17), fill=(104, 78, 61, 255))
        if phase in ("idle", "interact"):
            cane_x = 18 if direction in ("south", "east") else 5
            draw.line((cane_x, 18, cane_x, 29), fill=(137, 94, 61, 255), width=1)
            draw.point((cane_x - 1, 30), fill=(89, 68, 57, 255))
    return result


def main() -> None:
    frames = []
    for actor, source_dir in SOURCES.items():
        for stage in ACTOR_STAGES[actor]:
            for direction in DIRECTIONS:
                for phase in PHASES:
                    source = source_dir / f"{actor}-{direction}-{phase}.png"
                    if not source.is_file():
                        raise FileNotFoundError(source)
                    out = ROOT / "frames" / actor / stage / f"{actor}-{stage}-{direction}-{phase}.png"
                    out.parent.mkdir(parents=True, exist_ok=True)
                    age_frame(Image.open(source).convert("RGBA"), stage, direction, phase).save(out, optimize=False)
                    frames.append({
                        "id": f"{actor}/{stage}/{direction}/{phase}",
                        "character": actor,
                        "displayName": NAMES[actor],
                        "ageStage": stage,
                        "direction": direction,
                        "phase": phase,
                        "file": out.relative_to(ROOT).as_posix(),
                        "width": 24,
                        "height": 32,
                        "mode": "RGBA",
                        "pivot": PIVOT,
                        "source": source.relative_to(ASSET_ROOT).as_posix(),
                        "sha256": digest(out),
                        "runtimeReady": False,
                    })

    manifest = {
        "schemaVersion": 1,
        "batch": "named-role-age-cycles-v1",
        "direction": "PIXEL-ONLY",
        "description": "Original age-stage concept cycles derived from project-owned named-role base designs.",
        "runtimeReady": False,
        "frameSize": {"width": 24, "height": 32},
        "pivot": PIVOT,
        "directions": list(DIRECTIONS),
        "phases": list(PHASES),
        "ageStages": {actor: list(stages) for actor, stages in ACTOR_STAGES.items()},
        "identities": [
            {"id": actor, "displayName": NAMES[actor], "basePack": source_dir.parent.parent.name, "ageStages": list(ACTOR_STAGES[actor]), "runtimeReady": False}
            for actor, source_dir in SOURCES.items()
        ],
        "frames": frames,
    }
    manifest_path = ROOT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    provenance = {
        "batch": "named-role-age-cycles-v1",
        "authorship": "Locally authored deterministic transformations of original project-owned pixel concepts.",
        "sourceFiles": sorted({frame["source"] for frame in frames}),
        "providedArchivesUsed": [],
        "thirdPartyArtUsed": False,
        "generator": "build_assets.py using Pillow nearest-neighbor resizing and explicit pixel edits.",
        "runtimeReady": False,
        "licenseNote": "No third-party license is asserted; review and pixel-art QA are required before runtime promotion.",
    }
    prov_path = ROOT / "provenance.json"
    prov_path.write_text(json.dumps(provenance, indent=2) + "\n")
    manifest["provenanceSha256"] = digest(prov_path)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    # Review atlas: six age columns, 24 cells per row (four dirs × six phases).
    atlas = Image.new("RGBA", (24 * len(STAGES), 32 * len(DIRECTIONS) * len(PHASES)), (0, 0, 0, 0))
    for si, stage in enumerate(STAGES):
        for di, direction in enumerate(DIRECTIONS):
            for pi, phase in enumerate(PHASES):
                src = ROOT / "frames" / "teacher" / stage / f"teacher-{stage}-{direction}-{phase}.png"
                atlas.alpha_composite(Image.open(src).convert("RGBA"), (si * 24, (di * len(PHASES) + pi) * 32))
    atlas.save(ROOT / "teacher-age-review-atlas.png")
    preview_actors = tuple(SOURCES)
    preview_stages = tuple(stage for stage in STAGES if all(stage in ACTOR_STAGES[a] for a in preview_actors))
    sheet = Image.new("RGBA", (24 * 4 * len(preview_actors), 32 * 4 * len(preview_stages)), (28, 36, 48, 255))
    for si, stage in enumerate(preview_stages):
        for ai, actor in enumerate(preview_actors):
            source = ROOT / "frames" / actor / stage / f"{actor}-{stage}-south-idle.png"
            sprite = Image.open(source).convert("RGBA").resize((96, 128), Image.Resampling.NEAREST)
            sheet.alpha_composite(sprite, (ai * 96, si * 128))
    sheet.save(ROOT / "named-role-age-contact-sheet.png")
    manifest["outputs"] = {
        "teacherAgeReviewAtlas": {"file": "teacher-age-review-atlas.png", "width": atlas.width, "height": atlas.height, "sha256": digest(ROOT / "teacher-age-review-atlas.png")},
        "contactSheet": {"file": "named-role-age-contact-sheet.png", "width": sheet.width, "height": sheet.height, "sha256": digest(ROOT / "named-role-age-contact-sheet.png"), "stages": list(preview_stages), "actors": list(preview_actors)},
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
