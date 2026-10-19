# LIVEIT Iteration 03 — School, Household, Careers, Procedural Civilians

Branch: feat/liveit-continuous-pixel-life. Draft PR #10. This is a working-development slice, not a released game.

## Gameplay systems

### Family household (separate from infant cash)

Newly created newborn lives have a family home ledger: parental income, monthly bills, household savings, dependents and arrears. The budget reconciles exactly once per completed calendar month, produces memories for deficits, and never directly credits the infant's personal bank balance. The user can see this in HOME without leaving the game view. Previous adult saves remain readable because household is an optional v1 schema field.

### School from five to eighteen

A persistent school record tracks enrollment phase, grades, attendance, engagement, disciplinary points, club membership, study sessions and graduation results. It progresses through primary, secondary and graduation; the final score depends on attendance, actual player decisions, discipline and study, not on automatic age-only rewards. Playable SCHOOL actions include study, classes, help from teachers, friendships, four clubs and skipping classes with consequences. Professional careers are age-gated at 18.

### Careers in the actual life save

CAREER presents the repository's existing technology, creative, business and community job paths as playable actions. Applications, interviews, hiring, promotions and resignation affect salary, job title, reputation and real employment state. Rejections or lack of experience return explicit explanations rather than fake results.

### Infinite world reload and ambient lives

Saving and loading street positions now validates against the _seeded procedural map_ rather than the old 30x23 starter town. Travel outside the original town no longer silently snaps back on reload. Generated neighborhoods spawn a bounded set of seeded visual pedestrians on walkable sidewalks. Their commuting, work, leisure and nighttime patterns change with the in-game clock; civilians currently provide ambient population and are not full dialogue-capable agents.

### Local model context

Successful local Ollama conversations already persist character-specific receipts and past memories. Their canonical system prompt now also reflects real school performance and household conditions. Generated replies still have zero authority to directly change game finances, NPC relationships or quest flags.

## Source ownership and tests

- packages/world-schema/src/lifeSystems.ts — optional strict household and school contracts
- packages/simulation-core/src/familySchool.ts — budgets, school actions and monthly education
- packages/simulation-core/src/birthLife.ts and index.ts — initialize and tick school/household
- packages/simulation-core/src/life.ts — enforce professional career age eligibility
- apps/player/src/ArcadePixelLife.tsx — SCHOOL, HOME, CAREER panels; streamed ambient pedestrian render; save restore
- apps/player/src/proceduralWorld.ts — procedural position validation
- apps/player/src/ambientPedestrians.ts — deterministic time-dependent crowd
- tests/family-school.test.ts — enrollment, study, grades, household and save migration
- tests/procedural-world.test.ts — saved off-map positions
- tests/ambient-civilians.test.ts — culling, determinism, non-solid terrain and time-of-day

## Iteration acceptance

1. Birth-first life has no personal money but household funds that actually change after a month.
2. School unlocks at five; study/attendance/truancy alter outcomes; graduate at 18.
3. Job applications fail for children and can succeed or fail as adults based on real skills.
4. Travel far outside starter map, reload and keep exact valid position.
5. Civilian pedestrians are deterministic, stay within the camera window, avoid solid tiles and vary by time.
6. npm run check succeeds on a clean checkout, not only after hidden CI format normalization.
7. Real iOS simulator build, launch, touch, clock and performance QA are still separately required.

## Remaining limitations

School currently uses an over-world overlay rather than explorable classroom interiors. Household members have a limited scripted cast and no complete genetic/inheritance system. Career tracks are limited. Ambient civilians are non-interactive, not yet persistent independent NPCs. Procedural neighborhoods need authored land uses, interiors, stores, roads, true NPC schedules and multi-region streaming. A bundled on-device LLM and 60/120 Hz performance validation are not completed. Real-user stranger chat is not enabled; no minors will be matched with unknown adults.

## Formatting repair

The prior branch was valid after CI ran npx prettier --write but its source tree was unformatted, so local npm run check stopped early. A one-time GitHub Actions workflow should commit prettier normalization back onto this feature branch when this document lands. If that workflow cannot push, the safe local fallback is npm run format && npm run check. Never run npm audit fix --force without a dependency review.

Track the remaining requirements in MASTER_GAME_FEATURE_PARITY.md. Boxes remain unchecked until user-facing acceptance tests and mobile QA pass.
