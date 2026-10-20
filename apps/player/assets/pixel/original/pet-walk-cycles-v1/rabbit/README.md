# Rabbit walk cycles v1

Original AI-assisted concept walk cycle for a LIVEIT companion rabbit. This
is an isolated intake batch and remains outside the runtime and production
asset catalog until manual pixel cleanup, pivot review, collision review, and
renderer QA are complete.

## Deliverables

- `rabbit-walk-cycles-source.png` — exact generated 4×4 transparent source sheet.
- `rabbit-walk-cycles-atlas.png` — normalized 384×512 RGBA atlas.
- `rabbit-walk-cycles-preview-2x.png` — nearest-neighbor 768×1024 inspection preview.
- `frames/` — sixteen normalized 96×128 RGBA frames.
- `frames.json` — direction, phase, atlas coordinates, pivot, and readiness metadata.
- `normalize_walk_cycles.py` — deterministic nearest-neighbor packaging helper.

Rows are `south`, `west`, `east`, and `north`. Columns are `contact-a`,
`passing-a`, `contact-b`, and `passing-b`. Every frame uses the same metadata
pivot `{ "x": 48, "y": 126 }`; all records retain `runtimeReady: false`.

## Provenance and rights boundary

Generated with the built-in image generator on 2026-10-20. No user ZIPs,
third-party game art, external images, logos, or game-art references were
supplied. The source and normalized derivatives are original AI-assisted
working concepts for this repository. The generated source is preserved
unchanged; normalization only crops each alpha-bounded cell and resamples it
with nearest-neighbor pixels.

## Prompt (verbatim)

> Use case: stylized-concept
> Asset type: original 2D retro pixel game sprite sheet for a companion walk cycle
> Primary request: Create ONE transparent PNG sprite sheet with an exact 4 columns by 4 rows layout, no gutters or labels. Rows top to bottom are south/front, west/left profile, east/right profile, north/back. Columns left to right are contact-a, passing-a, contact-b, passing-b. Every cell contains one complete identical upright-eared rabbit companion with clearly different walking phases: alternating hind legs, subtle forepaw swing, small torso bob, and a visible tail shifting naturally. Keep a common stable bottom pivot across every cell.
> Subject: distinct original soft warm-brown rabbit, upright ears, compact friendly silhouette, tiny green neckerchief tied at the neck, readable face and tail in each applicable direction.
> Style/medium: crisp chunky 2D pixel art, limited warm brown and cream palette with green accent, clean hard pixel clusters, game-ready concept sheet.
> Composition/framing: one centered full-body rabbit per cell, consistent scale and baseline, feet/hind paws visible, generous transparent area inside each cell, all 16 cells separated by transparent space only.
> Lighting/mood: even flat sprite lighting.
> Color palette: soft warm brown fur, cream muzzle/belly accents, muted leafy green neckerchief.
> Materials/textures: clean pixel clusters, no antialiasing.
> Constraints: preserve the same rabbit identity and neckerchief in every direction; make hind-leg and tail motion visibly cycle from contact-a to passing-a to contact-b to passing-b; transparent background with true alpha; no text, labels, grid lines, borders, floor, shadows, extra characters, props, logos, watermark, 3D, photorealism, or existing game-art references.
> Avoid: any writing or UI elements.

## Limitations

The generated source has visible colored edge fringing in places and the
four-phase motion is a concept pass, so manual pixel cleanup and a renderer
animation review are still required. No runtime or catalog registration is
included in this batch.
