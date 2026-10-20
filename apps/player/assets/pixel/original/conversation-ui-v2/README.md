# Conversation UI v2

Original, text-free pixel UI studies for chat and social interactions in LIVEIT.

## Contents

- `nine-slice/`: 48×48 source tiles with 16px left, top, right, and bottom insets. The center is intended to repeat for variable bubble and panel sizes.
- `surfaces/`: fixed 128×56 incoming, outgoing, and system bubble examples with small directional tails.
- `indicators/`: a 3-frame typing dot atlas, three 21×24 frames in a 64×24 strip.
- `badges/`: unread, priority, activity, and muted badge studies in a 4×24×24 atlas.
- `avatars/`: neutral, focus, pressed, and disabled avatar frame states in a 4×48×48 atlas.
- `symbols/`: consent-safe, muted, blocked, and system-info symbols in a 4×24×24 atlas.
- `controls/`: send, reply, close, and consent controls, each with neutral/focus/pressed/disabled states in a 4×32×32 atlas.

All files are RGBA PNGs generated from integer rectangles and polygons by
`generate_assets.py`. No supplied ZIP, third-party image, font, or external
reference bytes were read. Dynamic text is deliberately absent so the game can
render localized labels and accessible text separately.

## Reproduction

```sh
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 generate_assets.py
```

The generator rewrites only this folder's PNGs and manifests. `manifest.json`
contains per-file dimensions, modes, and SHA-256 digests, plus the nine-slice
insets and atlas state order. `provenance.json` records the empty external
input set and the palette used to make the images.

## Integration boundary

Every record is `runtimeReady: false`. Before runtime admission, the renderer
still needs to import the atlases, apply nearest-neighbor sampling at the
project pixel scale, confirm focus/pressed/disabled transitions, wire semantic
text and accessibility labels, and review bubble tails at several widths.
