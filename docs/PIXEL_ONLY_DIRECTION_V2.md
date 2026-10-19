# LIVEIT — PIXEL-ONLY VISUAL DIRECTION V2

**Owner decision, 2026-10-19. ACTIVE SOURCE OF TRUTH.** The owner has eliminated all 3D from LIVEIT. This document overrides every inconsistent 3D requirement in GDS-001, GDS-002, ENG-003, ART-005, previous README/AGENTS materials, and the historical 1,481-asset catalog. **Do not produce/import glTF meshes, skinned 3D rigs, 3D café interiors, 3D animation or cinematic PBR camera passes for the game.**

## The pixel-only game

**Overworld:** original top-down, charming and deeply alive handheld-RPG inspired pixel city: 16×16 logical world tiles, crisp sprite atlases, smooth four-direction walking, indoors and out, real collisions and enterable doors, workplaces/school/family/shops, NPC routines, weather/time/season cycles, age and outfit variations.

**Dramatic story & dialogue:** never switch into 3D. Instead compose **large layered 2D pixel portraits/character busts** with speaking mouths, blinking eyes, poses, 12 expressive emotional faces, lighting/palette shifts, character blocking, depth-like 2D parallax, scene-specific background pixel rooms, reaction cuts and short dramatic transitions. Portraits come from the same canonical person/outfit/age identity as the small overworld sprite. Important scenes are richer pixel art, not a separate 3D engine. Dialogues and choices remain accessible text/HUD and save actual consequences.

**Game HUD:** tactile pixel-edged controls and widgets for aging, finances, relationships, dialogue choices, in-world phone, memories, chat, notifications, and reversible error/focus states; haptic confirmation only after a saved authoritative action. Keep dynamic body/dialogue text native and readable rather than rasterizing it into tiny pixel fonts.

**GPU/render:** 2D tile/sprite raster, logical pixel buffers, palette/weather/post and nearest presentation. Android Vulkan/iOS MoltenVK optional targets if the current engineering still warrants them; no active 3D passes. Existing headless Vulkan 3D samples remain archived technical experiments, not final visuals.

## Catalog & assets

The former 1,481-item inventory and its 400 3D parts / 200 3D locations are **archived historical goals, retired**. Do not claim the owner still wants them or require Blender modeling. Active needs: pixel tiles and collision maps, pixel 4-direction characters and modular wardrobe, larger animated pixel expression portraits, layered 2D cinematic rooms/backdrops/foregrounds, full 2D GUI, SFX/music, optional pixel shaders and verified safe font files. User has downloaded many ZIPs and sounds. Ingest via tools/intake_pixel_assets.py; scan first, approve commercial public GitHub redistribution separately per pack, then import supported media. No unlicensed source ZIPs in public GitHub, and raw archives remain local by default. Shader code and 3D formats are not accepted as assets.

## First actual play loop

Walk a Bellweather street on a real tile grid → enter café → see Amelia as pixel NPC → transition to richly animated, expressive **pixel portrait** dialogue in an original layered café scene → choose → show true saved trust/memory widget/haptic → return to correct tile → kill/reopen, consistent save. No 3D anywhere.

## Migration safety

Keep the working TypeScript simulation, narrative engine, saved worlds and current illustrated/district selection fallbacks until a tested pixel replacement exists. Never delete player lives, silently override existing user work or pretend a catalog/import script is a finished game. The old 3D shaders and focused test files can remain for archived proof or eventually be removed once native builds and CI are migrated. Update user-facing build status honestly.

All future Codex agents must read THIS document first, then selectively reuse older papers for domain design without resurrecting 3D requirements.
