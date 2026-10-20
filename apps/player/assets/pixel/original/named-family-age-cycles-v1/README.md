# Bellweather named-family age cycles v1

An additional original concept movement pack fills age-transition gaps for the
three named family identities. It contains nine identity-stage cycles: Mara
adult → midlife → elder, Eli adult → midlife → elder, and Niko child → teen →
young adult. Each cycle has 24 independently generated 24×32 RGBA frames:
south, west, east, and north, each with contact-a, passing-a, contact-b,
passing-b, idle, and interact. Every frame uses feet pivot `(12, 31)`.

## Files

- `frames/<identity>/<stage>/` — individual transparent PNG frames.
- `named-family-age-cycles-atlas.png` — all nine stages, with six phase columns
  and four direction rows per stage band (144×1152).
- `named-family-age-cycles-contact-sheet.png` — nine stage atlases in a 3×3
  review grid (432×384), ordered as the `ageTransitions` map in the manifest.
- `manifest.json` — frame records with per-frame SHA-256, dimensions, pivot,
  direction/phase, age stage, catalog mapping, and source lineage hashes.
- `provenance.json` — rights/provenance declaration and full generation prompt.
- `build_age_cycles.py` — deterministic standard-library PNG builder.
- `validate_age_cycles.py` — coverage, image structure, digest, and unique-pose
  validation.

## Visual cues

Mara keeps her curls, rust clothing, mustard scarf, tote, and pear-shaped
silhouette; midlife adds a few silver curls and face lines, while elder adds
more silver hair, a fuller silhouette, and cane. Eli keeps his close crop,
round glasses, navy jacket, and ochre shirt; midlife broadens his shape and
elder adds silver hair, brighter glasses, and cane. Niko keeps curly hair and
ponytail, cobalt hoodie, orange shoes, and backpack while growing taller and
more proportionate through teen and young-adult stages. Interactions are
friendly, non-romantic, fully clothed, and age-safe at every Niko stage.

## Build and validate

From the repository root:

```sh
python3 apps/player/assets/pixel/original/named-family-age-cycles-v1/build_age_cycles.py
python3 apps/player/assets/pixel/original/named-family-age-cycles-v1/validate_age_cycles.py
```

The builder uses Python's standard library only and produces the same pixel
bytes on repeat runs. All manifest entries remain `runtimeReady: false`. The
sprites are concept work requiring artist review and cleanup, animation
playback review, renderer sampling, collision/pivot integration, and device
validation before any runtime promotion. The `young-adult` Niko stage is a
modest continuation of the canonical child cues and should receive human age
readability review.
