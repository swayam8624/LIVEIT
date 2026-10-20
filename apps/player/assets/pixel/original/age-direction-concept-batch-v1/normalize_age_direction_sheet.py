from PIL import Image
from pathlib import Path
import json

root=Path(__file__).parent
src=Image.open(root/'age-directions-concept-master.png').convert('RGBA')
stages=json.loads((root/'frames.json').read_text())['rows']
directions=json.loads((root/'frames.json').read_text())['columns']
frame_w,frame_h=96,128
cell_w,cell_h=src.width/4,src.height/8
all_atlas=Image.new('RGBA',(frame_w*4,frame_h*8),(0,0,0,0))
for row,stage_id in enumerate(stages):
 stage=Image.new('RGBA',(frame_w*4,frame_h),(0,0,0,0))
 for col,direction in enumerate(directions):
  crop=src.crop((round(col*cell_w),round(row*cell_h),round((col+1)*cell_w),round((row+1)*cell_h)))
  alpha=crop.getchannel('A').point(lambda value:255 if value>=112 else 0)
  # Remove tiny disconnected color flecks while retaining disconnected accessories such as the elder cane.
  w,h=alpha.size; data=bytearray(alpha.tobytes()); seen=bytearray(w*h); components=[]
  for index,value in enumerate(data):
   if not value or seen[index]: continue
   stack=[index]; seen[index]=1; component=[]
   while stack:
    current=stack.pop(); component.append(current); x=current%w; y=current//w
    for yy in range(max(0,y-1),min(h,y+2)):
     for xx in range(max(0,x-1),min(w,x+2)):
      nxt=yy*w+xx
      if data[nxt] and not seen[nxt]: seen[nxt]=1; stack.append(nxt)
   components.append(component)
  clean=bytearray(w*h)
  for component in components:
   if len(component)>=12:
    for index in component: clean[index]=255
  alpha=Image.frombytes('L',(w,h),bytes(clean)); crop.putalpha(alpha); bounds=alpha.getbbox()
  if not bounds: raise RuntimeError(f'empty frame {stage_id}/{direction}')
  sprite=crop.crop(bounds)
  scale=min(frame_w/sprite.width,frame_h/sprite.height)
  sw=max(1,round(sprite.width*scale)); sh=max(1,round(sprite.height*scale))
  sprite=sprite.resize((sw,sh),Image.Resampling.NEAREST)
  frame=Image.new('RGBA',(frame_w,frame_h),(0,0,0,0)); frame.alpha_composite(sprite,((frame_w-sw)//2,frame_h-sh))
  frame.save(root/stage_id/f'{stage_id}-{direction}-idle.png')
  stage.alpha_composite(frame,(col*frame_w,0)); all_atlas.alpha_composite(frame,(col*frame_w,row*frame_h))
 stage.save(root/stage_id/f'{stage_id}-directions-atlas.png')
 stage.resize((frame_w*4,frame_h*4),Image.Resampling.NEAREST).save(root/stage_id/f'{stage_id}-preview-4x.png')
all_atlas.save(root/'age-directions-8stages-atlas.png')
all_atlas.resize((frame_w*16,frame_h*32),Image.Resampling.NEAREST).save(root/'age-directions-preview-4x.png')
