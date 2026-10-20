# Named family batch v1

Original pixel-only concept art for the Bellweather family cast referenced by
the life and family systems: Mara (parent/caregiver), Eli (parent/caregiver),
Niko (school-age sibling), and Aunt Sol (older relative).

## Deliverables

- `named-family-portraits-concept-master.png` — transparent 2×2 concept board
  with one distinct full-body portrait study per family member (1295×1214 RGBA).
- `named-family-sprite-atlas-concept-master.png` — transparent concept atlas
  arranged as four character bands. Each band is four facing rows
  (south/west/east/north) by four pose columns (idle/step-left/step-right/
  interact), for 16 cells per character (1024×1536 RGBA).
- `characters.json` — stable character IDs, silhouette/palette notes, and
  portrait board regions.
- `frames.json` — source dimensions, atlas grid, directions, pose tags,
  integer pivot guidance, and per-character frame records.

The atlas is intentionally a visual concept sheet. The generator did not
guarantee exact pixel-cell registration or animation continuity, so it remains
`runtimeReady: false` and needs manual pixel cleanup, alignment, collision-box
review, and renderer QA before any runtime use.

## Visual direction

This batch follows `docs/PIXEL_ONLY_DIRECTION_V2.md`: original 2D pixel art,
distinct silhouettes and palettes, readable small faces, transparent RGBA
backgrounds, and no 3D meshes, rigs, game-art references, logos, or text.
Mara and Eli are adults; Niko is a child; Aunt Sol is an older relative.
Niko has no adult-coded romantic or intimate expressions.

## Provenance and rights boundary

Both PNGs were generated with the built-in image generator on 2026-10-20.
No user ZIPs, third-party game art, external game-art references, or external
images were supplied to either generation. These are original AI-assisted
concepts contributed as project-owned working material; they are not final
production art and have no runtime/catalog promotion.

SHA-256: `b7c3e06b35564e5ff7c5c1f50f6ef00247273d5353f5224aec392a87b6ceff96`
for the portrait board and
`4e14ef0b6c8e644622abb5f4a55762ad3d3064ad9f71d2b70f0852016a85d28b` for the
sprite atlas at this revision.

### Portrait prompt (verbatim)

> Use case: stylized-concept. Asset type: original pixel-art family NPC concept portrait board for a retro top-down life simulator. Primary request: create a clean 2x2 board of four separate full-body pixel character portrait studies with generous transparent spacing: Mara, adult mother/caregiver, sturdy pear-shaped silhouette, warm rust cardigan, mustard scarf, deep brown skin, short natural curls, canvas tote; Eli, adult father/caregiver, tall lean silhouette, navy work jacket, ochre shirt, medium olive skin, close-cropped dark hair, round glasses; Niko, school-age sibling, small energetic silhouette, cobalt hoodie, orange sneakers, warm brown skin, curly ponytail; Aunt Sol, older relative, compact upright silhouette with silver braid, plum coat, sage walking cane. Every character must be clearly distinct in height, body shape, hair, clothing blocks and palette. Strictly original 2D pixel art, crisp chunky clusters, limited 16-color palette per character, front-facing 3/4 full body, transparent background, no text, no labels, no logos, no grid lines, no shadows outside figures, no 3D, no game-art references, no photorealism. Preserve readable faces at small scale.

### Atlas prompt (verbatim)

> Use case: stylized-concept. Asset type: original multi-character top-down pixel sprite atlas for a retro life simulator. Primary request: a clean 4 columns by 4 rows transparent atlas with the same four original named family characters repeated as cardinal facing poses. Rows are south/front, west/left, east/right, north/back. Columns are idle, walk-left-step, walk-right-step, interact. Use Mara (adult mother/caregiver: sturdy pear shape, rust cardigan, mustard scarf, dark curly hair, warm deep-brown skin), Eli (adult father/caregiver: tall lean, navy work jacket, ochre shirt, glasses, olive skin), Niko (small school-age sibling: cobalt hoodie, orange shoes, ponytail), Aunt Sol (short older relative: silver braid, plum coat, sage cane). Arrange four separate character bands vertically, each band 4 rows x 4 columns, every cell equal size, feet visible, aligned bottom pivots, silhouettes and palette blocks remain distinct. Strictly original 2D top-down 3/4 retro pixel art, crisp chunky clusters, limited palette, transparent background, no text, no labels, no logos, no grid lines, no shadows outside figures, no 3D, no game-art references, no photorealism. Keep identity, clothes, hair, accessories consistent across each character's 16 cells.
