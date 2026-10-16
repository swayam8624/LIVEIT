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

Start with [the specification](docs/PRODUCT_SPEC.md) and [architecture](docs/ARCHITECTURE.md). The project is private and unlicensed pending an owner decision; no open-source license has been selected implicitly.

## Cinematic design branch

The `design/immersive-gameplay-v1` branch is a preview of the new game-like presentation. It includes a bundled illustrated café stage, tappable destinations in Free Life, character portraits, visual-novel dialogue overlay and a significantly more usable Creator Studio. The scene plate is a deliberately compressed placeholder, so expect visible blur rather than final game artwork.

To inspect this preview on your own machine:

```sh
git fetch origin
git switch design/immersive-gameplay-v1
npm ci
npm run dev
# In another terminal: npm run dev:studio
```

Production art, layered rigged actors, multiple distinct city locations, user-upload publishing, cloud saves, native-device QA, and moderation are still in progress. See [immersive gameplay production gates](docs/IMMERSIVE_GAMEPLAY_GATE.md). Do not deploy this branch to paying users or merge it into production on the strength of bundle exports alone.
