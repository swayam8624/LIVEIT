from pathlib import Path

import struct
import zlib


ROOT = Path(__file__).parent
W, H = 320, 256


def color(value):
    if isinstance(value, tuple):
        return value if len(value) == 4 else (*value, 255)
    value = value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4)) + (255,)


class MiniDraw:
    def __init__(self, image):
        self.image = image

    def rectangle(self, box, fill, outline=None):
        x0, y0, x1, y1 = box
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                if outline and (x in (x0, x1) or y in (y0, y1)):
                    self.image.set(x, y, color(outline))
                else:
                    self.image.set(x, y, color(fill))

    def line(self, coords, fill, width=1):
        x0, y0, x1, y1 = coords
        steps = max(abs(x1 - x0), abs(y1 - y0)) or 1
        for i in range(steps + 1):
            x = round(x0 + (x1 - x0) * i / steps)
            y = round(y0 + (y1 - y0) * i / steps)
            for oy in range(width):
                for ox in range(width):
                    self.image.set(x + ox, y + oy, color(fill))


class MiniImage:
    def __init__(self, rgba=True, fill=(0, 0, 0, 0)):
        self.rgba = rgba
        self.pixels = [color(fill)] * (W * H)

    def set(self, x, y, value):
        if 0 <= x < W and 0 <= y < H:
            self.pixels[y * W + x] = value

    def save(self, path, optimize=True):
        rows = b"".join(b"\x00" + bytes(sum((list(px) if self.rgba else list(px[:3]) for px in self.pixels[y * W:(y + 1) * W]), [])) for y in range(H))
        raw = zlib.compress(rows, 9)
        def chunk(kind, data):
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
        channels = 6 if self.rgba else 2
        header = struct.pack(">IIBBBBB", W, H, 8, channels, 0, 0, 0)
        path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", raw) + chunk(b"IEND", b""))


class ImageFacade:
    @staticmethod
    def alpha_composite(base, overlay):
        result = MiniImage(True)
        for i, (b, o) in enumerate(zip(base.pixels, overlay.pixels)):
            oa = o[3] / 255
            ba = b[3] / 255
            a = oa + ba * (1 - oa)
            if a == 0:
                result.pixels[i] = (0, 0, 0, 0)
            else:
                result.pixels[i] = tuple(round((o[c] * oa + b[c] * ba * (1 - oa)) / a) for c in range(3)) + (round(a * 255),)
        return result


def new_layer(alpha=True):
    return MiniImage(alpha, (0, 0, 0, 0) if alpha else (28, 25, 35))


def rect(draw, box, fill, outline=None):
    draw.rectangle(box, fill=fill, outline=outline)


def background():
    im = new_layer(False)
    d = MiniDraw(im)
    # Warm dusk interior: wall, tiled floor, and window light.
    rect(d, (0, 0, 319, 173), "#49384a")
    rect(d, (0, 0, 319, 12), "#2d2736")
    rect(d, (0, 143, 319, 173), "#3d3040")
    rect(d, (0, 174, 319, 255), "#785747")
    for y in range(176, 256, 16):
        rect(d, (0, y, 319, y + 1), "#5e443e")
    for x in range(-16, 352, 32):
        d.line((x, 174, x + 34, 255), fill="#654942", width=1)
    # Left rain window and mullions.
    rect(d, (15, 28, 108, 119), "#6f91a0", "#2d2a3b")
    rect(d, (20, 33, 103, 114), "#87a9ad")
    rect(d, (60, 33, 63, 114), "#425565")
    rect(d, (20, 67, 103, 70), "#425565")
    for x, y in [(29, 44), (46, 86), (78, 52), (91, 96), (32, 103), (84, 77)]:
        d.line((x, y, x - 4, y + 12), fill="#bfd0c0", width=1)
    rect(d, (11, 120, 112, 128), "#2e2938")
    # Shelving and coffee counter in the back.
    rect(d, (126, 31, 297, 110), "#2b2937")
    rect(d, (132, 37, 291, 104), "#5c3c39")
    for y in (57, 79, 101):
        rect(d, (132, y, 291, y + 3), "#2d2733")
    for x in (151, 181, 212, 244, 275):
        rect(d, (x, 37, x + 3, 104), "#342b37")
    for x, y, c in [(137, 42, "#c27a55"), (157, 62, "#7fb0a0"), (185, 42, "#d59b5a"), (218, 84, "#9c6d83"), (250, 63, "#d2b17c"), (280, 42, "#7992a8"), (270, 84, "#c77b5d")]:
        rect(d, (x, y, x + 10, y + 12), c)
    rect(d, (123, 108, 301, 119), "#a16b4c")
    rect(d, (117, 119, 306, 128), "#3a2b36")
    # Pendant lamps and wall art, with no lettering.
    rect(d, (137, 13, 139, 34), "#242332")
    rect(d, (133, 34, 143, 39), "#d2a25d")
    rect(d, (137, 39, 139, 43), "#f4c76f")
    rect(d, (246, 13, 248, 34), "#242332")
    rect(d, (242, 34, 252, 39), "#d2a25d")
    rect(d, (246, 39, 248, 43), "#f4c76f")
    rect(d, (287, 16, 306, 48), "#302a3d", "#211e2c")
    rect(d, (291, 20, 302, 43), "#b65d54")
    rect(d, (294, 24, 299, 38), "#e5b466")
    # Door and wall plant silhouette at far right.
    rect(d, (10, 139, 43, 172), "#3a2d3b")
    rect(d, (14, 143, 39, 168), "#594557")
    rect(d, (296, 115, 317, 173), "#2b2838")
    rect(d, (302, 137, 311, 140), "#9a6749")
    return im


def stage():
    im = new_layer()
    d = MiniDraw(im)
    # Empty café table and two chairs as a modular staging plate.
    rect(d, (85, 159, 247, 169), "#3a2932")
    rect(d, (91, 169, 241, 178), "#986044")
    rect(d, (102, 178, 113, 229), "#472f35")
    rect(d, (219, 178, 230, 229), "#472f35")
    rect(d, (73, 171, 89, 213), "#55383b")
    rect(d, (77, 166, 85, 174), "#a56d4a")
    rect(d, (238, 171, 254, 213), "#55383b")
    rect(d, (242, 166, 250, 174), "#a56d4a")
    # Small cup and saucer, deliberately separated from actors.
    rect(d, (156, 151, 178, 154), "#2d2632")
    rect(d, (159, 143, 175, 152), "#d3af7d")
    rect(d, (162, 141, 172, 144), "#efe0b2")
    rect(d, (175, 145, 181, 150), "#d3af7d")
    # Book and candle.
    rect(d, (188, 148, 209, 153), "#4b6680")
    rect(d, (192, 143, 205, 148), "#9ab2b0")
    rect(d, (130, 147, 135, 159), "#d9b56c")
    rect(d, (131, 143, 134, 147), "#f3d17c")
    # Soft contact shadows for independent actor anchors.
    rect(d, (111, 202, 145, 207), (39, 30, 40, 150))
    rect(d, (180, 202, 214, 207), (39, 30, 40, 150))
    return im


def actor_amelia():
    im = new_layer()
    d = MiniDraw(im)
    # Amelia portrait, transparent cutout, 44x92 logical footprint centered at anchor.
    skin, hair, dress, scarf = "#d99573", "#5b3040", "#31555b", "#d2a55b"
    rect(d, (137, 84, 173, 122), hair)
    rect(d, (142, 91, 169, 119), skin)
    rect(d, (139, 86, 146, 108), hair)
    rect(d, (166, 87, 174, 108), hair)
    rect(d, (147, 96, 151, 100), "#382735")
    rect(d, (160, 96, 164, 100), "#382735")
    rect(d, (150, 108, 160, 111), "#8a4450")
    rect(d, (133, 120, 178, 161), dress)
    rect(d, (141, 119, 168, 128), scarf)
    rect(d, (130, 128, 140, 157), skin)
    rect(d, (171, 128, 180, 157), skin)
    rect(d, (141, 158, 151, 166), skin)
    rect(d, (161, 158, 171, 166), skin)
    rect(d, (136, 164, 153, 169), "#2a2634")
    rect(d, (159, 164, 176, 169), "#2a2634")
    return im


def actor_player():
    im = new_layer()
    d = MiniDraw(im)
    skin, hair, coat, shirt = "#c98368", "#844e37", "#6f4e67", "#d5bb84"
    rect(d, (194, 84, 230, 122), hair)
    rect(d, (199, 91, 226, 119), skin)
    rect(d, (196, 87, 204, 108), hair)
    rect(d, (222, 86, 231, 106), hair)
    rect(d, (204, 97, 208, 101), "#382735")
    rect(d, (216, 97, 220, 101), "#382735")
    rect(d, (207, 109, 217, 112), "#8a4450")
    rect(d, (190, 120, 236, 161), coat)
    rect(d, (203, 120, 224, 143), shirt)
    rect(d, (187, 128, 197, 157), skin)
    rect(d, (230, 128, 239, 157), skin)
    rect(d, (198, 158, 208, 166), skin)
    rect(d, (219, 158, 229, 166), skin)
    rect(d, (193, 164, 210, 169), "#2a2634")
    rect(d, (217, 164, 234, 169), "#2a2634")
    return im


def foreground():
    im = new_layer()
    d = MiniDraw(im)
    # Transparent edge foliage and hanging lamp framing the dialogue-safe center.
    rect(d, (0, 208, 8, 256), "#283d3c")
    for box in [(4, 193, 16, 212), (0, 181, 12, 198), (11, 215, 24, 236), (22, 201, 35, 224)]:
        rect(d, box, "#3e6854")
    rect(d, (309, 215, 319, 256), "#27393b")
    for box in [(292, 209, 307, 232), (303, 192, 319, 216), (285, 228, 301, 248)]:
        rect(d, box, "#41664f")
    rect(d, (17, 232, 50, 238), "#372b35")
    rect(d, (22, 225, 45, 233), "#7e553f")
    # Foreground lamp at upper-right, kept away from camera-safe dialogue band.
    rect(d, (270, 0, 272, 24), "#1f202d")
    rect(d, (263, 24, 279, 29), "#bd8750")
    rect(d, (265, 29, 277, 34), "#e5b763")
    return im


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    layers = {
        "background-cafe-interior.png": background(),
        "midground-table-staging.png": stage(),
        "actor-amelia-portrait.png": actor_amelia(),
        "actor-player-portrait.png": actor_player(),
        "foreground-plants-lamp.png": foreground(),
    }
    for name, image in layers.items():
        image.save(ROOT / name, optimize=True)
    composite = ImageFacade.alpha_composite(layers["background-cafe-interior.png"], layers["midground-table-staging.png"])
    composite = ImageFacade.alpha_composite(composite, layers["actor-amelia-portrait.png"])
    composite = ImageFacade.alpha_composite(composite, layers["actor-player-portrait.png"])
    composite = ImageFacade.alpha_composite(composite, layers["foreground-plants-lamp.png"])
    composite.save(ROOT / "cafe-composite-preview.png", optimize=True)


if __name__ == "__main__":
    main()
