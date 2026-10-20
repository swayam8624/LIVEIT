"""Deterministic, original pixel movement batch for named catalog families."""
from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path
from typing import Any
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
SIZE = (24, 32)
PIVOT = (12, 31)
DIRECTIONS = ("south", "west", "east", "north")
PHASES = ("contact-a", "passing-a", "contact-b", "passing-b")
POSES = ("idle", "interact")
COLUMNS = (*PHASES, *POSES)

FAMILIES: tuple[dict[str, Any], ...] = (
    {"id":"sibling", "catalogId":"liveit.prod.v1.pixel.sprite.named.sibling", "name":"Niko", "role":"school-age sibling", "ageStage":"child", "height":22, "skin":"9a603f", "skinHi":"c68158", "shadow":"673c38", "hair":"2b1d2b", "hairHi":"553347", "top":"2458a6", "topHi":"4e8bd1", "bottom":"3a394c", "shoe":"e27635", "shoeHi":"f4a149", "accent":"f19a3f", "prop":"backpack", "identity":["curly ponytail","cobalt hoodie","orange sneakers","backpack"], "interaction":"shares a small comic book"},
    {"id":"partner", "catalogId":"liveit.prod.v1.pixel.sprite.named.partner", "name":"Nora", "role":"adult partner", "ageStage":"adult", "height":28, "skin":"7b4d43", "skinHi":"b87962", "shadow":"4a3037", "hair":"20243a", "hairHi":"4e5e83", "top":"873f62", "topHi":"c66d82", "bottom":"303e58", "shoe":"1e263d", "shoeHi":"536b8f", "accent":"e5bb6e", "prop":"ring", "identity":["short indigo bob","rose overshirt","cream ring","wide-leg trousers"], "interaction":"offers a ringed hand and letter"},
    {"id":"child", "catalogId":"liveit.prod.v1.pixel.sprite.named.child", "name":"Tavi", "role":"young child", "ageStage":"child", "height":21, "skin":"d39a70", "skinHi":"f1bd8d", "shadow":"8d5b55", "hair":"63432e", "hairHi":"9b6b3c", "top":"6a9b43", "topHi":"acd265", "bottom":"7654a0", "shoe":"503a70", "shoeHi":"9d79ca", "accent":"e4c65c", "prop":"kite", "identity":["purple cap","leaf-green overalls","violet boots","yellow kite spool"], "interaction":"shows a bright kite spool"},
    {"id":"grandparent", "catalogId":"liveit.prod.v1.pixel.sprite.named.grandparent", "name":"Dadi", "role":"grandparent", "ageStage":"senior", "height":25, "skin":"744941", "skinHi":"ad7060", "shadow":"473139", "hair":"c0bac0", "hairHi":"eee2df", "top":"714b70", "topHi":"a982a3", "bottom":"4a415a", "shoe":"3b3343", "shoeHi":"786578", "accent":"91aa7b", "prop":"cane", "identity":["silver bun","plum cardigan","sage cane","round spectacles"], "interaction":"steadies a cane and framed photo"},
    {"id":"mentor", "catalogId":"liveit.prod.v1.pixel.sprite.named.mentor", "name":"Ishan", "role":"career mentor", "ageStage":"midlife", "height":27, "skin":"9a6d4d", "skinHi":"d49d6c", "shadow":"5c4037", "hair":"302d31", "hairHi":"777071", "top":"344d67", "topHi":"6688a1", "bottom":"2f3645", "shoe":"252936", "shoeHi":"5b657a", "accent":"d8ad56", "prop":"notebook", "identity":["silver-streak hair","indigo vest","gold glasses","notebook"], "interaction":"opens a notebook plan"},
)

def color(value: str) -> tuple[int,int,int,int]:
    return tuple(int(value[i:i+2], 16) for i in (0,2,4)) + (255,)

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def r(draw: ImageDraw.ImageDraw, box: tuple[int,int,int,int], value: str | tuple[int,int,int,int]) -> None:
    draw.rectangle(box, fill=color(value) if isinstance(value, str) else value)

def poly(draw: ImageDraw.ImageDraw, points: list[tuple[int,int]], value: str | tuple[int,int,int,int]) -> None:
    draw.polygon(points, fill=color(value) if isinstance(value, str) else value)

def draw_frame(p: dict[str, Any], direction: str, mode: str, phase: int) -> Image.Image:
    im = Image.new("RGBA", SIZE, (0,0,0,0)); d = ImageDraw.Draw(im)
    out = color("1c2030"); move = mode == "move"; reach = mode == "interact"
    bob = (-1,0,1,0)[phase % 4] if move else (-1 if reach else 0)
    gait = (-2,1,2,-1)[phase % 4] if move else 0
    top = 30 - p["height"] + bob; child = p["id"] in {"sibling","child"}; senior = p["id"] == "grandparent"
    # Each cardinal branch has its own geometry; no image mirroring is used.
    if direction == "south":
        x0,x1,y = 8,15,top; r(d,(x0-1,y+1,x1+1,y+7),out); r(d,(x0,y+1,x1,y+6),p["skin"]); r(d,(x0+1,y+1,x1-1,y+2),p["skinHi"]); r(d,(x0,y,x1,y+1),p["hair"]); r(d,(x0,y+2,x0+1,y+4),p["hair"]); r(d,(x1-1,y+2,x1,y+4),p["hairHi"])
        if p["id"] == "sibling": r(d,(x1+1,y+1,x1+3,y+4),p["hair"]); r(d,(x1+2,y+3,x1+3,y+5),p["hairHi"])
        if p["id"] == "child": r(d,(x0-1,y-1,x1+1,y),p["accent"])
        if p["id"] == "grandparent": r(d,(x0+1,y-1,x1-1,y),p["hairHi"])
    elif direction == "west":
        x,y = 8,top; r(d,(x-1,y+1,x+6,y+7),out); r(d,(x,y+1,x+5,y+6),p["skin"]); r(d,(x,y,x+3,y+2),p["hair"]); r(d,(x+1,y,x+5,y+1),p["hairHi"]); r(d,(x-2,y+3,x,y+4),p["skinHi"])
        if p["id"] in {"child","grandparent"}: r(d,(x+1,y-1,x+4,y),p["accent"] if p["id"] == "child" else p["hairHi"])
    elif direction == "east":
        x,y = 10,top; r(d,(x-1,y+1,x+6,y+7),out); r(d,(x,y+1,x+5,y+6),p["skin"]); r(d,(x+2,y,x+5,y+2),p["hair"]); r(d,(x,y,x+4,y+1),p["hairHi"]); r(d,(x+5,y+3,x+7,y+4),p["skinHi"])
        if p["id"] == "sibling": r(d,(x-2,y+1,x,y+4),p["hair"])
        if p["id"] in {"child","grandparent"}: r(d,(x+1,y-1,x+4,y),p["accent"] if p["id"] == "child" else p["hairHi"])
    else:
        x0,x1,y = 8,15,top; r(d,(x0-1,y+1,x1+1,y+7),out); r(d,(x0,y,x1,y+6),p["hair"]); r(d,(x0+1,y+1,x1-1,y+2),p["hairHi"]); r(d,(x0+1,y+4,x1-1,y+6),p["hair"])
        if p["id"] == "sibling": r(d,(x1+1,y+1,x1+3,y+5),p["hair"])
        if p["id"] == "child": r(d,(x0-1,y-1,x1+1,y),p["accent"])
        if p["id"] == "grandparent": r(d,(x0+2,y-1,x1-2,y),p["hairHi"])
    torso = top+7; width = 7 if child else 8; left,right = 12-width//2,12+width//2
    if p["id"] == "partner": poly(d,[(left-1,torso),(right+1,torso),(right+2,torso+10),(left-2,torso+10)],out); poly(d,[(left,torso+1),(right,torso+1),(right+1,torso+9),(left-1,torso+9)],p["top"])
    else: r(d,(left-1,torso,right+1,torso+10),out); r(d,(left,torso+1,right,torso+9),p["top"])
    r(d,(left+1,torso+1,right-1,torso+2),p["topHi"])
    if p["id"] == "sibling":
        if direction == "south": r(d,(right-1,torso+3,right+2,torso+8),p["accent"])
        elif direction == "west": r(d,(left-2,torso+3,left,torso+8),p["accent"])
        elif direction == "east": r(d,(right,torso+3,right+2,torso+8),p["accent"])
        else: r(d,(left-1,torso+3,left+2,torso+8),p["accent"])
    elif p["id"] == "partner": r(d,(left+1,torso+1,right-1,torso+2),p["accent"])
    elif p["id"] == "child": r(d,(left+2,torso+3,left+3,torso+7),p["accent"]); r(d,(right-2,torso+3,right-1,torso+7),p["accent"])
    elif p["id"] == "mentor": r(d,(left+1,torso+1,left+2,torso+8),p["accent"]); r(d,(right-2,torso+1,right-1,torso+8),p["accent"])
    arm = torso+4
    if direction in ("south","north"):
        swing = gait if move else (2 if reach else 0); r(d,(left-3+swing,arm,left-1+swing,arm+3),p["skin"]); r(d,(right+1-swing,arm+(1 if phase%2 else 0),right+3-swing,arm+4),p["skinHi"])
    elif direction == "west":
        x = left-(5 if reach else 3)+(gait if move else 0); r(d,(x,arm+(phase%2 if move else 0),left,arm+2+(phase%2 if move else 0)),p["skinHi"]); r(d,(right-1,arm+1,right+1,arm+4),p["shadow"])
    else:
        x = right+(5 if reach else 3)-(gait if move else 0); r(d,(right,arm+(phase%2 if move else 0),x,arm+2+(phase%2 if move else 0)),p["skinHi"]); r(d,(left-1,arm+1,left+1,arm+4),p["shadow"])
    leg_y = torso+10; leg_len = max(4,30-leg_y)
    if senior: r(d,(left+1,leg_y,right-1,leg_y+leg_len-1),p["bottom"])
    else: r(d,(left,leg_y,left+2,leg_y+leg_len-1),p["bottom"]); r(d,(right-2,leg_y,right,leg_y+leg_len-1),p["bottom"])
    if move: r(d,(left-1+max(0,gait),30,left+2+max(0,gait),31),p["shoe"]); r(d,(right-1-max(0,-gait),30,right+2-max(0,-gait),31),p["shoeHi"])
    else: r(d,(left-1,30,left+2,31),p["shoe"]); r(d,(right-1,30,right+2,31),p["shoeHi"])
    if reach:
        prop = p["prop"]
        if prop == "backpack": r(d,(right+2,torso+5,right+4,torso+7),p["accent"])
        elif prop == "ring": r(d,(right+3,arm-1,right+4,arm),p["accent"]); r(d,(right+2,arm-2,right+3,arm-1),p["accent"])
        elif prop == "kite": r(d,(right+2,arm-1,right+4,arm+1),p["accent"]); r(d,(right+3,arm-3,right+4,arm-2),p["accent"])
        elif prop == "cane": r(d,(right+2,arm-1,right+3,30),p["accent"]); r(d,(right+3,arm-2,right+4,arm-1),p["accent"])
        elif prop == "notebook": r(d,(right+2,arm,right+5,arm+3),p["accent"]); r(d,(right+3,arm+1,right+4,arm+1),p["topHi"])
    return im

def save(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); im.save(path, format="PNG", optimize=False)

def atlas(images: list[Image.Image], cols: int, scale: int = 1) -> Image.Image:
    out = Image.new("RGBA", (24*cols,32*((len(images)+cols-1)//cols)), (0,0,0,0))
    for i,im in enumerate(images): out.alpha_composite(im, ((i%cols)*24,(i//cols)*32))
    return out.resize((out.width*scale,out.height*scale), Image.Resampling.NEAREST) if scale != 1 else out

def main() -> None:
    if OUT.exists():
        for entry in OUT.iterdir():
            if entry.name == Path(__file__).name: continue
            shutil.rmtree(entry) if entry.is_dir() else entry.unlink()
    records=[]; hashes={}; previews=[]
    for p in FAMILIES:
        images=[]; family_records=[]
        for direction in DIRECTIONS:
            for tag in COLUMNS:
                mode = "move" if tag in PHASES else tag; phase = PHASES.index(tag) if tag in PHASES else 0
                im=draw_frame(p,direction,mode,phase); path=OUT/"frames"/p["id"]/f"{p['id']}-{direction}-{tag}.png"; save(im,path); digest=sha(path); hashes[str(path.relative_to(OUT))]=digest; images.append(im)
                rec={"id":f"{p['id']}/{direction}/{tag}","catalogId":p["catalogId"],"character":p["name"],"family":p["id"],"direction":direction,"animation":"walk" if tag in PHASES else tag,"phase":tag if tag in PHASES else None,"file":str(path.relative_to(OUT)),"width":24,"height":32,"pivot":list(PIVOT),"sha256":digest,"runtimeReady":False}; records.append(rec); family_records.append(rec)
        save(atlas(images,6),OUT/"atlases"/f"{p['id']}-atlas.png"); previews.append(atlas(images,6,4)); (OUT/"frames"/p["id"]/"frames.json").write_text(json.dumps({"family":p["id"],"frames":family_records},indent=2)+"\n")
    sheet=Image.new("RGBA",(max(i.width for i in previews),sum(i.height for i in previews)),(24,27,40,255)); y=0
    for im in previews: sheet.alpha_composite(im,(0,y)); y+=im.height
    save(sheet,OUT/"named-characters-contact-sheet-4x.png")
    manifest={"batch":"named-characters-batch-v2","direction":"PIXEL-ONLY","runtimeReady":False,"frameSize":{"width":24,"height":32},"pivot":list(PIVOT),"directions":list(DIRECTIONS),"walkPhases":list(PHASES),"poseTags":list(POSES),"atlasColumns":list(COLUMNS),"familyCount":5,"framesPerFamily":24,"frameCount":len(records),"families":[{k:p[k] for k in ("id","catalogId","name","role","ageStage","identity","interaction")} for p in FAMILIES],"frames":records,"hashes":hashes}; (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    provenance={"batch":"named-characters-batch-v2","created":"2026-10-20","method":"deterministic hand-authored Pillow pixel clusters","source":"No supplied ZIP files, third-party sprites, external images, or internet assets were used.","rights":"Original project-owned working concepts; no third-party art embedded.","identityNotes":{"sibling":"Preserves Niko cues from named-family-batch-v1: warm brown skin, curly ponytail, cobalt hoodie, orange sneakers, backpack.","otherFamilies":"New role studies use independent palettes, silhouettes, accessories, and interaction props."},"runtimeReady":False,"limitations":["Needs human pixel cleanup and motion review.","Pivots and collision boxes need renderer validation.","Catalog promotion is intentionally omitted."]}; (OUT/"provenance.json").write_text(json.dumps(provenance,indent=2)+"\n")
    (OUT/"README.md").write_text("""# Named characters batch v2

Five original named-family pixel movement studies: Niko (sibling), Nora
(partner), Tavi (child), Dadi (grandparent), and Ishan (mentor). Each has 24
transparent RGBA frames at `24x32`: four independently authored directions,
four walk phases, idle, and interact. Atlas columns are `contact-a`,
`passing-a`, `contact-b`, `passing-b`, `idle`, `interact`.

Niko preserves the existing catalog cues: curly ponytail, cobalt hoodie,
orange sneakers, warm brown skin, and backpack. The other families use new
role-specific silhouettes, palettes, accessories, and age-safe interaction
props. No supplied ZIP, external image, third-party sprite, game-art
reference, or internet asset is embedded. `manifest.json` contains exact
catalog IDs, per-frame hashes, pivots, and `runtimeReady: false`;
`provenance.json` records the rights boundary. These are concept previews and
need human pixel cleanup, motion/identity review, renderer sampling,
collision/pivot checks, and device capture before promotion.
""")
    print(f"generated {len(records)} frames for {len(FAMILIES)} families")

if __name__ == "__main__": main()
