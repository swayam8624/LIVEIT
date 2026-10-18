# LIVEIT unified Vulkan visual engine — the actual LIFEWEAVE vision

The user's original LIFEWEAVE Master Build Spec requires more than a Vulkan city. The vision is a persistent birth-to-death world with Episode-quality acting, BitLife-like choices, AI characters who remember, optional consent-based real-player social interactions, and an ever-expanding visual content library. The recent request explicitly broadens Vulkan to **all characters, costumes, props, interiors, scene art, lighting, transitions and interactive world graphics**. Do not treat a city-map renderer as the product.

Read the user-provided LIFEWEAVE spec sections 1–3, 4, 5.11, 6, 8, 12–13 before making any visual architecture decisions. The original spec proposed Unity 6 URP by default, but the current existing LIVEIT application is Expo/React Native with a TypeScript domain engine. A true Vulkan core shared across mobile platforms is the updated rendering target. Preserve validated saves and engine rules while phasing in the native engine; avoid imposing a second contradictory simulation.

## One living world and one identity everywhere

A single persistent player/NPC identity must render consistently in: isometric 3D cities, interiors and homes, schools and jobs, cinematic story chapters, creator character editor, AI chat portraits, relationship constellation, memory flashbacks, aged life recaps, heirloom displays and social cameos. Scene/actor data derives from saved simulation identity, appearance, age, emotion, relationships and the event log; the rendering engine NEVER fabricates a separate NPC or mutates simulation state.

Native text entry, screen-reader annotations and accessibility controls can stay platform-native on top. Shader-rasterizing ALL text is not acceptable if it makes the game inaccessible. Vulkan should drive the actual animated characters, environments, props, particles, lighting, materials, cinematic transitions and diegetic game HUD graphics, rather than RN rectangles posing as final artwork.

## Look: painterly cinematic comic + restrained retro game character

Original style bible: saturated location-dependent colors; confident ink silhouettes, deliberate material palettes, expressive eyes/faces/acting, parallax painted scene layers, strong rim light, dusk/rain mood grades. The recent midnight/mint/amber theme is a native HUD style, NOT an instruction to make every room, body and environment dark teal. Life-stage grades: childhood warm pastel, teen neon, young adult saturated, midlife warmer realism, elder golden sepia and restrained film grain. Retro styling belongs in punchy menus, readable arcade glyphs, signage, item cards, status orbs and animated transitions. Preserve modern text legibility.

## Single render graph

Deterministic saved world -> WorldVisualScene -> validated visual asset packs -> render graph -> Vulkan/SPIR-V -> Android Vulkan native surface OR MoltenVK/Metal iOS surface -> native accessible UI.

Render-graph passes: GPU culling and instancing; world terrain/roads/building mesh material; environment props/vegetation/interiors; character 2.5D rig and clothing layer atlas; character animation/face and age overlays; cinematic depth layers, lights and shadow; weather/particles; ink outline, color grading, grain, lighting and dissolve passes; GPU selection/object ID output for hit testing; transparent UI FX passes. The mobile native view must own swapchain, device/layer lifecycle, frame pacing, resizing and error fallback. No GL/WebGL substitution masquerading as Vulkan. On iOS Vulkan uses MoltenVK correctly linked to CAMetalLayer; physical iPhone verification is required.

The existing headless Vulkan prototype is only the first two passes of this journey. Current shader-generated actors are procedural painter-like placeholders (not yet a full rigged artwork atlas). Current player still uses an illustrated RN fallback until native surface integration. Make this limitation visible in build reports.

## Character/rig system and targets FROM THE ORIGINAL SPEC

Canonical attachment/depth slots: back hair, body, head, eyes/iris/lids, brows, mouth, neck, limbs, front hair, outfits, accessories, makeup, scars/tattoos, body/age layers, headwear and lighting masks. Keep rig skeleton/anchors, animations and cosmetic parts in data/atlas resources. A character needs stable skin/body/face/eyes/hair/wardrobe variations, including aging and legacy generations. Use shader parameters, palette/texture variants and layered rigging to avoid duplicating all combinations.

Twelve expressions: neutral, happy, sad, angry, flirty, shocked, scared, smug, crying, embarrassed, tired and thoughtful; idle breathing, blinking, eye tracking and dialogue-triggered mouth animation; gesture, movement, entrances/exits and scene camera staging. The original source target is approximately 400 genuine rig parts at launch. This is NOT the current built count. Named NPCs and lite statistical NPCs should render through the same system as each one is promoted to a chattable identity. About 20 memory-aware named NPCs and 300 lightweight population NPCs is the source's world scale target, not a rendered crowd currently achieved.

## Scenes, cameras, FX and asset volume

About 200 reusable authored location templates, home/school/work/street/clinic/airport/hospital/garden/court/bar/prison etc, each with 3–5 depth layers; 30 cinema camera/FX presets; time-of-day, weather, world-era and life-stage shaders; rain, embers, fog, paper overlays, holographic shines, memory fade/dissolves and route milestones. Every scene must drive a real choice, NPC interaction or meaningful activity, not be a decorative background.

The visual pipeline must support large **growing** asset libraries without app-code changes: versioned manifest + full source/author/license record + SHA-256 for external bytes + dependencies + rig slots + variant and quality-tier metadata; source files converted to GPU-ready atlases, KTX2/ASTC textures and geometry/LOD; staged download, hash verification, validation, atomic activation and rollback; offline cache; local storage/budget UI; no executable shaders or arbitrary code downloaded from untrusted packs. The original spec targets an under-150MB core app, supplemental country/story/cosmetic/era packs, 2048 texture atlases, <600MB memory on medium hardware, and low/medium/high quality tiers. Treat budgets as acceptance targets, not measured results.

One editorial review step ensures all new generated/source art is consistent at phone size, licensed for commercial use, and linked to playable content. Do not confuse metadata recipes with new finished illustrated parts.

## Existing source, exact truth

- packages/world-schema/src/visual-assets.ts: strict VisualAsset/VisualPack/VisualScene schemas, graph/path validation.
- packages/simulation-core/src/visual-scene.ts: uses saved player appearance/identity to produce render-scene data for city, story and chat.
- content/visual-packs/core/manifest.json: 51 shader-backed procedural **recipes**, including facial expressions, palette choices and scene resources; they are neither 51 bespoke rendered illustrations nor production character atlas parts.
- native/city-vulkan/shaders/city.comp: headless GPU raycast scene prototype.
- native/city-vulkan/shaders/actors.comp: actual GPU compositing of character expressions/skin/hair/clothing plus story backdrop, in portrait/conversation/cast modes.
- native/city-vulkan/src/main.cpp: Vulkan device/compute dispatch and PPM output for test visualization.
- apps/player/src/AvatarPortrait.tsx: current old RN illustrated fallback; must be replaced when Vulkan module is ready.

## Required execution gates

1. CI proves compiled SPIR-V draws distinct day/night city, character portrait, alternate expression, two-character dialogue and multiple cast images. Compare image bytes and attach artifact evidence.
2. Core asset pack parses and rejects duplicate IDs, cycles, nonexistent references, unsafe paths, corruption; scene adapter preserves player identity/appearance consistently after save/restart.
3. Native Vulkan surfaces on Android and MoltenVK iPhone display characters AND city inside the shipped app with real picking/animation, working across pause/resume/reload and offline mode.
4. Import real licensed texture atlas rig-part packs, not just shader palette swatches. Swap clothing/hairstyles/accessories at runtime and confirm world/story/chat visual parity.
5. Implement the scalable content delivery/cache with verified and versioned signed downloaded packs; author/edit over 200 places and 400 actual parts progressively, exposing installed storage and quality controls.
6. Test 60fps mid/high and 30fps low cinematic, reduced-motion, touch/readability, memory/thermal/power, deterministic world and screenshot/visual regressions.

Agents: do not claim the all-graphics Vulkan engine is complete until 3–6 are verified. Prioritize shipping real working native end-to-end slices over another series of aspirational docs.
