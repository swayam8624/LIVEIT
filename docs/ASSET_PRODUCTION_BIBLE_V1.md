# LIVEIT — Asset Production Bible and Expandable Library (ART-005)

> **ARCHIVED 3D/HYBRID PLANNING DOCUMENT:** The owner changed LIVEIT to **100% expressive 2D retro pixel art** on 2026-10-19. Its former 3D cinematic/model requirements below are superseded by [PIXEL_ONLY_DIRECTION_V2](PIXEL_ONLY_DIRECTION_V2.md) and [active pixel-v2 requirements](../content/production-assets/pixel-v2/required-assets.json). Do not implement 3D from this document.

**Step 5 of the approved 5-step LIVEIT visual program. Status: production specification and inventory metadata, NOT 1,481 finished artwork files. Version: 1.0, 19 October 2026.**

**Binding upstream:** [GDS-001](LIVEIT_GRAPHICS_DESIGN_SPEC_V1.md) → [GDS-002](LIVEIT_SCREEN_MODE_BLUEPRINT_V1.md) → [ENG-003](LIVEIT_RENDER_ENGINE_ARCHITECTURE_V1.md) → [hybrid implementation plan](HYBRID_RENDER_IMPLEMENTATION_PLAN.md). The user's final design is **original top-down handheld-RPG-inspired pixel gameplay**, **genuinely rigged 3D emotional/cinematic scenes**, and **tactile game HUD/social widgets** sharing the same saved ages, faces, clothes, relationships and world facts. Android Vulkan and iOS MoltenVK are the target native GPU APIs. Do not copy Pokémon character sheets, ROMs, font artwork, proprietary music, Episode costumes, branded UI/trade dress or other protected game art.

## 1. Truth and scope

The independent production catalog lives under [content/production-assets/v1](../content/production-assets/v1). It contains **1,481 planned work items**. A work item represents a distinct authored deliverable or explicitly identified technical behavior/record; it is not guaranteed to correspond 1:1 to one output file and is not evidence that the artwork exists. It covers **400** proposed interchangeable mesh/material _parts_ (not 400 complete NPC models), **200** distinct 3D stage location templates, 55 pixel character sprite families, 302 individual top-down tile designs and all primary HUD, music, SFX, GPU shader and animation libraries.

**Existing binaries in GitHub at inspection:** 28 pinned Kenney CC0 PNGs in the historic isometric district-map/UI fallback, with source blob SHA-1/provenance in assets/kenney_city_provenance.json and assets/kenney_ui_provenance.json; two miniature concept JPEG previews (Amelia portrait and dusk café), subject to separate rights/final-art review. Existing content/visual-packs/core/manifest.json contains 51 procedural shader-backed **metadata recipes**, not 51 independently finished character parts. The present pixel tile atlas, true glTF rigged 3D actor set and cinematic 3D location set each have **zero verified production items**. See [exact machine-readable baseline audit](../content/production-assets/v1/existing-repo-audit.json). Git blob SHA-1 from the existing provenance is not a SHA-256 of a runtime binary and must never be mislabeled as one.

No downloaded textures, meshes, sounds, font files or third-party materials have been newly installed by Step 5. The objective is to make subsequent asset work **verifiable, legally safe and extensible**, not to call generated lists a finished game.

## 2. Canonical machine-readable files and counts

The [self-contained searchable Asset Atlas](../content/production-assets/ASSET_ATLAS.html) lets artists and engineers filter every planned item by category/priority or only the 110 first-playable IDs. It is deliberately metadata-only and can be opened locally without a server.

| Catalog                | Item classes                                                      |                Count | Where                                           |
| ---------------------- | ----------------------------------------------------------------- | -------------------: | ----------------------------------------------- |
| 3D people              | interchangeable custom rig parts                                  |              **400** | content/production-assets/v1/characters-3d.json |
| 3D people              | age-stage base rigs, emotions, action clips                       | 5 + 12 + 40 = **57** | same                                            |
| 3D environments        | named, artist-distinct cinematic locations                        |              **200** | locations-3d.json                               |
| 3D environment props   | furniture/electronics/street/domestic/school/clinic/nature        |               **90** | locations-3d.json                               |
| Pixel environment      | original individual 16px top-down tile designs                    |              **302** | pixel-world.json                                |
| Pixel maps             | 8 authored map archetypes per district × 5 districts              |               **40** | pixel-world.json                                |
| Pixel actors           | player age stages (5), named cast (20), lightweight crowd (30)    |      **55 families** | pixel-world.json                                |
| Pixel visual weather   | dedicated pixel-grid-aware effects                                |               **16** | pixel-world.json                                |
| HUD                    | screen panels, choice states, nav/status widgets and visual icons |              **105** | hud-audio-fx.json                               |
| Audio                  | gameplay/UI/ambience sound cues                                   |               **73** | hud-audio-fx.json                               |
| Music                  | 27 thematic compositions/stems                                    |               **27** | hud-audio-fx.json                               |
| Shaders                | app-bundled Vulkan/SPIR-V material/pixel/render families          |               **30** | hud-audio-fx.json                               |
| Screen/scene visual FX | original in-world, 3D and HUD effect presets                      |               **40** | hud-audio-fx.json                               |
| Camera direction       | separately staged camera/storyboard shot presets                  |               **30** | hud-audio-fx.json                               |
| Haptics                | semantic device patterns, settings-gated                          |               **12** | hud-audio-fx.json                               |
| Typography             | commercial redistribution-approved font roles                     |                **4** | hud-audio-fx.json                               |
| **Planned total**      |                                                                   |            **1,481** | catalog-index.json                              |

All 1,481 planned work items are initialized **status="planned"** with no claimed binary, source license approval, artist or rights proof. These are substantially more granular than the original headline aspirations; a model/mesh may require multiple files and a shader may require multiple SPIR-V platform variants.

Priority labels: **P0 = 723 records** (front-loaded foundational needs and early expansion), **P1 = 501**, **P2 = 257**. This is a prioritized backlog, **not** a requirement to create 723 items before the first playable build. The first playable _vertical slice_ is a much smaller artist-approved subset, described below.

## 3. Pixel overworld: exact atlas and tile production

**Visual rule:** authoritative top-down 2D, tile grid with 16×16 logical source pixels; main actor small-scale 16×24 logical-pixel footprint, contact at the feet. At minimum four cardinal orientations (north/east/south/west), four walking frames per direction, plus idle/interact where the cast supports it. All map art is original and rendered in a 1:1 pixel-aligned logical target then nearest-neighbor scaled when feasible. Avoid bilinear filtering, blurry downsampling, generic HD illustrations reduced to pixel size, and photographed proprietary tiles.

**Tile source library:**

- 77 shared outdoor foundations: paths, grass, walls, roof, water, crossing, street signage, traffic and navigation debugging.
- 45 original indoor source tiles: flooring, wall and window/door trim, roof occluders, table/bed/kitchen/clinic/classroom furniture at world scale.
- 36 individually named specialized top-down tiles for each district (Riverside, University, Market, Studio, Gardens): 180 themed tiles total. These are physically authored distinctions such as dock planks, ferry ropes, science laboratory/dorm motifs, produce stalls and public transit, film set/lighting pieces, gardens/pond/veterinary details.
- 16 pixel-grid-aware overlays: rain, snow, glow, fog, stars, reflections, leaf wind and other visual conditions. Effects run in a separate logical render pass and do not soften sprite edges.

**Map set:** 40 authored navigation maps = five districts × eight types (central street, residential lane, public square, primary interior, café, workplace, school and park). A map requires solid/walkable tile layers, occlusion/roof definitions, portals/return coordinates, player/NPC spawns, route graph, dynamic collision and daytime/nighttime palette refs. A map is NOT a pretty background JPG; the player must walk, approach, encounter blocks, enter doors and return to the original tile.

**Pixel actors:** 55 sprite families: the player's child/teen/young adult/midlife/elder stages, 20 distinctive named NPC roles, and 30 lightweight crowd archetypes. Main player/named cast: nominal minimum 4 orientations × (4 walking + 1 idle + 1 interact) = **24 frames per family**. Crowd archetypes: reduced 4 orientations × (2 walking + 1 idle) = **12 frames per family** (individual importer must enforce animation tags and timing). Therefore catalog implies up to **5×24 + 20×24 + 30×12 = 960 explicitly required base pose frames**, BEFORE outfit/hair/body combinations. Do **not** author an impossible sprite sheet for every combinatorial outfit; composite modular pixel layers from stable semantic appearance slots and cache assembled variants at runtime.

Each sprite exports a layer order, feet pivot, body collision box, palette index and string family ID. Separate movement delta/world position from frame animation time. Pixel and 3D identities must resolve to the same canonical hair/outfit/skin IDs and age from saved world; the asset registry must make unsupported permutations explicit, not silently randomize.

**First tiny Bellweather prototype palette (art-target, not assets):** original park moss, brick/pink market signage, river blue, street slate, cream facades, night amber windows, accent mint selection. The dark HUD tokens must not apply as a blanket terrain shader.

## 4. Rigged 3D character customization: a real 400-part production queue

The exact 400 distinct parts are individually named in characters-3d.json. Each must be an **artist-authored geometry/topology or independently authored decal/skin overlay part** with actual source and shippable runtime data. A mere palette recolor does **not** satisfy an additional numbered part. Separately list material palette variations later with shared geometry IDs.

| Rig part family                     | Distinct artistic targets |
| ----------------------------------- | ------------------------: |
| Face mesh forms                     |                        24 |
| Eye shape components                |                        24 |
| Eyebrow forms                       |                        20 |
| Nose meshes/morphs                  |                        18 |
| Mouth/lip meshes/morphs             |                        18 |
| Ear shapes                          |                        12 |
| Hairstyle geometry                  |                        60 |
| Facial hair parts                   |                        20 |
| Tops/tunic/shirts                   |                        48 |
| Bottoms/trousers/skirts             |                        32 |
| Jackets/coats/outerwear             |                        24 |
| Shoes                               |                        22 |
| Accessories                         |                        36 |
| Headwear                            |                        16 |
| Body proportion mesh adaptors       |                        16 |
| Real skin/scar/freckle/age overlays |                        10 |
| **Total unique parts**              |                   **400** |

Additionally plan **five age-stage foundational rig states** (child, teen, young adult, midlife, elder; compatible reusable skeleton family where technically possible), **12 named facial expressions** and **40 animation clips** (idle breathe/blink/look, listening, speech, turn, walk-in/out, sit/stand, emotion response, hand gestures, etc). None of those is counted toward the 400 interchangeable parts.

**Minimum skeleton:** pelvis, spine chain, shoulders/arms/hands, legs/feet, neck/head, eye joints or gaze constraints, facial morph groups, jaw and hands; common attachment slots with stable world-space transforms. Animation export must preserve bone names; group compatibility and retargeting tested. Body size/age adjustments should not automatically break hair clipping, outfit topology or collision. Avoid stereotypes and mechanical bonuses based on complexion/body features.

**12 expression QA:** neutral, happy, sad, angry, flirty, shocked, scared, smug, crying, embarrassed, tired, thoughtful. Each must be distinguishable without text labels at small phone cinematic size, preserve identity, transition with blending rather than popping, animate both eyes/eyebrows/mouth and be measured under warm/cool lighting. "Flirty" is adult-only and must not map onto children; controls and story metadata enforce age/context boundaries. Simulated text mouth movement not evidence of actual voice acting.

**Motion:** subtle, not uncanny; separate emotional change from life-state mutation. Eye gaze must match speaker, lip movement loosely correspond to timed dialogue, hair/cloth can have lightweight procedural response without mandatory physics every frame. Default 30/60fps tiers, quality depending on device, reduced-motion option.

**2D⇄3D identity parity:** Each authored appearance element must map (family variant, palette and applicable rig slots) to both pixel sprite composite and 3D mesh/material blend. Test at least 12 unique cross-skin/hair/outfit combinations × five age states, before/after saving and reloading. Never use a temporary static portrait in chat as proof that the new actor model is ready.

## 5. Cinematic environments and props: 200 actual distinct scenes

**Five districts × 40 authored 3D locations each:** Riverside, University, Market, Studio, Gardens. Catalog IDs name every one (for example riverside river-cafe and ferry terminal, campus physics-lab and dorm, market corner apartment and bank, studio editing suite and wardrobe room, gardens hospital room and wedding pavilion).

**Art direction:** locations may share a modular prop/material kit, but the 200 records require **200 distinct spatial compositions** with layout/staging, camera occupancy/safe zones, lighting and approved world connection. Renaming the same café 40 times, swapping only a palette, or saving 200 JSON descriptions of one photograph does NOT pass. Distinct does not require 200 entirely bespoke mesh libraries; modular reuse is a cost/size necessity, but the authored room layouts must differ materially.

Every set delivers: scene ID and district, source authored file (Blender), light/camera block, 3D models and baked textures, optional painterly flat/parallax background depth, 2–3 actor spawn/eyeline markers, hero closeup safe rectangle, correct day/night or time/weather variants, occlusion and picking bounds, valid portal mapping to a pixel world location, fallback camera and tiered mesh/material LOD. Import and runtime scene layer cannot change world day or NPC identity.

**90 cinematic prop work items** enumerate furniture, phones/screens, streets/transport, household pieces, lab/classroom, clinics/hospitals and landscape/vegetation. All have actual world-space dimensions, origin/pivot/attach targets, LOD/material bands, collision/picking metadata and license. Props must support 3D closeup framing and must not be random oversized primitives.

**30 authorable camera presets** are separately defined in hud-audio-fx.json: establishing, two-shots, OTS, single/dual closeups, reaction shots, object inserts, tracking walk-ins, sitting conversations, three-person blocking, hospital, job interview, school, memory, aging and finale. Validate lens-like field-of-view, faces not obscured by native dialogue dock and orientation-safe framing. A camera preset is not counted as another location.

## 6. Tactile game HUD, sidebars, anonymous/AI chat distinctions

**105 HUD/component records** include branding, top meters, currencies, profile frames, age wheel, wardrobe selectors, relationship/family graphs, event/choice state panels (idle/focused/armed/pending/committed/failed), "what changed" widgets with authoritative deltas, minimap and NPC markers, in-world phone drawer, inbox badges, AI-vs-real contact tags, report/block, download/verification, recovery, settings and accessible focus states.

Design per GDS-002 at 320pt/390pt phones and tablets. Build reusable nine-slice skins/semantic icon system; no giant bitmap overlays hiding gameplay or UI that looks like a banking application. Use haptic selection on discrete changes; only confirm meaningful choices after persisted authoritative outcome; no per-tile walk vibrations. The catalog defines **12 semantic haptic events**, not "12 separate generated WAV files". No vibration hardware? Native still provides visible/audio feedback when enabled.

**Communications:** NPC roleplay is labeled as AI when model-backed, while human social presence must be real, opt-in, bounded by age/consent/moderation and platform policy, and report/block visible. The UI art inventory must support these distinctions. A human-chat sprite or generic "online" badge does not implement a real secure backend. Do not use "anonymous" visual design to imply untraceable or guaranteed access to random strangers.

**Four font roles** (display, body, mono-HUD, pixel diegetic) remain **planned until exact font licenses, files, authors and redistribution terms are recorded**. Use licensed fonts only, never screenshot/embed unlicensed proprietary system fonts as distributable assets. Gameplay body/dialogue/legal/moderation text must be scalable native text.

## 7. Audio, music, VFX and GPU shader sources

**73 sound cues** cover UI haptics companions, choice/outcome, messages, age-up, steps on surfaces, doors, café, river, transit, gardens, weather, story mood and respectful grief. Separate mono/ambisonic/stereo options for devices; optimized compressed mobile playback plus source WAV, mastered levels and loop boundary tests. Haptics are separately data-defined, not raw sound.

**27 music tracks/stems** for title, five districts day/night, café, relationships, career/school, narrative tension/release, memories, legacy and credits. Music progression must derive from verified actual state, e.g., do not play triumphant reward stinger when a loved one dies. Scene author owns transitions and allowed loops.

**40 VFX records** for shader-based pixel weather and interaction, cinema face/hair/lighting mood transitions, camera moves/ink dissolves and meaningful HUD visuals. **30 shader families** include tile/sprite instancing, pixel ID picking/nearest presentation, pixel-light/weather, true 3D GPU skinning/morph, toon-lit PBR, hair/eye materials, shadows, post-process and common tonemap/transitions. Shader binaries are **app-bundled source→SPIR-V builds** with compilable artifact hashes and Vulkan validation. A downloaded pack can describe a preset/material instance, NEVER execute new untrusted SPIR-V/Metal/native code.

## 8. Actual first playable asset kit (small enough to finish)

The first **playable production vertical slice** should consist of:

- an original 40–60 authored top-down tile subset (road, building, grass, doors, café and interior furniture) selected from pixel-world.json, plus **one** bounded Bellweather Market map with collisions and a usable café doorway;
- one player base sprite family and one named NPC (Amelia) with four directions, four walks and idle/interaction; enough outfit/hair choices to visibly match the cinematic look;
- two legitimate source-approved 3D human meshes (player + Amelia), one real café scene/room with actor markers, current outfits and hair, at least neutral/happy/sad/angry/tired expressions initially, with all 12 expression IDs specified and completed before claiming the full expression milestone;
- original interior props: two chairs, café table, lamp, counter, cup, window and door; one 2-shot and one close-up/OTS camera; idle/blink/listen/talk/gesture animation to establish genuine 3D acting;
- minimal HUD: status strip, player/age card, talk/enter, choice dock, save pending/committed/error, "what changed" event widget, phone badge, accessibility labels and optional haptics;
- 8–12 short original SFX plus two music/ambience themes; an approved legal license record;
- true native Vulkan pixel viewport on Android and Vulkan→MoltenVK cinema on iPhone, player collision → conversation → committed trust delta → same return tile → kill/relaunch world parity.

A polished small slice beats hundreds of thumbnails or generated data recipes that cannot be played.

**Mini-slice item IDs should be resolved from the catalog by their real names**, e.g. pixel tile road-asphalt/shared and market cafe, cinematic location market coffeehouse, pixel sprite named amelia, character rig hair and outfit part, camera two-shot and single close-up. Catalog priority P0 means backlog priority, NOT that each P0 item must ship in the first milestone. Keep a release manifest of the actual selected IDs once files exist.

**Exact first playable selection:** The [110-item machine-readable first kit](../content/production-assets/v1/first-playable-slice.json) lists the stable IDs that artists and engineers can start on for Bellweather's pixel street→café→3D Amelia talk. The kit contains 28 tiles, 2 collision/portal maps, 2 pixel actor families, 1 real 3D room, 1 base rig, 11 unique rig parts, 4 actual props, 4 cameras, 5 face expressions, 5 motion clips, 12 shader families, 22 HUD units, 8 SFX, 2 music tracks and 3 haptic patterns. This is a list of **unbuilt targets**, not 110 shipped assets. These five first-slice face expressions are an initial acting milestone; all 12 remain in the full production target.

## 9. Asset production pipeline: from idea to verified device

Production lifecycle is audited for EACH catalog item:

    planned
      ↓ scope and identify canonical appearance/world/scene dependency
    sourced / rights-cleared
      ↓ acquire original artist-created source OR candidate third-party exact file
      ↓ record creator / copyright / specific license / terms snapshot / territory
    in-production
      ↓ paint/model/animate/rig in editable source
      ↓ human art-direction and inclusivity review
      ↓ 2D tile atlas (nearest) / 3D GLB/texture KTX2/Basis/LOD transform
    qa-passed
      ↓ validated digest and linked QA evidence
      ↓ pixel at 1×/3×, 3D pose/expression, rig slots, light and collision tests
      ↓ embedded native renderer smoke and reversible save/cache test
    released
      ↓ signed manifest/version, private app-storage install, staged activation
      ↓ on-device screenshot/perf/thermal and quality-tier evidence
      ↓ license credits and effective offline rollback
    deprecation (separate recorded migration, not invisible deletion)

**Source:** Blender .blend / layered Aseprite or lossless PNG / properly authored vector/icon sources / source WAV/DAW/notation / shader GLSL and offline material presets. Do not delete source assets after generating GPU-ready runtime representations.

**Runtime:** top-down pixel PNG/RGBA atlas and collision JSON with nearest sampling, 3D GLB/glTF and KTX2 compressed textures, GPU-appropriate mip maps and device-format transcode, scene placement/camera JSON, precompiled SPIR-V from app builds, audio compressed files, selected font files with licenses. KTX2+Basis Universal is a Khronos-standard distribution format with mobile transcode support; validate support per hardware (see official Khronos links below).

**Mandatory metadata on sourced/QA/released items:** stable ID, source path, output path, creator/owner and dates, source URL or commission agreement, exact asset license and approved commercial/redistribution rights, origin rights evidence snapshot, source revision, semantic slots, derived-asset references, digest SHA-256 of FINAL runtime bytes, toolchain versions, renderer/schema minVersion, QA captures and device profile, pack ID and declared dependencies. If not all these are ready, keep status planned/in-production and mark blockage explicitly. CI refuses a falsely released item.

**Runtime pack install algorithm:** only accept authorized data; validate signed index, byte limits, SHA-256, JSON schemas and dependency graph, normalize allowed relative paths, stage into private versioned directory, verify referenced assets, atomically activate last-good pointer, rollback on corrupt/partial install, manage retention/offline cache and display exact installed bytes. Installed source/asset files must not be sourced from publicly writable or arbitrary URL origins. Current prepareVisualPackActivation supplies only preliminary validation, not signature transport/device transaction.

**Atlas/rig import checks:** pixel UV bleeding on transparent sprite boundary, integer tile region, alpha preblend, directions, idle/walk frame tags, foot pivot, collision under legs, maximum frames/sprite, very long dialogue safe zones, 3D skeleton compatibility, mobile triangle/material budgets, armature scale/orientation, glTF skin joints/morph weights, texture colour space, KTX2 mipmaps, age/hair mesh penetrations, skeleton animation clip loop/crossfade, OS touch safe areas. A shader image of a face made from procedural circles is NOT a valid glTF character rig.

## 10. Licensing / provenance matrix, with 2026 caution

**Verify the exact asset page and downloaded archive before acquiring it.** "Free" may mean free to play, free personal-use, free to download but not redistribute, CC0, a specific custom license, or something that changed since an older FAQ.

| Source                                                                                                                         | Present evidence / legal caution                                                                                                                                                                                                                                                                        | Recommended use                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Original artist-authored LIVEIT commissions or owned original work**                                                         | Obtain explicit assignment or perpetual worldwide commercial game distribution, adaptation, porting, marketplace and sublicense provisions in writing; retain invoice/rights statement                                                                                                                  | BEST for hero player/NPC rigs, original tile language, branded HUD and core theme                                                                    |
| **Kenney** (https://kenney.nl/assets; https://kenney.nl/support)                                                               | Kenney confirms assets on its asset pages use **CC0**, including commercial use without obligatory attribution; repository already contains 28 pinned UI/isometric PNGs, see provenance JSON                                                                                                            | Interim HUD/icon and material blockouts; do not pretend existing isometric Kenney props are final top-down pixel tiles                               |
| **Poly Haven** (https://polyhaven.com/license)                                                                                 | Its assets are **CC0** per published policy; inspect specific downloaded HDRI/texture/model and original source/format                                                                                                                                                                                  | Neutral lighting/HDRI and texture helpers for polished 3D, not final character-face direction by default                                             |
| **Quaternius** (https://quaternius.com/faq.html and https://github.com/Quaternius/quaternius.github.io/blob/main/license.html) | **Caution as of 2026:** older official FAQ says CC0, while newer **QAL v1.0 updated 2026-08-28** grants commercial game use but **restricts standalone resale/redistribution of original/modified assets**. Resolve applicable terms for the exact pack/download and date; DO NOT blindly import as CC0 | 3D blockout candidates only after per-pack legal confirmation; avoid republishing a third-party asset as a standalone downloadable LIVEIT asset pack |
| **OpenGameArt** (https://opengameart.org/node/5571)                                                                            | Per-work licenses may be CC0, CC-BY, OGA-BY, GPL or others. Attribution, derivative or DRM restrictions can apply. Choose exact compatible license and store proof                                                                                                                                      | Selectively licensed SFX/pixel filler, not a wholesale undifferentiated import                                                                       |
| **Google Fonts** (https://developers.google.com/fonts)                                                                         | Source platform indicates open-source commercial fonts, but must record each font's specific license, source file/author, OFL notices and bundled distribution requirements                                                                                                                             | HUD/display/body/pixel font candidates, no font files downloaded in this step                                                                        |
| **Blender and Khronos tooling** (https://www.blender.org/, https://www.khronos.org/gltf/, https://www.khronos.org/ktx/)        | Tools/formats, not blanket rights to any character/assets encountered online. glTF 2.0 models and KTX2 textures still need item-level copyright rights                                                                                                                                                  | Original rig/model/texture export and GPU compression pipeline                                                                                       |

Creative Commons CC0 still does not remove third-party trademark/privacy/personality rights. A photo or likeness could require model consent. No Nintendo, Episode or other competitor-proprietary art is authorized. Existing preview JPEGs require provenance/redistribution review before final commercial use. Do not place fonts/assets under unverified "MIT" just because the shader prototype used that identifier.

**Every future source import record** should capture source URL, source publisher/creator, download date, file sha256, source archive license text/screenshot or agreement pointer, redistribution/sublicensing rights, modifications, and component destinations. Source and derivative asset separation is mandatory. For stores, retain a credits/about-this-art view even where legally unnecessary—it improves transparency.

## 11. Realistic production budgets and mobile constraints

Original ambitious constraints retained for engineering validation, not as guaranteed measured facts: core app target under approximately **150MB** where feasible, native runtime memory envelope around **600MB** mid-tier, 60fps high/medium and 30fps battery saver. Source masters are NOT part of install size. Installed premium 3D content can be split into separately requested/streamed packs.

Provisional per-asset budgets to profile and revise by platform:

- pixel tile atlas page: 1024×1024 or 2048×2048 RGBA8 source atlas, guard pixels, nearest-sampled. A **1024² RGBA8 page is 4MiB uncompressed**, a **2048² page is 16MiB uncompressed**; page count and LOD remain constrained.
- 3D mobile hero model: first target at most ~20–35k visible triangles for closeup actor and appropriate LOD reductions; actual frame time, expression shapes and material draw calls decide tier, not an arbitrary polygon boast.
- background NPC 3D geometry LOD and outfit cloth simplified; first scene two hero actors and café should hold frame budget on a real mid-device without thermal runaway.
- 3D skin/hair/outfit texture: 512/1024/2048 per class as necessary, GPU compressed KTX2/BasisU with mobile transcoding and appropriate mip pyramid. Check sRGB vs linear data and transparency; never use blurred KTX sampling for pixel sprites.
- audio voice/music stems streamed or compressed appropriately; avoid decompressed hours-long WAV residing in memory.
- on-device texture asset residency/eviction tracked; do not prefetch all 200 locations and 400 cosmetics on app start. Show user storage/pack status.
- performance proof: 10-minute pixel wander + 10-minute 3D closeup per representative Android/iPhone, frame-time p95/p99, upload spikes, loading latency, battery, memory, color/face QA and font/haptics. All are future acceptance gates.

Simple production load estimate (non-binding): The 400 rig-piece goal + 200 distinct staged rooms and mobile QA represent a substantial multi-disciplinary art budget. The first playable slice deliberately uses a tiny curated subset and **reuses compatible rigging/material/environment modules**. Do not claim an entire 1,481-piece catalog can be produced by generating a JSON file or a single image model prompt.

## 12. Creator Studio and content packs

Asset studio should gain:

- item search/filter by stable ID, family, slot, source format, production wave and status, with "blocked on license" prominent;
- import original/approved assets, preview 1×/3× pixel sprite animations and the same character's true 3D turntable, eye/face/age/outfit checks;
- collision/tile map editor that previews physically walkable map routes, portal anchors and actor movement, not just background image;
- 3D scene stage for camera-blocking, NPC eye lines, costume attachments, re-lighting, emotional state timeline and dialogue panel safe region;
- original art rights inspector with source rights attachments/metadata, hashed compile outputs and native asset smoke results;
- pack publishing, download simulation, dependency/digest/signature validation and rollback evidence; author approvals logged.

Note the existing Next.js Creator Studio can author/edit story JSON; these native asset authoring preview capabilities are **future** feature gates. Don't claim present UI supports mesh importing/rigging.

## 13. QC and release signoff

Before marking an item **qa-passed**:

1. Distinct original look checked against style bible and competitor-copyright risk; original source is in source storage with own author/rights.
2. Correct asset shape/format, runtime metadata and canonical ID verified; hash recorded for actual final bytes.
3. Cross-platform import test: Vulkan/Android and Vulkan→MoltenVK/iOS when relevant. HUD audio/haptic asset tested on real OS semantics; fail on black views.
4. Rig/appearance parity or tile/collision link verified, depending on family. For pixel atlas, nearest sampling/UV seam captures at target scales. For 3D, inspect under several complexions/age morphs, outfit clipping, animation transitions and actual facial acting.
5. Performance and footprint measured, and fallback render supported if optional pack is missing.
6. License provenance and version audit stored, including publication/redistribution rights (crucial for downloadable asset packs).
7. QA evidence references stored as real file paths and reviewed; source integrity SHA-256 and pack dependency graph consistent.
8. Only then allow release manifest inclusion (plus separate publisher signing/staging). Asset status itself never triggers engine runtime code execution.

Cross-mode signoff: golden captures for pixel street, rain, interior, one named NPC; 3D matched hero and partner, 12 expressions and dress changes; actual outcome and HUD widget, story choice, memory and age shift. Real device install/restart and accessible talk/select/map/phone navigation must all work.

## 14. Inventory CLI and maintenance rules

The tracked [validator](../tools/validate-production-assets.mjs) reads all four catalogs and the [catalog index](../content/production-assets/v1/catalog-index.json), checks ID uniqueness, metadata, wave/category totals, 400/200/12/30 targets, the 28-existing-art proof and 51 procedural-baseline count, and enforces at least initial QA/source/rights/binary evidence on records promoted beyond **planned**. It is a **policy gate**, not cryptographic verification of the actual file digest nor a review of the art itself; future pipeline must compute digest and validate file contents.

    npm run assets:validate
    npm run assets:summary
    npm run check

In production progression the validator must be extended to compute real on-disk SHA-256 for promoted/QA/released runtime bytes, verify an allowlisted licensed rights/status taxonomy, guard symlinks/large files and confirm source licenses; current script's main purpose is safe and truthful _planned_ inventory lifecycle. Test it on CI. Do not mark a shader/procedural definition as a finished character just to improve percentage metrics.

The item lists are catalog targets and can be expanded without modifying gameplay reducers. When adding legitimate assets:

- add full entry and category target changes to catalog-index.json intentionally;
- supply source files, exact provenance, art/animation/geometry shape and device QA proof;
- build runtime manifest only for validated items and keep source/derived asset references separate;
- verify it loads/resumes on iOS/Android; render mode selection uses actual platform capability reported by installed native module, not an invented success flag;
- keep user save data compatible when assets are added/retired and introduce reversible migration for semantic part IDs when necessary.

**Definition of done for Step 5 (this current deliverable):** complete named machine-readable target inventories, current asset audit, rights/source candidates, formats, priorities, art/animation/QA specifications and executable validation/test tooling are committed. **Not included:** actual new art binary generation, world/3D native runtime integration, 400 completed artist meshes, 200 finished sets, downloaded sound/font licenses or live content delivery.

## 15. Source links, licensing and technical specifications

- Kenney verified commercial CC0 policy: https://kenney.nl/support
- Poly Haven CC0 licensing: https://polyhaven.com/license
- Quaternius FAQ: https://quaternius.com/faq.html ; updated Quaternius Asset License (Aug 28, 2026): https://github.com/Quaternius/quaternius.github.io/blob/main/license.html
- OpenGameArt FAQ and per-asset licenses: https://opengameart.org/node/5571
- Google Fonts open-source fonts: https://developers.google.com/fonts
- Creative Commons CC0 legalcode: https://creativecommons.org/publicdomain/zero/1.0/legalcode.en
- Khronos glTF formats/specification: https://www.khronos.org/gltf/ and https://registry.khronos.org/glTF/specs/2.0/
- Khronos KTX texture format and Basis: https://registry.khronos.org/KTX/specs/2.0/ktxspec.v2.html
- Khronos KHR_texture_basisu extension: https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_texture_basisu/README.md
- LIVEIT current 28 Kenney images source proofs: assets/kenney_ui_provenance.json and assets/kenney_city_provenance.json; rights candidates at assets/open_source_sources.json.
