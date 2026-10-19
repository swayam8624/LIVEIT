> **Visual production direction revised on 19 October 2026:** this 2026-10-17 roadmap remains useful for gameplay, free-life events, story authoring, content operations and user experience but its rendering options and "2.5D as production" suggestions are historical. Authoritative current graphics: [GDS-001](LIVEIT_GRAPHICS_DESIGN_SPEC_V1.md) (top-down crisp pixel overworld + actual 3D cinematic faces), [GDS-002](LIVEIT_SCREEN_MODE_BLUEPRINT_V1.md), [ENG-003](LIVEIT_RENDER_ENGINE_ARCHITECTURE_V1.md). Do not execute a Skia/2.5D renderer evaluation as if it overrode those decisions. Existing game/domain state and release QA rules below remain valid.

# LIVEIT 2.0: Game-Feel Rebuild, Story Library, and Creator Platform

Prepared: 2026-10-17. Planning artifact; **not a claim that the features described here exist yet**.

## Vision and non-negotiables

Create an original, commercial-quality life-simulation and animated-interactive-fiction platform. Free Life and Story Mode are equally important, with shared state and explicit standalone timeline isolation. Borrow successful _interaction principles_ from BitLife and Episode, **not their proprietary artwork, animations, scripts, interfaces, stories, sounds, or trademarks**. No advertisements, energy timers, paid dialogue choices, forced retries, pay-to-win outcomes, or frustrating time-walls. Monetize optional creator tipping, cosmetics, or separately priced substantial additions only after the product works well for free.

Success is not measured in how many buttons are visible or how many story JSON files are indexed. It is measured by fast, expressive, consistent, replayable, _finished_ interactive experiences.

## Direct source-code audit (main branch at 2026-10-17)

- `apps/player/App.tsx` is about 1,800 lines: app boot, storage queue, navigation, onboarding, Scene UI, Free Life actions, people, and journal are coupled.
- Free Life offers work / study / friends / rest activity clicks that largely adjust stats and pass time. There are limited careers, no proper school/family/purchasing/health/romance/career transitions and no life-stage arc. Current character starts at 23; the age-up loop of a life simulator is missing.
- `chooseCareer()` explicitly rejects switching careers while describing a _future_ transition event. A missing gameplay mechanic is not a feature.
- `visitDistrict()` updates a stored district and history; many city opportunities are not strongly tied to spatial or social context.
- The 20 scripted encounters are interesting prototypes but mostly one-off paired decisions. The scheduler offers them on fixed simulated-day cadences, and resolved content doesn't replay.
- NPC careers/goals advance on authored day numbers, not reactive plans, budgets, schedules or interpersonal situations.
- Story Mode uses largely one illustrated stage, minimal portrait logic, and conventional card-like text choices; no true rigged actors, outfit continuity, scene-specific backgrounds, camera blocking, reactions, music, or cinematic pacing.
- Current story schema supports fact/trust conditions and two consequence operations: relationship adjustment and memory creation. Authoring new cast, dynamic flags, items, money, job changes, playable minigames and scene-level animation cues requires v2.
- Creator Studio _does_ execute real shared-state preview choices, but it is not yet a production publishing service. Locally imported packages are JSON and are not secure public-media packages.
- Shared save state is validated and backward compatible, but player event handlers close over prior rendered state and persist asynchronously: audit rapid concurrent taps for dropped actions, stale revision updates and duplicate choices.
- Browser visual smoke tests and Hermes bundle exports pass. Native signed binaries, actual devices and public-user feedback are not verified.

### Critical rebuild decisions

Retain shared TypeScript schemas, deterministic simulation, consequence engine, narrative core, continuity/save format and CI; redesign player visuals/flows **without** throwing away the game rules. The selected long-term production graphics engine is a shared C++ Vulkan/MoltenVK native renderer, with a dedicated **sharp top-down pixel tile/sprite pass** for Free Life and a **real mesh/skeletal 3D scene pass** for important conversations/stories; RN continues to own accessible HUD and temporary fallback. Implement the native module and persistent pixel navigation incrementally with actual device evidence. Do not switch to Unity, Skia-only graphics or offscreen screenshot rendering by assumption.

Split `App.tsx` into `app/navigation`, `app/bootstrap`, `app/save-coordinator`, `features/life`, `features/story-player`, `features/people`, `features/library`, `features/studio-bridge`, and `ui/game-primitives`. Introduce an atomic action dispatcher with a single authoritative state update + durable save queue and idempotent action IDs. Store migrations must preserve all v1 player progress.

## EXPERIENCE A — Free Life (BitLife-grade speed, LIVEIT identity)

### Information architecture

One dedicated game screen per activity group, not a lengthy vertical webpage:

```
[Top HUD: avatar • first name • age • cash • happiness/health]
[Current life event timeline: 1-3 recent outcomes]
[Primary central button: AGE UP +1 YEAR] [one subtle haptic]
[Contextual event card: meaningful dilemma, if one is pending]
[Dock: Life • People • Career • Assets • Activities]
```

A separate optional `City` screen can be entered from Activities. The map must not push the actual life loop several scrolls down. User should never have to scroll from a fixed café photo to find `Age up`.

### Action resolution loop (target 5-15 seconds)

1. Read life state at a glance; choose life activity or age up.
2. Action opens specific choices and immediate feedback (not just stats), like apply for a job, ask someone out, purchase a vehicle, start a business or join a club.
3. Resolve transaction using data-driven rules and seeded randomness based on skill, finances, mood, relationships and world.
4. Show a short story-like event response: who reacted, what changed, one optional detail view, and **exactly** what game state was updated.
5. Add the event to the life chronicle. Reopen activities within a single tap.
6. Age up advances _world years_ with birthdays, jobs, school, relationships, finances, life events; don't blindly multiply all daily wages by 365 without economics tests.

### Feature domains, ordered

**Tier 0 (vertical slice, fully functional)**: player age/family life stage; education/school/jobs with interview and promotion pipeline; 12-20 distinct activities; friendship/date/relationship system with NPC boundaries; finances and recurring expenses; property basics; 80-120 contextual events with flags, cooldowns and follow-ups; initial setup with multiple background choices; an at-a-glance lifetime timeline; save/load/restart with restore warning; fast age up; audiovisual feedback.

**Tier 1 (closed beta)**: birth-to-elderly life cycle, health/habits, grades and educational opportunities, marriage/children/parents, career branching + layoffs + job switching + entrepreneurship, housing/vehicles/debt, reputation and social networks, achievements and legacy; 300+ hand-edited event _templates_, broad enough that runs are recognizably distinct.

**Tier 2 (post validation)**: evolving world conditions, legal/social consequences, travel, ambitions, community outcomes, generational continuity, accessibility/localization and creator-authored compatible life events.

Do not call a profession implemented merely because a drop-down sets a string. Every domain requires gameplay, progression, affordances, failures and narrative feedback.

### Event rules

Use `EventDefinition` with `eligibility`, `probabilityWeight`, `cooldown`, `priority`, `followUpGroup`, `requirements`, `choices`, `consequences`, `resolutionText`, `storyHooks`, `contentRating`, and `sourceProvenance`. Variation should emerge from world state, not repeated generic LLM prose. Guard contradictory situations (dead relatives calling, child owning an established company, repeated one-time crises), money overflow, invisible negative balances and NPC stats outside range.

A year can contain a small story reel (1-3 memorable changes + optional context) and 0-2 decisions; use gameplay balance tests to tune this—not random spam.

## EXPERIENCE B — Story Mode (original animated interactive fiction)

### Main navigation

```
[Continue Reading — large illustrated cinematic chapter cover]
[Carousel: LIVEIT Originals] [Public-domain adaptations] [Community]
[Genres: Romance | Drama | Mystery | Thriller | Horror | Fantasy | Sci-fi]
[Cards: poster, author, chapter length, content tags, completion, likes]
[Search, Bookmarks, Downloads, Published/New/Completed filters]
```

### A scene is NOT a web card

Each scene fills the viewport with stage layers, actors, lighting/weather and an _anchored_ bottom dialogue dock. Dialogue reveals on tap, optional skip/read history. Character portrait/bodies are in-stage and expressive. The dock exposes speaker, styled line, decision rows _only when a decision is meaningful_, save/exit, history and accessibility settings. No nav chrome over the actor's face.

```
┌────────── Episode Player (phone portrait) ────────────┐
│  ‹ chapter title                           ⚙   •••  │
│  Background image, depth/parallax, mood, location     │
│      [NPC A: left  -  pose] [NPC B: right  -  pose]  │
│  Camera crops / slide / fade / ambient light          │
│                                                       │
│  [AMELIA]                                             │
│  “I thought you weren’t coming.”                      │
│  [I came because I promised.]                         │
│  [I needed to see you.]                                │
│  ▼ history                    tap to continue →       │
└───────────────────────────────────────────────────────┘
```

Episode's own directing documentation describes character placement, animation, camera cuts/pans, overlays and background staging; these principles inform the feature requirements, **not copying their proprietary implementation**. See https://pocketgems-support.helpshift.com/hc/en/10-episode-writer-s-portal/section/85-writer-s-portal-guides/.

### Animation asset strategy

**Updated first production visual tier:** one original 16px tile city street and café with actual walk/collision/door interaction; a pixel player/NPC with four-direction animation; and two **real skinned 3D character rigs** in a genuine 3D café set with at least basic eye/blink/face/gesture animation, author-approved lighting, camera, story dialogue dock, music/ambience toggle, optional haptics and voice-off default. Author 12 named expression controls as a growing rig goal. Preserve scene/age/outfit state from the same saved identity; deliver real native Vulkan and MoltenVK frames before calling this released. Existing 2.5D cutouts may remain temporary accessibility/fallback artwork but are not the production cinematic requirement.

**Longer-term tier**: scalable rigs, lip-sync, prop interactions, richer gesturing, group staging, rain/reflections and authored cinematic cutscenes. Keep deterministic timeline tests independent of rendering. A clean story with basic expressive animation beats a huge catalog with broken poses.

### Shared/standalone continuity

Every story has explicit continuity mode: `standalone`, `life-compatible`, or `world-pack` (future). `standalone` must never leak choices into Free Life. `life-compatible` declares character/world/age/location requirements and can change the player's world via permissions. Support at least two independent saved story timelines; version-pin story packages so creator revisions don't corrupt chapter resumes.

### Story renderer acceptance

- Stable 60fps target on representative mid-tier Android hardware **when animations are active**, measured, not assumed.
- Choice input visual acknowledgement target <100ms at p95 on tested devices; durable writes may complete asynchronously with safe recovery.
- No speech box clipping on 320/390/430px widths or with large accessibility text.
- Scene transition cannot trap a user or hide options; skip/auto-play/reduced motion/read history accessible.
- A 10-minute original chapter has no placeholder initial circles, mock CTA cards, broken portraits, or repeated café background in all locations.
- Branch decisions alter visible consequences or later dialogue; no paid good endings.

## CONTENT ACQUISITION: LEGALLY REUSABLE, ACTUALLY PLAYABLE

See machine-readable vetted candidates `content/open_licensed_source_catalog.json` (**30 individual catalog entries** including 19 root editions, 9 selected short stories and two open-licensed interactive-source libraries). A catalog entry is not a playable, cleared package. Every entry starts in `candidate` state.

**Source categories and permissions**

1. Existing historical literature believed U.S. public domain: Standard Ebooks (https://standardebooks.org/about), Project Gutenberg (https://www.gutenberg.org/policy/license), Wikisource only with edition/translation inspection. Check country rights _before_ adaptation/publication. India literary term is generally author's life + 60 years from calendar year following death (https://copyright.gov.in/Copyright_Act_1957/chapter_v.html); other jurisdictions differ. Do not reuse copyrighted covers, illustrations, typography asset files or translations just because the original author died long ago. Project Gutenberg's trademark rules make removing their boilerplate/trademark and keeping provenance essential for altered commercial derivative works. Do not bulk scrape their main website; use permitted archive mirrors for bulk (https://www.gutenberg.org/policy/terms_of_use.html).
2. Explicit CC0 narrative repositories: e.g. https://github.com/lightlogic/twine-stories (check subassets). Actual stories, not all tools.
3. MIT sample **story** files: https://github.com/inkle/ink-library/tree/master/Stories; review per-file notices and attributed third-party material. MIT requires retaining its notice in redistribution.
4. Other Twine/Ink/ChoiceScript source repositories: only when story text license explicitly permits commercial adaptation; a compiler/runtime's MIT license gives **no** story rights.
5. Original or commissioned author work: writer keeps copyright; LIVEIT needs a clear nonexclusive publishing license, allowed territories/formats, creator attribution, takedown rules, revisions, and optional revenue agreements.

**Ingestion pipeline**

- Catalog discovery: Gutendex REST metadata `?copyright=false&languages=en&search=...` and Standard Ebooks feeds. Metadata marked `copyright=false` is U.S. status, not global clearance.
- Rights review per original work, selected edition, translator, territory, illustrations, third-party brand use, and distribution strategy. Save permanent source URL, author death year, first publication date, source SHA-256, text version, analyst note and recorded decision; uncertain license blocks shipping.
- Fetch/archive legal source texts in a private provenance store; stripping headers only when permitted.
- Convert a **copy** into a narrative adaptation brief: synopsis, cast, locations, character motives, tone, original plot beats, proposed player role, branches and ending constraints.
- Human-written or human-edited chapters: coherent dialogue, choices with later consequences, authored scene blocking and audio, consistent character speech; AI may produce drafts for reviewed, rights-cleared material, not blindly autopublish.
- Compile to restricted LIVEIT story-v2 IR; static validate every reachable path, endings, code injection, effect permissions, age/genre tags, data lengths, media references, version pinning and supported languages.
- Editorial playtest all branches (including safe content), verify accessibility and mobile/desktop frames, QA outcomes and rights approval. Only signed/approved packages enter public catalog.

**Launch library proposal — quality-gated**: 2 existing original story arcs extended to multi-chapter structure; 4-6 carefully adapted classics across romance, mystery, horror and speculative fiction (shorter works first); 8-12 high-quality independent episodes by commissioned/opt-in creators; 25-50 authored life events with multi-step follow-ups. Do not announce 1000 stories when 1000 plain texts are still not interactive.

Recommended first pilots:

- `The Adventure of the Speckled Band` — concise detective narrative (check depiction of threats), objective/hypothesis choices.
- `Behind a Mask` — social strategy with strong character motives and alternate alliance outcomes.
- `The Strange Case of Dr. Jekyll and Mr. Hyde` — short, psychological, atmospheric identity story.
- `The Time Machine` — strong reusable locations and exploration/survival choices.
- `Pride and Prejudice` — flagship longer romance/social strategy arc after actors/costumes mature.
- One intentionally small CC0 Twine source as import-compiler test, then editorially re-stage it.

## AUTHOR STUDIO & PUBLIC PUBLISHING

### Creator Studio tools

Art-first scene builder with actor timeline, backdrop layering, poses/expressions, speaker/camera/audio tracks, flow graph, branches, conditions, state effects, asset browser, tutorial previews, preview of current player state, automatic reachability checks, accessibility and locale checks. Authors should not need to edit raw JSON except advanced work.

Accept sanitized Twine/Twee (Harlowe/SugarCube supported subset) and ink via versioned parsers; **never execute creator-provided HTML, JavaScript, macros or arbitrary code** in the player or on the service. Unsupported expressions produce actionable diagnostics. Provide export roundtrips, no silent branch deletion, basic conflict detection and autosave checkpoints.

### Publishing backend

- Identity and author profiles (verified accounts, unique handles and age policy).
- Versioned StoryDraft → ReviewSubmission → ApprovedVersion → PublishedListing → DownloadableContentPackage. Immutable published versions, checksums and content signatures.
- Object storage/CDN for safely processed images and audio; validation, MIME sniffing, decompression/image bomb limits, virus scanning and strict quotas. Never hotlink arbitrary external uploads at runtime.
- Moderation: report/block tools, pre-publication review when necessary, copyright declarations, takedown process, appeals, escalating repeat-abuse controls and youth-safe filtering.
- Search/discovery, genre tags, reading history, save state version pinning, authorship ownership, recommendation ranking and reviews with abuse prevention.
- Content package compatibility: old client must reject unsupported node features gracefully, never partially apply invalid economy/trust effects.
- No implementation of monetization or creator revenue splitting until accounting/consumer refund/tax and store compliance are approved.

## QUALITY AND MEASUREMENT

Collect on-device gameplay test metrics, not just build success:

- age-up completion under 1 sec on a median supported device, UI immediate feedback target <100ms, and no scroll-position surprises;
- 30-minute Free Life session with no obvious repeated unique encounter and actual progression in education/career/relationships;
- every user-visible activity affects concrete world state; disabled buttons explain precisely why;
- storyline first decision occurs promptly and is meaningful; 10-minute chapter is fully staged and has differentiated characters;
- 100% story graphs compiler-validated; property/fuzz tests cover malformed package inputs and extreme player states;
- rapid 100-tap harness verifies correct idempotence, ordered state transitions and durable save/restart;
- all pages tested at 320, 390, 430, 768 and 1440 widths, large font and reduced motion;
- physical Android/iPhone smoke test in airplane mode and after suspend/resume; no store-readiness assertion from JS bundle exports.

## EXECUTION ORDER AND ACCEPTANCE GATES

| Phase                                  | Scope                                                                                                                  | Gate                                                                                              |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| P0: stability foundation               | Profile CPU/renders/taps; freeze/migrate saves; state dispatcher; eliminate duplicate effects; split monolithic player | Existing progress preserved; 100 rapid taps deterministic; no crashes or lost updates             |
| P1: **Free Life vertical slice**       | New HUD/dock, age-up, 4 complete career steps, education, social and money loops, event follow-ups                     | 30-minute complete playable life arc; repeat runs meaningfully distinct                           |
| P2: **Story cinematic vertical slice** | Staged café + 2nd location, 2 cutout actors, 6 expressions, dialogue dock, scene transitions, sound                    | 10-minute polished chapter; all paths and mobile layouts tested                                   |
| P3: source library                     | Rights manifest, metadata importer, Twine/ink compiler subset; adapt 3-4 shorter works, add reviewed art               | 100% rights-reviewed shipped assets; reviewed chapters playable from beginning to end             |
| P4: expand both modes                  | Wider life ages, work/relationships/family/economy; 4-6 edited adapted story arcs and UGC-ready schema                 | Both modes equally supported; retention sessions show no dead-end mechanics                       |
| P5: Creator Studio                     | Graph editor, staging/pose tracks, effect GUIs, packaging, safe import/export                                          | New writer creates and plays a complete chapter without modifying JSON                            |
| P6: moderated catalog                  | Accounts, review, search, store, CDN, security, analytics/privacy                                                      | Creator uploads allowed only after review, abuse/copyright/age policy and tested package rollback |
| P7: native/public beta                 | Phone builds, signed artifacts, accessibility, localization, performance, hosting, privacy and app-store compliance    | Native QA, crash analytics, player feedback, explicit launch approval                             |

**Recommended staffing:** One lead developer + code agent can rebuild logic and CI, but artwork, animation, writing, licensing, QA and moderation remain significant independent disciplines. Commission or art-direct a _small consistent visual kit_ rather than trying to generate thousands of mismatched portraits.

**Priority order:** Fix basic game feel and the two 10-minute vertical slices **before** bulk importing books. Otherwise LIVEIT will have a huge library that still looks and plays like a document reader.

## Immediate Codex-ready first milestone

1. Snapshot current main and branch `feat/gamefeel-p0`.
2. Add tests for action idempotence, save queue races, stale closures, scene resume and player-visible life progression; record screenshots/performance baseline.
3. Extract controller/store/navigation from `App.tsx` without changing narrative/economic results.
4. Implement a dedicated Free Life Age-Up scene and one complete Job → Interview → Salary → Promotion chain.
5. Build full-screen Story Player stage with anchored choices while preserving current content and save schema; insert actual two-actor illustration/pose placeholders only when art is available.
6. Verify iOS/Android JS bundles, responsive Playwright interactions, rapid tap harness, color/contrast and accessibility labels.
7. Compare gameplay visually to prior build and use qualitative user playtesting; do not merge based solely on TypeScript checks.
