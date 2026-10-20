# Adult and elder movement cycles v1

Four original adult and elder character stages with four cardinal directions and four walk phases per direction. The sheet is organized as 16 facing rows and four phase columns:

1. young adult woman: south, west, east, north
2. midlife adult woman: south, west, east, north
3. elder woman: south, west, east, north
4. elder man: south, west, east, north

Every facing row contains `contact-a`, `passing-a`, `contact-b`, and `passing-b`. Individual frames are normalized to 96×128 RGBA with a bottom-center pivot at (48, 126). `frames.json` is authoritative for coordinates and marks all frames `runtimeReady: false`.

## Files

- `adult-elder-cycles-source.png` — unmodified generated source sheet; visual audit reference.
- `adult-elder-cycles-atlas.png` — clean 384×2048 RGBA atlas, four phase columns by 16 facing rows.
- `<stage>/<stage>-cycle-atlas.png` — 384×512 stage atlas for each of the four stages.
- `<stage>/*.png` — 64 normalized individual frame PNGs in total.
- `frames.json` — stage, facing, phase, atlas rectangle, pivot, and readiness metadata.
- `prepare_assets.py` — initial deterministic crop attempt retained for source-layout investigation.
- `prepare_from_concepts.py` — final clean fallback builder using the repository’s four directional concept poses and deterministic phase offsets.

## Provenance

Generated on 2026-10-20 with the built-in image generator. No user ZIPs or third-party art were used. The generated source sheet is retained as `adult-elder-cycles-source.png` for provenance, but its nominal 4×16 grid was not reliable enough for production slicing: horizontal silhouettes crossed seams and adjacent stage rows overlapped vertically. The final normalized frames therefore use the repository’s existing clean four-direction concept poses as the source fallback, with deterministic one-pixel phase offsets. The concept batch itself was originally generated for this repository and is used here as an internal art source, not as a third-party reference.

Verbatim generation prompt:

> Use case: stylized-concept
> Asset type: original top-down pixel-art movement sprite sheet for a life simulator
> Input images: Image 1 is a visual reference only for broad identity continuity, palette, and age progression; do not copy its exact pixels or layout.
> Primary request: Create one strict transparent pixel-art sprite sheet with exactly 4 equal columns and 16 equal rows (4 columns x 16 rows), no borders, no labels, no text, no grid lines. Each cell contains one centered full-body character frame with a consistent bottom-center foot pivot and generous transparent padding.
> Row order, grouped by stage then facing: rows 1-4 young adult woman facing south/front, west/profile, east/profile, north/back; rows 5-8 midlife adult woman facing south/front, west/profile, east/profile, north/back; rows 9-12 elder woman facing south/front, west/profile, east/profile, north/back; rows 13-16 elder man facing south/front, west/profile, east/profile, north/back. Within each 4-row facing group, the character performs a 4-phase walk cycle: phase 1 contact, phase 2 passing, phase 3 opposite contact, phase 4 passing. Keep each stage/facing group visually consistent across all four phases while changing leg and arm positions subtly and clearly.
> Subject details: same warm medium-brown-skinned family identity across all four characters; young adult woman with dark brown shoulder-length hair, cream blouse, teal trousers, ochre accent; midlife woman with slightly broader mature proportions, dark hair with a few gray strands, cream cardigan, teal skirt or trousers, ochre accent; elder woman with silver hair in a bun, cream shawl/cardigan, teal long skirt, ochre accent; elder man with silver hair, cream shirt, teal vest, brown trousers, and a clearly visible brown walking cane in every phase and every facing. Fully clothed, non-sexualized, readable silhouettes, distinct age traits.
> Style/medium: clean handcrafted retro pixel art, crisp hard pixel edges, limited cohesive palette, no gradients, no blur, no anti-aliased edges, no ground plane, no cast shadows beyond tiny intentional pixel contour if any.
> Composition/framing: perfect uniform cells, characters centered, consistent scale within each stage, all limbs/accessories contained inside cells, no clipping, transparent background.
> Constraints: preserve exact 4-column by 16-row geometry; each cell must contain one frame only; all 64 frames must be present; directions must be unambiguous; phases must visibly differ; cane must remain visible for elder man. Avoid extra objects, duplicate characters, text, UI, border, checkerboard, background, watermark, logos, photorealism, 3D rendering, perspective camera, missing limbs, merged neighboring cells, inconsistent cropping, or extra rows/columns.

## Limitations and visual audit

The first source slicing attempt was rejected after visual inspection because its vertical registration caused adjacent rows to contaminate stage atlases. The final atlas has 16 rows × 4 columns with clean transparent padding and no horizontal or vertical frame contamination. Since the clean fallback is based on directional concept poses, the four phases are deliberately conservative one-pixel offsets rather than authored leg and arm choreography. Palette cleanup, true walk-pose authoring, collision-box review, pivot validation in the renderer, and a human motion-quality pass remain before runtime approval. The elder man’s cane is visible in all 16 elder-man frames. All metadata remains `runtimeReady: false`.
