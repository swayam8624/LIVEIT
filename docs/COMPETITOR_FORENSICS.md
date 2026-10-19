# LIVEIT competitor forensics: research ledger and reconstruction targets

Last reviewed: 2026-10-18. The following observations are grounded in **public app listings, official docs, and app help articles**, not in claims that full YouTube playthroughs or private app code were already accessed. A later agent must watch/annotate actual long-form gameplay recordings and test app builds before marking a gameplay sequence "verified by observation."

## Research evidence hierarchy

1. Directly operated app with version/device/date, sanitized screen recording and step-by-step state changes.
2. Full-length YouTube gameplay with creator/title/URL/date and inspected timestamp ranges.
3. Official developer documentation, app-store description, help articles or product announcements.
4. Multiple independent current community reports (treat claims as subjective until reproduced).
5. Inference/hypothesis, always marked **unverified**.

Record for each feature: source, build/version, timestamp or documentation heading, preconditions, input gestures, UI latency, animation/audio, world-state mutation, persistence after kill/restart, error/loading/empty state, social/server behavior, business model, observed anti-patterns, original LIVEIT implementation approach, design difference, code path and automated plus manual acceptance test.

No claim that a game feature has been reverse-engineered "to bits" until user-visible behavior and edge cases have been documented. Never scrape private accounts, violate paywalls, use leaked source, extract protected app assets, evade anti-bot/rate-limits, copy protected art or bypass DRM.

## Verified reference catalog

### BitLife — life simulator spine

- Official Google Play: https://play.google.com/store/apps/details?id=com.candywriter.bitlife
- Public description claims birth-to-death life, year-by-year events, careers, marriage/family, health, reputation, crime, fame and wealth.
- Investigation targets: birth country/family/traits, age increment, screen hierarchy and activity categorization, timing of single/multiple events, school lifecycle, education gates, employment ladders, interviews, earnings/expenses, romance/family tree, assets/investing, medical care, legal systems, death/obituary, achievement/legacy and challenges.
- Capture **25 separate seeded playthrough journeys**, not 25 screenshots. At least five each: straight career, crime/legal, family/dynasty, finance/business, unconventional lifestyle. Measure clicks to meaningful decision, age progression speed and specific long-term consequences.
- Original LIVEIT differentiation: authored cinematic decisions genuinely change the same simulation record; friends and AI personas must know witnessed events.

### Episode — cinematic and player-created story language

- Episode help center: https://pocketgems-support.helpshift.com/hc/en/10-episode-writer-s-portal/section/84-writing-directing/
- Official character animation: https://pocketgems-support.helpshift.com/hc/en/10-episode-writer-s-portal/faq/255-basic-directing-character-animation-overview/
- Placement/layers: https://pocketgems-support.helpshift.com/hc/en/10-episode-writer-s-portal/faq/317-advanced-directing-layers/
- Tutorial video collection: https://www.episodelife.com/p/tutorials (third-party tutorial index; videos must be individually verified).
- Grounded concepts: characters occupy layered stage positions, enter/exit, gesture alongside dialogue, camera pans/zooms, overlays, conditional branching, character points, timed choices, outfit/appearance selection, user-created story authoring and on-device playtest.
- Record **10 entire chapters** and timing: scene transition, text speed, tap-to-advance, camera blocking, acting beats, wardrobe, body-language changes, animations starting and ending, chapter forks, premium prompts, and end-of-chapter hook. Never reuse their scripts, style assets, proprietary animations or visual trademarked layouts.
- LIVEIT bar: two fully animated original characters, 12+ meaningful emotions, idle/blink/breath, eye direction, rigged clothing, camera positions and expressions changing **as dialogue progresses**, not static cards with a background.

### AnonChat — real-player conversation mechanics

- First-party: https://anonchat.com/
- Play Store: https://play.google.com/store/apps/details?id=io.anonchat
- Public features: find stranger, anonymous identity, persistent friend request, typing/presence, text/voice/photo/calls, erase/edit messages, interests, ongoing conversations, no-match outcomes. First-party says 18+, and notes it has renamed its iOS app due to Apple guidelines.
- Record connect-queue, search matching/cancel, mutual connection, reconnect, blocking, reports, typing indicators, read receipts or their absence, history deletion, profile reveal and requeue. Do not confuse "no visible name" with untraceability to operators.
- Important: Apple App Review Guideline 1.2 says apps used primarily for random/anonymous chat do not belong in the App Store. LIVEIT's store-distributed game must not be an anonymous-chat roulette clone. Instead design adult-only opt-in **contextual multiplayer interactions tied to life/story gameplay**, and get policy review before launch. No underage stranger matching.

### zeta — AI-character plot/creator loop

- Official Apple listing: https://apps.apple.com/us/app/zeta-ai-chat-story-play/id1619030760
- Official Play listing: https://play.google.com/store/apps/details?id=com.scatterlab.messenger
- Public features: discover chat characters/plots, create public/private personas, roleplay dialogue, suggested replies, AI-generated image snapshots, continuity and creator discovery. Unlimited/free messaging is an advertised product characteristic, not a guarantee that another product has the same costs.
- Evaluate 20 persona categories including original non-romance personalities, branching story scenes, length controls, character creation fields, conversation reset, editing/retry, error and network states, user-owned visual snapshots, latency and retention.
- LIVEIT difference: AI characters inhabit the existing deterministic world; responses must respect known facts, travel, calendar and relationships. Do not claim memory simply because past messages exist.

### Character.AI — persona consistency and user controls

- Official memory announcement (2026): https://blog.character.ai/memory/
- Official pinned memories: https://support.character.ai/hc/en-us/articles/24327914463003-Pinned-Memories
- Official voice/calls: https://support.character.ai/hc/en-us/articles/23957274129691-Character-Calls-Voice-FAQ
- Features documented publicly: pinned messages, story memory/facts, chat history, voice, character creation and controls.
- Investigate prompt/persona setup, first-message design, chat discoverability, regeneration, edit/retry, memory management, pinned facts, roleplay formatting, moderation, feedback, group conversations, voice UX and long-session performance.
- Memory tests: 200 turns, 20 planted private facts, indirect recall, contradiction resolution, secret knowledge scope, offline access and 60-day simulated time passage.

### OpenLife — permitted mechanics reference

- Archived mirror: https://github.com/WinFan3672/OpenLife
- Its README redirects to: https://codeberg.org/WinFan3672/OpenLife
- User separately supplied https://codeberg.org/OpenLife/OpenLife.git ; verify owner and current upstream commit before equating versions. Archived mirror's MIT license permits reuse with notices, but its single 9k+ line Python terminal app must not become LIVEIT's engine architecture.
- See docs/OPENLIFE_REVERSE_ENGINEERING.md for mapping of player/family/jobs/investing/housing/health/justice and preservation concerns.

## Video-study operational protocol — not yet completed

The AI coding agent must search YouTube for public, permitted, **actual in-app** long-form sessions for every reference product (filter out generic marketing slides, unrelated apps sharing similar names, and out-of-date UI). Research at least three credible full playthroughs per product, plus short specialist tutorials for difficult features; retain URLs and creator names, publication date, timestamps and exact observations in docs/research/VIDEO_LEDGER.md. Preference order: 2026 current build, 2025 recent build, historical technique references clearly labelled. Sample chronological gameplay at key decision transitions; a frame alone is insufficient to infer the backend.

For each source document:

- 00:00–... initial onboarding, first valid input, permission prompts and default state
- Character creation: appearance subcategories, animation and actually persistent appearance after relaunch
- Core repeated 10-minute session: every meaningful choice, immediate feedback, time/scene progression
- Explore hard-to-reach routes, negatives, denied permissions, no network and insufficient resources
- Design measurements: touch targets, screen hierarchy, text density, feedback latency, motion timing, readable caption contrast, sound/haptic cues (observed, not guessed)
- How the experience stays compelling: anticipation, goal, surprise, player agency, consequences, reward and replay
- Exact LIVEIT acceptance test linked to each observed pattern, tagged inspired-by versus original

If a video cannot be accessed, say "unobserved" and rely on first-party product documentation until direct recording becomes available. Never hallucinate a watched timestamp or reverse engineered private implementation.

## Apple/transport constraints that affect game design

- Apple review guideline: https://developer.apple.com/app-store/review/guidelines/
- Apple's October 16, 2026 update: https://developer.apple.com/news/?id=92th7e5i
- iOS HTTP/3 and QUIC testing guidance: https://developer.apple.com/documentation/technotes/tn3102-http3-in-your-app
- Private, adult-oriented romance is not a license for exploitative or nonconsensual sexual content. Block/report, child safety, transparent model labeling, account deletion and opt-in social privacy are core.
- Do not use QR/hidden configuration to conceal prohibited functionality from app review. Separate distribution rules must be evaluated openly.

## First-principles synthesis

Do **not** bolt together five separate mini apps. Player character, life log, story episode, NPC facts, long-term AI memory and player-to-player connections must share coherent domain identities and consequences. Every module must have a user interaction, real state transition, offline/online error path, visual effect, persistence, metrics and a test. A feature is not complete because a React component rendered or a button incremented a number.
