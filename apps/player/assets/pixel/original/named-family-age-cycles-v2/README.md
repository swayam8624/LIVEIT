# Named family age cycles v2

This isolated original concept pack extends named-character lifecycle coverage
for Nora Bellweather (adult → midlife → elder) and Tavi Bellweather (toddler →
child → teen → young adult). Each stage has 24 independently rasterized 24×32
RGBA frames: four cardinal directions, each with four gait phases plus idle and
interact. All frames share feet pivot `(12, 31)` and remain `runtimeReady: false`.

## Identity cues and pose boundaries

Nora retains the canonical short indigo bob, rose overshirt, cream ring, and
wide-leg trousers. Midlife introduces a few silver strands; elder shifts to
silver hair and a discreet cane. Tavi retains the purple cap, leaf-green
overalls, violet boots, and kite-spool cue. Clothing and cap scale with growth;
all Tavi poses are fully clothed, age-safe, and non-romantic. The child kite
spool appears only at toddler and child stages.

## Package files

- `frames/<identity>/<stage>/` contains the individual frames.
- `named-family-age-cycles-v2-atlas.png` arranges stages in seven 4-row bands.
- `named-family-age-cycles-v2-contact-sheet.png` presents the seven bands in a
  four-column review grid.
- `manifest.json` records frame IDs, catalog references, pivots, directions,
  phases, SHA-256 hashes, source lineage, atlas hashes and runtime gates.
- `provenance.json` records the original prompt, rights statement, builder and
  concept limitations.
- `build_age_cycles.py` is a deterministic Python standard-library builder.
- `validate_age_cycles.py` checks coverage, PNG structure, hashes, lineage and
  rejects duplicate phases or frames within each identity-stage cycle.

## Build and validate

From the repository root:

```sh
python3 apps/player/assets/pixel/original/named-family-age-cycles-v2/build_age_cycles.py
python3 apps/player/assets/pixel/original/named-family-age-cycles-v2/validate_age_cycles.py
```

The builder references identity metadata from `named-characters-batch-v2`; it
does not read or copy image bytes from `named-family-age-cycles-v1`. These are
concept sprites pending artist review, motion playback review, renderer
sampling, collision/pivot integration and device validation. Catalog IDs are
references only; no runtime mapping or runtime promotion is included.
