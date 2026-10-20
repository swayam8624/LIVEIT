#!/usr/bin/env python3
"""Build original, deterministic mobility-diverse movement concept sprites."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
FRAME_SIZE = (32, 40)
PIVOT = (16, 39)
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("contact-a", "passing-a", "contact-b", "passing-b")
POSES = ("idle", "interact")

CHARACTERS = {
    "rhea-powered": {
        "label": "Rhea, adult powered-wheelchair user",
        "skin": (145, 82, 65, 255), "hair": (50, 34, 37, 255),
        "shirt": (54, 132, 155, 255), "accent": (246, 184, 77, 255),
        "chair": (47, 56, 74, 255), "metal": (107, 133, 151, 255),
        "wheel": (31, 35, 48, 255), "notes": "teal jacket, gold scarf, powered joystick pod",
    },
    "samir-manual": {
        "label": "Samir, senior manual-wheelchair user",
        "skin": (112, 72, 50, 255), "hair": (185, 185, 176, 255),
        "shirt": (126, 74, 128, 255), "accent": (240, 182, 111, 255),
        "chair": (58, 69, 75, 255), "metal": (137, 157, 161, 255),
        "wheel": (28, 34, 39, 255), "notes": "silver hair, plum cardigan, manual push rims, cane hook",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def px(d: ImageDraw.ImageDraw, box, color):
    d.rectangle(box, fill=color)


def draw_frame(character: str, direction: str, state: str, phase: str | None) -> Image.Image:
    c = CHARACTERS[character]
    im = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # Every direction is authored separately. Small phase offsets imply momentum,
    # while chair wheel/hand placement makes each frame visibly distinct.
    phase_i = PHASES.index(phase) if phase else 0
    moving = phase is not None
    bob = (0, -1, 0, 1)[phase_i] if moving else 0
    reach = 1 if state == "interact" else 0
    skin, hair, shirt, accent = c["skin"], c["hair"], c["shirt"], c["accent"]
    chair, metal, wheel = c["chair"], c["metal"], c["wheel"]
    if direction in ("south", "north"):
        # Front/back view: broad chair back, two independent wheels, compact torso.
        y = 14 + bob
        px(d, (8, y + 13, 23, y + 22), chair)
        px(d, (6, y + 17, 9, y + 30), wheel)
        px(d, (22, y + 17, 25, y + 30), wheel)
        px(d, (7, y + 18, 8, y + 27), metal)
        px(d, (23, y + 18, 24, y + 27), metal)
        px(d, (10, y + 10, 21, y + 19), metal)
        px(d, (11, y + 9, 20, y + 17), shirt)
        # Head shape and hair/face orientation are deliberately not mirrored.
        px(d, (12, y + 2, 19, y + 9), skin)
        if direction == "south":
            px(d, (12, y + 1, 19, y + 3), hair)
            px(d, (11, y + 3, 12, y + 6), hair)
            px(d, (19, y + 4, 20, y + 6), skin)
            px(d, (13, y + 6, 14, y + 6), (44, 36, 39, 255))
            px(d, (17, y + 6, 18, y + 6), (44, 36, 39, 255))
        else:
            px(d, (12, y + 1, 19, y + 3), hair)
            px(d, (11, y + 3, 13, y + 8), hair)
            px(d, (18, y + 3, 20, y + 8), hair)
        # Shoulder accent and controls.
        px(d, (10, y + 10, 12, y + 12), accent)
        px(d, (19, y + 10, 21, y + 12), accent)
        px(d, (20, y + 14, 22, y + 16), accent if character == "rhea-powered" else metal)
        if direction == "south":
            # hands/push rim (manual) or joystick reach (powered)
            if character == "rhea-powered": px(d, (21 + reach, y + 13, 23 + reach, y + 14), skin)
            else: px(d, (7, y + 14, 9, y + 15), skin)
    else:
        # Side view: chair depth, large wheel and explicit user/chair silhouette.
        y = 14 + bob
        facing_east = direction == "east"
        wheel_x = 19 if facing_east else 10
        body_x = 13 if facing_east else 11
        px(d, (wheel_x - 5, y + 16, wheel_x + 5, y + 27), wheel)
        px(d, (wheel_x - 3, y + 18, wheel_x + 3, y + 25), metal)
        px(d, (body_x - 2, y + 11, body_x + 4, y + 19), chair)
        px(d, (body_x - 3, y + 16, body_x + 5, y + 20), shirt)
        px(d, (body_x - 1, y + 3, body_x + 5, y + 10), skin)
        if facing_east:
            px(d, (body_x + 3, y + 2, body_x + 6, y + 5), hair)
            px(d, (body_x + 5, y + 6, body_x + 6, y + 7), skin)
            px(d, (body_x + 5 + reach, y + 12, body_x + 7 + reach, y + 14), skin)
            px(d, (wheel_x + 5, y + 12, wheel_x + 8, y + 14), metal)
        else:
            px(d, (body_x - 3, y + 2, body_x + 1, y + 5), hair)
            px(d, (body_x - 4, y + 6, body_x - 3, y + 7), skin)
            px(d, (body_x - 5 - reach, y + 12, body_x - 3 - reach, y + 14), skin)
            px(d, (wheel_x - 8, y + 12, wheel_x - 5, y + 14), metal)
        px(d, (body_x - 2, y + 13, body_x, y + 14), accent)
        # Manual user reaches push rim during alternating passing frames.
        if character == "samir-manual" and moving and phase_i in (1, 3):
            px(d, (wheel_x - 1, y + 15, wheel_x + 2, y + 16), skin)
        if character == "samir-manual" and state == "interact":
            # Cane hook stored beside the chair, with a hand reaching to it.
            cane_x = wheel_x + 7 if facing_east else wheel_x - 7
            px(d, (min(cane_x, cane_x + 1), y + 9, max(cane_x, cane_x + 1), y + 25), metal)
            px(d, (cane_x - 1, y + 8, cane_x + 2, y + 9), accent)
    if moving:
        # A four-step wheel highlight gives each authored phase a unique
        # contact/passing read without relying on mirrored geometry.
        px(d, (7 + phase_i * 5, y + 23, 8 + phase_i * 5, y + 23), metal)
    # Ground contact pixels keep the pivot visually stable.
    px(d, (6, 38, 25, 39), (23, 27, 36, 150))
    return im


def write_frames() -> list[dict]:
    all_frames: list[dict] = []
    frames_root = ROOT / "frames"
    for character in CHARACTERS:
        char_dir = frames_root / character
        char_dir.mkdir(parents=True, exist_ok=True)
        atlas = Image.new("RGBA", (FRAME_SIZE[0] * 4, FRAME_SIZE[1] * 4), (0, 0, 0, 0))
        pose_atlas = Image.new("RGBA", (FRAME_SIZE[0] * 4, FRAME_SIZE[1] * 2), (0, 0, 0, 0))
        for row, direction in enumerate(DIRECTIONS):
            for col, phase in enumerate(PHASES):
                im = draw_frame(character, direction, "idle", phase)
                filename = f"{character}-{direction}-{phase}.png"
                path = char_dir / filename
                im.save(path, "PNG", optimize=False)
                atlas.alpha_composite(im, (col * FRAME_SIZE[0], row * FRAME_SIZE[1]))
                all_frames.append({"id": f"{character}/{direction}/{phase}", "character": character, "direction": direction, "phase": phase, "kind": "movement", "file": f"frames/{character}/{filename}", "size": list(FRAME_SIZE), "pivot": list(PIVOT), "sha256": sha256(path), "runtimeReady": False})
            for col, state in enumerate(POSES):
                im = draw_frame(character, direction, state, None)
                filename = f"{character}-{direction}-{state}.png"
                path = char_dir / filename
                im.save(path, "PNG", optimize=False)
                pose_atlas.alpha_composite(im, (col * FRAME_SIZE[0], row * FRAME_SIZE[1]))
                all_frames.append({"id": f"{character}/{direction}/{state}", "character": character, "direction": direction, "state": state, "kind": "pose", "file": f"frames/{character}/{filename}", "size": list(FRAME_SIZE), "pivot": list(PIVOT), "sha256": sha256(path), "runtimeReady": False})
        atlas.save(ROOT / f"{character}-movement-atlas-4x4.png", "PNG", optimize=False)
        pose_atlas.save(ROOT / f"{character}-pose-atlas-4x2.png", "PNG", optimize=False)
        combined = Image.new("RGBA", (FRAME_SIZE[0] * 4, FRAME_SIZE[1] * 6), (0, 0, 0, 0))
        combined.alpha_composite(atlas, (0, 0)); combined.alpha_composite(pose_atlas, (0, FRAME_SIZE[1] * 4))
        combined.save(ROOT / f"{character}-combined-atlas-4x6.png", "PNG", optimize=False)
    return all_frames


def main() -> None:
    frames = write_frames()
    combined = Image.new("RGBA", (FRAME_SIZE[0] * 8, FRAME_SIZE[1] * 6), (0, 0, 0, 0))
    for i, character in enumerate(CHARACTERS):
        combined.alpha_composite(Image.open(ROOT / f"{character}-combined-atlas-4x6.png"), (i * FRAME_SIZE[0] * 4, 0))
    combined.save(ROOT / "mobility-diverse-cycles-atlas-8x6.png", "PNG", optimize=False)
    combined.resize((combined.width * 4, combined.height * 4), Image.Resampling.NEAREST).save(ROOT / "mobility-diverse-cycles-preview-4x.png", "PNG", optimize=False)
    manifest = {"schemaVersion": 1, "id": "mobility-diverse-cycles-v1", "runtimeReady": False, "frameSize": list(FRAME_SIZE), "pivot": list(PIVOT), "directions": list(DIRECTIONS), "phases": list(PHASES), "poseStates": list(POSES), "characters": [{"id": k, "label": v["label"], "mobilityRepresentation": v["notes"], "movementFrameCount": 16, "poseFrameCount": 8, "runtimeReady": False} for k, v in CHARACTERS.items()], "frames": frames, "derivedOutputs": [{"file": p.name, "sha256": sha256(p)} for p in ROOT.glob("*.png")], "provenance": {"source": "original deterministic Pillow pixel clusters", "thirdPartyAssets": False, "externalReferenceImages": False, "commercialLicense": "not applicable to authored pixels"}}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (ROOT / "provenance.json").write_text(json.dumps({"batch": manifest["id"], "method": "hand-authored geometric pixel clusters", "sourceMaterials": [], "runtimeReady": False}, indent=2) + "\n", encoding="utf-8")
    (ROOT / "README.md").write_text("""# Mobility-diverse cycles v1\n\nOriginal deterministic concept sprites for two adult characters: Rhea uses a powered wheelchair and Samir uses a manual wheelchair. Each has four independently authored cardinal directions, four locomotion phases, and idle/interact poses (48 frames per character; 96 total). The 32×40 logical canvas uses pivot `(16,39)`, transparent RGBA output, and nearest-neighbour review atlases. Chair geometry is part of each silhouette; side views include wheel/rim mechanics, while interaction poses operate the controls or reach for a cane.\n\nNo supplied ZIP, third-party sprite, logo, or external reference image was used. `runtimeReady` is false pending pixel-art cleanup, palette review, collision/pivot checks, renderer import, and human visual approval.\n""", encoding="utf-8")


if __name__ == "__main__":
    main()
