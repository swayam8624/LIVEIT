"""Make transparent placement guides for v2 generated composite concepts."""
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).parent
W, H = 320, 256
SCENES = {
    "garden-graduation": [(115, 190, 36, 58), (205, 193, 36, 58)],
    "new-parenthood-home": [(108, 190, 38, 58), (205, 190, 38, 58), (160, 179, 30, 24)],
    "elder-farewell-legacy": [(188, 188, 46, 62), (126, 193, 38, 57)],
}

for scene, boxes in SCENES.items():
    out = np.zeros((H, W, 4), dtype=np.uint8)
    cv2.rectangle(out, (42, 232), (278, 255), (210, 180, 90, 100), 1)
    for i, (x, y, w, h) in enumerate(boxes):
        color = (90, 180, 190, 160) if i < 2 else (210, 130, 120, 160)
        cv2.rectangle(out, (x - w // 2, y - h), (x + w // 2, y), color, 1)
        cv2.drawMarker(out, (x, y), color, cv2.MARKER_CROSS, 7, 1)
    cv2.imwrite(str(ROOT / f"{scene}-layout-guide.png"), out)
