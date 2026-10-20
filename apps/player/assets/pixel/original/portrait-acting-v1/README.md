# Portrait acting v1: dialogue mouth and blink

Original transparent pixel portrait acting sheets for the `portrait-animations.dialogue-mouth-blink` production need. This batch contains five registered 96×128 frames for the adult player and Amelia identities:

`neutral-open`, `blink`, `talk-open-a`, `talk-open-b`, and `talk-closed`.

Each character directory contains the untouched generated source sheet, individually named normalized frames, a 480×128 atlas, a 2× nearest-neighbor review preview, and `frames.json` with pivots, timing suggestions, provenance, and `runtimeReady: false`. The source expression batches were used only as identity and palette references. The generated source sheets remain unchanged; derived frames had a conservative cleanup that removes isolated alpha components smaller than 24 pixels to discard generator specks.

## Exact generation prompt

Both sheets used the same prompt, with the character-specific identity in the input reference and subject line:

```text
Use case: illustration-story
Asset type: original 2D pixel portrait acting sprite sheet for a mobile dialogue game
Input images: Image 1 is an identity and palette reference only; preserve the adult character's hair, teal accents, cream blouse, and general face proportions, while redrawing an original asset. Do not copy any exact pose or background.
Primary request: Create one clean transparent pixel-art face sheet with exactly five separate complete head-and-shoulders portraits of the same adult character arranged in a single horizontal row, equal cells, consistent scale and centered pose. The five states left to right are: neutral-open (eyes open, small relaxed mouth), blink (both eyes closed, mouth relaxed), talk-open-a (eyes open, mouth open in a small rounded speaking shape), talk-open-b (eyes open, mouth open in a slightly wider speaking shape), talk-closed (eyes open, mouth closed).
Scene/backdrop: fully transparent background including all gutters; no backdrop.
Subject: adult identity, bust portrait only, same hair and teal accents in every cell.
Style/medium: crisp retro pixel art with deliberate pixel clusters, readable at 96x128 pixels, limited warm palette, clean dark outline.
Composition/framing: exact 5-column horizontal strip, each cell 96x128 proportion, portrait aligned to identical head top, eye line, shoulder baseline, and pivot; generous transparent padding inside each cell.
Lighting/mood: even soft portrait lighting; subtle acting changes only in eyes and mouth.
Color palette: warm skin, cream, teal, dark brown outlines, and character-specific hair color.
Constraints: no text, no labels, no symbols, no watermark, no extra objects, no speech bubbles, no anatomy changes, no head tilt changes, no eye direction changes except blink, no mouth movement outside the five requested states, adult character only.
Avoid: gradients, painterly blur, anti-aliased edges, photographic rendering, 3D, multiple characters, opaque background, cell borders.
```

Generated with the built-in image generation tool on 2026-10-20. These are original concept assets pending visual/gameplay approval and runtime integration.
