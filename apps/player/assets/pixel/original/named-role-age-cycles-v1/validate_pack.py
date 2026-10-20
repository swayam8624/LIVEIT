"""Validate named role age cycles v1 completeness and byte hashes."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
ACTOR_STAGES = {
    "teacher": ("toddler", "child", "teen", "adult", "midlife", "elder"),
    "shopkeeper": ("toddler", "child", "teen", "adult", "midlife", "elder"),
    "nurse": ("toddler", "child", "teen", "adult", "midlife", "elder"),
    "physician": ("toddler", "child", "teen", "adult", "midlife", "elder"),
    "transit-worker": ("toddler", "child", "teen", "adult", "midlife", "elder"),
    "cafe-owner": ("toddler", "child", "teen", "adult", "midlife", "elder"),
    "grandparent": ("adult", "midlife", "elder"),
    "mentor": ("adult", "midlife", "elder"),
    "boss": ("adult", "midlife", "elder"),
    "coworker": ("adult", "midlife", "elder"),
    "friend-one": ("child", "teen", "adult", "midlife", "elder"),
    "friend-two": ("child", "teen", "adult", "midlife", "elder"),
    "neighbor": ("adult", "midlife", "elder"),
}
STAGES = ("toddler", "child", "teen", "adult", "midlife", "elder")
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("contact-a", "passing-a", "contact-b", "passing-b", "idle", "interact")
PIVOT = {"x": 12, "y": 31}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    provenance_path = ROOT / "provenance.json"
    provenance = json.loads(provenance_path.read_text())
    assert manifest["batch"] == "named-role-age-cycles-v1"
    assert manifest["runtimeReady"] is False and all(not f["runtimeReady"] for f in manifest["frames"])
    assert manifest["frameSize"] == {"width": 24, "height": 32}
    assert manifest["pivot"] == PIVOT
    assert set(x["id"] for x in manifest["identities"]) == set(ACTOR_STAGES)
    assert manifest["ageStages"] == {actor: list(stages) for actor, stages in ACTOR_STAGES.items()}
    assert all(x["ageStages"] == list(ACTOR_STAGES[x["id"]]) for x in manifest["identities"])
    assert manifest["provenanceSha256"] == sha(provenance_path)
    assert provenance["providedArchivesUsed"] == [] and provenance["thirdPartyArtUsed"] is False
    expected_count = sum(len(stages) for stages in ACTOR_STAGES.values()) * len(DIRECTIONS) * len(PHASES)
    assert len(manifest["frames"]) == expected_count
    seen = set()
    for frame in manifest["frames"]:
        key = (frame["character"], frame["ageStage"], frame["direction"], frame["phase"])
        assert frame["ageStage"] in ACTOR_STAGES[frame["character"]], key
        assert key not in seen, key
        seen.add(key)
        path = ROOT / frame["file"]
        assert path.is_file(), path
        with Image.open(path) as im:
            assert im.size == (24, 32) and im.mode == "RGBA", (path, im.size, im.mode)
        assert frame["pivot"] == PIVOT and frame["sha256"] == sha(path), path
        source = ROOT.parent / frame["source"]
        assert source.is_file(), source
    assert len(seen) == expected_count
    for output in manifest["outputs"].values():
        path = ROOT / output["file"]
        assert path.is_file() and sha(path) == output["sha256"], path
        with Image.open(path) as im:
            assert im.size == (output["width"], output["height"]), path
    full = sum(len(ACTOR_STAGES[a]) for a in ACTOR_STAGES if a in {"teacher", "shopkeeper", "nurse", "physician", "transit-worker", "cafe-owner"})
    print(f"PASS: {len(seen)} unique frames across {len(ACTOR_STAGES)} identities; {full // 6} full six-stage identities plus role-specific age subsets; source hashes and previews valid; runtimeReady=false")

if __name__ == "__main__":
    main()
