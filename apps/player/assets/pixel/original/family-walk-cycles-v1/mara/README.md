# Mara walk cycles v1

Original AI-assisted pixel locomotion concept for Mara, the adult Bellweather
parent/caregiver. This is an isolated intake batch and is not registered in the
runtime asset catalog.

## Deliverables

- `mara-walk-cycles-source.png` — exact generated 4×4 source sheet.
- `mara-walk-cycles-atlas.png` — normalized 384×512 RGBA atlas.
- `frames/` — sixteen normalized 96×128 RGBA frames.
- `frames.json` — direction, phase, atlas coordinates, pivot, and readiness metadata.
- `normalize_cycles.py` — deterministic nearest-neighbor crop/normalization script.

Rows are south, west, east, and north. Columns are contact-a, passing-a,
contact-b, and passing-b. Each row contains visibly different leg and arm
positions; the scarf and tote retain Mara's identity while moving naturally.

## Provenance and rights boundary

Generated with the built-in image generator on 2026-10-20. The existing
`named-family-portraits-concept-master.png` was supplied only as an internal
visual identity reference. No ZIP contents, third-party game art, logos, or
external images were used. The source and normalized derivatives are original
AI-assisted concept material and remain `runtimeReady: false` pending manual
pixel cleanup, pivot/collision review, and renderer QA.

## Prompt (verbatim)

> Use the attached original pixel concept board only as visual identity reference for Mara. Generate ONE clean 4 columns x 4 rows sprite sheet for the same adult caregiver woman Mara. Transparent background, no grid, no labels, no text. Every cell must contain the same recognizable sturdy pear-shaped woman with deep brown skin, short natural curls, rust cardigan, mustard scarf, olive trousers, brown shoes, and a cream canvas tote hanging at her side. Layout: rows are south/front, west/left profile, east/right profile, north/back; columns are contact-a, passing-a, contact-b, passing-b. Four genuinely different locomotion phases in each row: alternating legs, swinging arms, shifting scarf and tote naturally, but keep feet aligned to a common bottom pivot and leave generous transparent gutters between cells. Crisp original 2D top-down 3/4 pixel art, chunky 1-3 pixel clusters, limited warm palette, readable silhouette at 96x128 cell scale. No 3D, no photorealism, no existing game art, no logos, no UI, no shadows or floor.
