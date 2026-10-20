# Button states v1

Original pixel-edged button plates for the pixel-only LIVEIT HUD. This is a
self-contained visual source batch. It is not integrated into the player,
registered in a production catalog, or evidence that a corresponding action,
save receipt, navigation route, or accessibility label exists at runtime.

## Contents

- `buttons/` — 24 transparent RGBA button plates: six semantic families ×
  `normal`, `focused`, `pressed`, and `disabled` states. Each plate is 160×48
  logical pixels with an 8px nine-slice-safe border inset.
- `icons/` — 24 transparent 24×24 RGBA icon layers, matching each plate. The
  icon layers are separable so runtime text and layout can be authored outside
  the raster art.
- `*-states-atlas.png` — one 640×48 nearest-neighbor atlas per family, with
  states ordered normal, focused, pressed, disabled.
- `frames.json` — family, state, crop, icon, nine-slice, sampling, and
  `runtimeReady: false` metadata for every frame.
- `button-states-preview-2x.png` — a nearest-neighbor review montage.
- `generate_buttons.py` — deterministic Pillow source generator.

Families are `primary` (confirm/continue), `secondary` (open/inspect),
`choice` (story choice), `phone` (phone/messages), `danger` (cancel/leave),
and `utility` (settings/utility). Plates contain no words, letters, numbers,
logos, or copied game UI. The consuming interface must render real localized
text and accessible labels on top of these visual surfaces.

## Provenance and rights

Generated locally with Pillow on 2026-10-20 using only integer rectangles and
polygons, a fixed hand-authored palette, and the source code in this folder.
No downloaded image, supplied ZIP, third-party icon pack, font, logo,
reference image, or image-generation service was used. The artwork is an
original concept batch; no third-party license or attribution is asserted.

## Pixel and runtime limits

- Use nearest-neighbor sampling. Do not blur, anti-alias, or apply linear
  texture filtering when scaling these pixels.
- The 160×48 dimensions are logical concept dimensions. Runtime code still
  needs a platform-appropriate touch target, layout constraints, localization,
  focus order, haptics, contrast review, and accessible text.
- The plate border and metadata describe a possible nine-slice contract. A
  renderer must preserve the stepped corners and fixed 8px border before
  stretching the middle region.
- State art is visual only. `pressed`, `focused`, `disabled`, and `normal` do
  not encode permission, save success, story consequences, or any other game
  state. Every manifest frame remains `runtimeReady: false` until separate
  visual QA, import, runtime, and native acceptance are completed.
