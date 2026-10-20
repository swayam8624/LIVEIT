# Exclusive scenes v1

Three original, rights-safe layered pixel scene concepts for distinctive life-story beats:

- **Garden graduation** — a small outdoor ceremony with paper lanterns, a shared table, and two graduates.
- **New baby / parenthood** — a quiet home welcome with a swaddled baby as a prop on a blanket; no medical procedure or hospital imagery.
- **Elder farewell / legacy memory** — a warm family room with a framed keepsake, memory table, and an older person sharing a final keepsake moment.

Each scene is a 320×256 canvas with five independently composable plates and one flattened preview. The plates use this order at composite time: opaque background, midground props, actor primary, actor secondary, then transparent foreground framing. The lower centre (`x=42, y=232, width=236, height=24`) is reserved as an advisory dialogue-safe region. Actor anchors and pivots are recorded in `layers.json`.

## Files

For each scene, the files are named `<scene-id>-<layer>.png`:

- `background` — RGB opaque room or outdoor plate.
- `midground-props` — RGBA staging objects and contact shadows.
- `actor-primary-portrait` and `actor-secondary-portrait` — RGBA portrait cutouts with bottom-centre anchors.
- `foreground-framing` — RGBA edge foliage, framing architecture, or furniture.
- `composite-preview` — RGBA order-of-layers preview for visual review.

`layers.json` is the exact manifest. It records dimensions, alpha expectations, SHA-256 hashes, anchors, dialogue-safe regions, layer order, provenance, and `runtimeReady: false` at both batch and scene/layer level.

## Provenance

This batch was authored in the repository on 2026-10-20 with `generate_exclusive_scenes.py`, a deterministic Pillow renderer using integer rectangles and polygons and a small shared palette. No supplied archive, downloaded art, third-party image, external image reference, font, logo, or image-generation service was used. The parenthood scene is intentionally tasteful and non-medical: the baby appears only as a small wrapped prop in a home setting.

The production brief was:

> Use case: illustration-story. Asset type: modular 320x256 pixel-art story plates. Create three original life-simulator story beats with a cohesive dusk-and-lamplight palette: a garden graduation with lanterns; a quiet new-parenthood home welcome with a swaddled baby and no medical procedure; and an elder farewell/legacy memory with a framed keepsake. Separate opaque background, transparent props, two transparent actor portrait cutouts, transparent foreground framing, and a composite preview. Hard pixel clusters, no antialiasing, no text, no logos, no external references.

## Validation status

The generator is reproducible with `python3 generate_exclusive_scenes.py`. PNG dimensions, color modes, alpha expectations, and hashes are recorded in `layers.json`. These are art-direction concepts awaiting manual pixel cleanup, crop/aspect review, palette accessibility review, actor animation, collision/pivot tuning, and native renderer acceptance. They must remain `runtimeReady: false` until those gates pass. This folder does not modify runtime code, content catalogs, or asset registration.
