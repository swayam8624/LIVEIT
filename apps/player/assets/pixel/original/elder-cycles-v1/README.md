# Elder cycles v1 — rejected generation

This directory retains the original generated source for audit, but it does not contain a valid movement atlas. The requested strict 4-column × 8-row phase sheet failed visual inspection and was not normalized into runtime-shaped frames.

## Files

- `elder-cycles-source.png` — unmodified generated output, retained as provenance evidence only.
- `frames.json` — rejection manifest; it contains no frame records and marks the source as `runtimeReady: false`.

No `elder-cycles-atlas.png`, preview, or individual frame PNGs are shipped from this attempt because the source cannot be cropped into truthful contact/passing phases without inventing or duplicating motion.

## Provenance

Generated on 2026-10-20 with the built-in image generator. `age-direction-concept-batch-v1/age-directions-concept-master.png` was supplied as a visual identity/style reference only. No pixels were copied from a third-party source, and no user ZIP or external game art was used.

Generation prompt, condensed: create an original transparent 4-column × 8-row sheet with phase columns `contact-a`, `passing-a`, `contact-b`, `passing-b`; rows elder woman south/west/east/north followed by elder man south/west/east/north; show clear arm/leg movement and keep a cane visible in every elder-man frame.

## Rejection findings

- Source dimensions are `887×1774` RGBA, rather than a divisible 4×8 grid.
- The visible content is arranged as direction views across columns and repeated pose bands down the sheet, rather than the requested phase columns and direction rows.
- Only seven separable character bands are visible in the source; the requested eight direction rows are not present.
- Fixed source-cell crops split heads and bodies across horizontal boundaries. The resulting preview was visually inspected and rejected for registration and motion quality.
- Because the generated layout is invalid, there is no truthful exact 32-frame atlas to describe. All generated material in this attempt remains concept-only with `runtimeReady: false`.

## Limits

This is a failed source-generation attempt, not a completed elder movement cycle. A new generation is required before any normalized frames, atlas, renderer integration, or runtime acceptance can be claimed.
