# Pixel sprite family coverage audit

Audit date: 2026-10-20<br>
Authoritative catalog: [`content/production-assets/v1/pixel-world.json`](../content/production-assets/v1/pixel-world.json)<br>
Concept root: [`apps/player/assets/pixel/original`](../apps/player/assets/pixel/original)

## Age-cycle update (2026-10-20)

The role coverage below records the base movement packs. Since that audit,
`named-role-age-cycles-v1` adds 1,464 frames across 13 named identities and
`crowd-life-stage-cycles-v1` adds 900 frames across 75 plausible age/role
combinations for all 30 crowd identities. Along with the 528 frames in the
three existing named-family/friend age packs, named-age concepts now cover all
20 named identities. Exact available stages are in each new package manifest.

The player lifecycle is still split across multiple visual branches; two
single-pose eight-stage sheets and the linked movement aggregate are concepts,
not one reconciled, appearance-preserving production character. All age
manifests remain `runtimeReady: false`; this update changes concept coverage
only and does not promote any production-catalog item.

## Scope and interpretation

The catalog contains **55** `pixel-sprite-family` entries: five player ages, 20
named families, and 30 crowd families. This report maps every catalog ID to
observed concept manifests. A `full-frame concept` has the catalog's requested
frame count and four views in a concept package. `partial concept` means frames
exist but a required state, direction vocabulary, identity, or canonical mapping
still needs work. `gap` means no candidate concept was found. These labels do
not change catalog status and do not imply runtime readiness: every inspected
concept manifest remains `runtimeReady: false`.

The catalog asks for 24 frames for player and named families and 12 frames for
crowd families. For this audit, a 24-frame family means four directions × four
walk phases (`contact-a`, `passing-a`, `contact-b`, `passing-b`) × `idle` ×
`interact`; a 12-frame crowd family means four directions × `walk-a`, `walk-b`,
and `idle`. The direction names are recorded exactly as observed; `front/back/
left/right` is not silently treated as the catalog's cardinal vocabulary.

## Player ages (5)

| Catalog ID                                             | Candidate concept package and stage                                                                                                                                                                                                                                     | Observed coverage                                                                                                                                       | Evidence status                                     |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| `liveit.prod.v1.pixel.sprite.world.player-child`       | [`linked-life-arc-family-v2`](../apps/player/assets/pixel/original/linked-life-arc-family-v2/manifest.json), `child-walk`                                                                                                                                               | 24 refs: 4 dirs (`south`, `west`, `east`, `north`) × 4 movement phases + `idle`/`interact`; 24 is aggregated from the linked movement and pose packages | full-frame concept                                  |
| `liveit.prod.v1.pixel.sprite.world.player-teen`        | [`linked-life-arc-family-v2`](../apps/player/assets/pixel/original/linked-life-arc-family-v2/manifest.json), `teen-walk`                                                                                                                                                | 24 refs, 4 cardinal dirs, 4 movement phases + `idle`/`interact`                                                                                         | full-frame concept                                  |
| `liveit.prod.v1.pixel.sprite.world.player-young-adult` | [`linked-life-arc-family-v2`](../apps/player/assets/pixel/original/linked-life-arc-family-v2/manifest.json), `young-adult-woman` and [`linked-male-adult-cycles-v1`](../apps/player/assets/pixel/original/linked-male-adult-cycles-v1/manifest.json), `young-adult-man` | 24 refs per presentation branch: 16 movement + 8 pose refs, 4 dirs; two identity branches are candidates for one catalog slot                           | partial concept (two unmerged canonical identities) |
| `liveit.prod.v1.pixel.sprite.world.player-midlife`     | [`linked-life-arc-family-v2`](../apps/player/assets/pixel/original/linked-life-arc-family-v2/manifest.json), `midlife-woman` and `linked-male-adult-cycles-v1`, `midlife-man`                                                                                           | 24 refs per presentation branch: 16 movement + 8 pose refs, 4 dirs; two identity branches are candidates for one catalog slot                           | partial concept (two unmerged canonical identities) |
| `liveit.prod.v1.pixel.sprite.world.player-elder`       | [`linked-life-arc-family-v2`](../apps/player/assets/pixel/original/linked-life-arc-family-v2/manifest.json), `elder-woman` and `elder-man`; [`linked-elder-poses-v1`](../apps/player/assets/pixel/original/linked-elder-poses-v1/manifest.json)                         | 24 refs per elder presentation branch: 16 movement + 8 pose refs, 4 dirs; one catalog ID has two candidate gender presentations                         | partial concept (ambiguous canonical identity)      |

The linked aggregate explicitly says its stages are separately generated and need
human identity reconciliation. The adult pose studies are therefore counted as
observed concept references, not as proof of one continuous final player.

## Named families (20)

| Catalog ID                                         | Candidate concept package                                                                                                                                  | Observed coverage                                                                                                                | Evidence status    |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `liveit.prod.v1.pixel.sprite.named.amelia`         | [`named-characters-batch-v1`](../apps/player/assets/pixel/original/named-characters-batch-v1/manifest.json), `amelia`                                      | 24 frames; 4 dirs (`south`, `west`, `east`, `north`) × walk phases `contact-a/passing-a/contact-b/passing-b` + `idle`/`interact` | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.noah`           | [`named-characters-batch-v1`](../apps/player/assets/pixel/original/named-characters-batch-v1/manifest.json), `noah`                                        | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.teacher`        | [`named-characters-batch-v1`](../apps/player/assets/pixel/original/named-characters-batch-v1/manifest.json), `teacher`                                     | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.parent-one`     | [`named-characters-batch-v1`](../apps/player/assets/pixel/original/named-characters-batch-v1/manifest.json), `parent-one` / Mara                           | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.parent-two`     | [`named-characters-batch-v1`](../apps/player/assets/pixel/original/named-characters-batch-v1/manifest.json), `parent-two` / Eli                            | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.sibling`        | [`named-characters-batch-v2`](../apps/player/assets/pixel/original/named-characters-batch-v2/manifest.json), `sibling` / Niko                              | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.partner`        | [`named-characters-batch-v2`](../apps/player/assets/pixel/original/named-characters-batch-v2/manifest.json), `partner` / Nora                              | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.child`          | [`named-characters-batch-v2`](../apps/player/assets/pixel/original/named-characters-batch-v2/manifest.json), `child` / Tavi                                | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.grandparent`    | [`named-characters-batch-v2`](../apps/player/assets/pixel/original/named-characters-batch-v2/manifest.json), `grandparent` / Dadi                          | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.mentor`         | [`named-characters-batch-v2`](../apps/player/assets/pixel/original/named-characters-batch-v2/manifest.json), `mentor` / Ishan                              | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.boss`           | [`named-characters-batch-v3`](../apps/player/assets/pixel/original/named-characters-batch-v3/manifest.json), `boss`                                        | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.coworker`       | [`named-characters-batch-v3`](../apps/player/assets/pixel/original/named-characters-batch-v3/manifest.json), `coworker`                                    | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.friend-one`     | [`named-characters-batch-v3`](../apps/player/assets/pixel/original/named-characters-batch-v3/manifest.json), `friend-one`                                  | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.friend-two`     | [`named-characters-batch-v3`](../apps/player/assets/pixel/original/named-characters-batch-v3/manifest.json), `friend-two`                                  | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.neighbor`       | [`named-characters-batch-v3`](../apps/player/assets/pixel/original/named-characters-batch-v3/manifest.json), `neighbor`                                    | 24 frames; 4 cardinal dirs × 4 walk phases + `idle`/`interact`                                                                   | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.shopkeeper`     | [`named-characters-batch-v4`](../apps/player/assets/pixel/original/named-characters-batch-v4/manifest.json), `shopkeeper` / Bellweather shopkeeper         | 24 frames; 4 cardinal dirs × `contact-a`, `passing-a`, `contact-b`, `passing-b`, `idle`, `interact`                              | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.nurse`          | [`named-characters-batch-v4`](../apps/player/assets/pixel/original/named-characters-batch-v4/manifest.json), `nurse` / Bellweather nurse                   | 24 frames; 4 cardinal dirs × `contact-a`, `passing-a`, `contact-b`, `passing-b`, `idle`, `interact`                              | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.physician`      | [`named-characters-batch-v4`](../apps/player/assets/pixel/original/named-characters-batch-v4/manifest.json), `physician` / Bellweather physician           | 24 frames; 4 cardinal dirs × `contact-a`, `passing-a`, `contact-b`, `passing-b`, `idle`, `interact`                              | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.transit-worker` | [`named-characters-batch-v4`](../apps/player/assets/pixel/original/named-characters-batch-v4/manifest.json), `transit-worker` / Bellweather transit worker | 24 frames; 4 cardinal dirs × `contact-a`, `passing-a`, `contact-b`, `passing-b`, `idle`, `interact`                              | full-frame concept |
| `liveit.prod.v1.pixel.sprite.named.cafe-owner`     | [`named-characters-batch-v4`](../apps/player/assets/pixel/original/named-characters-batch-v4/manifest.json), `cafe-owner` / Bellweather cafe owner         | 24 frames; 4 cardinal dirs × `contact-a`, `passing-a`, `contact-b`, `passing-b`, `idle`, `interact`                              | full-frame concept |

## Crowd families (30)

All v1, v2, and v3 rows below have exactly 12 frames in their per-role manifests:
four independently authored cardinal directions (`south`, `west`, `east`,
`north`) × `walk-a`, `walk-b`, `idle`. The v2 package has the same numerical
coverage and now records the canonical cardinal names. Its source folders retain
the legacy labels through `sourceDirection`: `north`←`back`, `east`←`right`,
`south`←`front`, and `west`←`left`; this source mapping is implementation
evidence, not a second direction set.

| Catalog ID                                               | Candidate package / role                                                                                                    | Observed coverage                                                                                   | Evidence status    |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------ |
| `liveit.prod.v1.pixel.sprite.crowd.student`              | [`crowd-archetypes-batch-v1`](../apps/player/assets/pixel/original/crowd-archetypes-batch-v1/manifest.json), `student`      | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.office-worker`        | `crowd-archetypes-batch-v1`, `office-worker`                                                                                | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.store-clerk`          | `crowd-archetypes-batch-v1`, `store-clerk`                                                                                  | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.baker`                | `crowd-archetypes-batch-v1`, `baker`                                                                                        | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.delivery-rider`       | `crowd-archetypes-batch-v1`, `delivery-rider`                                                                               | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.elder-walker`         | [`crowd-archetypes-batch-v3`](../apps/player/assets/pixel/original/crowd-archetypes-batch-v3/manifest.json), `elder-walker` | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.child-playground`     | `crowd-archetypes-batch-v3`, `child-playground`                                                                             | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.gardener`             | `crowd-archetypes-batch-v3`, `gardener`                                                                                     | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.bus-driver`           | `crowd-archetypes-batch-v1`, `bus-driver`                                                                                   | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.taxi-driver`          | `crowd-archetypes-batch-v1`, `taxi-driver`                                                                                  | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.nurse`                | `crowd-archetypes-batch-v3`, `nurse`                                                                                        | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.police-officer`       | `crowd-archetypes-batch-v1`, `police-officer`                                                                               | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.library-visitor`      | `crowd-archetypes-batch-v1`, `library-visitor`                                                                              | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.street-musician`      | `crowd-archetypes-batch-v1`, `street-musician`                                                                              | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.runner`               | [`crowd-archetypes-batch-v2`](../apps/player/assets/pixel/original/crowd-archetypes-batch-v2/manifest.json), `runner`       | 12; `south/north/west/east` × `walk-a/walk-b/idle`; `sourceDirection` preserves legacy folder names | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.tourist`              | `crowd-archetypes-batch-v2`, `tourist`                                                                                      | 12; `south/north/west/east` × `walk-a/walk-b/idle`; `sourceDirection` preserves legacy folder names | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.teacher`              | `crowd-archetypes-batch-v3`, `teacher`                                                                                      | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.caregiver`            | `crowd-archetypes-batch-v3`, `caregiver`                                                                                    | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.mechanic`             | `crowd-archetypes-batch-v2`, `mechanic`                                                                                     | 12; `south/north/west/east` × `walk-a/walk-b/idle`; `sourceDirection` preserves legacy folder names | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.artist`               | `crowd-archetypes-batch-v2`, `artist`                                                                                       | 12; `south/north/west/east` × `walk-a/walk-b/idle`; `sourceDirection` preserves legacy folder names | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.filmmaker`            | `crowd-archetypes-batch-v2`, `filmmaker`                                                                                    | 12; `south/north/west/east` × `walk-a/walk-b/idle`; `sourceDirection` preserves legacy folder names | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.athlete`              | `crowd-archetypes-batch-v2`, `athlete`                                                                                      | 12; `south/north/west/east` × `walk-a/walk-b/idle`; `sourceDirection` preserves legacy folder names | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.shopper`              | `crowd-archetypes-batch-v2`, `shopper`                                                                                      | 12; `south/north/west/east` × `walk-a/walk-b/idle`; `sourceDirection` preserves legacy folder names | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.barista`              | `crowd-archetypes-batch-v2`, `barista`                                                                                      | 12; `south/north/west/east` × `walk-a/walk-b/idle`; `sourceDirection` preserves legacy folder names | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.parent-with-stroller` | `crowd-archetypes-batch-v3`, `parent-with-stroller`                                                                         | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.pet-walker`           | `crowd-archetypes-batch-v2`, `pet-walker`                                                                                   | 12; `south/north/west/east` × `walk-a/walk-b/idle`; `sourceDirection` preserves legacy folder names | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.market-vendor`        | `crowd-archetypes-batch-v2`, `market-vendor`                                                                                | 12; `south/north/west/east` × `walk-a/walk-b/idle`; `sourceDirection` preserves legacy folder names | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.security-guard`       | `crowd-archetypes-batch-v3`, `security-guard`                                                                               | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.historian`            | `crowd-archetypes-batch-v3`, `historian`                                                                                    | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |
| `liveit.prod.v1.pixel.sprite.crowd.park-cleaner`         | `crowd-archetypes-batch-v3`, `park-cleaner`                                                                                 | 12; `south/west/east/north` × `walk-a/walk-b/idle`                                                  | full-frame concept |

## Duplicate and ambiguous mappings

- `teacher` is both a named family and a crowd family. The exact named package
  is [`named-characters-batch-v1`](../apps/player/assets/pixel/original/named-characters-batch-v1/manifest.json);
  the crowd teacher is a separate 12-frame role and is not counted toward the
  named 24-frame family.
- `nurse` is now covered by the exact named v4 family. The separate crowd nurse
  remains a distinct 12-frame crowd role and is not counted toward the named
  24-frame family.
- `cafe-owner` is now covered by the exact named v4 family. Noah's café
  supervisor concept and the crowd barista remain separate role analogues and
  are not silently merged into the catalog ID.
- `player-young-adult`, `player-midlife`, and `player-elder` each have multiple
  presentation branches in the linked aggregate. Their counts are recorded per
  branch, but no branch is selected as canonical here.
- The named v1/v2/v3/v4 and crowd v1/v2/v3 manifests have distinct batch IDs and
  independent hashes. Identical frame counts across packages do not imply
  deduplication or identity continuity.
- [`named-family-age-cycles-v1`](../apps/player/assets/pixel/original/named-family-age-cycles-v1/manifest.json)
  adds nine supplemental age-stage variants for Mara, Eli, and Niko (216 frames).
  They are continuity expansions for recurring named identities, not additional
  catalog rows and not replacements for the single-stage named-family entries.
- [`named-family-age-cycles-v2`](../apps/player/assets/pixel/original/named-family-age-cycles-v2/manifest.json)
  adds seven supplemental stages for Nora and Tavi (168 frames), including
  Tavi's toddler-to-young-adult progression. These stages extend named-person
  continuity beyond the base catalog rows and remain concept-only.

## Missing features after movement coverage

The catalog's 24-frame named/player target includes `idle` and `interact`; the
12-frame crowd target currently includes only `walk-a`, `walk-b`, and `idle`.
The following work is still required even for rows marked full-frame concept:

- human pixel cleanup, palette approval, pivot and collision-box review;
- runtime atlas intake, nearest-neighbour import validation, and device capture;
- identity continuity review for all age branches and named role analogues;
- authored crowd interaction states if crowd roles need gestures, held-object
  actions, or conversation staging beyond their catalog walk target;
- verify the crowd v2 `sourceDirection` mapping during runtime intake while
  retaining the canonical `south/north/west/east` manifest directions;
- visual cleanup, identity review, and renderer intake for the new v4 named
  families (`shopkeeper`, `nurse`, `physician`, `transit-worker`, and
  `cafe-owner`);
- explicit canonical selection and reconciliation for the three multi-branch
  player ages.

## Reproducible audit method

The audit was produced from the current worktree without changing the catalog or
any manifest. The catalog row count and IDs can be reproduced with:

```sh
cd /Users/swayamsingal/Desktop/projects/LIVEIT-iteration2
python3 - <<'PY'
import json
d = json.load(open('content/production-assets/v1/pixel-world.json'))
rows = [e for e in d['entries'] if e['category'] == 'pixel-sprite-family']
assert len(rows) == 55
assert sum(e['group'] == 'world' for e in rows) == 5
assert sum(e['group'] == 'named' for e in rows) == 20
assert sum(e['group'] == 'crowd' for e in rows) == 30
for e in rows:
    print(e['id'], e['framesRequired'], e['viewDirections'])
PY
```

For each candidate package, inspect its root `manifest.json`, then any nested
per-role manifest referenced by `roles[].manifest`. The observed counts in this
report were taken from those manifest records, not from PNG filename counts.
