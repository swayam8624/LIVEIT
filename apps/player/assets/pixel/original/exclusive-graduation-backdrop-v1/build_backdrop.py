from __future__ import annotations
import hashlib, json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
SOURCE = ROOT / 'source.png'
PROMPT = '''Use case: illustration-story
Asset type: exclusive story-scene background concept for a top-down pixel life simulator
Primary request: create an original, beautiful graduation ceremony courtyard backdrop, suitable to become a crisp 320x256 logical-pixel game scene after nearest-neighbor normalization
Scene/backdrop: a small welcoming neighborhood school courtyard with brick arches, a modest stage, leafy trees, bunting, flower planters, and warm late-afternoon light; no recognizable real-world location
Composition/framing: 5:4 landscape; stage and diploma table at upper center, clear uncluttered actor-safe floor across the lower half, generous readable silhouettes, purposeful foreground/midground/background depth
Style/medium: exceptionally polished classic handheld-era pixel art; intentional square pixel clusters, limited coherent palette, crisp stepped edges, no anti-aliasing, no painterly blur, no gradients made of tiny noise; handcrafted richly detailed environment tiles and light clusters
Lighting/mood: joyful, intimate, sentimental, golden-hour celebration; warm sunlight with cool green-blue shadow grouping
Color palette: restrained warm brick, cream stone, leafy greens, muted teal shadows, gold-orange accents, soft sky blue
Constraints: background plate only, no people, no portraits, no text, no lettering, no logos, no watermark, no UI; preserve the lower central floor as a clean character staging area; keep all detail aligned to a consistent visible pixel grid; original fictional game art with no supplied ZIP, no third-party sprite references'''

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> None:
    with Image.open(SOURCE) as image:
        source = image.convert('RGB')
        w, h = source.size
        target_ratio = 5 / 4
        if w / h > target_ratio:
            crop_w = round(h * target_ratio)
            left = (w - crop_w) // 2
            source = source.crop((left, 0, left + crop_w, h))
        else:
            crop_h = round(w / target_ratio)
            top = (h - crop_h) // 2
            source = source.crop((0, top, w, top + crop_h))
        logical = source.resize((320, 256), Image.Resampling.LANCZOS)
    records=[]
    for colors in (32, 64):
        out = logical.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
        path = ROOT / f'graduation-courtyard-{colors}-color-320x256.png'
        out.save(path, optimize=True)
        records.append({'file':path.name,'size':[320,256],'mode':'RGB','paletteColors':colors,'sha256':sha(path),'runtimeReady':False})
        if colors == 32:
            preview = out.resize((960,768),Image.Resampling.NEAREST)
            preview_path=ROOT/'graduation-courtyard-preview-3x.png'
            preview.save(preview_path,optimize=True)
    manifest={
      'schemaVersion':1,'id':'exclusive-graduation-backdrop-v1','runtimeReady':False,
      'conceptQuality':'ImageGen source has soft painterly texture; normalized exports are pixel-art studies requiring manual review and scene composition validation.',
      'source':{'file':'source.png','size':list(Image.open(SOURCE).size),'mode':'RGB','sha256':sha(SOURCE),'tool':'built-in image_gen','prompt':PROMPT},
      'builder':{'file':'build_backdrop.py','sha256':sha(Path(__file__))},
      'exports':records,
      'preview':{'file':preview_path.name,'size':[960,768],'sha256':sha(preview_path),'runtimeReady':False},
      'constraints':{'scene':'graduation courtyard','actorSafeRegion':'lower central courtyard floor','thirdPartyArtUsed':False,'providedZipUsed':False,'externalImageUsed':False}
    }
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (ROOT/'README.md').write_text('''# Exclusive graduation courtyard backdrop v1\n\nThis isolated original concept batch adds a warm neighborhood-school courtyard for graduation scenes. The built-in ImageGen source provides the composition, stage and open actor-safe foreground. The source is detailed and softly rendered; the 32- and 64-color exports are nearest logical-size palette studies, not approved runtime art.\n\n## Files\n\n- `source.png`: retained generated source image.\n- `graduation-courtyard-32-color-320x256.png`: 320×256 limited-palette export.\n- `graduation-courtyard-64-color-320x256.png`: 320×256 alternate palette export.\n- `graduation-courtyard-preview-3x.png`: nearest-neighbor review preview.\n- `manifest.json`: exact prompt, source/export hashes, dimensions and readiness status.\n- `build_backdrop.py`: reproducible normalization script.\n\n## Review boundary\n\nThe image was newly generated; no supplied ZIP contents, downloaded assets, third-party art, logos, or fonts were used. The export still needs pixel-artist review, layer/depth separation, collision and walkability authoring, actor-safe-region validation, palette approval, and actual renderer integration. Every export remains `runtimeReady: false`.\n\nRebuild with Python Pillow:\n\n```sh\npython3 build_backdrop.py\n```\n''')
    print('Built 2 limited-palette exports and preview from source',Image.open(SOURCE).size)

if __name__=='__main__': main()
