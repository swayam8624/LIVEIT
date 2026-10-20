# Player and Amelia chat avatars v1

Original compact transparent pixel avatars for the player life arc and adult
Amelia. Seven player age stages—infant, toddler, child, teen, young adult,
midlife, elder—plus Amelia each have six 48×48 states:
`listening`, `curious`, `concerned`, `reassuring`, `speaking`, and `blink`.

## Files

- `frames/` — 48 individual RGBA frames at native 48×48 size.
- `player-amelia-chat-avatars-atlas-6x8-48.png` — six states per row, in
  player age order then Amelia.
- `player-amelia-chat-avatars-preview-3x.png` — labeled nearest-neighbor review
  sheet.
- `manifest.json` — stable IDs, stage/state metadata, atlas positions, pivots,
  timings, SHA-256 hashes, and `runtimeReady: false`.
- `provenance.json` — original geometric drawing method and text-only reference
  manifests with hashes.
- `build_chat_avatars.py` — deterministic Pillow builder.
- `validate_chat_avatars.py` — coverage, age-safety, unique-byte, dimensions,
  atlas-crop, and hash checks.

The player's auburn hair and teal accent form one visual thread through the
seven ages; the elder is one presentation concept, not an exhaustive player
customization set. Amelia's adult avatar uses the existing brown-hair,
cream-and-teal identity notes. Reference pixels are not sampled. All states are
ordinary, non-romantic interaction cues. The infant and toddler `speaking`
frames mean babbling only and do not imply words or adult-coded behavior.

These are concept assets only. Pixel-art cleanup, identity and age review,
accessible state naming, renderer timing, and target-device checks remain before
runtime integration.
