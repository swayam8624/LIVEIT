# Pet age movement cycles v1

Original, deterministic pixel-cluster movement studies for cat, dog, and rabbit companions. Each species has young, adult, and senior forms; every form has authored south, west, east, and north directions with contact-a, passing-a, contact-b, and passing-b phases. This is 9 forms × 4 directions × 4 phases = 144 transparent RGBA frames.

The logical drawing canvas is 48×64 and is enlarged 2× with nearest-neighbour sampling to the existing 96×128 pet frame contract. Every frame uses the shared bottom pivot `(48,124)`. Directions are drawn from separate geometry recipes; no frame is mirror-flipped. Species identity persists through coat palette, silhouette, facial features, and collar/bandana/harness cues. Senior forms use reduced gait amplitude, silver muzzle accents, and lower posture.

Files include per-species atlases and previews, one combined review atlas, `frames/` with per-frame hashes in `manifest.json` and `frames.json`, and unmodified deterministic source sheets. `runtimeReady` is false everywhere: these are original concept studies requiring pixel cleanup, timing, collision-box review, renderer sampling, and human art direction.

No supplied ZIP files, third-party sprites, logos, or external reference images were used.
