# Pixel sprite runtime integration — evidence ledger (2026-10-20)

This slice implements **deterministic visual assignment for ambient residents** without claiming that concept art has shipped.

## Implemented and committed

- `apps/player/src/spriteIdentity.ts`: stable 32-bit hash of `(worldSeed, residentId)`; only two currently bundled Pulse CC0 looks are eligible.
- `apps/player/src/ambientPedestrians.ts`: adds `spriteKey` to every ambient record; movement, spawning, collisions, routines, world identity and gameplay still use their existing logic.
- `apps/player/src/spriteIdentity.test.ts`: deterministic mapping, approved-key allowlist, seed normalization and discovery-order assertions.

The visual key is ready to be stored in a persisted named-resident record if a crowd resident is promoted, **but no such save-schema migration has been made**. No generated concept manifest or production catalog status has been modified.

## Runtime coverage and missing gates

- **Actually referenced by this change:** existing `pulse:n1` / `pulse:n2` CC0 character family through the unchanged `look` renderer. The new `spriteKey` is metadata only; it does not load a new PNG.
- **Concept art activated:** zero. The index of 86 original concept packs, 20 named people, 83 identity-stage cycles and 75 crowd role-stage cycles remains concept-only (`runtimeReady: false`).
- **Named character and age fallback:** unchanged; the existing narrowly gated player/Amelia age atlases remain as before. All other unresolved identity/stage/direction/state combinations need verified mappings and safe fallbacks.
- **Seed:** stable integer world seed + stable resident ID (including existing chunk coordinate and slot). Not dependent on camera, display order, clock time, frame count or rerender.
- **Overworld composition:** `PixelTown.tsx`, `ArcadePixelLife.tsx` and `pixelArt.ts`. **Story composition:** `GameStage.tsx` / `PixelStoryBackdrop.tsx`.
- **Device and test evidence:** GitHub source modifications only in this session. Node/npm, Metro and iOS/Android simulators were not run; do not mark test, native QA or gameplay bar passed.

## Subsequent hard gates

1. Generate static Metro sprite bindings from each approved manifest, with per-frame dimensions, pivots, direction and phase metadata; reject dynamic `require()`.
2. Inspect every intended PNG for rights/provenance, palette and canonical identity; compare it at native 16-pixel scale on real mobile devices; approve each pack explicitly before adding it to the resolver.
3. Resolve appearance by persistent canonical ID and saved cues, then simulation-derived age stage. Keep pose and identity continuity; missing packs use a diagnostic fallback.
4. Separate actor feet/collision footprint from drawn sprite size. Drive walk phase by travel distance or simulation time; test four directions and idle/interact transitions.
5. Preserve native, selectable, accessible dialogue and reliable state acknowledgments. Validate Bellweather street → café → Amelia → meaningful saved choice → return → restart.
6. Record Android/iOS visual screenshots, FPS/frame-pacing, accessibility checks, hashes, tests and save/reload traces before promoting production catalog items.

## Commands to run on the exact branch

```bash
git switch feat/pixel-sprite-identity-gates-20261020
npm ci
npm run check
npm run web -w @living/player -- --clear
# On macOS with Xcode and booted simulator:
npm run ios
# Separately test a configured Android emulator/device:
npm run android
```

The checklist is an evidence requirement, not a declaration that those flows succeeded.
