# Accessible controls v1

Original, text-free pixel control concepts that extend `button-states-v2`,
`hud-controls-batch-v1`, and `conversation-ui-v3`. This batch focuses on
selection widgets, navigation surfaces, and feedback states that are not
covered by large action-button plates or chat controls.

## Contents

- `controls/` contains 52 transparent 64×48 RGBA state sprites across ten
  families: checkbox, switch, radio, slider, tab, segment, disclosure,
  settings key, phone key, and map key.
- `manifest.json` records family/state coverage, dimensions, hashes, nearest
  sampling, and the runtime readiness boundary.
- `provenance.json` records the local drawing method and hashes/dimensions for
  the PNG files.
- `accessible-controls-preview-3x.png` is a nearest-neighbor review board. Rows
  follow the family order in `manifest.json`; labels under each sprite name the
  state. Labels appear only in this review image, never in the individual art.
- `generate_controls.py` regenerates the PNGs and metadata deterministically.
- `validate_controls.py` audits PNG dimensions/modes and manifest/provenance
  hashes.

## State coverage

| Family       | States                                              |
| ------------ | --------------------------------------------------- |
| Checkbox     | unchecked, checked, focused, disabled, error        |
| Switch       | off, on, focused, disabled, loading                 |
| Radio        | unselected, selected, focused, disabled, error      |
| Slider       | normal, focused, pressed, disabled, error           |
| Tab          | idle, selected, focused, disabled, loading          |
| Segment      | idle, selected, focused, disabled                   |
| Disclosure   | closed, open, focused, disabled, error              |
| Settings key | normal, selected, focused, disabled, loading, error |
| Phone key    | normal, selected, focused, disabled, loading, error |
| Map key      | normal, selected, focused, disabled, loading, error |

The gold corner brackets distinguish visible focus; shape and marks supplement
color for key states. Every glyph keeps dynamic labels outside the image. Error,
loading, and disabled marks are artwork only: the consuming interface must pair
them with accurate state, accessible semantics, and explanatory text where
needed. Focus brackets do not replace operating-system focus indicators.

## Provenance and limits

Authored locally on 2026-10-20 from integer-coordinate Pillow drawing
primitives in `generate_controls.py`. No third-party art, supplied archive,
downloaded material, image-generation output, logo, or external font was used.
There is no third-party source license to attribute.

This is source concept art only. `runtimeReady` is `false`; the batch is not
registered in the production catalog or connected to app state. It does not
implement touch or keyboard input, focus order, screen-reader labels, haptics,
phone/chat flows, navigation, save behavior, or accessibility settings.
Contrast, color-vision, device-scale, localization, native rendering, and
human pixel cleanup still require review before any runtime use. The batch
does not cover a high-contrast theme, a full keyboard/controller focus system,
or all visible controls in the 323-feature checklist.

## Checklist relationship

The sprites support the HUD/social-display visual workstream listed in
`docs/PIXEL_SPRITE_ASSET_NEEDS.md` (not edited here): checklist groups
11.01–11.18, 14.01–14.09, 17.01–17.18, 18.01–18.19, and 19.13. These are
reusable control concepts, not evidence that any checklist feature is
implemented or complete.
