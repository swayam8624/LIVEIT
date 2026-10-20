# First-home exclusive scene concept v1

An original AI-generated moving-day apartment scene, normalized into two
logical-resolution palette studies for the LIVEIT pixel-only direction.

## Files

- `first-home-generated-master.png`: preserved ImageGen source, 1402×1122 RGB.
- `first-home-32c-320x256.png`: 320×256 palette study limited to 32 colors.
- `first-home-64c-320x256.png`: 320×256 palette study limited to 64 colors.
- `first-home-layout-guide.png`: transparent actor/dialogue staging guide.
- `first-home-preview-2x.png`: nearest-neighbor comparison of both palette exports.
- `manifest.json`: dimensions, palette counts, staging guides, hashes, and status.
- `provenance.json`: source prompt, generator, and source/output hashes.
- `build_first_home.py`: deterministic source normalization and preview builder.

## Limits

This is a flattened scene concept. The guide only marks a proposed actor-safe
area and dialogue band; it is not a walkable map, collision layer, portal map,
or separate depth composition. The generated master has richer pixel-like
texture than the current character clusters. Review the palette exports and
repaint any soft texture and furniture edges before scene integration.

All outputs remain `runtimeReady: false` until human visual review, separation
into composable layers, map authoring, and renderer/device validation.
