# Named role age cycles v1

This pack fills age-cycle gaps for 13 named identities. The Bellweather teacher, shopkeeper, nurse, physician, transit worker, and cafe owner have toddler, child, teen, adult, midlife, and elder stages. Dadi (grandparent), Ishan (mentor), boss, coworker, and neighbor have adult, midlife, and elder stages. Friend one and friend two have child, teen, adult, midlife, and elder stages. These subsets keep age presentation plausible for each role and avoid inventing infant sprites or changing one identity into another.

Every identity/stage combination has 24 individual 24×32 RGBA frames: four directions (`south`, `west`, `east`, `north`) and six phases (`contact-a`, `passing-a`, `contact-b`, `passing-b`, `idle`, `interact`). Frames share the bottom-center pivot `(12, 31)`. Each age line derives from that same identity's existing local concept PNGs; age stages are deterministic nearest-neighbor silhouette transformations. Midlife and elder stages add restrained gray hair pixels. Elder idle and interaction poses include a small cane cue. Dadi and Ishan are derived from their own established Dadi and Ishan sprites, never borrowed from another identity.

## Provenance and limits

`build_assets.py` reads only the local project concept PNGs in `named-characters-batch-v1` through `named-characters-batch-v4`. It does not read the supplied ZIP archives, internet assets, or third-party art. `provenance.json` records this boundary. Frame and preview SHA-256 values are recorded in `manifest.json`.

These are original concept derivatives, not final age designs. In particular, occupational clothing on younger stages is only a continuity concept; it should be reviewed for age appropriateness and narrative fit. The small fixed cell size also limits facial expression and detailed elder posture. `runtimeReady` is false throughout. Pixel-art review, identity continuity review, accessibility palette review, collision and pivot checks, and renderer/native visual QA are required before runtime promotion.

## Files

- `manifest.json`: dimensions, pivots, coverage, source lineage, and hashes.
- `provenance.json`: authorship and asset-source boundary.
- `frames/<identity>/<age-stage>/`: all individual directional movement and pose frames.
- `named-role-age-contact-sheet.png`: south-facing idle stage overview for all six identities.
- `teacher-age-review-atlas.png`: teacher frames arranged by age, direction, and phase.
- `validate_pack.py`: validates exact coverage, image metadata, hashes, source files, and concept-only status.
