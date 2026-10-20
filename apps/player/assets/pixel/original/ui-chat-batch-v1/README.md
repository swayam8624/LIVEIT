# UI Chat Batch v1

Original transparent pixel-art components for Bellweather's chat and dialogue surfaces. This batch is intentionally a visual source atlas only; runtime integration, CSS sizing, localization, and interaction states remain separate work.

## Contents

- `ui-chat-atlas-v1.png` — 1402×1122 RGBA atlas with 24 crop-safe components.
- `frames.json` — atlas coordinates, IDs, categories, and semantic state tags.

The atlas includes four button states, four dialogue/message bubbles, two avatar frames, online and unread markers, typing/read/unread/empty/error chat markers, and eight compact toolbar icons. No words, letters, numbers, logos, or third-party pack art are present; product text should be rendered as accessible UI text over these frames.

## Generation provenance

Generated with the built-in Codex image generation tool on 2026-10-20 using one transparent-background prompt. The prompt requested a 4×4-ish component atlas with extra toolbar row, warm storybook pixel styling, deep plum outlines, cream parchment, teal, auburn, gold, and slate disabled colors, crisp 1-pixel-style edges, no text, and no copied supplied archive art. The source output was copied unchanged into this folder after visual inspection; no supplied zip was used.

## Limitations and follow-up

- AI generation does not guarantee mathematically exact pixel-grid alignment. Use nearest-neighbor sampling and review crops before shipping.
- Coordinates are conservative crop boxes around each visible component; trim transparent margins in the consuming pipeline if needed.
- Button and bubble dimensions are visual variants, not final responsive measurements. Add code-side nine-slice or layout rules before runtime use.
- The source contains no pressed animation frames, localization text, or accessibility labels. Those belong in the UI implementation.
- This batch is not yet registered in the asset catalog or bundled into the player build.
