"""Create exact-size nearest-neighbor exports and alpha layout guides.

The source PNGs in each district folder are preserved built-in imagegen outputs.
This script only derives review exports and transparent, non-runtime staging guides.
"""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).parent
SIZE = (320, 256)
DISTRICTS = {
    "university": "university-quad",
    "studio": "studio-district",
    "gardens": "gardens-courtyard",
}


def make_guide() -> Image.Image:
    guide = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(guide)
    # Dialogue-safe band: intentionally transparent except for a review outline.
    draw.rectangle((0, 204, 319, 255), outline=(255, 232, 112, 190), width=2)
    draw.line((0, 204, 319, 204), fill=(255, 232, 112, 220), width=2)
    # Central actor staging lane and side pockets.
    draw.rectangle((96, 66, 224, 199), outline=(116, 224, 232, 150), width=1)
    draw.rectangle((20, 84, 92, 199), outline=(116, 224, 232, 110), width=1)
    draw.rectangle((228, 84, 300, 199), outline=(116, 224, 232, 110), width=1)
    return guide


for district, stem in DISTRICTS.items():
    folder = ROOT / district
    source = folder / f"{stem}-source.png"
    export = folder / f"{stem}-320x256.png"
    with Image.open(source) as image:
        image.convert("RGB").resize(SIZE, Image.Resampling.NEAREST).save(export, optimize=True)
    make_guide().save(folder / f"{stem}-layout-guide.png", optimize=True)
