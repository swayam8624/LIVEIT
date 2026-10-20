# Appearance kit v1

This is an original, deterministic modular appearance study for LIVEIT's
24×32 actor grid. It contains separate RGBA layers for skin tone, hair,
tops, bottoms, shoes, and accessories, plus eight compositing examples.

## Contents

- 4 skin masks
- 6 hairstyles
- 6 tops
- 5 bottoms
- 4 shoe styles
- 8 accessories
- 8 composite examples in `composites/`
- `appearance-composites-preview-4x.png` for nearest-neighbor review
- `manifest.json` with stable IDs, layer order, dimensions, pivots, hashes,
  and readiness flags

The logical frame is 24×32 RGBA with a shared bottom-center pivot of `[12, 28]`.
The composition order is:

```text
skin → bottoms → tops → shoes → hair → accessories
```

Every layer uses transparent pixels outside its own silhouette. Later layers
may cover earlier pixels according to the order above. The examples are proof
that the layers can be composed with Pillow; they are not player identities and
are not registered in the runtime asset catalog.

## Provenance

All pixels were authored by `generate_appearance_kit.py` with Pillow drawing
primitives and a small, hand-authored palette. No ZIP archive, third-party
asset, internet image, or AI-generated source was used. The source of truth is
the script itself, and the manifest records SHA-256 hashes for every PNG.

## Validation and limitations

The generated layers and composites were checked for exact 24×32 RGBA mode,
nonempty alpha, shared pivot metadata, deterministic layer order, and successful
alpha compositing. `runtimeReady` is `false` for every record.

This is a south-facing compositing concept only. It does not yet provide
directional or walk-phase variants, renderer import, collision validation,
palette accessibility review, or age-specific clothing variants. The cane,
satchel, braid, and hat intentionally approach the frame bounds and need an
in-renderer occlusion and touch-size review before adoption.
