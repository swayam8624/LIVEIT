# LIVEIT BUILD STATUS — observed, not aspirational

Updated 2026-10-19. Branch: feat/native-life-economic-foundation. Main remains the earlier foundation. PR: https://github.com/swayam8624/LIVEIT/pull/8

| Area                 | Reality                                                                                                                                      | Evidence / next gate                                                                                                 |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Node/TS domain tests | Previous branch CI Foundation checks succeeded; check most recent head as code changes                                                       | GitHub Actions > Foundation checks                                                                                   |
| Formatting           | Whole-repository Prettier normalization workflow created; bot may create formatting commit on push                                           | Verify npm run check at exact fetched commit; previous 23 warnings were on legacy source paths                       |
| iOS native run       | Old local Expo Go route failed simctl openurl timeout (code 60); npm run ios has been replaced with expo run:ios                             | Run latest branch on local Mac, boot simulator manually if necessary, capture actual user interaction and screenshot |
| iOS CI build         | macOS native simulator test workflow exists; initial Xcode 16.4 run failed at Swift package resolution; macos-26 rerun not yet verified here | Inspected CI log, native proof required; SDK exports don't count                                                     |
| Android              | Android Expo bundle export previously tested; Android emulator run not demonstrated                                                          | Run expo run:android and automated UI flows                                                                          |
| Life simulation      | Career progression; 13 authored annual decisions with persistent consequences; fictional assets/index investment with upkeep                 | Gameplay is partial: initial player still age 23, no birth→death systems, no mortality and legacy                    |
| Cinematics           | Existing short dialogue/story player, preliminary art/character editor                                                                       | No demonstrated Episode-grade rigs, blocking, animations or scene production                                         |
| AI NPCs              | No deployed provider-backed chattable NPC with evaluated semantic/episodic memory                                                            | Provider, memory storage/evaluation and privacy controls unimplemented                                               |
| Human multiplayer    | No deployed two-client anonymous/contextual message system                                                                                   | Backend, authentication, abuse controls, room delivery and real-world compliance unimplemented                       |
| QUIC                 | No QUIC transport implemented/tested                                                                                                         | Needs real physical device/network test after baseline TLS transport                                                 |
| Vulnerabilities      | User's npm ci reported 22 advisories: 7 moderate, 15 high                                                                                    | Inspect npm audit detail and actual production exposure; do not auto-apply force updates                             |
| Playtesting          | No verified external 10-minute playtest or retention metrics                                                                                 | First iOS simulator quality baseline required                                                                        |
| Research             | Competitor/feature dossier grounded in public official pages plus archived OpenLife code                                                     | Real gameplay video timestamp ledger is yet to be completed, must never be faked                                     |

## 2026-10-19 Step 4: hybrid direction reconciliation and source fallbacks

**Direction now locked:** top-down original **pixel tile/sprite Free Life**, true **skinned mesh 3D** dialogue/story and accessible tactile native HUD; **NOT** the previously proposed 3D/isometric city as primary roaming mode. Read docs/DOCUMENT_INDEX.md for precedence and docs/HYBRID_RENDER_IMPLEMENTATION_PLAN.md for concrete M0–M7 implementation dependencies. GDS-001, GDS-002 and ENG-003 remain authoritative.

| Item | Verified source or limitation |
|---|---|
| Art and mission docs | docs/UNIFIED_VISUAL_ENGINE_VISION.md and ART_DIRECTION.md rewritten to the pixel/3D/HUD split, with prototype and target distinctions |
| Agent instructions | AGENTS.md previous "interactive 3D city Free Roam" and unresolved Skia/2.5D production choices removed; historical REA/legal/QA instructions retained |
| Historical specs | docs/VULKAN_CITY_RENDERING.md and LIVEIT_2_GAMEFEEL_CONTENT_MASTERPLAN.md marked or updated for superseded graphics assumptions; NATIVE_RECONSTRUCTION.md aligned |
| README and index | README now prioritizes the hybrid GDS/ENG guides and correctly calls CityMap an illustrated district-selection fallback |
| New source | apps/player/src/visualPresentation.ts resolves native GPU use only with active surface generation, supported scene mode and ready assets; static CURRENT_VISUAL_CAPABILITY remains **unavailable** |
| Runtime screens | CityWorld title now states DISTRICT PREVIEW; CityMap accessibility calls it a district-selection map; StoryPlayer accessibility says illustrated fallback, not native rigged 3D |
| Tests | tests/visual-presentation.test.ts covers absent device view, missing assets, unsupported mode, invalid generation and success only when a capability is reported; tests are *contracts*, not on-device GPU evidence |
| Underlying engine | render-contract.ts and render-adapter.ts from Step 3 still type/validate renderer snapshots but no native bridge is wired; actual world tile persistence not implemented |
| GPU prototype | independent Vulkan shader compute CI continues to verify city/2.5D character PPM captures; this is **not** shipping pixel gameplay nor genuine rigged 3D phone acting |
| Device status | iOS/Android Vulkan live swapchain not verified, walkable pixel overworld not built, rendered 3D mesh/café stage not built, signed downloaded asset distribution not deployed |

**Relevant CI evidence:** [City Vulkan compute smoke run 39218405157](https://github.com/swayam8624/LIVEIT/actions/runs/39218405157) completed successfully at the implementation-plan commit. Latest foundation, iOS and formatting checks must be read at their exact branch SHA; cancelled or action_required workflows are **not** passes. No assertion is made here that a physical iPhone or Android has rendered Vulkan game pixels.

**Next implementation gates in strict order:** (1) a valid persistent walkable tile map with collision/old-save migration, (2) original sprite/tile assets and real pixel navigation, (3) Android/iOS native Vulkan/MoltenVK live swapchains, (4) two licensed genuine 3D skinned actors and café stage, (5) the saved choice→widget/haptic→exact-coordinate-return end-to-end loop. The existing illustrated fallback stays functional until separately verified replacement.

## 2026-10-18 Vulkan/retro city implementation update


- `apps/player/src/gameTheme.ts` and the main player, city, story and avatar
  UIs now use an arcade-influenced, accessible color/type system rather than
  a primarily editorial serif look. Native device visual acceptance remains
  unverified.
- `CityMap` is an interactive illustrated isometric city fallback with real
  gameplay location actions, camera zoom, day/night preview, actual day,
  available event markers. It **is not a Vulkan surface**.
- `city-scene.ts` deterministically generates renderer-neutral 3D block
  geometry; Vitest includes city determinism, bounds and isometric projection
  regression tests.
- `native/city-vulkan` contains an original C++17 Vulkan compute renderer,
  SPIR-V city shader, CMake and CI. On 2026-10-18, **City Vulkan compute smoke**
  run [39101544442](https://github.com/swayam8624/LIVEIT/actions/runs/39101544442)
  succeeded and uploaded real 256×160 day/night PPM results. This uses Mesa
  Lavapipe software Vulkan in CI, NOT an iPhone GPU. It proves that executable
  Vulkan rendering code builds and dispatches; no mobile swapchain integration
  is claimed.
- Next required: actual native view, Android Vulkan SurfaceView and iOS
  CAMetalLayer/MoltenVK swapchain, in-app state binding, selection/raycast,
  animation/traffic/LOD and 10-minute mobile playtest. Details in
  [VULKAN_CITY_RENDERING.md](VULKAN_CITY_RENDERING.md).

## Required next exact actions

1. Validate local git status and stash only local modifications that could conflict with tracked formatting changes (notably apps/creator-studio/next-env.d.ts). git fetch and fast-forward the development branch. Keep user changes intact.
2. Resolve formatting through tracked source changes; npm ci, npm run check, dependency audit classification.
3. Stop only stale LIVEIT Metro processes, boot iPhone 17 Pro simulator, npm run ios (native app build). Capture actual screen with xcrun simctl io and exercise onboarding/age/choice/assets/restart.
4. Gather YouTube recording evidence with creator, URL and timestamps; do not turn official feature lists into claims of observed gameplay.
5. Build the first **top-down pixel town + real 3D dialogue** playable mobile slice with persistent navigation and fallback, then the birth-to-death lifespan, AI memory and lawful opt-in multiplayer. Follow the new M0–M7 implementation plan and AGENTS.md.

## Definition of done

No feature considered done unless a human can trigger it on an installed app, observe an actual consequence, restart and restore it, and see a successful edge-case test. A progress claim must state whether evidence is a real device, emulator/simulator, automated code test, official docs, or inference.
