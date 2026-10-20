# Life arc later cycles v1

This isolated concept batch contains 64 original transparent movement frames:
young adult woman, midlife woman, elder woman, and elder man. Each stage has
four cardinal directions (`south`, `west`, `east`, `north`) and four walk
phases (`contact-a`, `passing-a`, `contact-b`, `passing-b`). The logical frame
size is 24×32 and every derived frame uses the shared bottom-center pivot
`(12, 31)`.

The four unmodified generator outputs remain in `sources/`. `build_life_arc_later_cycles.py`
deterministically thresholds faint source fringe, crops each 4×4 source cell,
scales the silhouette with nearest-neighbour sampling, and registers it at the
shared pivot. It also writes one 96×128 stage atlas, a combined 96×512 review
atlas, a 4× preview, and `manifest.json`.

## Provenance

The artwork was generated on 2026-10-20 with the built-in image generator.
`player-age-arc-diverse-v1/player-age-arc-diverse-24x32.png` was supplied as a
visual identity and palette reference only. Its pixels were not copied or
edited. No supplied ZIP, third-party game art, web image, or external archive
was used. The exact prompts are retained in `prompts.md`.

The elder woman keeps the family cues while changing the hair to silver-white
coils. The elder man is intentionally a distinct presentation with short
silver hair, beard, vest, and trousers while retaining the warm deep-brown,
sky-blue, and ochre family palette.

## Readiness and limitations

All manifest records are `runtimeReady: false`. This is concept and pipeline
art pending a human pixel-cluster cleanup, identity-continuity review across
the existing age arc, renderer sampling checks, collision-box review, and
gameplay integration. Generated sheets can contain approximate anatomy,
profile asymmetries, or residual edge colors; the derived thresholded frames
make those limits explicit but do not prove production quality.

Rebuild with:

```sh
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 build_life_arc_later_cycles.py
```
