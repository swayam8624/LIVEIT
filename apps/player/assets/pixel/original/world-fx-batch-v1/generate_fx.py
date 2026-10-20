from PIL import Image, ImageDraw
from pathlib import Path
import json, random
OUT=Path(__file__).parent
SIZE=32
KINDS=['rain','snow','autumn-leaves','night-lights']
frames=[]
for kind in KINDS:
 atlas=Image.new('RGBA',(SIZE*4,SIZE*2),(0,0,0,0))
 for idx in range(8):
  im=Image.new('RGBA',(SIZE,SIZE),(0,0,0,0)); d=ImageDraw.Draw(im); rng=random.Random(4200+idx)
  if kind=='rain':
   for n in range(7):
    x=(n*7+idx*3)%SIZE; y=(n*13+idx*5)%SIZE
    d.line((x,y,x-2,y+5),fill=(115,181,220,150),width=1)
    d.point((x-2,y+6),fill=(192,220,234,115))
  elif kind=='snow':
   for n in range(9):
    x=(n*11+idx*2)%SIZE; y=(n*7+idx*3)%SIZE
    col=(231,243,246,185 if n%3 else 125)
    d.point((x,y),fill=col); d.point((x+1,y),fill=col)
    if n%2==0: d.point((x,y+1),fill=col)
  elif kind=='autumn-leaves':
   for n in range(6):
    x=(n*9+idx*2)%SIZE; y=(n*11+idx*3)%SIZE
    col=[(210,119,65,190),(194,82,67,175),(223,166,77,185)][n%3]
    d.rectangle((x,y,x+2,y+1),fill=col); d.point((x+1,y+2),fill=(93,114,69,170))
  else:
   for n in range(7):
    x=(n*13+idx*5)%SIZE; y=(n*9+idx*7)%SIZE
    col=(246,209,119,190 if n%2 else 120)
    d.point((x,y),fill=col)
    if n%3==0: d.point((x+1,y),fill=(255,241,184,210))
  x=(idx%4)*SIZE; y=(idx//4)*SIZE; atlas.alpha_composite(im,(x,y))
  fn=f'{kind}-{idx+1:02}.png'; im.save(OUT/fn)
  frames.append({'id':fn[:-4],'file':fn,'family':kind,'phase':idx,'x':x,'y':y,'width':SIZE,'height':SIZE,'sampling':'nearest','runtimeReady':False})
 atlas.save(OUT/f'{kind}-atlas.png')
 atlas.resize((SIZE*8,SIZE*4),Image.Resampling.NEAREST).save(OUT/f'{kind}-preview-2x.png')
# Five frame pixel iris transition, each cell 48x48.
S=48; trans=Image.new('RGBA',(S*5,S),(0,0,0,0)); tframes=[]
for idx,radius in enumerate([0,7,14,21,34]):
 im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im)
 # use a dark-plum opaque veil with a pixelated circular transparent reveal
 d.rectangle((0,0,S-1,S-1),fill=(39,31,47,238))
 cx=cy=S//2
 for yy in range(S):
  for xx in range(S):
   dx=xx-cx; dy=yy-cy
   if (dx*dx+dy*dy)<=radius*radius and (xx//2+yy//2)%2==0: im.putpixel((xx,yy),(0,0,0,0))
 trans.alpha_composite(im,(idx*S,0)); im.save(OUT/f'pixel-iris-{idx+1:02}.png')
 tframes.append({'id':f'pixel-iris-{idx+1:02}','file':f'pixel-iris-{idx+1:02}.png','x':idx*S,'y':0,'width':S,'height':S,'radius':radius,'runtimeReady':False})
trans.save(OUT/'pixel-iris-atlas.png'); trans.resize((S*10,S*2),Image.Resampling.NEAREST).save(OUT/'pixel-iris-preview-2x.png')
manifest={'batch':'world-fx-batch-v1','runtimeReady':False,'weatherFamilies':KINDS,'sampling':'nearest','frameSize':[SIZE,SIZE],'transitionFrameSize':[S,S],'frames':frames+tframes,'limitations':['prototype overlays and iris transition only','weather particles are sparse pixel clusters and must be layered over game scenes in renderer','lighting palettes/night grading not included','transition direction/timing must be authored and tested in runtime']}
(OUT/'frames.json').write_text(json.dumps(manifest,indent=2)+'\n')
(OUT/'README.md').write_text('''# World effects batch v1\n\nOriginal pixel overlays for rain, snow, autumn leaves, and night lights, plus a five-frame pixel iris transition. Each weather family has eight 32×32 transparent frames; iris frames are 48×48. Frames are individual files and packed in nearest-sampled atlases.\n\nAll artwork was generated deterministically with integer-coordinate drawing in `generate_fx.py` on 2026-10-20. No downloaded, supplied-archive, or third-party assets or references were used. Metadata and frame limits are in `frames.json`. These are visual prototypes with runtimeReady false; particle density, palette integration, timing, accessibility contrast, and renderer performance still need review.\n''')
