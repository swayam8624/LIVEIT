# Age and identity variety study v1

This is an original, generated concept batch for LIVEIT's ordinary-life pixel direction. It covers two distinct identities for each of four stages: child, teen, adult, and elder. Each identity has a four-phase three-quarter-front movement mini-cycle for visual review.

## Deliverables

- `source/age-identity-lineup-original.png` is the preserved lineup source.
- `source/age-identity-walk-original.png` is the preserved movement-study source.
- `identities/` contains deterministic 256x192 identity crops.
- `walk-cycles/<identity>/` contains four 96x128 RGBA concept frames, a 384x128 atlas, and a 4x preview.
- `age-identity-walk-montage-4x.png` is a review montage.
- `manifest.json` records source crops, dimensions, pivots, and the runtime boundary.
- `extract_assets.py` rebuilds every derived image deterministically from the preserved sources.

## Provenance and limits

The source sheets were generated with the built-in ImageGen workflow on 2026-10-20. No downloaded game art or user ZIP art was used as an input. The source sheets and prompt record are retained so this batch can be reviewed or regenerated without treating the outputs as shipped assets.

The lineup and movement sheet are separate studies. The movement sheet provides useful age and silhouette variety, but exact identity correspondence between a lineup cell and its walk strip is not yet proven. The movement sheets also cover only one three-quarter-front direction, retain a solid background, and have no engine-validated collision pivots, palette lock, animation timing, or transparent production cutout. Every manifest record is therefore `runtimeReady: false`.
