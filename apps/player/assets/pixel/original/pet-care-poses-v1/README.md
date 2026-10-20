# Pet care and emotion pose concepts v1

This isolated batch contains original pixel-art concept sheets for cat, dog, and rabbit care state presentation. Each animal has six derived 96x128 RGBA frames: `idle`, `happy`, `worried`, `sleeping`, `care`, and `recovering`, plus a 576x128 atlas and a 2x nearest-neighbour preview.

The source sheets were generated specifically for this project with the built-in image generation tool. No ZIP, marketplace, or internet artwork was used as an input. Source sheets are retained unchanged for provenance; `build_care_poses.py` only derives the transparent frames and previews from those sources.

These are concept assets, not runtime-ready game art. They have no engine import registration, animation timing, collision/pivot review, or gameplay integration. Keep `runtimeReady: false` in every manifest until those gates are completed.

Regenerate derived files with:

```sh
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 build_care_poses.py
```
