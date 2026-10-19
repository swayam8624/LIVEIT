# LIVEIT — Pixel-Only Art Direction V2

**Approved 2026-10-19. All prior hybrid and 3D direction is RETIRED.** Detailed authority: [PIXEL_ONLY_DIRECTION_V2](PIXEL_ONLY_DIRECTION_V2.md). All art, screens, stories and city travel are original **2D retro pixel art**. Prior ENG-003 3D actor plans, ART-005 3D catalogs and cinematic GLB rigs are historical only.

## Everyday world

Original 16×16 source tiles, cardinal walk cycles, walkable interiors/market/school/hospital, portrait-safe camera, colliders and useful interaction masks. Pixel sprites with body, hair, outfit, accessory modular layers, deterministic life-stage changes and palette shifts. Smooth movement and subtle weather effects without smoothing the pixels themselves.

## Important story and emotional dialogue

**Large expressive 2D pixel portraits and staged animated scenes**, not 3D. Author 64×96 / 96×128 style portrait bust variants as useful working sizes, compatible with the saved character's small overworld sprite. Each key character needs blink frames, mouth talking frames, gestures, eye direction and 12 named emotional variations. Original pixel café/house/event foreground/background layers, cinematic 2D parallax, timing and lighting are what make the story premium. Allow multiple characters, speaker focus, reaction cuts, animated dialogue dock, choice cards and a factual outcome widget; preserve reduced motion and legible native text.

## Game HUD

Retro-futurist panel pixel edges, original icon language, intuitive thumb controls, compact life stats and in-world phone/chat, event cards, accessible dialogue/choices, meaningful haptics after committed state. Preserve the established HUD palette as a starting point: midnight #101827, mint #97E6AC, amber #FFD28A, coral #F49A82 and warm legible cream #F5F2D9. World district palettes need not all look identical to the HUD.

## Actual downloadable/source formats

PNG sprite atlases/layered source Aseprite .ase/.aseprite, Tiled .tmx/.tsx/.json maps (with collision/spawn/portals), background pixel PNG, safe font TTF/OTF + licenses, sound .wav/.ogg/.flac source converted when feasible to M4A/AAC mobile audio, MP3/M4A originals, UI graphics and 2D shader/palette parameters. Do not add .blend/.fbx/.glb/.gltf/3D/photorealistic PBR scene content. Only user-reviewed public-repository redistributable assets may be staged via [intake script](../tools/intake_pixel_assets.py).

## Current reality and QA

Current isometric district selector and static-ish RN illustrated StoryPlayer are fallback/prototypes, not pixel-complete free roaming. Pixel art needs actual asset files, proper frame tags, tile collision and portal tests, accessible story rendering and real phone captures. Existing 28 Kenney fallback assets and 51 procedural recipes do not automatically satisfy the new art standards. Old 3D demo can remain as archived technical history but not run as part of the production game.

View the active asset checklist: [pixel-v2 requirements](../content/production-assets/pixel-v2/required-assets.json).
