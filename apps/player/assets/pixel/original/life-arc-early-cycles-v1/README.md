# Life arc early cycles v1

This batch adds the early part of the same player's life arc: infant crawl,
toddler waddle, child walk, and teen walk. Each stage contains 16 transparent
24×32 frames in a four-row by four-column atlas. Rows are south, west, east,
north; columns are contact-a, passing-a, contact-b, passing-b. Every frame uses
the feet pivot `(12, 31)`.

The four source sheets are preserved in their stage directories. They were
generated with the built-in ImageGen workflow using only the local static
identity references in `player-age-arc-diverse-v1`; exact prompts and reference
paths are recorded in `prompts.md`. `normalize_extract.py` divides each source
into its equal 4×4 cells and applies nearest-neighbor scaling to 24×32, so the
derived frames can be regenerated without editing the source.

These are original concept studies, not licensed ZIP assets. Infant and toddler
poses are care-safe and non-romantic. Identity correspondence is strongest in
the recurring deep-brown skin, coiled dark hair, sky-blue accent, and small
facial mark; clothing and proportions intentionally mature between stages.
Some generated cells have uneven margins and need pixel-cluster cleanup and
renderer review before integration. All manifests keep `runtimeReady: false`.
