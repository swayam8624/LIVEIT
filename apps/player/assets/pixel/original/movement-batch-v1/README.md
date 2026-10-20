# Movement batch v1

This folder contains an original, transparent 4-direction walk-cycle study for the canonical auburn-haired adult woman identity used by the first age-arc batch.

## Deliverables

- `movement-walk-4dir-32x48.png` — 128×192 RGBA atlas, 4 columns × 4 rows, with 32×48 logical frames.
- `movement-walk-4dir-preview-16x.png` — nearest-neighbor review preview.
- `frames.json` — frame rectangles, directions, phases, timing, and pivot metadata.
- `south-*.png`, `west-*.png`, `east-*.png`, `north-*.png` — individual 32×48 RGBA frames.

Rows are `south`, `west`, `east`, `north`; columns are `contact-a`, `passing-a`, `contact-b`, `passing-b`. The suggested playback duration is 120 ms per frame.

## Generation and provenance

The source concept was generated with the built-in OpenAI image generation tool. The existing `player-age-arc-v1/life-arc-concept-master.png` was supplied as a style and identity reference only. No supplied download archive was copied into this folder.

Exact generation prompt:

> Use case: stylized-concept. Asset type: production reference for a pixel-art life-simulation game character. Use the supplied life-arc image only as a visual identity reference: preserve the auburn-haired adult woman identity, teal scarf accent, warm handcrafted palette, and crisp chunky pixel-art language; do not copy any exact pose or pixels.
>
> Create ONE clean transparent-background pixel-art character walk-cycle sheet, arranged as a strict 4 columns by 4 rows grid with equal spacing and no labels, borders, shadows, text, or background. Same canonical adult woman in every cell: auburn curly hair tied with a teal ribbon, teal scarf, cream blouse, deep teal skirt, brown satchel, warm light skin. Show full body, centered, consistent scale and ground alignment.
>
> Rows top to bottom: facing down/front, facing left, facing right, facing up/back. Columns left to right: walk phase 1 contact, phase 2 passing, phase 3 contact opposite foot, phase 4 passing opposite foot. Make the animation readable with clear alternating legs and arm swing; front and back silhouettes must remain distinct. Pixel-art sprite sheet suitable for a 32x48 logical gameplay frame, rendered at high resolution with hard edges and no anti-aliasing. Transparent background genuinely alpha. No extra characters or props, no UI, no text, no watermark.

The generated sheet was normalized with Pillow: the four equal source cells were segmented from the generated studio gradient, resized with nearest-neighbor friendly output to 32×48 frames, and assembled into the atlas. The source generation remains outside the repository under the Codex generated-image cache and is not a shipped dependency.

## Runtime limitation

This is an art intake batch, not integrated game content. The 4×4 poses are a usable timing/layout reference, but the generated source has subtle frame-to-frame costume and silhouette drift and is not yet a final animation-quality character. Before runtime adoption, an artist should clean individual pixels, confirm collision-foot alignment, and test the cycle in the player renderer. No player code, asset catalog, or world files were changed.
