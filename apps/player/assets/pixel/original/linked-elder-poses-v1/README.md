# Linked elder poses v1

This is an isolated, concept-only batch for the linked life-arc family. It
contains 16 transparent 24×32 RGBA frames: elder woman and elder man, each
with south, west, east, and north directions, and `idle` / `interact` states.
Every frame uses the shared bottom-center pivot `[12, 31]`.

The elder woman interact studies use a small open-hand wave cue. The elder man
studies use a short steadying-cane / hello cue. These are care-safe, readable
interaction concepts intended to support accessible acknowledgement without
requiring intimate or strenuous actions.

## Provenance and identity

The only visual references are the local original frames in
`../life-arc-later-cycles-v1/frames/elder-woman/` and
`../life-arc-later-cycles-v1/frames/elder-man/`. No supplied ZIP, web image,
third-party game art, or external asset was used. The source batch is not
edited, copied into this folder, or promoted to runtime.

Each direction is authored from its matching source frame. The builder does
not mirror or flip frames. Silver-white elder hair, deep-brown skin, sky-blue
clothing, and warm ochre accents keep the batch visually linked to
`linked-life-arc-family-v1`.

## Rebuild and validation

Use the repository's bundled Pillow runtime from the repository root:

```sh
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  apps/player/assets/pixel/original/linked-elder-poses-v1/build_linked_elder_poses.py
```

The builder writes per-stage atlases, a combined atlas, a nearest-neighbor
review preview, and `manifest.json`. The manifest records each frame hash,
the matching source-frame hash, source-sheet hash, atlas rectangle, pivot,
dimensions, and `runtimeReady: false` / `conceptOnly: true`.

The atlas direction order is explicitly south, west, east, north, with idle
then interact for each direction. The
source mapping is explicit in the manifest so reviewers can confirm that no
direction was created by mirroring.

`manifest.json` also records SHA-256 references to the local harmonized elder
atlases in `../linked-life-arc-family-v1/harmonized-32-color/`. Those files are
used for palette and identity-cue comparison only; they are not copied into
this batch or promoted to runtime.

## Review boundary

This package proves transparent frame coverage, reproducible derivation, and
source provenance. It does not prove final anatomy, animation timing,
collision behavior, renderer sampling, accessibility acceptance, save/reload
continuity, or runtime integration. A pixel artist must review and reconcile
the wave/cane clusters before this concept can become a production asset.
