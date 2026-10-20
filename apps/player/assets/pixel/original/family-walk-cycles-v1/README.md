# Family walk cycles v1

Original AI-assisted concept walk cycles for the named Bellweather family cast.
This batch is deliberately kept outside the runtime/catalog until manual pixel
cleanup, pivot review, collision review, and renderer QA are complete.

## Contents

- `niko/` — 4 directions × 4 phases for school-age Niko.
- `aunt-sol/` — 4 directions × 4 phases for senior Aunt Sol.
- `normalize_walk_cycles.py` — deterministic nearest-neighbor packaging helper.
- `mara/frames.json`, `eli/frames.json`, `niko/frames.json`, and
  `aunt-sol/frames.json` — frame manifests; all records retain
  `runtimeReady: false`.

Rows are `south`, `west`, `east`, `north`. Columns are `contact-a`, `passing-a`,
`contact-b`, `passing-b`. Exact source outputs are preserved in `niko/niko-walk-cycles-source.png` and
`aunt-sol/aunt-sol-walk-cycles-source.png`; each character folder also contains
its normalized atlas, preview, frames, and manifest.

## Provenance and rights boundary

Both sheets were generated with the built-in image generator on 2026-10-20.
No user ZIPs, third-party game art, external game-art references, or external
images were supplied. They are original AI-assisted project-owned working
concepts. They are not promoted to production runtime assets.

### Niko prompt (verbatim)

> Create one original transparent PNG sprite sheet for a retro top-down pixel life simulator. Character: Niko, school-age child sibling, small energetic silhouette, warm brown skin, curly ponytail, cobalt blue hoodie, orange sneakers, small backpack. Layout exact 4 columns by 4 rows, no gutters: rows SOUTH/front, WEST/left, EAST/right, NORTH/back; columns four distinct genuine locomotion phases contact-a, passing-a, contact-b, passing-b. Every cell one complete full-body child with feet visible and consistent bottom pivot. Make phases clearly different with alternating legs, opposite arm swings, torso bob, backpack movement. Keep Niko age-appropriate, preserve cobalt hoodie, orange sneakers, ponytail, backpack. Original 2D pixel art, crisp chunky clusters, limited vibrant palette, transparent background, no text, labels, grid lines, borders, outside shadows, extra characters, props, logos, 3D, photorealism, or game-art references.

### Aunt Sol prompt (verbatim)

> Create one original transparent PNG sprite sheet for a retro top-down pixel life simulator. Character: Aunt Sol, compact upright senior woman relative, warm brown skin, silver braid, plum coat, sage green walking cane, small crossbody pouch. Layout exact 4 columns by 4 rows, no gutters: rows SOUTH/front, WEST/left, EAST/right, NORTH/back; columns four distinct genuine locomotion phases contact-a, passing-a, contact-b, passing-b. Every cell one complete full-body older woman with feet visible and consistent bottom pivot. Make phases clearly different with alternating legs, gentle senior gait, opposite arm swing while the sage cane visibly changes support position between phases. Preserve silver braid, plum coat, sage cane, crossbody pouch in every direction. Original 2D pixel art, crisp chunky clusters, limited warm palette, readable at small scale, transparent background, no text, labels, grid lines, borders, outside shadows, extra characters, props, logos, 3D, photorealism, or game-art references. This sheet is a source concept, prioritize visual consistency and clean separation of all 16 cells.
