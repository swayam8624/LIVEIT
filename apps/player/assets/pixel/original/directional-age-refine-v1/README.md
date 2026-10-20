# Directional age refinement v1

This batch is an original, rights-safe pixel-cluster study for the life arc:
infant crawl, toddler waddle, child walk, teen walk, adult walk, elder woman
walk, and elder man walk. Every stage has directly drawn south, west, east, and
north rows with four phases (`contact-a`, `passing-a`, `contact-b`,
`passing-b`). The logical frame is 24×32 pixels, sampled with nearest-neighbor,
and every frame uses the same feet pivot `(12, 31)`.

The sprites were hand-authored as deterministic Pillow primitives in
`build_directional_age.py`. No supplied ZIP, third-party sprite, web image, or
external archive was used. The source contact sheet and exact palette are
retained beside the derived atlases. `manifest.json` records every frame and
keeps `runtimeReady: false`.

## Files

- `directional-age-refine-source.png`: source contact sheet, one stage per row.
- `directional-age-refine-preview-4x.png`: nearest-neighbor review preview.
- `frames/<stage>/<stage>-atlas.png`: 4×4 directional atlas per stage.
- `frames/<stage>/*.png`: individual 24×32 transparent frames.
- `manifest.json`: frame coordinates, pivots, palette, and limitations.
- `build_directional_age.py`: reproducible generator.

This is not a runtime-ready character pack. The small logical resolution needs
artist review for anatomy, clothing variants, shadows, collision boxes, and
identity continuity. The elder man cane is an accessory study only. Integrate
only after visual cleanup, renderer sampling checks, and the game's collision
and appearance-slot review.

Rebuild from this folder with:

```sh
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 build_directional_age.py
```
