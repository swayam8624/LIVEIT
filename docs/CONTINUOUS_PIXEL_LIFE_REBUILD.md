# LIVEIT · Continuous Pixel Life Rebuild (19 October 2026)

## Owner direction — source of truth

LIVEIT is a **2D pixel-sprite game**, never 3D and never an isometric
illustration masquerading as a controllable world. The free-life simulation,
authored stories, user-authored quests and dialogue share **one saved life**.
The playable map, not a dashboard, owns the phone screen.

This document tracks *implemented* code separately from *planned* features.

## Gameplay references actually inspected

- [Stardew Valley mobile gameplay walkthrough](https://www.youtube.com/watch?v=1KjG0wjK4ps):
  world-first layout, restrained upper-edge time/health panels, thumb
  control options and touch targets. Do **not** copy copyrighted art.
- [Stardew Valley mobile control options](https://stardewvalleywiki.com/Mobile_Controls):
  tap-to-move, invisible joystick, joystick + action combinations.
- [Eastward early gameplay](https://www.youtube.com/watch?v=skkXqfkcCwY):
  16-bit-density scenery, strongly authored locations, directional sprites,
  memorable NPC silhouettes, lighting and characters integrated into place.
- Moonlighter and CrossCode: fast spatial movement, legible contextual action,
  world-native quests, quick inventory/pause access.

Use these for interaction/design critique, not asset copying.

## Current delivered implementation in this branch

| System | Status | Concrete files / behavior |
|---|---|---|
| Game-first screen | Implemented initial slice | \`App.tsx\` uses \`ArcadePixelLife\` for Free Life. |
| Sprite actor | Implemented | 4-frame CC0 directional PNG sheets; optional **locally installed** Modern 24-frame art. |
| Game loop | Implemented | \`requestAnimationFrame\`, delta-time movement, GPU-style Animated transforms for player and camera. |
| Input | Implemented first pass | WASD/arrows; on-screen held directional pad and TALK. Touch pathfinding and gamepad pending. |
| World | Implemented small prototype | Connected street/café, expanded market, neighborhood and garden; deterministic tile collision. |
| Game clock | Implemented first pass | 60 active real minutes / one simulated calendar month; 12 monthly ticks / 365-day birthday; saves progress. |
| World economy | Basic | Monthly cost, employed wages, NPC ticks and relationship decay. Full per-shift work simulation pending. |
| NPC free text | Implemented adapter | Type or quick-prompts; local \`qwen3:0.6b\` through Ollama; if unreachable uses explicit authored responses. |
| Story integration | Implemented UI bridge | Story scenes open as an overlay over the paused Free Life world, choices applied to original life. |
| Custom missions | Implemented journal | Type title/objective, store in active life timeline, completion toggle, birthday expiration. |
| Original ZIPs | Partially integrated | CC0 Pulse sprites publicly bundled; noncommercial Modern installer makes local sprite override; raw restricted packs remain out of GitHub. |
| Validation | CI | \`npm run check\`, browser export and native Expo bundle are run in GitHub Actions; real device touch/perf QA still required. |

## Gameplay laws

1. **Time**: one **active** real-life hour crosses one in-game month.
   Clock pauses in menus/stories and continues when roaming; mobile apps in
   the background should not age the character. Twelve calendar months add
   to a birthday. Do not do 30 days of fake "rest" to move the calendar.
2. **Consequence**: model text is narrative, **not authoritative state**.
   Financial, relationship, medical, age, job and quest changes come only
   from validated, auditable domain events.
3. **Identity**: one appearance across overworld, creator and dialogue.
   Current optional local 24-frame avatars are a provisional directional
   sprite option; creator appearance-to-sprite mapping is NOT yet finished.
4. **Story**: mission progression does not reset the avatar or replace the
   main world. Outcomes should alter relationships, resources, world access,
   and long-term memory. The overlay is a temporary first implementation.
5. **Content safety / licensing**: public git may contain CC0 and genuinely
   redistributable authored art. A locally installed noncommercial pack
   stays local. Never assume GitHub public source makes downloaded sprites
   redistributable.
6. **Performance**: a constantly advancing frame loop does not guarantee
   60/120 FPS. Measure frame times on iPhone/Android and profile GPU/CPU.
   Render *only* visible map chunks before expanding to a big city.

## Priority implementation queue

### P0 — game must be playable (initial implementation in this branch)
- Game fullscreen, camera and world independently redraw, responsive touch
  movement, correctly sized/animated pixel sprite, connected café portal,
  one timeline, saved location and time, free text NPC panel, custom missions.
- Acceptance: perform 5min roaming with zero softlocks, save/relaunch,
  dialogue persist, no positional jumps, all old saves still decode.

### P1 — AAA-quality 2D visual language / mobile touch
- Pixel atlas with 16px authored source grid, nearest-neighbor sampling,
  Y-sorted sprites/occlusion, trees and buildings with shaded roofs, layered
  foreground props, real parallax, tile-edge autotiling, indoor shadows.
- Expanding/chunk-streamed streets + 5 districts + buildings, automated
  navigation to doors, footstep sounds, ambience, weather and day/night.
- Virtual joystick centered around thumb, action prompt based on proximity,
  mobile landscape/portrait and safe area support; gesture and gamepad parity.
- Character creator mapped to pixel skin/hair/outfit/face/body/ages and
  directional animated walk/idle/sit cycles, cosmetics retained through aging.
- Acceptance: capture side-by-side true device gameplay against design
  references, profile P95 frame time, hot-reload and 30-min gameplay test.

### P2 — the free-life system becomes gameplay
- Continuous jobs, wages, groceries, rent, health, schooling, friendship,
  social events, dating, shops, travel, family and aging by age-relevant bands.
- NPC schedules and persistent emotional/social memory, not repetitive
  generic assistant conversations.
- Dialogue-to-intent validation: NPC replies may PROPOSE action but cannot
  secretly mint cash, facts or relationship changes.
- A proper journal of missions, ongoing quests, failed quests, rewards and
  unique endings that alter the next monthly state. Mission compiler maps
  text to whitelisted goal predicates and events.
- Birth-to-death timeline, generation/legacy saves, age gating and memories.

### P3 — creator and narrative ecosystem
- Author quests and multi-hour stories as bundles for the shared Free Life
  world; age, season, location, inventory, relationships and previous
  choices become scene conditions. Branches affect ordinary play.
- NPC authoring, local LLM memory compression and lore reference retrieval,
  deterministic scripted failover, streaming dialogue, safety filters,
  offline performance budgets and user-generated episodic missions.
- Creator Studio live preview shows the *same* renderer/map and player
  identity; no disconnected "Episode-like" web cards.

### P4 — release hardening
- iPhone and Android device lab, measurable 60Hz target, optional 120Hz
  target where available (no blanket guarantee), thermal throttling,
  save crash recovery, disk-space budgets, privacy and model LAN discovery.
- Accessibility, localization, content moderation, security, licenses
  for each ZIP/media source, public open-source asset manifest.

## Local run — protect the existing messy worktree

Do not reset, pull over, or checkout branches inside a dirty original tree.

\`\`\`bash
cd "$HOME/Desktop/projects"
git clone --single-branch --branch feat/liveit-continuous-pixel-life \
  https://github.com/swayam8624/LIVEIT.git living-universe-new-pixel
cd living-universe-new-pixel
npm ci
npm run web -w @living/player -- --clear
\`\`\`

Optional **personal, noncommercial** Modern character sprites:

\`\`\`bash
python3 tools/install_private_pixel_art.py --source "$HOME/Downloads"
npm run web -w @living/player -- --clear
\`\`\`

If using a connected mobile device, set the game's LOCAL AI URL to the Mac's
LAN address with Ollama configured to listen there. \`localhost\` on iPhone
is the iPhone, not the Mac.

\`\`\`bash
ollama pull qwen3:0.6b
ollama serve
\`\`\`

Avoid \`npm audit fix --force\` until dependencies have been reviewed.
