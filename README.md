# LIVEIT

A shared life simulator and interactive story engine. Foundation Sprint 001 implements **A New Beginning**: a new life in Bellweather and an unfinished conversation with Amelia.

## Run

Requires Node.js 22.13+ and npm 10+. From this directory:

```sh
npm ci
npm run dev          # Expo web player: http://localhost:8081
npm run dev:studio   # Next.js Creator Studio: http://localhost:3000
```

Run each development server in its own terminal. For native development:

```sh
npm run ios          # Expo starts and opens the iOS simulator; requires macOS + Xcode
npm run android      # Expo starts and opens an Android emulator; requires Android SDK
npm run start -w @living/player  # QR / device connection and platform shortcuts
```

A compatible Expo Go installation or a development build and reachable development server are required for physical devices. Native distribution is not configured. The current Expo SDK and its supported native runtimes must match. Web and native use the same React Native app and pure TypeScript engines. Native device behavior has not been verified in this sprint.

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

Free Life is now best played by choosing a destination, spending time working/studying/socializing/resting, opening the city encounter when a new opportunity appears, and making one of the event's trade-off decisions. Events appear as *game time* advances: there are no ads, energy, paid-choice gates or real-time waiting.

Free/open graphics in this branch are **actually bundled and pinned**:
- 4 Kenney CC0 UI control icons;
- 15 Kenney CC0 city tile pieces;
- 9 Kenney CC0 isometric building pieces (5 currently visible in the main city map).
All 28 source assets have exact Git blob hashes, pinned upstream commit information and credits in `assets/kenney_ui_provenance.json` and `assets/kenney_city_provenance.json`. Source files remain owned by their respective original authors; the LIVEIT repository itself is not automatically CC0.

Do not merge or publish without green foundation checks, visual screenshots and a review of original asset rights. Physical iOS and Android devices are still untested. The public creator marketplace, remote accounts, UGC moderation, full-body rigs, advanced story editing and real store distribution have not yet been implemented.

See [open-asset intake policy](docs/OPEN_SOURCE_ASSET_PIPELINE.md) for adding legitimate free content.
