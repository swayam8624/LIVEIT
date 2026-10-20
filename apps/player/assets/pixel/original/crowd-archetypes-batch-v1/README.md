# Crowd archetypes batch v1

This original concept batch covers ten planned crowd entries from
`content/production-assets/v1/pixel-world.json`: student, office worker, store
clerk, baker, delivery rider, bus driver, taxi driver, police officer, library
visitor, and street musician.

Each role has exactly twelve transparent RGBA frames on a 24x32 canvas: four
independently authored cardinal directions (`south`, `west`, `east`, `north`)
and three states (`walk-a`, `walk-b`, `idle`). The bottom pivot is `(12,31)`.
Role cues are intentionally small but readable at game scale: backpacks and
books, work cases, apron tags, bread trays, helmets and delivery packs, uniform
caps, key rings, radios, library totes, and instruments.

`build_crowd_archetypes.py` is deterministic and creates all frame PNGs,
role atlases, previews, the contact sheet, manifests, and provenance metadata.
No supplied ZIP, internet asset, or third-party sprite was used. All outputs
are concept studies and remain `runtimeReady: false` until palette review,
engine import, device capture, and a human pixel-art cleanup pass are complete.
