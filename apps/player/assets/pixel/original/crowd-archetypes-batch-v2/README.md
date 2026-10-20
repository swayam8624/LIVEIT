# Crowd archetypes batch v2

This concept batch covers ten planned LIVEIT crowd families: runner, tourist,
mechanic, artist, filmmaker, athlete, shopper, barista, pet walker, and market
vendor. Every role has twelve 24x32 RGBA frames: four independently authored
cardinal views (`north`, `east`, `south`, `west`) and three states (`walk-a`,
`walk-b`, `idle`). The bottom-center pivot is `(12,31)` for all frames.

The catalog convention is explicit: `north` maps to the legacy `back` source
folder, `east` to `right`, `south` to `front`, and `west` to `left`. Existing
PNG folders retain those source names so frame bytes and paths remain stable;
`sourceDirection` in each frame record preserves that implementation detail,
while `direction` is always the catalog cardinal name.

Each role directory contains a 3x4 nearest-neighbour atlas, a 6x preview, a
manifest with per-frame SHA-256 hashes, and the original frame PNGs. The root
contact sheet places all ten role atlases side by side for visual review and
labels each role column plus its four cardinal rows.

The pixel clusters were authored deterministically in
`build_crowd_archetypes.py`. The role silhouettes, clothing palettes, and held
objects are original work; no supplied archive or internet image was used and
there are no external source files to license. `runtimeReady` is `false` in
every manifest. These exports still require human pixel-art review, palette
approval, engine import, and device capture before runtime admission.

Regenerate from the repository root with:

```text
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 apps/player/assets/pixel/original/crowd-archetypes-batch-v2/build_crowd_archetypes.py
```
