# Chat reaction icons v1

Original, deterministic pixel clusters for expressive chat and social feedback. Six character identities each receive ten age-safe sticker reactions: heart, laugh, surprise, comfort, thinking, celebrate, wave, thanks, apology, and consent. The consent frame contains only affirmative/negative symbols; labels and accessibility text stay external.

The contact-status atlas adds online, offline, typing, unread, saved, error, and muted symbols. Bubble tails and avatar badge frames are separate transparent primitives so the chat renderer can compose them without embedding text.

All files are concept-only (`runtimeReady: false`) until imported into the renderer, reviewed at the game's pixel scale, and wired to accessible labels and state behavior. No downloaded or third-party asset bytes were used. See `manifest.json` and `provenance.json` for exact hashes and generation record.
