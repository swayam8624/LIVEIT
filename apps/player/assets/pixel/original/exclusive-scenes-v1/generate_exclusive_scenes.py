"""Generate the rights-safe exclusive-scene pixel plates.

The renderer is intentionally small and deterministic: integer rectangles and
polygons, a shared authored palette, and no fonts, source images, or network
inputs.  The output is concept art and stays runtimeReady=false in the manifest.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).parent
W, H = 320, 256
P = {
    "ink": (35, 30, 52, 255), "deep": (45, 46, 75, 255), "night": (55, 61, 92, 255),
    "sky": (92, 115, 139, 255), "mist": (146, 159, 159, 255), "cream": (242, 213, 156, 255),
    "gold": (215, 157, 77, 255), "coral": (201, 102, 93, 255), "rose": (163, 77, 93, 255),
    "teal": (65, 133, 130, 255), "leaf": (68, 104, 77, 255), "sage": (119, 148, 103, 255),
    "brick": (133, 76, 68, 255), "wood": (98, 60, 55, 255), "paper": (241, 224, 180, 255),
    "skin1": (201, 139, 108, 255), "skin2": (163, 100, 82, 255), "hair": (49, 39, 51, 255),
    "silver": (184, 182, 167, 255), "white": (252, 242, 204, 255),
}


class Canvas:
    def __init__(self, alpha: bool, pixels=None):
        self.alpha = alpha
        if pixels is not None:
            self.pixels = pixels.copy()
        else:
            channels = 4 if alpha else 3
            fill = (0, 0, 0, 0) if alpha else P["sky"][:3]
            self.pixels = np.zeros((H, W, channels), dtype=np.uint8)
            self.pixels[:] = fill

    def copy(self): return Canvas(self.alpha, self.pixels)
    def convert(self, mode):
        if mode == "RGB" and self.alpha:
            return Canvas(False, self.pixels[:, :, :3])
        return self
    def alpha_composite(self, over):
        if self.pixels.shape[2] == 3:
            base = np.dstack((self.pixels, np.full((H, W), 255, dtype=np.uint8)))
        else:
            base = self.pixels
        src = over.pixels if over.pixels.shape[2] == 4 else np.dstack((over.pixels, np.full((H, W), 255, dtype=np.uint8)))
        sa = src[:, :, 3:4].astype(np.float32) / 255.0
        da = base[:, :, 3:4].astype(np.float32) / 255.0
        outa = sa + da * (1 - sa)
        rgb = (src[:, :, :3] * sa + base[:, :, :3] * da * (1 - sa)) / np.maximum(outa, 1e-6)
        self.pixels = np.dstack((rgb.clip(0, 255).astype(np.uint8), (outa * 255).clip(0, 255).astype(np.uint8)))
        self.alpha = True
    def save(self, path):
        data = self.pixels[:, :, ::-1] if self.pixels.shape[2] == 3 else self.pixels[:, :, [2, 1, 0, 3]]
        cv2.imwrite(str(path), data)


class ImageDraw:
    @staticmethod
    def Draw(canvas): return canvas


def img(alpha: bool) -> Canvas:
    return Canvas(alpha)


def color(c): return P[c] if isinstance(c, str) else c
def rect(d, box, c):
    x1, y1, x2, y2 = [int(v) for v in box]
    d.pixels[y1:y2 + 1, x1:x2 + 1, :] = color(c)[:d.pixels.shape[2]]
def poly(d, points, c):
    cv2.fillPoly(d.pixels, [np.asarray(points, dtype=np.int32)], color(c)[:d.pixels.shape[2]])


def person(d, x, y, shirt, skin="skin1", hair="hair", scale=1, cap=False):
    # A compact portrait cutout with a readable silhouette at native size.
    s = scale
    rect(d, (x-10*s, y+22*s, x+10*s, y+46*s), shirt)
    rect(d, (x-7*s, y+8*s, x+7*s, y+23*s), skin)
    rect(d, (x-8*s, y+5*s, x+8*s, y+11*s), hair)
    rect(d, (x-9*s, y+10*s, x-7*s, y+19*s), hair)
    rect(d, (x+7*s, y+10*s, x+9*s, y+19*s), hair)
    rect(d, (x-4*s, y+14*s, x-2*s, y+16*s), "ink")
    rect(d, (x+2*s, y+14*s, x+4*s, y+16*s), "ink")
    rect(d, (x-4*s, y+20*s, x+4*s, y+22*s), "coral")
    if cap:
        rect(d, (x-11*s, y+3*s, x+11*s, y+7*s), "deep")
        rect(d, (x-5*s, y-1*s, x+5*s, y+3*s), "deep")


def graduation():
    bg, mid, fg, a1, a2 = img(False), img(True), img(True), img(True), img(True)
    d = ImageDraw.Draw(bg); rect(d, (0, 0, W, H), "sky"); rect(d, (0, 0, W, 106), "night")
    rect(d, (18, 32, 302, 139), "brick"); rect(d, (27, 43, 293, 133), "deep")
    rect(d, (52, 62, 268, 115), "sky"); rect(d, (0, 140, W, H), "leaf")
    for x in range(8, 320, 22): rect(d, (x, 177, x+3, 196), "sage")
    rect(d, (95, 124, 225, 143), "wood"); rect(d, (105, 116, 215, 128), "paper")
    # Paper lanterns and a string of lights make this a distinct garden ceremony.
    for x, c in ((48, "gold"), (91, "coral"), (230, "gold"), (273, "coral")):
        rect(d, (x-5, 48, x+5, 61), c); rect(d, (x-2, 44, x+2, 48), "paper")
    for x in range(28, 294, 18): rect(d, (x, 28+(x%3)*2, x+3, 31+(x%3)*2), "cream")
    d = ImageDraw.Draw(mid); rect(d, (72, 147, 248, 185), "wood"); rect(d, (80, 142, 240, 151), "paper")
    for x in (91, 130, 169, 208): rect(d, (x, 149, x+10, 159), "gold")
    rect(d, (145, 133, 175, 142), "paper"); rect(d, (149, 129, 171, 133), "coral")
    # foreground leaves frame a clean dialogue-safe band in the lower centre.
    d = ImageDraw.Draw(fg); poly(d, [(0, 256), (0, 199), (18, 183), (32, 200), (25, 256)], "deep")
    poly(d, [(320, 256), (320, 187), (298, 202), (291, 256)], "deep")
    person(ImageDraw.Draw(a1), 116, 135, "teal", "skin1", "hair", 2, True)
    person(ImageDraw.Draw(a2), 207, 140, "coral", "skin2", "hair", 2, True)
    return "garden-graduation", [bg, mid, fg, a1, a2]


def parenthood():
    bg, mid, fg, a1, a2 = img(False), img(True), img(True), img(True), img(True)
    d = ImageDraw.Draw(bg); rect(d, (0, 0, W, H), "cream"); rect(d, (0, 0, W, 18), "wood")
    rect(d, (18, 34, 127, 126), "teal"); rect(d, (25, 41, 120, 119), "sky")
    rect(d, (31, 47, 114, 113), "mist"); rect(d, (195, 30, 302, 128), "paper")
    rect(d, (208, 45, 290, 52), "coral"); rect(d, (208, 61, 275, 68), "gold")
    rect(d, (0, 132, W, H), "sage"); rect(d, (0, 164, W, 170), "leaf")
    rect(d, (141, 55, 180, 118), "wood"); rect(d, (146, 62, 175, 112), "deep")
    for x in (151, 162, 173): rect(d, (x, 71, x+5, 95), "coral")
    d = ImageDraw.Draw(mid); rect(d, (93, 152, 239, 201), "paper"); rect(d, (100, 146, 232, 157), "wood")
    rect(d, (119, 159, 213, 186), "cream"); rect(d, (152, 160, 181, 177), "coral")
    rect(d, (164, 164, 183, 180), "skin1"); rect(d, (166, 161, 180, 166), "hair")
    rect(d, (87, 195, 245, 202), "wood")
    d = ImageDraw.Draw(fg); poly(d, [(0, 256), (0, 206), (19, 193), (38, 211), (29, 256)], "teal")
    for x in (11, 26, 301): rect(d, (x, 179+(x%4)*5, x+5, 218), "leaf")
    person(ImageDraw.Draw(a1), 119, 136, "coral", "skin1", "hair", 2)
    person(ImageDraw.Draw(a2), 207, 140, "teal", "skin2", "hair", 2)
    return "new-baby-parenthood", [bg, mid, fg, a1, a2]


def farewell():
    bg, mid, fg, a1, a2 = img(False), img(True), img(True), img(True), img(True)
    d = ImageDraw.Draw(bg); rect(d, (0, 0, W, H), "deep"); rect(d, (0, 0, W, 123), "night")
    rect(d, (25, 28, 295, 126), "wood"); rect(d, (34, 38, 286, 115), "deep")
    rect(d, (47, 48, 132, 103), "sky"); rect(d, (188, 47, 273, 103), "sky")
    rect(d, (0, 126, W, H), "brick"); rect(d, (0, 158, W, 166), "wood")
    rect(d, (142, 39, 178, 103), "paper"); rect(d, (148, 47, 172, 96), "cream")
    rect(d, (153, 55, 168, 67), "gold"); rect(d, (151, 74, 170, 80), "coral")
    d = ImageDraw.Draw(mid); rect(d, (99, 143, 220, 191), "wood"); rect(d, (106, 136, 214, 148), "paper")
    rect(d, (130, 149, 190, 181), "cream"); rect(d, (145, 154, 177, 174), "paper")
    rect(d, (151, 158, 171, 162), "coral"); rect(d, (151, 166, 170, 170), "teal")
    d = ImageDraw.Draw(fg); poly(d, [(0, 256), (0, 204), (22, 184), (47, 207), (37, 256)], "ink")
    poly(d, [(320, 256), (320, 201), (297, 182), (279, 210), (288, 256)], "ink")
    for x, y in ((27, 179), (294, 177), (16, 192), (304, 191)):
        rect(d, (x, y, x+6, y+24), "sage"); rect(d, (x-5, y+5, x+10, y+10), "sage")
    person(ImageDraw.Draw(a1), 119, 133, "teal", "skin1", "silver", 2)
    person(ImageDraw.Draw(a2), 207, 140, "coral", "skin2", "hair", 2)
    return "elder-farewell-legacy", [bg, mid, fg, a1, a2]


def save_scene(scene_id, plates):
    names = ["background", "midground-props", "foreground-framing", "actor-primary-portrait", "actor-secondary-portrait"]
    for name, im in zip(names, plates):
        # Background stays RGB; every staging/actor plate deliberately keeps alpha.
        out = im.convert("RGB") if name == "background" else im
        out.save(ROOT / f"{scene_id}-{name}.png")
    comp = plates[0].copy()
    for plate in plates[1:]: comp.alpha_composite(plate)
    comp.save(ROOT / f"{scene_id}-composite-preview.png")


def main():
    scenes = [graduation(), parenthood(), farewell()]
    manifest = {
        "batch": "exclusive-scenes-v1", "canvas": {"width": W, "height": H},
        "runtimeReady": False, "layerOrder": ["background", "midground-props", "actor-primary-portrait", "actor-secondary-portrait", "foreground-framing"],
        "scenes": [], "provenance": {"tool": "deterministic authored procedural pixel renderer", "date": "2026-10-20", "thirdPartyAssetsUsed": False, "suppliedArchivesUsed": False, "externalReferencesUsed": False, "prompt": "Original rights-safe pixel scene plates for graduation, new parenthood, and elder farewell/legacy memory; 320x256, hard nearest-neighbor clusters, shared dusk/lamplight palette, no text or logos."}
    }
    for scene_id, plates in scenes:
        save_scene(scene_id, plates)
        records = []
        names = ["background", "midground-props", "foreground-framing", "actor-primary-portrait", "actor-secondary-portrait"]
        for i, name in enumerate(names):
            path = ROOT / f"{scene_id}-{name}.png"
            records.append({"file": path.name, "role": name, "width": W, "height": H, "alpha": name != "background", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "runtimeReady": False})
        comp = ROOT / f"{scene_id}-composite-preview.png"
        records.append({"file": comp.name, "role": "composite-preview", "width": W, "height": H, "alpha": True, "sha256": hashlib.sha256(comp.read_bytes()).hexdigest(), "runtimeReady": False})
        primary_y = 225 if scene_id == "elder-farewell-legacy" else 227
        manifest["scenes"].append({"id": scene_id, "dialogueSafeRegion": {"x": 42, "y": 232, "width": 236, "height": 24}, "anchors": {"primary": {"x": 119, "y": primary_y, "pivot": "bottom-center"}, "secondary": {"x": 207, "y": 232, "pivot": "bottom-center"}}, "layers": records, "runtimeReady": False})
    (ROOT / "layers.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
