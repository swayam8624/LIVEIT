# Named friend age cycles v1

Original lifecycle movement concepts for Amelia Chen and Noah Bennett. Each
identity has adult, midlife, and elder stages. Every stage contains 24
individually rasterized 24×32 RGBA frames: south, west, east, and north, each
with contact-a, passing-a, contact-b, passing-b, idle, and interact. All frames
share the feet pivot `(12, 31)` and remain `runtimeReady: false`.

## Identity and age cues

- Amelia keeps her brunette bob, cream blouse, teal apron dress, gold earring,
  and teal shoulder satchel. Midlife adds silver temple strands and a rose
  layer; elder shifts to a silver bob, softer silhouette, cardigan details,
  and a discreet cane.
- Noah keeps his tall, lean build, auburn close crop, rolled-sleeve blue shirt,
  café apron, and pocket notebook. Midlife adds silver temples and a sage layer;
  elder shifts to silver hair, a relaxed posture, cardigan details, and a
  discreet cane.
- Interact poses are gentle open-hand conversation gestures. The cane is a
  mobility cue and remains planted beside elder characters.

These are deterministic, hand-authored pixel concepts built from simple raster
shapes, not production-ready character art. Please review facial readability,
age separation, garment details, gait playback, and the elder mobility cue at
native scale before runtime use.

## Files

- `frames/<identity>/<stage>/` — the 144 individual source PNGs.
- `named-friend-age-cycles-atlas.png` — six stage bands; six phase columns by
  four direction rows per band (144×768).
- `named-friend-age-cycles-contact-sheet.png` — Amelia's three age stages in
  the first row and Noah's in the second; each cell shows one complete 6×4
  cycle (432×256).
- `manifest.json` — frame IDs, directions, phases, pivots, SHA-256 hashes,
  catalog IDs, and links to the exact named-identity manifest/cues.
- `provenance.json` — rights statement, source lineage, and generation brief.
- `build_friend_age_cycles.py` — deterministic Python standard-library
  builder.
- `validate_friend_age_cycles.py` — coverage, uniqueness, PNG, hash, lineage,
  and no-overlap checks against the base named-character frames and both
  existing named-family age-cycle packs.

## Build and validate

From the repository root:

```sh
python3 apps/player/assets/pixel/original/named-friend-age-cycles-v1/build_friend_age_cycles.py
python3 apps/player/assets/pixel/original/named-friend-age-cycles-v1/validate_friend_age_cycles.py
```

The builder uses only the Python standard library. All frames need artist
review, animation playback review, collision/pivot integration, renderer
sampling, and device validation before any runtime promotion. This pack does
not modify the base named-character or named-family age-cycle packs.
