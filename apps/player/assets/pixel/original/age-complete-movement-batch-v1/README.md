# Age-complete movement batch v1

A deterministic procedural pixel-primitives experiment for all requested life stages: infant crawl, toddler waddle, child, teen, young adult, midlife adult, elder woman, and elder man. Each stage has four cardinal directions and four movement phases (16 frames per stage, 128 total). Each logical frame is 24×32 RGBA with bottom-center foot pivot. Infant crawling is a distinct horizontal locomotion pose.

## Files

- `age-movement-all-stages-atlas.png`: 96×1024 composite, one 4×4 stage atlas per vertical band.
- `age-movement-all-stages-preview-16x.png`: nearest-neighbor review at 16×.
- Each stage folder contains its own 96×128 atlas, 16 individual frame PNGs, and 16× preview.
- `frames.json`: exact stage, direction, phase, atlas coordinates, pivots, and limitations.
- `generate_age_movement.py`: reproducible drawing source.

## Provenance and limitations

Authored on 2026-10-20 with Pillow integer rectangles and pixel clusters. All silhouettes, palettes, and pose details were drawn by this script. No AI generation, user ZIP, external game art, or third-party visual reference was used for this batch.

This is a technical coverage mockup only. Its simplified silhouettes, rotated directions, limited details, and repeated-looking poses make it unsuitable as the visual target for the game; prefer the generated concept batches for art direction. It remains not approved runtime art. Adult directional movement currently rotates the south-facing sprite for cardinal directions, so side silhouettes are only approximated; frame-specific walk leg changes are present, but animation needs visual cleanup, palette refinement, appropriate age-specific collision boxes, and renderer review. It does not provide idle, interact, sit, talk, or wardrobe/skin/hair modular layers. All 128 frames are labeled `runtimeReady: false`.
