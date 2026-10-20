# Graduation garden background study v1

This isolated batch explores a higher-detail graduation garden backdrop for a
life milestone scene. The generated source is preserved as `source.png`; two
320×256 exports show different palette and sampling treatments. Both remain
concepts with `runtimeReady: false`.

## Generation and provenance

Generated on 2026-10-20 with the built-in OpenAI image generator. The prompt
specified an original, character-free 2D pixel-art graduation courtyard at
late afternoon, with a flowered stage and blank banner in the upper half, an
open actor staging area through the middle, and a clear lower dialogue-safe
band. It called for warm gold, teal shadow, coral flowers, crisp pixel clusters,
no text, no UI, no logo, and no third-party references. No supplied ZIP or
external game art was used.

`graduation-garden-pixel-320x256.png` was derived by resizing the source to a
160×128 logical canvas with Lanczos sampling, reducing it to 48 colors without
dither, then doubling it with nearest-neighbor sampling. The separate
`graduation-garden-detail-320x256.png` uses a direct 320×256 Lanczos reduction
followed by a 64-color no-dither palette. `graduation-garden-pixel-24c-320x256.png`
is a lower-color version from the same 160×128 logical treatment. All three
preserve the source aspect ratio. The exact source prompt and reproducible
derivation are preserved in `prompts.md` and `build_variants.py`.

Run the derivation from the repository root with the bundled Python/Pillow
runtime:

```sh
python3 apps/player/assets/pixel/original/graduation-garden-art-v1/build_variants.py
```

## Review boundary

These are backdrop concepts, not authored walkable maps or production tiles.
The detailed output has polished environmental depth but is softer than the
game's small-cluster character sprites. The logical-pixel exports have chunkier
groupings but may lose small scene details. Compare all three at game scale
before selecting an art direction. Collision, portals, lighting layers,
foreground occlusion, map bounds, and renderer sampling remain unreviewed.
