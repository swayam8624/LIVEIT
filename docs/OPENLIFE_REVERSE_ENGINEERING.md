# OpenLife → LIVEIT reverse-engineering dossier (phase 1)

> Source inspected 2026-10-18: [WinFan3672/OpenLife](https://github.com/WinFan3672/OpenLife), archived mirror (version 0.2.1, 2023); its README redirects to `https://codeberg.org/WinFan3672/OpenLife`. The user supplied `codeberg.org/OpenLife/OpenLife.git`, which is **not** the redirect shown by the mirror. Inspect and verify the Codeberg upstream separately before treating it as the same revision.
>
> Mirror: one 9,431-line `openlife.py` Python program, mostly a terminal life simulator, MIT-licensed. It is a **reference**, not a production engine for the phone. Keep its license/notice with copied substantial portions. This implementation intentionally rewrites mechanics instead of importing its monolith.

## Inventory grounded in the archived code

| Domain | OpenLife source | LIVEIT target |
|---|---|---|
| Life/player progression | `Person`, `Player`, age-up and yearly menu | deterministic annual transition, birth→death, visible consequence reel |
| Family & social | `Parent`, `Child`, `Friend`, `Spouse`, `Ex`, `makeFriend`, `loveMenu` | persistent family graph, birth/adoption, NPC autonomy, courtship and breaks |
| Education & work | `university`, `uniApplication`, `jobInterview`, `Job`, `CoWorker`, `freelanceWork` | school grades, scholarships, working contract and job ladder |
| Investing | `Bond`, `Crypto`, `Metal`, `IndexFund`, `Stock`; `investMenu` | ledger-based playable instruments with stochastic macro regimes and reproducible seed |
| Housing | `House`, `buyHouse`, `houseInteract` | rent, mortgages, property upkeep/depreciation, moving |
| Vehicles | `Vehicle`, `Car`, `Boat`, `Plane`, dealerships/docks/hangar | purchase, resale, upkeep, optional travel interactions |
| Law & justice | `Offence`, `adultCrime`, `robBank`, `lawsuit`, `prison` | crime risks, court outcomes, incarceration, reputation |
| Health | `Surgeon`, `doctorMenu`, `rehab`, illness states | symptoms, conditions, healthcare access, recovery and mortality |
| Fame/creator | `OpenTube`, `createChannel`, `openTube` | content-creator reputation/economy route |
| Legacy & progression | `Achievement`, `grantAchievement`, `die`, ribbons, lifetime statistics | achievements, multiple endings, heirs, unlocked traits and Life Recap |
| Special routes | `myLab`, `researchLab`, `emigrate`, `adoption` | researcher, immigration, family and extraordinary outcome arcs |
| Save/load | `saveGame`, `loadGame`, converters | schema migrations, event log, offline persistence, backed-up snapshots |

This is a **mechanics inventory**, not an assertion that each upstream mechanic is balanced, complete or bug-free. Audit each function's state mutation, probability, UI wiring, and tests before adapting it.

## Problems to avoid when porting

1. OpenLife combines rules, UI, input, text, persistence and randomness in one file. Do not transplant its global state, direct `input()` menus or scattered random calls.
2. Multiple game domains use procedural mutable Python objects and ad-hoc save transitions. LIVEIT must reject malformed states and preserve legacy save migration.
3. LIVEIT v1 has a similar *smaller* problem: the player `App.tsx` still coordinates navigation, scene, persistence, world and user actions. Split by domain instead of growing the component.
4. A million generated generic events is less valuable than 150 meaningful, tested, reactive events. Use eligibility/cooldown chains and record durable consequences.
5. Do not copy game titles, art, dialogues, copyrighted assets, or UI from BitLife/Episode/Character.AI. Similar mechanical systems can be original.

## Concrete adoption ledger

- [x] Read archived OpenLife 0.2.1 source inventory (classes/functions/menus).
- [x] Map investment and housing/vehicle mechanics to a validated, pure TypeScript portfolio domain.
- [x] Wire portfolio purchase, sale, index investing and annual upkeep into LIVEIT life + mobile UI.
- [x] Add regression tests for old saves, financial exploits, deterministic annual repricing and input validation.
- [ ] Inspect Codeberg upstream latest revision (unavailable in current environment; do **not** assume mirror is current).
- [ ] Complete function-level audit and parity tests for education, family, health, legal, travel, entrepreneurship and achievements.
- [ ] Replace age-23 start with data-driven birth backgrounds, lifetime progression and legacy.
- [ ] Add seeded event director and 10,000-life statistical balancing harness.
- [ ] Replace the current stylized-primitive avatars with original layer-based 2.5D animated rigs.
- [ ] Implement the account/service layer with real deployed persistence and abuse handling.

## Design contract

Every new domain needs a state schema, zero-dependency pure transition function, append-only timeline event, error/failure outcomes, displayed actionable UI, accessibility semantics, save round-trip tests, and gameplay balance checks. UI controls must never be labelled "working" unless a full action including state effects and storage has been demonstrated. Signed native binaries and iOS simulator tests are distinct from browser screenshots and JS exports.
