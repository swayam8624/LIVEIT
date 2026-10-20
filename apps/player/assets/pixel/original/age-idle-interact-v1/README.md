# Age idle and interact studies v1

This is a 56-frame, original pixel-cluster concept pack for the seven-stage
life arc used by `directional-age-refine-v1`: infant crawl, toddler waddle,
child, teen, adult, elder woman, and elder man. Each stage has south, west,
east, and north frames for two pose families: `idle` and `interact`.

Every logical frame is 24x32 RGBA with a feet pivot of `(12, 31)`. The idle
cue is a quiet age-specific rest; the interaction cue is a safe, readable
gesture such as reaching for a toy, waving, showing a toy, offering a phone,
offering tea, or greeting with a cane. Infant and toddler gestures are limited
to care-safe play and communication cues.

## Provenance

`build_age_idle_interact.py` reuses the body silhouettes from the local,
original `directional-age-refine-v1` movement studies and adds deterministic
Pillow pixel clusters. It does not read any supplied ZIP, third-party sprite,
web image, or external archive. The source PNGs are never modified. The
manifest records the source frame path and SHA-256 for every derived frame.

## Files

- `frames/<stage>/*.png`: individual 24x32 concept frames.
- `frames/<stage>/*-idle-interact-atlas.png`: 2-column pose by 4-row direction atlas.
- `age-idle-interact-preview-4x.png`: nearest-neighbor review sheet.
- `manifest.json`: exact coverage, cues, pivots, hashes, source hashes, and limitations.
- `build_age_idle_interact.py`: reproducible generator.

Rebuild with:

```sh
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 build_age_idle_interact.py
```

This is not runtime-ready. The reused movement silhouettes need an artist pass
for anatomy, clothing and identity continuity; the cues need interaction
semantics, animation timing, collision review, renderer sampling checks, and
runtime atlas registration before integration.
