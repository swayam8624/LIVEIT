# HUD panels batch v1

Original deterministic pixel UI panel source art for LIVEIT's pixel-only
dialogue and in-game phone surfaces. This is a visual source batch only. It is
not registered in the production catalog, imported into runtime navigation, or
evidence that the corresponding save, chat, memory, or settings behaviors are
implemented.

## Deliverables

- `hud-panels-atlas-v1.png` — 1056×2160 RGBA atlas with 14 crop-safe panels in
  a three-column layout.
- `frames.json` — exact atlas crops, semantic categories, nearest-neighbor
  sampling, and per-panel nine-slice insets.
- Individual RGBA PNG crops for the dialogue window, choice-card states,
  saved/error receipts, phone shell, and phone views.
- `hud-panels-preview-2x.png` — nearest-neighbor review sheet with transparent
  spacing between components.
- `generate_panels.py` — standard-library-only deterministic source generator.

The choice-card set includes `idle`, `selected`, `armed`, `saving`,
`committed`, and `error`; the requested state list contains six names even
though it is described as five states. Status receipts cover `saved` and
`error`. Phone views cover `chat`, `contacts`, `memory`, and `settings`.

## Nine-slice contract

All crops are authored on integer pixel boundaries and use nearest-neighbor
sampling. `frames.json` records the inset in logical source pixels. The inset
is the fixed border region: keep each corner intact, stretch the top/bottom
edge horizontally, stretch the left/right edge vertically, and tile or stretch
the center according to the consuming renderer. The dialogue, cards, receipts,
and phone views use an 8px border; the taller phone shell uses a 10px border.
Runtime code must choose the final scale and minimum content size, keep text
outside these raster assets, and preserve accessible native labels.

## Provenance

Generated locally on 2026-10-20 with `generate_panels.py`. The generator uses
only a fixed hand-authored palette and integer rectangles/lines, then writes
PNG bytes with Python's standard-library `zlib` and `struct` modules. No user
ZIP art, supplied game art, downloaded image, third-party icon pack, logo,
font, or reference image was used. The source is original repository-local
concept art; no third-party license or attribution is being asserted.

The art language is a warm retro handheld HUD: deep plum structural outlines,
parchment content surfaces, muted teal navigation accents, mustard action
accents, mint saved state, and coral error state. The crops intentionally
contain abstract lines and blocks only; product copy, names, dates, balances,
conversation text, and accessibility text belong to the consuming interface.

## Runtime limits

- These are source concepts, not final device measurements or a shipped UI.
- Use nearest-neighbor sampling. Do not smooth, blur, or apply linear texture
  filtering to these pixels.
- Nine-slice metadata does not define hit targets, layout constraints,
  localization behavior, focus order, haptics, persistence, or save protocol.
- The status art cannot prove that an action was durably saved. Show a receipt
  only after the authoritative runtime result is known, and keep error recovery
  reversible.
- The phone shell and phone views are visual surfaces. Actual chat, contacts,
  memory, settings, and privacy semantics must remain native, accessible, and
  connected to the shared world state.
- The source batch intentionally makes no runtime, manifest, catalog, or code
  change. It still needs visual QA, responsive layout review, rights review,
  and native device acceptance before shipping.
