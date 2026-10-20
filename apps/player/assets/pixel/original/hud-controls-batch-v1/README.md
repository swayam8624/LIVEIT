# HUD controls batch v1

Original pixel-art HUD symbols for the pixel-only LIVEIT direction. This is an
isolated visual source batch. It is not integrated into the player, registered
in the production catalog, or a claim that any HUD behavior is implemented.

## Deliverables

- `hud-controls-atlas-v1.png` — 384×256 RGBA atlas, 24 logical 64×64 cells.
- `frames.json` — atlas crop rectangles, semantic categories, actions/statuses,
  and integer center pivots.
- `dpad.png` through `state-focus.png` — individual 64×64 RGBA crops using the
  same IDs as the atlas.
- `hud-controls-preview-6x.png` — nearest-neighbor review image.
- `hud-controls-concept-master.png` — untouched generated source for provenance;
  it is not a runtime asset because its generated backdrop is opaque.

The atlas covers a directional pad and arrows; interaction, enter, exit, phone,
and menu symbols; player/NPC/door/transit minimap markers; heart, energy, mood,
and money status symbols; and saving, saved, error, success, disabled, and focus
states. Product copy, numbers, dates, balances, labels, and accessibility text
must remain real UI text rendered by the consuming interface.

## Generation provenance

Generated with the built-in Codex image generation tool on 2026-10-20. No
downloaded ZIP, supplied game art, third-party icon pack, logo, or reference
image was used.

Exact generation prompt:

> Use case: stylized-concept. Asset type: original pixel-art HUD icon atlas for a top-down life-simulation game. Create one transparent-background pixel-art sprite atlas containing 24 separate, clearly spaced icons arranged in a strict 6 columns by 4 rows grid, with no labels, letters, numbers, text, border, shadow, watermark, or background. Every icon must be centered in its cell with generous transparent padding and consistent scale, using crisp hard-edged chunky pixel clusters and a cohesive warm retro handheld palette: deep plum outlines, parchment cream, muted teal, auburn, mustard gold, slate disabled gray, and small coral error accents. Use an original visual language; do not copy any supplied game art or icon pack.
>
> Row 1: a four-way directional pad, a single up arrow, a single down arrow, a left arrow, a right arrow, and a hand/cursor interaction symbol. Row 2: enter doorway, exit doorway, phone handset, menu hamburger, minimap player pin, minimap NPC pin. Row 3: minimap door pin, minimap transit pin, heart/life status, energy/lightning status, mood/spark status, money/coin status. Row 4: saving disk state, saved check state, error warning state, success star state, locked/disabled state, focus/selected state.
>
> All symbols should be recognizable at small logical pixel sizes, with no decorative scenery and no duplicated icons. Maintain consistent icon scale and transparent separation for reliable crop metadata. Pixel-only 2D game UI art, intended for nearest-neighbor sampling. Avoid gradients, anti-aliasing, photorealism, 3D, vector-like smooth curves, tiny illegible detail, text, logos, and any resemblance to existing proprietary game UI.

The generated master was visually inspected, then normalized with Pillow. The
source grid was cropped into 24 cells, a conservative foreground mask removed
the dark studio backdrop, and each crop was fit to a 64×64 transparent cell with
nearest-neighbor resampling. The mood symbol was cleaned as a small integer-pixel
star after masking because the generated source retained a broad glow. The
master remains unchanged so the transformation is auditable.

## Concept limitations

- Generated art can have silhouette, palette, or edge inconsistencies. These
  crops are concept references and need artist cleanup before shipping.
- The source generation produced an opaque studio backdrop despite the
  transparent-background request; only the normalized RGBA crops are intended
  for review or future pipeline work.
- The 64×64 cells are a visual scale, not a final device size. Runtime code must
  choose hit targets, pixel density, pressed/hover animation, localization-safe
  layout, and accessibility labels.
- Symbols do not encode a save protocol, player state, map semantics, or error
  copy. They cannot prove persistence, navigation, haptics, or native HUD QA.
- No disabled/pressed animation sequence, nine-slice panel, font, or colorblind
  alternative is included.
- This batch intentionally makes no catalog, runtime, manifest, or integration
  change. It remains `original` source art until rights, visual QA, import, and
  device acceptance are separately demonstrated.
