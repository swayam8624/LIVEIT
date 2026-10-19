# LIVEIT — first actual pixel-world gameplay slice

**Snapshot, 19 October 2026.** Branch: feat/pixel-town-cafe-playable, based on feat/native-life-economic-foundation. This is a *partial but real* 2D game foundation, not a finished BitLife/Episode-equivalent game.

## Implemented and testable

- **24 Git-tracked, native-bundled 16×16 PNG files** in apps/player/assets/pixel/pulse/; original Pulse Everyday Streets CC0 art, source provenance and automated PNG signature/dimension/chunk-CRC verification. No photo or 3D asset in the current new gameplay slice.
- **19×14 Bellweather Market and 12×10 café** deterministic 2D tile collision maps. Working furniture collisions, entry/exit portals and Amelia interaction. tests/pixel-town.test.ts covers stepping, portals and position verification.
- **Four-way D-pad**, including hold-to-walk repeats, player viewport, adjacent TALK interaction, descriptive status and local coordinate storage with queued writes to AsyncStorage.
- **Story integration:** Amelia talk starts the existing reunion narrative. The authoritative story engine still owns conditions, choices, relationships and saves. No fake trust/money changes.
- **Fully 2D emotional stage:** original original pixel-block café background, city window, warm lamp, palette moods, and character pixel busts with saved appearance colors and basic blink/speaking mouth (subject to reduced-motion settings). Not yet 12 individually illustrated emotion animations.
- GameStage no longer renders the old photographic cafe JPG. The whole product remains 100% pixel direction; old 3D and isometric code may be retained for build compatibility but are not active goals.

## Safe launch on your Mac without touching uncommitted work

Your original checkout at ~/Desktop/projects/living-universe has substantial uncommitted work and an unpushed local commit. Never run reset --hard, git clean -fd or force push to make this playable branch work. Create a separate worktree:

    cd ~/Desktop/projects/living-universe
    git fetch origin
    git worktree add --detach ../living-universe-pixel-preview origin/feat/pixel-town-cafe-playable
    cd ../living-universe-pixel-preview
    npm ci
    npm run web -w @living/player

Open the Expo local web URL (often localhost:8081), start/load Free Life and visit the pixel city. At (11,8), walk up once, then TALK beside Amelia at (10,7). Enter the café from street (5,7) into doorway (5,6); exit from café (5,8) down through doorway (5,9). Invalid paths and NPC position are blocked, and tile positions persist across reopening this same timeline. Physical-device and simulator gameplay still require direct evidence.

## Fast batch import of the six already-verified CC0 ZIPs

The general importer scans all 953 items in Downloads and prompts for every file. **Do not use it for this batch.** The exact-archive allowlist only imports matching SHA-256 copies of Pulse Streets, Kenney pixel UI, Kenney UI, Kenney UI audio, Kenney jingles and OwlishMedia SFX.

    cd ~/Desktop/projects/living-universe-pixel-preview
    python3 tools/import_known_cc0_packs.py --source "$HOME/Downloads"
    python3 tools/import_known_cc0_packs.py --source "$HOME/Downloads" --apply
    python3 tools/validate_pixel_assets.py
    du -sh assets/imported
    git status --short

Incorrect/missing hashes are SKIPPED, not auto-approved. This importer retains the original ZIPs where they are, rejects unsafe archive entries, excludes executables/3D content and creates source/license evidence receipts. Other itch.io packs with no rights proof or licenses restricting public raw-source redistribution are excluded—even if the game itself is free/open-source.

After inspecting the imported contents, check GitHub file size limits and push *only* the imported approved files from this detached worktree:

    git add assets/imported
    git diff --cached --stat
    git commit -m "assets(pixel): import verified CC0 sprites UI and audio"
    git push origin HEAD:refs/heads/feat/pixel-town-cafe-playable

This does NOT affect the local unpushed commit in the owner's original checkout. If push rejects after a collaborator updates remote, fetch/reconcile and never force-push.

## Explicit outstanding engineering and creative work

- The pixel grid is an early two-map demonstration, not a continuous whole city, functional career/location path, or finished Episode-style game.
- Sprite image scaling uses React Native Images; native nearest-neighbor shader and hardware frame timings have NOT been verified.
- Directional standing frames work; authored 4-frame walks, appearance-aware overworld customization, aging, wardrobe consistency, broader character animation and rich emotional acting sprite sheets are future work.
- The story background uses original pixel block geometry, not yet full hand-authored animation plates across every chapter.
- Audio event playback from imported SFX/music is not wired yet. Haptics and authoritative saved consequence widgets require integration.
- Position is persisted independently by timelineId; new-life isolation and move-to-main-save-schema migration are still open. Narrative consequences are stored in the existing timeline save system.
- The user's original local life-simulation, memory, navigation and local social edits have NOT been imported or overwritten. That work needs careful future reconciliation.
- No first-class complete native simulator/gameplay signoff is implied by a green foundation test.

## Test commands

    npm run check
    python3 tools/validate_pixel_assets.py

CI foundation validates formatting, lint, TypeScript and unit tests including the tile maps and actual PNG files. Additional actual iOS/Android install and interaction evidence is needed before claiming the native game works.

**Next:** integrate approved user audio and new sprites, proper appearance matching between town/portrait, full animated walk frames and dialogue portraits, context-aware choice/outcome UI, more locations and real device gameplay.
