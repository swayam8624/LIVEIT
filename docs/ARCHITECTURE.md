# Architecture and contracts

## Ownership

World schemas define authoritative characters, relationships, structured facts, memories, event history and story progress. Simulation owns day ticks and systemic changes. Narrative owns scene selection, conditions and campaign progress. Consequences owns the restricted effect transaction. Saves own versioned envelopes and storage. Both UI applications consume these packages as workspace source modules. Runtime validation uses Zod; packages have no UI dependency.

A player action follows: validate world and story → confirm compatibility and cast → resolve available choice → clone → validate/apply permitted effects → update progress → record history → validate complete result → return. Inputs remain unchanged on failure. The UI stores only a successfully produced world. Duplicate or stale scene choices cannot reapply effects after progress moves. Cyclic graphs are permitted if every scene can reach an ending; intentional repeated loops can still accumulate effects and must be considered during editorial review.

## Persistence

Save version 1 has an active continuity, a required life and an optional standalone story. Each world has schema version 1 and a timeline ID. Story progress pins ID and version. No automatic timeline merging. All state uses serializable data, simulated integer days and integer pence. Storage is injected as asynchronous getItem/setItem. The player serializes writes through a promise queue to avoid out-of-order autosaves. Read failures preserve the existing stored bytes; write failures remain visible and allow retry.

Save migrations are not implemented: unsupported versions are rejected. Add migrations with immutable fixtures before introducing version 2. Local storage is not a cloud backup. The application is local-first; installable offline web caching and concurrent multi-tab edit resolution are future work. Snapshots currently contain full history; retention limits require compaction before long campaigns.

## Compatibility and safety

Only modern_life_v1 is supported. Stories declare an age requirement and named effect targets. All targets must exist. Conditions are finite fact or minimum-trust checks. Effects are only bounded relationship changes and structured memories. Schema checks cover unique scene/choice identities, references, reachability, ending paths and fallback choices. Derived prose summaries are not authoritative. Declarative permissions do not yet constitute a production publication capability policy.

## Presentation

React Native primitives render the same gameplay UI on each target. The temporary layered café and breathing animation prove scene presentation without locking the foundation to an unbenchmarked renderer. Native driver transforms animate the reusable character layer. A later renderer adapter can read scene/cast/mood data while leaving simulation unchanged. Native fonts, safe areas, screen readers, reduced-motion behavior, clipping and low-end performance need native QA before release.

## Tooling decisions

npm workspaces avoid extra orchestration dependencies. Expo and Next handle source workspace transpilation. TypeScript, ESLint, Prettier and Vitest supply static and behavioral checks. No database, cloud account, analytics or AI key is needed for this sprint. The implementation checked current package metadata and official [Expo monorepo guidance](https://docs.expo.dev/guides/monorepos/) and [Next installation guidance](https://nextjs.org/docs/app/getting-started/installation) during setup.
