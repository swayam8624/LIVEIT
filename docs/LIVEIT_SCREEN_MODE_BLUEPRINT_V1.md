# LIVEIT — Screen & Mode Design Blueprint (GDS-002)

**Step 2 of 5, after GDS-001:** detailed visual screen specifications, responsive geometry, navigation, screen states and interactions. **Status: design only**, not proof these screens are implemented. Superseded aesthetic: an isometric low-poly Vulkan city as the primary Free Life world. The committed [GDS-001](LIVEIT_GRAPHICS_DESIGN_SPEC_V1.md) is authoritative: ORIGINAL handheld-era **top-down pixel overworld**, premium **smooth stylized 3D** for significant conversations/stories, and **tactile widgets and HUD** as the shared interaction layer. Preserved gameplay source: simulation, city districts, stories, saved identity, memories; new visuals must not change world facts.

**Purpose:** every screen must be designable, implementable, testable and navigable without guessing about gestures, overlays, empty/error states, mobile breakpoints or UI layering. This spec deliberately lists **target screens** beyond the current repo; only a few existing RN screens currently work. No copyrighted Pokémon/Episode/BitLife artwork or screen cloning is authorized.

## A. Master screen identity and design tokens

- Design basis: **390×844 pt** reference modern phone in portrait, with physical safe areas; minimum target width **320 pt**. Do not scale bitmap UI fonts with pixel-world sampling. Responsive UI uses dp/pt layout, not game pixels.
- Narrow phone <=359pt: summary-only top HUD and tighter drawers; standard portrait 360–599pt: one-handed bottom and slide-in edge panels; small tablet 600–999pt: single pinned contextual rail; landscape and tablet >=1000pt: left navigation (208–256pt), world centered, right context (260–340pt), retaining immersive cinematic letterboxing when appropriate.
- Physical safe areas: top strip begins below OS status/notch; bottom controls avoid home indicator; keyboard recomputes available viewport before camera; notch/rotation never crops an avatar or decision label.
- Pixel world target: logical **320×256**, 16×16 source tiles, crisp nearest filtering, camera framing adapted by crop/letterbox with full tile alignment and an independent pixel-friendly interaction hit map. Main actor 16×24 logical px plus 4 cardinal walk directions.
- Cinematic: independent full viewport **3D native Vulkan/MoltenVK** target with authorable scene lighting, stable eyelines, text dock and camera compositions; no in-world bitmap dialogue.
- HUD: background #101827, main surfaces #1A2737, raised #223449, ink #F5F2D9, muted #B6C6C8, mint #97E6AC, amber #FFD28A, coral #F49A82, borders #507174, errors #FF7588. World palettes vary by district, weather, life-stage; do NOT recolor cinematic skin or every pixel with HUD navy.
- Text: condensed arcade heading, mono compact meters, real scalable dialogue text. Brand display 26–38sp, body 16–18sp, dialogue 18–22sp. Secondary HUD >=11sp unless decorative coordinates.
- 44×44pt / 48×48dp practical target floor for primary taps; icon-only actions always accessible-labeled with selected/expanded state; Android/iOS back gesture and physical keyboard Esc close top overlay, never discard draft without confirmation.
- Interaction priority for overlays: **blocking safety/error > irreversible choice > story choice dock > keyboard and conversation > active outcome > sidebar > transient toast**. No two conflicting modal focus traps. Quick taps/rapid events coalesce. Camera game state and player coordinates persist under temporary drawers.
- Everyday navigation: press/sweep virtual pad, tap-to-route accessible option, contextual interact button, map toggle, quick phone and life dashboard. Pinch camera zoom may affect scale only; do not turn top-down mode into a generic free-rotate 3D camera.
- Four animation tiers: instant 0–100ms on input; 100–300ms HUD; 450–750ms warm pixel→cinematic transition; 600–1400ms skippable milestone; no auto-confetti on grief. Haptics Off/Subtle/Full and reduced-motion are cross-screen.
- Central rule: **one saved identity** for each character in avatar editor, pixel sprite, chat, 3D portrait and future legacy view. Separate representations are keyed to one versioned appearance/rig registry, never independently randomized.

## B. Primary navigation map

    DEVICE BOOT / RESTORE
      ├── New user → Character creator → First day intro → Free Roam (OVERWORLD)
      ├── Existing life → Continue saved mode → Free Roam / Story scene / current panel
      └── Recoverable save error → Safe Recovery
    FREE ROAM [anchor mode, world visible underneath]
      ├── NPC / interact → PIXEL BUBBLE → Quick event OR 3D Conversation → Choice → Outcome → Same world coordinate
      ├── Door/entrance → Pixel interior → context actions/occupation/home activity
      ├── HUD Life → Character / Career / Education / Finance / Health / Skills / Inventory / Home / Family / People
      ├── HUD Messages → Inbox (separate NPC AI and real contact labels) → Thread → Report/mute/block/leave
      ├── HUD Map → Local map / District transit / Destination
      ├── HUD Story → Library → Detail → CINEMATIC STORY → Ending/Return
      ├── Age Up → Preflight and confirmation → Age transition → Consequence digest → Resume roam
      ├── HUD Memory → Journal / Album / Flashback / Legacy
      └── Settings → Accessibility, controls, pack storage, save/restore
    CREATOR STUDIO (separate existing Next.js authoring app; creator-facing design appendix)
      ├── Story library → graph/scene editor → authoring preview (pixel and cinema)
      └── Asset library → appearance/rig/animation/scene packing + validation and licensing

**Global quick-open:** on phones, a bottom-left or thumb-reachable side button opens the menu sheet; right-side game-phone chip opens communications. Tablet uses pinned side rails where they do not hide the playfield. Bottom thumb controls hide in modal/cinematic flows. Never show a giant desktop fixed sidebar on 320px phone.

## C. Annotated master wireframe geometry

### C1 — Portrait OVERWORLD (390×844pt base)

    ┌────────── safe OS status  ───────────┐
    │ [LV] AGE 23 · D041  £1,800  ♡ 72   │  HUD top: 48–56pt
    │  BEL L W E A T H E R   ◉ CLOUDY     │  district micro-label 20pt
    ├──────────────────────────────────────┤
    │                                      │
    │        PIXEL WORLD VIEWPORT          │  viewport fills remaining
    │   café   │ road │ market            │  flexible 55–72% height
    │     NPC   🧍 PLAYER    ✦ !          │  in GPU pixel-coordinate space
    │                                      │
    │       ▧ NPC: TALK  / ENTER          │  context floating at actor
    │                                      │
    ├──────── responsive HUD safe ────────┤
    │ [☰]  [← ↑ → ↓ PAD]  [A TALK] [⌕]   │  soft virtual controls or gestures
    │ [⏭ AGE UP]     [☏ PHONE  ●2]        │  persistent time & messages affordance
    └───────── home safe area ────────────┘

Top status is compressible; game world is NEVER a scroll-view of location cards. Left menu/right phone open overlay drawers with a dimmed but still recognizable world backdrop; world simulation may remain active for nonblocking menus but controls are gated appropriately during modal choices.

### C2 — Cinematic 3D scene, phone portrait

    ┌────────── safe OS status ────────────┐
    │ [← LEAVE]           SCENE 03 · ♥ AM │  slim overlay, unobtrusive
    │                                      │
    │     TRUE STYLIZED 3D SET            │
    │     TWO RIGGED CHARACTERS           │  ~52–65% height, adjustable
    │      ACTING / EYE CONTACT           │  full-resolution shader
    │     [LOWER THIRD NAME LABEL]        │
    ├─  dialogue dock (real UI text) ──────┤
    │ AMELIA                               │
    │ “I waited. I didn't know if you...” │  multiline selectable text
    │ [ 1  TELL THE TRUTH            ➤ ] │  primary choice, 52pt min
    │ [ 2  ASK FOR TIME              ➤ ] │
    │ [ 3  LEAVE GENTLY              ➤ ] │
    │  [HISTORY]   [AUTO]   [NEXT]         │
    └──────── home-safe / no overlap ─────┘

3D render sits behind dock; preserve eye-line in upper/middle safe region, and lower camera framing shifts when the dock expands. Dialogue stays accessible and scrollable without scrolling camera objects.

### C3 — Story/choice-to-outcome result layer

    ┌───── same underlying scene ─────────┐
    │ [RECAP]             [PAUSE]          │
    │      THE PERSON STILL EXISTS        │
    │      AND RESPONDS TO THE CHOICE      │
    │                                      │
    │ ┌── WHAT CHANGED ──────────────────┐│
    │ │  RELATIONSHIP   AMELIA           ││
    │ │  Trust +12   ◇ New memory        ││  real simulation deltas only
    │ │  “We spoke honestly.”            ││
    │ │  [VIEW MEMORY]     [DONE]         ││
    │ └───────────────────────────────────┘│
    │ [CONTINUE SCENE] / [BACK TO CITY]    │
    └──────── home safe ──────────────────┘

Feedback is factual and reversible (dismiss only, underlying world already committed). If a choice is pending/saving, show spinner/disabled and an honest retry path rather than pretending commit succeeded.

## D. Complete screen catalog and authoritative variants

Each row below is a **design target**; "existing" means a code pathway with some analogous behavior, not parity with this screen. Master codes are stable across subsequent steps. Any newly scoped content must be added with code, trigger, visual mode, actions, responsive variant and acceptance state.

### S00 — Boot, restore & safe loading

**Visual mode:** system. **Entry:** auto app launch / return after termination.

**Composition:** game logo over a subtle original pixel Bellweather skyline, 1 progress indicator and subtitle; resume still frame if already cached.

**Primary controls:** Continue restored world; no user action until ready. **Required variants:** damaged save / offline / interrupted download / restore compatible.

**State/acceptance:** do not overwrite existing save; retry and accessible error. **Current repo status:** partial (local-save load exists).

### S01 — Title, continue, new life

**Visual mode:** system. **Entry:** fresh install or title menu.

**Composition:** large pixel town silhouette under twilight sky; a cinematic character reflection in central portal; two tactile large start buttons.

**Primary controls:** Continue; Start New Life; Stories; Settings; Credits. **Required variants:** no saves / multiple saves target / existing life replacement confirmation.

**State/acceptance:** Title does not fabricate available saves. **Current repo status:** partial (onboard vs save).

### S02 — New life setup

**Visual mode:** system. **Entry:** Start New Life.

**Composition:** character name/pronouns and optional origin values in a left/bottom card; live avatar split preview showing PIXEL and 3D identity.

**Primary controls:** name field; pronouns; create; appearance; safe restore. **Required variants:** invalid/empty name; keyboard; previous save; permissions.

**State/acceptance:** never erase old save without explicit confirmation. **Current repo status:** partial (name/pronouns/start).

### S03 — Avatar studio (pixel ⇄ 3D preview)

**Visual mode:** hybrid. **Entry:** New Life / wardrobe / relationships portrait.

**Composition:** left pixel 4-direction turnaround with snap grid; right beautiful lit 3D rig close-up; footer tabs for skin/face/hair/body/clothes/accessories.

**Primary controls:** part/category selectors, palette chips, presets, rotate rig, compare, save/cancel. **Required variants:** asset unavailable; malformed rig; age stage; long lists; accessibility.

**State/acceptance:** all parts deterministic from same saved appearance. **Current repo status:** partial (RN 2D paper-doll editor).

### S04 — Free Roam — Bellweather overworld

**Visual mode:** pixel. **Entry:** Continue Life / exit scene / exit door.

**Composition:** top-down 16px authored pixel tiles, pixel NPCs, interactive doorways, lighting/weather, player's avatar centered or camera-follow.

**Primary controls:** walk, sprint, touch route, A interact, age, map, phone, menu. **Required variants:** blocked tile, wall, crowds, blocked door, day/night, rainy, low power.

**State/acceptance:** save exact travel position and district; no 3D low-poly replacement. **Current repo status:** not implemented (district cards only).

### S05 — Pixel interior — home/work/shop

**Visual mode:** pixel. **Entry:** enter door / workplace / school.

**Composition:** top-down pixel furniture with layered occluders, clear exit tile and unique authored interactable props; tasteful room lighting.

**Primary controls:** move; inspect; work/study/shop; leave; talk NPC. **Required variants:** door locked, actor busy, furniture collision, indoor zoom, item unavailable.

**State/acceptance:** door return to original world coordinates. **Current repo status:** not implemented.

### S06 — City transit & fast-travel map

**Visual mode:** system + pixel. **Entry:** world map icon / transit stop.

**Composition:** full-screen layered schematic of original districts, unlockable waypoints and cost/time summary; mini pixel vignette for selection.

**Primary controls:** choose destination, route preview, confirm, back. **Required variants:** unavailable location, not enough money, transit closed, interrupted travel.

**State/acceptance:** travel updates world day/money and destination only after confirmed simulation action. **Current repo status:** partial (visitDistrict exists).

### S07 — NPC approach bubble & quick talk

**Visual mode:** pixel overlay. **Entry:** nearby named person / tap interact.

**Composition:** world freezes actor stance locally while floating bubble with avatar pixel icon, short line, Speak / Ask / Leave; avoid full-screen modal.

**Primary controls:** quick talk; deep talk into 3D; inspect profile; dismiss. **Required variants:** stranger unavailable; NPC scripted busy; deceased/unborn/blocked; no script.

**State/acceptance:** only relationships/entities in saved world. **Current repo status:** not implemented.

### S08 — Cinematic dialogue — two actors

**Visual mode:** 3D + native dock. **Entry:** deep talk / important encounter.

**Composition:** real 3D close-up or two-shot, keyed lights/materials and moving face/eyes/hair, bottom real-text dialogue dock, compact story header.

**Primary controls:** advance, history, auto, skip approved, speaker info, close safely. **Required variants:** loading shaders, missing pack, reduced motion, long dialogue, NPC expression.

**State/acceptance:** actor matches pixel identity and current age; no fabricated outcome. **Current repo status:** partial (RN illustrated dialogue only).

### S09 — Cinematic meaningful choice

**Visual mode:** 3D + choice dock. **Entry:** author choice / important AI NPC beat.

**Composition:** same 3D camera continues moving slightly; 2–4 tall cards over lower 40%, short emotional stance and known costs; selected card accents mint.

**Primary controls:** select/commit, details, cancel when allowed, hold irreversible. **Required variants:** insufficient resources, irreversible choice, double tap, disconnect.

**State/acceptance:** effect is one atomic world action; no fake probability tag. **Current repo status:** partial (story choice buttons).

### S10 — What changed? outcome widget

**Visual mode:** system overlay. **Entry:** confirmed action / job / relationship / purchase.

**Composition:** small stacked upper corner card or portrait bottom sheet, event type icon, one-line summary and 1–4 truthful deltas; view journal link.

**Primary controls:** expand, pin, dismiss, view details. **Required variants:** zero-delta, neutral, grief, simultaneous changes, save pending/error.

**State/acceptance:** do not show success before commit; coalesce fast actions. **Current repo status:** partial (status messages; no widget system).

### S11 — Age Up & life-milestone sequence

**Visual mode:** pixel→3D optional. **Entry:** tap Age Up / chosen year-advance.

**Composition:** pixel year wheel and seasonal street tint with abbreviated time montage; key memories appear as chips; high-impact life moments may open 3D cinematic.

**Primary controls:** advance, skip visual, inspect consequence timeline, continue. **Required variants:** death, hardship, disabled motion, multiple events, low money, no effect.

**State/acceptance:** never auto celebrate tragedy; all ages and consequences from saved world. **Current repo status:** partial (short sim advance).

### S12 — Life hub / stats character

**Visual mode:** system + pixel backdrop. **Entry:** menu / character portrait tap.

**Composition:** character sprite card and smooth portrait thumbnail, wellbeing/energy/skill/career/finance meters, latest real memory, horizontal domain tabs.

**Primary controls:** open domains, apply time action, settings, change avatar. **Required variants:** missing data from old save, oversize values, debt, state stale.

**State/acceptance:** live values from deterministic schema; portrait consistent. **Current repo status:** partial (LifeDashboard).

### S13 — Career, job & workplaces

**Visual mode:** system / pixel interior. **Entry:** Life > Career / workplace interact.

**Composition:** retro ledger with title/employer, salary, experience track, skill requirements and pixel workplace badge; contextual real opportunity cards.

**Primary controls:** search/apply/interview/work/promote/resign; walk to job. **Required variants:** unemployed, job rejected, interview pending, duplicate action.

**State/acceptance:** salary/cash changes persisted; no fictitious open jobs. **Current repo status:** partial (career subsystem).

### S14 — Education & skill progression

**Visual mode:** system / pixel interior. **Entry:** Life > Learning / school.

**Composition:** course/library shelf motif, chronological education cards, pixel campus icon, skill meter and time-cost picker.

**Primary controls:** enroll, attend, study, exams, inspect qualifications. **Required variants:** ineligible, exam failure, age constraints, save upgrade.

**State/acceptance:** learning changes skill, calendar and eligibility only via simulation. **Current repo status:** mostly unimplemented.

### S15 — Relationships constellation

**Visual mode:** system with 3D preview. **Entry:** People / NPC profile.

**Composition:** relationship nodes linked by styled threads, highlighted person triggers live 3D portrait inset; trust category, shared events, last contact.

**Primary controls:** inspect, meet, message, gift if implemented, boundaries. **Required variants:** death, no-contact, estranged, no memory, blocked.

**State/acceptance:** lines have explicit meaning; no invented emotional scores. **Current repo status:** partial (people cards/trust).

### S16 — Family & generations

**Visual mode:** system + pixel domestic. **Entry:** Life > Family.

**Composition:** family-tree cards with same appearance sprites and 3D portrait reveal, lineage and household milestones, relationship history.

**Primary controls:** inspect person, household choice, view legacy. **Required variants:** single-parent, adoption, child aging, deceased relative.

**State/acceptance:** stable unique family IDs and permissions. **Current repo status:** not implemented.

### S17 — Home / inventory / ownership

**Visual mode:** pixel interior + overlay. **Entry:** enter home or inventory.

**Composition:** walkable pixel home and furniture positions; bottom catalog with actual owned items, equip/dress/inspect and asset provenance.

**Primary controls:** interact, place, equip, move, sell, view ledger. **Required variants:** invalid placement, locked area, multiple items, ownership conflict.

**State/acceptance:** spending and owned inventory persisted; visuals are not authority. **Current repo status:** partial (financial assets, not walkable home).

### S18 — Wardrobe & appearance update

**Visual mode:** hybrid pixel+3D. **Entry:** closet/inventory/customize.

**Composition:** two previews of same avatar in same outfit: pixel standing turntable and lit 3D torso/full character; browsable clothing slot rows.

**Primary controls:** equip, unequip, palette, inspect, revert, save. **Required variants:** missing downloaded pack, unsupported body rig, old appearance.

**State/acceptance:** never allow outfit desync between rendering modes. **Current repo status:** partial (appearance editor).

### S19 — Money, banking & property ledger

**Visual mode:** system. **Entry:** Life > Money / buy action.

**Composition:** game-style financial ledger with monetary units, income and expense arcs, actual portfolio assets, next recurring cost.

**Primary controls:** buy/sell, bank activity, loan if implemented, receipt. **Required variants:** debt, failed purchase, duplicate payment, market fictional assumptions.

**State/acceptance:** all totals match pence in saved state. **Current repo status:** partial (portfolio).

### S20 — Health / wellbeing / goals / skills

**Visual mode:** system. **Entry:** Life > Personal.

**Composition:** clear health bars, life-stage badge, habits/activity tiles, optional progress map and real goals.

**Primary controls:** choose rest/gym/care/work/study, inspect history. **Required variants:** zero wellbeing, accessibility high-contrast, time cost.

**State/acceptance:** no misleading medical diagnoses or fabricated stat improvements. **Current repo status:** partial (wellbeing, experience).

### S21 — Story library and campaigns

**Visual mode:** system + cinematic cover. **Entry:** Stories tab / town episode entry.

**Composition:** original 3D illustrated cover crops with genre/state chips, tabs Your Life / Standalone / Continue, original story synopsis.

**Primary controls:** browse, details, play/resume, imported local stories. **Required variants:** not installed, new chapter available, bad import, offline.

**State/acceptance:** campaign and main-life timelines kept separate. **Current repo status:** partial (two short authored stories).

### S22 — Story details & branch overview

**Visual mode:** system. **Entry:** select a story card.

**Composition:** large cover hero art, character cast thumbnails, estimated duration, ratings/labels, branching preview without spoilers.

**Primary controls:** start, resume, preview, view author, install if legal. **Required variants:** content missing, version mismatch, no rights, mature rating.

**State/acceptance:** never represent unverified public content as installed. **Current repo status:** partial.

### S23 — Full-screen cinematic episode

**Visual mode:** 3D. **Entry:** start/resume story mode.

**Composition:** 3D story stage with moving actor blocking, matching 3D props/interiors, dialogue UI, chapter progress and meaningful choice points.

**Primary controls:** advance, replay if permitted, history, pause, exit, skip. **Required variants:** branch restore, orientation, 3-character speaker, lag, missing asset.

**State/acceptance:** story state machine and saved facts are authoritative. **Current repo status:** partial (illustrated StoryPlayer).

### S24 — In-world phone & communications hub

**Visual mode:** system + identity icons. **Entry:** Phone chip / right drawer.

**Composition:** fictional handheld phone shell; strict tabs NPC Messages, AI Characters, Real Contacts; unread count, offline indicator and accessibility labels.

**Primary controls:** tab, open thread, search local, settings. **Required variants:** offline, permission no, unavailable social, no messages.

**State/acceptance:** honest AI/human labels; chat never replaces the game. **Current repo status:** not implemented.

### S25 — AI NPC conversation thread

**Visual mode:** 3D portrait + native chat. **Entry:** Phone > AI character / NPC profile.

**Composition:** top smooth 3D live expression portrait as horizontal hero; speech threads below with time, remembering indicators and typed composer.

**Primary controls:** send, regenerate if supported, view/edit memory, return to world. **Required variants:** provider offline, safety refusal, context too long, deleted memories.

**State/acceptance:** only labeled AI; no pretend human, no secret leaks. **Current repo status:** not implemented.

### S26 — Consent-bound real-player social lobby

**Visual mode:** system. **Entry:** Phone > Real Contacts / contextual invitation.

**Composition:** clear HUMAN-only indicator, opt-in state, context activity banner, privacy disclosure, invite acceptance; no random-match casino UX.

**Primary controls:** accept known/context invite, privacy, decline, disconnect. **Required variants:** no human online, underage, moderation unavailable, no consent.

**State/acceptance:** no disguised random-anonymous chat app; conditional distribution. **Current repo status:** not implemented.

### S27 — Real-player conversation thread

**Visual mode:** system + optional consented avatar. **Entry:** accepted context-bound contact.

**Composition:** minimal chat thread with human status, delivery states and visible persistent report/block; optional consented avatar only.

**Primary controls:** send, mute, block, report, leave/delete. **Required variants:** reconnect, duplicate sends, unsafe messages, revoked consent, disconnect.

**State/acceptance:** no fabricated online humans; real account-scoped transport. **Current repo status:** not implemented.

### S28 — Memories & journal timeline

**Visual mode:** system + sprite moments. **Entry:** Memory tab / outcome View History.

**Composition:** chronological ribbon of actual saved life event entries with day/age and tiny pixel scene icon, filters and search.

**Primary controls:** expand, bookmark, optional flashback, return. **Required variants:** empty history, full timeline, missing imported story.

**State/acceptance:** show recorded events; no invented facts. **Current repo status:** partial (journal tab).

### S29 — Flashback / memory cinematic

**Visual mode:** 3D stylized recalled. **Entry:** tap existing memory requiring scene.

**Composition:** cinematic diorama with sepia/ink edge and archival caption "Reconstruction of a recorded moment"; actor at correct past age.

**Primary controls:** replay fact, step through, close. **Required variants:** unsupported scene reconstruction, ambiguous memory, original story missing.

**State/acceptance:** recollection must not be hallucinated as authoritative video. **Current repo status:** not implemented.

### S30 — Death, remembrance & legacy

**Visual mode:** hybrid system+cinematic. **Entry:** authoritative terminal life outcome.

**Composition:** quiet respectful cinematic still, memory object floating in warm shader space; inherited artifacts and timeline lineages below.

**Primary controls:** review life, family tree, memorial, start successor if enabled. **Required variants:** no heir, sensitive content, early death, inherited save corrupt.

**State/acceptance:** never turn mortality into confetti or success badge. **Current repo status:** not implemented.

### S31 — Pause, settings & personalization

**Visual mode:** system overlay. **Entry:** pause or menu.

**Composition:** structured handheld settings page with visual preview strips for pixel filter/quality/HUD scale, controls and save states.

**Primary controls:** resume, tune sound/music/haptics, accessibility, log out if relevant. **Required variants:** offline, settings sync pending, device capabilities missing.

**State/acceptance:** safe defaults and no unintended world skip. **Current repo status:** partial/basic.

### S32 — Visual packs, downloads & storage

**Visual mode:** system. **Entry:** Settings > Content.

**Composition:** pack cards with verified license/title, preview original icons, bytes installed and download availability; offline/progress badges.

**Primary controls:** install, pause, remove, verify, asset credits. **Required variants:** hash mismatch, low disk, rollback, dependency, airplane mode.

**State/acceptance:** staged atomic activation; don't run downloaded shaders. **Current repo status:** schema exists, no delivery UI.

### S33 — World map and quest markers

**Visual mode:** pixel/schematic. **Entry:** tap minimap or Map in sidebar.

**Composition:** pixel atlas with current player marker, reachable zones, known NPC locations if genuinely tracked, purposeful event icons.

**Primary controls:** pan/zoom/select route, close, pin. **Required variants:** undiscovered, inaccessible, path invalid, stale event.

**State/acceptance:** mapped routes can reflect valid world paths only. **Current repo status:** partial district map.

### S34 — Notifications center & outcome archive

**Visual mode:** system. **Entry:** top bell or phone badge.

**Composition:** stack of time-ordered in-world event widgets, unread and urgency categories, ability to expand real changed values.

**Primary controls:** read, pin, mute category, open underlying screen. **Required variants:** 10 simultaneous events, muted, duplicate, loss-sensitive.

**State/acceptance:** archived messages have source event ID. **Current repo status:** not implemented.

### S35 — Quest/opportunities board

**Visual mode:** system. **Entry:** HUD opportunity icon / location.

**Composition:** pixel pin and collectible-feeling cards with start date, deadline, location, eligibility, expected known cost; no invented quest reward.

**Primary controls:** pin, route, start, abandon if rule permits. **Required variants:** expired, missing requirements, duplicate acceptance.

**State/acceptance:** references existing city opportunities and eligibility. **Current repo status:** partial (opportunities list).

### S36 — Settings > Accessibility / controller

**Visual mode:** system. **Entry:** Settings > Accessibility.

**Composition:** large real-text controls with theme/contrast side-by-side preview and test haptic/audio buttons.

**Primary controls:** text scaling, reduce motion, haptic Off/Subtle/Full, remap virtual controls. **Required variants:** small phone, VoiceOver/TalkBack, motor needs, low color vision.

**State/acceptance:** never require animation or color recognition to progress. **Current repo status:** not implemented.

### S37 — Offline, retry & save recovery

**Visual mode:** system. **Entry:** save error / network down / GPU lost.

**Composition:** retains last valid world frame blurred or pixel-stilled with direct status, Retry, Play Offline, Safe Restore buttons.

**Primary controls:** retry, restore, export user data where allowed, dismiss. **Required variants:** damaged save, invalid downloaded pack, offline provider, renderer crashed.

**State/acceptance:** no save overwrite, no fabricated success. **Current repo status:** partial error banner.

### S38 — Story Creator Studio — authoring console

**Visual mode:** creator desktop/tablet. **Entry:** separate existing Next.js app.

**Composition:** editor triple-pane: story/node list, center pixel/3D live scene preview, right inspector/timeline/choices; publish checks footer.

**Primary controls:** add/validate scenes, routes, preview, import/export. **Required variants:** invalid choices, missing assets, unsafe imports, unsaved.

**State/acceptance:** exports original validated scene data. **Current repo status:** partial existing Next.js Creator Studio.

### S39 — Asset Creator Studio — rig and pack manager

**Visual mode:** creator desktop/tablet. **Entry:** creator app > assets.

**Composition:** dual viewport left 2D sprite 4 direction + right lit 3D rig; bottom asset grid/atlas provenance; animation preview scrubber.

**Primary controls:** import lawful asset, assign slots, rig animation, rebuild atlas, pack validation. **Required variants:** bad license, unsupported model, oversized pack, digest mismatch.

**State/acceptance:** all packs have provenance and QA before release. **Current repo status:** not implemented.

### S40 — Report, block & privacy management

**Visual mode:** system modal. **Entry:** real-player thread safety / app settings.

**Composition:** clear report reason choices, user identity context, evidence disclosure, block confirmation and safety routes; no opaque punishment animation.

**Primary controls:** report, block, mute, delete, appeal access/help. **Required variants:** abusive actor, loss of network, missing moderation, re-contact.

**State/acceptance:** safety visible, persists server-side where relevant. **Current repo status:** not implemented.

### S41 — Tutorial and first-roam guidance

**Visual mode:** pixel + contextual HUD. **Entry:** first entry into world, optional revisit.

**Composition:** pixel route ribbon guiding one café visit, meet NPC and time skip; never a giant intrusive wizard; guided controls/OS touch demo.

**Primary controls:** walk, interact, open HUD, skip, replay help. **Required variants:** controller enabled, reduced motion, unfamiliar labels.

**State/acceptance:** teach through actual playable steps and save progress. **Current repo status:** not implemented.

### S42 — Photo, profile and visual identity share

**Visual mode:** 3D still + pixel ID. **Entry:** avatar studio/profile optional.

**Composition:** polished framed 3D portrait and smaller pixel counterpart, non-sensitive badges, watermarked as player-controlled fiction; share preview editable.

**Primary controls:** save own screenshot, copy permitted profile, privacy control. **Required variants:** third-party NPC consent, external share fail, teen safety.

**State/acceptance:** never automatically share private NPC/human chat. **Current repo status:** not implemented.



## E. Mode state contracts and transitions (not merely navigation labels)

| Source → Destination | Visual transition | State preserved | Cancel/failure path |
|---|---|---|---|
| S04 overworld → S07 NPC bubble | world camera eases a few px; interact affordance outlines NPC; short compact bubble | actor tile coordinate, facing, NPC ID, current date | actor out of range closes bubble; player still at original tile |
| S07 → S08 3D talk | optional 1–3tile pixel mosaic iris to matched 3D wardrobe/pose, audio bed crossfade | world action paused, one character identity, age, outfit, props, scene and story ID | shader/pack unavailable uses accessible dialogue fallback and no fake 3D |
| S08 → S09 choices | actor expression/blink continues; dock expands and camera reframes | speaker and NPC emotional context, last valid story node | cancel/back only when authored; blocking choice persists |
| S09 → S10 outcome | choose card locks, others dim, world commit occurs once; widget animates only after authoritative result | exact world deltas, event IDs, save revision | pending saving, error, retry and idempotency visibly different |
| S10 → S04 return | close widget, reverse pixel/3D aperture, player resumes same tile/facing | world position, completed consequence, NPC route | emergency bypass retains state; no duplicate choice |
| S04 → S05 building | feet hit valid entrance collider; roof fades, indoor scene snaps to matching entrance | location ID, world time, avatar and NPC state | locked door stays outside with status |
| S04 → S06 transit | map zooms from player marker into labeled schematic with real cost/time | old position until confirmation | canceled route returns to original location |
| S04 → S11 Age Up | world dims slightly, calendar dial time shift with skippable animation | pre-advance world snapshot; one atomic age result | no input duplicates; interrupted animation restores committed result without duplicating it |
| S04 → S24 Phone | right drawer slides over paused/continuing pixel view according to chosen action | gameplay camera, queued notifications, draft message | offline banner, drawer closes without moving player |
| S24 → S25 AI thread | character 3D portrait animates while text thread remains native | NPC identity, memory authority and consent | provider unavailable explicitly shown |
| S24 → S27 Real thread | human-chat UI remains clearly labeled as human; no forced 3D character illusion | authenticated scope, consent, send idempotency | disconnect/revoke shows honest status, report/block always accessible |
| S08/S23 → S29 flashback | muted ink/cel transition, dated archival title visible | current life frozen, recalled scene from known events | no reconstructable scene offers text journal, never fabricated visuals |
| S04 → S12/S13 etc | context panel docks from left; world remains visible or stops only if necessary | player position and HUD state | back returns to exact world viewport |
| S04 → S37 safe recovery | preserve last valid rendered scene as background and show error semantics | previously committed save and pending revisions | no destructive retry, opt-in recovery |
| S38/S39 creator → S23 preview | device-frame preview with source model selection; never edits player save | creator draft, test fixture, content manifest | return to draft with validation issues unchanged |

**Interaction ownership:** keyboard/text input and native dialogs take focus before world movement inputs. When a choice dock, recovery or report modal is active, moving the pixel player is disabled. A secondary drawer may allow gameplay to continue only in an explicit low-focus nonblocking state. All three representations share the same saved character ID; 3D facial expressions may represent emotion but never create a new world event.

## F. Component-level visual and haptic states

| Component | Required states | Motion / haptic | Data contract |
|---|---|---|---|
| Primary arcade button | idle, focus, pressed, disabled, loading, committed, failed | <50ms press appearance; selection/light haptic only when enabled, confirmation on commit | one callback, duplicate tap guard |
| Age Up orb | ready, progress, saving, complete, blocked | 600–1400ms, skippable; category-sensitive feedback | stored age days + changed event ledger |
| Story choice card | focus, hover/controller, armed, committed, branch-loading, resolved, unavailable | card closes in 160–260ms, haptic commit; 3D actor reacts | author choice ID and atomic effect |
| Outcome toast/widget | queued, visible, expanded, dismissed, pinned | short slide; never auto-success before storage confirms | exact event ID and real net deltas |
| NPC marker | offscreen, within range, talkable, busy, quest, blocking, gone | 1px pixel outline and subtle icon; no per-frame haptic | live NPC world ID |
| Phone inbox chip | unread, read, offline, restricted, hidden | badge scale only if opted in, no interrupting 3D drama | distinct NPC/AI/human origin |
| Social report/block | open, selecting, submitted, failed, confirmed | quiet modal, no gamified animation | audit-safe moderation action |
| Download pack card | not-installed, queued, downloading, verifying, activating, installed, failed, rolled-back | readable progress, error text, cancel | digest, version, license, storage bytes |
| Avatar part selector | default, selected, preview-draft, incompatible, locked-download | show pixel+3D same change before commit, light tick | appearance slot and manifest variant ID |
| Dialogue dock | hidden, typing, complete line, history, choice, skip, error | text-tied mouth actuation and native type speed, can instantly reveal | script/AI source label, accessible text |
| Walk control | neutral, direction, sprint, blocked, movement-disabled | 0–100ms respond; no haptic per step | logical tile collision + world position |
| Save status | dirty, saving, saved, retry, conflict, read-only | unobtrusive small icon, errors announced | on-disk revision and actual result |

**Haptic semantics:** selection on discrete focus, one medium confirmation for substantial committed choice, subtle positive/warning only when context appropriate; grief/death neutral by default. Do not vibrate per tile step, letter, scroll tick, NPC idle animation, frame or frequent currency update. Reduce Motion removes zoom/shake/fast aperture and preserves all world facts.

## G. UI layout/overlay priority and input focus by form factor

### Narrow portrait 320–359pt
- top compact age/currency only with expandable stat chip and location on separate narrow caption; do not horizontally clip even with large names.
- bottom primary actions collapse to menu, interact and phone; joystick can be virtual or gesture-based; Age Up moves to explicit thumb drawer if spatial conflicts arise.
- dialogue dock uses 16–18sp text and a maximum visible height that keeps eyes visible; choices scroll within own panel; focused input and keyboard bring composer above home indicator.
- overlay width = safe screen width minus 12–16pt margins. Do not pin both sidebars.

### Standard portrait 360–599pt
- status strip 48–56pt; world fills flexible area with original tile pixel density; in-city HUD occupies bottom ~112–168pt depending on virtual-pad setting, respecting home indicator.
- left menu and right phone slide over world, max ~80–88% width, dark backdrop; one at a time; swipe dismissal and icon/back restore.
- 3D conversation image stays ~52–65% of screen, with dynamic dock lower part; 12–24pt safe vertical text spacing; camera framing adjusts for keyboard/choice panel.

### Tablet / landscape >=600pt
- world takes central 55–70%; context sidebar 208–280pt, optional phone/notifications rail 260–340pt if width >=1000; no overlay of central gameplay by default.
- default cinematic scene 16:9 or author-defined 2.35:1 *within* available view; safe dialogue dock can sit beside or beneath it, not cover critical faces.
- multi-input focus switching (mouse, controller, keyboard, touch) has visual selected state; no hover-exclusive functionality.

### Creator desktop >=1024pt
- left content rail ~240px; center timeline/viewport flexible min 560px; inspector 280–340px; bottom debug and validation bar 64–120px.
- preview emulates 320/390/430 phone widths with true safe areas and scales content, not text raster.

### Orientation & OS interruptions
- restoring from background, switching tabs, incoming calls, keyboard presentation and notification permission changes never duplicate simulation choices.
- stage camera recomputes view safe region when rotated; pixel map rescales by tiles, not bilinear stretching; 3D frame composition uses camera rigs to keep eyes above the dock.

## H. Journey maps / test scripts for all modes

**J1 — A first night in Bellweather:** S00→S01→S02→S03→S41→S04. Move through 4 tiles, pass one blocked collider, enter café S05, greet Amelia S07, choose deep conversation S08/S09, observe real trust widget S10, return S04 at previous tile. Open S28 memory and verify event recorded. Force close/reload, compare position, outfit, trust and story continuity.

**J2 — Daily career, aging, responsibility:** S04→S13 at job location, earn legitimate wage after one time action, S19 verifies ledger, choose S11 Age Up, experience exact event set and life-stage appearance if threshold crossed, S10 demonstrates net delta and supports inspecting journal. Loss-sensitive event uses non-celebratory presentation. Accessibility reduced-motion path must work.

**J3 — Cinematic chapter with saved branching:** S21→S22→S23; three choices including failure/disabled case, two emotional expression transitions in 3D, clean dialogue accessibility, save midway, reopen same speaker/scene and compare outfits/age. Return through S10 to S04 if this story is world-compatible; otherwise remain isolated standalone continuity.

**J4 — AI NPC chat:** S24→S25; real provider-backed message shows correct AI disclosure, live expression from allowed state, retrieved user-permitted memory (not a hallucinated fact), reconnect and delete-memory behavior. Offline failure is legible and never represented as a human being.

**J5 — Real contact safety:** S24→S26→S27; consent-based human contact only when feature is legitimately enabled, block/report at any stage via S40, offline/unsupported state without pretending humans are online. iOS app store policy concerns remain unresolved until review.

**J6 — Asset pack and appearance:** S03/S18→S32 install authorized pack; verify license/hash/revision; equip a new part in pixel and 3D, persist after force close, handle missing optional pack with safe fallback. No downloaded executable shaders.

**J7 — Memorial and lineage:** S11 terminal event → S30 → S28/S29 known memories → heir selection or new-life prompt; correct respectful treatment, ability to exit/review without involuntary resets.

## I. Current repo mapping and implementation truth

| Screen family | Existing starting code | Gap |
|---|---|---|
| New life / editor S02/S03 | apps/player/App.tsx + AvatarEditor.tsx / AvatarPortrait.tsx | no pixel↔3D true render parity or introduction loop |
| Free roam S04/S06/S33 | CityWorld.tsx + CityMap.tsx, generated city scene | map/district cards, NOT walkable pixel world, no collision/door/interior |
| Life/career/widgets S10–S20/S34/S35 | LifeDashboard.tsx, simulation-core moments/portfolio/city | only partial action panels, no unified HUD widget state machine or true haptics |
| Dialogue S08/S09/S21–S23 | StoryPlayer.tsx, GameStage.tsx, narrative-core | current illustrated prototype, no live rigged native 3D world |
| People/memory S15/S28 | App.tsx people & journal tabs | cards and logs exist but graph/flashback/legacy not built |
| Communications S24–S27/S40 | no actual real-player or AI provider-backed messaging | must build with safety controls, consent and API-backend separation |
| Settings/asset/storage S31/S32/S36/S37 | simple status/errors and asset-pack schema | UI and actual staged downloads/cache missing |
| Creator S38/S39 | apps/creator-studio | existing web editing, no authored 3D rig/tile/live preview pipeline |

Design-only **screen atlas**: [docs/design/LIVEIT_SCREEN_ATLAS.html](design/LIVEIT_SCREEN_ATLAS.html) contains schematic compositions for principal modes; it is not a production build or claimed final render. The atlas should be browsed locally from a checked-out repo and visually reviewed across narrow, standard and tablet widths. The full 43-item list above is the completeness authority; atlas uses representative screen *families*, not 43 separate production images.

## J. Design review signoff gates (before Step 3 architecture)

- Every named journey has a clear entry, return, persisted state and controller/back strategy.
- Pixel world is visibly **top-down** and walkable, not a sky-view city poster.
- Important conversation shows a true 3D character with UI dock avoiding facial occlusion.
- Screens do not invent missing AI/human features or simulate hidden active chat users.
- Haptic and outcome widgets are bound to authoritative state; accessibility paths preserved.
- Pixel and 3D avatars have testable identity and outfit parity.
- Social scopes include age eligibility, consent, report/block, and transparent humans-vs-AI language.
- Empty/offline/error/recovery designs exist for every remote and asset-dependent feature.
- Non-implemented features are marked FUTURE/NOT DONE in build status, not asserted shipped by visual mockup.
- All screens are original and avoid copying Pokémon visual assets, dialogue boxes or branded trade dress.

**End Step 2 specification. Stop here: do not silently execute Step 3–5.**
