# LIVEIT

> **ACTIVE DIRECTION (19 Oct 2026): 100% PIXEL ART.** The owner retired **all** 3D graphics, 3D models, cinematic 3D actors, rigged meshes and glTF content. Both free-roam and emotionally rich dialogue/story scenes use original expressive layered 2D pixel art. [Pixel-only spec V2](docs/PIXEL_ONLY_DIRECTION_V2.md) overrides any stale 3D plans elsewhere in this repository. Current fallback is not yet a complete walkable pixel game.

## Import your downloaded ZIPs, pixel art and sounds

The built-in safe intake tool scans your Mac Downloads, has you approve each pack's actual license and public GitHub redistribution rights, then extracts supported assets into Git-tracked, source-attributed folders **without pushing raw ZIPs or 3D files**.

```bash
cd ~/Desktop/projects/living-universe
git fetch origin
git switch feat/native-life-economic-foundation
git pull --ff-only
npm run assets:intake -- --source "$HOME/Downloads" --scan
npm run assets:intake -- --review
npm run assets:intake -- --import-approved
git status --short
du -sh assets/imported
# Commit only after inspecting files and public redistribution terms:
git add assets/imported
git commit -m "assets(pixel): import approved sprites tiles UI and audio"
git push origin feat/native-life-economic-foundation
```

The local review report is in **assets/local-intake/reviews.json**, ignored by Git. If a source's raw files cannot legally be redistributed, do NOT approve it for the public repository. Originals remain in Downloads. PNG art is preserved losslessly, and if ffmpeg exists, WAV/OGG/FLAC sound is converted to mobile-readable AAC/M4A. Existing historic 3D inventory is **not an active target**.


An original native iOS/Android life simulator and interactive-story game. **Target art: pixel-crisp top-down everyday exploration, beautifully rigged 3D dramatic conversations and tactile accessible game HUD.** The current playable foundation includes Bellweather district selection and authored stories; the full walkable pixel/3D native renderer remains under construction.

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

## Current graphics target: pixel free-roam + true 3D conversations

**RETRO TO LIVE IN. CINEMATIC TO FEEL. TACTILE TO CONTROL.** The production rendering direction is original classic-handheld top-down **pixel** streets/interiors and NPC navigation for ordinary daily life, with **genuine smooth rigged 3D** cinematic dialogue, story chapters and significant life moments. The common character identity/appearance/age must remain consistent across modes. The UI is a responsive retro-futurist native game HUD with thumb controls, sidebars, contextual choices, "what changed" outcome widgets and meaningful haptics.

**Current runnable reality:** The existing React Native city view still shows **an illustrated isometric district selector** with zoom/lighting preview and real district/event choices. StoryPlayer still uses React Native illustrations. These are valuable FALLBACKS; the full pixel navigation, native GPU swapchain and 3D mesh-rig characters do **not** exist in the phone player yet.

Independent Vulkan C++/SPIR-V compute tests in [native/city-vulkan](native/city-vulkan) can render seed-generated 3D buildings and 2.5D actor illustrations into PPM files in software or hardware Vulkan. They validate shader execution, **not** a live Vulkan app viewport or production 3D rigged dialogue. The future shared renderer uses Android Vulkan and iOS MoltenVK and keeps accessible native HUD text.

**Follow the specifications in order:**

- [Step 1 · Final graphics bible](docs/LIVEIT_GRAPHICS_DESIGN_SPEC_V1.md)
- [Step 2 · All 43 screens and interaction states](docs/LIVEIT_SCREEN_MODE_BLUEPRINT_V1.md) and [browsable screen atlas](docs/design/LIVEIT_SCREEN_ATLAS.html)
- [Step 3 · Architecture and native implementation gates](docs/LIVEIT_RENDER_ENGINE_ARCHITECTURE_V1.md)
- [Current unified vision](docs/UNIFIED_VISUAL_ENGINE_VISION.md) and [art direction](docs/ART_DIRECTION.md)
- [Honest build status](docs/BUILD_STATUS.md)
- [Historical Vulkan city proof](docs/VULKAN_CITY_RENDERING.md)

For the only current independently runnable Vulkan proof:

    cmake -S native/city-vulkan -B build/city-vulkan
    cmake --build build/city-vulkan
    ctest --test-dir build/city-vulkan --output-on-failure

Do not describe this command as the game rendering inside an iPhone. For a proper native player run, use the iOS/Android commands above and separately confirm the actual installed view and actions.

## Original asset production catalog (Step 5)

The approved visual roadmap now includes a **machine-readable catalog of 1,481 PLANNED production work items**, including 400 separately named 3D rig parts, 200 distinct cinematic environments, 302 original top-down pixel tiles, 55 sprite families and the supporting HUD/audio/VFX/shader/camera library. Naming an asset in JSON does not create its actual geometry, sprite, sound or rights.

- [Art Production Bible — ART-005](docs/ASSET_PRODUCTION_BIBLE_V1.md): rigorous source formats, art direction, commercial rights intake, GPU conversion and QA.
- [Browsable 1,481-item asset atlas](content/production-assets/ASSET_ATLAS.html) — self-contained HTML; open locally to search, filter by production wave, inspect QA and isolate the first playable kit.
- [Catalog totals](content/production-assets/v1/catalog-index.json), [3D character inventory](content/production-assets/v1/characters-3d.json), [200 3D locations/props](content/production-assets/v1/locations-3d.json), [pixel world inventory](content/production-assets/v1/pixel-world.json) and [HUD/audio/camera/shader inventory](content/production-assets/v1/hud-audio-fx.json).
- [First playable Bellweather café kit](content/production-assets/v1/first-playable-slice.json): 110 planned starter work items, selected from the full catalog.
- [Actual current-repo asset audit](content/production-assets/v1/existing-repo-audit.json): 28 Kenney CC0 fallback PNGs, two tiny concept JPGs and 51 procedural prototype recipes, not a finished 3D or pixel production library.
- Validator: npm run assets:validate. Summary: npm run assets:summary. CI also runs the catalog regression tests.

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

This gameplay branch adds meaningful gameplay rather than a static mockup: an illustrated isometric neighborhood selector with five destinations, twenty authored choice events, a career direction, independent NPC life milestones, and **A Place for Second Chances**, a second original 11-scene / three-ending narrative connected to the Amelia reunion. Consequences modify trust, wellbeing, finances, skill, stress, reputation, connections, memories, and saved world history.

Free Life is now best played by choosing a destination, spending time working/studying/socializing/resting, opening the city encounter when a new opportunity appears, and making one of the event's trade-off decisions. Events appear as _game time_ advances: there are no ads, energy, paid-choice gates or real-time waiting.

Free/open graphics in this branch are **actually bundled and pinned**:

- 4 Kenney CC0 UI control icons;
- 15 Kenney CC0 city tile pieces;
- 9 Kenney CC0 isometric building pieces (5 currently visible in the main city map).
  All 28 source assets have exact Git blob hashes, pinned upstream commit information and credits in `assets/kenney_ui_provenance.json` and `assets/kenney_city_provenance.json`. Source files remain owned by their respective original authors; the LIVEIT repository itself is not automatically CC0.

Do not merge or publish without green foundation checks, visual screenshots and a review of original asset rights. Physical iOS and Android devices are still untested. The public creator marketplace, remote accounts, UGC moderation, full-body rigs, advanced story editing and real store distribution have not yet been implemented.

See [open-asset intake policy](docs/OPEN_SOURCE_ASSET_PIPELINE.md) for adding legitimate free content.
