# Exclusive scene graduation actors v1

This isolated original concept batch adds transparent, direction-aware actor
poses for the `garden-graduation` exclusive scene. It contains a graduate, a
family supporter, and a teacher. Each role has `stand` plus a ceremony-specific
pose and `cheer`, rendered for south, east, north, and west directions.

The batch contains 36 individual `48×80` RGBA frames, a nearest-neighbour 2×
review preview, and an atlas. Every frame uses the same integer bottom-centre
pivot `(24,79)` as `exclusive-scene-actor-staging-v1`; the advisory scene anchor
is `(156,216)` in the existing `320×256` scene canvas.

`build_graduation_actors.js` uses only integer primitives and repository-local
code. It does not read, embed, or rewrite supplied ZIP assets, downloaded art,
fonts, logos, or third-party images. Existing graduation scene images are
referenced only for scene placement and palette conventions.

These are concept-quality studies. They require manual pixel cleanup, identity
and costume continuity review, occlusion review against the graduation garden,
phone-size legibility review, animation timing, and native renderer acceptance.
All manifest records remain `runtimeReady: false` and the batch is not admitted
to runtime code or the asset catalog.

## Rebuild

```sh
/opt/homebrew/opt/node@22/bin/node build_graduation_actors.js
```
