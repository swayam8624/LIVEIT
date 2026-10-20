# Infant and toddler movement cycles v1

A generated transparent 4-phase movement sheet for the two youngest life stages. The normalized atlas has four phase columns and eight age-direction rows:

- infant south, west, east, north: crawling on hands and knees
- toddler south, west, east, north: upright toddler waddling

Each normalized cell is 96×128 RGBA. The corresponding logical frame exports are 24×32 RGBA with nearest-neighbor sampling. The atlas is 384×1024 and the review preview is 1536×4096.

## Files

- `source-generated-sheet.png`: generated source sheet retained for provenance (887×1774 RGBA).
- `infant-toddler-cycles-atlas.png`: normalized 4×8 atlas; columns are phases and rows are age-direction pairs.
- `infant-toddler-cycles-preview-4x.png`: nearest-neighbor 4× review image.
- `frames/`: 32 individual 24×32 logical frames.
- `frames@3x/`: the same 32 frames at normalized 96×128 display size.
- `frames.json`: exact row/column coordinates, frame IDs, pivots, provenance, and limitations.

## Exact generation prompt

The built-in image generation tool generated the source sheet on 2026-10-20. The supplied concept image was used only as a visual style and player-identity reference. No supplied ZIP, third-party game art, or background art was used.

> Use case: stylized-concept. Asset type: original top-down retro pixel-art animation sprite sheet for a life simulator. Input image 1 is a visual style and player-identity reference only; do not copy its layout artifacts or any other age rows. Generate a NEW strict transparent sprite sheet with exactly 4 equal columns and 8 equal rows, no margins, no labels, no text, no grid lines, no borders, no background. Every cell contains exactly one centered full-body sprite with transparent pixels around it. Columns left-to-right are animation phases 1, 2, 3, 4. Rows top-to-bottom are: infant south/front crawling, infant west/left profile crawling, infant east/right profile crawling, infant north/back crawling, toddler south/front waddling, toddler west/left profile waddling, toddler east/right profile waddling, toddler north/back waddling. Same warm medium-brown-skinned player identity, dark brown hair, cream clothing with teal and ochre accents, chunky handcrafted pixel clusters, crisp hard pixel edges, cohesive limited palette. Infants stay low and horizontal on hands and knees in all four directions; phase changes show alternating hand/knee positions and gentle body bob. Toddlers stay upright with short toddler proportions and visibly different waddle phases; phase changes show alternating feet, bent knees, and side-to-side balance. Keep each row's character consistent across all four phases and each direction. Keep bottom-center ground pivots aligned within each row; infant pivot is under the crawling body, toddler pivot under the feet. This sheet will be cropped into 32x32 logical frames, so silhouettes must be readable at tiny scale. Avoid: photorealism, 3D, gradients, anti-aliased blur, cast shadows, scenery, props, extra characters, speech bubbles, letters, numbers, watermarks, nontransparent pixels outside sprites, merged cells, inconsistent cell sizes, missing directions, standing infant, walking infant, adult characters.

## Visual inspection and limitations

The normalized atlas was visually inspected after cropping. It has the requested 4×8 layout, transparent background, distinct four directions per age, and readable crawling/waddling phase changes. No grid seams, labels, background scene, or missing row was observed.

This remains concept art. The generated pixels show small frame-to-frame silhouette and edge-color drift, and the 24×32 logical exports need a renderer pass for readability, collision-box tuning, pivot verification, and animation timing. The source contains no runtime integration or shipped asset claim. Every frame and the batch are explicitly marked `runtimeReady: false` in `frames.json`.
