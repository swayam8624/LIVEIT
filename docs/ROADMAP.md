# LIVEIT Roadmap and Verified Implementation

## Working systems

- Single deterministic simulation core, validated story graphs and restricted consequences.
- Timeline-isolated standalones and Free Life with versioned, backwards-compatible offline saves.
- Five explorable isometric Bellweather neighborhoods; work, study, rest and social actions.
- Twenty original non-paywalled civic/social/career encounters, with two durable options apiece; outcomes persist as facts, memory events, and history.
- Career direction and neighborhood modifiers affect actual earnings, skills and wellbeing.
- Off-screen NPC life beats give Amelia and Noah distinct careers, emotions, ambitions, and milestones as game time advances.
- Two original story campaigns: the café reunion (seven scenes, three endings) and _A Place for Second Chances_ (11 scenes, three endings). The bookshop episode naturally unlocks after the reunion and a simulated week.
- Reusable offline image-backed cinematic stage, NPC portraits, accessible dialog choices.
- Interactive full-screen isometric city map with list-mode fallback, composed from 28 imported and SHA-verified Kenney CC0 icons/buildings/tiles.
- Standalone browser Creator Studio with branching, scene editing, local draft backup, JSON export and validated local player import.
- Unit tests, CI checks, web production builds, iOS/Android Hermes bundle exports and mobile/desktop Playwright screenshots.

## Current acceptance gates

- Story and city simulation choices deterministically yield valid save envelopes.
- All old v1 save files remain decodable, despite optional new city/NPC fields.
- Native iOS/Android _bundles_ export successfully, but signed binaries and device startup remain **unverified**.
- The game still has low-resolution original café/Amelia preview artwork; five Kenney isometric buildings are genuine game assets but **not yet a commercial art pass**.
- Community publishing is still local-only with no public creator accounts, moderation or takedown service.
- CI and screenshot evidence are attached to GitHub Actions and linked in PR #2.

## Next critical work

1. Upgrade to production-resolution original café/background/portrait and a rigged character animation system with reactions and art-direction reviews.
2. Extend city life beyond initial 20 encounters: more NPCs, schedules, housing, jobs, purchases and interwoven stories.
3. Use the actual narrative and consequence runtime in Creator Studio preview; add no-code conditions, character staging and robust graph visualization.
4. Implement author identity, story upload quarantine, immutable versioned packages, content moderation and copyright review before public creator onboarding.
5. Build account-based cloud sync with conflict detection, signed package distribution, anti-abuse limits and privacy policies.
6. Test physical Android and iOS devices (safe areas, performance, offline behavior, storage, accessibility); obtain developer credentials, stage TestFlight/Play internal testing and complete store requirements.
7. Expand localization and accessibility and create an actual player feedback program before any monetization.
8. Avoid ads, paid-choice gates, artificial energy timers and pay-to-win mechanics as formal game rules.

See [Open-source art and licensing policy](OPEN_SOURCE_ASSET_PIPELINE.md) and [production visual gates](IMMERSIVE_GAMEPLAY_GATE.md).

## Truthfulness standard

Passing unit tests and bundle exports does **not** mean the game is fully polished, publicly published, publicly moderated, or available in the app stores.
