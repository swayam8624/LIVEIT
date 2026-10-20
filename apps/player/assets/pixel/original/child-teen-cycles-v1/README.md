# Child + teen movement cycles v1

This batch contains two age stages with complete four-direction, four-phase movement coverage. The atlas is a strict 4-column by 8-row RGBA sheet: columns are phases 1–4; rows are child south, west, east, north followed by teen south, west, east, north. Every normalized frame is 96×128 with a shared bottom-center pivot at `(48,124)`.

## Files

- `child-teen-cycles-source.png` — generated source sheet retained for provenance; its transparent gutters are normalized by the included script.
- `child-teen-cycles-atlas.png` — 384×1024 RGBA runtime-shaped atlas, four phase columns and eight direction rows.
- `child-teen-cycles-preview-4x.png` — nearest-neighbor 4× review image.
- `frames/` — 32 normalized 96×128 RGBA frame PNGs.
- `frames.json` — frame coordinates, stage, direction, phase, pivot, and readiness state.
- `normalize_cycles.mjs` — reproducible crop and normalization script using the repository's existing `sharp` dependency.

## Provenance

Generated on 2026-10-20 with the built-in image generator. The supplied `age-direction-concept-batch-v1/age-directions-concept-master.png` was used only as a style and identity reference. No user ZIP, reference game art, or third-party art was used.

Verbatim generation prompt:

> Use case: stylized-concept. Asset type: original top-down retro pixel-art sprite-sheet source for a life simulator. Input image 1 is a style and identity reference only: preserve the warm medium-brown skin, dark brown hair, cream and teal/ochre clothing language, and distinct child versus teen proportions, but do not copy poses or pixels. Create ONE strict transparent 4-column by 8-row sheet with equal cells, no borders, no labels, no text, no shadows outside characters. The four columns are movement phases 1, 2, 3, 4. The eight rows are exactly: child south, child west, child east, child north, teen south, teen west, teen east, teen north. Every cell contains one centered full-body age-safe fully clothed character in the row's direction, walking in place with visibly different leg and arm positions across the four phases. Child silhouette: shorter, rounder, teal overalls over cream shirt, dark hair in two small tied puffs. Teen silhouette: taller and slimmer, teal jacket/vest over cream shirt and dark teal trousers, dark shoulder-length hair tied back. Keep bottom-center feet aligned within each row and preserve clear cardinal direction silhouettes, including readable profile and back views. Crisp handcrafted pixel clusters, limited cohesive palette, no gradients, no readable text, no romantic or sexual cues, no weapons. Render at a large enough resolution for later nearest-neighbor cropping, with exact grid geometry and substantial transparent padding inside every cell.

## Limitations

This is an original AI-generated movement concept batch and is marked `runtimeReady: false`. The generator preserved the requested ordering and silhouettes but did not produce equal source row gutters, so `normalize_cycles.mjs` uses measured source row boundaries before producing the strict atlas. Colored edge pixels, phase timing, foot contact, collision boxes, palette consistency, and renderer sampling still require art-direction and runtime review. Child and teen clothing is fully covered and age-safe; this batch contains no romantic or sexual content. The atlas is suitable for inspection and pipeline integration tests only until those reviews are complete.
