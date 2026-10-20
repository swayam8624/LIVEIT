# Pixel character concept registry

This registry is the game-facing index for the authored pixel concept packs in
`../original/`. It makes the packs discoverable from the player asset tree while
keeping their provenance and review status attached. `apps/player/src/pixelArt.ts`
still statically loads the verified Pulse base assets. The separate
`apps/player/src/pixelAgeSprites.ts` resolver has a narrow integration for the
linked player age atlas and Amelia's adult/elder atlas. Player art is selected
only for a strict saved-Appearance cue match; unsupported appearances keep the
existing CC0 actor. Do not set `runtimeReady` or change the production catalog
from this registry alone.

Open [`character-packs.json`](./character-packs.json) for exact pack paths,
manifest paths, available frame counts and status. Individual manifests are the
source of truth for image filenames, dimensions, frame order and pivots. The
family-level gap audit is in [`docs/PIXEL_SPRITE_FAMILY_COVERAGE.md`](../../../../../docs/PIXEL_SPRITE_FAMILY_COVERAGE.md).

Before moving a concept pack into runtime imports, complete the gates in
`docs/OPEN_SOURCE_ASSET_PIPELINE.md` and the active pixel production checklist:
visual review at native scale, person/age identity continuity, complete states
and directions, rights and provenance, platform bundle behavior, and player
integration. Current generated packs are original concepts; ZIP contents are
not included by this registry.
