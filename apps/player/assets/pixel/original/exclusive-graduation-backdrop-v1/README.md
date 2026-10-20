# Exclusive graduation courtyard backdrop v1

This isolated original concept batch adds a warm neighborhood-school courtyard for graduation scenes. The built-in ImageGen source provides the composition, stage and open actor-safe foreground. The source is detailed and softly rendered; the 32- and 64-color exports are nearest logical-size palette studies, not approved runtime art.

## Files

- `source.png`: retained generated source image.
- `graduation-courtyard-32-color-320x256.png`: 320×256 limited-palette export.
- `graduation-courtyard-64-color-320x256.png`: 320×256 alternate palette export.
- `graduation-courtyard-preview-3x.png`: nearest-neighbor review preview.
- `manifest.json`: exact prompt, source/export hashes, dimensions and readiness status.
- `build_backdrop.py`: reproducible normalization script.

## Review boundary

The image was newly generated; no supplied ZIP contents, downloaded assets, third-party art, logos, or fonts were used. The export still needs pixel-artist review, layer/depth separation, collision and walkability authoring, actor-safe-region validation, palette approval, and actual renderer integration. Every export remains `runtimeReady: false`.

Rebuild with Python Pillow:

```sh
python3 build_backdrop.py
```
