# LIVEIT — definitive graphics design specification (GDS-001)

> **ARCHIVED 3D/HYBRID PLANNING DOCUMENT:** The owner changed LIVEIT to **100% expressive 2D retro pixel art** on 2026-10-19. Its former 3D cinematic/model requirements below are superseded by [PIXEL_ONLY_DIRECTION_V2](PIXEL_ONLY_DIRECTION_V2.md) and [active pixel-v2 requirements](../content/production-assets/pixel-v2/required-assets.json). Do not implement 3D from this document.

**Design title:** A Life in Two Dimensions and a Thousand Feelings  
**Tagline:** Retro to live in. Cinematic to feel. Tactile to control.  
**Version:** 1.0 — approved for production specification, not a claim of finished implementation  
**Effective direction:** 2026-10-18  
**Scope:** Step 1 of 5, comprehensive product-wide graphics style bible. Step 2 defines every screen/mode, Step 3 the implementation architecture, Step 4 updates other repository vision docs and source, and Step 5 creates the full asset production inventory. Treat this document as the visual authority until explicitly revised.  
**References:** The user's original LIFEWEAVE master brief (§1–3, §4, §5, §8, §9, §10, §12–13), subsequent LIVEIT requests for an original Vulkan graphics engine and ever-expanding assets, and the latest explicit direction: Pokémon Red/Blue-style daily city exploration; lavish smooth 3D characters and conversations; responsive widget/choice HUD, sidebar and masked/anonymous social functionality.

## 0. Core product statement

LIVEIT is not a Pokémon clone, an open-world action RPG, a text novel, a Discord client or a cinematic viewer. It is a living, branching, multi-generational life simulator whose visual presentation deliberately **changes register with emotional distance**.

- **Live:** roam and perform daily life in a deliberately crisp, collectible-feeling, top-down, pixel-art world reminiscent of the visual _grammar_ of first-generation handheld role-playing games. This is a stylistic reference to grid/tile logic, camera clarity and small-town charm, not copying characters, maps, UI, sprite sheets, music or brand identity.
- **Feel:** step into luxurious, expressive **stylized 3D** when another person or major event requires attention: dialogue, romance, grief, family milestones, confrontations, major authored chapters, memories. Real depth, models/rigs, shader materials, facial acting, camera blocking and expressive lighting; **not merely an enlarged 2D sprite**.
- **Control:** operate life and social systems through a tactile, information-rich **game HUD** that can overlay the overworld and cinematic moments without becoming an office dashboard. Every confirmed meaningful interaction should respond immediately visually, with suitably light haptic/audio feedback when enabled.
- **Remember:** the same simulation identity, clothing, aging, relationships, home, memories, choices and consequences survive the transition between modes and after reload. The user can recognize their character in an overworld sprite and an emotional 3D close-up.
- **Grow:** cities, actors, costumes, shops, props, chapters, eras and countries must expand through versioned validated **asset/content packs**, not manually coded bespoke screen components. A content recipe or shader swatch is not equivalent to a finished, reviewed production asset.

**Success statement:** "I can casually live my life like a retro handheld RPG, and when something matters, the world opens into a beautiful 3D scene—then the consequence appears in my HUD and remains true."

## 1. Non-negotiable style decisions

| ID     | Design contract                                                                                                                                                           | Forbidden outcome                                                                                    |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| VIS-01 | Overworld art is actual bespoke **2D pixel art with top-down readability**, rendered using GPU compositing, pixel-perfect scaling and optional pixel-aware shader passes. | Pseudo-3D low-poly city replacing the requested tile-based exploration                               |
| VIS-02 | Overworld character travel is playable with responsive directional control and navigation, enterable places, collision, NPC markers and context prompts.                  | A picture of a town with only district selection cards                                               |
| VIS-03 | Important conversation and story shots contain **real 3D stylized characters and believable cinematic depth**.                                                            | Pixel sprites merely zoomed to fill dialogue panels; flat static portraits asserted to be 3D         |
| VIS-04 | One identity/appearance source supplies 2D sprite variants and the 3D rig, with consistent color, silhouette, outfit, age and distinctive features.                       | User looking like unrelated people in map and dialogue                                               |
| VIS-05 | Main navigation is a **game HUD**: animated stats, readable widgets, choice cards, quick drawers, status indicators and contextual interaction.                           | Productivity-app tab pages, unlabeled icons or static React Native prototype cards as final graphics |
| VIS-06 | Meaningful player actions return prompt feedback and an outcome widget that reports **true authoritative deltas**, using haptics when enabled and supported.              | Fake rewards, fabricated outcome cards, vibration for every scroll tick                              |
| VIS-07 | "Anon chat" lives in an in-world communications panel, visually separate from AI NPC roleplay, with consent and identity safeguards.                                      | Falsely posing AI as humans; making a random anonymous chat app as the product's primary purpose     |
| VIS-08 | Retro nostalgia is **playful, colorful, warm and legible**; cinematic scenes are lush and materially rich.                                                                | Gray-green monochrome across all scenes; nonstop scanlines/noisy CRT; blurry faux-pixel textures     |
| VIS-09 | Vulkan/ SPIR-V is the target gameplay GPU interface on Android; iOS uses MoltenVK over Metal. Accessible text/input may remain native.                                    | Claiming Expo image views, WebGL or generated PPM renders are a native live Vulkan view              |
| VIS-10 | Every asset/scene stays lawful, original or licensed with auditable provenance, and downloadable packs remain validated data.                                             | Borrowed Pokémon/Episode artwork, proprietary extracted assets or downloaded executable shaders      |

## 2. Visual hierarchy: three presentation spaces

### A. PIXEL WORLD — ordinary life and exploration (principal play space)

Purpose: the everyday feeling of owning a living town and a growing life. Use for streets, parks, homes, storefront entrances, campuses, schools, workplaces, neighborhoods, public transit stops and common interior activities. Movement is four-directional by default; cardinal routes, city blocks and contextual obstacles are visually obvious. The camera follows the avatar rather than the player following a long list of place cards.

Visual grammar:

- Deliberate visible pixel grid and strong silhouettes; **nearest-neighbor texture sampling only** for pixel-layer color sprites and tiles.
- Original 16×16 logical-pixel environment tile as production default. Signage, facade details, foliage and shadows can occupy multiple tiles.
- Character sprite footprint: 16×24 logical pixels for standard adult small-scale mode; hero/important NPC silhouettes may occupy 20×28 or 24×32; collision uses smaller feet rectangles, not whole sprite bounding boxes. Child and older-life forms have separately authored/adapted silhouettes, preserving identity.
- Default 4 directions, 4 walk frames per direction for all main cast; idle frames and optional turn/gesture variants. Crowd NPCs can have fewer frames but must not all look alike. Eight directions or richer animation becomes a quality-tier/production expansion, not a day-one blocker.
- Each asset uses palette discipline: approximately 8–16 distinct scene color families with intelligently reused ramps; this is a _new artistic target_, not original Game Boy hardware's enforced 4 grays. Color changes with district and weather.
- Buildings show doorway, services and occupiable purpose. 1–3 tile signage legible at world scale; paths, doors, intersections and stairs must not visually lie about collision.
- Depth from sorted sprites, occlusion cutouts, foreground tiles, local lighting gradients, shadow/sun rays and subtle water/rain shader; keep actual player silhouette clean.

Chosen logical viewport design baseline: **320×256 world pixels** (20×16 environment tiles at 16px), with camera crop/letterbox adaptation to each device. Keep original pixels square and scale by integers where display layout permits. On modern portrait phones the world viewport occupies the safe gameplay area, not the full screen: remaining physical pixels belong to the HUD. When variable device size prevents exact integer scale, adapt framing and resolution rather than stretching source assets; do not introduce visible texture blur. The historic Game Boy's 160×144 serves as a historical reference only, not a limitation or forced resolution for a premium mobile app.

The town should have original neighborhoods with distinctive silhouettes (e.g., Bellweather's riverside, university, market, studio and gardens), traffic/time-of-day ambiance, NPC routines and access to homes and jobs. City assets and upgrades visibly persist. User must be able to walk from one walkable district point of interest to an enterable location in the first playable slice. Long-distance travel can use a fast-travel transit screen as an optional convenience, never as the only navigation.

**Movement contract:** digital input/virtual joystick, continuous finger-direction swipe option and tap-to-route where accessible. Default avatar movement should finish one 16px tile in roughly 160–220ms depending on run/walk speed (a tuning target), with subpixel logical interpolation and pixel-snap display to avoid shimmer. World simulation positions are floats/fixed point; visuals snap only at final raster. Movement and NPC animation update at game simulation ticks independent of display refresh; render targets 60fps on medium/high devices, 30fps on low. Disable interpolation or switch to discrete grid stepping in an authenticity setting, without delaying inputs. Footsteps audio/haptic: spatially appropriate step sound but NOT a vibration every step.

**Pixel shader treatment:** composite tile maps, sprite atlases, lights/shadows, fog, fireflies, puddles, occasional light cone, rain/snow. Pixel-aware light and weather may run at coarser resolution for stylistic cohesion. Keep NPC selection outline 1–2 logical pixels; do not apply full-scene TAA blur, film grain at per-pixel noise or bloom that erases hard sprite edges.

### B. CINEMATIC WORLD — dialogue and major moments (premium emotional space)

Purpose: make conversations and choices _worth stopping the world for_. Use for face-to-face dialogue, named NPC meeting, episode chapters, family events, romance, career successes or failures, betrayals, crises, intimate quiet moments, memory flashbacks and meaningful introductions.

Visual grammar:

- **Stylized 3D**, not photorealism: anime-adjacent painterly comic forms, realistic proportions where appropriate, original identity, expressive eye/brow/lip poses, deliberate skin and hair material choices, soft cloth, warm depth and rich art-directed light. A 2.5D painted background is acceptable BEHIND a genuine rigged 3D actor, but not as replacement for 3D expression/motion.
- Actor pipeline: mesh, skeletal rig, blended shape keys for faces, layered outfit meshes/materials, hair geometry/card shaders, eye gaze, lip-sync-to-text timings, hand/upper-body acting and aging overlays. Body- and outfit-safe retargeting. Current Vulkan procedural actor shader is a useful experimental reference, not this finished rig.
- Frame composition includes foreground texture/props, midground actor blocking and background architecture/environment. Soft rim lighting, motivated key light, soft shadow/contact geometry, optional depth-of-field with text and eyes remaining clear. Avoid excessive plastic specular and uncanny facial hyperrealism.
- **Camera language:** 1-shot establishing (1–2 seconds), 2-shot medium, portrait/medium close-up, over-the-shoulder, reaction close-up and optional dramatic push or rack focus. Dialogue often uses two actors in same spatially coherent set. Camera may slide/zoom as beats land, not sway forever.
- Reference lenses/field of view are approximate art-direction labels: establishing 28–35mm equivalent, standard dialogue 50mm, emotional close-up 70–85mm; maintain UI readability, safe cropping and consistent eyelines rather than literal lens physics.
- Frame-rate goal: stable 60fps medium/high, 30fps low when quality trade-offs demand; actor mouth/eyes should animate smoothly. Texture/mip/filter settings for cinematic surfaces may use trilinear/anisotropic filtering, contrasting pixel-world nearest neighbor.
- Twelve facial expressions from the original vision remain: neutral, happy, sad, angry, flirty, shocked, scared, smug, crying, embarrassed, tired, thoughtful. Support blended transition between emotions plus idle blink/breath, listening nod, speech mouth motion, hand gestures, anticipation and recoil. Voice acting is not required for text-responsive mouth animation.

**Trigger doctrine:** the entire screen need not switch to 3D for every routine click. Lightweight encounters first show a pixel-world speech bubble/context card. Switch to 3D for player-started "Talk deeply", authored story/chapter, meaningful relational choice, a unique NPC introduction, high-impact life event, important memory or user-selected cinematic inspection. Repeated routine conversations should offer "Quick Talk" without camera interruption. Story Mode is always capable of cinematic presentation.

**Transition grammar:** player/NPC lock into final valid world position → pixel camera focus (90–160ms) → pixel-art aperture/iris or 2–4 tile mosaic break (180–260ms) → low-contrast 3D scene reveal/actor settle (250–450ms) → first line arrives. The same silhouette/palette bridges formats: e.g., pixel scarf becomes recognizable 3D scarf. Default entire interaction-start target ~450–750ms after scene resources are warm; cold-loading must show an honest loading state and should not trap inputs. Returning should spatially restore the player at a valid location. Reduced motion substitutes a clean crossfade. These are **animation design targets to measure** on devices, not measured performance claims.

Narrative choice display may use a subtle HUD dock over lower frame. 3D scene should never be obscured by opaque wall-to-wall chat cards. When the speaker changes, eyelines and framing respond deliberately; when relationship trust changes, the actual character expression should reflect the event, subject to the authored emotional state, not an unrelated random smile.

### C. SYSTEMS WORLD — interactive HUD, sidebar, widgets and messages

Purpose: be a tactile interface that makes statistics, choices and messages part of playing—not an interrupting productivity app. Panels should feel like tactile cartridges/cards from a fictional modern retro handheld console.

Visual primitives: 1–2px high contrast strokes, restrained bevel/shadow, slight square corners (4–10dp), stepped corner motif on primary cards, layered translucent backing over 3D only, sharp icon language, personality in typography and audio. Full-screen settings and long text stay readable and adaptable.

**HUD structure by responsibility** (exact per-screen variants belong to Step 2):

- top strip (persistent unless full-screen cinematic): avatar, name, current location, age/phase, in-game date, major currency value, current energy/health indicator;
- left edge / swipe drawer: character and appearance, relationships, family/legacy, career/school, inventory/home, skills and achievements, route graph, Memory Vault;
- right edge / swipe drawer: communications hub (NPC chat distinctly labeled AI, consenting real-player contacts distinct), notifications, journal, major pending events, tasks. Masked social is behind a secondary labeled section, never shoved as the app's primary unsolicited entry.
- bottom interaction zone: 1–3 current context actions, walk/talk/enter, a prominent annual "Age Up" / time-advance affordance when the mode permits; gesture-safe joystick area with contextual hiding; choice dock appears here during major decisions.
- transient "WHAT CHANGED?" outcome card: event/result title, actual state changes, involved person, verified journal/memory entry and a quick "View details" link; user can dismiss it without losing the underlying fact. Do not invent immediate guaranteed reward for probabilistic consequences. Show only validated effects known to the authoritative engine.

**Sidebars on phones** are overlay drawers or bottom sheets; **on tablets/desktops** may become pinned rails. Preserve clear viewport and 44×44pt / 48×48dp touch targets (design minimum). Never occupy more than ~25% of portrait gameplay width with persistent chrome. In world roam mode, essential HUD is collapsible to a minimal status strip; a new event may surface a subtle badge rather than forcibly opening a chat panel. Navigation is reversible and retains the world camera position.

**Choice cards** must show: concise action label; affordance icon; emotional stance tag (if meaningfully authored: honest, ambitious, impulsive, thoughtful); confirmed cost if known; uncertain future outcomes as uncertainty, never false odds. Selection is a 4-phase state machine: idle → pressed/armed → committed → resolved. For irreversible life-altering actions offer undo policy/confirmation per game rules, but no confirmation-spam for ordinary interactions.

**Events and aging:** after Age Up, animate a short month/year counter sequence, contextual day or season shift, NPC reactions if present, stat/finance changes in one truthful consolidated widget, a memory recap entry and optional milestone cinematic. Suppress extra celebration if year includes loss or death. A major loss is presented with care rather than reward confetti. Aging affects overworld sprite silhouette, cinematic model, voice-less acting, clothing and broader environment context—not automatic color grading that makes every elderly scene bleak.

**Conversation/social:** the communications drawer has clearly distinct lanes: in-world scripted/NPC messages; AI-backed NPC conversations with visible AI disclosure; real-player contacts/consented masked interactions (subject to platform policy), with report/block/mute controls attached to every relevant conversation. Distinctly labeled real/AI status; no synthetic avatars represented as available humans. Chat previews can display the same 3D character's current expression/pose only for AI/NPC or a consented character; never imply a human user's live face is captured. UI supports offline states, queued send, disconnect, unread and moderation controls.

### Masked social compliance guardrail

The user's original specification proposed random matching of masked strangers. **Current Apple App Store Guideline 1.2 is explicit that services used primarily for random/anonymous chat do not belong in the App Store**, and requires filtering, report, block and contact mechanisms for user-generated content. Product direction for iOS must be opt-in **context-bound gameplay social**, with explicit interaction, moderation and identifiable product purpose beyond chat; even then platform acceptance is not assured. Do not hide random chat behind an in-game phone to sidestep review. Preserve a safe, offline-capable NPC alternative, visibly AI-labeled. Relevant official source: https://developer.apple.com/app-store/review/guidelines/ and February 2026 clarification https://developer.apple.com/news/?id=d75yllv4.

## 3. Design tokens: colors, contrast and lighting

Existing gameTheme.ts tokens should remain a **HUD** foundation, not forcibly tint world environments. These hex values define the baseline; all variants require testing under color blindness, low brightness and 200% text scaling.

| Use                     | Hex     | Rule                                                        |
| ----------------------- | ------- | ----------------------------------------------------------- |
| UI deep night           | #101827 | default card/console backing, not all world pixels          |
| UI panel                | #1A2737 | clear information surface                                   |
| Raised/tappable panel   | #223449 | control affordance, visible outline                         |
| Primary readable ink    | #F5F2D9 | bright warm off-white for primary text                      |
| Secondary readable ink  | #B6C6C8 | adequate size/contrast, avoid tiny muted text               |
| Edge/keyline            | #507174 | 1–2px borders; increase contrast for focus                  |
| Positive/action mint    | #97E6AC | choice focus, selected target, non-destructive confirmation |
| Dark mint               | #356D62 | solid action fill with text contrast testing                |
| Milestone amber         | #FFD28A | earned discovery and important event emphasis               |
| Human warmth coral      | #F49A82 | social, relationship emphasis; not automatic danger         |
| Actual warning/negative | #FF7588 | real errors or health/risk warning + icon/text              |
| Water/world teal        | #2B617A | environment only                                            |
| Park green              | #427969 | environment only                                            |
| Road slate              | #243543 | environment only                                            |

**World-local palettes:** every location pack supplies original daytime/night/weather palettes that harmonize rather than match the HUD. Suggested art-target families: sunlit seaside ochres/blue-green, campus brick/cream/lavender, downtown signage cyan/magenta, studio warm plum/terracotta, gardens moss/leaf/amber, childhood cream and apricot, snowy city muted blue/violet, autumn elder scene gold/chestnut. Scene palette color counts may exceed Game Boy constraints. A location "mood" shader can blend lighting but should not globally suppress outfit colors, skin-tone differentiation or label contrast.

**Skin representation:** 12 existing skin-tone identifiers must render with even-handed material lighting and legibility in both styles; no complexion is mechanically "better". Warm/cool key lights must not collapse dark skin into silhouette or blow out light skin. 3D material/SSS values and sprite color ramps get artist QA across all tones. Outfit palettes need reasonable perceived correspondence in pixel and 3D modes.

**Accessibility:** color never conveys state alone. Selected route also has clear focus shape/check mark, loss has icon and text, severity has descriptive label. Stronger contrast mode provides thicker outlines and flatter backgrounds for interactive UI.

## 4. Typography and text readability

Four typography roles; no unlicensed bundled fonts, no platform-styled defaults leaking inconsistently between views.

| Role                          | Default direction                             | Metrics / behavior                                                                          |
| ----------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Brand/display                 | condensed bold arcade-inspired non-pixel face | roughly 26–38sp portrait, letter spacing restrained; all caps only short headlines          |
| Game HUD                      | monospaced, bold, systematic numbers          | roughly 11–14sp except safely smaller decorative coordinates, tabular digits; high contrast |
| Dialogue/body                 | smooth, characterful sans-serif               | default 16–18sp body, cinematic dialogue 18–22sp, line-height 1.35–1.5                      |
| Diegetic overworld pixel text | authored bitmap pixel font                    | pixel-world sign labels/rare headings only, never legal controls or long story dialogue     |

Font selections pending license/per-device QA, but current built-in AvenirNextCondensed-DemiBold, Menlo-Bold and AvenirNext-Medium can serve as temporary fallbacks. Production fonts must include commercial redistribution licenses, Android/iOS matching metrics and fallback language coverage. The older all-serif editorial appearance is **superseded**.

All reading text is a true scalable text layer independent of nearest-neighbor game scaling. Honor larger OS accessibility text settings, dyslexia-friendly option, high contrast, reduced motion and long-name clipping. Scene art never embeds essential dialogue or mandatory controls inside an inaccessible bitmap.

## 5. Motion, controls, haptics and audio: game-feel standard

The player should feel an input immediately, even if the server or storage result comes later. Input acknowledgment never falsely claims the consequence committed.

| Event                          | Visual response                                                     | Sound                          | Haptic policy                                                    | Suggested timing                                     |
| ------------------------------ | ------------------------------------------------------------------- | ------------------------------ | ---------------------------------------------------------------- | ---------------------------------------------------- |
| Menu/choice touch-down         | 1–2 logical pixel press/depth change; bright outline                | short click                    | soft selection only if not a repeated scroll                     | <50ms acknowledgement target                         |
| Navigation/select tab          | selected row slides/snap to detent                                  | light tick                     | selection when change commits                                    | 100–180ms                                            |
| Enter building                 | centered character passes doorway, short iris/scene wipe            | door/jingle ambience           | light confirmation                                               | 200–450ms                                            |
| NPC conversation               | avatar faces NPC, bubble opens or 3D focus transition               | gentle chime/ambience stem     | light on action, not each line                                   | 450–750ms warm cinematic target                      |
| Branching choice commit        | card accepts, others fade, authoritative effect resolves            | distinct decision signature    | medium on confirmed action                                       | immediate acknowledgement + honest loading if needed |
| Age Up                         | ring advances, sky/calendar shifts, counters roll and recap appears | restrained whoosh/stem cue     | medium/success for positive milestone; neutral or none for grief | 600–1400ms optional / skippable                      |
| Opportunity or message arrives | contextual badge/widget and readable title                          | short private notification cue | only for allowed opt-in notifications                            | never steals focus from a major scene                |
| Relationship change            | small heart/thread widget with real trust text/delta                | warm ping only if fitting      | one subtle pulse                                                 | 300–550ms                                            |
| Purchase/spend                 | amount updates, inventory changes, concise receipt                  | cash/confirm                   | one confirmation if success                                      | 250–450ms                                            |
| Error/rejection                | card returns, reason and retry action visible                       | soft low cue                   | warning/error only when appropriate                              | no fake success flash                                |
| Death/loss                     | restrained, respectful fade/ink memory transition                   | avoid celebratory cues         | off/soft only by player preference                               | event-paced, full skip and accessibility alternative |

Haptics **opt-in according to OS/user settings**, use Expo Haptics when supported (selectionAsync, impactAsync, notificationAsync); Android-specific supported haptics where available. Debounce duplicate triggering, avoid pulses for every walk step, chat character, frame or continuous scroll. Keep an accessibility toggle **Off / Subtle / Full**, default to system behavior; silence/reduced motion must never hide a game state. Sound is similarly independently adjustable: music, effects, ambience and notifications. Source: https://docs.expo.dev/versions/v58.0.0/sdk/haptics/

**Motion tokens:** quick feedback 80–140ms; small overlay 160–260ms; medium panel 220–340ms; story focus 450–750ms; milestone 600–1400ms. Curves: ease-out for entry and restrained spring for card settle; no rubbery, bouncing reaction to tragic scenes. Every animation can be skipped by user tap without skipping the game logic. Reduce Motion replaces camera shakes/zoom/parallax with crossfades or immediate transitions. Do not rapidly flash high-contrast material; retain source rule of no more than 3 flashes/s and favor zero.

Audio: gentle retro melodic motifs, short satisfying UI bleeps, city weather beds, context-specific footsteps; richer adaptive instrumental stems for cinematic tension, warmth, romance, reflection and triumph. Retain original spec's "no voice acting at launch". Text-linked mouth movement is not proof of recorded dialogue.

## 6. Identity parity, aging and narrative continuity

Character appearance is **domain data**, not a bitmap chosen randomly per presentation. The existing appearance schema includes skin, face, eyes, nose, lips, brows, hairstyles, hair color, body frame, outfit, outfit color, accessories, facial hair, headwear and makeup. Every cosmetic identifier maps into two representations via a shared identity/material/rig registry:

**Canonical saved character identity and appearance** -> **overworld pixel sprite atlas resolver** (body/age/facing/outfit palette) **and** **cinematic 3D skeleton/model/material resolver** (face shapes, brows, hair mesh, accessory anchor, cloth/outfit, aging). The two renderers may use different artistic detail, but wardrobe and personal identity must not diverge. Avoid creating a separate "chat avatar" identity. If a downloadable visual variant is unavailable, show a clear, design-approved fallback consistent with outfit/color, never an invented complete asset.

Aging is world-state driven: childhood, adolescence, young adult, midlife and elder form sets, with gradual scale, hairstyle/gray, posture, face morphology, scars/wrinkles only where plausible, new wardrobe availability and life-stage mood grading. Changes are not always a hard cut at birthday: blend the age-specific representation at important transitions and update sprites/model on the next frame/scene. Existing old saves must resolve valid default appearance and scene state. Cross-generational heirs inherit genealogical/contextual traits through simulation rules, not automatic identical clone appearances.

**World consistency examples:**

- The player's blue hair and red scarf appear in pixel town, at the café in 3D and on the relationship/message profile.
- After a saved clothing purchase, outfit changes only if equipped, persists on reload and shows in both modes.
- After aging years, older sprite/3D face update without changing identity.
- A character's emotional expression stays plausible between dialogue beats; AI outputs can request allowed expression names but cannot overwrite true relationship/simulation values.
- If a partner is absent/deceased in world state, a routine town encounter cannot spawn them as a living active NPC; explicit flashback mode may show them with correct framing.

**Visual continuity acceptance:** an independent tester can pair pixel and cinematic views of a character by silhouette, key palette and signature accessories across at least 12 canonical character combinations, five age states and 12 expression states; no test depends only on a name label.

## 7. Story visual grammar and outcome widgets

Three encounter scales:

1. **Micro-event:** Pixel-world callout and 1–2 choices, short HUD result. E.g., purchase bread, casual greeting, tiny job decision.
2. **Scene:** Dialogue in 3D with medium shot and two actors, 2–4 substantial replies/choices, meaningful emotional or financial state. E.g., confession, interview, reunion.
3. **Chapter / life milestone:** authored multi-location 3D sequence with acting, multiple participants, camera changes and ending/route consequences. E.g., marriage, child, death, campaign finale.

The visual director picks scale from authored event metadata, not a random LLM text heuristic. Emotional intensity also determines transition and haptic behavior. Non-interactive cutscenes must never exceed reasonable durations without skip or pause. A 3D scene begins with correct clothing, location, time, weather, NPC status and continuity.

**Outcome widget grammar:** title ("You were hired"), typed category ("CAREER"), 1–4 verified deltas ("Income +£X/year", "Trust with Amelia +Y", "Cash −£Z") and optional consequence hint only if the simulation authored it; no made-up future certainty. Widget occupies safe upper/right area in portrait or appears as a small bottom sheet when busy. It queues/coalesces rapid events; never obscures speaker captions or current choice. Accessible narration announces the important new fact once. A source log/memory entry links to a full journal for later review. Life loss/death displays facts carefully without misleading gamified scoring.

**Memory visual:** player-triggered flashback may desaturate or add faded halftone edge and 3D diorama; the scene must be a reconstruction of known authorized memory entries, not confabulated visual events labeled as historical truth.

## 8. Per-life-stage mood and city seasons

| Life stage  | Overworld treatment                                                                     | Cinematic scene treatment                                                | UI tone                                                              |
| ----------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| Childhood   | warm apricot/mint grass, bright clean edges and playful traffic density                 | pastel warm key light, close family eyelines, moderate bloom             | bright sticker-like badges, larger icons                             |
| Adolescence | energetic blue/coral signage, more school/friend social activity                        | stronger contrast and camera energy, youthful styling                    | dynamic but readable activity cues                                   |
| Young adult | most saturated and varied world palette, broad urban districts                          | deep expressive cinematic colors and diverse nightlife/daytime locations | balanced adventure/agency                                            |
| Midlife     | warmer, grounded architecture and wardrobe with changing neighborhood history           | realistic material restraint, richer domestic setting                    | clearer long-horizon finance/family surfaces                         |
| Elder       | optional golden seasonal light, preserved colorful environment, no mandatory bleak tone | gentle gold and sepia options, crisp face/eyes, quiet camera             | larger default readability preference offered, respectful milestones |

Age does not force identical emotional weather or culturally stereotyped appearance. Day/night and weather have separate physical/environment cues. In-game time and weather are derived from simulation/world data; user manual "visual preview" never rewrites the day/time.

## 9. Asset content style bible and scalable publication

**Overworld source art:** author original tile sets (16px tile), sprite atlases with 4 directions, one idle, four walk frames, terrain transitions, walls/roof occluders, collision/interaction masks and palette variants. Every asset has a logical anchor, layer depth and visual collision preview. Sprites must be nearest sampled without corrupted compression introducing halo/fringing.

**Cinematic source art:** original commercial-rights cleared 3D characters/models, skeletal rigs, blendshapes/expression controls, hair/outfit parts, animation clips, GLB/glTF or appropriate authored source, textures PBR/art-toon materials, scene sets, light probe/presets, camera blocking and timeline metadata. LOD and mobile-friendly atlas management. The original specification's ~400 rig parts, 200 locations and 30 FX/camera presets are **launch design goals**, not currently authored inventory.

**System visuals:** icon family, bordered HUD nine-slices, stat orbs, graph connectors, contextual event widget illustration, choice feedback FX, notification badges, branded fictional in-world phone UI; separate from Unicode glyph dependency on actual phone fonts.

**Pack rules:** stable resource IDs, version, author/source license, SHA-256 for external files, slot/body/rig compatibility, pixel/3D resolution, color-space, atlas and LOD metadata, download/uninstall size, fallback and regional/era tags. Downloaded packs are data/assets only, validated before atomic activation. The currently committed core has 51 procedural **recipes**, not 51 completed artistic images. Avoid asset pack code execution. The current renderer-neutral scene schemas are a foundation, not the final integrated mobile renderer.

Default budget targets from original brief: core app under ~150MB where feasible, texture atlases up to 2048, background source up to 2560×1440, memory under ~600MB on mid-range devices, quality modes Low 0.7 resolution/30fps, Medium 0.85, High 1.0/60fps; some requirements are ambitious and need real hardware profiling. Pixel-world internal resolution should remain logical/pixel-crisp across tiers; cinematic 3D renders may change resolution dynamically. Fail with a readable fallback rather than showing black/unavailable graphics.

## 10. Safety, accessibility and platform expectations

- User settings: haptics Off/Subtle/Full; audio stem/sfx/mute; type speed and tap-to-complete; reduce motion and flashing; colorblind palette; larger labels, text scaling, subtitles, one-handed HUD and accessible input.
- All touch controls have label, state, focus outline and sufficient hit target. Decorative pixel density cannot dictate tappability. Dialogue text and privacy disclosures stay real platform-readable layers.
- HUD notifications respect focus, quiet hours and notification permissions; provide in-game unread lists without unsolicited device notifications.
- Social real-player controls have explicit human/AI distinction, reporting, blocking/muting, privacy and service availability; platform-specific UX may omit disallowed matching altogether. No hidden bypass of iOS review rules.
- Small-screen portrait is first-class. Safe area, home indicator, hardware keyboards/controllers and tablet layout are supported modes with independent QA. No hard-coded screen-specific screenshot placement.
- Copyright: Pokémon Red/Blue serves only as a conceptual reference for simple top-down maps and purposeful tile encounters. Create every map, character, sound, sprite, font and UI ornament originally or from properly licensed sources; no Nintendo sprites, tiles, logos or other proprietary assets.

## 11. Twelve must-produce visual acceptance frames

These are **required future golden image targets**, not mockups claimed in this design-only deliverable:

1. Bellweather street, daylight: original tile grid, readable avatar, three enterable businesses, contextual HUD.
2. Same saved scene, night/rain: crisp sprite silhouettes plus shader lights/puddles, accurate world state.
3. Overworld interior: character at home, decorative inventory and job/financial context.
4. Moving player meets named NPC: obstacle collision, accessible prompt, face direction.
5. Pixel-to-3D match: identical player wardrobe/hair immediately before and after talk.
6. 3D café conversation: 2 active rigged actors, eye line, face emotion, motivated light, dialogue and choice dock.
7. 3D episode moment: 3-character blocking, layered set, camera move, completed branch and real aftermath.
8. 12-expression face sheet: stable identity, no different person generated between emotions.
9. Avatar aging board: same player at child, teen, adult, midlife and elder stages, in pixel and cinematic.
10. Life HUD/choice outcome: responsive widgets, verified trust/cash/age changes and haptic status.
11. Communication side panel: NPC/AI/human identity labels, safe message state and block/report visibility.
12. Memory/legacy scene: respectfully timed transition, actual saved journal fact, accessible text and skip.

Each frame has a source world save fixture, expected render mode, rig/outfit IDs, device/scale specification and a visual review record. Golden snapshots must be repeatable from deterministic frame/seed. Dynamic weather effects use fixed QA seeds. QA requires live interactions and screenshots/video captured on real iOS/Android builds, not just image-generation prompts.

## 12. Device performance and measurable interaction acceptance

Metrics are acceptance **targets to test**, not benchmark claims:

- World scroll/gameplay at steady 60fps on medium/high test devices; stable 30fps low/battery saver. No pixels jitter or texture shimmer during slow walking and diagonally near tile edges.
- Existing CI Vulkan headless rendering is a _prototype_. True shipped-world readiness requires Vulkan swapchain/camera/pixel atlas on Android, MoltenVK/CAMetalLayer equivalent iOS, character 3D rendering, render lifecycle/restart and fallback in the installed app.
- Input acknowledgement p95 within 50ms under normal load; 3D transition warm scene preferably under 750ms; any loading beyond that clearly represented. No deliberate haptic lag or spinner for simple offline interactions.
- Character appearance parity across both render modes before/after outfit, age, inheritance, save/relaunch.
- HUD and choice overlays never hide critical interaction areas in smallest supported layout or 200% text scaling; verify screen reader route.
- Battery saver and thermal degradation preserve clear pixel rendering and game authority while reducing 3D resolution, light complexity, shadow and particle budgets.
- 3D cinematic mode respects texture/material/animation quality tiers; no failing to maintain life state when GPU is lost or app backgrounds mid-scene.
- Social notifications and AI streams cannot mutate save or scene from out-of-date identity; user explicitly initiates any real-player contact.

## 13. Existing implementation reality (2026-10-18)

Already in repository: a deterministic Bellweather city scene generator; illustrated React Native city fallback; a retro HUD token set; a headless Vulkan compute city shader; a separate Vulkan compute procedural character/shader prototype able to generate character portraits, cast and emotion variants; a versioned 51-recipe visual catalog and validation/activation schemas; world-to-scene adapter; tests/CI for the preliminary prototypes.

**Not yet implemented, and not supplied by writing this specification:** a playable free-roaming top-down overworld; production pixel tile and sprite sheets; a complete rigged true-3D cinematic renderer; Vulkan embedded as a live player surface on iPhone/Android; a 400-part/200-location asset library; an actual live communications drawer; all HUD haptics and outcome widgets; tested publisher-ready accessibility across phones.

The new visual direction **supersedes** the old assumption of "Vulkan low-poly city exploration plus procedural 2.5D conversations" as the final product. Keep relevant Vulkan infrastructure/clean state code, but **pivot** the primary renderer outputs to: pixel-art daily-life world **plus** real stylized 3D conversations. Do not delete functioning simulation or legacy saves as a shortcut.

## 14. Step sequencing after this document

**Step 1 (this document):** definitive graphics design specification and acceptance rules.  
**Step 2:** screen/mode visual designs, layout and interaction state maps across phone/tablet and both render modes; including age-up, avatar, life HUD, story, chat and settings.  
**Step 3:** exact rendering/programming architecture, shader passes, sprite vs 3D interoperability, Expo/native bridge, scene graph, assets/events, performance and build/test strategy.  
**Step 4:** rewrite old vision/agent/art-direction docs consistently to point to this GDS as primary and remove city-only assumptions; implement needed wiring in scoped source changes.  
**Step 5:** exhaustive prioritized production asset manifest, license/format/rig slots, pack sizes, acquisition/generation pipeline and progression to 400+ parts / 200+ locations.

Do not silently claim Steps 2–5 were finished by documenting them as downstream work.

## 15. References and provenance

Source-of-truth user intent: user's current conversation and original LIFEWEAVE master specification, particularly its visual style (§8), HUD and life progression (§9), masked social (§10), artwork/content pipeline (§12) and QA targets (§13). Explicit user revision supersedes earlier Unity/URP and all-Vulkan-3D-overworld default.

Historical Game Boy screen facts only: Nintendo technical data, https://www.nintendo.com/en-gb/Support/Legacy-system/Technical-data-619585.html . No extraction of protected Pokémon art, ROMs or sound. Expo Haptics v58: https://docs.expo.dev/versions/v58.0.0/sdk/haptics/ . Apple App Store Guideline 1.2: https://developer.apple.com/app-store/review/guidelines/ ; official February clarification: https://developer.apple.com/news/?id=d75yllv4 . Existing code/source: LIVEIT repository docs/UNIFIED_VISUAL_ENGINE_VISION.md, docs/VULKAN_CITY_RENDERING.md, packages/world-schema/src/visual-assets.ts, apps/player/src/gameTheme.ts and native/city-vulkan.

Design-specific defaults (320×256 virtual viewport, 16px tiles, animation/motion times, typography ranges, new tile/camera style) are **new proposed LIVEIT design constraints**, not original Game Boy or LIFEWEAVE facts or tested runtime metrics.
