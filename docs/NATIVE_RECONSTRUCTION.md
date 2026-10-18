# LIVEIT Native-First Reconstruction Contract

**Status:** engineering program, not a claim of a finished product. Updated 2026-10-18.

## Product decision

LIVEIT is an **iOS/Android game**. The Expo web export and separate Next.js Creator Studio may remain temporary developer/test harnesses; they are **not** a web product or launch surface. Build and test iOS simulator first on the owner's Mac, then a physical iPhone and Android emulator/device. No app-store launch until store review conditions and human/social safety gates pass.

Preserve and progressively replace the existing TypeScript deterministic simulation/story/save packages. Do **not** rewrite everything into Unity before demonstrating a production-quality mobile vertical slice: that would discard verified save compatibility and delay gameplay. For richer scenes, evaluate a native animated rendering layer (Skia/Reanimated/Rive or a dedicated renderer) on real devices before choosing an engine migration. Keep one real game state and never use a web view as the main life UI.

## Exact player experience

1. Start a life at birth with a country/city, family and inherited traits. Early years have real parental/school events; user is not forced into an identical 23-year-old city start.
2. Advance one year and see an engaging timeline of 1–4 conditional, age-appropriate, non-repeated situations. Meaningful branching consequences modify family, school, jobs, wealth, health, friends and story route conditions.
3. Choose activities with opportunity cost and risk, not stat-spam. Profession gates require actual qualifications; salaries, loan repayments, inflation, housing expenses and childcare settle once per year.
4. Open Episode-like full-screen scenes with original characters animated using layered parts, motion tracks, costumes, lighting, camera direction, sound/haptic cues, dialogue history and replayable choices.
5. Speak to named AI characters whose response references facts they could know and who remember promises, relationship state and previous interactions across chapters/years.
6. Opt into pseudonymous, contextual social interactions with **real** players; do not fabricate online activity or disguise AI fallback as a real person. Friend/reveal/block/report actions must be real server operations.
7. At death, generate an authentic life recap, legacy choices, optional continuation as an heir and unlock progression.

## Architecture targets

```text
apps/player/                     Expo native shell, production mobile views
  src/features/{onboarding,life,stories,people,assets,ai-chat,social,legacy}/
packages/simulation-core/        pure TypeScript state transitions + seeded director
packages/world-schema/           schema and versioned migration rules
packages/narrative-core/         validated route/scene/choice/condition graph
packages/save-system/            transactional offline save coordinator
packages/memory-core/            local SQLite, episodic/semantic/reflection retrieval
packages/network-contracts/      versioned client/server schemas
services/gateway/                TypeScript server: auth, matching, relay, LLM proxy
services/moderation/             detection, reports, review, appeals and audit
content/                         edited, licensed events, routes, art provenance
tools/                           seeded stress simulator, balanced economy harness
```

Add testable interfaces for storage, clock, RNG, event bus and AI provider. Data packs must be validated before installation. Avoid another god-object `App.tsx`.

## Mobile integration and storage

The current React Native project already supports Expo iOS and Android bundle generation, but bundle generation is not simulator installation. On macOS with Xcode and a booted iOS simulator:

```sh
git switch feat/native-life-economic-foundation
npm ci
npm run check
npm run ios -w @living/player
```

If Expo does not automatically launch a device, boot an iPhone simulator with Xcode → Open Developer Tool → Simulator, then run the command again. For an actual native Xcode compilation use `npx expo run:ios` inside `apps/player`; this creates native project files, runs CocoaPods, builds with Xcode and installs on an appropriate simulator. Be deliberate about checking in generated ios/android folders. Repeat startup, choices, save, app force-close/relaunch, airplane mode, Accessibility Large Text and rapid-tap consistency on the simulator. A real iPhone hardware acceptance pass is still mandatory.

Long-term memory belongs in **local SQLite** (facts, episodes, vector embeddings, relationships, chat sessions) with backups controlled by the player. Memory retrieval must never expose private facts NPCs could not know. The mobile client must hold **no shared LLM API keys**, and LLM-generated state changes pass through an allow-listed effect interpreter.

## Chat, QUIC, and adults-only content

**Real players:** guest-to-verified upgrade; server-generated pseudonyms; interest/scene-based opt-in entry; content moderation; rate limits; message-level block/report; connection revoke; expiring server transcripts; data deletion/consent. Never claim a private anonymous room is magically untraceable: server account IDs are needed to enforce abuse controls. Never identify a real player to another without explicit mutual consent.

**Transport:** begin with server-relayed authenticated TLS WebSocket/HTTPS for messaging (simple, observable, reliable fallback); QUIC/HTTP3 on capable real devices is an optional transport implementation behind `IChatTransport`, not a replacement for authentication, encryption, moderation or application-level ordering. QUIC connection keys remain server-managed. Implement network interruption and resume with ordered per-room sequence numbers and idempotent sends. Always retain a fallback; no claim of QUIC until tested on hardware.

**AI characters:** local memory + model-provider abstraction + server-side proxy; configurable personalities and mature fictional dialogue for adults with consent/age verification. Do not add hidden app-review evasion switches. Prohibit any sexual content involving minors, exploitation, nonconsensual intimate material, grooming and deceptive impersonation. Store-distributed content must meet applicable Apple/Google policies. Adults-only preferences do not override store rules.

**Key external constraints (reviewed 2026-10-18):**
- Apple App Review Guidelines §1.1.4 restrict pornographic content; §1.2 warns about apps primarily used for random/anonymous chat and requires filtering, reports and blocks.
- Apple clarified restrictions against nonconsensual intimate images and hidden prohibited features on 2026-10-16.
- Google Play's AI content rules require in-app user reporting.
- Apple's HTTP/3 technote warns of simulator limitations. Test QUIC on real devices.

## Build gates (must all be demonstrable)

| Gate | Proof |
|---|---|
| A. Native bootstrap | Boot/launch on iOS simulator and Android emulator; no webview-as-game |
| B. Interesting life loop | Birth → school → job → relationship → assets → death/heir; minimum ten independently repeatable lives |
| C. Story | 15-minute complete expressive chapter, branching consequences across scenes, no placeholder portraits |
| D. Memory | 200-turn seeded recall/contradiction/knowledge tests; data persists after restart |
| E. Social | Two physical/simulated clients exchange real messages, block/report, disconnect/resume, handle no-match honestly |
| F. Services | Token auth, room isolation, message replay/idempotency, abuse throttling and privacy deletion in integration tests |
| G. Performance | 60 fps target, accessible controls, measured cold start and input latency on a mid-tier phone |
| H. Content | Rights-checked content, human-edited routes, replay analysis and legally sound art provenance |

The current branch's small asset feature **only** advances Gate B. Until D/E/F pass, neither AI chat nor anonymous chat should appear as fabricated "online" gameplay.
