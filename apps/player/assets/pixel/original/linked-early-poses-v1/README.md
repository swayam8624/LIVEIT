# Linked early-age poses v1

This isolated batch adds identity-linked idle and interaction concepts for the
infant, toddler, child, and teen stages in `linked-life-arc-family-v1`. It
contains 32 transparent RGBA frames at `24×32`: four stages × four authored
directions × idle/interact. Every frame uses pivot `(12,31)`.

The frames are derived only from the local original directional movement frames
in `life-arc-early-cycles-v1`. The linked cues are deep-brown skin, coiled dark
hair, recurring sky-blue clothing accents, and the small facial mark. No ZIP
contents, third-party pixels, external downloads, or mirrored directions are
used. Infant interaction is a soft-toy reach; toddler interaction is a gentle
wave/comfort cue; child and teen interactions use small keepsake cues.

## Rebuild

From the repository root:

```sh
python3 apps/player/assets/pixel/original/linked-early-poses-v1/build_linked_early_poses.py
```

The builder writes per-stage atlases, one combined nearest-neighbor preview,
and `manifest.json`. The manifest records every output SHA-256, every source
frame SHA-256, dimensions, pivots, cues, and `runtimeReady: false`.

## Review boundary

These are original rights-safe concept derivatives for human review. They
prove directional coverage and a coherent motif link to the early movement
batch, but they do not prove exact saved-person identity continuity, collision
or animation timing, renderer sampling, or save/reload behavior. A pixel artist
and the runtime asset integration gate must approve them before use in-game.
