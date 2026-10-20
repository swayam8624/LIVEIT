# Exclusive scene layers v1

Original 2D pixel-art concept kit for reusable story-scene staging in LIVEIT. The kit covers three milestone moments: graduation, new parenthood, and an elder birthday. It is intentionally isolated under `original/` and is not registered in the runtime catalog.

## Contents

- `sources/exclusive-scene-triptych-source.png` is the preserved RGB source sheet for the three scene environments.
- `backgrounds/` contains flattened environment crops, compact review exports, and placement guides. The placement guides mark a center actor-safe zone (cyan) and lower-third dialogue-safe band (gold).
- `sources/exclusive-props-source.png` is the preserved RGBA prop source sheet.
- `props/` contains twelve individually cropped transparent props: graduation (mortarboard, diploma, bouquet, bunting), new parenthood (bassinet, bottle, lamp, swaddle), and elder birthday (cake, gift, teacup, framed photo).
- `previews/exclusive-scenes-layer-order-preview.png` is a flattened review mock showing the three panel order and safe zones. It is not runtime-ready.

The three environment crops are deliberately labeled `flattened-concept`: the source presents background, midground and foreground depth in one painted panel. Reusable transparent props are separate, but no complete background/midground/foreground atlas has been authored yet. Actor placement remains an empty zone in the guides; no character art is embedded.

## Provenance and rights

Both source sheets were generated in-session with the Codex ImageGen tool from the prompts recorded in `provenance.json`. No supplied ZIP, third-party asset or web image was used. The generated artwork is original work for this project; keep the source and prompt record alongside any later derivative export.

## Review status

Every output has `runtimeReady: false`. Before integration, an artist or engineer must review pixel density at device size, choose a target atlas scale, assign pivots and safe rectangles, and stage real actors/dialogue over each background. `generate_layers.py` is deterministic derivation code; rerun it only when replacing a source sheet.
