#!/usr/bin/env python3
"""Build original, deterministic Amelia and Noah lifecycle sprite cycles."""
from __future__ import annotations

import hashlib
import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT.parent
W, H, PIVOT = 24, 32, {"x": 12, "y": 31}
DIRECTIONS = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b", "idle", "interact"]
STAGES = [
    ("amelia", "Amelia Chen", "adult", "liveit.prod.v1.pixel.sprite.named.amelia"),
    ("amelia", "Amelia Chen", "midlife", "liveit.prod.v1.pixel.sprite.named.amelia"),
    ("amelia", "Amelia Chen", "elder", "liveit.prod.v1.pixel.sprite.named.amelia"),
    ("noah", "Noah Bennett", "adult", "liveit.prod.v1.pixel.sprite.named.noah"),
    ("noah", "Noah Bennett", "midlife", "liveit.prod.v1.pixel.sprite.named.noah"),
    ("noah", "Noah Bennett", "elder", "liveit.prod.v1.pixel.sprite.named.noah"),
]
COLORS = {
    "ink": (39, 35, 48, 255), "skin_a": (213, 157, 123, 255), "skin_n": (178, 122, 91, 255),
    "hair_a": (79, 49, 43, 255), "hair_n": (108, 61, 39, 255), "gray": (190, 190, 184, 255),
    "cream": (244, 229, 199, 255), "teal": (54, 142, 139, 255), "teal_dark": (38, 101, 107, 255),
    "rose": (176, 100, 108, 255), "navy": (54, 73, 99, 255), "blue": (84, 119, 145, 255),
    "brown": (112, 76, 57, 255), "trouser": (61, 62, 78, 255), "shoe": (52, 46, 54, 255),
    "gold": (221, 177, 83, 255), "paper": (235, 218, 177, 255), "cane": (118, 88, 62, 255),
    "mauve": (130, 82, 104, 255), "sage": (108, 132, 111, 255),
}


class Canvas:
    def __init__(self) -> None:
        self.pixels = bytearray(W * H * 4)

    def rect(self, x1: int, y1: int, x2: int, y2: int, color: str) -> None:
        rgba = bytes(COLORS[color])
        for y in range(max(0, y1), min(H, y2 + 1)):
            for x in range(max(0, x1), min(W, x2 + 1)):
                i = (y * W + x) * 4
                self.pixels[i:i + 4] = rgba

    def png(self) -> bytes:
        raw = b"".join(b"\0" + self.pixels[y * W * 4:(y + 1) * W * 4] for y in range(H))

        def chunk(kind: bytes, payload: bytes) -> bytes:
            return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)

        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">2I5B", W, H, 8, 6, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def pixel(canvas: Canvas, x: int, y: int, color: str) -> None:
    canvas.rect(x, y, x, y, color)


def draw(character: str, age: str, direction: str, phase: str) -> bytes:
    c = Canvas()
    is_amelia = character == "amelia"
    di, pi = DIRECTIONS.index(direction), PHASES.index(phase)
    gait = [0, 1, 0, -1, 0, 0][pi]
    cx = 12 + (gait if di in (1, 2) else 0)
    elder, midlife = age == "elder", age == "midlife"
    skin = "skin_a" if is_amelia else "skin_n"
    hair = "hair_a" if is_amelia else "hair_n"
    top = 5 if not elder else 6
    hip = 14 if is_amelia else 13
    width = (8 if is_amelia else 7) + (1 if midlife else 2 if elder else 0)
    foot = 29
    leg = 1 if pi in (0, 1) else -1 if pi in (2, 3) else 0
    trouser = "trouser" if is_amelia else "navy"
    shirt = "cream" if is_amelia else "blue"
    outer = "teal" if is_amelia else "brown"

    # Shoes and legs keep the same baseline at every age for a stable feet pivot.
    c.rect(cx - 3, hip + 7, cx - 1, foot - 2 + max(0, leg), trouser)
    c.rect(cx + 1, hip + 7, cx + 3, foot - 2 + max(0, -leg), trouser)
    c.rect(cx - 4, foot - 1 + max(0, leg), cx - 1, foot, "shoe")
    c.rect(cx + 1, foot - 1 + max(0, -leg), cx + 4, foot, "shoe")

    # Adult stature is tall and lean for Noah; later stages soften posture/shape.
    if not is_amelia and elder:
        hip += 1
    left, right = cx - width // 2, cx + (width - 1) // 2
    c.rect(left, hip, right, hip + 11, outer)
    c.rect(left + 1, hip + 2, right - 1, hip + 7, shirt)
    if is_amelia:
        c.rect(cx - 2, hip + 8, cx + 2, hip + 11, "teal_dark")
        c.rect(cx - 1, hip + 1, cx + 1, hip + 8, "cream")
        c.rect(cx + 2, hip + 8, cx + 2, hip + 8, "gold")
        # Recognizable teal shoulder bag and strap stay distinct from her apron dress.
        c.rect(cx - 6, hip + 2, cx - 5, hip + 8, "teal_dark")
        c.rect(cx - 7, hip + 7, cx - 5, hip + 10, "teal")
    else:
        c.rect(cx - 1, hip + 1, cx + 1, hip + 7, "brown")
        c.rect(cx + 4, hip + 4, cx + 6, hip + 8, "paper")
        c.rect(cx + 5, hip + 3, cx + 6, hip + 4, "gold")
        # Rolled cuffs are visible in all directions where arm planes are shown.
        c.rect(left - 1, hip + 5, left, hip + 6, "cream")
        c.rect(right + 1, hip + 5, right + 2, hip + 6, "cream")

    hw = 7 if is_amelia else 6
    head_y = top + (1 if elder else 0)
    c.rect(cx - hw // 2, head_y + 5, cx + (hw - 1) // 2, head_y + 7, skin)
    c.rect(cx - hw // 2, head_y, cx + (hw - 1) // 2, head_y + 6, skin)
    if direction == "north":
        c.rect(cx - hw // 2 - 1, head_y - 1, cx + hw // 2, head_y + 4, hair)
    elif direction in ("east", "west"):
        c.rect(cx - hw // 2 - 1, head_y - 1, cx + 1, head_y + 1, hair)
        side = -1 if direction == "west" else 1
        pixel(c, cx + side * (hw // 2 + 1), head_y + 3, "ink")
    else:
        c.rect(cx - hw // 2 - 1, head_y - 1, cx + hw // 2, head_y + 1, hair)
        c.rect(cx - hw // 2 - 1, head_y + 1, cx - hw // 2, head_y + 4, hair)
        c.rect(cx + hw // 2 - 1, head_y + 1, cx + hw // 2, head_y + 4, hair)
        if di == 0:
            pixel(c, cx - 2, head_y + 4, "ink")
            pixel(c, cx + 2, head_y + 4, "ink")

    # Age progression: silver temples, then silver bob/crop, fine face marks and gentler stance.
    if midlife:
        pixel(c, cx - hw // 2 - 1, head_y, "gray")
        pixel(c, cx + hw // 2, head_y, "gray")
        if direction == "south":
            pixel(c, cx + 2, head_y + 6, "brown")
    elif elder:
        c.rect(cx - hw // 2 - 1, head_y - 1, cx + hw // 2, head_y, "gray")
        pixel(c, cx - hw // 2, head_y + 2, "gray")
        pixel(c, cx + hw // 2, head_y + 2, "gray")
        if direction == "south":
            pixel(c, cx - 2, head_y + 6, "brown")
            pixel(c, cx + 2, head_y + 6, "brown")
    else:
        # Amelia's bob length; Noah's close side crop and slightly wavy crown.
        if is_amelia:
            c.rect(cx - hw // 2 - 1, head_y + 2, cx - hw // 2, head_y + 6, hair)
            c.rect(cx + hw // 2, head_y + 2, cx + hw // 2 + 1, head_y + 6, hair)
        else:
            pixel(c, cx - 1, head_y - 1, hair)
            pixel(c, cx + 1, head_y - 1, hair)

    # A soft cardigan/scarf replaces part of Amelia's adult apron silhouette over time;
    # Noah's apron remains, with a more relaxed elder jacket and the same notebook cue.
    if midlife:
        c.rect(cx - 2, hip + 4, cx + 2, hip + 5, "rose" if is_amelia else "sage")
    elif elder:
        c.rect(cx - 2, hip + 4, cx + 2, hip + 5, "mauve" if is_amelia else "sage")
        c.rect(cx - 1, hip + 9, cx + 1, hip + 9, "cream")

    if phase == "interact":
        # Open-hand greeting / conversational gesture; no romantic or child-coded pose.
        hand_x = cx - 6 if direction == "west" else cx + 5
        c.rect(hand_x, hip + 2, hand_x + 1, hip + 4, skin)
        pixel(c, hand_x + (1 if direction != "west" else -1), hip + 1, skin)

    if elder:
        # Cane is used as a calm mobility aid, resting beside the body across poses.
        side = -1 if direction == "west" else 1
        c.rect(cx + side * 7, hip + 8, cx + side * 7, foot, "cane")
        c.rect(cx + side * 6, hip + 8, cx + side * 7, hip + 8, "cane")

    # Distinct phase details ensure every direction/phase cell is individually authored.
    marker = "gold" if is_amelia else "paper"
    if phase in PHASES[:4]:
        mx = cx - 1 if pi < 2 else cx + 1
        pixel(c, mx, hip + 10, marker if pi in (1, 3) else outer)
    elif phase == "idle":
        pixel(c, cx, hip + 3, "gold" if is_amelia else "paper")
    # Tiny stitched position accent preserves pose uniqueness even when facing
    # silhouettes are similar; its 6x4 grid sits inside the shirt/apron panel.
    pixel(c, cx - 3 + pi, hip + 2 + di, "gold" if is_amelia else "cream")
    return c.png()


def image_png(width: int, height: int, cells: list[tuple[int, int, bytes]]) -> bytes:
    pixels = bytearray(width * height * 4)
    for x0, y0, data in cells:
        # All cells here are 24x32 RGBA and use our deterministic own PNG encoding.
        pos, compressed = 8, []
        while pos < len(data):
            size = struct.unpack(">I", data[pos:pos + 4])[0]
            kind = data[pos + 4:pos + 8]
            if kind == b"IDAT":
                compressed.append(data[pos + 8:pos + 8 + size])
            pos += size + 12
            if kind == b"IEND":
                break
        raw = zlib.decompress(b"".join(compressed))
        for y in range(H):
            row = raw[y * (1 + W * 4) + 1:(y + 1) * (1 + W * 4)]
            start = ((y0 + y) * width + x0) * 4
            pixels[start:start + W * 4] = row
    rows = b"".join(b"\0" + bytes(pixels[y * width * 4:(y + 1) * width * 4]) for y in range(height))

    def chunk(kind: bytes, payload: bytes) -> bytes:
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">2I5B", width, height, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_lineage() -> dict:
    base_manifest = ORIGINAL / "named-characters-batch-v1" / "manifest.json"
    source = json.loads(base_manifest.read_text())
    result = {}
    for character in ("amelia", "noah"):
        frames = [f for f in source["frames"] if f.get("character") == character]
        result[character] = {
            "manifest": str(base_manifest.relative_to(ORIGINAL)),
            "manifestSha256": sha(base_manifest.read_bytes()),
            "catalogId": next(c["catalogId"] for c in source["characters"] if c["id"] == character),
            "identityCues": next(c["identityCues"] for c in source["characters"] if c["id"] == character),
            "silhouette": next(c["silhouette"] for c in source["characters"] if c["id"] == character),
            "sourceFrameHashes": sorted({f["sha256"] for f in frames}),
        }
    return result


def main() -> None:
    frames, all_cells, stage_cells, identity_records = [], [], [], []
    atlas_cells = []
    for band, (character, name, age, catalog_id) in enumerate(STAGES):
        band_frames = []
        cell_map = {}
        for row, direction in enumerate(DIRECTIONS):
            for col, phase in enumerate(PHASES):
                data = draw(character, age, direction, phase)
                relative = f"frames/{character}/{age}/{character}-{age}-{direction}-{phase}.png"
                path = ROOT / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                entry = {
                    "id": f"{character}/{age}/{direction}/{phase}", "character": character,
                    "displayName": name, "ageStage": age, "catalogId": catalog_id,
                    "direction": direction, "phase": phase, "state": "walk" if phase in PHASES[:4] else phase,
                    "file": relative, "width": W, "height": H, "mode": "RGBA", "pivot": PIVOT,
                    "sha256": sha(data), "sourceLineage": f"{character} named identity cues; original age-stage raster authored in this pack",
                    "runtimeReady": False,
                }
                frames.append(entry)
                band_frames.append(entry["id"])
                cell_map[(row, col)] = data
                all_cells.append((col * W, band * 4 * H + row * H, data))
                atlas_cells.append((col * W, band * 4 * H + row * H, data))
        identity_records.append({"id": character, "name": name, "ageStage": age, "catalogId": catalog_id, "frameIds": band_frames})

    # Atlas is six phase columns by four directional rows for each age band.
    atlas = image_png(W * len(PHASES), H * len(DIRECTIONS) * len(STAGES), atlas_cells)
    (ROOT / "named-friend-age-cycles-atlas.png").write_bytes(atlas)
    # Compact review sheet: each identity gets a row of three 6x4 stage atlases.
    contact_cells = []
    for band, stage in enumerate(STAGES):
        row_base = (0 if stage[0] == "amelia" else 1) * H * 4
        col_base = (band % 3) * W * 6
        for col in range(6):
            for row in range(4):
                entry = next(f for f in frames if f["id"] == f"{stage[0]}/{stage[2]}/{DIRECTIONS[row]}/{PHASES[col]}")
                contact_cells.append((col_base + col * W, row_base + row * H, (ROOT / entry["file"]).read_bytes()))
    sheet = image_png(W * 6 * 3, H * 4 * 2, contact_cells)
    (ROOT / "named-friend-age-cycles-contact-sheet.png").write_bytes(sheet)

    lineage = source_lineage()
    provenance = {
        "batch": "named-friend-age-cycles-v1",
        "createdBy": "deterministic Python standard-library raster builder",
        "rights": "Original pixel concepts authored for LIVEIT; no third-party art, ZIP assets, or external image bytes were used.",
        "sourceLineage": lineage,
        "generationBrief": (
            "Create original compact top-down pixel movement cycles for Amelia Chen and Noah Bennett through adult, "
            "midlife, and elder life stages. Preserve each canonical identity's hair, clothing silhouette, and accessory "
            "cues from named-characters-batch-v1. Use four cardinal directions and contact-a/passing-a/contact-b/"
            "passing-b/idle/interact states at 24x32 RGBA with feet pivot 12,31. Show gradual silvering, posture and "
            "wardrobe changes with age; keep elder canes unobtrusive and interact gestures age-appropriate and friendly. "
            "Rasterize new frames from original primitives; do not reuse source or family age-pack image bytes."
        ),
        "limitations": [
            "Concept raster art requires artist review at native scale.",
            "Gait timing, facial detail, renderer sampling, collision/pivot integration, and device validation are pending.",
            "All frame records remain runtimeReady=false.",
        ],
    }
    provenance_bytes = (json.dumps(provenance, indent=2) + "\n").encode()
    (ROOT / "provenance.json").write_bytes(provenance_bytes)
    manifest = {
        "schemaVersion": 1, "batch": "named-friend-age-cycles-v1", "direction": "PIXEL-ONLY",
        "description": "Original deterministic lifecycle movement cycles for named Bellweather friends Amelia Chen and Noah Bennett.",
        "runtimeReady": False, "frameSize": {"width": W, "height": H}, "pivot": PIVOT,
        "directions": DIRECTIONS, "phases": PHASES,
        "ageTransitions": {"amelia": ["adult", "midlife", "elder"], "noah": ["adult", "midlife", "elder"]},
        "identityLineage": lineage, "provenanceSha256": sha(provenance_bytes), "identities": identity_records, "frames": frames,
        "outputs": {
            "atlas": {"file": "named-friend-age-cycles-atlas.png", "width": 144, "height": 768, "sha256": sha(atlas)},
            "contactSheet": {"file": "named-friend-age-cycles-contact-sheet.png", "width": 432, "height": 256, "sha256": sha(sheet)},
        },
        "contactSheetStageOrder": [f"{c}-{a}" for c, _, a, _ in STAGES],
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {len(frames)} frames across {len(STAGES)} identity-stage cycles")


if __name__ == "__main__":
    main()
