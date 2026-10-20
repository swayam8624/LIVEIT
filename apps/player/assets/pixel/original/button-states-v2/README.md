# Button states v2

This isolated batch contains original pixel button surfaces for LIVEIT's
retro-futurist HUD. It expands the six semantic families from v1 with a
stronger stepped silhouette, two-tone bevel, state-specific depth, and a
text-safe center. The family set is `primary`, `secondary`, `choice`,
`danger`, `phone`, and `utility`; every family has `normal`, `focused`,
`pressed`, and `disabled` plates plus a matching separable icon layer.

Each plate is 192×56 logical pixels with a 10px nine-slice inset. Icon layers
are 32×32 transparent RGBA files. The center region has no words, numbers,
letters, logos, or baked language. Runtime code can render localized labels,
hit targets, focus order, and accessible names over the plate.

## Provenance and use

Generated locally with Pillow on 2026-10-20 from the accompanying
`generate_buttons.py`. Geometry is made from integer rectangles, lines,
polygons, and circles with a fixed hand-authored palette. No supplied ZIP,
downloaded image, third-party icon, font, logo, or image-generation output was
used. This is an original concept batch and makes no third-party license claim.

`frames.json` records every plate and icon, dimensions, crop, nine-slice
contract, text-safe rectangle, SHA-256, nearest-neighbor sampling, and
`runtimeReady: false`. The atlas and preview are review artifacts. They are
not runtime/catalog registration or proof of touch, accessibility, import,
save, navigation, or native acceptance.

Use nearest-neighbor sampling and preserve the stepped corners when scaling.
Before integration, perform visual QA at target sizes, localization and
contrast review, runtime import validation, and native acceptance checks.
