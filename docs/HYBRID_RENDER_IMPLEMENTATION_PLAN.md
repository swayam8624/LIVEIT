# LIVEIT Hybrid Renderer — Implementable Delivery Program

**Status:** implementation and migration plan, dated 2026-10-19, **NOT** shipped feature list. Visual source-of-truth: GDS-001 → GDS-002 → ENG-003. Only phase-bound code changes and source-level readiness gates have been added so far. Preserve existing working simulation/story/save compatibility and honest illustrated fallbacks.

## Required product result

Live an actual original, top-down **pixel** everyday life like an early handheld RPG with responsive controls, people, jobs, interiors and aging, then see real premium stylized **3D** character acting whenever a story/conversation matters, with game-console tactile sidebar widgets and accurate outcome/haptic feedback. Both use identical persistent character identity and outfit. Android renders via Vulkan, Apple via MoltenVK. No copyrighted competitor game assets.

## Workstreams and dependency graph

    Domain save + tile navigation -------+
    Original tile/actor atlases ------+  |
                                      v  v
    GPU Pixel Pipeline ------------> Native Expo View/SWAPCHAIN
                                              |
    Licensed 3D glTF Rig -> 3D GPU Pipeline --+
                                              |
    Scene handoff + state receipt -----------+
                                              |
    HUD widgets, accessible controls, haptics
                                              |
    All-device vertical-slice E2E/benchmarks
                                              |
    Content packs / town growth / social / release

The temporary illustrated map and story stages remain available until each replacement is proven and capability-gated. No direct JS mutation from renderer selection/haptics.

## Milestone M0 — Branch hygiene and test gates

**Existing source:** apps/player (Expo 58/RN 0.88), shared TS simulation/story/world schemas, local saves, currently illustrated map/stories; native/city-vulkan offscreen proof.

**Work:** pull/merge latest branch without overwriting user modifications (especially apps/creator-studio/next-env.d.ts). Run npm ci, npm run check, Expo native iOS install and Android emulator; capture actual screenshots, failures and test logs. Avoid speculative checkmarks from web export or successful PPM GPU CI. Fix foundation warnings and verify exact commit, native iOS and Android separately.

**Acceptance:** same commit passes format/lint/types/unit/export, local save unchanged before and after branch update, existing city visit and story choice work after relaunch.

## Milestone M1 — World map authority / persistence (critical path)

**Proposed source:** packages/world-schema/src/world-navigation.ts, simulation-core/src/world-navigation.ts, save-system migration tests, content/maps/bellweather-*.

**Work:** model TilePosition {region, mapRevision, x, y, facing, doorway, interiorReturn}; add optional migration-safe saved world field with deterministic old-save spawn; no always-age-23 replacement world. Define collision/portal/mobility/interaction masks and deterministic 16px tile world coordinates. Walking input seq/idempotency, fixed tick, 4-direction step and blocked target; day advances only on explicit domain actions. Persist one tile/portal operation with event/revision; handle invalid saved maps and pack unavailability.

**Acceptance:** unit tests 1,000 blocked/nonblocked walking commands on seeded map; same coordinates/facing after reload and interrupted save; portal exit returns correct coordinate; v1 legacy save loads intact with same day/trust/money.

**Blockers:** no actual walkable map/tiles currently bundled; must author one lawfully.

## Milestone M2 — Original retro pixel art / walkable UI baseline

**Proposed source:** content/world-packs/bellweather-market v1, tools/asset-pipeline/tilepack, apps/player/src/game/GameViewport.tsx, PixelHud and InputCoordinator.

**Work:** original 16px tile city starter pack: road/sidewalk/grass/roof/wall/window/shop/café door/tree/weather sign; NPC/player 4-direction 4-walk frames and collision; sprite/tile anchors consistent with appearance; view viewport logical 320×256 and safe-area mobile framing; joystick, arrows, tap-route and controller focus; actual entered café pixel interior. Retain current CityMap only as user-accessible fallback/fast-travel route.

**Acceptance:** phone sees actor move four tiles, attempts blocked movement, interacts with café door and NPC, input and camera remain pixel sharp even at non-integer device scale. Asset provenance and animation fixture committed. A static screenshot is insufficient.

## Milestone M3 — Native Vulkan/MoltenVK view and 2D raster

**Proposed source:** native/liveit-render/{include,src,shaders}, apps/player/modules/liveit-render/{android,ios,src}.

**Work:** refactor headless Vulkan only as _development test harness_; a new shared C++ runtime with Vulkan instance/device, surface, swapchain, queue, multi-frame submit/present, dirty chunk atlas uploads, logical pixel target, nearest presentation, visibility sorting and pixel lighting/weather. Wrap in Android Kotlin ExpoView SurfaceView + JNI, iOS Swift ExpoView CAMetalLayer + Objective-C++/MoltenVK, proper slices/linker flags, teardown/recreate, debug validation. JS props use the validated render-contract.ts messages; avoid heavy JSON per vsync. Read render capability callbacks, not an assumed file/existence check.

**Acceptance:** on real iPhone and Android, installed app displays **actual Vulkan-composited top-down world**; documented device names/driver, drawable lifecycle, scene frame and screenshots; background/foreground and resize 50x safely; no native memory corruption.

**Important:** do not use WebGL/Skia to assert this gate; they are allowed as fallback UI technologies only.

## Milestone M4 — Real stylized 3D cinematic actors

**Proposed source:** original licensed glTF character source, rig bones/morph registry, cinema shader pipeline and GDS-001 shot director.

**Work:** produce at least two original **mesh/skinned** adult characters with stable body/head bones, hair/clothes/materials, eyes/brows/mouth blend shapes and expressions. Build 3D depth/environment/material shader passes, rig animation, light/shadow, camera presets, response to actual saved outfit and age. Draw café room, shadows and actor blocking. Text remains semantic native dialogue dock. Blend transition out of pixel world and back; no fake offscreen PPM used as live actor.

**Acceptance:** 3D rendered iOS/Android scene with two clearly distinct actors, validated camera framing and 12 different facial expression states; actual 3D rig source/model/license; matching pixel avatar hair/outfit; screenshot/video and animation test.

## Milestone M5 — Handoff, choices, haptics, widgets, app memory

**Proposed source:** apps/player/src/game/SceneHandoff, choice dock/OutcomeQueue/Haptics service, narrative-core and save coordinator transaction additions.

**Work:** walk→approach→interact→warm assets→transition→conversation→choose→save ack→accurate outcome widget→return to same pixel tile. Exact event IDs and scene revisions, bounded queues, stale input rejection, lifecycle resume. Settings Off/Subtle/Full and Reduce Motion; only _committed_ choices produce confirmation haptic. Grief context avoids cheerful cues.

**Acceptance:** full 3D Amelia café interaction after pixel-world meeting, trust delta matches world and journal, same coordinates/appearance remain after force-close. Error/retry and 10x rapid taps cannot double-pay or double-choice.

## Milestone M6 — World, lifecycle and content expansion

**Work:** 5 distinct walkable districts, home and career/school interiors, crowd/NPC schedules, town assets and fast transit, aging sprite/rig parity, memory/legacy scene context. Introduce playable life stages based on actual world age; do not fake birth-to-death by color tint. Return from every drawer without losing focus. Add signed data-pack downloads, platform-native cache and truthful storage UI.

**Acceptance:** 30-minute play on medium Android and physical iPhone covering 3 location changes, NPC encounters and year progression with no lost save. Battery/thermal/memory recorded, accessible text navigation successful.

## Milestone M7 — Production art/content/economics and service quality

**Work:** grow real production inventory toward the user’s ~400 rig parts, ~200 reusable authored locations, 12 expressions and ~30 camera/FX presets. Author chapters, career/family/legacy loops, NPC memory integration and lawful opt-in human communications with backend/age/privacy/safety/moderation. Pack build/publish/sign/rollback, QA, performance/size/caching metrics and actual human device playtests.

**Acceptance:** never equate a target with the current count; verify original art/license, device screenshots, distinct meaningful branches, replay variety, real human statuses and store-compliant social availability.

## R1 technical API contract (already present in Step 3)

- world-schema/src/render-contract.ts exports validated PixelRenderFrameSchema / CinematicRenderFrameSchema / RenderUserIntentSchema / OutcomeReceiptSchema and integer viewport plan.
- simulation-core/src/render-adapter.ts converts authoritative world to pixel/3D frame, but **expects a supplied valid navigation pose** because persistence is not implemented.
- apps/player/src/visualPresentation.ts (Step 4) defines VisualCapability and selectVisualPresentation. It refuses to label a renderer as native until a real supported mode, active generation and required assets are ready. It is currently statically FALLBACK, not native detection.
- CityWorld and StoryPlayer retain their screens, use the fallback policy and avoid falsely calling selection-map a walkable town or RN cutouts a native 3D scene.
- tests/visual-presentation.test.ts checks unloaded, unsupported, unmounted and valid backend cases. It does not prove a native device.

Add actual native module event decoding plus generation verification before permitting readiness in production; never flip a boolean without proving the API/surface installed.

## Phase gates / signoffs

| Gate                                | Test and proof                                                        | Current                         |
| ----------------------------------- | --------------------------------------------------------------------- | ------------------------------- |
| A: existing gameplay remains intact | TypeScript Vite/Vitest + Metro/web + existing local save              | Partial; follow latest exact CI |
| B: domain pixel position real       | deterministic collisions/portal + old-save migration                  | NOT IMPLEMENTED                 |
| C: GPU pixel tiles playable         | native Vulkan/Metal through MoltenVK, on-device screenshots and input | NOT IMPLEMENTED                 |
| D: 3D story actors                  | actual glTF skeleton/face animation rendered on devices               | NOT IMPLEMENTED                 |
| E: scene conversion                 | pixel→3D→same position + saved consequence + haptic                   | NOT IMPLEMENTED                 |
| F: pack delivery                    | licensed/hashes/signed indices/atomic store and rollback              | SCHEMA ONLY                     |
| G: human social safety              | verified real contacts, consent, report/block and store compliance    | NOT IMPLEMENTED                 |

The old native/city-vulkan PPM CI is an **offscreen GPU proof**, not gates C/D.

## Repository hygiene / working agreement

- Do not rewrite the TS domain just to simplify the GPU architecture.
- Do not delete working CityMap, StoryPlayer, local stories, save adapters, actual assets or financial/NPC tests while replacing visuals. Decommission only after demonstrated native equivalent.
- No external competitor assets; look at gameplay grammar and build original designs.
- Every new shader, asset and model: license/source/version/hash and owner; no download-executed SPIR-V.
- Preserve old save files and test rollback; use reversible branches and code-reviewed steps.
- Native renderer errors always fallback to honest UI and preserve world.
- Update docs/BUILD_STATUS.md after verified tests, not wishful thinking.
- Only Step 5 will author the comprehensive individual asset item inventory; do not pretend it is already finished by this plan.
