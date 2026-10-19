# LIVEIT Art Direction — Authoritative Hybrid Visual Bible

**Current direction (19 October 2026): RETRO TO LIVE IN. CINEMATIC TO FEEL. TACTILE TO CONTROL.** This supersedes the quiet editorial/2.5D aesthetic and interim all-3D/isometric-city proposals. Primary authority: [GDS-001](LIVEIT_GRAPHICS_DESIGN_SPEC_V1.md), [GDS-002](LIVEIT_SCREEN_MODE_BLUEPRINT_V1.md), [ENG-003](LIVEIT_RENDER_ENGINE_ARCHITECTURE_V1.md) and [unified vision](UNIFIED_VISUAL_ENGINE_VISION.md).

## Two visual worlds, one persistent identity

**EVERYDAY PIXEL OVERWORLD.** A rich, original, top-down handheld-RPG-inspired walkable town, made from authored 16×16 logical environment tiles, pixel NPCs, enterable homes/shops/schools, city/weather/time changes and real collisions. Four cardinal walk directions initially; adults roughly 16×24 logical pixels. Foot-based sprite anchors, authored 2D occlusion, roof fade, safe collision maps. Original colorful Bellweather districts (riverside, university, market, studio and gardens). Nearest-neighbor integer pixel scaling where possible, no TAA/bilinear blurring. 30/60Hz logical movement and fixed-step world physics distinct from frame refresh. The inspiration from Pokémon Red/Blue is the legibility, grid travel, top-down map and charming exploration _principles_, not Nintendo imagery, sprites, sounds, maps, text or UI trade dress. This is NOT a 3D/isometric city and NOT a passive district-card picture.

**IMPORTANT CINEMATIC 3D.** A major story/NPC encounter crosses from pixel play into genuine, smoothly rendered, original **3D geometry**: skinned mesh actors, facial blendshapes, skeletal poses, expressive hair/clothing, rich interior/set materials, camera director and artist-controlled lighting. Painterly comic and slightly anime-adjacent original style, clear skin/hair and natural shadows, gentle depth of field and rim. Twelve canonical expressions (neutral, happy, sad, angry, flirty, shocked, scared, smug, crying, embarrassed, tired, thoughtful), breath/blink/eye gaze, speech-related mouth/face motion and body gestures. Routine town hellos stay in a pixel bubble. 3D should never be faked by enlarging a sprite or claiming that the current procedural 2.5D circles/ellipses are a rig.

**TACTILE SYSTEM HUD.** Midnight/mint/amber/coral retro-futurist game surfaces support status orbs, real money/stats, navigation drawers, in-world phone, anonymous/social permissions, choice cards and factual "what changed" event widgets. Use short mono/condensed labels, properly sized readable body/dialogue text, accessible native text fields/screen-reader semantics, thumb-sized controls and haptics only at meaningful commits. GPU handles visual art/effects; meaningful controls and moderated chat remain actual native UI.

**ONE IDENTITY.** Same saved player/NPC identity, age, outfit, hair/skin, accessories and life events feed the pixel sprite atlas resolver and the true 3D rig/material resolver, including cinematic camera, phone portrait and memory/legacy views. Changing clothes does not independently create a new person in another mode. No skin, body or appearance style grants a game advantage.

## Palette ownership and presentation

The current shared gameTheme palette is **HUD**, not a rule that makes every room teal:

| Token        | Value   | Intended use                         |
| ------------ | ------- | ------------------------------------ |
| Dark         | #101827 | UI console backing                   |
| Raised panel | #223449 | Selectable surfaces                  |
| Ink          | #F5F2D9 | Readable primary text                |
| Muted        | #B6C6C8 | Secondary text (minimum readability) |
| Border       | #507174 | Selection and frames                 |
| Mint         | #97E6AC | Positive action / focus              |
| Amber        | #FFD28A | Discovery and milestone              |
| Coral        | #F49A82 | Human connection                     |
| Danger       | #FF7588 | Actual error                         |

World art has district-specific palettes, day/night weather and life-stage grading (childhood warmth, teenage energy, adult diversity, midlife grounding, elder warmth rather than automatic bleakness). 3D materials use correct linear/sRGB handling, art-directed skin-lighting QA for all supported tones, eye and face visibility, shadows and toned bloom. Pixel textures use nearest filtering and pixel-aware lighting/weather; 3D textures use mipmapped linear/anisotropic sampling. Those pipelines must remain distinct.

## Production formats and requirements

**Pixel:** original raster tile atlas, four-direction idle/walk/interact strips, intentional layering and feet anchor, collision/door masks, collision test map, atlas guard pixels and palette variants, QA at native 1× and presentation 2–4×. Default map tiles 16px; sprite footprints around 16×24; four frames per walking direction is the initial target.

**3D:** original licensed sculpt/mesh, GLB/glTF export with bone/face rig + expressions, outfit/hat/hair attachment rules, realistic-enough eye lines, age morph variations, PBR/toon material definitions, genuine environment props, camera/lighting presets, mobile LOD and prefetch. Existing 2.5D plates can be background layers behind actual 3D rigs if useful, but cannot replace 3D faces for important scenes.

**HUD:** crisp original icons, scalable accessible fonts with correct commercial licenses, nine-slice panels, arcade-like stat chips, safe-area adaptive sidebars, contextual choice/outcome widgets and short diegetic pixel labels. Avoid hard-to-read pixel paragraphs or rasterized report/block controls.

**Asset contract:** all content needs creator/source/license/rights record, human review, version, SHA-256 for external files, rig/map slots, animation/collision metadata and validated dependencies. Production ambition ~400 genuine customizable rig parts, ~200 reusable scene locations, 12 expressions, ~30 camera/VFX presets. Current **51 shader-backed manifest entries are procedural definitions, not 51 finished artworks**. Future signed downloadable packs are DATA, not executable new SPIR-V.

## Motion, interaction and reference checks

Pixel roaming should feel smoothly responsive without blur; do not add per-step haptics. Pixel-to-3D handoff uses matched wardrobe silhouette and purposeful iris/mosaic reveal, design warm target approximately 450–750ms after resources loaded, cold load honest about delay. Choice states idle/armed/pending/committed/failed, with a confirmation haptic only after saved outcome. Widget shows _actual_ changes to trust, money, reputation, journal—not random rewards. Respect reduced motion, skip, haptics Off/Subtle/Full and accessible 44pt/48dp targets. Grief or death does not trigger celebratory fireworks.

Required visual acceptance set: walkable original Bellweather tile street; an enterable pixel home; player/NPC walk/collision; rain/night pixel palette; identical pixel/3D person with same hair/outfit; actual 3D café face acting; meaningful choice dock; factual outcome after restart; child/adult/elder identity; in-game phone distinguishing NPC AI from actual consent-based humans; missing-pack recovery; and faithful memories. Every capture must have saved fixture/scene ID, device/resolution and source-asset rights.

## Prototype truth and historical styles

The current React Native CityMap/CityWorld is an **illustrated isometric district-selection FALLBACK**, not free-walk pixel gameplay. The headless Vulkan city.comp raycaster is a valid offscreen Vulkan proof but not the intended tile/sprite render pass. The headless actors.comp procedural graphics are GPU images but not mesh-rigged 3D cinema. Legacy RN StoryPlayer, AvatarPortrait and the current art placeholders remain useful until functioning native views replace them; don't delete their gameplay pathways. No phone Vulkan/MoltenVK surface has been proven.

Superseded historical options, preserved only as context: warm editorial all-2.5D; single low-poly city renderer; "modern indie 60%/retro 40%" as a uniform world rule; defaulting to Skia/WebGL in place of the required native Vulkan target. The original 2.5D character illustrations and existing CC0 props can remain legal fallback art, not final visuals. Never copy proprietary game source assets or unlicensed story art.

If style is changed later, GDS-001/002, ENG-003, this file and agent instructions must be reconciled together; no silent visual-direction reversals.
