"""Derive review-only scene crops and transparent props from original source sheets.

The source sheets are preserved byte-for-byte. Outputs are concepts only and stay
runtimeReady=false until atlas packing, pivot review, and in-game staging pass.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "sources"
BG = ROOT / "backgrounds"
PROPS = ROOT / "props"
PREV = ROOT / "previews"
for d in (BG, PROPS, PREV): d.mkdir(exist_ok=True)

trip = Image.open(SRC / "exclusive-scene-triptych-source.png").convert("RGB")
tw, th = trip.size
names = ["graduation-garden", "new-parenthood-nursery", "elder-birthday-dining"]
# Remove the left icon strip and the two gutters. These are deliberate review crops.
left, right = 68, tw
panel_h = th // 3
for i, name in enumerate(names):
    y0 = i * panel_h + (0 if i == 0 else 4)
    y1 = (i + 1) * panel_h - (4 if i < 2 else 0)
    crop = trip.crop((left, y0, right, y1))
    crop.save(BG / f"{name}-flattened-concept.png")
    # A compact review export keeps the pixel grid legible in the catalog.
    crop.resize((640, 256), Image.Resampling.NEAREST).save(BG / f"{name}-320x128-review.png")
    guide = crop.resize((640, 256), Image.Resampling.NEAREST).convert("RGBA")
    overlay = Image.new("RGBA", guide.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle((int(guide.width*.22), int(guide.height*.28), int(guide.width*.78), int(guide.height*.88)), outline=(91, 223, 255, 210), width=3)
    draw.rectangle((0, int(guide.height*.72), guide.width, guide.height), fill=(26, 21, 46, 72), outline=(255, 210, 110, 200), width=3)
    Image.alpha_composite(guide, overlay).save(BG / f"{name}-placement-guide.png")

props = Image.open(SRC / "exclusive-props-source.png").convert("RGBA")
pw, ph = props.size
prop_names = [
    "graduation-mortarboard", "graduation-diploma", "graduation-bouquet", "graduation-bunting",
    "new-parenthood-bassinet", "new-parenthood-bottle", "new-parenthood-lamp", "new-parenthood-swaddle",
    "elder-birthday-cake", "elder-birthday-gift", "elder-birthday-teacup", "elder-birthday-photo",
]
cell_w, cell_h = pw // 4, ph // 3
for idx, name in enumerate(prop_names):
    col, row = idx % 4, idx // 4
    cell = props.crop((col*cell_w, row*cell_h, (col+1)*cell_w, (row+1)*cell_h))
    # Trim transparent margins and remove faint chromatic fringe only at nearly
    # transparent pixels; opaque source pixels are never altered.
    pix = cell.load()
    for y in range(cell.height):
        for x in range(cell.width):
            r, g, b, a = pix[x, y]
            if a <= 8 and max(r, g, b) - min(r, g, b) >= 40:
                pix[x, y] = (r, g, b, 0)
    bbox = cell.getbbox()
    if bbox:
        cell = cell.crop(bbox)
    cell.save(PROPS / f"{name}.png")

# A mock composite demonstrates layer order and actor-safe zones; it is not runtime art.
preview = Image.new("RGB", (960, 128), (18, 18, 28))
for i, name in enumerate(names):
    panel = Image.open(BG / f"{name}-320x128-review.png").convert("RGB").resize((320, 128), Image.Resampling.NEAREST)
    preview.paste(panel, (i*320, 0))
    d = ImageDraw.Draw(preview)
    d.rectangle((i*320+72, 20, i*320+248, 112), outline=(91,223,255), width=2)
    d.rectangle((i*320, 96, i*320+320, 128), fill=(26,21,46), outline=(255,210,110), width=2)
preview.save(PREV / "exclusive-scenes-layer-order-preview.png")
print("generated", len(list(BG.glob("*.png"))), "background/guide exports and", len(list(PROPS.glob("*.png"))), "transparent props")
