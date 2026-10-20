# Linked early-age poses v2

This isolated review batch contains 32 original, redrawn pixel-cluster poses
for the linked primary player's early life arc: infant, toddler, child, and
teen. Each stage has four authored directions (`south`, `west`, `east`, and
`north`) with a distinct idle and interaction pose. Frames are transparent
RGBA at `24x32` with pivot `[12,31]`.

The interactions are deliberately age-specific: an infant reaches toward a
soft toy, a toddler waves or clasps a comfort token, a child presents a
keepsake, and a teen checks a keepsake close to the body. Full silhouettes,
hands, legs, and action props are redrawn rather than made by a one-pixel
offset or a tiny overlay. Directions are authored independently and are never
mirrored.

## Provenance and rights

The source frames in `life-arc-early-cycles-v1` are used only as local
identity references for palette, hair, skin, blue clothing accents, and the
facial mark. The builder does not copy source pixels. No supplied ZIP, third
party art, or external download is used. Source and output SHA-256 values are
recorded in `manifest.json`.

## Rebuild

From the repository root:

```sh
python3 apps/player/assets/pixel/original/linked-early-poses-v2/build_linked_early_poses.py
```

The deterministic Pillow builder writes per-stage atlases, a combined atlas,
a nearest-neighbor review preview, and the manifest. Every output remains
`runtimeReady: false` until visual review, collision/timing authoring,
renderer sampling checks, and runtime integration are complete.
