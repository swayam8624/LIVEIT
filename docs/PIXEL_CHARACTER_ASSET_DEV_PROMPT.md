# Dev AI prompt: integrate LIVEIT's pixel character and scene assets

Paste this into the implementation task for the dev AI. The player art is in
concept production; implement the loader and runtime behavior behind explicit
readiness gates. Do not present the concept packs as finished production art.

---

You are implementing LIVEIT's all-2D pixel game. Read `AGENTS.md`,
`docs/PIXEL_ONLY_DIRECTION_V2.md`,
`content/production-assets/pixel-v2/required-assets.json`,
`docs/PIXEL_SPRITE_FAMILY_COVERAGE.md`, and
`apps/player/assets/pixel/registry/README.md` first. The pack index is
`apps/player/assets/pixel/registry/character-packs.json`. Use each package's
manifest as the authority for filenames, dimensions, pivots, frame order,
identity labels and provenance.

## Current asset state and boundaries

- Original generated concepts are under
  `apps/player/assets/pixel/original/<pack>/`. The registry indexes 86 packs.
  It does not mean those packs are loaded in the game.
- The current static Metro asset imports are in `apps/player/src/pixelArt.ts`.
  Today that module imports the verified Pulse CC0 base pack and two placeholder
  character types. `apps/player/src/pixelAgeSprites.ts` separately wires the
  linked player age movement atlas behind a strict saved-Appearance match and
  Amelia's adult/senior (elder-art) movement cycles. Unsupported player looks
  keep the existing CC0 fallback; story portraits remain unchanged.
- Every indexed concept manifest says `runtimeReady: false`. Keep the production
  catalog rows `planned` until the asset has visual, identity, rights,
  integration, accessibility and device QA evidence. Never rewrite a manifest
  status just to make an asset load.
- Do not copy or import anything from the supplied ZIP archives without checking
  the relevant pack's recorded rights decision and item-level provenance. In
  particular, the SuperRetroWorld character pack disallows AI use and source
  redistribution; Modern Interiors Free is non-commercial; the Humble Gift
  modified files cannot be shared; and other archive licenses remain
  unverified. The original concept generators and generated files are the
  current candidates.
- Respect `PIXEL_ONLY_DIRECTION_V2`: no 3D meshes, rigs, rendered 3D scenes or
  3D cinematic pipeline. Keep current save and simulation behavior intact.

## Pixel scale, frame layout and movement

- The player world is top-down, on a logical 16×16 tile grid. Most actor
  concepts use transparent 24×32 RGBA frames with feet pivot `(12, 31)`. Some
  mobility-diverse actors use 32×40. Never stretch a source frame to fit a
  different canvas: preserve integer nearest-neighbor scale and each pack's own
  pivot. Keep collision footprint separate from the visual frame and anchor
  collision at the feet.
- Direction mapping is canonical: `south` = down, `north` = up, `west` = left,
  `east` = right. Some legacy v2 crowd folders use `front/back/left/right`; use
  `sourceDirection` in their per-role manifests. Do not rotate one direction to
  fake the other three.
- Named walk cycles have four ordered gait phases:
  `contact-a → passing-a → contact-b → passing-b → repeat`. Choose the current
  phase from distance traveled or normalized movement time, not render count, so
  frame cadence is stable across devices. Idle and interact are separate poses;
  never play the walk cycle while stationary or while the actor is interacting.
  Crowd cycles have `walk-a → walk-b → repeat` and `idle`. Manifest phase order
  is authoritative. Tune playback speed from character speed and verify visually
  at native scale; the concepts contain no approved final timing values yet.
- Use nearest-neighbor sampling, integer logical-pixel positions where
  practical, and stable pivots through every direction and age. No blur,
  subpixel resampling, accidental palette filters, or per-frame anchor changes.

## Character lookup, age stages and safe randomization

- Resolve a named person by the persistent canonical person ID, not display
  name, array index, current screen order or a fresh random roll. Resolve
  appearance from saved identity/customization, then select the life stage from
  the authoritative simulation date and that person's saved birth date.
  Stage changes happen only at defined age thresholds and update the visual
  actor atomically; preserve person ID, outfit/identity cues, relationships,
  saved choices, position and facing.
- Concept frame coverage now includes age cycles for all 20 named identities
  and age-appropriate variants for 30 ambient roles. `named-role-age-cycles-v1`
  adds 1,464 frames across 13 identities; combine it with the 22 existing
  identity-stage cycles (528 frames) from `named-family-age-cycles-v1/v2` and
  `named-friend-age-cycles-v1`. `crowd-life-stage-cycles-v1` adds 900 frames in
  75 age-role cycles. The crowd pack intentionally omits implausible child or
  teen occupations. Manifests contain each role's exact stage set.
- Player age concepts still have unresolved branches: two static eight-stage
  lines exist, and the linked four-direction movement aggregates preserve more
  than one adult/elder presentation with source-continuity concerns. Do not map
  pronouns to an art line. Use a persistent, explicit visual identity key or a
  close match against saved appearance metadata; otherwise use the current
  fallback. The current simulation has `infant/toddler/child/teen/adult/senior`;
  the current narrow resolver uses the linked movement atlas and maps `senior`
  to its elder pose. Do not invent a second age-threshold table. Do not broaden
  the Appearance gate until identity continuity and palette matches are reviewed.
- All new and existing age packs remain concept-only (`runtimeReady: false`),
  including the two atlases currently referenced by the limited resolver.
  Frame counts and hashes do not establish identity continuity, visual quality,
  native rendering, or production approval.
- If the selected identity-stage has no complete reviewed pack, use the
  deliberate safe fallback already supported by the character system and mark
  the missing stage in diagnostics. Do not borrow another named person's face,
  silently morph appearance, or randomly select an age/gender presentation.
- Crowd appearance variation may be randomized, but it must be deterministic:
  seed selection from stable `(worldSeed, residentId)` (and a stable variant
  index), then save/persist the assigned resident identity wherever the game
  promotes a crowd resident into a named character. Randomize only among
  compatible, reviewed variants for the same role, age band, outfit/context,
  and mobility/accessibility constraints. Do not reroll on camera movement,
  rerender, app resume, or save reload. Keep named people and story-scene actors
  out of ambient random selection.
- The ambient crowd currently comes from `apps/player/src/ambientPedestrians.ts`
  and uses stable IDs, time-of-day routines and two placeholder looks. Extend
  that deterministic record with a stable pack/variant key; keep routine,
  collision, spawn/portal behavior and simulation identity separate from pixels.

## Where each visual mode belongs

1. **Retro top-down world** (`PixelTown.tsx` / `ArcadePixelLife.tsx`): use for
   walking streets and interiors, shops, school/work, daily routines, weather,
   navigation, exploration and ordinary interactions. Render tile/map layers,
   props, then actors sorted by feet Y (with occlusion rules), then world-space
   interaction indicators. Use the small four-direction movement sprites here.
   Keep doors, collisions, portals, movement, time and saved-world consequences
   connected to the real simulation; a decorative screen is not a playable
   replacement.
2. **Dramatic story or dialogue scene** (`GameStage.tsx`, currently backed by
   `PixelStoryBackdrop.tsx`): remain entirely 2D. Compose an authored scene
   background at a 320×256 logical design size (or use the exact manifest
   dimensions), optional distant/parallax layer, midground architecture/props,
   actor busts or staged full-body sprites, foreground occluders, then a readable
   native dialogue/choice UI above the art. Keep the speaker and reaction actor
   in stable stage anchors; reserve the manifest's dialogue safe region so
   captions and choices never cover faces or important props. Use 2D pixel
   palette/mood changes, nearest-neighbor camera moves, reaction cuts and pixel
   transitions for drama. Do not switch to 3D.
3. **Dialogue actors**: use large portrait/bust art and emotion/acting frames,
   not the tiny overworld sprite enlarged beyond its intended pixel scale.
   Match the portrait to the same canonical identity, age stage and outfit as
   the current story date. Animate from authored mouth/eye/acting frames only
   where available; do not synthesize lip movement by distorting the image.
   Dynamic dialogue text stays native, scalable, selectable and accessible.
4. **Chat, buttons and HUD**: use `chat-avatar-*`, `chat-reaction-icons-*`,
   `conversation-ui-*`, `button-states-*` and `accessible-controls-*` manifests
   only after a runtime consumer and accessibility review exist. Slice panels
   using the manifest's nine-slice insets; keep labels and body text live/native.
   Expose focus, selected, pressed, disabled, error, consent and saved states
   semantically and visually. Art must not fake a successful saved choice;
   show confirmation only after authoritative state persistence succeeds.
5. **Exclusive life scenes** (graduation, first home, new parenthood, elder
   legacy): use scene-specific composable background, midground, prop,
   foreground and dialogue-safe-region layers from the relevant
   `exclusive-scene-*` manifests. Place actors by manifest staging guides and
   sort by explicit layer/depth; never bake dialogue text or actors into a
   flattened backdrop. Preserve age-safe, context-appropriate actor poses.
   These packages are staging concepts and need repainting/cleanup and real
   scene behavior before production.

## Required implementation shape

- Add a typed character asset resolver near `pixelArt.ts` (or a focused sibling
  module) that maps canonical character ID + selected age stage + direction +
  animation state to a static Metro `require()` source and validated metadata.
  Metro cannot safely resolve arbitrary file paths built at runtime. Generate
  static imports from manifests or write an explicit typed map; never use
  `require(dynamicString)` or filesystem access in the app.
- Keep actor gameplay state independent from the image key. When an asset is
  missing or not production-approved, render a known fallback and continue real
  gameplay; do not crash, block saves, replace narrative state or change
  collision dimensions.
- Add diagnostics that report unresolved character/stage/direction/state keys
  once per asset key. Add focused verification for manifest frame coverage,
  hashes/dimensions/pivots, stable deterministic crowd assignment, age-stage
  selection, story-safe-region composition, save/reload and fallback behavior.
  Do not claim complete character art until the actual PNGs have been visually
  reviewed at game scale and every active production requirement has QA proof.

## Completion report

Report which packages and frames are actually loaded, which people/stages still
fall back, what the crowd randomization seed depends on, where overworld and
story art are composed, and which exact commands/device flows were executed.
The first player-loop bar remains: walk the Bellweather street, enter the café,
meet pixel Amelia, make a choice that changes and saves real state, return to the
world, then reload and observe the same outcome.

---

## Current known frame counts

These are concept counts recorded by the prior coverage audit, not a runtime
coverage claim:

- Named role movement: 20 roles × 24 frames each = 480 base concept frames.
- Crowd archetypes: 30 roles × 12 frames each = 360 base concept frames.
- Named age movement: 83 identity-stage cycles across all 20 named identities
  × 24 frames = 1,992 concept frames. Role-specific stage subsets are listed in
  the package manifests; not every person has an infant or toddler stage.
- Crowd age movement: 75 plausible role-stage cycles across 30 crowd roles × 12
  frames = 900 concept frames.
- The eight-stage player age sheet is a static front-facing reference, not a
  complete directional movement pack. The linked player movement concepts have
  several stages, but multiple identity branches have not been reconciled.
- Additional folders contain UI, chat, portraits, pets, effects, world props,
  and exclusive-scene staging. See the registry and `PIXEL_SPRITE_ASSET_NEEDS.md`
  for the concept inventory and outstanding production work.
