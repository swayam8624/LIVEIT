# Alternate life-arc family v1

This is a rights-safe, runtime-disabled concept package for a second player
identity. It intentionally does not copy any supplied ZIP contents or
third-party art. The family uses a warm-olive complexion, auburn hair,
mustard scarf, teal satchel and small gold star cue across ten stages:
infant, toddler, child, teen, young-adult woman, midlife woman, elder woman,
young-adult man, midlife man and elder man.

The package contains 160 movement frames (ten stages × four authored directions
× four phases) and 80 idle/interact frames (ten stages × four directions × two
states), all 24×32 RGBA with pivot `(12,31)`. The generated stage masters,
stage atlases, branch atlases, combined atlases and labeled preview are
deterministic outputs from `build_alternate_family.py`.

`manifest.json` records the exact source prompt, identity cues, per-frame
dimensions, pivots, non-mirroring declaration, output hashes, and limitations.
`provenance.json` records the offline Pillow source policy and external-input
list. `hashes.sha256` covers every generated file. Every payload is explicitly
`runtimeReady: false`; pixel cleanup, identity review and renderer integration
are required before this becomes a runtime asset.

Rebuild with:

```bash
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 build_alternate_family.py
```
