# Backend design: intentionally not deployed

The foundation keeps backend work to contracts and service boundaries until the local gameplay loop is proven. The future TypeScript API should use PostgreSQL for accounts, versioned save manifests, creator ownership, publication state and moderation records; immutable story JSON and assets belong in object storage behind a CDN.

## Domain modules

Identity owns accounts and sessions. Saves owns per-account timeline revisions and optimistic concurrency. Catalogue owns immutable story identities, versions and compatible worlds. Publishing owns compile/test/review/release transitions. Assets owns provenance, content hashes, rig compatibility and usage rights. Moderation owns reports, decisions, appeals and blocking. None should receive unrestricted mutation access to another domain.

## Planned contracts

- Load save by account and timeline, returning schema version, state, revision and ETag.
- Update save only against an expected revision; conflicts preserve both candidates for explicit resolution.
- Resolve story by immutable ID/version and verify its package hash.
- Upload a private draft with byte and schema limits; server revalidates graphs and platform-granted capabilities.
- Request review of a frozen draft version; public release requires moderation and rights metadata.

Authentication, authorization and ownership checks belong on every server operation. Never accept a client-provided account ID as proof of ownership. No raw SQL or migrations are included because no database behavior is implemented. Add schema migrations, transaction tests, an object-storage adapter, deployment configuration and integration tests when this service is commissioned. Do not represent the current Studio export as publication.
