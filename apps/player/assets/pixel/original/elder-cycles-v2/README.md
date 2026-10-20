# Elder movement cycles v2

Two independently generated original 4×4 movement sheets for the elder woman and elder man. Each sheet has four phase columns and four direction rows:

| Columns | `contact-a` | `passing-a` | `contact-b` | `passing-b` |
| ------- | ----------- | ----------- | ----------- | ----------- |
| Rows    | south       | west        | east        | north       |

Each normalized frame is RGBA `96×128` with a bottom-center pivot at `(48,124)`. Each stage has a `384×512` atlas and 16 individual frames. Every frame and both batches are explicitly `runtimeReady: false`.

## Files

- `elder-woman/elder-woman-cycles-source.png` — unmodified generated 4×4 source.
- `elder-woman/elder-woman-cycles-atlas.png` — normalized 384×512 RGBA atlas.
- `elder-woman/elder-woman-cycles-preview-4x.png` — nearest-neighbor visual review.
- `elder-woman/frames/` — 16 normalized frame PNGs.
- `elder-woman/frames.json` — exact frame coordinates, phases, pivots, and limits.
- `elder-man/elder-man-cycles-source.png` — unmodified generated 4×4 source.
- `elder-man/elder-man-cycles-atlas.png` — normalized 384×512 RGBA atlas.
- `elder-man/elder-man-cycles-preview-4x.png` — nearest-neighbor visual review.
- `elder-man/frames/` — 16 normalized frame PNGs.
- `elder-man/frames.json` — exact frame coordinates, phases, pivots, and limits.
- `normalize_cycles.mjs` — deterministic normalization script using the repository's existing `sharp` dependency.

## Provenance

Generated on 2026-10-20 with the built-in image generator in two separate calls. The matching directional concept atlases were used as visual identity/style references only:

- `age-direction-concept-batch-v1/elder-woman/elder-woman-directions-atlas.png`
- `age-direction-concept-batch-v1/elder-man/elder-man-directions-atlas.png`

No source pixels were intentionally copied from those references, no user ZIPs were used, and no third-party game art is claimed.

The woman call requested an original transparent 4×4 sheet with elder woman south/west/east/north rows, contact-a/passing-a/contact-b/passing-b columns, visible alternating limbs, silver bun, cream patterned shawl, teal skirt, and ochre accents.

The man call requested the same 4×4 layout with silver hair, cream shirt, teal vest, brown trousers, and a clearly visible brown cane in every frame and direction. Visual inspection confirms the cane remains visible in all 16 normalized elder-man frames.

## Normalization and visual QA

The sources have non-divisible dimensions and unequal transparent gutters. `normalize_cycles.mjs` measures the four occupied alpha row bands per source, crops each phase column from those measured bands, resizes with nearest-neighbor sampling into 88×120 content, and centers it in a transparent 96×128 frame. This avoids the horizontal body-splitting seen in the prior rejected attempt.

The normalized previews were visually inspected. Both sheets preserve four distinct directions, clean row registration, readable limb changes across the four phases, and consistent bottom registration. The elder-man cane is visible in every phase and direction.

## Limits

These are original AI-generated movement concepts and are not runtime-approved art. Colored edge pixels, subtle phase timing, collision boxes, palette cleanup, silhouette consistency at native scale, renderer sampling, and device performance still require a dedicated art and runtime review. No claim of native integration or final production readiness is made.
