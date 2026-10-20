#!/usr/bin/env python3
"""Build deterministic age-stage variants from the original crowd concepts.

This concept pack reuses only the project's own v1-v3 Pillow-drawn crowd
sprites. Child and teen proportions are produced with nearest-neighbour
resizing anchored to the shared ground pivot; elder variants recolor the
source role's exact hair palette to a silver palette. Adult is the source
frame unchanged. No ZIP archive, internet image, or model output is read.
"""
from __future__ import annotations

import hashlib
import json
import re
import runpy
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
ORIGINALS = ROOT.parent
SIZE = (24, 32)
PIVOT = {"x": 12, "y": 31}
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("walk-a", "walk-b", "idle")
AGES = ("child", "teen", "adult", "elder")
SILVER = (169, 177, 188, 255)

# Ages are intentionally conservative. Child variants are non-working
# participants/hobbyists (8-12); teen variants are 16-19, still limited to
# non-professional activities. Adult is 20-59; elder is 60+. Occupation cues
# remain costume/context cues and do not imply a minor is employed.
AGE_POLICY: dict[str, dict[str, str]] = {
    "student": {"child": "school-age learner", "teen": "late-teen learner", "adult": "adult learner", "elder": "lifelong learner"},
    "office-worker": {"adult": "working-age office role", "elder": "older worker or retired neighbor retaining the role's style"},
    "store-clerk": {"adult": "working-age shop role", "elder": "older worker or retired neighbor retaining the role's style"},
    "baker": {"adult": "working-age bakery role", "elder": "older worker or retired neighbor retaining the role's style"},
    "delivery-rider": {"adult": "working-age delivery role", "elder": "older worker or retired neighbor retaining the role's style"},
    "bus-driver": {"adult": "working-age transit role", "elder": "older worker or retired neighbor retaining the role's style"},
    "taxi-driver": {"adult": "working-age driving role", "elder": "older worker or retired neighbor retaining the role's style"},
    "police-officer": {"adult": "adult public-safety role", "elder": "older professional or retired neighbor retaining the role's style"},
    "library-visitor": {"child": "school-age library visitor", "teen": "late-teen library visitor", "adult": "adult library visitor", "elder": "older library visitor"},
    "street-musician": {"adult": "adult performer", "elder": "older performer"},
    "runner": {"child": "recreational runner; not a professional athlete", "teen": "late-teen recreational runner", "adult": "adult runner", "elder": "older recreational walker or runner"},
    "tourist": {"child": "child tourist with guardian context", "teen": "late-teen tourist", "adult": "adult tourist", "elder": "older tourist"},
    "mechanic": {"adult": "working-age mechanic role", "elder": "older mechanic or retired neighbor retaining the role's style"},
    "artist": {"child": "young hobby artist", "teen": "late-teen hobby or student artist", "adult": "adult artist", "elder": "older artist"},
    "filmmaker": {"adult": "adult filmmaker", "elder": "older filmmaker"},
    "athlete": {"child": "youth recreation; not professional sport", "teen": "late-teen recreational or school athlete", "adult": "adult athlete", "elder": "older recreational athlete"},
    "shopper": {"child": "child shopper with guardian context", "teen": "late-teen shopper", "adult": "adult shopper", "elder": "older shopper"},
    "barista": {"adult": "adult cafe role", "elder": "older worker or retired neighbor retaining the role's style"},
    "pet-walker": {"adult": "adult pet walker", "elder": "older pet walker"},
    "market-vendor": {"adult": "adult market role", "elder": "older worker or retired neighbor retaining the role's style"},
    "security-guard": {"adult": "adult security role", "elder": "older professional or retired neighbor retaining the role's style"},
    "historian": {"adult": "adult historian", "elder": "older historian"},
    "park-cleaner": {"adult": "adult park-maintenance role", "elder": "older worker or retired neighbor retaining the role's style"},
    "nurse": {"adult": "adult nursing role", "elder": "older professional or retired neighbor retaining the role's style"},
    "caregiver": {"adult": "adult caregiving role", "elder": "older caregiver or retired neighbor retaining the role's style"},
    "gardener": {"child": "supervised garden hobbyist, not an employee", "teen": "late-teen garden hobbyist", "adult": "adult gardener", "elder": "older gardener"},
    "teacher": {"adult": "adult teaching role", "elder": "older professional or retired neighbor retaining the role's style"},
    "parent-with-stroller": {"adult": "adult parent", "elder": "grandparent accompanying a child"},
    "child-playground": {"child": "child at play", "teen": "older youth at play"},
    "elder-walker": {"elder": "older adult with a cane; mobility aid is not treated as a defect"},
}

SOURCE_DIRS = {
    1: ORIGINALS / "crowd-archetypes-batch-v1",
    2: ORIGINALS / "crowd-archetypes-batch-v2",
    3: ORIGINALS / "crowd-archetypes-batch-v3",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_color(value: object) -> tuple[int, int, int, int] | None:
    if isinstance(value, (tuple, list)) and len(value) >= 3:
        return (int(value[0]), int(value[1]), int(value[2]), int(value[3]) if len(value) > 3 else 255)
    if isinstance(value, str):
        match = re.fullmatch(r"#?([0-9a-fA-F]{6})(?:([0-9a-fA-F]{2}))?", value)
        if match:
            rgb = tuple(int(match.group(1)[i:i + 2], 16) for i in (0, 2, 4))
            alpha = int(match.group(2), 16) if match.group(2) else 255
            return (*rgb, alpha)
    return None


def load_role_hair() -> dict[str, tuple[int, int, int, int]]:
    result: dict[str, tuple[int, int, int, int]] = {}
    for version, source_dir in SOURCE_DIRS.items():
        script = next(source_dir.glob("build_*.py"))
        definitions = runpy.run_path(str(script))["ROLES"]
        for role, definition in definitions.items():
            color = parse_color(definition.get("hair"))
            if color is not None:
                result[role] = color
    return result


def load_sources() -> dict[str, dict[str, object]]:
    sources: dict[str, dict[str, object]] = {}
    for version, source_dir in SOURCE_DIRS.items():
        batch_manifest = json.loads((source_dir / "manifest.json").read_text(encoding="utf-8"))
        for role_summary in batch_manifest["roles"]:
            role_manifest_path = source_dir / role_summary["manifest"]
            role_manifest = json.loads(role_manifest_path.read_text(encoding="utf-8"))
            frames: dict[tuple[str, str], Path] = {}
            for frame in role_manifest["frames"]:
                raw = Path(frame["file"])
                candidates = (role_manifest_path.parent / raw, source_dir / raw)
                frame_path = next((p for p in candidates if p.is_file()), None)
                if frame_path is None:
                    raise FileNotFoundError(f"Could not resolve source frame {frame['file']} for {role_summary['role']}")
                frames[(frame["direction"], frame["phase"])] = frame_path
            sources[role_summary["role"]] = {
                "version": version,
                "sourceBatch": batch_manifest["id"],
                "sourceManifest": str(role_manifest_path.relative_to(ORIGINALS)),
                "roleManifest": role_manifest,
                "frames": frames,
            }
    return sources


def stage_frame(source: Image.Image, age: str, hair: tuple[int, int, int, int] | None) -> Image.Image:
    frame = source.convert("RGBA")
    if age in ("child", "teen"):
        # Preserve the bottom-center ground anchor while making a compact,
        # readable age silhouette. Props remain attached to the character.
        target = (20, 27) if age == "child" else (22, 29)
        scaled = frame.resize(target, Image.Resampling.NEAREST)
        canvas = Image.new("RGBA", SIZE, (0, 0, 0, 0))
        canvas.alpha_composite(scaled, ((SIZE[0] - target[0]) // 2, SIZE[1] - target[1]))
        return canvas
    if age == "elder" and hair is not None:
        pixels = frame.load()
        for y in range(frame.height):
            for x in range(frame.width):
                if pixels[x, y] == hair:
                    pixels[x, y] = SILVER
    return frame


def build() -> None:
    sources = load_sources()
    hair_by_role = load_role_hair()
    role_summaries = []
    total_frames = 0
    for role, age_notes in AGE_POLICY.items():
        if role not in sources:
            raise ValueError(f"Age policy references unknown crowd role: {role}")
        source = sources[role]
        role_manifest = source["roleManifest"]
        source_frames = source["frames"]
        role_root = ROOT / "frames" / role
        age_entries = []
        for age in AGES:
            if age not in age_notes:
                continue
            age_root = role_root / age
            age_root.mkdir(parents=True, exist_ok=True)
            records = []
            for direction in DIRECTIONS:
                for phase in PHASES:
                    source_path = source_frames[(direction, phase)]
                    with Image.open(source_path) as opened:
                        image = stage_frame(opened, age, hair_by_role.get(role))
                    output_path = age_root / f"{role}-{age}-{direction}-{phase}.png"
                    image.save(output_path, format="PNG", optimize=False)
                    records.append({
                        "id": f"{role}/{age}/{direction}/{phase}",
                        "role": role,
                        "ageStage": age,
                        "ageBand": {"child": "8-12", "teen": "16-19", "adult": "20-59", "elder": "60+"}[age],
                        "ageNote": age_notes[age],
                        "direction": direction,
                        "phase": phase,
                        "file": str(output_path.relative_to(ROOT)),
                        "width": 24,
                        "height": 32,
                        "mode": "RGBA",
                        "pivot": PIVOT,
                        "sha256": digest(output_path),
                        "sourceFile": str(source_path.relative_to(ORIGINALS)),
                        "sourceSha256": digest(source_path),
                        "runtimeReady": False,
                    })
            total_frames += len(records)
            age_manifest = {
                "id": f"crowd-{role}-{age}-movement-age-v1",
                "role": role,
                "ageStage": age,
                "ageBand": {"child": "8-12", "teen": "16-19", "adult": "20-59", "elder": "60+"}[age],
                "ageNote": age_notes[age],
                "catalogId": role_manifest.get("catalogId", role_manifest.get("catalog")),
                "sourceBatch": source["sourceBatch"],
                "sourceManifest": source["sourceManifest"],
                "frameSize": {"width": 24, "height": 32},
                "pivot": PIVOT,
                "directions": list(DIRECTIONS),
                "phases": list(PHASES),
                "frameCount": len(records),
                "frames": records,
                "runtimeReady": False,
            }
            (age_root / "manifest.json").write_text(json.dumps(age_manifest, indent=2) + "\n", encoding="utf-8")
            age_entries.append({"ageStage": age, "manifest": str((age_root / "manifest.json").relative_to(ROOT)), "frameCount": len(records), "runtimeReady": False})
        role_manifest_out = {
            "role": role,
            "label": role_manifest.get("label", role),
            "catalogId": role_manifest.get("catalogId", role_manifest.get("catalog")),
            "description": role_manifest.get("description", ""),
            "sourceBatch": source["sourceBatch"],
            "sourceManifest": source["sourceManifest"],
            "ageStages": age_entries,
            "frameCount": sum(entry["frameCount"] for entry in age_entries),
            "runtimeReady": False,
        }
        (role_root / "manifest.json").write_text(json.dumps(role_manifest_out, indent=2) + "\n", encoding="utf-8")
        role_summaries.append(role_manifest_out)

    provenance = {
        "id": "crowd-life-stage-cycles-v1",
        "created": "2026-10-20",
        "method": "Deterministic nearest-neighbour resizing and exact source-palette hair recoloring of original project-authored crowd concept frames from batches v1-v3.",
        "sourceRights": "All source pixels came from locally authored, project-owned concept batches. No supplied ZIP, internet asset, external raster, or model output was used.",
        "ageMethod": {
            "child": "20x27 nearest-neighbour source frame anchored on the common ground pivot; non-professional participation only.",
            "teen": "22x29 nearest-neighbour source frame anchored on the common ground pivot; age band is 16-19 and employment roles are not represented at this stage.",
            "adult": "Exact source frame copy.",
            "elder": "Exact source frame with exact palette hair pixels changed to silver; mobility cues remain role-specific and are not universalized.",
        },
        "technical": {"frameSize": {"width": 24, "height": 32}, "mode": "RGBA", "pivot": PIVOT, "directions": list(DIRECTIONS), "phases": list(PHASES)},
        "runtimeReady": False,
    }
    (ROOT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    root_manifest = {
        "id": "crowd-life-stage-cycles-v1",
        "kind": "original-pixel-crowd-age-movement-concepts",
        "ageBands": {"child": "8-12", "teen": "16-19", "adult": "20-59", "elder": "60+"},
        "frameSize": {"width": 24, "height": 32},
        "pivot": PIVOT,
        "directions": list(DIRECTIONS),
        "phases": list(PHASES),
        "roleCount": len(role_summaries),
        "frameCount": total_frames,
        "roles": [{"role": item["role"], "manifest": str((ROOT / "frames" / item["role"] / "manifest.json").relative_to(ROOT)), "ageStages": [age["ageStage"] for age in item["ageStages"]], "frameCount": item["frameCount"], "runtimeReady": False} for item in role_summaries],
        "runtimeReady": False,
    }
    (ROOT / "manifest.json").write_text(json.dumps(root_manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
