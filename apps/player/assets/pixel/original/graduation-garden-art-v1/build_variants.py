from pathlib import Path
from PIL import Image, ImageOps
import json, hashlib
root=Path('apps/player/assets/pixel/original/graduation-garden-art-v1')
src=root/'source.png'
im=Image.open(src).convert('RGB')
# Preserve the source and create two reversible pixel-sampling candidates.
w,h=im.size; target_ratio=5/4
if w/h > target_ratio:
    nw=round(h*target_ratio); left=(w-nw)//2; im=im.crop((left,0,left+nw,h))
else:
    nh=round(w/target_ratio); top=(h-nh)//2; im=im.crop((0,top,w,top+nh))

def save(name, image):
    p=root/name; image.save(p,optimize=True)
    return p
# Strong pixel-cluster variant: quantize on 160x128 logical plate, scale to 320x256 nearest.
small=im.resize((160,128),Image.Resampling.LANCZOS)
# Restrict palette colors while retaining scene depth and preserve hard pixel edges.
small=small.quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
pixel=small.resize((320,256),Image.Resampling.NEAREST)
p1=save('graduation-garden-pixel-320x256.png',pixel)
# Lower-color option for a simpler handheld-scale palette.
small24=im.resize((160,128),Image.Resampling.LANCZOS).quantize(colors=24,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
p3=save('graduation-garden-pixel-24c-320x256.png',small24.resize((320,256),Image.Resampling.NEAREST))
# Higher-detail concept plate reduced with nearest sampling, then palette constrained.
detail=im.resize((320,256),Image.Resampling.LANCZOS).quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
p2=save('graduation-garden-detail-320x256.png',detail)
records=[]
for role,p in [('logical-pixel-study-48c',p1),('detail-concept-export-64c',p2),('logical-pixel-study-24c',p3)]:
    with Image.open(p) as out:
        records.append({'id':f'graduation-garden.{role}','role':role,'file':p.name,'width':out.width,'height':out.height,'mode':out.mode,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'runtimeReady':False})
(root/'manifest.json').write_text(json.dumps({'schemaVersion':1,'batch':'graduation-garden-art-v1','runtimeReady':False,'source':{'file':'source.png','sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'dimensions':list(Image.open(src).size),'mode':'RGB'},'records':records,'limitations':['One generated graduation courtyard background study; no characters or UI.','The 160x128 logical version is palette-quantized and nearest-neighbor scaled; verify readability at game scale.','This is a backdrop concept, not a walkable map, tile set, or layered production scene.']},indent=2)+'\n')
