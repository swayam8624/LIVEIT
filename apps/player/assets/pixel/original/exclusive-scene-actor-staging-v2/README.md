# Exclusive scene actor staging v2

This isolated concept batch supplies original, transparent actor studies for
the four `exclusive-scenes-variety-v1` backdrops: first-paycheck diner, rainy
reconciliation bus stop, harvest-table gathering, and fresh-start apartment.
It does not edit those backdrops, their layout guides, runtime catalogs, or
shared documentation.

## Contents

- Two distinct character identities for each scene.
- Three scene-specific body poses per identity, each in south/east/north/west
  directions: 96 transparent `48×80` RGBA frames total.
- Four directional `64×64` bust studies per identity: 32 transparent portraits.
- One transparent `320×256` low foreground prop plate per scene.
- `actor-staging-atlas.png`, `portrait-atlas.png`, and a nearest-neighbour
  2× four-scene backdrop-composite review sheet.
- `manifest.json` with advisory actor anchors, dialogue/actor-safe regions,
  pivot, z-order, palette/alpha data, and SHA-256 records. All records remain
  `runtimeReady: false`.
- `prompts.md` with original character and prop design prompts, plus
  `hashes.sha256` for every generated PNG.

All authored actor and overlay pixels use integer primitives and binary alpha.
Body frames use bottom-centre pivot `(24,79)`; busts use `(32,63)`. Scene
anchors describe review placement only. The foreground plate is authored as a
separate full-scene overlay and does not establish final per-object occlusion
or animation timing.

## Rebuild and validate

From the repository root on this machine:

```sh
/opt/homebrew/opt/node@22/bin/node apps/player/assets/pixel/original/exclusive-scene-actor-staging-v2/build_actor_staging.mjs
/opt/homebrew/opt/node@22/bin/node apps/player/assets/pixel/original/exclusive-scene-actor-staging-v2/validate_actor_staging.mjs
```

The scripts use `pngjs` and Prettier already installed in the repository. The builder
reads only the existing scene manifest and concept backdrops for identifiers,
palette mood, and a disposable visual review composite. It never writes to
that source batch. Authored actor/prop sprites are drawn from scratch; no
external art, supplied archive, download, font, logo, or image-generation
service is used.

## Review limits

These are original concept studies, not canonical saved-character identities
or runtime-ready animation. Manual cleanup and identity matching, expressive
mouth/blink frames, perspective checks, scene-by-scene foreground occlusion,
phone-size readability, animation timing, renderer integration, and native
device review remain outstanding. The composite is a staging aid only and
does not settle final layering. The batch is intentionally not referenced by
runtime code or the asset catalog.
