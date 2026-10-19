# LIVEIT Pixel-Only First Playable — Development Runbook

PR: https://github.com/swayam8624/LIVEIT/pull/9

This separate development branch protects the user's original heavily modified local checkout and its unpushed code changes. Do not force-push or reset that checkout.

## What exists on this branch

A playable touch D-pad top-down Bellweather Market map and an enterable café, collision with buildings and furniture, an Amelia proximity-gated story activation, position saved in AsyncStorage by timeline, real user-uploaded CC0 Pulse 16px PNG assets embedded offline, and pixel-block character busts for the existing saved-appearance/choice-driven story. Unit tests cover movement, collision, portals, position validity, pixel art PNG integrity, and pixel-only specifications. This is a FIRST SLICE, not a complete released life game.

## Try it without touching the original Mac checkout

    cd ~/Desktop/projects/living-universe
    git fetch origin
    git worktree add --detach ../living-universe-pixel-game origin/feat/pixel-town-cafe-playable
    cd ../living-universe-pixel-game
    npm ci
    npm run dev

Open the Expo web URL shown in the terminal. Under Life > Bellweather, walk the map, approach Amelia, press TALK and use the existing branching story. A web build isn't proof of a successful native iOS install; use npm run ios separately on a correctly configured Mac when appropriate.

## Auto-import the SIX exact rights-approved CC0 ZIPs you supplied

    cd ~/Desktop/projects/living-universe-pixel-game
    python3 tools/import_known_cc0_packs.py --source "$HOME/Downloads"
    python3 tools/import_known_cc0_packs.py --source "$HOME/Downloads" --apply
    python3 tools/validate_pixel_assets.py
    du -sh assets/imported
    git status --short

The batch importer selects only hash-pinned matching versions of Pulse Everyday Streets, Kenney Pixel UI, Kenney UI Pack, Kenney UI Audio, Kenney Music Jingles, and Owlish Media Sound Effects. All six are CC0 with embedded text or the verified original publisher's public CC0 listing. It does not ask about 953 unrelated Downloads files; it preserves a local backup of the old scan report and does not alter the source ZIPs. It transcodes audio for mobile when ffmpeg exists.

Open-source distribution of raw source art is still redistribution. Archive terms matter even when the game is entirely free: SuperRetroWorld, Humble Gift, other custom-licensed and unknown-license packs cannot automatically be published as raw game assets. They are not auto-approved. Game-icons.net assets are separately CC BY and require author credit and SVG processing, which this pixel importer does not yet provide.

After inspecting the imported files and their SOURCE.json rights receipts:

    git add assets/imported
    git diff --cached --stat
    git commit -m "assets(pixel): ingest approved six CC0 packs"
    git push origin HEAD:refs/heads/feat/pixel-town-cafe-playable

If GitHub rejects a non-fast-forward push, do not force it. Reconcile the isolated worktree with the remote branch carefully without altering the original dirty checkout.

## Unfinished production work

This branch is not the full LIVEIT game. The starter map is small; the player overworld sprite does not yet express all saved hairstyle/age/outfit combinations, and the pixel portraits are an early native block-pixel art system, not the final artist-designed full expression sheets. The next playable roadmap covers larger districts, lawful imported tile atlas activation, fine animation timing, a full range of authorable pixel story backgrounds, NPC schedules, world-navigation save schema merge, UI widgets, music/SFX hooks, performance, accessibility and real device validation. Older 3D experiments and the 1481-item three-dimensional art catalog remain archived, not LIVEIT's pixel-only targets.
