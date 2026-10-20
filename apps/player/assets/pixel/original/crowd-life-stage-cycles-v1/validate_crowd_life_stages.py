#!/usr/bin/env python3
"""Validate hashes, source links, stage coverage, and pixel contracts."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import build_crowd_life_stages as build  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    root_manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    provenance = json.loads((ROOT / "provenance.json").read_text(encoding="utf-8"))
    if root_manifest.get("runtimeReady") is not False or provenance.get("runtimeReady") is not False:
        fail("pack and provenance must remain runtimeReady:false")
    if root_manifest["frameSize"] != {"width": 24, "height": 32} or root_manifest["pivot"] != {"x": 12, "y": 31}:
        fail("root frame size or pivot differs from the 24x32 contract")
    if root_manifest["directions"] != list(build.DIRECTIONS) or root_manifest["phases"] != list(build.PHASES):
        fail("root direction/phase contract mismatch")

    sources = build.load_sources()
    expected_roles = set(build.AGE_POLICY)
    if set(sources) != expected_roles:
        fail(f"source and age-policy role set differs: source={len(sources)} expected={len(expected_roles)}")
    if root_manifest["roleCount"] != len(expected_roles):
        fail(f"expected {len(expected_roles)} roles, found {root_manifest['roleCount']}")
    if len(root_manifest["roles"]) != len(expected_roles):
        fail("root role index is incomplete or has duplicate entries")

    checked = 0
    seen_paths: set[str] = set()
    actual_stages: dict[str, set[str]] = {}
    for role_summary in root_manifest["roles"]:
        role = role_summary["role"]
        if role not in expected_roles:
            fail(f"unexpected role {role}")
        role_manifest_path = ROOT / role_summary["manifest"]
        role_manifest = json.loads(role_manifest_path.read_text(encoding="utf-8"))
        if role_manifest.get("runtimeReady") is not False or role_summary.get("runtimeReady") is not False:
            fail(f"{role}: runtimeReady must remain false")
        expected_stage_set = set(build.AGE_POLICY[role])
        summary_stage_set = {item["ageStage"] for item in role_manifest["ageStages"]}
        if summary_stage_set != expected_stage_set:
            fail(f"{role}: stage coverage mismatch expected={sorted(expected_stage_set)} found={sorted(summary_stage_set)}")
        actual_stages[role] = summary_stage_set
        role_frame_count = 0
        source_frame_map = sources[role]["frames"]
        for age_summary in role_manifest["ageStages"]:
            age = age_summary["ageStage"]
            age_manifest_path = ROOT / age_summary["manifest"]
            age_manifest = json.loads(age_manifest_path.read_text(encoding="utf-8"))
            if age_manifest.get("runtimeReady") is not False:
                fail(f"{role}/{age}: runtimeReady must remain false")
            if age_manifest["frameSize"] != {"width": 24, "height": 32} or age_manifest["pivot"] != {"x": 12, "y": 31}:
                fail(f"{role}/{age}: frame size or pivot mismatch")
            if age_manifest["directions"] != list(build.DIRECTIONS) or age_manifest["phases"] != list(build.PHASES):
                fail(f"{role}/{age}: direction/phase list mismatch")
            expected_ids = {f"{role}/{age}/{direction}/{phase}" for direction in build.DIRECTIONS for phase in build.PHASES}
            frame_ids = {frame["id"] for frame in age_manifest["frames"]}
            if frame_ids != expected_ids or len(age_manifest["frames"]) != 12:
                fail(f"{role}/{age}: expected exactly 12 unique direction/phase frames")
            if age_manifest["frameCount"] != 12 or age_summary["frameCount"] != 12:
                fail(f"{role}/{age}: summary frame count is not 12")
            for record in age_manifest["frames"]:
                path = ROOT / record["file"]
                if record["file"] in seen_paths:
                    fail(f"duplicate generated path {record['file']}")
                seen_paths.add(record["file"])
                if not path.is_file() or sha(path) != record["sha256"]:
                    fail(f"missing or mismatched output hash: {record['file']}")
                source_path = build.ORIGINALS / record["sourceFile"]
                if not source_path.is_file() or sha(source_path) != record["sourceSha256"]:
                    fail(f"missing or mismatched source hash: {record['sourceFile']}")
                if record["runtimeReady"] is not False:
                    fail(f"{record['id']}: frame must remain runtimeReady:false")
                if record["width"] != 24 or record["height"] != 32 or record["mode"] != "RGBA" or record["pivot"] != {"x": 12, "y": 31}:
                    fail(f"{record['id']}: record geometry mismatch")
                with Image.open(path) as image:
                    if image.size != (24, 32) or image.mode != "RGBA":
                        fail(f"{record['id']}: image geometry or mode mismatch")
                    alpha_bounds = image.getchannel("A").getbbox()
                    if alpha_bounds is None:
                        fail(f"{record['id']}: fully transparent frame")
                    if alpha_bounds[3] != 32:
                        fail(f"{record['id']}: opaque art no longer rests on the shared bottom baseline")
                    if age == "adult":
                        source_frame = source_frame_map[(record["direction"], record["phase"])]
                        with Image.open(source_frame) as source_image:
                            if image.tobytes() != source_image.convert("RGBA").tobytes():
                                fail(f"{record['id']}: adult frame must be an exact source copy")
                checked += 1
            role_frame_count += len(age_manifest["frames"])
        if role_frame_count != role_manifest["frameCount"] or role_frame_count != role_summary["frameCount"]:
            fail(f"{role}: role frame counts do not reconcile")

    if checked != root_manifest["frameCount"]:
        fail(f"root frame count mismatch expected={root_manifest['frameCount']} checked={checked}")
    if checked != len(seen_paths):
        fail("generated frame path uniqueness check failed")
    if any("child" in stages for role, stages in actual_stages.items() if role not in {"student", "library-visitor", "runner", "tourist", "artist", "athlete", "shopper", "gardener", "child-playground"}):
        fail("a child variant was assigned to a role outside the age-safe participation allowlist")
    print(f"PASS: {len(expected_roles)} roles; {sum(len(v) for v in actual_stages.values())} role-age cycles; {checked} unique 24x32 RGBA frames; all hashes and adult source copies match; runtimeReady=false")


if __name__ == "__main__":
    main()
