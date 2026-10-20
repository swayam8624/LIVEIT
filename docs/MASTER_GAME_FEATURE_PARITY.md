# LIVEIT — Feature-by-feature master acceptance checklist

> October 2026. An original game inspired by _categories_ from BitLife, Episode and pseudonymous chat, not a copy of their copyrighted assets or scripts. Their proprietary features change; this is a living scope ledger, not a claim to catalog every historical product expansion.

> Baselines: https://apps.apple.com/in/app/bitlife-life-simulator/id1374403536 · https://home.episodeinteractive.com/ · https://episodesupport.zendesk.com/hc/en-us/sections/360008483713-Writer-s-Portal-Guides · https://anonychat.app/how-it-works · https://anonychat.app/safety

> A box remains unchecked until user-visible behavior, save restoration, age/consent restrictions, automated regression and actual mobile QA pass. Existing prototypes **do not** count as finished.

## Ordered implementation waves

P0: game identity / facing / genuine LLM / birth / streamed tile world. P1: families, activities, ordinary relationships, life integrated story. P2: age-gated romance, adult family, school, career, money and health. P3: advanced Episode authoring, NPC memory, pets, housing. P4: specialist jobs, fame, crime, large content inventory. P5: opt-in adults-only REAL-user anonymous chat with moderation and privacy. P6: instrumented iOS/Android release quality.

## 00 Foundation

- [ ] `00.01` Origin and genetic/cultural context
- [ ] `00.02` Birth-first new game
- [ ] `00.03` Name/pronouns and identity
- [ ] `00.04` Parents and guardians
- [ ] `00.05` Monthly world clock
- [ ] `00.06` Infant-to-elder stages
- [ ] `00.07` Aging through gameplay
- [ ] `00.08` Death and inheritance
- [ ] `00.09` Family continuation
- [ ] `00.10` Multiple save slots
- [ ] `00.11` History and journal
- [ ] `00.12` Reproducible event simulation
- [ ] `00.13` Automatic local recovery
- [ ] `00.14` Life achievement and ribbons
- [ ] `00.15` Age-specific safe actions

## 01 Pixel rendering

- [ ] `01.01` Correct sprite orientation
- [ ] `01.02` Directional idle/run/sit animations
- [ ] `01.03` Avatar skin and hair layers
- [ ] `01.04` Outfit and accessories
- [ ] `01.05` Infant/child/teen/adult/elder sprites
- [ ] `01.06` Interactive world-first HUD
- [ ] `01.07` Dynamic camera and zoom
- [ ] `01.08` Mobile joystick
- [ ] `01.09` Tap-to-walk/pathfinding
- [ ] `01.10` Gamepad/keyboard
- [ ] `01.11` 60FPS measured device target
- [ ] `01.12` 120FPS optional
- [ ] `01.13` Occlusion and depth sorting
- [ ] `01.14` Ambient lighting
- [ ] `01.15` Weather and seasons
- [ ] `01.16` Audio and haptics
- [ ] `01.17` Pixel crisp sampling
- [ ] `01.18` Accessibility

## 02 Endless generated world

- [ ] `02.01` Seeded infinite tile coordinates
- [ ] `02.02` Chunk 32x32 generation
- [ ] `02.03` Stable chunk seams
- [ ] `02.04` Chunk loading and eviction
- [ ] `02.05` Deterministic terrain and collisions
- [ ] `02.06` Rivers roads and crossroads
- [ ] `02.07` Biome transitions
- [ ] `02.08` Shops and commercial zones
- [ ] `02.09` Housing neighborhoods
- [ ] `02.10` Schools universities hospitals
- [ ] `02.11` Work and offices
- [ ] `02.12` Gardens playgrounds countryside
- [ ] `02.13` Building entry/interiors
- [ ] `02.14` Objects and furnishings
- [ ] `02.15` NPC population schedules
- [ ] `02.16` Player world edits persist
- [ ] `02.17` World map and navigation
- [ ] `02.18` Player housing in world
- [ ] `02.19` Vehicles transit and fast travel
- [ ] `02.20` Story landmark persistence

## 03 Birth and childhood

- [ ] `03.01` Pregnancy/birth scenario
- [ ] `03.02` Parents/family wealth occupations
- [ ] `03.03` Single parent adoption or guardianship
- [ ] `03.04` Sibling births twins step-siblings
- [ ] `03.05` Early feeding sleep and care
- [ ] `03.06` Toddler development
- [ ] `03.07` Daycare and preschool
- [ ] `03.08` Child health and vaccinations
- [ ] `03.09` Primary schooling
- [ ] `03.10` Grades and homework
- [ ] `03.11` Teachers and classmates
- [ ] `03.12` Friends rivals and bullies
- [ ] `03.13` Sports arts and hobbies
- [ ] `03.14` Family trips and holidays
- [ ] `03.15` Divorce and remarriage impacts
- [ ] `03.16` Moving households
- [ ] `03.17` Childhood milestones
- [ ] `03.18` Memories from age zero

## 04 Teen and education

- [ ] `04.01` Puberty and age transitions
- [ ] `04.02` Secondary school and grades
- [ ] `04.03` Clubs sports orchestra theater
- [ ] `04.04` Part-time teen jobs
- [ ] `04.05` Graduation and exams
- [ ] `04.06` School discipline
- [ ] `04.07` University applications
- [ ] `04.08` Scholarships grants
- [ ] `04.09` Student loans
- [ ] `04.10` College majors and degrees
- [ ] `04.11` Internships and apprenticeships
- [ ] `04.12` Postgraduate degrees
- [ ] `04.13` Law medicine teaching schools
- [ ] `04.14` Friends and campus life
- [ ] `04.15` Career placement and recruiters

## 05 Adult jobs

- [ ] `05.01` Hourly and salary careers
- [ ] `05.02` Applications interviews CVs
- [ ] `05.03` Job acceptance or rejection
- [ ] `05.04` Coworker and boss relationships
- [ ] `05.05` Work shifts in buildings
- [ ] `05.06` Raises promotions demotions
- [ ] `05.07` Firing unemployment retirement
- [ ] `05.08` Careers tied to real geography
- [ ] `05.09` Technology science and creative jobs
- [ ] `05.10` Police education healthcare
- [ ] `05.11` Trades service and retail jobs
- [ ] `05.12` Government public service
- [ ] `05.13` Freelance and gig work
- [ ] `05.14` Self employment and company ownership
- [ ] `05.15` Corporate office politics
- [ ] `05.16` Burnout work-life balance
- [ ] `05.17` Career training and skill trees

## 06 Special careers

- [ ] `06.01` Sports professional and league
- [ ] `06.02` Musician recording and touring
- [ ] `06.03` Actor director film studio
- [ ] `06.04` Model and fashion work
- [ ] `06.05` Politics and elections
- [ ] `06.06` Military and intelligence fantasy
- [ ] `06.07` Astronaut and scientist
- [ ] `06.08` Creator streaming fame
- [ ] `06.09` Business CEO entrepreneurship
- [ ] `06.10` Writer/author royalties
- [ ] `06.11` Underworld storytelling role paths
- [ ] `06.12` Celebrity PR reputation
- [ ] `06.13` Special career mini-games

## 07 Romance and relationships

- [ ] `07.01` All ages family affection
- [ ] `07.02` Parents siblings cousins grandparents
- [ ] `07.03` Friends and best friends
- [ ] `07.04` Enemies rivals gossip
- [ ] `07.05` NPC trust and emotional memory
- [ ] `07.06` Friend meetups and gifts
- [ ] `07.07` Real typed conversations
- [ ] `07.08` NPC proactive messages
- [ ] `07.09` Age-appropriate first crush
- [ ] `07.10` Dating from appropriate age
- [ ] `07.11` Adult match/dating applications
- [ ] `07.12` First date and romance
- [ ] `07.13` Partner compatibility and boundaries
- [ ] `07.14` Communication conflicts
- [ ] `07.15` Mutual consent before intimacy
- [ ] `07.16` Commitment engagement marriage
- [ ] `07.17` Living together
- [ ] `07.18` Prenups shared finances
- [ ] `07.19` Breakups divorce and reconnection
- [ ] `07.20` Affairs and trust repair
- [ ] `07.21` Long-distance partners
- [ ] `07.22` Bereavement and grieving

## 08 Adult intimacy and family

- [ ] `08.01` Romantic intimacy 18+ only
- [ ] `08.02` Consent and reversible refusal
- [ ] `08.03` Non-graphic fade-to-black scenes
- [ ] `08.04` Sexual health and contraception
- [ ] `08.05` Pregnancy and prenatal care
- [ ] `08.06` Partner family planning
- [ ] `08.07` Parenthood and child development
- [ ] `08.08` Fertility support IVF
- [ ] `08.09` Adoption and surrogacy
- [ ] `08.10` Child support and custody
- [ ] `08.11` Parenting routines
- [ ] `08.12` Family events and ceremonies
- [ ] `08.13` Multiple generations
- [ ] `08.14` No sexual content involving minors

## 09 Health and wellbeing

- [ ] `09.01` Physical health fitness
- [ ] `09.02` Nutrition hunger energy sleep
- [ ] `09.03` Illness prevention doctor visits
- [ ] `09.04` Disease and injury treatment
- [ ] `09.05` Vaccination and specialists
- [ ] `09.06` Mental health and therapy
- [ ] `09.07` Addiction rehabilitation
- [ ] `09.08` Disability access
- [ ] `09.09` Stress mood grief anxiety
- [ ] `09.10` Ageing chronic conditions
- [ ] `09.11` Medical cost insurance
- [ ] `09.12` Death cause and obituary
- [ ] `09.13` Fitness hobbies and exercise

## 10 Daily life and activities

- [ ] `10.01` Shopping and groceries
- [ ] `10.02` Cooking and meals
- [ ] `10.03` Restaurants cafes
- [ ] `10.04` Library reading
- [ ] `10.05` Gym exercise
- [ ] `10.06` Movies cinema
- [ ] `10.07` Music lessons
- [ ] `10.08` Art writing photography
- [ ] `10.09` Museums and concerts
- [ ] `10.10` Gardening and parks
- [ ] `10.11` Sports clubs
- [ ] `10.12` Volunteering and charity
- [ ] `10.13` Games mini-games arcades
- [ ] `10.14` Social nightlife adult-gated
- [ ] `10.15` Vacations sightseeing
- [ ] `10.16` Birthday holidays festivals
- [ ] `10.17` Hobbies and collectible inventories
- [ ] `10.18` Activity-dependent skill development
- [ ] `10.19` Daily scheduling and cooldowns

## 11 Money and housing

- [ ] `11.01` Accounts cash transfers
- [ ] `11.02` Salary expense ledgers
- [ ] `11.03` Rent utilities taxes
- [ ] `11.04` Loans credit cards debts
- [ ] `11.05` Student loans
- [ ] `11.06` House mortgage ownership
- [ ] `11.07` Cars and transport ownership
- [ ] `11.08` Insurance and warranties
- [ ] `11.09` Property upgrades decoration
- [ ] `11.10` Real estate letting
- [ ] `11.11` Investments and stocks
- [ ] `11.12` Cryptocurrency simulations
- [ ] `11.13` Savings and interest
- [ ] `11.14` Business ventures
- [ ] `11.15` Jewelry collectibles luxury goods
- [ ] `11.16` Lottery gambling age-gated
- [ ] `11.17` Charity inheritance and wills
- [ ] `11.18` Bankruptcy litigation

## 12 Crime and justice

- [ ] `12.01` Lawful consequences for crimes
- [ ] `12.02` Theft fraud and vandalism narratives
- [ ] `12.03` Arrest suspicion police
- [ ] `12.04` Lawyers and courts
- [ ] `12.05` Convictions and sentences
- [ ] `12.06` Prison life and parole
- [ ] `12.07` Appeal and legal records
- [ ] `12.08` Prison social relationships
- [ ] `12.09` Civil lawsuits and settlements
- [ ] `12.10` Police and detective careers
- [ ] `12.11` No real-world criminal instructions

## 13 Pets and nature

- [ ] `13.01` Pet adoption
- [ ] `13.02` Breeds and personality
- [ ] `13.03` Pet training and care
- [ ] `13.04` Veterinary visits
- [ ] `13.05` Pet aging and loss
- [ ] `13.06` Wildlife and zoos
- [ ] `13.07` Weather and nature systems
- [ ] `13.08` Animal shelters and charities

## 14 Fame and society

- [ ] `14.01` Social media profiles
- [ ] `14.02` Content creation and reach
- [ ] `14.03` Fan encounters
- [ ] `14.04` Public awards and scandals
- [ ] `14.05` Politics elections polls
- [ ] `14.06` Community reputation
- [ ] `14.07` Press interviews
- [ ] `14.08` Brand deals and contracts
- [ ] `14.09` Social graph and rumor propagation

## 15 Episode-like authored story

- [ ] `15.01` Original story catalogue
- [ ] `15.02` Genres and tags
- [ ] `15.03` In-life mission initiation
- [ ] `15.04` Chapters and acts
- [ ] `15.05` Directed pixel scenes
- [ ] `15.06` Character expressions and animations
- [ ] `15.07` Camera pans and zooms
- [ ] `15.08` Sound effects music
- [ ] `15.09` Interactive choice panels
- [ ] `15.10` Free-type dialogue alternative
- [ ] `15.11` Branching conditional scenes
- [ ] `15.12` Consequences to same life
- [ ] `15.13` Player cosmetic continuity
- [ ] `15.14` Persistent story characters
- [ ] `15.15` Choice journal
- [ ] `15.16` Multiple endings
- [ ] `15.17` Save and resume stories
- [ ] `15.18` Author stories age/location gated
- [ ] `15.19` Relationship driven quests
- [ ] `15.20` On-world quest markers
- [ ] `15.21` Offline story download packs

## 16 Authoring and creator studio

- [ ] `16.01` Scene and mission authoring
- [ ] `16.02` Visual scene director
- [ ] `16.03` Branch graph editor
- [ ] `16.04` NPC cast creator
- [ ] `16.05` Pixel wardrobe editor
- [ ] `16.06` Foreground overlays
- [ ] `16.07` Animations timing and transitions
- [ ] `16.08` Choice conditions and scoring
- [ ] `16.09` Creator variables and memory flags
- [ ] `16.10` Mission objective compiler
- [ ] `16.11` Validation and linting
- [ ] `16.12` Preview in real runtime
- [ ] `16.13` Story import export and versioning
- [ ] `16.14` Rights clearance and attribution
- [ ] `16.15` Community publishing workflow
- [ ] `16.16` Search rankings discovery
- [ ] `16.17` Moderation report for UGC
- [ ] `16.18` Creator collaboration and testing

## 17 Anonymous real-user chat

- [ ] `17.01` Explicitly separate from NPC AI
- [ ] `17.02` Adults-only account eligibility
- [ ] `17.03` Pseudonymous profiles
- [ ] `17.04` Random strangers and skip
- [ ] `17.05` Interest language filters
- [ ] `17.06` Chat rooms and topics
- [ ] `17.07` Private messages with requests
- [ ] `17.08` Mutual contact consent
- [ ] `17.09` Typing online status
- [ ] `17.10` Block and report
- [ ] `17.11` Spam and abuse handling
- [ ] `17.12` Content moderation and appeal
- [ ] `17.13` Data retention and deletion
- [ ] `17.14` Privacy controls and audit
- [ ] `17.15` Age restrictions before stranger matching
- [ ] `17.16` Realtime delivery and retries
- [ ] `17.17` Voice media optional
- [ ] `17.18` No contact with minors

## 18 Local NPC LLM

- [ ] `18.01` Ollama endpoint diagnostics
- [ ] `18.02` Selected model installed check
- [ ] `18.03` Clear failure instead of fake responses
- [ ] `18.04` Local Qwen models
- [ ] `18.05` Free text and multi turn context
- [ ] `18.06` Per-NPC persistent memories
- [ ] `18.07` Semantic retrieval and summaries
- [ ] `18.08` Consistent NPC personae
- [ ] `18.09` Proactive conversations
- [ ] `18.10` Relationship-aware language
- [ ] `18.11` Age-appropriate conversations
- [ ] `18.12` Structured safe intent proposals
- [ ] `18.13` Authoritative consequence validator
- [ ] `18.14` Streaming and cancellation
- [ ] `18.15` LAN mobile setup
- [ ] `18.16` Private offline by default
- [ ] `18.17` High-quality context and evaluation
- [ ] `18.18` Conversation latency metrics
- [ ] `18.19` Distinct emotion and goals

## 19 Quality and release

- [ ] `19.01` Tests for save migration
- [ ] `19.02` Tests for sprite mapping
- [ ] `19.03` Tests for chunk continuity
- [ ] `19.04` Tests for age gates
- [ ] `19.05` Tests for NPC chat failures
- [ ] `19.06` Multiplayer security review
- [ ] `19.07` Device smoke on iPhone
- [ ] `19.08` Android smoke
- [ ] `19.09` Web smoke
- [ ] `19.10` Real measured FPS frame histograms
- [ ] `19.11` Memory budget and texture atlas
- [ ] `19.12` Crash recovery
- [ ] `19.13` Localization and accessibility
- [ ] `19.14` Power and thermal targets
- [ ] `19.15` Legal license provenance
- [ ] `19.16` Offline first resilience
- [ ] `19.17` Continuous CI and release builds

## Completion proof

Each checked task must link to: an implemented source file, a regression test, a visible gameplay path, a save/load check, and actual device validation where relevant. No `docs-only = implemented`, no `API adapter = online LLM`, no `procedural tile function = limitless world` without streaming, no minor access to adult intimacy or stranger chat.

**Current prior-branch foundations (NOT checked):** a fullscreen pixel town, monthly ticking, a tiny activity subset, a few story scenes, a local model adapter, prototype quests, initial avatar choices. Missing coverage remains extensive.

TOTAL: 323 individually trackable features across 20 categories.
