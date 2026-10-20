# Linked male adult cycles v1

This is an original, rights-safe concept batch for the missing male branch of the LIVEIT life arc. It supplies `young-adult-man` and `midlife-man` movement coverage at 24x32 pixels, with four directions and four distinct walk phases per stage (32 transparent frames total), plus four-direction idle and everyday interaction poses for each stage (16 additional transparent frames). The elder-man handoff is documented in `manifest.json` and points to the existing elder-man movement and pose batches for continuity review.

## Provenance

The two source sheets in `source/` were generated with the built-in image generator on 2026-10-20. The exact prompts are preserved below. They are original generation inputs; no supplied ZIP, third-party sprite, or web image was used. The builder crops each 4x4 source sheet, reduces it to a compact 32-color hard-alpha sprite, and writes deterministic frame, atlas, preview, and manifest outputs.

Young-adult source prompt:

> Use case: stylized-concept. Asset type: original pixel-art game sprite source sheet. Generate an original 4 by 4 sheet with rows south, west, east, north and columns contact-a, passing-a, contact-b, passing-b. Deep-brown-skinned young adult man, short coiled dark hair, tiny crescent facial mark, sky-blue shirt accent, ochre trousers, russet shoes, teal wrist band. Direction-specific authoring, no mirroring. Crisp hand-authored pixel clusters, limited 32-color palette, hard edges, transparent alpha, no text, logo, watermark, grid lines, duplicate copies, or extra characters.

Midlife source prompt:

> Use case: stylized-concept. Asset type: original pixel-art game sprite source sheet. Generate an original 4 by 4 sheet with rows south, west, east, north and columns contact-a, passing-a, contact-b, passing-b. The same deep-brown-skinned man, now midlife with a slightly broader relaxed build, short coiled hair with silver strands at the temples, the same crescent mark, sky-blue overshirt, ochre trousers, russet shoes, teal wrist band. Direction-specific authoring, no mirroring. Crisp hand-authored pixel clusters, limited 32-color palette, hard edges, transparent alpha, no text, logo, watermark, grid lines, duplicate copies, or extra characters.

Idle and interaction source prompts:

> Use case: stylized-concept. Asset type: original pixel-art game sprite source sheet. Generate an original 4 by 2 sheet with columns south, west, east, north and rows calm idle and gentle everyday interaction. The same deep-brown-skinned young adult man, short coiled dark hair, tiny crescent facial mark, sky-blue shirt accent, ochre trousers, russet shoes, teal wrist band. Idle has relaxed arms and slight breathing asymmetry. Interaction has one hand raised in a friendly wave or offering a small object, remains everyday-safe, and reads clearly at sprite scale. Direction-specific authoring, no mirroring. Crisp hard-edged 32-color pixel clusters, transparent alpha, no text, logo, watermark, grid lines, duplicate copies, or extra characters.

> Use case: stylized-concept. Asset type: original pixel-art game sprite source sheet. Generate an original 4 by 2 sheet with columns south, west, east, north and rows calm idle and gentle everyday interaction. The same deep-brown-skinned man at midlife, slightly broader relaxed build, short coiled hair with silver strands at the temples, same crescent mark, sky-blue overshirt, ochre trousers, russet shoes, teal wrist band. Idle has relaxed arms and slight breathing asymmetry. Interaction has one hand raised in a friendly wave or offering a small object, remains everyday-safe, and reads clearly at sprite scale. Direction-specific authoring, no mirroring. Crisp hard-edged 32-color pixel clusters, transparent alpha, no text, logo, watermark, grid lines, duplicate copies, or extra characters.

## Review boundary

The frames are intentionally marked `runtimeReady: false`. They have valid dimensions, pivots, alpha, source and output hashes, and deterministic build steps, but still require human identity reconciliation against the existing woman-led linked arc and elder-man presentation before runtime integration. The interaction row is a friendly wave or small-object offer and is not tied to any specific dialogue system yet.

Rebuild with:

```sh
/Users/swayamsingal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 build_linked_male_adult_cycles.py
```
