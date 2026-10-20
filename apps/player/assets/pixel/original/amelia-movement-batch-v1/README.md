# Amelia movement batch v1

Adult Amelia four-direction walk-cycle concept, cropped from one generated 4×4 sheet. South/front, west, east, and north/back are rows; four cycle phases are columns. Every normalized frame is 32×48 RGBA, with a common bottom-center foot pivot.

## Files

- `amelia-walk-4dir-32x48.png`: 128×192 transparent atlas.
- `amelia-walk-preview-16x.png`: 512×768 nearest-neighbor preview.
- Individual direction/phase PNGs and `frames.json`.
- `amelia-walk-concept-master.png`: unmodified generator output.

## Provenance and limits

Generated with the built-in image generator on 2026-10-20, using the existing `apps/player/assets/amelia-portrait.jpg` only as visual identity reference. No user ZIPs or third-party game art were used. The generator returned a transparent sheet. This sheet is an original AI-assisted concept, not a runtime-ready actor: silhouette and clothes vary slightly frame to frame, side facings are asymmetric, and walking cadence/pivots need manual pixel cleanup and renderer review. Idle, interact, talk, outfit variants, and age variants remain unmade.

Prompt: “Original pixel art game character spritesheet, based on the adult brunette woman from reference as Amelia: short softly waved dark brown bob, cream blouse, teal apron dress, tiny gold-and-teal earrings. Draw clean small handheld RPG pixel-art, strictly top-down 3/4 overworld characters, consistent design. Exact 4 columns by 4 rows grid, four directions as rows (south/front, west/left, east/right, north/back), four distinct walking frames as columns. Each cell same size and fully contained, full body, feet visible, centered, transparent background, crisp chunky pixel clusters and limited palette, no text, no grid lines, no shadows outside character, no objects. Character identity/clothes/hair must remain consistent across every frame. No romance coding, adult woman.”
