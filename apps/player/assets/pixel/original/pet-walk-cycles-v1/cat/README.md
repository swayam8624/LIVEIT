# Cat companion movement cycles v1

An original AI-generated warm-gray tabby cat companion walk-cycle concept. The
single source sheet has four phase columns and four direction rows:

| Columns | `contact-a` | `passing-a` | `contact-b` | `passing-b` |
| ------- | ----------- | ----------- | ----------- | ----------- |
| Rows    | south       | west        | east        | north       |

Each normalized frame is transparent RGBA `96×128` with a shared bottom-center
pivot at `(48,124)`. The atlas is `384×512`, and the nearest-neighbor preview is
`1536×2048`. All 16 frames and the batch are explicitly `runtimeReady: false`.

## Files

- `cat-walk-cycles-source.png` — exact unmodified generated 4×4 source.
- `cat-walk-cycles-atlas.png` — normalized `384×512` RGBA atlas.
- `cat-walk-cycles-preview-4x.png` — nearest-neighbor visual review.
- `frames/` — 16 normalized frame PNGs.
- `frames.json` — frame coordinates, directions, phases, pivots, and limits.
- `manifest.json` — matching batch manifest with `runtimeReady: false`.
- `prompt.md` — exact generation prompt and provenance record.
- `normalize_cat_cycles.mjs` — deterministic normalization script using the
  repository's existing `sharp` dependency.

## Prompt and provenance

Generated on 2026-10-20 with the built-in OpenAI image generator in one call.
The prompt requested a transparent 4×4 sheet with south/west/east/north rows,
contact-a/passing-a/contact-b/passing-b columns, a warm-gray tabby silhouette,
amber eyes, teal collar, visible alternating limbs, a swishing tail, and a
stable bottom pivot. The exact prompt is preserved in `prompt.md` and the
generated source is preserved byte-for-byte at `cat-walk-cycles-source.png`.

No reference images, user ZIPs, third-party game art, logos, or text were used.
The source is an original generated concept and does not constitute a license
clearance or runtime acceptance decision.

## Normalization and visual QA

`normalize_cat_cycles.mjs` measures the four occupied alpha row bands, crops
each phase column from those bands, resizes each cat to `88×120` with nearest
neighbor sampling, and centers it in a transparent `96×128` frame with a
four-pixel gutter. It then assembles the atlas, exports individual frames, and
writes both manifests. The visual review checks the four directional silhouettes,
leg and tail changes across phases, alpha edges, and bottom registration.

## Limitations

This is a concept batch and is not runtime-approved art. Pixel cleanup, colored
edge review, exact phase timing, collision-box authoring, palette accessibility,
renderer sampling, and native device performance still require dedicated review.
No runtime or catalog entry is added by this batch.
