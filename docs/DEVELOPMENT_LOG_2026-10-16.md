# LIVEIT implementation and visual verification log — 16 October 2026

## Product objective

Two equally complete games — an open-ended Free Life simulation and a branching cinematic Story Mode — share a validated, deterministic world model. A browser Creator Studio can author compatible narratives. Gameplay is ad-free and meaningful decisions require no purchase.

## Completed and committed on `design/immersive-gameplay-v1`

- New dark, atmospheric interface foundation and compact responsive game navigation.
- Bundled original café location art and Amelia portrait. The café preview was replaced after byte-level validation exposed a corrupted initial sample; it is still intentionally low resolution. Full original ChatGPT art is available in the conversation's concept pack.
- `GameStage`: offline image-backed scene, narrative mood tint, legible overlay regions, optional ambient animation governed by OS reduced-motion preference, and a stage responsive to the available width.
- Free Life: first-screen scene destinations perform actual typed work/study/rest/social/café actions; simulation pace selectors and optional advanced planner rather than the old dashboard as the default interaction.
- People screen: persistent NPC relationship values, portrait/placeholder, trust meters, and grounded actions.
- Story Mode: shared illustrated stage with a persistent dialogue dock, character speaker portrait and original branching consequences.
- Creator Studio: visual scene editing, choice text/destination changes, connected-scene creation, new story templates, previous-draft backup/restore, validated JSON import/export and copy to the player.
- Local story shelf in the player: validated JSON package ingestion, limited offline library, preserved timeline changes and protection against deleting/replacing packages referenced by a save.
- Save compatibility: optional `activeStoryId` field in the existing v1 schema preserves legacy saves while allowing imported stories to be restored on reload. Missing content produces a recoverable warning rather than silently corrupting the saved life.
- Test additions for creator package roundtrip, security restrictions, v1 compatibility and imported scene restoration.
- Release asset preparation tooling: `tools/prepare_art.py` and `tools/install_concept_art.py`, including hashes and a provenance manifest.
- CI: Prettier, ESLint, strict TypeScript, Vitest, Expo web/Studio production builds, and Hermes iOS/Android **bundle exports only**. Bundle exports do not demonstrate signed native binaries or tested phone interaction.
- Separate visual-review workflow: Playwright-driven web onboarding, Free Life, Story Mode and Studio screenshots at phone/desktop sizes. This is a browser smoke test, not a native certification. Files are attached as workflow artifacts to each run.

## Visual defects discovered by screenshot review

- The first generated sample JPEG rendered as a distorted horizontal strip: replaced with a byte-verified original photo preview (real Git blob SHA checked against source bytes).
- Story Mode's stage initially used a constrained flex wrapper and was not reliably full-width: replaced with an explicit width contract.
- Small-device navigation previously overflowed the viewport: allocated equal space to four buttons.
- The ScrollView preserved its prior offset when a new life or story scene opened: added an instance ref to restore top-of-screen navigation.
- The Creator Studio automated smoke test initially stalled when creating a new story: introduced a recoverable previous-draft backup and switched the test to the supported local Next.js development origin.

## Current limitations / blockers

1. **Art**: no layered transparent actor sprites, no pose/expression rig, no true city map, and no separately painted locations. Visual screenshots must be reviewed on actual devices; a tiny preview image is not approved launch art.
2. **Creator ecosystem**: local import is real, but there is still no public backend, verified author accounts, content moderation, copyright review or public publishing pipeline.
3. **Story authoring**: the Studio preview follows branches but does not apply actual world consequences; advanced condition/effect editing remains partly raw JSON.
4. **Platform release**: no signed TestFlight/Play internal distribution builds, production hosting, privacy policy or store compliance approval yet.
5. **Test coverage**: browser screenshot smoke tests are useful but are not a substitute for verified deterministic end-to-end native testing and save migrations.
6. **Gameplay scale**: one complete short encounter and a constrained simulated city do not yet represent a full game.

## Next technical milestones

- Approve and install full-resolution art pack locally, optimize for multiple device resolutions and validate privacy/licensing records.
- Separate game scene backgrounds by location; build a reusable full-body character rig with actual expression swapping and transitions.
- Use the same narrative/consequence engine inside Creator Studio's preview, not only its branching text navigation.
- Extend Free Life with event scheduling, multi-actor NPC simulation, additional careers and location-specific choices, and maintain deterministic test traces.
- Add secure author accounts, story version pinning, review/moderation queue and a download/catalog service.
- Confirm TestFlight and Google Play internal builds on real devices, then prepare store submissions.

## Important verification policy

Never claim that web bundle exports prove functional iOS/Android. Do not merge into `main` or call this beta-ready until CI is green, screenshots have been reviewed, and an actual device smoke test has been performed. The design branch is an implementation preview, not a launch release.
