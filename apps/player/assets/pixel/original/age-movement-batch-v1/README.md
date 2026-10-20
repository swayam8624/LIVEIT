# Age movement batch v1

This folder is an original, rights-safe concept batch for age-aware player locomotion. It covers infant crawling, toddler waddling, child/teen/young-adult walking, and distinct elder man and elder woman walking variants. The art is intentionally 2D pixel-only and is kept in its own intake folder; no player code, asset catalog, or runtime manifest was changed.

## Deliverables

- `source-*-concept.png` — three generated source concept sheets retained for visual review.
- `*-4frame-atlas.png` — one compact four-frame atlas per stage, in contact/passing/contact-opposite/passing-opposite order.
- `*-01.png` through `*-04.png` — individual RGBA concept frames extracted from each stage row.
- `frames.json` — stage, frame, logical-size, timing, pivot, and provenance metadata.

The frame sizes are deliberately stage-specific to preserve readable silhouettes: crawling is low and wide, toddlers are short, adults are taller, and elder variants reserve room for the cane or shawl. The sheets are side-facing three-quarter studies. They are not four-direction player sprites.

## Generation and provenance

The three source sheets were generated with the built-in OpenAI image generation tool on 2026-10-20. The prompts requested original chunky pixel art, transparent alpha, strict grids, age-readable silhouettes, no text, no logos, no watermark, no 3D, and no source-pack or character reference. No downloaded ZIP, third-party game art, or existing repository image was used as an input reference.

The generated files were copied from the local image-generation cache into this folder and then normalized with Pillow using nearest-neighbor resizing. Equal source-grid cells were cropped into stage rows and assembled into the compact per-stage atlases. The source generation remains outside the repository as cache history; the copied PNGs and this metadata are the only project deliverables.

## Runtime and rights limitations

This is an art-intake concept batch, not runtime-ready content. The generated poses have subtle frame-to-frame silhouette and costume drift, the source sheets provide only one side-facing direction, and the crop/rescale step has not been artist-cleaned. Before runtime adoption, an artist should redraw pixels, verify ground alignment and collision pivots, produce south/west/east/north directions, test age transitions against the saved identity, and review accessibility/readability at the target logical scale. The elder man cane is a concept prop and needs collision/interaction decisions before use.

The metadata records the generation provenance but does not claim copyright clearance, commercial legal review, player integration, native-device acceptance, or final animation quality. These files must remain `in-production` until those gates are separately demonstrated.
