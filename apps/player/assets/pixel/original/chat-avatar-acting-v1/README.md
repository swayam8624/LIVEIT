# Chat avatar acting v1

An original compact portrait set for chat lists and in-conversation speaker
states. It contains six 48×48 transparent avatar frames for each of four named
Bellweather family characters: Mara, Eli, Niko, and Aunt Sol. States are
`listening`, `curious`, `concerned`, `reassuring`, `speaking`, and `blink`.

## Files

- `frames/` — 24 individual RGBA PNGs at native 48×48 size.
- `chat-avatar-acting-atlas-6x4-48.png` — six states per row; character order
  is Mara, Eli, Niko, Aunt Sol.
- `chat-avatar-acting-preview-3x.png` — nearest-neighbor contact preview with
  state labels.
- `manifest.json` — stable IDs, cell coordinates, pivots, suggested state
  durations, per-file SHA-256 hashes, identity notes, and `runtimeReady: false`.
- `provenance.json` — generation method, text-only identity reference, and
  source-script hash.
- `build_chat_avatars.py` — deterministic Pillow builder and manifest writer.
- `validate_chat_avatars.py` — local integrity, layout, and coverage checks.

All six states are ordinary, age-safe conversation cues. Niko has no
romance-coded, intimate, or adult-coded expressions. The speaking and blink
frames are intended as brief swaps; the timing values are starting suggestions,
not a complete animation system. Portraits use an original compact pixel
language and text-only identity/palette notes from the existing named-family
concept. No source images are sampled or copied.

These are concept assets, not admitted runtime sprites. Human review should
confirm pixel cleanup, named identity continuity, platform-scale legibility,
accessible semantic labels, and renderer timing before integration. Existing
chat panel, reaction glyph, and full-size expression sets are separate and are
not duplicated here.
