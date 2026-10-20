# Appearance kit expansion v1

This isolated review batch adds original directional wardrobe and accessory
parts for the 24x32 actor grid. It expands the earlier appearance kit with
six hair forms, six outerwear silhouettes, four bottoms, four mobility aids,
four seasonal layers, and four culturally respectful accessory cues. Every
part has explicit south, west, east, and north drawings; no facing is created
by mirroring another facing.

The package also includes three composited example identities (`dara`,
`imani`, and `soren`) in all four directions. Components use the shared
bottom-center pivot `[12, 28]` and transparent RGBA canvases. Mobility aids
are independent accessory layers so age and accessibility choices can be
combined with a character without changing the base body.

## Provenance and limits

All pixels are hand-authored Pillow primitives with a compact original
palette. No supplied ZIP archive, web image, or third-party sprite was used.
`generate_wardrobe_expansion.py` is the source of truth; `manifest.json`
stores per-file SHA-256 hashes and every record is `runtimeReady: false`.
These are concept assets pending human art direction, palette/accessibility
review, renderer import, collision/touch review, and device evidence. The
examples are compositing demonstrations and do not register playable
identities.

## Rebuild

```sh
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  apps/player/assets/pixel/original/appearance-kit-expansion-v1/generate_wardrobe_expansion.py
```

The builder rewrites only this package's layers, composites, contact sheet,
manifest, and provenance files.
