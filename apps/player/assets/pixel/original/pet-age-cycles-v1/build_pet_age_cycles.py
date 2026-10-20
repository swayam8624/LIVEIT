#!/usr/bin/env python3
"""Build original pixel-cluster pet age movement studies.

The logical drawing canvas is 48x64 and is enlarged with nearest-neighbour
sampling to the 96x128 frame contract used by pet-walk-cycles-v1.  Every
direction is drawn from its own coordinate recipe; no directional bitmap is
mirrored at export time.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
LOGICAL = (48, 64)
FRAME = (96, 128)
PIVOT = {"x": 48, "y": 124}
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("contact-a", "passing-a", "contact-b", "passing-b")
AGES = ("young", "adult", "senior")
SPECIES = ("cat", "dog", "rabbit")

PALETTES = {
    "cat": {
        "outline": (38, 35, 45, 255), "body": (119, 105, 102, 255),
        "shadow": (78, 70, 76, 255), "light": (180, 161, 143, 255),
        "cream": (226, 205, 171, 255), "accent": (23, 119, 126, 255),
        "eye": (236, 177, 63, 255),
    },
    "dog": {
        "outline": (49, 37, 34, 255), "body": (157, 103, 69, 255),
        "shadow": (103, 65, 54, 255), "light": (201, 145, 97, 255),
        "cream": (229, 195, 151, 255), "accent": (183, 68, 65, 255),
        "eye": (58, 39, 31, 255),
    },
    "rabbit": {
        "outline": (51, 44, 61, 255), "body": (185, 155, 160, 255),
        "shadow": (120, 91, 111, 255), "light": (226, 196, 190, 255),
        "cream": (242, 219, 195, 255), "accent": (58, 132, 126, 255),
        "eye": (83, 49, 76, 255),
    },
}

AGE = {
    "young": {"scale": 0.74, "y": 2, "muted": False, "gait": 0},
    "adult": {"scale": 1.0, "y": 0, "muted": False, "gait": 0},
    "senior": {"scale": 0.94, "y": 1, "muted": True, "gait": 1},
}

PHASE_LEG = {"contact-a": (-3, 3), "passing-a": (-1, 1),
             "contact-b": (3, -3), "passing-b": (1, -1)}


def rgba(c):
    return c


def poly(d, pts, fill):
    d.polygon(pts, fill=fill)


def rect(d, box, fill):
    d.rectangle(box, fill=fill)


def ellipse(d, box, fill):
    x0, y0, x1, y1 = box
    d.ellipse((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)), fill=fill)


def line(d, pts, fill, width=1):
    d.line(pts, fill=fill, width=width, joint="curve")


def tone(p, key, age):
    c = p[key]
    if not AGE[age]["muted"] or key in ("outline", "accent", "eye"):
        return c
    # Senior coats are slightly desaturated while preserving species identity.
    return tuple(round(v * 0.88 + 192 * 0.12) for v in c[:3]) + (255,)


def draw_tail(d, p, species, age, direction, phase, cx, cy, s):
    col = tone(p, "body", age)
    sh = tone(p, "shadow", age)
    swing = {"contact-a": -2, "passing-a": 1, "contact-b": 3, "passing-b": -1}[phase]
    if species == "cat":
        if direction in ("south", "north"):
            pts = [(cx + 12, cy + 14), (cx + 16 + swing, cy + 5),
                   (cx + 14 + swing, cy - 7), (cx + 10 + swing, cy - 11),
                   (cx + 7, cy - 7), (cx + 11, cy + 3), (cx + 7, cy + 12)]
        else:
            side = -1 if direction == "west" else 1
            pts = [(cx - side * 9, cy + 5), (cx - side * 15, cy - 5),
                   (cx - side * (17 + swing), cy - 16),
                   (cx - side * (13 + swing), cy - 20),
                   (cx - side * 10, cy - 14), (cx - side * 12, cy - 5),
                   (cx - side * 5, cy + 7)]
        poly(d, pts, sh)
        line(d, pts[:4], col, 2)
    elif species == "dog":
        side = -1 if direction == "west" else 1
        if direction in ("south", "north"):
            pts = [(cx + 12, cy + 12), (cx + 17 + swing, cy + 6),
                   (cx + 17 + swing, cy - 5), (cx + 12, cy - 7),
                   (cx + 9, cy + 0), (cx + 7, cy + 9)]
        else:
            pts = [(cx - side * 10, cy + 7), (cx - side * 17, cy + 4),
                   (cx - side * (20 + swing), cy - 5),
                   (cx - side * (17 + swing), cy - 12),
                   (cx - side * 12, cy - 7), (cx - side * 6, cy + 7)]
        poly(d, pts, col)
        line(d, pts[:4], sh, 2)
    else:
        # Rabbit tail is a small, high-contrast puff visible behind the body.
        tail_shift = {"contact-a": -2, "passing-a": 0, "contact-b": 2, "passing-b": 1}[phase]
        if direction in ("south", "north"):
            ellipse(d, (cx + 9 + tail_shift, cy + 1, cx + 17 + tail_shift, cy + 9), tone(p, "cream", age))
        else:
            side = -1 if direction == "west" else 1
            ellipse(d, (cx - side * 17 - 3, cy + 1 + tail_shift, cx - side * 9 + 3, cy + 9 + tail_shift), tone(p, "cream", age))


def draw_legs(d, p, species, age, direction, phase, cx, foot_y, body_w, s):
    dark, sh, light = tone(p, "outline", age), tone(p, "shadow", age), tone(p, "light", age)
    a, b = PHASE_LEG[phase]
    if AGE[age]["gait"]:
        a = round(a * 0.65)
        b = round(b * 0.65)
    if direction in ("south", "north"):
        # Four separately rendered legs; front pair stays readable in south.
        xs = [cx - body_w // 3, cx - body_w // 7, cx + body_w // 7, cx + body_w // 3]
        for i, x in enumerate(xs):
            off = (a if i % 2 == 0 else b)
            legw = 4 if species == "rabbit" else 5
            if age == "young": legw = max(3, legw - 1)
            rect(d, (x - legw // 2 + off, foot_y - 13, x + legw // 2 + off, foot_y - 1), sh)
            rect(d, (x - legw // 2 + off, foot_y - 7, x + legw // 2 + off, foot_y - 1), light)
            rect(d, (x - legw // 2 + off, foot_y - 1, x + legw // 2 + off + 1, foot_y), dark)
    else:
        side = -1 if direction == "west" else 1
        xs = [cx - 10 * side, cx - 3 * side, cx + 5 * side, cx + 11 * side]
        for i, x in enumerate(xs):
            off = a if i in (0, 3) else b
            legw = 5 if species == "dog" else 4
            rect(d, (x - legw // 2, foot_y - 13 + off, x + legw // 2, foot_y - 1 + off), sh)
            rect(d, (x - legw // 2, foot_y - 4 + off, x + legw // 2 + 1, foot_y + off), light)
            rect(d, (x - legw // 2 - 1, foot_y + off, x + legw // 2 + 1, foot_y + 1 + off), dark)


def draw_front_back(d, p, species, age, direction, phase, s):
    sc = AGE[age]["scale"]
    cx = 24
    foot = 61 - AGE[age]["y"]
    body_w = round((14 if species == "rabbit" else 15 if species == "cat" else 17) * sc)
    body_h = round((22 if species == "rabbit" else 20 if species == "cat" else 19) * sc)
    cy = foot - body_h // 2 - 5
    draw_tail(d, p, species, age, direction, phase, cx, cy, sc)
    # Body silhouette and belly patch.
    ellipse(d, (cx - body_w, cy - body_h // 2, cx + body_w, cy + body_h // 2), tone(p, "outline", age))
    ellipse(d, (cx - body_w + 2, cy - body_h // 2 + 2, cx + body_w - 2, cy + body_h // 2 - 2), tone(p, "body", age))
    ellipse(d, (cx - body_w // 2, cy - 2, cx + body_w // 2, cy + body_h // 2 - 2), tone(p, "cream", age))
    draw_legs(d, p, species, age, direction, phase, cx, foot, body_w, sc)
    head_y = cy - body_h // 2 - (6 if species != "rabbit" else 8)
    hw = round((10 if species == "dog" else 9) * sc)
    hh = round((9 if species != "rabbit" else 8) * sc)
    ellipse(d, (cx - hw, head_y - hh, cx + hw, head_y + hh), tone(p, "outline", age))
    ellipse(d, (cx - hw + 2, head_y - hh + 2, cx + hw - 2, head_y + hh - 2), tone(p, "body", age))
    if species == "cat":
        poly(d, [(cx - hw + 1, head_y - 4), (cx - hw + 2, head_y - 14), (cx - 2, head_y - 8)], tone(p, "body", age))
        poly(d, [(cx + hw - 1, head_y - 4), (cx + hw - 2, head_y - 14), (cx + 2, head_y - 8)], tone(p, "body", age))
        rect(d, (cx - 7, head_y - 8, cx - 4, head_y - 4), tone(p, "light", age)); rect(d, (cx + 4, head_y - 8, cx + 7, head_y - 4), tone(p, "light", age))
    elif species == "rabbit":
        ear = tone(p, "body", age)
        poly(d, [(cx - 7, head_y - 5), (cx - 8, head_y - 25), (cx - 3, head_y - 29), (cx - 1, head_y - 7)], tone(p, "outline", age))
        poly(d, [(cx + 1, head_y - 7), (cx + 3, head_y - 29), (cx + 8, head_y - 25), (cx + 7, head_y - 5)], ear)
        line(d, [(cx - 5, head_y - 9), (cx - 5, head_y - 23)], tone(p, "light", age), 1)
        line(d, [(cx + 5, head_y - 9), (cx + 5, head_y - 23)], tone(p, "light", age), 1)
    else:
        # floppy ears make the dog silhouette distinct.
        poly(d, [(cx - hw + 2, head_y - 4), (cx - hw - 4, head_y + 8), (cx - 2, head_y + 5), (cx - 4, head_y - 6)], tone(p, "shadow", age))
        poly(d, [(cx + hw - 2, head_y - 4), (cx + hw + 4, head_y + 8), (cx + 2, head_y + 5), (cx + 4, head_y - 6)], tone(p, "shadow", age))
    # Face markings deliberately change with view, keeping each direction authored.
    if direction == "south":
        rect(d, (cx - 5, head_y - 1, cx - 2, head_y + 2), tone(p, "eye", age)); rect(d, (cx + 2, head_y - 1, cx + 5, head_y + 2), tone(p, "eye", age))
        ellipse(d, (cx - 2, head_y + 3, cx + 2, head_y + 6), tone(p, "outline", age))
    else:
        rect(d, (cx - 5, head_y - 1, cx - 2, head_y + 2), tone(p, "eye", age)); rect(d, (cx + 2, head_y - 1, cx + 5, head_y + 2), tone(p, "eye", age))
    # Collar, harness, or bandana remains the persistent identity cue.
    rect(d, (cx - body_w + 2, cy - body_h // 2 + 5, cx + body_w - 2, cy - body_h // 2 + 7), tone(p, "accent", age))
    if AGE[age]["muted"]:
        # Silver muzzle and one slower, lowered shoulder mark senior readability.
        ellipse(d, (cx - 5, head_y + 2, cx + 5, head_y + 7), tone(p, "light", age))
        rect(d, (cx - body_w + 3, cy + 4, cx - body_w + 5, cy + 8), tone(p, "light", age))


def draw_side(d, p, species, age, direction, phase, s):
    sc = AGE[age]["scale"]
    side = -1 if direction == "west" else 1
    foot = 61 - AGE[age]["y"]
    bw = round((18 if species == "dog" else 17 if species == "rabbit" else 16) * sc)
    bh = round((13 if species != "rabbit" else 15) * sc)
    cx, cy = 24, foot - bh - 9
    draw_tail(d, p, species, age, direction, phase, cx, cy, sc)
    ellipse(d, (cx - bw, cy - bh, cx + bw, cy + bh), tone(p, "outline", age))
    ellipse(d, (cx - bw + 2, cy - bh + 2, cx + bw - 2, cy + bh - 2), tone(p, "body", age))
    ellipse(d, (cx - 4, cy - 3, cx + 12, cy + bh - 2), tone(p, "cream", age))
    draw_legs(d, p, species, age, direction, phase, cx, foot, bw, sc)
    hx = cx + side * (bw - 1)
    hy = cy - 5
    hw = round((9 if species != "rabbit" else 8) * sc)
    hh = round((8 if species != "rabbit" else 7) * sc)
    ellipse(d, (hx - hw, hy - hh, hx + hw, hy + hh), tone(p, "outline", age))
    ellipse(d, (hx - hw + 2, hy - hh + 2, hx + hw - 2, hy + hh - 2), tone(p, "body", age))
    if species == "cat":
        poly(d, [(hx - side * 3, hy - 4), (hx - side * 2, hy - 14), (hx + side * 3, hy - 8)], tone(p, "body", age))
        poly(d, [(hx + side * 4, hy - 4), (hx + side * 6, hy - 13), (hx + side * 9, hy - 6)], tone(p, "body", age))
    elif species == "rabbit":
        poly(d, [(hx - side * 3, hy - 4), (hx - side * 3, hy - 25), (hx + side * 1, hy - 28), (hx + side * 3, hy - 5)], tone(p, "body", age))
        poly(d, [(hx + side * 1, hy - 5), (hx + side * 7, hy - 25), (hx + side * 10, hy - 21), (hx + side * 6, hy - 3)], tone(p, "body", age))
        line(d, [(hx - side * 1, hy - 8), (hx - side * 1, hy - 22)], tone(p, "light", age), 1)
    else:
        poly(d, [(hx - side * 3, hy - 4), (hx - side * 11, hy + 7), (hx - side * 5, hy + 8), (hx + side * 1, hy - 4)], tone(p, "shadow", age))
        poly(d, [(hx + side * 2, hy - 4), (hx + side * 11, hy + 6), (hx + side * 5, hy + 8), (hx, hy - 3)], tone(p, "shadow", age))
    # Authored one-eye and nose placement, with a species-specific muzzle.
    eye_x = hx + side * 3
    rect(d, (eye_x - 1, hy - 2, eye_x + 2, hy + 1), tone(p, "eye", age))
    poly(d, [(hx + side * (hw - 2), hy + 1), (hx + side * (hw + 4), hy + 3), (hx + side * (hw - 1), hy + 5)], tone(p, "cream", age))
    rect(d, (cx - 9, cy - bh + 4, cx + 10, cy - bh + 6), tone(p, "accent", age))
    if AGE[age]["muted"]:
        ellipse(d, (hx + side * 1, hy + 2, hx + side * 8, hy + 7), tone(p, "light", age))


def render(species, age, direction, phase):
    low = Image.new("RGBA", LOGICAL, (0, 0, 0, 0))
    d = ImageDraw.Draw(low)
    p = PALETTES[species]
    if direction in ("south", "north"):
        draw_front_back(d, p, species, age, direction, phase, AGE[age]["scale"])
    else:
        draw_side(d, p, species, age, direction, phase, AGE[age]["scale"])
    return low.resize(FRAME, Image.Resampling.NEAREST)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def build():
    if ROOT.exists():
        for child in ROOT.iterdir():
            if child.name == Path(__file__).name:
                continue
            if child.is_dir(): shutil.rmtree(child)
            else: child.unlink()
    frames_root = ROOT / "frames"
    frames_root.mkdir(parents=True, exist_ok=True)
    all_frames = []
    species_manifests = []
    combined_cols = len(SPECIES) * len(AGES) * len(PHASES)
    combined = Image.new("RGBA", (combined_cols * FRAME[0], len(DIRECTIONS) * FRAME[1]), (0, 0, 0, 0))
    for si, species in enumerate(SPECIES):
        species_dir = frames_root / species
        species_dir.mkdir(parents=True, exist_ok=True)
        atlas = Image.new("RGBA", (len(AGES) * len(PHASES) * FRAME[0], len(DIRECTIONS) * FRAME[1]), (0, 0, 0, 0))
        frames = []
        col = 0
        for age in AGES:
            for direction_i, direction in enumerate(DIRECTIONS):
                for phase_i, phase in enumerate(PHASES):
                    frame = render(species, age, direction, phase)
                    name = f"{species}-{age}-{direction}-{phase}.png"
                    path = species_dir / name
                    frame.save(path)
                    x = (AGES.index(age) * len(PHASES) + phase_i) * FRAME[0]
                    y = direction_i * FRAME[1]
                    atlas.paste(frame, (x, y))
                    cx = (si * len(AGES) * len(PHASES) + AGES.index(age) * len(PHASES) + phase_i) * FRAME[0]
                    combined.paste(frame, (cx, y))
                    frames.append({"id": name[:-4], "species": species, "age": age, "direction": direction,
                                   "phase": phase, "file": f"frames/{species}/{name}", "x": x, "y": y,
                                   "width": FRAME[0], "height": FRAME[1], "pivot": PIVOT,
                                   "sha256": sha(path), "runtimeReady": False,
                                   "limitations": ["Original pixel study; requires visual cleanup, timing, collision-box review, and renderer intake."]})
                    all_frames.append(frames[-1])
            col += len(PHASES)
        atlas_path = ROOT / f"{species}-age-cycles-atlas.png"
        atlas.save(atlas_path)
        preview = atlas.resize((atlas.width * 2, atlas.height * 2), Image.Resampling.NEAREST)
        preview_path = ROOT / f"{species}-age-cycles-preview-2x.png"
        preview.save(preview_path)
        source_path = ROOT / f"{species}-age-cycles-source.png"
        atlas.save(source_path)
        species_manifest = {"schemaVersion": 1, "assetId": f"liveit.pixel.pet.{species}.age-cycles.v1",
                            "species": species, "source": source_path.name, "atlas": {"file": atlas_path.name, "width": atlas.width, "height": atlas.height,
                            "columns": len(AGES) * len(PHASES), "rows": len(DIRECTIONS), "cellWidth": FRAME[0], "cellHeight": FRAME[1],
                            "order": "age groups young/adult/senior; phase columns contact-a/passing-a/contact-b/passing-b; direction rows south/west/east/north"},
                            "sampling": "nearest-neighbor", "forms": list(AGES), "frames": [f for f in frames], "runtimeReady": False,
                            "sourceSha256": sha(source_path), "atlasSha256": sha(atlas_path), "previewSha256": sha(preview_path)}
        save_json(ROOT / f"{species}-manifest.json", species_manifest)
        species_manifests.append(species_manifest)
    combined_path = ROOT / "all-pets-age-cycles-atlas.png"
    combined.save(combined_path)
    combined_preview = combined.resize((combined.width * 2, combined.height * 2), Image.Resampling.NEAREST)
    combined_preview_path = ROOT / "all-pets-age-cycles-preview-2x.png"
    combined_preview.save(combined_preview_path)
    manifest = {"schemaVersion": 1, "assetId": "liveit.pixel.pet.age-cycles.v1", "status": "original procedural pixel-art study",
                "frameSize": list(FRAME), "pivot": PIVOT, "species": list(SPECIES), "ages": list(AGES),
                "directions": list(DIRECTIONS), "phases": list(PHASES), "frameCount": len(all_frames),
                "logicalCanvas": list(LOGICAL), "sampling": "nearest-neighbor", "atlas": {"file": combined_path.name, "width": combined.width, "height": combined.height,
                "columns": combined_cols, "rows": len(DIRECTIONS), "cellWidth": FRAME[0], "cellHeight": FRAME[1]},
                "preview": combined_preview_path.name, "frames": all_frames, "runtimeReady": False,
                "sourcePolicy": "Original deterministic Pillow drawings; no supplied ZIPs, third-party sprites, or reference images used.",
                "sourceSha256": {f"{s}-age-cycles-source.png": sha(ROOT / f"{s}-age-cycles-source.png") for s in SPECIES},
                "atlasSha256": sha(combined_path), "previewSha256": sha(combined_preview_path)}
    save_json(ROOT / "manifest.json", manifest)
    save_json(ROOT / "frames.json", {"schemaVersion": 1, "frameCount": len(all_frames), "frames": all_frames, "runtimeReady": False})
    save_json(ROOT / "provenance.json", {"batch": manifest["assetId"], "createdBy": "deterministic local Pillow builder", "source": "procedural authored shapes on 48x64 logical canvas", "externalReferences": [], "license": "original work; no third-party source bytes", "runtimeReady": False})
    (ROOT / "README.md").write_text("""# Pet age movement cycles v1\n\nOriginal, deterministic pixel-cluster movement studies for cat, dog, and rabbit companions. Each species has young, adult, and senior forms; every form has authored south, west, east, and north directions with contact-a, passing-a, contact-b, and passing-b phases. This is 9 forms × 4 directions × 4 phases = 144 transparent RGBA frames.\n\nThe logical drawing canvas is 48×64 and is enlarged 2× with nearest-neighbour sampling to the existing 96×128 pet frame contract. Every frame uses the shared bottom pivot `(48,124)`. Directions are drawn from separate geometry recipes; no frame is mirror-flipped. Species identity persists through coat palette, silhouette, facial features, and collar/bandana/harness cues. Senior forms use reduced gait amplitude, silver muzzle accents, and lower posture.\n\nFiles include per-species atlases and previews, one combined review atlas, `frames/` with per-frame hashes in `manifest.json` and `frames.json`, and unmodified deterministic source sheets. `runtimeReady` is false everywhere: these are original concept studies requiring pixel cleanup, timing, collision-box review, renderer sampling, and human art direction.\n\nNo supplied ZIP files, third-party sprites, logos, or external reference images were used.\n""", encoding="utf-8")


if __name__ == "__main__":
    build()
    print("built pet-age-cycles-v1: 144 frames")
