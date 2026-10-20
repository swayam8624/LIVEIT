#!/usr/bin/env python3
"""Build original deterministic 24x32 Bellweather family age-cycle sprites."""
from __future__ import annotations

import hashlib
import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
W, H, PIVOT = 24, 32, [12, 31]
DIRECTIONS = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b", "idle", "interact"]
STAGES = [
    ("mara", "Mara Bellweather", "adult", "liveit.prod.v1.pixel.sprite.named.parent-one", "adult"),
    ("mara", "Mara Bellweather", "midlife", "liveit.prod.v1.pixel.sprite.named.parent-one", "midlife"),
    ("mara", "Mara Bellweather", "elder", "liveit.prod.v1.pixel.sprite.named.parent-one", "elder"),
    ("eli", "Eli Bellweather", "adult", "liveit.prod.v1.pixel.sprite.named.parent-two", "adult"),
    ("eli", "Eli Bellweather", "midlife", "liveit.prod.v1.pixel.sprite.named.parent-two", "midlife"),
    ("eli", "Eli Bellweather", "elder", "liveit.prod.v1.pixel.sprite.named.parent-two", "elder"),
    ("niko", "Niko Bellweather", "child", "liveit.prod.v1.pixel.sprite.named.sibling", "child"),
    ("niko", "Niko Bellweather", "teen", "liveit.prod.v1.pixel.sprite.named.sibling", "teen"),
    ("niko", "Niko Bellweather", "young-adult", "liveit.prod.v1.pixel.sprite.named.sibling", "young-adult"),
]

# Palette entries are purposefully constrained, with a shared base plus readable age cues.
PAL = {
    "ink": (47, 37, 42, 255), "skin_mara": (111, 65, 54, 255), "skin_eli": (160, 126, 91, 255),
    "skin_niko": (137, 76, 58, 255), "cream": (235, 218, 177, 255), "white": (245, 237, 214, 255),
    "rust": (163, 76, 53, 255), "rust_dark": (111, 52, 43, 255), "mustard": (220, 167, 57, 255),
    "navy": (46, 61, 82, 255), "navy_light": (67, 86, 110, 255), "ochre": (196, 139, 53, 255),
    "cobalt": (48, 92, 166, 255), "cobalt_light": (75, 126, 198, 255), "orange": (225, 119, 50, 255),
    "olive": (93, 103, 62, 255), "gray": (150, 157, 151, 255), "silver": (202, 205, 189, 255),
    "shoe": (57, 47, 49, 255), "shadow": (70, 47, 43, 255), "bag": (114, 82, 54, 255),
}

class Canvas:
    def __init__(self): self.p = bytearray(W * H * 4)
    def rect(self, x1, y1, x2, y2, color):
        c = PAL[color] if isinstance(color, str) else color
        for y in range(max(0, y1), min(H, y2 + 1)):
            for x in range(max(0, x1), min(W, x2 + 1)):
                i = (y * W + x) * 4; self.p[i:i+4] = bytes(c)
    def png(self):
        raw = b"".join(b"\0" + bytes(self.p[y*W*4:(y+1)*W*4]) for y in range(H))
        def chunk(kind, data): return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
        return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">2I5B", W, H, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")

def draw(identity, age, direction, phase):
    c = Canvas()
    move = {"contact-a": (0,0), "passing-a": (1,-1), "contact-b": (0,0), "passing-b": (-1,-1), "idle": (0,0), "interact": (0,0)}[phase]
    dx, dy = move
    # Balanced left/right stride alternation and a common feet pivot keep the cycle registered.
    leg = 1 if phase in ("contact-a", "passing-a") else -1 if phase in ("contact-b", "passing-b") else 0
    is_side = direction in ("west", "east")
    facing = direction == "south"
    if phase == "interact": dy = -1
    skin = {"mara":"skin_mara", "eli":"skin_eli", "niko":"skin_niko"}[identity]
    top = (8 if age == "elder" else 7) if identity != "niko" else {"child": 9, "teen": 7, "young-adult": 6}[age]
    height = 24 if identity != "niko" or age != "child" else 21
    # Lower body and shoes; older Mara/Eli have softer, wider silhouettes, Niko grows by stage.
    hip_y = top + (8 if identity != "niko" or age != "child" else 7)
    foot_y = 29
    bodyw = 10 if identity == "mara" else 8 if identity == "eli" else (7 if age == "child" else 8)
    if identity == "mara" and age == "elder": bodyw = 11
    if identity == "eli" and age == "elder": bodyw = 9
    if identity == "niko" and age == "young-adult": bodyw = 9
    cx = 12 + dx
    # legs/stride
    pants = "olive" if identity == "mara" else "navy" if identity == "eli" else "navy"
    if direction == "north":
        c.rect(cx-3, hip_y+6, cx-1, foot_y-2, pants); c.rect(cx+1, hip_y+6, cx+3, foot_y-2, pants)
    else:
        c.rect(cx-3, hip_y+6, cx-1, foot_y-2 + max(0, leg), pants)
        c.rect(cx+1, hip_y+6, cx+3, foot_y-2 + max(0, -leg), pants)
    c.rect(cx-4, foot_y-1+max(0,leg), cx-1, foot_y, "shoe")
    c.rect(cx+1, foot_y-1+max(0,-leg), cx+4, foot_y, "orange" if identity == "niko" else "shoe")
    # torso, stable color signature across age
    shirt = "rust" if identity == "mara" else "navy" if identity == "eli" else "cobalt"
    c.rect(cx-bodyw//2, hip_y, cx+(bodyw-1)//2, hip_y+11, shirt)
    c.rect(cx-bodyw//2+1, hip_y+10, cx+(bodyw-1)//2-1, hip_y+12, shirt)
    # arms follow facing and gesture; preserve accessory placement to retain identity.
    c.rect(cx-bodyw//2-2, hip_y+2, cx-bodyw//2, hip_y+8, shirt)
    c.rect(cx+(bodyw-1)//2+1, hip_y+2, cx+(bodyw-1)//2+2, hip_y+8, shirt)
    c.rect(cx-bodyw//2-2, hip_y+8, cx-bodyw//2, hip_y+9, skin)
    c.rect(cx+(bodyw-1)//2+1, hip_y+8, cx+(bodyw-1)//2+2, hip_y+9, skin)
    # head and neck. North-facing hair silhouette, side profiles and front features differ intentionally.
    headw = 8 if identity != "niko" or age != "child" else 7
    hy = top + dy
    c.rect(cx-2, hy+5, cx+2, hy+7, skin)
    c.rect(cx-headw//2, hy, cx+(headw-1)//2, hy+6, skin)
    if direction == "north":
        c.rect(cx-headw//2-1, hy-1, cx+(headw-1)//2+1, hy+2, "ink" if identity != "niko" or age != "elder" else "silver")
        c.rect(cx-2, hy+1, cx+2, hy+4, "ink" if identity != "niko" or age != "elder" else "silver")
    elif is_side:
        c.rect(cx-headw//2-1, hy-1, cx+1, hy+1, "ink" if identity != "niko" or age != "elder" else "silver")
        c.rect(cx-1, hy+3, cx+2, hy+3, skin)
        if direction == "west": c.rect(cx-2, hy+3, cx-2, hy+4, "ink")
        else: c.rect(cx+2, hy+3, cx+2, hy+4, "ink")
    else:
        hair = "ink" if identity != "niko" or age != "elder" else "silver"
        if identity == "mara":
            c.rect(cx-5, hy-1, cx+5, hy+2, hair); c.rect(cx-5, hy+2, cx-4, hy+5, hair); c.rect(cx+4, hy+2, cx+5, hy+5, hair)
            # tight natural curl clusters, unchanged silhouette cue across her aging stages
            for x,y in [(-4,-2),(-2,-2),(1,-2),(3,-2),(-5,0),(5,0),(-5,2),(5,2)]: c.rect(cx+x,hy+y,cx+x,hy+y,hair)
            if age == "midlife":
                c.rect(cx-5,hy,cx-5,hy+1,"silver"); c.rect(cx+4,hy-1,cx+5,hy-1,"silver")
            elif age == "elder":
                c.rect(cx-5,hy-1,cx-3,hy,"silver"); c.rect(cx+2,hy-1,cx+5,hy,"silver")
                c.rect(cx-5,hy+1,cx-5,hy+3,"silver"); c.rect(cx+5,hy+1,cx+5,hy+3,"silver")
        elif identity == "eli":
            c.rect(cx-4, hy-1, cx+4, hy+1, hair); c.rect(cx-4, hy+1, cx-3, hy+3, hair); c.rect(cx+3, hy+1, cx+4, hy+3, hair)
            if age == "elder": c.rect(cx-1,hy-1,cx+1,hy, "silver"); c.rect(cx-3,hy,cx-2,hy+1,"silver")
        else:
            # same curls and ponytail evolve in scale, never accessories or adult-coded cues while young
            c.rect(cx-4, hy-1, cx+4, hy+2, "ink"); c.rect(cx-4,hy+2,cx-3,hy+4,"ink"); c.rect(cx+3,hy+2,cx+4,hy+4,"ink")
            pony = 5 if age in ("child", "teen") else 4
            c.rect(cx+3,hy+2,cx+5,hy+pony,"ink"); c.rect(cx+4,hy+pony,cx+6,hy+pony+1,"ink")
        # eyes, expressive age marks; age-safe Niko remains neutral and fully clothed.
        if facing:
            eye = "ink"
            c.rect(cx-2, hy+3, cx-2, hy+3, eye); c.rect(cx+2, hy+3, cx+2, hy+3, eye)
            if age in ("midlife", "elder") and identity == "mara":
                c.rect(cx-3,hy+2,cx-1,hy+2,"rust_dark"); c.rect(cx+1,hy+2,cx+3,hy+2,"rust_dark")
                if age == "elder": c.rect(cx-1,hy+5,cx+1,hy+5,"rust_dark")
            if age == "elder" and identity == "eli":
                c.rect(cx-3,hy+2,cx+3,hy+2,"silver")
    # Clothing continuity and elder/teen aging signals.
    if identity == "mara":
        c.rect(cx-3,hip_y+1,cx+3,hip_y+2,"mustard")
        c.rect(cx+bodyw//2-1,hip_y+4,cx+bodyw//2+1,hip_y+10,"bag")
        if age == "elder": c.rect(cx-4,hip_y+7,cx+4,hip_y+8,"mustard")
        elif age == "midlife": c.rect(cx-1,hip_y+3,cx+1,hip_y+3,"cream")
    elif identity == "eli":
        c.rect(cx-1,hip_y+1,cx+1,hip_y+7,"ochre")
        # glasses remain the unmistakable face cue at adult and midlife; elder lens rims silvered.
        if facing:
            frame = "silver" if age == "elder" else "ink"
            c.rect(cx-4,hy+2,cx-1,hy+4,frame); c.rect(cx+1,hy+2,cx+4,hy+4,frame)
            c.rect(cx-1,hy+3,cx+1,hy+3,frame)
        if age == "elder": c.rect(cx-2,hip_y+9,cx+2,hip_y+10,"silver")
        elif age == "midlife": c.rect(cx-3,hip_y+10,cx+3,hip_y+10,"navy_light")
    else:
        # Hoodie, orange lace/shoe blocks, and backpack stay recognizable; growth changes proportions.
        c.rect(cx-3,hip_y+3,cx-2,hip_y+8,"cobalt_light")
        if direction == "north" or is_side:
            c.rect(cx-bodyw//2-1,hip_y+1,cx-bodyw//2+1,hip_y+4,"bag")
            c.rect(cx-bodyw//2,hip_y+3,cx-bodyw//2+2,hip_y+8,"ochre")
        if age == "teen":
            c.rect(cx+2,hip_y+1,cx+3,hip_y+2,"ochre") # small enamel pin, age-neutral
        if phase == "interact":
            # comic book shown at chest height, in child/teen/young-adult family scenes
            c.rect(cx+4,hip_y+3,cx+7,hip_y+7,"cream"); c.rect(cx+5,hip_y+4,cx+6,hip_y+6,"cobalt")
    # Elder Mara/Eli use a discreet walking cane only as a mobility cue in one hand.
    if age == "elder" and identity in ("mara", "eli"):
        side = -1 if direction == "west" else 1
        c.rect(cx+side*7,hip_y+7,cx+side*7,foot_y,"olive")
        c.rect(cx+side*7,hip_y+7,cx+side*8,hip_y+7,"olive")
    # Expose a phase-specific knee/hem pixel above overlapping coats so every authored
    # movement phase remains a real pose even on the fuller elder silhouettes.
    if phase in ("contact-a", "contact-b", "passing-a", "passing-b"):
        moving_x = cx - 2 if phase in ("contact-a", "passing-a") else cx + 2
        c.rect(moving_x, hip_y + 8, moving_x, hip_y + 8, "navy_light" if identity == "eli" else "olive" if identity == "mara" else "cobalt_light")
    return c.png()

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    frames, family_data = [], []
    for ident, name, age, catalog, biological in STAGES:
        stage_dir = ROOT / "frames" / ident / age
        stage_dir.mkdir(parents=True, exist_ok=True)
        stage_frames = []
        for di, direction in enumerate(DIRECTIONS):
            for phase in PHASES:
                data = draw(ident, biological, direction, phase)
                path = stage_dir / f"{ident}-{age}-{direction}-{phase}.png"
                path.write_bytes(data)
                frame = {"id": f"{ident}/{age}/{direction}/{phase}", "character": ident, "displayName": name,
                         "ageStage": age, "catalogId": catalog, "direction": direction, "phase": phase,
                         "file": path.relative_to(ROOT).as_posix(), "width": W, "height": H, "mode": "RGBA",
                         "pivot": {"x": 12, "y": 31}, "sha256": sha(path), "runtimeReady": False,
                         "sourceLineage": "originally rasterized by this builder; identity cues/catalog mapping reference named-family-batch-v1, named-characters-batch-v1, and named-characters-batch-v2"}
                frames.append(frame); stage_frames.append(frame)
        # contact atlas: rows directions; columns movement phases, idle, interact
        atlas = Canvas()
        # separate atlas has its own arbitrary 144x128 RGBA encoder below
        family_data.append({"id": ident, "name": name, "ageStage": age, "catalogId": catalog,
                            "frameIds": [f["id"] for f in stage_frames], "runtimeReady": False})
    # Build full atlas (9 family-stage bands, 4 rows x 6 columns) and a labeled-free review sheet.
    atlas_png(6*W, len(STAGES)*4*H, frames, ROOT / "named-family-age-cycles-atlas.png")
    atlas_png(6*W*3, 4*H*3, frames, ROOT / "named-family-age-cycles-contact-sheet.png", contact=True)
    manifest = {"schemaVersion": 1, "batch": "named-family-age-cycles-v1", "direction": "PIXEL-ONLY",
                "description": "Original, deterministic named Bellweather family aging and movement concept pack.",
                "runtimeReady": False, "frameSize": {"width":W,"height":H}, "pivot":{"x":12,"y":31},
                "directions": DIRECTIONS, "phases": PHASES,
                "ageTransitions":{"mara":["adult","midlife","elder"],"eli":["adult","midlife","elder"],"niko":["child","teen","young-adult"]},
                "identities": family_data, "frames": frames,
                "outputs": {"atlas":{"file":"named-family-age-cycles-atlas.png","size":[144,1152],"sha256":sha(ROOT/"named-family-age-cycles-atlas.png")},
                            "contactSheet":{"file":"named-family-age-cycles-contact-sheet.png","size":[432,384],"sha256":sha(ROOT/"named-family-age-cycles-contact-sheet.png")}},
                "sourceLineage": {"package":"named-family-batch-v1 + named-characters-batch-v1 + named-characters-batch-v2",
                                  "meaning":"Only names, roles, catalog IDs and identity cues are referenced. All age-stage frames are independently rasterized by this builder; no source PNG bytes are embedded or copied.",
                                  "sourceFiles":[
                                      {"file":"../named-family-batch-v1/characters.json","sha256":sha(ROOT.parent/"named-family-batch-v1"/"characters.json")},
                                      {"file":"../named-family-batch-v1/frames.json","sha256":sha(ROOT.parent/"named-family-batch-v1"/"frames.json")},
                                      {"file":"../named-characters-batch-v1/manifest.json","sha256":sha(ROOT.parent/"named-characters-batch-v1"/"manifest.json")},
                                      {"file":"../named-characters-batch-v2/manifest.json","sha256":sha(ROOT.parent/"named-characters-batch-v2"/"manifest.json")}]}}
    (ROOT/"manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    provenance = {"package":"named-family-age-cycles-v1", "created":"2026-10-20", "creator":"Codex assisted deterministic procedural pixel-art builder",
                  "rights":"Original project working material generated from repository-authored character descriptions; no third-party ZIP, external image, or game artwork used.",
                  "prompt":"Create an original top-down retro pixel family movement-cycle set for Mara Bellweather (adult, midlife, elder), Eli Bellweather (adult, midlife, elder), and Niko Bellweather (child, teen, young adult). Preserve recognizable canonical cues: Mara's natural curls, rust clothing, mustard scarf and tote; Eli's close-cropped hair, glasses, navy work jacket and ochre shirt; Niko's curls/ponytail, cobalt hoodie, orange shoes and backpack. Show visible age progression through posture, height/proportions, hair greying/wrinkles where appropriate, and clothing fit/details. For each identity-stage create four authored cardinal facings, four distinct walk-cycle phases plus neutral idle and friendly age-safe interact. Niko is fully clothed and non-romantic in every stage. Transparent 24x32 RGBA, crisp limited-palette pixels, common feet pivot at (12,31), no text, logos, perspective shadows, 3D, external art or copied assets.",
                  "builder":"build_age_cycles.py", "runtimeReady":False,
                  "limitations":["Procedural sprite concepts need artist review and motion cleanup.","Niko's young-adult stage is a modest age progression from the child signature, not a different person.","Not mapped into runtime atlas loading; catalog IDs are references only."]}
    (ROOT/"provenance.json").write_text(json.dumps(provenance, indent=2)+"\n")

def atlas_png(width, height, frames, path, contact=False):
    # Construct RGBA PNG without third-party libraries; transparent gaps are intentional.
    pixels = bytearray(width*height*4)
    ordered = frames
    bands = []
    for i in range(0,len(ordered),24): bands.append(ordered[i:i+24])
    if contact:
        for n, band in enumerate(bands):
            bx=(n%3)*6*W; by=(n//3)*4*H
            for frame in band:
                col=PHASES.index(frame["phase"]); row=DIRECTIONS.index(frame["direction"])
                raw=(ROOT/frame["file"]).read_bytes(); rgba=decode_rgba(raw)
                paste(pixels,width,height,rgba,(bx+col*W,by+row*H))
    else:
        for n, band in enumerate(bands):
            for frame in band:
                col=PHASES.index(frame["phase"]); row=DIRECTIONS.index(frame["direction"])
                raw=(ROOT/frame["file"]).read_bytes(); rgba=decode_rgba(raw)
                paste(pixels,width,height,rgba,(col*W,(n*4+row)*H))
    raw=b"".join(b"\0"+bytes(pixels[y*width*4:(y+1)*width*4]) for y in range(height))
    def chunk(k,d): return struct.pack(">I",len(d))+k+d+struct.pack(">I",zlib.crc32(k+d)&0xffffffff)
    data=b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">2I5B",width,height,8,6,0,0,0))+chunk(b"IDAT",zlib.compress(raw,9))+chunk(b"IEND",b"")
    path.write_bytes(data)

def decode_rgba(data):
    # The builder's own PNG encoder uses filter 0 and one IDAT stream.
    i=8; chunks=[]
    while i<len(data):
        n=struct.unpack(">I",data[i:i+4])[0]; typ=data[i+4:i+8]; payload=data[i+8:i+8+n]; i+=12+n
        if typ==b"IDAT": chunks.append(payload)
        if typ==b"IEND": break
    raw=zlib.decompress(b"".join(chunks)); out=bytearray(W*H*4)
    for y in range(H): out[y*W*4:(y+1)*W*4]=raw[y*(W*4+1)+1:(y+1)*(W*4+1)]
    return out

def paste(dst,dw,dh,src,pos):
    x,y=pos
    for row in range(H):
        a=((y+row)*dw+x)*4; b=row*W*4; dst[a:a+W*4]=src[b:b+W*4]

if __name__ == "__main__": main()
