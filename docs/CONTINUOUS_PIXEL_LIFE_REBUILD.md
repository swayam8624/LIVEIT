# LIVEIT · Continuous Pixel Life Rebuild (19 October 2026)

## Owner direction — source of truth

LIVEIT is a **2D pixel-sprite game**, never 3D and never an isometric
illustration masquerading as a controllable world. The free-life simulation,
authored stories, user-authored quests and dialogue share **one saved life**.
The playable map, not a dashboard, owns the phone screen.

This document tracks _implemented_ code separately from _planned_ features.

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

| System            | Status                      | Concrete files / behavior                                                                                                                                                     |
| ----------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Game-first screen | Implemented initial slice   | \`App.tsx\` uses \`ArcadePixelLife\` for Free Life.                                                                                                                           |
| Sprite actor      | Implemented                 | 4-frame CC0 directional PNG sheets; optional **locally installed** Modern 24-frame art.                                                                                       |
| Game loop         | Implemented                 | \`requestAnimationFrame\`, delta-time movement, GPU-style Animated transforms for player and camera.                                                                          |
| Input             | Implemented first pass      | WASD/arrows, held thumb-pad, tap-to-walk with BFS obstacle avoidance, tap an NPC to approach for conversation. Gamepad pending.                                               |
| World             | Implemented small prototype | Connected street/café, expanded market, shops, housing and gardens; camera-local tile culling; layered terrain/props and shaded building signage.                             |
| Game clock        | Implemented first pass      | 60 active real minutes / one simulated calendar month; 12 monthly ticks / 365-day birthday; saves progress.                                                                   |
| World economy     | Basic                       | Monthly cost, employed wages, NPC ticks and relationship decay. Full per-shift work simulation pending.                                                                       |
| NPC free text     | Implemented adapter         | Type or quick-prompts; choose local \`qwen3:0.6b\`, \`qwen3:1.7b\` or \`qwen3:4b\` through Ollama; if unreachable uses explicit authored fallback.                            |
| Story integration | Implemented UI bridge       | Story scenes open as an overlay over the paused Free Life world, choices applied to original life.                                                                            |
| Custom missions   | Implemented first pass      | Type title, pick validated in-world goal, complete by real travel/talk/month events or manually, choose birthday/five-year/lifetime expiry, store in current life.            |
| Original ZIPs     | Partially integrated        | CC0 Pulse walk sheets bundled; private Modern installer optionally adds Adam/Alex/Bob/Amelia pixel walk cycles; nonredistributable raw packs remain off GitHub.               |
| Validation        | CI                          | \`npm run check\` and web/Studio export run in GitHub Actions. iOS simulator and physical-device FPS/gesture QA are separate and must be confirmed before claiming readiness. |

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
   Render _only_ visible map chunks before expanding to a big city.

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
- Creator Studio live preview shows the _same_ renderer/map and player
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

### Verified gameplay interaction rules (new)

- **Walk/tap to go:** the pathfinder is tested against logical terrain,
  walls and NPC collision. Tapping Amelia routes to an accessible adjacent
  tile. The target can be abandoned at any time by using the joystick/keys.
- **Context action:** inside the café buy a £4.50 drink (+2 wellbeing);
  in the market take a £35 gig (+1 skill, -2 wellbeing); in the gardens
  rest (+5 wellbeing). Each type is capped at one per virtual day. This
  runs through the validated life domain and existing save, _without_ fake
  aging per button press.
- **Missions:** validated goals become complete only after travel,
  talking, work discussion or an actual month tick. Completion always
  affects the same active life. Arbitrary written mission objectives can
  be manually marked, never auto-completed by model hallucinations.
- **Dialogue:** local Ollama qwen3 supports ongoing typed turns and saves
  recent history. Its output cannot directly modify finances/age/quests.
  On iOS/Android the LAN access and app permission must be configured;
  an on-device packaged language model has not yet shipped.
- **Pixel visuals:** the character studio now shows a pixel character,
  while the world uses static PNGs with an animated player walk cycle.
  The locally installed Modern optional sprites permit choosing among
  four premade avatars; this is not equivalent to full per-pixel
  skin/hair/body/custom-outfit rigging.
- **Performance:** the render tree culls off-screen tiles and updates
  camera and sprite transforms each animation frame. This is _not_
  measured 60/120 FPS evidence; profile real devices.

### Acceptance still pending

A real-device playthrough must verify safe-area placement, touch movement,
1-hour clock scaling, foreground/background suspension, restart at saved
location, iOS networking to local Ollama, zero-stall conversation fallback,
all mission completion events and renderer frame timings on warm hardware.
The present PR is a feature branch, not a finished commercial game.
