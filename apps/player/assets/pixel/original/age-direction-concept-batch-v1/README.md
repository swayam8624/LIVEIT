# Age direction concept batch v1

An 8-stage, 4-direction set of idle reference sprites for the player's life arc: infant crawl, toddler, child, teen, young adult, midlife adult, elder woman, and elder man. Frames are normalized to 96×128 with shared bottom-center pivots.

## Files

- `age-directions-concept-master.png`: unmodified generated sheet.
- `age-directions-8stages-atlas.png`: 384×1024 RGBA atlas, four facing columns by eight age rows.
- `age-directions-preview-4x.png`: nearest-neighbor preview.
- Individual stage atlases, frames, and previews under each stage directory.
- `frames.json`: frame coordinates, age, facing, pose, pivots, and limitations.

## Provenance

Generated on 2026-10-20 with the built-in image generator. No reference images, third-party game art, or supplied ZIPs were used. Verbatim prompt: “Create an original pixel-art character reference sheet for a cozy top-down life simulator. Exact 4 columns by 8 rows, transparent background, no cell borders, labels, or text, equal cells. Each cell contains one centered full-body character. Rows: crawling infant; toddler; child; teenager; young adult woman; midlife adult woman; elder woman with silver hair; elder man with silver hair and cane. Same warm medium-brown-skinned player identity with dark brown hair evolving to silver, cream clothing with teal and ochre accents. Columns: south/front, west profile, east profile, north/back. Same person and outfit across each row, only facing changes. Clean handcrafted pixel clusters, crisp pixel edges, limited cohesive palette, no gradients, no outside shadows. Infant remains crawling in all facings, toddlers have toddler proportions, fully clothed non-sexualized adults. Strict consistent 4x8 layout suitable for slicing.”

## Limitations

These are directional idle/reference views, not complete animated walk cycles. Pair them with the stage locomotion studies in `age-movement-batch-v1`. The generated sheet has some design drift and colored edge artifacts. Frames need pixel cleanup, animation alignment, age collision-box review, and renderer validation before runtime integration. Metadata marks every frame concept-only and runtime readiness false.
