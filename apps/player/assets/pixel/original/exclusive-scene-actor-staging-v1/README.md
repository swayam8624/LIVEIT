# Exclusive scene actor staging v1

This isolated original concept batch adds transparent, direction-aware actor
poses for the existing `new-parenthood` and `elder-legacy` scene studies. It
is intended for compositing review against the actor-safe guides in
`exclusive-scene-depth-v2/`; it does not change those scene layers or admit
anything to the runtime catalog.

## Contents

- Two scene folders, each with two actor identities.
- Three actor-safe staging poses per identity, each drawn for south, east,
  north, and west directions (48 individual `48×80` RGBA frames total).
- `actor-staging-atlas.png` (`384×480`) and a nearest-neighbour 2× review
  image (`actor-staging-preview-2x.png`).
- `manifest.json` with exact dimensions, alpha mode, SHA-256 hashes, scene
  anchors, dialogue-safe region, frame pivots, directions, and `runtimeReady:
false` for the batch, scenes, actors, frames, and files.
- `hashes.sha256` for a quick integrity check.

All frames use an integer bottom-centre pivot at `(24,79)` within their
`48×80` canvas. Scene anchors are advisory compositing points in the existing
`320×256` scene canvas. They are not collision bounds or final animation
timings.

## Rebuild

From this directory:

```sh
/opt/homebrew/opt/node@22/bin/node build_actor_staging.js
```

The builder uses only `pngjs` already present in the repository dependency
tree. It draws the actors from integer primitives and does not read, embed, or
rewrite any existing artwork. Existing original scene batches are referenced
only for palette/staging conventions. No supplied ZIP, downloaded file,
third-party image, font, logo, or image-generation service was used.

## Honest status

These are concept-quality staging studies. The poses are suitable for
compositing experiments and direction/pivot review, but still need manual
pixel cleanup, identity continuity checks against the saved character,
occlusion review with each scene's props and foreground, phone-size legibility
review, animation timing, and native renderer acceptance. They remain
`runtimeReady: false` and are intentionally not referenced by runtime code or
the asset catalog.
