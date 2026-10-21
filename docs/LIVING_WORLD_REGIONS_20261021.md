# LIVEIT living-world regions / resident animation implementation

**Date:** 2026-10-21
**Branch:** `feat/living-regions-smooth-residents-20261021`
**Evidence:** GitHub repository writes only. No local Expo, Vitest, CI or native-device results claimed before verification.

## Code delivered

| File | Implementation |
| --- | --- |
| `worldRegions.ts` | Original nine-district catalog; deterministic nearest-district lookup, collision-safe regional transit destinations, and region-to-existing-game-activity mapping |
| `residentProfiles.ts` | Stable named procedural residents with contextual work roles, original outfit accent palette and small 2D accessories (no borrowed franchise art) |
| `ambientPedestrians.ts` | Sidewalk movement with stable ID/appearance, reversible triangular trajectories, smoothstep position interpolation, collision checks on integer logical coordinates |
| `AmbientActor.tsx` | React Native native-driver spatial interpolation and four-frame movement using the already-licensed Pulse n1 animation sheets; stationary animation remains idle; n2 uses the approved directional stills |
| `ArcadePixelLife.tsx` | Live world renders resident characters, tap-nearby introductions with saved acquaintances, nine region transit choices, district-specific accents, compatible regional activity semantics and distance-derived player gait |
| `residentDialogue.ts` | Authored, fully offline regional resident observations with deterministic variation by simulated day |
| `livingRegions.test.ts` | Automated regression fixtures for arrival validity, generated IDs, view-order stability, collision, interpolation, activity selection and deterministic dialogue |

No unapproved concept sprites were activated. The 86 concept packs retain `runtimeReady: false`. Basic avatar variety comes from original names, small pixel accessory layers and the existing two verified CC0 character looks. More character bodies, age lines, portraits and wardrobes require visual/identity/rights/device QA.

## Play path to verify

1. Start or resume the game on the branch; open Free Life in the mobile player.
2. Enter **REGIONS** and travel to North Quay or Willowmere. Validate that the avatar is on a solid-free logical tile and travel survives a process restart.
3. Walk the district. Verify that sidewalks have smooth, deterministic NPC trajectories and native crisp pixels, that NPCs are not visibly walking while stationary, and that a change in camera viewport does not reroll identity.
4. Approach a crowd resident and tap their tile. Read region-specific offline dialogue; **INTRODUCE YOURSELF** should only claim success after AsyncStorage acknowledges the saved ID. Close and reopen: the same resident should offer **ASK ABOUT THE NEIGHBORHOOD**. Check saved regional-discovery indicators across transit and reload.
5. Return to Bellweather, walk to the café, enter, meet Amelia, and verify authored choice and saved world consequences unchanged.
6. Inspect busy streets and low-end hardware for frame pacing, memory, layout, legible controls and actual gameplay. Test iOS and Android separately.

## Source/license investigation for multi-region game inspiration

- PokeMMO / multi-region Pokémon fan projects demonstrate interconnected worlds and region-specific content, but their public source and launch scripts **do not grant redistribution rights to Pokémon maps, species, ROMs, tiles or music**. The PokeMMO Linux helper repo explicitly requires legally held game ROMs. We have not copied them.
- RPGJS (https://github.com/RSamaium/RPG-JS) is MIT-licensed and describes tile maps, events, dialogs, save/load and 2D RPG workflows. It is a useful architectural reference, not a transplanted gameplay engine. LIVEIT already has its own TypeScript simulation and React Native renderer, so wholesale engine replacement would risk saves and native compatibility.
- Our nine region names, transit catalog, procedural home/role mapping and graphics overlays were authored for LIVEIT.

## Known limitations

- Nine *coordinate-distinct procedural districts* and a transport UI are implemented; this is **not** nine finished hand-painted cities with shops, schools, interiors, quests and region story campaigns.
- The stage presently has only two approved Pulse body sprites. Claimed 20 named identities and age cycles refer to concept files, not approved live artwork.
- Crowd introductions save a local acquaintance-ID sidecar. They do not silently change canonical relationship trust or produce model-generated dialogue.
- Native-driver animations, TS lint/format and platform rendering remain unverified until CI and device tests.
- Existing Mac Ollama endpoint settings remain in the old conversation view; this slice does not complete the separate phone-native inference integration.
