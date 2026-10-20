# Exclusive story backdrop polish v1

This batch adds richer new-parenthood and elder-legacy environment plates to
the existing graduation study. Each generated source is retained in
`source/`. The deterministic builder produces two RGB `320×256` alternatives
for each scene: a 32-color 160×128 logical image scaled 2× with nearest-neighbor
sampling, and a more detailed 64-color concept export. All files are
`runtimeReady: false`.

## Source prompts and rights

The original prompts are preserved in `prompts.md`. Both sources were created
with the built-in OpenAI image generator on 2026-10-20. No supplied ZIP, web
image, marketplace asset, or third-party game art was used. The sources contain
no characters and no readable text.

## Rebuild

From the repository root, run the deterministic crop, palette, and export
script with the bundled Python/Pillow runtime:

```sh
python3 apps/player/assets/pixel/original/exclusive-scene-backdrop-polish-v1/build_backdrops.py
```

The script writes SHA-256 hashes, source metadata, output dimensions, modes,
and explicit readiness limits to `manifest.json`.

## Review boundary

These plates provide actor-safe staging space and keep key furniture toward
the edges, but they are standalone alternatives, not walkable maps or
composited scene layers. The detailed exports have more atmosphere and object
detail than the previous shape-built scene drafts, but their texture is softer
than the crisp small-cluster actor art. The 32-color exports are chunkier and
may lose small forms. Compare at game scale before selecting a final art
direction or rebuilding the composable layers around them.
