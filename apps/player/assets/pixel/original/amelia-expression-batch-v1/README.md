# Amelia expression batch v1

Twelve adult Amelia expression concepts generated from the existing Amelia portrait as an identity/color reference. The generator kept a baked brown studio backdrop, so the crops and atlas are opaque concept portraits rather than production transparent sprites.

## Contents

- `amelia-expressions-concept-master.png`: unmodified 4×3 generated source.
- `amelia-emotions-12-96x128.png`: 384×384 atlas, 96×128 cells.
- `amelia-emotions-preview-2x.png`: nearest-neighbor review preview.
- Twelve individual 96×128 PNG crops.
- `frames.json`: expression/frame metadata and explicit runtime readiness.

Expressions in reading order: neutral, joyful, sad, angry, surprised, worried, confident, crying, embarrassed, tired, thoughtful, affectionate.

## Provenance and limits

Generated with the built-in image generator on 2026-10-20. Existing `apps/player/assets/amelia-portrait.jpg` was used only as a visual identity reference. No supplied ZIP archive art was used. The source grid and art are AI generated and may need face/pixel cleanup. Transparent extraction, crop alignment, facial consistency review, and renderer integration remain before runtime use. These are original concepts, not a claim of final production sprites.

Prompt: “Create a clean pixel-art sprite sheet of 12 distinct emotional portrait sprites for the same adult woman shown in the reference, preserving her recognizable brunette bob, warm face, cream blouse and teal accents while redesigning as original polished 32-bit storybook pixel art. Arrange an exact 4 columns by 3 rows grid, each cell identical 96x128 proportion, transparent background, one centered head-and-shoulders bust per cell with generous transparent gutters, no labels, no text, crisp deliberate pixel clusters and limited cohesive palette. Expressions left-to-right rows: neutral, joyful, sad, angry; surprised, worried, confident, crying; embarrassed, tired, thoughtful, affectionate. Every cell must be a separate complete portrait, consistent head size, outfit and identity, face readable at small size. Adult character only. No gradients, no painterly blur, no extra objects, no cell borders.” The generator baked in a backdrop despite the transparency instruction.
