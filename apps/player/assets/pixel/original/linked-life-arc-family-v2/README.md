# Linked life-arc family v2

This is a runtime-disabled aggregate for reviewing the complete age-aware
character family. It indexes existing transparent concept frames and builds two
deterministic review atlases:

- `linked-life-arc-family-v2-movement-atlas-24x32.png`: 10 stages × 16 frames,
  ordered south, west, east, north and contact-a, passing-a, contact-b,
  passing-b.
- `linked-life-arc-family-v2-pose-atlas-24x32.png`: 10 stages × 8 frames,
  ordered south, west, east, north and idle, interact.
- `linked-life-arc-family-v2-preview-4x.png`: a labeled review sheet showing
  the four-direction contact-a samples beside south-facing idle/interact.

The stages are infant, toddler, child and teen shared ages; young-adult,
midlife and elder woman; and young-adult, midlife and elder man. The adult man
movement and idle/interact frames come from `linked-male-adult-cycles-v1`,
including its newly added midlife poses. The elder-man movement branch is
indexed from `linked-life-arc-family-v1` and its poses from
`linked-elder-poses-v1`.

`build_linked_family.py` is the reproducible builder. It reads source manifests,
checks every referenced frame's SHA-256, checks 24×32 dimensions and the
(12,31) pivot, then generates the aggregate atlases without creating duplicate
per-frame files. `manifest.json` records every source package, source-manifest
hash, source file path/hash, derived atlas hash, stable frame ID, and the
explicit non-mirroring assumption.

All source art was generated or derived locally for this project. No supplied
ZIP contents are copied into this package. The source branches were generated
separately, so exact identity continuity still requires a human art pass before
runtime use. Every item is marked `runtimeReady: false`; this package is not
admitted to the runtime asset catalog.

Rebuild:

```bash
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 build_linked_family.py
```
