# Exclusive scene props v1

This pack adds 18 original, modular pixel props for the three authored exclusive scenes:

- `graduation/props/`: ceremony sign, folding chair, honor cord, confetti popper, diploma tube, and flower wreath.
- `new-parenthood/props/`: folded blanket, feeding bottle, lullaby mobile, toy blocks, footprint card, and night lamp.
- `elder-legacy/props/`: framed photo, tea tray, knitting basket, birthday cake, reading glasses, and keepsake box.

Each prop is a 64×64 RGBA tile on the same 1× grid. The declared pivot is `[32, 60]`, the bottom-center ground contact. Each item has object bounds, draw depth, and an interaction flag in `manifest.json`. Scene atlases and simple staging previews are included for visual review.

The images are authored from deterministic Pillow primitives with a deliberately limited pixel palette. No supplied archives, downloaded assets, or third-party source art were used. `provenance.json` records that source boundary. This is a concept/production pack: every item remains `runtimeReady: false` until it has been reviewed against the renderer's import contract, scene coordinates, and device output.

## Rebuild and checks

```sh
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 build_props.py
```

The builder recreates all PNGs, manifests, SHA-256 records, atlases, and previews reproducibly from the source script.
