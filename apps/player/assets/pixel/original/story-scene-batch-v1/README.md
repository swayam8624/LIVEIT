# Story scene batch v1

Two original, AI-assisted 2D pixel scene plates for dedicated dialogue and
exclusive story moments in LIVEIT. This batch is intentionally isolated from
runtime catalogs and game code.

## Deliverables

| File                                           | Use                                                                          | Art status                                 |
| ---------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------ |
| `bellweather-cafe-reunion-flat-concept-v1.png` | Warm Bellweather café reunion at blue hour; two actors staged across a table | Flat concept plate; 16:9, 1672x941 RGB PNG |
| `riverside-promise-dusk-flat-concept-v1.png`   | Rainy riverside promise at dusk; two actors under one umbrella               | Flat concept plate; 16:9, 1672x941 RGB PNG |
| `scenes.json`                                  | Scene IDs, staging, dock-safe areas, provenance, and readiness limits        | Authoring metadata only                    |

## Provenance

Both images were generated with the built-in OpenAI image generation tool on
2026-10-20. No supplied ZIP, third-party sprite, game-icons asset, or copied
character was used as a reference. The complete prompts are preserved in
`scenes.json` so the art pass can be reproduced or revised without guessing.

## Runtime limitations

These are reviewable concept backgrounds, not integrated runtime scenes. They
have no transparent layers, actor animation, parallax planes, dialogue UI,
localized text, accessibility-safe contrast validation, or device crop tests.
They remain flat plates because automatic background/midground/foreground
separation would cut through the rain, reflections, plants, and pixel clusters.
For runtime, re-author clean layered plates and separate actor sprites from the
same visual language before wiring them to StoryPlayer.

The café's lower center is the primary dialogue-dock-safe area. The riverside
scene keeps the lower center dark and places narration-friendly negative space
on the left. These staging hints are advisory metadata, not UI guarantees.
