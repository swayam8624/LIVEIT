# LIVEIT Documentation Authority & Build Roadmap

**Current as of 2026-10-19.** This index resolves formerly conflicting graphics proposals. LIVEIT is a native mobile life-simulation and interactive-fiction game: **top-down pixel overworld** for ordinary roaming, **true smooth skinned 3D** for important conversations/stories, **tactile accessible game HUD** across both. Vulkan on Android and Vulkan→MoltenVK on iOS are the intended shared GPU platforms.

## Read / implement in this order

| Priority | File                                                               | Owns                                                                                                                          | Status                                             |
| -------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| 1        | [GDS-001](LIVEIT_GRAPHICS_DESIGN_SPEC_V1.md)                       | The visual identity, color, pixel sampling, 3D conversation animation, haptics, identity, accessibility and visual QA targets | Final design specification, not code proof         |
| 2        | [GDS-002](LIVEIT_SCREEN_MODE_BLUEPRINT_V1.md)                      | 43 screen/mode designs, screen states, navigation, layouts, HUD, social distinctions                                          | Final design specification, not code proof         |
| 2a       | [Screen Atlas](design/LIVEIT_SCREEN_ATLAS.html)                    | 27 clickable schematic screen compositions                                                                                    | Original design mock, not game                     |
| 3        | [ENG-003](LIVEIT_RENDER_ENGINE_ARCHITECTURE_V1.md)                 | Vulkan pixel and genuine 3D GPU passes, identity/scene ABI, mobile module, asset graph, native lifecycles, test gates         | Technical architecture + preliminary TS contract   |
| 3a       | [Render Graph](design/LIVEIT_RENDER_GRAPH.mmd)                     | Engine/ownership diagram and module boundaries                                                                                | Architecture diagram                               |
| 4        | [Hybrid Implementation Plan](HYBRID_RENDER_IMPLEMENTATION_PLAN.md) | M0–M7 build order, target files, domain migration, on-device acceptance                                                       | Implementation schedule and checklist, not shipped |
| Primary  | [Unified Product Vision](UNIFIED_VISUAL_ENGINE_VISION.md)          | The whole game across Free Life, Story, NPCs, AI/social and art identity                                                      | Updated hybrid product direction                   |
| Primary  | [Art Direction](ART_DIRECTION.md)                                  | Pixel assets and smooth 3D character style; production assets, colors, font, provenance                                       | Updated hybrid art rules                           |
| Progress | [BUILD STATUS](BUILD_STATUS.md)                                    | What has _actually_ compiled, rendered, installed or been tested                                                              | Must be evidence-backed per exact commit           |
| Agent    | [AGENTS.md](../AGENTS.md)                                          | Binding coding/research/gating duties                                                                                         | Must follow this authority order                   |

Other documents remain useful as historical or domain-specific references, subject to the precedence above:

- [Historical Vulkan City Proof](VULKAN_CITY_RENDERING.md): valid offscreen Vulkan C++ compute shader tests but retired as the Free Life renderer.
- [Native Reconstruction](NATIVE_RECONSTRUCTION.md): original life/AI/social/backend and device criteria; graphics paragraph aligned to hybrid direction.
- [LIVEIT 2.0 Game Feel Masterplan](LIVEIT_2_GAMEFEEL_CONTENT_MASTERPLAN.md): original progression/content/interaction strategy; its earlier 2.5D/Skia options are superseded.
- [REA reconstruction runbook](REA_RECONSTRUCTION_RUNBOOK.md): legally authorized tool research and evidence gathering, not entitlement to proprietary artwork.
- [Reference research](research/REA_TARGETS.md), [feature ledger](research/REA_FEATURES.md), [parity evidence](research/REA_PARITY.md), [video observation ledger](research/VIDEO_LEDGER.md): use sources and evidence instead of invented timings.

## Precedence rule and safe future revisions

For graphics: **GDS-001 wins over all older prose**. For screen/navigation: **GDS-002**. For native pipeline ABI, state/asset/ownership: **ENG-003**. For current truth: **the verified runtime and BUILD_STATUS**, never the wish list. The complete user LIFEWEAVE source remains the baseline for game-system breadth; visual revisions made 2026-10-19 override its old Unity/all-2.5D rendering proposals without deleting the long-term life-simulation goal.

Do not treat the words "Vulkan city", "isometric" or "2.5D" in prototype source and old evidence files as the shipping Free Roam art choice. The existing React Native district selection and illustrated story flows remain fallback screens until production equivalents pass genuine iOS/Android checks. A generated UI atlas, offscreen shader PPM or passing npm test is not visual proof of the running native phone app.

If a new user art direction overrides this, update all three GDS-001/GDS-002/ENG-003 source-of-truth specs, product vision, art direction, AGENTS and BUILD_STATUS together, with explicit migration and tests.

## Truthful first playable hybrid milestone

1. The player walks a new original Bellweather 16px tile world with real collision/doors and a persisted position.
2. Amelia exists as the same persistent NPC in pixel and 3D.
3. A conversation transitions into two genuinely skinned 3D characters in an original scene on iOS/Android GPU.
4. User chooses a real authored branch, receives a saved factual outcome and one appropriate haptic.
5. User returns to the same valid map location, kills/reopens the app and sees identical age, outfit, money, trust and journal.
6. The app handles offline, missing art, hardware graphics loss and accessibility without deleting game state.

This defines future completion, not current progress.
