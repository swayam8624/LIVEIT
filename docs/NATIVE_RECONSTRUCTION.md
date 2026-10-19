# LIVEIT Native-First Reconstruction Contract

**Status:** engineering program, not a claim of a finished product. Vision reconciled 2026-10-19. Graphics authority: [GDS-001](LIVEIT_GRAPHICS_DESIGN_SPEC_V1.md) → [GDS-002](LIVEIT_SCREEN_MODE_BLUEPRINT_V1.md) → [ENG-003](LIVEIT_RENDER_ENGINE_ARCHITECTURE_V1.md).

## Product decision

LIVEIT is an **iOS/Android game**. The Expo web export and separate Next.js Creator Studio may remain temporary developer/test harnesses; they are **not** a web product or launch surface. Build and test iOS simulator first on the owner's Mac, then a physical iPhone and Android emulator/device. No app-store launch until store review conditions and human/social safety gates pass.

Preserve and progressively replace the existing TypeScript deterministic simulation/story/save packages. Do **not** rewrite everything into Unity before demonstrating a production-quality mobile vertical slice: that would discard verified save compatibility and delay gameplay. The final visual choice is now a **shared native Vulkan/MoltenVK renderer** with two distinct passes: original top-down pixel tile/sprite Free Roam and truly rigged 3D characters/sets for significant dialogue and story scenes. Skia/Reanimated/Rive remain UI/fallback implementation options, not alternatives silently replacing that target. Adopt migration incrementally and only after the new screen passes physical-device and save-restoration acceptance. Keep one real game state and never use a web view as the main life UI.

## Exact player experience

1. Start a life at birth with a country/city, family and inherited traits. Early years have real parental/school events; user is not forced into an identical 23-year-old city start.
2. Advance one year and see an engaging timeline of 1–4 conditional, age-appropriate, non-repeated situations. Meaningful branching consequences modify family, school, jobs, wealth, health, friends and story route conditions.
3. Choose activities with opportunity cost and risk, not stat-spam. Profession gates require actual qualifications; salaries, loan repayments, inflation, housing expenses and childcare settle once per year.
4. Walk an original crisp top-down pixel town and interiors; on meaningful encounters transition to an Episode-scale **real 3D character stage** with skinned face rigs, genuine lighting and camera blocking. Keep shared outfit/age/identity, dialogue history, meaningful branching consequences and safe haptic/audio feedback. Do not assert the earlier 2.5D portrait prototype is production cinema.
5. Speak to named AI characters whose response references facts they could know and who remember promises, relationship state and previous interactions across chapters/years.
6. Opt into pseudonymous, contextual social interactions with **real** players; do not fabricate online activity or disguise AI fallback as a real person. Friend/reveal/block/report actions must be real server operations.
7. At death, generate an authentic life recap, legacy choices, optional continuation as an heir and unlock progression.

## Architecture targets

```text
apps/player/                     Expo native shell, accessible HUD + fallback
  src/features/{onboarding,life,stories,people,assets,ai-chat,social,legacy}/
packages/simulation-core/        pure TypeScript state transitions + seeded director
packages/world-schema/           schema and versioned migration rules
packages/narrative-core/         validated route/scene/choice/condition graph
packages/save-system/            offline save coordinator; durable revisions/idempotent action upgrades needed
packages/memory-core/            local SQLite, episodic/semantic/reflection retrieval
packages/network-contracts/      versioned client/server schemas
services/gateway/                TypeScript server: auth, matching, relay, LLM proxy
services/moderation/             detection, reports, review, appeals and audit
content/                         licensed pixel atlases, 3D rigs, authored stages, events and art provenance
native/liveit-render/            PROPOSED Vulkan shared renderer, tile/sprite and true 3D passes
apps/player/modules/liveit-render/ PROPOSED Kotlin/Swift/ObjC++ native Expo view
packages/world-schema/src/render-contract.ts EXISTING typed mode frame, intents, receipts
tools/                           seeded stress simulator, art pack pipeline and economy harness
```

Add testable interfaces for storage, clock, RNG, event bus and AI provider. Data packs must be validated before installation. Avoid another god-object `App.tsx`.

## Hybrid graphics native-integration gate

**Not implemented yet:** The native player must display real Vulkan frames from a single common C++ renderer, pixel atlas pass for everyday movement and a true skinned/mesh 3D cinematic pass for story/NPC dialogue. Android requires SurfaceView/ANativeWindow Vulkan swapchain; iOS requires CAMetalLayer/MoltenVK, portable extensions and verified XCFramework slices. Share the same typed frame ABI and appearance resolver; real text-input, report/block and accessibility remain RN semantic overlays. The current Vulkan PPM test is headless, not a phone graphics proof. See [ENG-003](LIVEIT_RENDER_ENGINE_ARCHITECTURE_V1.md).

**Navigation and saves:** Implement explicit persisted location/tile/facing/portal with old-save migration and collision before claiming Free Roam. Current UI is a district selector. Life/story domain stays authoritative; shaders cannot grant life effects. Haptic feedback and consequence widgets only confirm saved world effects. The fallback components remain until live native replacements work.

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

| Gate                     | Proof                                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| A. Native bootstrap      | Boot/launch on iOS simulator and Android emulator; no webview-as-game                                              |
| B. Interesting life loop | Birth → school → job → relationship → assets → death/heir; minimum ten independently repeatable lives              |
| C. Story                 | 15-minute complete expressive chapter, branching consequences across scenes, no placeholder portraits              |
| D. Memory                | 200-turn seeded recall/contradiction/knowledge tests; data persists after restart                                  |
| E. Social                | Two physical/simulated clients exchange real messages, block/report, disconnect/resume, handle no-match honestly   |
| F. Services              | Token auth, room isolation, message replay/idempotency, abuse throttling and privacy deletion in integration tests |
| G. Performance           | 60 fps target, accessible controls, measured cold start and input latency on a mid-tier phone                      |
| H. Content               | Rights-checked content, human-edited routes, replay analysis and legally sound art provenance                      |

The current branch still provides only a partial Gate B, an illustrated district chooser, a preliminary story player and headless Vulkan shader tests. A true pixel-walk/3D conversation combined visual release gate is **not yet met**. Until D/E/F pass, neither AI chat nor anonymous chat should appear as fabricated "online" gameplay.
