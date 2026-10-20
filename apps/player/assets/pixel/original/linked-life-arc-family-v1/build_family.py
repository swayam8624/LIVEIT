from pathlib import Path
from PIL import Image
import hashlib, json

ROOT = Path(__file__).parent
ASSET_ROOT = ROOT.parent
EARLY_ROOT = ASSET_ROOT / "life-arc-early-cycles-v1"
LATER_ROOT = ASSET_ROOT / "life-arc-later-cycles-v1"
DIRECTIONS = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b"]
STAGE_MAP = [
    ("infant-crawl", "early", "infant crawl", "primary-player-life-arc"),
    ("toddler-waddle", "early", "toddler waddle", "primary-player-life-arc"),
    ("child-walk", "early", "child", "primary-player-life-arc"),
    ("teen-walk", "early", "teen", "primary-player-life-arc"),
    ("young-adult-woman", "later", "young adult woman", "primary-player-life-arc"),
    ("midlife-woman", "later", "midlife woman", "primary-player-life-arc"),
    ("elder-woman", "later", "elder woman", "primary-player-life-arc"),
    ("elder-man", "later", "elder man", "elder-man-presentation-variant"),
]

stage_records = []
all_frames = []
combined = Image.new("RGBA", (96, 128 * len(STAGE_MAP)), (0, 0, 0, 0))

for stage_index, (stage_id, batch, label, continuity_role) in enumerate(STAGE_MAP):
    atlas = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    frames = []
    if batch == "early":
        stage_root = EARLY_ROOT / stage_id
        source_manifest = json.loads((stage_root / "frames.json").read_text())
        source = source_manifest["source"]
        source_path = stage_root / source["file"]
        rows = source_manifest["frames"]
        base_path = stage_root
    else:
        late_manifest = json.loads((LATER_ROOT / "manifest.json").read_text())
        source_record = next(source for source in late_manifest["sources"] if source["stage"] == stage_id)
        source_path = LATER_ROOT / source_record["file"]
        rows = [frame for frame in late_manifest["frames"] if frame["stage"] == stage_id]
        base_path = LATER_ROOT
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()

    for frame in rows:
        direction = frame["direction"]
        phase = frame["phase"]
        file_path = base_path / frame["file"]
        if batch == "early":
            file_path = stage_root / frame["file"]
        with Image.open(file_path).convert("RGBA") as image:
            if image.size != (24, 32):
                raise ValueError(f"Unexpected frame size {image.size}: {file_path}")
            phase_index = PHASES.index(phase)
            direction_index = DIRECTIONS.index(direction)
            x, y = phase_index * 24, direction_index * 32
            atlas.alpha_composite(image, (x, y))
        frame_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
        item = {
            "id": f"{stage_id}/{direction}/{phase}",
            "stage": stage_id,
            "stageLabel": label,
            "continuityRole": continuity_role,
            "direction": direction,
            "phase": phase,
            "file": str(file_path.relative_to(ASSET_ROOT)),
            "size": [24, 32],
            "pivot": [12, 31],
            "sha256": frame_hash,
            "sourceSheet": str(source_path.relative_to(ASSET_ROOT)),
            "sourceSheetSha256": source_hash,
            "runtimeReady": False,
        }
        frames.append(item)
        all_frames.append(item)

    if len(frames) != 16:
        raise ValueError(f"{stage_id} has {len(frames)} frames; expected 16")
    for direction in DIRECTIONS:
        if {frame["phase"] for frame in frames if frame["direction"] == direction} != set(PHASES):
            raise ValueError(f"Incomplete direction/phase coverage for {stage_id}/{direction}")
    stage_atlas = ROOT / f"{stage_id}-atlas-4x4.png"
    atlas.save(stage_atlas)
    combined.alpha_composite(atlas, (0, stage_index * 128))
    stage_records.append({
        "id": stage_id,
        "label": label,
        "continuityRole": continuity_role,
        "batch": "life-arc-early-cycles-v1" if batch == "early" else "life-arc-later-cycles-v1",
        "atlas": stage_atlas.name,
        "frameCount": len(frames),
        "frames": frames,
        "runtimeReady": False,
    })

combined_path = ROOT / "linked-life-arc-atlas-24x32.png"
combined.save(combined_path)
preview = combined.resize((combined.width * 4, combined.height * 4), Image.Resampling.NEAREST)
preview_path = ROOT / "linked-life-arc-preview-4x.png"
preview.save(preview_path)

manifest = {
    "schemaVersion": 1,
    "id": "linked-life-arc-family-v1",
    "runtimeReady": False,
    "identityCues": [
        "deep-brown skin",
        "coiled dark hair through teen and adult stages, with silver-white coils in elder-woman stage",
        "recurring sky-blue accent and small facial mark",
    ],
    "primaryLifeArc": ["infant-crawl", "toddler-waddle", "child-walk", "teen-walk", "young-adult-woman", "midlife-woman", "elder-woman"],
    "elderPresentationVariant": "elder-man",
    "directions": DIRECTIONS,
    "phases": PHASES,
    "frameSize": [24, 32],
    "pivot": [12, 31],
    "stages": stage_records,
    "frameCount": len(all_frames),
    "combinedAtlas": {"file": combined_path.name, "size": list(combined.size), "mode": "RGBA", "sha256": hashlib.sha256(combined_path.read_bytes()).hexdigest()},
    "preview": {"file": preview_path.name, "size": list(preview.size), "mode": "RGBA", "sha256": hashlib.sha256(preview_path.read_bytes()).hexdigest()},
    "limitations": [
        "This index links two independently generated early- and later-life batches; it proves coverage and visual motif intent, not frame-perfect identity continuity.",
        "Elder man is a related presentation variant, not the primary woman's own age-stage continuation.",
        "All frames remain concept art pending pixel-artist review, collision and timing authoring, renderer validation, and integration.",
    ],
}
(ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Built {len(all_frames)} frames across {len(stage_records)} stages.")
