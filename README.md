# LIVEIT

A shared life simulator and interactive story engine. Foundation Sprint 001 implements **A New Beginning**: a new life in Bellweather and an unfinished conversation with Amelia.

## Run LIVEIT on iPhone Simulator (primary development path)

LIVEIT is an **iOS/Android game**. The web player exists only as a temporary
developer/browser test harness, **not** the target shipping experience.
The simulator needs a Mac with Xcode, Node.js 22.13+ and npm 10+.

```sh
git pull
npm ci
npm run ios                            # Xcode-native compile + iPhone Simulator
```

If an iPhone simulator is not booted, launch one in Xcode → Open Developer
Tool → Simulator. This command uses `expo run:ios`, not Expo Go or a LAN `exp://` redirect.
It avoids the Expo Go `simctl openurl ... code 60` timeout that occurred with
the old `expo start --ios` script. The optional legacy `npm run ios:go -w
@living/player` uses localhost rather than a Wi-Fi IP and remains useful for
isolated diagnostics, not game acceptance. Check that an old Metro process is
not already occupying port 8081 with `lsof -nP -iTCP:8081 -sTCP:LISTEN`;
terminate **only the confirmed stale LIVEIT process** before running again.
If the simulator hangs, manually boot an iPhone in Xcode and inspect
`xcrun simctl list devices booted` and `xcodebuild -version`.
The
[macOS iOS native smoke workflow](.github/workflows/ios-simulator-smoke.yml)
now attempts to compile, install, launch and capture a real simulator screenshot.

Android (Android Studio emulator/SDK required):

```sh
npm run android -w @living/player
```

The existing internal `npm run dev` (Expo web at localhost:8081) and
`npm run dev:studio` (creator development tool at localhost:3000)
remain available for regression tests and content authoring; they are not
public game destinations or a claim of app-store publication.

For the new OpenLife-inspired portfolio and choice gameplay, see
[reverse-engineering audit](docs/OPENLIFE_REVERSE_ENGINEERING.md) and
[native rebuilding/QA contract](docs/NATIVE_RECONSTRUCTION.md).
The project is still in pre-alpha; the new domain gameplay does not yet
constitute a complete birth-to-death game or a working real-player chat platform.

## Autonomous reconstruction agent

Give a full-capability coding agent the repository-root [AGENTS.md](AGENTS.md).
Its mandate is to study public gameplay recordings, inspect legitimate source
mechanics, rebuild genuine native interaction flows, test them on installed
iOS/Android builds and keep shipping verified working software. The research
evidence/source catalog is [competitor forensics](docs/COMPETITOR_FORENSICS.md),
and the test-backed current-state ledger is [build status](docs/BUILD_STATUS.md).
These files are instructions and evidence logs, **not** claims the game is
finished or that all playthroughs have already been reviewed.

## REA-assisted native reconstruction

A full operating guide for the [morluto/rea](https://github.com/morluto/rea)
reverse-engineering toolkit is available in
[REA → LIVEIT playbook](docs/REA_RECONSTRUCTION_RUNBOOK.md). It covers setup
for Codex on the owner's Mac, Node/Java/decompiler requirements,
owned-build JS/Android/Apple inspection, permitted browser/network/SQLite
evidence, safe research boundaries, exact commands, and proof-driven
implementation. Its findings feed into
[research templates](docs/research/REA_TARGETS.md) and the existing
[build-status ledger](docs/BUILD_STATUS.md). These are instructions;
installation, outside-app decompilation and full game parity are not claimed.

## Vulkan 3D city and retro-game UI

Bellweather now has a **deterministic 3D city geometry model** and a more
game-like, midnight/mint/amber native player theme. The offline iPhone/Android
map has functional zoom, day/night preview, current game-day display,
event hotspots and district navigation.

An independently buildable **Vulkan compute city renderer** is in
[native/city-vulkan](native/city-vulkan). Its shader generates genuine day and
night 3D city preview images through Vulkan, with a headless Mesa CI smoke test.
The [full native integration contract](docs/VULKAN_CITY_RENDERING.md)
explains the next surface/view bridge work. **Current mobile Free Life still
uses the React Native illustrated fallback, not a live Vulkan swapchain**;
we do not claim an in-app native Vulkan view is complete.

## Play the slice

1. Choose a name and pronouns, then **Begin your life**.
2. Choose work, learning, socializing, or rest. Each action advances 1, 7, or 30 simulated days, including living costs. Learning opens steady employment at 25 experience; then working secures the position.
3. Select **Meet Amelia**, choose an approach, and finish the reunion. Apologizing and telling the truth raises trust from 35 to 57. More guarded choices lead to different memories and endings.
4. Return to Free Life and open **Your journal**. The relationship and memories persist in the main timeline. Reload to verify the saved life.
5. In **Story Mode**, begin an independent campaign, leave mid-scene, resume, finish, and replay another branch. Its consequences never alter the main life. You can continue simulating life in the story continuity and switch back to your main life.
6. Open Creator Studio to edit dialogue, scene mood, speakers, branching choice labels/destinations and preview different paths. Import/export validated JSON or return to a locally saved draft. Public publishing into the player is not yet implemented.

The story is a short functional demonstration, not yet the blueprint's intended polished 10–20-minute experience. This design branch uses original AI-assisted, bundled low-resolution concept artwork for the café and Amelia's portrait, and retains offline play without any runtime AI service or paid choices. These previews are not final layered character rigs or commercial production art.

## Verify

```sh
npm run check          # Prettier check, ESLint, strict TypeScript, Vitest
npm run build:player   # Expo web export → apps/player/dist
npm run build:studio   # Next.js production build
npm run format         # Apply formatting
```

See [verification evidence](docs/VERIFICATION.md) for actual commands, outcomes, and device limits. CI runs checks, web and Studio production builds, plus native iOS and Android Expo bundle exports on Node 22. Exports do not replace physical-device or simulator smoke tests.

## Structure

| Directory                     | Responsibility                                                            |
| ----------------------------- | ------------------------------------------------------------------------- |
| `apps/player`                 | Expo player for web, iOS, Android                                         |
| `apps/creator-studio`         | Next.js local authoring and validation                                    |
| `packages/world-schema`       | Validated world, character, relationship, memory, event, progress data    |
| `packages/story-schema`       | Restricted versioned story format and graph validation                    |
| `packages/simulation-core`    | Deterministic day ticks, finances, skills, friendships                    |
| `packages/consequence-engine` | Atomic validated effect application                                       |
| `packages/narrative-core`     | Scene progression, conditions, choices, endings                           |
| `packages/save-system`        | Async storage contract, save envelope, timeline branching                 |
| `content`                     | Original reunion story shared by the runtime and Studio                   |
| `docs`                        | Specification, architecture, art standard, backend design, roadmap        |
| `tests`                       | Engine, compatibility, persistence and untrusted-content regression tests |

Start with [the specification](docs/PRODUCT_SPEC.md) and [architecture](docs/ARCHITECTURE.md). The repository is currently public, but the original LIVEIT code and story content have **not** been explicitly offered under an open-source license; do not assume they are reusable. Third-party Kenney assets have their own CC0-1.0 terms documented in `assets/`.

## Cinematic gameplay

The cinematic interface overhaul is merged into `main`. This project also has a separate `feat/living-city-systems` development branch adding five explorable districts, deterministic encounters, NPC autonomy, a second original story, and verified CC0 artwork. It includes a bundled illustrated café stage, tappable destinations in Free Life, character portraits, visual-novel dialogue overlay and a significantly more usable Creator Studio. The scene plate is a deliberately compressed placeholder, so expect visible blur rather than final game artwork.

To inspect this preview on your own machine:

```sh
git fetch origin
git switch feat/living-city-systems
npm ci
npm run dev
# In another terminal: npm run dev:studio
```

Production art, layered rigged actors, multiple distinct city locations, user-upload publishing, cloud saves, native-device QA, and moderation are still in progress. See [immersive gameplay production gates](docs/IMMERSIVE_GAMEPLAY_GATE.md). Do not deploy this branch to paying users or merge it into production on the strength of bundle exports alone.

## Install original high-resolution concept art

The GitHub branch includes tiny offline preview images so the player can build
without downloading asset libraries. For the substantially sharper original
concept pack, download `LIVEIT_Original_Concept_Art_Pack_v1.zip` from the
project conversation and run:

```sh
python3 -m pip install Pillow
python3 tools/install_concept_art.py ~/Downloads/LIVEIT_Original_Concept_Art_Pack_v1.zip --confirm-rights
npm run check
npm run build:player
```

The script installs optimized JPEGs into `apps/player/assets`, records hashes
and source references in `art-provenance.json`, and preserves the original ZIP.
Inspect responsive crops before you commit generated images. This is still
concept artwork, not a transparent modular character rig, and native devices
still require hands-on tests. Only use materials whose terms you have verified.

## Expanded Bellweather gameplay (living-city branch)

This gameplay branch adds meaningful gameplay rather than a static mockup: an explorable isometric neighborhood map with five destinations, twenty authored choice events, a career direction, independent NPC life milestones, and **A Place for Second Chances**, a second original 11-scene / three-ending narrative connected to the Amelia reunion. Consequences modify trust, wellbeing, finances, skill, stress, reputation, connections, memories, and saved world history.

Free Life is now best played by choosing a destination, spending time working/studying/socializing/resting, opening the city encounter when a new opportunity appears, and making one of the event's trade-off decisions. Events appear as _game time_ advances: there are no ads, energy, paid-choice gates or real-time waiting.

Free/open graphics in this branch are **actually bundled and pinned**:

- 4 Kenney CC0 UI control icons;
- 15 Kenney CC0 city tile pieces;
- 9 Kenney CC0 isometric building pieces (5 currently visible in the main city map).
  All 28 source assets have exact Git blob hashes, pinned upstream commit information and credits in `assets/kenney_ui_provenance.json` and `assets/kenney_city_provenance.json`. Source files remain owned by their respective original authors; the LIVEIT repository itself is not automatically CC0.

Do not merge or publish without green foundation checks, visual screenshots and a review of original asset rights. Physical iOS and Android devices are still untested. The public creator marketplace, remote accounts, UGC moderation, full-body rigs, advanced story editing and real store distribution have not yet been implemented.

See [open-asset intake policy](docs/OPEN_SOURCE_ASSET_PIPELINE.md) for adding legitimate free content.
