# Exclusive scene variety v1

Four original pixel-art scene concepts widen the story-event palette beyond graduation, new parenthood, elder legacy, and first home:

- **First paycheck, after closing** — earned relief and quiet pride.
- **A difficult reunion after rain** — apology and cautious hope.
- **A shared harvest table** — belonging and celebration.
- **Room to begin again** — grief settling into agency and possibility.

Each scene has an unmodified generated source in `sources/`, a 320×256 32-color concept export in `scenes/`, and a transparent placement guide in `guides/`. `previews/exclusive-scenes-variety-review-2x.png` is a four-panel, nearest-neighbor review sheet with the guides overlaid. Prompts, generator provenance, hashes, dimensions, alpha expectations, dialogue-safe regions, and `runtimeReady: false` are recorded in `prompts.md` and `manifest.json`.

## Build

Requires Python 3 and Pillow. From the repository root:

```sh
python3 apps/player/assets/pixel/original/exclusive-scenes-variety-v1/build_scene_variety.py
```

The builder preserves all source files and deterministically regenerates concept exports, guides, the review sheet, and manifest. The concept exports resize the generated source to 320×256 and quantize to 32 colors without dithering. The preview sheet scales concepts 2× with nearest-neighbor filtering.

## Review limits and exact gaps

These are concept assets, not integrated game content. The supplied exports are flattened RGB backdrops; actor-safe rectangles and dialogue-safe bands are placement suggestions only. The generated sources retain detailed, soft pixel texture and need human cleanup to match the game's crisp sprite-cluster standard. There are no separated background/midground/foreground plates, transparent scene props, authored collision/portal maps, actor sprites, narrative graph, runtime catalog entries, or renderer/native-device review. No asset is `runtimeReady`.

No user-supplied archive or external asset was used.
