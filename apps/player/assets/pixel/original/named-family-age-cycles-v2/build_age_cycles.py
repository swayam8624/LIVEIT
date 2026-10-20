#!/usr/bin/env python3
"""Build original deterministic Nora and Tavi age-stage pixel cycles."""
from __future__ import annotations
import hashlib, json, struct, zlib
from pathlib import Path
ROOT = Path(__file__).resolve().parent
W, H, PIVOT = 24, 32, [12, 31]
DIRECTIONS = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b", "idle", "interact"]
STAGES = [
    ("nora", "Nora Bellweather", "adult", "liveit.prod.v1.pixel.sprite.named.partner"),
    ("nora", "Nora Bellweather", "midlife", "liveit.prod.v1.pixel.sprite.named.partner"),
    ("nora", "Nora Bellweather", "elder", "liveit.prod.v1.pixel.sprite.named.partner"),
    ("tavi", "Tavi Bellweather", "toddler", "liveit.prod.v1.pixel.sprite.named.child"),
    ("tavi", "Tavi Bellweather", "child", "liveit.prod.v1.pixel.sprite.named.child"),
    ("tavi", "Tavi Bellweather", "teen", "liveit.prod.v1.pixel.sprite.named.child"),
    ("tavi", "Tavi Bellweather", "young-adult", "liveit.prod.v1.pixel.sprite.named.child"),
]
PAL = {
 "ink":(43,37,49,255), "skin_nora":(180,119,92,255), "skin_tavi":(157,92,70,255),
 "indigo":(76,69,131,255), "rose":(186,100,115,255), "cream":(244,224,180,255),
 "trouser":(63,65,87,255), "shoe":(57,48,61,255), "silver":(206,207,195,255),
 "green":(80,133,78,255), "greenlight":(120,167,91,255), "violet":(113,78,151,255),
 "purple":(111,70,139,255), "yellow":(238,188,64,255), "rust":(164,83,62,255),
 "gray":(151,156,153,255), "cane":(112,91,64,255), "white":(243,236,214,255),
}
class Canvas:
 def __init__(self): self.p=bytearray(W*H*4)
 def rect(self,x1,y1,x2,y2,color):
  c=PAL[color] if isinstance(color,str) else color
  for y in range(max(0,y1),min(H,y2+1)):
   for x in range(max(0,x1),min(W,x2+1)):
    i=(y*W+x)*4; self.p[i:i+4]=bytes(c)
 def png(self):
  raw=b"".join(b"\0"+bytes(self.p[y*W*4:(y+1)*W*4]) for y in range(H))
  def chunk(k,d): return struct.pack(">I",len(d))+k+d+struct.pack(">I",zlib.crc32(k+d)&0xffffffff)
  return b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">2I5B",W,H,8,6,0,0,0))+chunk(b"IDAT",zlib.compress(raw,9))+chunk(b"IEND",b"")
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def draw(identity, age, direction, phase):
 c=Canvas(); nora=identity=="nora"; skin="skin_nora" if nora else "skin_tavi"
 dirs={"south":0,"west":1,"east":2,"north":3}; di=dirs[direction]
 ph=PHASES.index(phase); stride=[0,1,0,-1,0,0][ph]; dx=stride if di in (1,2) else 0
 # Stage proportions preserve a common footline while distinguishing growth.
 tops={"adult":5,"midlife":5,"elder":6,"toddler":12,"child":10,"teen":7,"young-adult":6}
 widths={"adult":8,"midlife":9,"elder":10,"toddler":6,"child":7,"teen":8,"young-adult":8}
 top=tops[age]; bw=widths[age]; cx=12+dx; foot=29
 hip=top+(8 if nora else 7 if age in ("toddler","child") else 8)
 leg=1 if ph in (0,1) else -1 if ph in (2,3) else 0
 # Directional legs and footwear; every gait phase changes the knee/hem pixels.
 pants="trouser" if nora else "green"
 c.rect(cx-3,hip+5,cx-1,foot-2+max(0,leg),pants); c.rect(cx+1,hip+5,cx+3,foot-2+max(0,-leg),pants)
 shoe="shoe" if nora else "violet"
 c.rect(cx-4,foot-1+max(0,leg),cx-1,foot,shoe); c.rect(cx+1,foot-1+max(0,-leg),cx+4,foot,shoe)
 shirt="rose" if nora else "green"
 c.rect(cx-bw//2,hip,cx+(bw-1)//2,hip+10,shirt)
 c.rect(cx-bw//2-2,hip+2,cx-bw//2,hip+7,shirt); c.rect(cx+(bw-1)//2+1,hip+2,cx+(bw-1)//2+2,hip+7,shirt)
 c.rect(cx-2,hip+8,cx-2,hip+9,skin); c.rect(cx+2,hip+8,cx+2,hip+9,skin)
 hw=7 if age in ("toddler","child") else 8; hy=top
 c.rect(cx-2,hy+5,cx+2,hy+7,skin); c.rect(cx-hw//2,hy,cx+(hw-1)//2,hy+6,skin)
 hair="indigo" if nora else "ink"
 if direction=="north":
  c.rect(cx-hw//2-1,hy-1,cx+(hw-1)//2+1,hy+3,hair)
 elif direction in ("west","east"):
  c.rect(cx-hw//2-1,hy-1,cx+1,hy+1,hair)
  c.rect(cx-2 if direction=="west" else cx+2,hy+3,cx-2 if direction=="west" else cx+2,hy+4,"ink")
 else:
  c.rect(cx-hw//2-1,hy-1,cx+(hw-1)//2+1,hy+1,hair)
  c.rect(cx-hw//2-1,hy+1,cx-hw//2,hy+4,hair); c.rect(cx+(hw-1)//2,hy+1,cx+(hw-1)//2+1,hy+4,hair)
  if di==0:
   c.rect(cx-2,hy+3,cx-2,hy+3,"ink"); c.rect(cx+2,hy+3,cx+2,hy+3,"ink")
 # Nora's bob, ring and rose/indigo palette remain recognizable through adulthood.
 if nora:
  if age=="midlife": c.rect(cx-3,hy-1,cx-2,hy-1,"silver"); c.rect(cx+2,hy-1,cx+3,hy-1,"silver")
  if age=="elder":
   c.rect(cx-4,hy-1,cx+4,hy,"silver"); c.rect(cx-4,hy+1,cx-4,hy+3,"silver"); c.rect(cx+4,hy+1,cx+4,hy+3,"silver")
  c.rect(cx+2,hip+2,cx+2,hip+2,"cream")
 else:
  # The purple cap is Tavi's anchor at every age; only its scale changes.
  cap="purple" if age in ("toddler","child") else "indigo"
  c.rect(cx-hw//2-1,hy-2,cx+(hw-1)//2+1,hy-1,cap)
  c.rect(cx+(hw-1)//2,hy-2,cx+(hw-1)//2+2,hy,cap)
  c.rect(cx-2,hip+2,cx-1,hip+6,"greenlight")
  # Age-neutral child signal (kite spool) appears in child/toddler stages only.
  if age in ("toddler","child"):
   c.rect(cx+4,hip+3,cx+6,hip+5,"yellow"); c.rect(cx+5,hip+6,cx+5,hip+7,"rust")
  elif age=="teen": c.rect(cx+3,hip+2,cx+4,hip+3,"yellow")
 # Interact poses are friendly, non-romantic and age-safe; distinct hand gesture per facing.
 if phase=="interact":
  hx=cx+5 if direction!="west" else cx-5
  c.rect(hx,hip+1,hx+1,hip+3,skin)
  if not nora and age in ("toddler","child"): c.rect(hx+1,hip+2,hx+3,hip+4,"yellow")
 # Elder Nora uses a small cane as a mobility cue, with stable feet pivot.
 if nora and age=="elder":
  side=-1 if direction=="west" else 1
  c.rect(cx+side*7,hip+7,cx+side*7,foot,"cane"); c.rect(cx+side*7,hip+7,cx+side*8,hip+7,"cane")
 # Direction and phase marker pixels are part of garment seams, making all six poses authored distinctly.
 marker=("cream" if nora else "yellow")
 if phase in ("contact-a","passing-a","contact-b","passing-b"):
  mx=cx-1 if ph in (0,1) else cx+1
  c.rect(mx,hip+9,mx,hip+9,marker if ph in (1,3) else shirt)
 if direction=="west": c.rect(cx-bw//2,hip+4,cx-bw//2,hip+4,marker)
 elif direction=="east": c.rect(cx+(bw-1)//2,hip+4,cx+(bw-1)//2,hip+4,marker)
 elif direction=="north": c.rect(cx,hip+4,cx,hip+4,marker)
 else: c.rect(cx,hip+4,cx,hip+4,marker)
 # Orient idle/interact arm detail so they remain distinct for every direction.
 if phase=="idle": c.rect(cx-1,hip+2,cx-1,hip+2,"white")
 return c.png()

def main():
 frames=[]; identities=[]
 for ident,name,age,catalog in STAGES:
  directory=ROOT/"frames"/ident/age; directory.mkdir(parents=True,exist_ok=True)
  stage_frames=[]
  for direction in DIRECTIONS:
   for phase in PHASES:
    path=directory/f"{ident}-{age}-{direction}-{phase}.png"; path.write_bytes(draw(ident,age,direction,phase))
    frame={"id":f"{ident}/{age}/{direction}/{phase}","character":ident,"displayName":name,"ageStage":age,"catalogId":catalog,"direction":direction,"phase":phase,"file":path.relative_to(ROOT).as_posix(),"width":W,"height":H,"mode":"RGBA","pivot":{"x":12,"y":31},"sha256":sha(path),"runtimeReady":False,"sourceLineage":"originally rasterized by build_age_cycles.py; character identity and catalog mapping reference named-characters-batch-v2; no prior age-cycle PNG bytes are embedded or copied"}
    frames.append(frame); stage_frames.append(frame)
  identities.append({"id":ident,"name":name,"ageStage":age,"catalogId":catalog,"frameIds":[f["id"] for f in stage_frames],"runtimeReady":False})
 atlas_path=ROOT/"named-family-age-cycles-v2-atlas.png"; sheet_path=ROOT/"named-family-age-cycles-v2-contact-sheet.png"
 atlas_png(6*W,len(STAGES)*4*H,frames,atlas_path)
 atlas_png(6*W*4,4*H*2,frames,sheet_path,contact=True)
 stages={"nora":["adult","midlife","elder"],"tavi":["toddler","child","teen","young-adult"]}
 manifest={"schemaVersion":1,"batch":"named-family-age-cycles-v2","direction":"PIXEL-ONLY","description":"Original deterministic age-stage movement cycles for named Bellweather family identities Nora and Tavi.","runtimeReady":False,"frameSize":{"width":W,"height":H},"pivot":{"x":12,"y":31},"directions":DIRECTIONS,"phases":PHASES,"ageTransitions":stages,"identities":identities,"frames":frames,"outputs":{"atlas":{"file":atlas_path.name,"size":[144,len(STAGES)*128],"sha256":sha(atlas_path)},"contactSheet":{"file":sheet_path.name,"size":[576,256],"sha256":sha(sheet_path)}},"sourceLineage":{"package":"named-characters-batch-v2","meaning":"Only names, roles, identity cues and catalog IDs are referenced. Every PNG is independently rasterized; prior Mara/Eli/Niko cycle image bytes are not source inputs.","sourceFiles":[{"file":"../named-characters-batch-v2/manifest.json","sha256":sha(ROOT.parent/"named-characters-batch-v2"/"manifest.json")}]}}
 (ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
 provenance={"package":"named-family-age-cycles-v2","created":"2026-10-20","creator":"Codex-assisted deterministic procedural pixel-art builder","rights":"Original project working material generated from repository-authored character descriptions; no third-party ZIP, external image, or game artwork used.","builder":"build_age_cycles.py","runtimeReady":False,"prompt":"Create original top-down pixel movement cycles for Nora Bellweather (adult, midlife, elder) and Tavi Bellweather (toddler, child, teen, young adult). Preserve Nora's short indigo bob, rose overshirt, cream ring and wide-leg trousers, with silver hair/posture progression and a cane only for elder. Preserve Tavi's purple cap, leaf-green overalls, violet boots and kite-spool identity cue; scale the cap and garments with growth, omit adult-coded accessories, and keep all poses fully clothed and age-safe. For every stage produce four cardinal directions and four visibly distinct gait phases plus neutral idle and friendly non-romantic interact. Transparent 24x32 RGBA, common feet pivot (12,31), crisp limited-palette pixel clusters, no text/logos/shadow/3D or copied art.","limitations":["Concept sprites require artist review and animation playback review.","Age readability and pivot/collision fit require human review.","Catalog mappings are references only; not integrated with runtime loading."]}
 (ROOT/"provenance.json").write_text(json.dumps(provenance,indent=2)+"\n")
def atlas_png(width, height, frames, path, contact=False):
    # Construct RGBA PNG without third-party libraries; transparent gaps are intentional.
    pixels = bytearray(width*height*4)
    ordered = frames
    bands = []
    for i in range(0,len(ordered),24): bands.append(ordered[i:i+24])
    if contact:
        for n, band in enumerate(bands):
            bx=(n%4)*6*W; by=(n//4)*4*H
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
