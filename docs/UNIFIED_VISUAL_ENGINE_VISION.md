# LIVEIT — Unified Hybrid Visual Engine and Growing World

**Canonical product direction, 19 October 2026: RETRO TO LIVE IN, CINEMATIC TO FEEL, TACTILE TO CONTROL.** The actual first-generation handheld RPG inspiration applies to ordinary **top-down pixel-art movement**. Premium **real 3D** applies to important conversations, authored narratives, relationships and life moments. A tactile native HUD, sidebar, outcome widgets and an in-world communications device connect both. This supersedes earlier drafts that made all city exploration fully 3D/isometric or made all acting merely 2.5D cutouts.

**Read these three canonical specifications first, in order:**

1. [GDS-001 — Graphics Design Specification](LIVEIT_GRAPHICS_DESIGN_SPEC_V1.md): final visual style, accessibility and acceptance frames.
2. [GDS-002 — Screen & Mode Blueprint](LIVEIT_SCREEN_MODE_BLUEPRINT_V1.md), and [browsable atlas](design/LIVEIT_SCREEN_ATLAS.html): all 43 target screens, UI states, responsive views, interactions and journeys.
3. [ENG-003 — Hybrid Renderer Architecture](LIVEIT_RENDER_ENGINE_ARCHITECTURE_V1.md), and [render graph](design/LIVEIT_RENDER_GRAPH.mmd): the platform GPU, asset, movement and persistent state interfaces.

Historical [Vulkan city compute prototype](VULKAN_CITY_RENDERING.md) still matters as valid offscreen Vulkan technology; its city-only and renderer-model assumptions are retired for the actual game.

## Product: one life and one persistent identity, viewed through multiple art styles

The player lives a long, branching life: walk the town, enter homes, workplaces, schools, cafés, parks and shops; make day-to-day life choices, work and learn, grow older, own meaningful things and cultivate relationships. Important interactions open an actual smooth 3D cinematic with expressive actors, clothing and lighting matching the overworld. Story chapters use this same cinematic stage, or isolated timelines when selected. NPC identities/memories and the player persist across both visual styles, even after save/restart.

The HUD feels like a game—not a productivity app: compact top stats, collapsible navigation sidebar, accessible thumb controls, in-game phone with _distinctly labeled_ AI NPC and consented human contacts, meaningful haptics, timely progress feedback and truthful "what happened" widgets. A choice's new money/trust/status is never asserted before the deterministic domain engine and save coordinator commit it. Social contact is not fabricated: no sham online users or AI disguised as humans, and platform restrictions against primarily random anonymous chat must be respected. Real human communication requires moderation/consent/report/block, and can be separately disabled until compliant.

The renderer never mutates the simulation, advances calendar time per rendered frame, generates free money, chooses a story route or invents memories. The authoritative life/story domain stays in versioned TypeScript. A validated stable Character/Appearance ID can resolve to a 2D sprite and 3D rig using the same cosmetic selections and age.

## Hybrid art doctrine

**PIXEL WORLD:** Tile-based, top-down, independently walkable; initial logical 16px terrain tiles and 16×24 pixel adult actor visual footprints, four directions and 4 walking frames/direction. Original colorful Bellweather districts and interiors, smooth movement/camera with nearest-neighbor pixel-crisp sampling, pixel-aware day/night/rain/weather shader effects. The recognizable grid grammar is inspired by early Pokémon games, but never copies Nintendo visuals, sounds, names, maps, ROMs or interface artwork. A photographed/isometric district selection screen is **not** this gameplay.

**CINEMATIC 3D:** Genuine mesh/skinned character rigs, glTF/GLB scene assets, face blendshapes, twelve readable emotions, eye gaze, talking/blinking/breathing/gestures, relationship/camera reactions, authored interiors, real geometry depth and light/material/shadow/post. Painterly cinematic-comic visual direction, not uncanny photorealism. The current procedural 2.5D GPU face shader is **not** the target 3D actor system.

**TACTILE UI:** Retro-futurist mint/amber/coral on midnight HUD with original icons, responsive status bars, activity panels, accessible dialogue, choice cards, in-world phone, report/block where applicable, loss-sensitive feedback and readouts. Pixel display art may be shader-drawn; critical semantic text and controls remain native/React Native. World palette changes by district, era/weather/age; don't tint all rooms into the one HUD color.

**ONE IDENTITY:** Any change to hair, skin tone, outfit, accessories or age displays in every representation and does not alter gameplay advantages. Family, relationships and memories follow saved world state; cannot be invented by renderer or AI dialogue. Old saves receive safe deterministic defaults on migration and never get silently erased.

## Rendering architecture and native platforms

A single C++ Vulkan renderer has two separate GPU render pipelines under a common scene protocol and asset manager:

- pixel: atlas-driven tile/sprite instancing, occlusion, logical-resolution lighting/weather and nearest-neighbor presentation;
- cinema: skinned 3D meshes, expression morph targets, environment/shadows/material lighting, cinematic cameras and smooth 3D tonemapping;
- shared: frame/scene revision, identity resolver, input/picking commands, lifecycle/generation tokens, assets/cache/streaming, GPU present and effect transitions.

Native integration target: local Expo module; Kotlin Android SurfaceView/ANativeWindow + Vulkan surface/swapchain; Swift + Objective-C++ iOS CAMetalLayer + MoltenVK and portability support; verified on physical devices with resize/background/recovery. App's native accessible UI overlays gameplay. No WebGL/WebView/Expo Go/offscreen-PNG trick substitutes for a live native Vulkan scene.

Existing implementation includes TypeScript RenderFrame schemas and source-of-truth state adapters, versioned visual-pack schemas and stage verification, C++ headless Vulkan compute shaders and a React Native illustrated _fallback_. It **does not yet have** a playable free-roam tile engine, production sprite atlas, rigged 3D actor stage, device swapchain module or audited on-demand pack downloads.

## Growing, commercially usable asset universe

Original future production goals from the LIFEWEAVE brief: approximately 400 real swappable actor rig parts, 200 actual authored/reusable locations, 12 facial emotions, 30 cinema camera/FX presets, 20 named memory-aware NPCs and roughly 300 lightweight population characters per town. These are ambitious targets, not the current completed library. The currently committed 51 shader-backed entries are procedural metadata recipes; they are **not** 51 distinct approved costumes, sprites or meshes.

Every visual item carries source/author/license, editor review, version, dependencies, slot mapping, texture/geometry compatibility and SHA-256. Pixel data, mesh/texture/animation and script/scene content are packaged as versioned, data-only assets. New shader executable code ships through app updates, never hidden downloaded SPIR-V. Pack publication needs a signed index, validated hashes, staged verification and atomic activation/rollback, on-device offline cache, storage UI and memory budgets. Source and gameplay creator projects must be validated, rights-cleared and testable on actual screens.

## Milestone definition: ship a whole loop before claiming a game

The first release acceptance loop is a player walking Bellweather, bumping a collider, entering a café, meeting Amelia in pixel form, transitioning into genuinely animated 3D with matching hair/wardrobe/age, making a meaningful choice, receiving a confirmed factual outcome and haptic, returning to the same town tile, restarting and recovering all saved world changes. Repeat on actual iOS and Android, with real GPU captures, accessibility and battery/thermal testing. Current story and district fallback remain working until replaced.

- R0: validated persistent tile position, collision, old-save migration.
- R1: genuine original pixel atlas, free-walk and Vulkan tile/sprite pass.
- R2: mobile Vulkan/MoltenVK swapchain and Expo native view.
- R3: interact/talk handoff and return position.
- R4: real two-person rigged 3D story stage and expressions.
- R5: cross-mode appearance, outfit and age resolution.
- R6: haptic/outcome widgets tied to real world/save commits.
- R7: interiors, town expansion, NPC routines and weather.
- R8: lawful pack pipeline and secure on-device downloaded expansion.
- R9: large original content, AI NPC and lawful human social services, QA/release.

This is a program, not an assertion that R0–R9 have shipped. For exact dependencies, testable output, lifecycle and failure contracts follow ENG-003.

## Historical context: superseded choices

- The early warm editorial/2.5D concept remains only as a prototype styling history.
- The intermediate 3D/isometric city and raycast AABB demo are retained for useful Vulkan proof, but no longer determine Free Life presentation. Future exploration is **top-down pixel**.
- The procedural 2.5D actor demo remains valid GPU test, but actual authored story acting is **true 3D**.
- React Native, authored stories, saved domain schemas and financial/NPC rules stay until superseded by proven compatible functioning replacements; no Unity rewrite by default.

Related documents: [ART_DIRECTION](ART_DIRECTION.md), [NATIVE_RECONSTRUCTION](NATIVE_RECONSTRUCTION.md), [BUILD_STATUS](BUILD_STATUS.md), [LIVEIT_2_GAMEFEEL_CONTENT_MASTERPLAN](LIVEIT_2_GAMEFEEL_CONTENT_MASTERPLAN.md). A contradictory note in a historical file never overrides GDS-001/002 or ENG-003.
