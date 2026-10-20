# Crowd archetypes batch v3

This original concept batch covers ten remaining crowd entries from
`content/production-assets/v1/pixel-world.json`: security guard, historian, park
cleaner, nurse, caregiver, gardener, teacher, parent with stroller, child at a
playground, and elder walker.

Each role has twelve transparent RGBA frames on a 24×32 canvas: four
independently authored cardinal directions (`south`, `west`, `east`, `north`)
and three states (`walk-a`, `walk-b`, `idle`). The shared bottom pivot is
`(12,31)`. Role cues include a cap and radio, archive scroll, broom, medical
bag, care tote, watering can, pointer, joined stroller chassis and hood,
playground ball, and a stable cane. The elder's shoulders and head use a lower,
gentler gait; the stroller remains connected to the parent silhouette in every
view.

`build_crowd_archetypes_v3.py` is deterministic and creates all 120 frame PNGs,
role atlases, previews, the combined contact sheet, manifests, hashes, and
provenance metadata. No supplied ZIP, internet asset, or third-party sprite was
used. Every output is a concept study and remains `runtimeReady: false` until
palette review, pixel cleanup, engine import, device capture, and human art
direction are complete.
