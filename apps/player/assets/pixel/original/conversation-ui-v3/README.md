# Conversation UI v3

Original, text-free pixel UI concept package for LIVEIT social conversations. This is a new package generated from integer Pillow primitives; it does not copy or derive pixels from the supplied ZIP archives or from third-party artwork.

## Coverage

- `nine-slice/` contains seven 64×64 source tiles: dialogue, choice, status, phone, incoming, outgoing, and system. Each tile has a 12px perimeter and a repeatable center. The manifest records the insets and transparent-margin policy for each tile.
- `surfaces/` contains incoming, outgoing, and system 160×64 bubbles with directional tails, plus choice and status surfaces that leave their text regions empty.
- `indicators/` contains a three-frame typing atlas and four status markers: online, away, busy, and offline.
- `avatars/` contains neutral, focus, pressed, and disabled 48px avatar plates. The face mark is only a generic placeholder; character portraits remain separate assets.
- `phone/` contains a 176×240 chat panel and a 5-widget strip for contact, call, attachment, emoji, and more actions.
- `controls/` contains normal, focus, pressed, and disabled atlases for consent, report, block, send, reply, and close. These are semantic icon states without baked labels.

The preview board is `conversation-ui-v3-preview-2x.png`. All files use RGBA PNG, integer coordinates, and nearest-neighbor review scaling.

## Reproduction

```sh
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 generate_assets.py
```

The script rewrites only this directory's PNGs, `manifest.json`, and
`provenance.json`. The manifest stores every PNG's dimensions, mode, SHA-256
digest, state ordering, and nine-slice border metadata. Dynamic dialogue,
labels, timestamps, balances, and accessibility strings are intentionally
external to the images.

## Integration boundary

Every record is `runtimeReady: false`. Before admission, the renderer needs
nearest-neighbor import and variable-width expansion tests, confirmation that
12px corners and tails survive all supported sizes, semantic focus/pressed/
disabled transitions, accessible labels, and a human review of contrast and
pixel density at the project's actual scale.
