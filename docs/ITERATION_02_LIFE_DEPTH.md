# LIVEIT — Iteration 02: Life Depth, Activities and NPC Memory

**Branch:** feat/liveit-continuous-pixel-life · Draft PR #10 · Unreleased feature branch.

## Implemented code paths

### 31 deterministic life activities

Family, learning, friendships, fitness, creative practice, career, wellbeing and leisure each have original context-dependent activities. They execute against the canonical World save, applying finances (integer pence), wellbeing, skills, trust, stress and reputation. Activities are age-gated, some require walking to an appropriate district, each action has a daily cooldown, and players have four planned activity slots per virtual day. Minors do not pay personally while household finances remain a later feature.

Source: packages/simulation-core/src/dailyActivities.ts
UI: apps/player/src/ArcadePixelLife.tsx → ACTIVITY
Regression: tests/daily-activities.test.ts

### Lifelong event memory

Monthly progression records once-only life milestones, from early family experiences and birthdays through school, adulthood and later decades. Guardian trust does not decay merely because a newborn cannot repeatedly tap the conversation UI. A childhood skip preserves intermediate events; legacy adult saves do not acquire invented retrospective childhood milestones.

Source: packages/simulation-core/src/lifeMilestones.ts
Regression: tests/life-milestones.test.ts

### Real local-model NPC conversations

The player can converse with separate NPC personalities: parents Mara and Eli, adult friend Amelia, Noah and a childhood classmate, provided those people exist in the life and age requirements are met. NPC prompts are grounded in the saved world: trust, age, relevant story memories and recent events. Transcripts are stored separately per NPC. Only a successful real Ollama reply creates a bounded memory receipt; connection errors do not fabricate AI speech or reward friendship. Relationship gain from a successful conversation is limited to once per day. The AI never directly changes authoritative money or quests.

Source: packages/simulation-core/src/npcMemory.ts
UI: Arcade LIFE → PEOPLE or FAMILY → TALK
Regression: tests/npc-world-memory.test.ts

### Fullscreen social and journal UI

Activities, NPC roster and memories now open in world-preserving overlays, not a separate card-first player. The journal lists actual saved story consequences, simulation events and NPC memories. The chapter shelf, missions and local model settings remain accessible.

## Acceptance tests and QA

- Run npm ci and npm run check (TypeScript, lint, tests).
- Run web and native asset exports; inspect CI outcomes per commit.
- Start a birth-first life, use a family action, advance one month, and reload.
- Verify a relationship, completed activity and NPC transcript survive a restart.
- Disable Ollama to confirm explicit errors; then run npm run ai:check with a real local model.
- Verify location-restricted activities at café/garden/market, and daily exhaustion/reset.
- Inspect actual iOS simulator install/launch and later measure device 60/120 FPS.

## Still unfinished

These are working slices, NOT all BitLife/Episode features. There is no complete multi-generation family engine, on-device packaged LLM, dynamic population and building interiors, layered age-specific pixel sprites, streaming NPC responses, worldwide travel/economic simulation, comprehensive romance/fertility engine, or real-user anonymous chat. Real-person anonymous chat remains disabled until adult eligibility, moderation, report/block and privacy retention exist. Source ZIP assets with nonredistribution terms are not shipped.

See MASTER_GAME_FEATURE_PARITY.md for the 323-item acceptance inventory. Nothing is marked complete without functional and real-device evidence.
