# Bellweather tile concepts v1

An isolated, original 16×16 top-down pixel tile concept batch for the Bellweather neighborhood and café direction. This folder is a visual exploration only. It is not connected to the player bundle, runtime tile catalog, collision maps, portals, or production asset status.

## Contents

- `bellweather-tile-atlas-v1.png` — 128×64 RGBA atlas, 8 columns × 4 rows, with 32 exact 16×16 cells.
- `bellweather-tile-atlas-preview-6x.png` — nearest-neighbor review image for inspecting the native clusters.
- `bellweather-staging-map-v1.png` — 256×160 RGBA concept map, 16×10 cells, assembled only from the atlas.
- `bellweather-staging-map-preview-4x.png` — nearest-neighbor review image of the staging map.
- `tiles.json` — stable tile IDs, exact atlas coordinates, pivots, provisional collision hints, map dimensions, hashes, provenance, and limitations.
- `generate_concepts.py` — deterministic Pillow authoring source used to produce the PNGs and metadata.

## Atlas coordinate guide

Coordinates in `tiles.json` are pixel coordinates from the top-left of the atlas. Every entry has `width: 16`, `height: 16`, a zero-based `column` and `row`, and a provisional pivot at `(8, 15)`.

| Atlas row | Coverage                                                                   |
| --------- | -------------------------------------------------------------------------- |
| 0         | street, sidewalk, curbs, crosswalk, manhole, puddle, storm drain           |
| 1         | grass, flower grass, hedge, dirt, brick wall/corner, window, door          |
| 2         | wood floor, tile floor, rug, counter, table, chair, shelf, interior window |
| 3         | rain, snow, leaf scatter, lamp, planter, bench, trash can, awning          |

The atlas uses a warm brick and amber-light language against sage greens, teal glass, slate roads, and indigo shadows. The staging map suggests a street loop around a small café façade and a lower interior area; it is intentionally a visual staging sheet rather than a playable map.

## Originality, prompt, and provenance

The images were hand-authored as deterministic pixel clusters with the repository’s bundled Pillow runtime. No supplied ZIP, Pulse tile, Kenney asset, external reference pixel, copied character, logo, or third-party source image was used. The work is original repository-local concept art; no third-party license or attribution is being asserted.

Authoring brief:

> Create a cohesive 16×16 top-down handheld-RPG pixel language for a rainy Bellweather neighborhood café street and interior. Cover street, sidewalk, grass, brick, window, door, floor, furniture, and weather accents. Use warm brick, teal glass, sage grass, indigo shadow, and amber light. Keep every cell self-contained, crisp, and readable at native size. Keep the atlas suitable for nearest-neighbor sampling and leave runtime text out of the artwork.

The exact method, brief, empty source list, file hashes, and generation date are recorded in `tiles.json`.

## Limitations and next review

These are concept tiles, not production-ready game assets. They still need an art review for cluster rhythm, edge joins, palette accessibility, repeated-tile seams, alpha-edge behavior, and visual distinction at native size. The collision values in `tiles.json` are art-direction hints only. The staging map has no authoritative portal, spawn, occlusion, weather, season, or save-state contract. Do not mark any catalog item complete or integrate this folder into runtime without a separate review and game-play verification pass.
