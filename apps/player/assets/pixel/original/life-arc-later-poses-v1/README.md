# Life arc later poses v1

This isolated concept batch contains 16 transparent 24×32 RGBA frames:
young-adult woman and midlife woman, each in four cardinal directions with an
`idle` and an `interact` state. Every frame uses the shared bottom-center pivot
`(12, 31)` and is marked `runtimeReady: false`.

## Provenance

The only visual references are local original derived frames in
`../life-arc-later-cycles-v1/frames/<stage>/`. The source batch is not edited,
copied into this folder, or promoted to runtime. No supplied ZIP, third-party
game art, web image, or external archive was used.

`build_life_arc_later_poses.py` is a reproducible Pillow adaptation pass. Idle
keeps the source feet fixed and applies a one-pixel upper-body settling bob.
Interact uses the passing pose and adds a tiny direction-aware held-object or
greeting cue using colors sampled from that same source frame. These are
stylized adaptations rather than genuinely redrawn anatomy; a human pixel
artist must reconcile hands, clothing folds, and face continuity before use.

## Layout and validation

Each stage has an 8-frame, one-row atlas ordered west-to-east by direction,
with idle then interact pairs. `life-arc-later-poses-atlas.png` stacks the two
stage atlases, and the 4× preview is for review only. `manifest.json` contains every
frame SHA-256, source-frame SHA-256, atlas rectangle, pivot, dimensions, and
the runtime-disabled state.

Rebuild with:

```sh
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 build_life_arc_later_poses.py
```
