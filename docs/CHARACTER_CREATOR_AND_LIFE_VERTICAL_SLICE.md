# LIVEIT character customization and life-loop vertical slice

Implemented branch: `feat/character-creator-life-loop` (17 October 2026).

## Built, not just planned

The player now has an original Episode-inspired appearance builder, implemented with React Native core primitives. It **does not reuse Episode artwork, interface graphics, character scripts or proprietary character assets**.

The avatar's appearance is represented as validated portable data stored on the player character (optional on legacy v1 saves). Cosmetic fields have no influence on relationship trust, earning power, health, skill or storyline privileges.

### Appearance menu

| Category | Available options |
| --- | --- |
| Skin tones | 12 |
| Face shapes | 5 |
| Eye shapes | 5 |
| Eye colors | 7 |
| Nose shapes | 4 |
| Lip styles | 4 |
| Brow styles | 4 |
| Hairstyles | 14 (including curls, coils, locs, braids, afro, waves, bob, pixie) |
| Hair colors | 12 |
| Body frames | 4 |
| Outfit styles | 9 |
| Outfit colors | 9 |
| Accessories | 5 |

The same appearance renderer is reused for the character creation screen, main Life HUD, custom appearance editing in People, and the player actor in Story Mode. It supports basic expression changes for warm and tense scenes. All options are unlocked from the beginning, are separate from pronouns and can be changed without payment. Save files preserve appearance and old files without appearance default visually without modification.

This is an **original 2D illustrated paper-doll prototype**, not a professional cinematic rig. Its facial dimensions/hair/outfits remain authored as stylized primitives. Full-body movement, reusable sprite textures, animation state machines, voice, character proportions and lighting are the next dedicated production-art phase.

### Next art pipeline

1. Establish one approved art bible: realistic/stylized level, proportions, full-body sprite canvas, lighting, outline widths, diversity requirements, animation frame rate and visual references.
2. Build 2-3 original layered full-body neutral rigs with consistent head/neck/torso/mouth/eyes/arm anchors; use a permissively licensed rig system or artists' owned vectors. Keep customizable avatar **data** unchanged when replacing renderer.
3. Add layered transparent hairstyles + outfits using anchor and mask contracts, not flattened generated portraits. Hair must work on every head shape; outfits must respect body variants without deformation.
4. Produce expressions: neutral, happy, anxious, angry, surprised, sad + blinking / talking / gesture motions. Bind Story Mode `mood` and future `actingCues` to these states.
5. Animate with Skia / Reanimated (or equivalent after FPS profiling), add anchored camera and scene position tracks, preserve reduced motion, and benchmark low-end phones.
6. Commission or generate art concept pieces with documented commercial rights; manually clean, layer and validate before bundling. Never infer that a drawing is rigged because an AI tool depicts multiple poses.
7. Add an appearance migration test so all previously created characters retain their saved choices.

### Life mode improvements

The Free Life first screen now exposes a game-like Character HUD with savings, wellbeing, skill, recent life event, and **AGE UP**. Age Up advances a simulated year in one deterministic world transaction, accrues annual income/expense calculations, updates NPC offscreen milestones, schedules a limited city opportunity and records a history summary. It does not require a paid energy/ticket timer.

A real career chain is available: apply for a job in technology, creative work, business or community service; attend a skill/reputation/stress-dependent interview; earn a contractual salary; build actual work experience; ask for promotions and raises; resign and change field. The prior auto-employment logic remains for old v1 sandbox activities and will be migrated in a later dedicated economic overhaul.

The app's gameplay action dispatcher now reads the latest synchronized save reference before committing a new action, reducing lost updates from rapid user input. Persist operations still queue asynchronously. More robust per-action IDs/recovery and backup history remain future tasks.

### Regression gates

- Input validation rejects unapproved appearance values and additional executable properties.
- No stat changes when an existing character changes clothing.
- Existing v1 saves without appearance/employment still decode and load.
- Annual age-up is pure/reproducible and NPC careers advance chronologically without simulating 365 full daily UI actions.
- Interviews can succeed or fail; promotions have prerequisites; leaving a job permits a later career switch.
- Browser automated flow tests creator options, creating a life, age progression, revisiting People to customize, reload persistence, career interview, and desktop/mobile layouts.
- JS bundles/builds are not a substitute for signed physical-device testing or frame pacing tests.

### Significant unfinished parts

This milestone is **not full BitLife or Episode**: school/family/health/economy/legal systems, long-form multi-episode cinematic characters, camera, voice/sound, mature creator asset tooling, store approvals and moderated publishing are not yet implemented. See `docs/LIVEIT_2_GAMEFEEL_CONTENT_MASTERPLAN.md` for ordered P0-P7 scope. Avoid describing the prototype illustration as Episode-quality animation until produced and verified.
