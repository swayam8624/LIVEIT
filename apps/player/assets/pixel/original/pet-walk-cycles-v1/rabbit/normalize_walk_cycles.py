#!/usr/bin/env python3
"""Package the generated rabbit sheet into fixed 96x128 nearest-neighbor frames."""
from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "rabbit-walk-cycles-source.png"
FRAME_W, FRAME_H = 96, 128
FACING = ["south", "west", "east", "north"]
PHASES = ["contact-a", "passing-a", "contact-b", "passing-b"]

def read_png(path: Path):
    raw = path.read_bytes(); assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    pos = 8; idat = bytearray(); width = height = None
    while pos < len(raw):
        n = struct.unpack(">I", raw[pos:pos+4])[0]; kind = raw[pos+4:pos+8]
        chunk = raw[pos+8:pos+8+n]; pos += n + 12
        if kind == b"IHDR":
            width, height, depth, color, comp, filt, interlace = struct.unpack(">IIBBBBB", chunk)
            if (depth, color, comp, filt, interlace) != (8, 6, 0, 0, 0): raise ValueError("expected RGBA PNG")
        elif kind == b"IDAT": idat.extend(chunk)
        elif kind == b"IEND": break
    packed = zlib.decompress(idat); stride = width * 4; rows = []; p = 0; prev = bytearray(stride)
    for _ in range(height):
        mode = packed[p]; p += 1; cur = bytearray(packed[p:p+stride]); p += stride
        for i in range(stride):
            left = cur[i-4] if i >= 4 else 0; up = prev[i]; ul = prev[i-4] if i >= 4 else 0
            if mode == 1: cur[i] = (cur[i] + left) & 255
            elif mode == 2: cur[i] = (cur[i] + up) & 255
            elif mode == 3: cur[i] = (cur[i] + ((left + up)//2)) & 255
            elif mode == 4:
                q = left + up - ul; a,b,c = abs(q-left), abs(q-up), abs(q-ul)
                cur[i] = (cur[i] + (left if a <= b and a <= c else up if b <= c else ul)) & 255
            elif mode != 0: raise ValueError(f"unsupported PNG filter {mode}")
        rows.append(bytes(cur)); prev = cur
    return width, height, b"".join(rows)

def write_png(path: Path, width: int, height: int, pixels: bytes) -> None:
    def chunk(kind, data): return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    rows = b"".join(b"\0" + pixels[y*width*4:(y+1)*width*4] for y in range(height))
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))

def crop_cell(pixels, width, height, col, row):
    x0, x1 = round(col*width/4), round((col+1)*width/4)
    y0, y1 = round(row*height/4), round((row+1)*height/4)
    cw, ch = x1-x0, y1-y0
    cell = bytearray().join(pixels[(y0+y)*width*4+x0*4:(y0+y)*width*4+x1*4] for y in range(ch))
    # The generated sheet has one isolated silhouette per cell. A direct alpha
    # bounds scan keeps packaging deterministic and avoids rewriting any source pixels.
    points = [(y*cw+x) for y in range(ch) for x in range(cw) if cell[(y*cw+x)*4+3] > 8]
    if not points: raise ValueError(f"empty cell {row},{col}")
    xs, ys = [q % cw for q in points], [q // cw for q in points]
    bx0, bx1 = max(0,min(xs)-3), min(cw,max(xs)+4); by0, by1 = max(0,min(ys)-3), min(ch,max(ys)+4)
    out = bytearray((bx1-bx0)*(by1-by0)*4)
    for y in range(by0,by1):
        for x in range(bx0,bx1):
            q = y*cw+x
            out[((y-by0)*(bx1-bx0)+(x-bx0))*4:((y-by0)*(bx1-bx0)+(x-bx0)+1)*4] = cell[q*4:q*4+4]
    return bytes(out), bx1-bx0, by1-by0

def normalize(cropped, sw, sh, target_h):
    scale = min((FRAME_W-8)/sw, target_h/sh); ow, oh = max(1,round(sw*scale)), max(1,round(sh*scale)); ox, oy = (FRAME_W-ow)//2, FRAME_H-oh-2
    out = bytearray(FRAME_W*FRAME_H*4)
    for y in range(oh):
        for x in range(ow):
            src = (min(sh-1,int(y/scale))*sw + min(sw-1,int(x/scale)))*4; dst = ((oy+y)*FRAME_W+ox+x)*4; out[dst:dst+4] = cropped[src:src+4]
    return bytes(out)

def main():
    width, height, pixels = read_png(SOURCE); cells = [crop_cell(pixels,width,height,c,r) for r in range(4) for c in range(4)]
    target_h = min(FRAME_H-8, max(c[2] for c in cells)); atlas = bytearray(384*512*4); frames = []; (ROOT/"frames").mkdir(exist_ok=True)
    for row, facing in enumerate(FACING):
        for col, phase in enumerate(PHASES):
            frame = normalize(*cells[row*4+col], target_h); name = f"rabbit-{facing}-{phase}.png"; write_png(ROOT/"frames"/name,FRAME_W,FRAME_H,frame)
            for y in range(FRAME_H): atlas[((row*FRAME_H+y)*384+col*FRAME_W)*4:((row*FRAME_H+y)*384+(col+1)*FRAME_W)*4] = frame[y*FRAME_W*4:(y+1)*FRAME_W*4]
            frames.append({"id":f"rabbit/{facing}/{phase}","character":"rabbit","facing":facing,"phase":phase,"file":f"frames/{name}","atlas":{"x":col*FRAME_W,"y":row*FRAME_H,"width":FRAME_W,"height":FRAME_H},"pivot":{"x":48,"y":126},"runtimeReady":False})
    write_png(ROOT/"rabbit-walk-cycles-atlas.png",384,512,bytes(atlas)); preview = bytearray(768*1024*4)
    for y in range(512):
        for x in range(384):
            px = atlas[(y*384+x)*4:(y*384+x+1)*4]
            for dy in (0,1):
                for dx in (0,1): preview[((y*2+dy)*768+x*2+dx)*4:((y*2+dy)*768+x*2+dx+1)*4] = px
    write_png(ROOT/"rabbit-walk-cycles-preview-2x.png",768,1024,bytes(preview))
    (ROOT/"frames.json").write_text(json.dumps({"schemaVersion":1,"runtimeReady":False,"sourceMode":"generated-four-phase","sheet":{"columns":4,"rows":4,"frameWidth":96,"frameHeight":128,"sourceWidth":width,"sourceHeight":height},"frames":frames},indent=2)+"\n")

if __name__ == "__main__": main()
