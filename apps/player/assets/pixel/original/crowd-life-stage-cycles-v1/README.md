# Crowd life-stage cycles v1

This original concept pack adds age-stage variants to the 30 crowd archetypes
from `crowd-archetypes-batch-v1`, `v2`, and `v3`. It creates 24×32 transparent
RGBA frames with a shared bottom-center pivot `(12,31)`, four independently
authored source directions (`south`, `west`, `east`, `north`), and three
movement states (`walk-a`, `walk-b`, `idle`) for every listed role and stage.

The stage bands are child 8–12, teen 16–19, adult 20–59, and elder 60+. Age
coverage is role-aware. Child and teen variants are limited to non-professional
participation, recreation, and learning; no child or teen employment is
depicted. Roles such as `child-playground` and `elder-walker` only receive
stages that fit their identity. Older workers remain possible crowd concepts,
not a claim that an older person is retired or needs mobility assistance.

Generation is deterministic. Adult frames are exact copies of the authored
source frames; child and teen frames scale the source silhouette and its prop
with nearest-neighbour sampling, anchored at the shared ground pivot; elder
frames recolor the source's exact hair palette to silver. Role-specific cues
such as uniforms, props, bags, instruments, stroller, ball, and cane stay with
the source silhouette. This is a readable age-variation study, not a final
character-acting or identity-continuity solution.

## Contents and regeneration

- `build_crowd_life_stages.py`: deterministic builder using the original local
  v1–v3 crowd concepts only.
- `manifest.json`: pack-level role, age, direction, phase, dimension, pivot,
  and runtime-status index.
- `frames/<role>/<age>/`: 12 PNG frames and a per-stage manifest per age stage.
- `provenance.json`: source and transformation disclosure.
- `validate_crowd_life_stages.py`: source, geometry, combination, hash, and
  `runtimeReady:false` checks.

Regenerate and validate from the repository root with the bundled runtime:

```sh
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 apps/player/assets/pixel/original/crowd-life-stage-cycles-v1/build_crowd_life_stages.py
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 apps/player/assets/pixel/original/crowd-life-stage-cycles-v1/validate_crowd_life_stages.py
```

All files are concept-only and remain `runtimeReady: false`. Human pixel-art
review, palette approval, licensed-use review where relevant to future edits,
engine import, and on-device visual validation are still required before any
runtime admission. No supplied ZIP art or internet art was used.
