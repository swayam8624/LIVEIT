import hashlib, json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent
records = []
for p in sorted(root.rglob('*.png')):
    rel = p.relative_to(root).as_posix()
    im = Image.open(p)
    records.append({
        'path': rel,
        'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
        'width': im.width,
        'height': im.height,
        'mode': im.mode,
        'alpha': im.mode in ('RGBA', 'LA') or 'transparency' in im.info,
        'runtimeReady': False,
    })
out = {'batchId':'exclusive-scene-layers-v1','version':1,'runtimeReady':False,'records':records}
(root/'manifest.json').write_text(json.dumps(out, indent=2) + '\n')
print('records', len(records))
