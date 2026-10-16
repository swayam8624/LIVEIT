# LIVEIT — Visual Gameplay Production Gate

## Diagnosis (16 Oct 2026)

The original implementation passes engine-oriented acceptance tests but its UI is structurally an editorial dashboard: horizontal header, sidebar navigation, metric cards, list of activities, white dialogue panels, and a cafe illustrated with React Native rectangles. That validates state transitions, not player immersion. A mobile bundle export does not validate native art composition.

## Design target

A cinematic illustrated 2.5D narrative game. Prioritize a full-bleed scene, diegetic character presentation, expressive dialogue, deliberate camera staging, and unobtrusive persistent life HUD. In Free Life, a navigable illustrated city/room screen replaces the web-dashboard home; daily activities become in-world destinations or an intentional game action wheel. Story Mode opens in a full-screen scene with dialogue dock and actor portraits. Preserve all simulation and timeline semantics.

## Completed in design branch

- Dark, high-contrast jewel-tone player palette and upgraded typography hierarchy.
- Taller, letterboxed prototype cafe viewport, nighttime lighting and narrative place/time treatment.
- Updated branded shell and cinematic Creator Studio styling.
- No changes to simulation state, saves, story validation or serialized formats.

These are _presentation groundwork_, not completion of the game art overhaul. The existing cafe still uses primitive shapes and the navigation shell still has dashboard DNA.

## Required production tasks (in order)

1. Create original, commercially usable visual asset plates for Bellweather cafe exterior/interior and two named characters. Maintain source records, provenance and licensing. Use AI only where service rights allow. Never copy Episode/BitLife assets.
2. Produce layered artwork: background, weather, furniture foreground, character base portraits, separate expressions and anatomy/pose guides. Character overlays must anchor to normalized positions and share a stable rig/style contract.
3. Implement a cross-platform `SceneStage` component with art loading, safe-area layout, responsive portrait and landscape camera composition, text-safe zones, parallax depth and a reduced-motion toggle.
4. Replace the CSS-like cafe primitives, retaining a fallback if assets cannot be loaded.
5. Redesign Free Life as an illustrated destination-based game (home, city, contacts, occupation) while keeping actions and rules unchanged. Include an accessible stat HUD and event journal, but **do not use cards as the primary game surface**.
6. Redesign Story Mode as a visual-novel scene, dialogue dock, touch-sized contextual decisions, character reactions and animated scene transitions.
7. Redesign Creator Studio to visually preview the same runtime `SceneStage`, and progressively replace raw JSON editing with a branching node graph.
8. Run web mobile/desktop screenshots, native simulators and real-device QA. Compare against approved art boards, not just snapshots of generated UI.

## Strict acceptance gate

- In both game modes, artwork is the dominant first-screen surface rather than form controls or metric cards.
- The opening scene shows at least one original rigged/expressive character and an original location plate with obvious depth.
- Selecting a choice visibly changes character emotion and game state, and survives save/reload.
- At widths 360, 390, 768 and 1440, no dialogue or action is obscured by a portrait crop or phone safe area.
- Free Life gameplay isn't a spreadsheet: a first-time user can identify where to go and what to do without explanatory prose.
- Story Mode is fully navigable by keyboard, touch and screen reader; reduced motion is respected.
- Native device tests are required. Browser verification alone is insufficient.
- Existing world-state, time progression, save and branching regression tests continue to pass.

## Blocking external dependency

The connected fal image-generation account returned a `balance_exhausted` error when attempting an original rainy-dusk cafe plate. No generated asset was committed. This branch uses source-only visual improvements until asset generation succeeds.

## Note for Codex

Do not declare the art overhaul complete because checks pass. Insist on actual rendered screenshots for each mode, visual comparisons, verified art provenance, and native smoke testing. Keep improvements in small reviewable commits and preserve all engine contracts.
