# Home props v1

This batch covers reusable home-interior props that were missing from the
current original-art concept set: bed, sofa, dining table and chairs, kitchen
counter and sink, refrigerator, bathtub, crib, storage chest, wardrobe, floor
lamp, potted plant, and wall clock.

The source sheet is preserved at `source/home-props-original.png`. The
`normalize_props.py` script derives twelve transparent 128x128 cells, places
them into `home-props-atlas-4x3.png`, and creates the nearest-neighbor
`home-props-preview-2x.png`. Every record in `manifest.json` is
`runtimeReady: false`: these are original concept sprites awaiting pixel-artist
cleanup, collision and occupancy bounds, draw-order metadata, interaction
semantics, and a real in-game integration pass.

Provenance and limitations are recorded in `provenance.json`; the exact prompt
is retained in `prompts.md`. The generated source was not derived from any
user-supplied ZIP or third-party reference art.
