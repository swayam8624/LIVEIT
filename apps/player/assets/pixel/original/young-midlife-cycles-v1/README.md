# Young adult + midlife movement cycles v1

This batch contains two original female adult stages with four cardinal directions and four walk phases per direction. The generated source is organized as a strict 4-column × 8-row sheet:

1. young adult woman: south, west, east, north
2. midlife adult woman: south, west, east, north

Every facing row contains `contact-a`, `passing-a`, `contact-b`, and `passing-b`. The normalized deliverable uses 96×128 RGBA frames with a shared bottom-center pivot at `(48,126)`, a 384×1024 RGBA atlas, and 32 metadata records. Every record is `runtimeReady: false` pending renderer sampling, collision-box review, and a human motion-quality pass.

## Files

- `young-midlife-cycles-source.png` — unmodified generated 4×8 source sheet retained for visual provenance.
- `young-midlife-cycles-atlas.png` — normalized 384×1024 RGBA atlas, four phase columns by eight facing rows.
- `young-adult-woman/*.png` — 16 normalized 96×128 RGBA frames.
- `midlife-adult-woman/*.png` — 16 normalized 96×128 RGBA frames.
- `frames.json` — authoritative stage, facing, phase, atlas rectangle, pivot, and readiness metadata.
- `normalize_cycles.py` — deterministic source crop and nearest-neighbor normalization script.

## Provenance

Generated on 2026-10-20 with the built-in image generator. The supplied `../age-direction-concept-batch-v1/age-directions-concept-master.png` was used only as a visual identity and palette reference. It was not copied or edited. No user ZIP, reference game art, or third-party art was used.

Verbatim generation prompt:

> Use case: stylized-concept. Asset type: original top-down retro pixel-art walk-cycle sprite sheet for a life simulator.
>
> Input image 1 is a visual identity and palette reference only. Preserve the broad warm medium-brown skin, dark brown hair, cream clothing with teal and ochre accents, and age progression language, but do not copy its pixels, poses, or layout.
>
> Create ONE strict transparent sprite sheet with exactly 4 equal columns by 8 equal rows (4 columns x 8 rows), no cell borders, no labels, no text, no grid lines, no shadows outside the characters. The four columns are exactly: contact-a, passing-a, contact-b, passing-b. The eight rows in exact order are: young adult woman south/front, young adult woman west/profile, young adult woman east/profile, young adult woman north/back, midlife adult woman south/front, midlife adult woman west/profile, midlife adult woman east/profile, midlife adult woman north/back.
>
> Every cell contains one centered full-body character, with transparent padding and a stable bottom-center foot pivot. Each row's four frames must show a REAL walk cycle with clearly different leg and arm poses: contact-a has one leg extended and opposite arm forward; passing-a has one knee passing under the body with arms closer; contact-b reverses the lead leg and opposite arm; passing-b reverses the passing pose. Make the limb changes visibly readable at sprite scale, while keeping the character identity and clothing consistent within each four-row age group. Do not use duplicated or nearly identical frames.
>
> Young adult woman: warm medium-brown skin, dark shoulder-length hair tied back, cream blouse, teal high-waisted trousers, small ochre sash accent, slim young-adult proportions.
> Midlife adult woman: warm medium-brown skin, dark hair with a few gray strands tied low, cream cardigan, teal trousers or skirt, ochre scarf accent, slightly broader mature proportions and a confident relaxed gait.
>
> Cardinal directions must be unambiguous: south shows face and front clothing, west and east show clean opposite profiles with nose/chin direction and profile legs, north shows the back of hair and clothing. Keep rows visually separated, keep each stage's four phases aligned to the same scale, and keep all arms, legs, hair, and clothing fully inside their cells.
>
> Style/medium: crisp handcrafted pixel art with hard pixel clusters, limited cohesive palette, no gradients, no blur, no antialiasing, no photorealism, no 3D, no perspective camera, no ground plane. Transparent background only.
>
> Avoid: extra characters, duplicate frames, merged neighboring cells, missing limbs, ambiguous facing, inconsistent clothing, text, watermark, logos, checkerboard, border, cast shadows, decorative props, excessive highlights, sexualized content.

## Visual audit and limitations

The source and atlas were visually inspected at native resolution. The four phase columns show visibly different leg and arm poses; the south, west, east, and north silhouettes are readable; and the young adult and midlife groups remain visually distinct. The generated source has a few tight row seams around the profile rows. The normalizer removes disconnected seam residue where possible and retains the unmodified source for audit. This is concept and pipeline art only: it needs palette cleanup, a motion-quality pass, collision-box review, and renderer validation before `runtimeReady` can become true.
