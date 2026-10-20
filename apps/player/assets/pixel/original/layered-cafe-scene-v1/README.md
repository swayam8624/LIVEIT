# Layered café scene v1

An original modular 320×256 pixel-art café interior prepared for cinematic dialogue staging. The batch separates the opaque room, table staging, two actor cutouts, and transparent foreground framing so a camera can move actors independently while preserving a centered dialogue-safe band.

## Deliverables

- `background-cafe-interior.png` — opaque RGB room plate with window, shelves, counter, lamps and tiled floor. It contains no characters, UI, lettering or dialogue.
- `midground-table-staging.png` — transparent table, chairs, cup, book, candle and contact shadows.
- `actor-amelia-portrait.png` — transparent Amelia portrait cutout.
- `actor-player-portrait.png` — transparent player portrait cutout.
- `foreground-plants-lamp.png` — transparent edge foliage, table edge and hanging lamp framing.
- `cafe-composite-preview.png` — 320×256 composite in background → midground → Amelia → player → foreground order.
- `layers.json` — layer offsets, actor anchors, camera safe region, dialogue-safe band, provenance and validation expectations.
- `generate_cafe.py` — deterministic integer-coordinate hand-pixel source used to produce every PNG.

## Provenance and exact prompt

This is hand-pixel artwork authored in the repository on 2026-10-20. No supplied archive, downloaded art, third-party image, external image reference, font, or image-generation service was used. The PNGs are produced by `generate_cafe.py` with integer-coordinate rectangles and lines, a small authored palette, and no antialiasing. The source is retained so the plates can be regenerated and audited.

The production brief used for the hand-pixel pass was:

> Use case: illustration-story. Asset type: modular background and portrait staging plates for an original retro pixel life-simulator dialogue scene. Create a 320×256 café interior at warm dusk in crisp chunky pixel clusters. Keep the background architecture free of characters, UI, lettering and logos: rain window at left, dark wood shelves with colorful book blocks, small counter, pendant lights, framed abstract wall art, and a tiled floor. Create a separate transparent staging plate for a café table, two chairs, cup, book, candle and subtle contact shadows. Create two separate transparent portrait cutouts: an adult woman with auburn hair, teal clothing and amber scarf, and an adult player figure with warm brown hair, plum jacket and cream shirt. Create a transparent foreground plate with edge plants, low table edge and a hanging lamp. Reserve a clean centered camera region and a lower centered dialogue-safe band. Use hard nearest-neighbor pixels, no gradients, no antialiasing, no text, no UI and no external references.

`runtimeReady` is deliberately `false`: these are original production plates and a compositing reference, not an integrated player asset. Final renderer integration, actor animation, crop tests at device aspect ratios, palette accessibility review, and native acceptance remain outstanding.

## Validation

All six PNGs are 320×256 and were inspected with `file`. The background is RGB and the five remaining plates are RGBA; the transparent plates retain alpha. The composite was assembled in the layer order recorded in `layers.json`. Use `python3 generate_cafe.py` to regenerate the batch before rechecking hashes or visual changes.
