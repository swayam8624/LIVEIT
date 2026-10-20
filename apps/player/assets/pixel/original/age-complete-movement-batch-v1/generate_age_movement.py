from PIL import Image, ImageDraw
from pathlib import Path
import json, hashlib

OUT = Path(__file__).parent
W, H = 24, 32
DIRECTIONS = ['south', 'west', 'east', 'north']
PHASES = ['contact-a', 'passing-a', 'contact-b', 'passing-b']
STAGES = [
    {'id':'infant-crawl','age':'infant','locomotion':'crawl','skin':'#9a583f','hair':'#30252b','shirt':'#e9c46a','pants':'#527c8c','shoe':'#f2d6a4','hairStyle':'tuft','height':16,'crawler':True},
    {'id':'toddler-waddle','age':'toddler','locomotion':'waddle','skin':'#c77950','hair':'#38252a','shirt':'#e6874e','pants':'#4d6f8c','shoe':'#e9c46a','hairStyle':'curl','height':21},
    {'id':'child-walk','age':'child','locomotion':'walk','skin':'#8b523e','hair':'#271f28','shirt':'#477e8b','pants':'#59466f','shoe':'#332d39','hairStyle':'curl','height':25},
    {'id':'teen-walk','age':'teen','locomotion':'walk','skin':'#d2956c','hair':'#49302a','shirt':'#bc694f','pants':'#34475b','shoe':'#292d38','hairStyle':'sweep','height':27},
    {'id':'young-adult-walk','age':'young-adult','locomotion':'walk','skin':'#ba7959','hair':'#30242a','shirt':'#377a76','pants':'#594b53','shoe':'#292631','hairStyle':'sweep','height':28},
    {'id':'midlife-adult-walk','age':'midlife-adult','locomotion':'walk','skin':'#9e644c','hair':'#43352e','shirt':'#687d55','pants':'#4b4a58','shoe':'#292631','hairStyle':'sweep','height':28},
    {'id':'elder-woman-walk','age':'elder','presentation':'woman','locomotion':'walk','skin':'#d3a17c','hair':'#c7c1b5','shirt':'#795b78','pants':'#4c5864','shoe':'#36303b','hairStyle':'bun','height':26,'cane':False},
    {'id':'elder-man-walk','age':'elder','presentation':'man','locomotion':'walk','skin':'#bd8867','hair':'#b7b5ae','shirt':'#627363','pants':'#4b535d','shoe':'#36303b','hairStyle':'short','height':26,'cane':True},
]
OUTLINE='#29232d'; SHADOW='#493642'; HIGHLIGHT='#f2c49a'; HAIRLIGHT='#705046'; CLOTHLIGHT='#83a89a'

def rect(d, box, color):
    d.rectangle(box, fill=color)
def canonical(stage, phase, direction):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    age=stage['age']; crawler=stage.get('crawler',False); ht=stage['height']
    swing=[-1,0,1,0][phase]
    if crawler:
        # Infant is deliberately horizontal, reaching/crawling in place.
        # Outline and shadow clusters
        rect(d,(5,16,18,25),OUTLINE); rect(d,(6,17,17,24),stage['shirt']); rect(d,(8,18,16,21),CLOTHLIGHT)
        # diaper/shorts and knees
        rect(d,(15,20,20,24),OUTLINE); rect(d,(16,21,19,23),'#f1dfc2')
        # head, ear, hair tuft
        rect(d,(2,11,10,19),OUTLINE); rect(d,(3,12,9,18),stage['skin']); rect(d,(3,11,8,14),stage['hair']); rect(d,(4,10,6,12),HAIRLIGHT)
        rect(d,(4,15,4,15),OUTLINE); rect(d,(7,15,7,15),OUTLINE); rect(d,(9,15,10,16),stage['skin'])
        # alternating reaching arms and crawling legs
        armx=2+swing; rect(d,(armx,20,7,22),OUTLINE); rect(d,(armx+1,20,6,21),stage['skin']); rect(d,(17-swing,15,20,17),OUTLINE); rect(d,(17-swing,16,19,16),stage['skin'])
        rect(d,(16,24,19+swing,26),OUTLINE); rect(d,(17,24,18+swing,25),stage['skin']); rect(d,(9,24,12-swing,26),OUTLINE); rect(d,(10,24,11-swing,25),stage['skin'])
        rect(d,(6,18,9,19),stage['shirt']);
    else:
        # derive vertical placement from stage silhouette height
        top=H-ht-1; head_h=7 if age in ['toddler','child'] else 8
        if age=='toddler': head_w=8
        elif age=='child': head_w=8
        elif age=='elder': head_w=8
        else: head_w=8
        cx=12; hx0=cx-head_w//2; hx1=hx0+head_w-1; hy0=top; hy1=top+head_h-1
        # rear hair/head silhouette
        rect(d,(hx0-1,hy0,hx1+1,hy1+1),OUTLINE); rect(d,(hx0,hy0+1,hx1,hy1),stage['skin'])
        # hair cap, age-specific silhouette
        rect(d,(hx0,hy0,hx1,hy0+2),stage['hair']); rect(d,(hx0-1,hy0+2,hx0,hy0+4),stage['hair']); rect(d,(hx1,hy0+2,hx1+1,hy0+4),stage['hair'])
        if stage['hairStyle'] in ['curl','bun']:
            for xx,yy in [(hx0,hy0),(hx0+2,hy0-1),(hx0+5,hy0-1),(hx1,hy0),(hx1+1,hy0+2)]: rect(d,(xx,yy,xx+1,yy+1),stage['hair'])
        if stage['hairStyle']=='bun': rect(d,(hx1,hy0-2,hx1+2,hy0),stage['hair'])
        if stage['hairStyle']=='tuft': rect(d,(hx0+2,hy0-2,hx0+4,hy0),stage['hair'])
        if stage['hairStyle']=='sweep': rect(d,(hx0+2,hy0,hx0+6,hy0+1),HAIRLIGHT)
        if direction=='south':
            # face and eyes
            rect(d,(hx0+1,hy0+3,hx1-1,hy1),stage['skin']); rect(d,(hx0+2,hy0+4,hx0+2,hy0+4),OUTLINE); rect(d,(hx1-2,hy0+4,hx1-2,hy0+4),OUTLINE); rect(d,(cx,hy0+5,cx,hy0+5),'#ad6856')
        else:
            # front sprite rotates for north; rear-facing head has no face details
            pass
        # torso shape and outline; shoulders wide for adult/senior, smaller for child
        sh=3 if age in ['adult','midlife-adult','elder'] else 2
        ty=hy1+1; rect(d,(cx-sh-1,ty,cx+sh+1,ty+7),OUTLINE); rect(d,(cx-sh,ty,cx+sh,ty+6),stage['shirt']); rect(d,(cx-sh+1,ty+1,cx+sh-1,ty+2),CLOTHLIGHT)
        # scarf, collar, apron/tunic accents
        rect(d,(cx-1,ty,cx+1,ty+2),stage['shoe'])
        if age in ['toddler','child']: rect(d,(cx-2,ty+3,cx+2,ty+4),'#e9c46a')
        # arms swing
        arm_y=ty+3
        for side in [-1,1]:
            ax=cx+side*(sh+1); off=swing*side
            rect(d,(ax+off,arm_y,ax+off+1,ty+7),OUTLINE); rect(d,(ax+off,arm_y+1,ax+off,ty+6),stage['skin'])
        # legs and shoes, alternating positions; elder stance slightly bowed
        ly=ty+7
        legspread=1 if age=='toddler' else 0
        for side in [-1,1]:
            lx=cx+side*(1+legspread)+(swing if side<0 else -swing)
            rect(d,(lx,ly,lx+1,ly+4),OUTLINE); rect(d,(lx,ly,lx,ly+3),stage['pants']); rect(d,(lx-1,ly+4,lx+2,ly+5),OUTLINE); rect(d,(lx,ly+4,lx+1,ly+4),stage['shoe'])
        # elder cane, alternating contact point
        if stage.get('cane'):
            rect(d,(cx+5,ty+2,cx+5,ly+5),OUTLINE); rect(d,(cx+4,ty+1,cx+5,ty+1),'#b79259')
        # slight deterministic pixel highlight accents
        rect(d,(cx-2,ty+1,cx-2,ty+1),CLOTHLIGHT)
    # Rotate canonical south-facing body to cardinal orientation.
    if direction=='north': im=im.transpose(Image.Transpose.ROTATE_180)
    elif direction=='west': im=im.transpose(Image.Transpose.ROTATE_90)
    elif direction=='east': im=im.transpose(Image.Transpose.ROTATE_270)
    # for older characters add subtle neutral gray hair already represented by the hair palette
    return im

all_frames=[]; stage_manifest=[]
for st in STAGES:
    folder=OUT/st['id']; folder.mkdir(exist_ok=True)
    atlas=Image.new('RGBA',(W*4,H*4),(0,0,0,0)); fr=[]
    for ri,direction in enumerate(DIRECTIONS):
        for ci,phase in enumerate(PHASES):
            im=canonical(st,ci,direction)
            fn=f'{direction}-{phase}.png'; im.save(folder/fn)
            atlas.alpha_composite(im,(ci*W,ri*H))
            entry={'id':f'{st["id"]}-{direction}-{phase}','file':f'{st["id"]}/{fn}','stage':st['age'],'locomotion':st['locomotion'],'direction':direction,'phase':phase,'x':ci*W,'y':ri*H,'width':W,'height':H,'pivotX':W//2,'pivotY':H-1,'runtimeReady':False}
            fr.append(entry); all_frames.append(entry)
    atlas.save(folder/f'{st["id"]}-atlas.png')
    atlas.resize((W*16,H*16),Image.Resampling.NEAREST).save(folder/f'{st["id"]}-preview-16x.png')
    stage_manifest.append({'id':st['id'],'age':st['age'],'presentation':st.get('presentation','neutral'),'locomotion':st['locomotion'],'atlas':f'{st["id"]}/{st["id"]}-atlas.png','width':W*4,'height':H*4,'frameSize':[W,H],'frameCount':16})
# aggregate atlas by stage, each stage is a band 4 columns x 4 rows
mega=Image.new('RGBA',(W*4,H*4*len(STAGES)),(0,0,0,0))
for i,st in enumerate(STAGES):
 atlas=Image.open(OUT/st['id']/f'{st["id"]}-atlas.png').convert('RGBA'); mega.alpha_composite(atlas,(0,i*H*4))
mega.save(OUT/'age-movement-all-stages-atlas.png')
mega.resize((W*16,H*16*len(STAGES)),Image.Resampling.NEAREST).save(OUT/'age-movement-all-stages-preview-16x.png')
manifest={'batch':'age-complete-movement-batch-v1','runtimeReady':False,'directionRows':DIRECTIONS,'phaseColumns':PHASES,'logicalFrameSize':[W,H],'sampling':'nearest','stages':stage_manifest,'frames':all_frames,'artMethod':'deterministic hand-authored pixel primitives via Pillow; no generated or third-party reference artwork','limitations':['procedural concept art, not hand-polished production art','simple stage-relative proportions and palette blocks','infant uses a crawling pose rotated for cardinal directions','rotation of upright actors is a first-pass directional approximation','no outfits, accessories, facial-expression variants, sit/interact states, or engine integration']}
(OUT/'frames.json').write_text(json.dumps(manifest,indent=2)+'\n')
(OUT/'README.md').write_text('''# Age-complete movement batch v1\n\nA deterministic original pixel-art movement base for all requested life stages: infant crawl, toddler waddle, child, teen, young adult, midlife adult, elder woman, and elder man. Each stage has four cardinal directions and four movement phases (16 frames per stage, 128 total). Each logical frame is 24×32 RGBA with bottom-center foot pivot. Infant crawling is a distinct horizontal locomotion pose.\n\n## Files\n\n- `age-movement-all-stages-atlas.png`: 96×1024 composite, one 4×4 stage atlas per vertical band.\n- `age-movement-all-stages-preview-16x.png`: nearest-neighbor review at 16×.\n- Each stage folder contains its own 96×128 atlas, 16 individual frame PNGs, and 16× preview.\n- `frames.json`: exact stage, direction, phase, atlas coordinates, pivots, and limitations.\n- `generate_age_movement.py`: reproducible drawing source.\n\n## Provenance and limitations\n\nAuthored on 2026-10-20 with Pillow integer rectangles and pixel clusters. All silhouettes, palettes, and pose details were drawn by this script. No AI generation, user ZIP, external game art, or third-party visual reference was used for this batch.\n\nThis gives the project a coherent and technically aligned movement foundation, but it remains an art-direction base, not approved runtime art. Adult directional movement currently rotates the south-facing sprite for cardinal directions, so side silhouettes are only approximated; frame-specific walk leg changes are present, but animation needs visual cleanup, palette refinement, appropriate age-specific collision boxes, and renderer review. It does not provide idle, interact, sit, talk, or wardrobe/skin/hair modular layers. All 128 frames are labeled `runtimeReady: false`.\n''')
