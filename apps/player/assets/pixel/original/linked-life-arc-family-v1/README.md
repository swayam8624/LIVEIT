# Linked player life-arc family v1

This batch connects original early- and later-life movement concepts into one
reviewable character-family atlas. It indexes eight stages and 128 directional
frames at `24×32`: infant crawl, toddler waddle, child, teen, young adult
woman, midlife woman, elder woman, and an elder man presentation variant.
Each stage has south/west/east/north directions and four contact/passing
phases. Every frame uses pivot `(12,31)`.

The seven-stage primary life arc carries deep-brown skin, coiled dark hair
through adulthood, silver-white coils at elder age, a recurring sky-blue
accent, and a small facial mark. The elder man is recorded as a related
presentation variant. The combined atlas and nearest-neighbor preview are
derived from the source batches; the individual frame PNGs and original
ImageGen sheets remain in their source folders.

## Rebuild and verification

Run the index, stage atlases, combined atlas, preview, and hashes from the
repository root:

```sh
python3 apps/player/assets/pixel/original/linked-life-arc-family-v1/build_family.py
```

`manifest.json` resolves each frame to its source batch and records frame and
source-sheet SHA-256 hashes. All records are marked `runtimeReady: false`.

## Continuity boundary

Early and later sheets were generated in separate sessions using the existing
original diverse life-arc sheet as their local visual reference. Shared
features and palette establish a clear art-direction link, but this index does
not prove that every face, outfit detail, or silhouette is the exact same
saved person. A pixel-artist must reconcile the stages before runtime use.
Collision boxes, animation timing, appearance-layer composition, renderer
sampling, and save/reload continuity also remain unverified.
