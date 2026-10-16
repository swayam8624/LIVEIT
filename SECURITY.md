# Security

The foundation is a local prototype, without authentication or a deployed backend. Saves are local, unencrypted application data and can be edited by their device owner. They must never authorize server-side rewards or account actions. Do not store secrets or personal information in story metadata.

Story packages are untrusted data. Runtime Zod validation rejects unknown fields, operations, excessive effect values, undeclared targets, invalid destinations, unreachable scenes, and graphs without a possible ending. Conditional scenes require an unconditional fallback. Only relationship adjustments and memory creation are allowed. No eval, user code, network access, filesystem access or arbitrary object paths are supported.

Permissions currently restrict the supported safe operations and named cast. A production publisher must also validate requested permissions against platform-granted capabilities; author declarations are not a server authorization policy. Schema limits do not replace byte-level upload limits or moderation.

Corrupt or newer saves fail explicitly and are not silently overwritten. Storage write failures are shown. Public security-reporting contacts and a supported-version policy must be configured before launch. Until then, report issues privately to the project owner rather than publishing sensitive details in a public tracker.
