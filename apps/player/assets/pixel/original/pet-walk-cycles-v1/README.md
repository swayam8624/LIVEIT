# Companion movement studies v1

This batch contains original AI-assisted 4-direction, 4-phase concept cycles
for a tabby cat, a small dog, and a rabbit. Each species has sixteen extracted
`96×128` RGBA frames, a `384×512` atlas, a nearest-neighbor preview, and frame
metadata with direction, phase, pivot, provenance, and `runtimeReady: false`.

The dog and rabbit previews have readable silhouettes at review size. The cat
is visibly softer and more detailed than the intended pixel-cluster style; it
needs a substantial redraw. None of these concepts is approved for runtime.
The set still lacks additional identities, coat patterns, idle/emotion/care
poses, pet age stages, collision shapes, and renderer review.

## Source and cleanup

The original generated source sheet for each animal is retained unchanged.
`cleanup_transparent_fringe.py` edits only extracted frame PNGs, clears
strongly saturated edge pixels with alpha at most 8/255, and rebuilds that
species' atlas and existing nearest-neighbor preview. To repeat the cleanup
from this folder's parent project root:

```sh
python3 apps/player/assets/pixel/original/pet-walk-cycles-v1/cleanup_transparent_fringe.py
```

This is a deterministic fringe pass, not a replacement for manual pixel-art
cleanup or animation approval. All sources are original generated concepts;
no supplied archive art or third-party game art was used.
