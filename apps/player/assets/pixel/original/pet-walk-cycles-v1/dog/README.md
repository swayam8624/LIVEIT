# Dog companion walk cycles v1

Original AI-assisted concept walk cycle for a small LIVEIT dog companion. This
is an isolated art intake batch. It is not registered in the runtime asset
catalog and remains `runtimeReady: false` pending manual pixel cleanup, pivot
and collision review, animation review, and renderer QA.

## Deliverables

- `dog-walk-cycles-source.png` — exact generated transparent 4×4 source sheet.
- `dog-walk-cycles-atlas.png` — normalized 384×512 RGBA atlas.
- `frames/` — sixteen normalized 96×128 RGBA frames.
- `dog-walk-cycles-preview-2x.png` — nearest-neighbor inspection preview.
- `frames.json` — direction, phase, atlas coordinates, pivot, identity, and
  readiness metadata.
- `normalize_dog_walk_cycles.py` — deterministic packaging helper. It crops
  each equal source cell, fits the opaque subject, aligns the bottom pivot, and
  uses nearest-neighbor resampling for derivatives. The generated source is
  preserved byte-for-byte and is never rewritten by the helper.

Rows are `south`, `west`, `east`, and `north`. Columns are `contact-a`,
`passing-a`, `contact-b`, and `passing-b`. The dog keeps a cream-and-caramel
coat, floppy ears, short tail, and plum harness in all cells. Legs, tail, ears,
and body height vary across the four phases.

## Provenance and rights boundary

Generated with the built-in image generator on 2026-10-20. No user ZIPs,
third-party game art, external images, logos, or game-art references were
provided or used. The source and derivatives are original AI-assisted project
working concepts. They are intentionally excluded from runtime and catalog
promotion until human art and native renderer review is complete.

## Prompt (verbatim)

> Use case: stylized-concept
> Asset type: original game sprite sheet for LIVEIT top-down pixel life simulator
> Primary request: Create ONE clean transparent PNG sprite sheet containing a small cream-and-caramel floppy-eared mixed-breed dog companion in a four-direction, four-phase walk cycle. Exact layout is 4 columns by 4 rows, no gutters: rows are south/front, west/left profile, east/right profile, north/back; columns are contact-a, passing-a, contact-b, passing-b. Every cell contains one complete full-body dog with visible feet, stable common bottom pivot, and clearly different locomotion phases with alternating legs, body bob, ear motion, tail sway, and readable walking pose. Keep the same dog identity in every cell: small compact cream coat with caramel patches, floppy ears, short tail, plum harness with no logos.
> Scene/backdrop: genuinely transparent background in every cell.
> Subject: one original small mixed-breed dog companion, consistent silhouette and markings across all directions and phases.
> Style/medium: crisp original 2D retro pixel art, chunky pixel clusters, limited cream/caramel/plum palette, readable at 96x128 frame scale.
> Composition/framing: centered dog in each cell, feet and tail fully inside the cell, common baseline and bottom pivot, generous transparent space around the dog.
> Lighting/mood: flat pixel-art shading with subtle underside shadowing encoded in the sprite only, no floor shadow.
> Color palette: warm cream fur, caramel patches, dark brown outline, plum harness.
> Materials/textures: clean hard pixel edges, small highlight clusters, floppy ears and tail visibly animate between phases.
> Text (verbatim): ""
> Constraints: exact 4x4 sheet; no labels; no text; no grid; no borders; no floor; no extra characters; no props; no logos; no watermark; no 3D; no photorealism; no game-art references; preserve alpha transparency; make all 16 cells distinct and coherent.

## Limitations and review status

- `runtimeReady` is false for the batch and every frame.
- The source generator output is not hand-pixel-cleaned; inspect colored edge
  pixels and silhouette consistency at native scale before promotion.
- The normalized frames use a common metadata pivot of `(48, 124)` and bottom
  align the detected subject. Collision footprint, walk speed, timing, and
  pet-follow behavior are not defined here.
- No runtime imports, catalog records, archives, or gameplay code were changed.
