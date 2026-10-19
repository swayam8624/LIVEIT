# LIVEIT — Unified Hybrid Rendering Architecture (ENG-003)

> **ARCHIVED 3D/HYBRID PLANNING DOCUMENT:** The owner changed LIVEIT to **100% expressive 2D retro pixel art** on 2026-10-19. Its former 3D cinematic/model requirements below are superseded by [PIXEL_ONLY_DIRECTION_V2](PIXEL_ONLY_DIRECTION_V2.md) and [active pixel-v2 requirements](../content/production-assets/pixel-v2/required-assets.json). Do not implement 3D from this document.

**Status:** Step 3 of 5, architecture locked and TypeScript interface-contract prototype added. This does not claim native mobile renderer, walkable overworld, 3D actors or downloadable assets are currently shipped.

**Authoritative design:** GDS-001 in docs/LIVEIT_GRAPHICS_DESIGN_SPEC_V1.md and GDS-002 in docs/LIVEIT_SCREEN_MODE_BLUEPRINT_V1.md. The user explicitly wants original early-Pokémon-like top-down pixel exploration, smooth modern **true-3D** conversations, and dense tactile Life/Story/HUD/Phone interfaces, all populated by the **same persistent, aging human identities**. Those decisions supersede the previous isometric low-poly town or procedural 2.5D faces as the final art output. Retain their Vulkan demo as technical groundwork and test evidence.

**Platform matrix:** iOS + iPadOS -> Vulkan translated through MoltenVK to Metal, using a CAMetalLayer. Android -> native Vulkan presented to an ANativeWindow provided by SurfaceView. The creator is a separate Next.js desktop/web authoring application. Existing Expo web preview remains a functional fallback for domain/content testing but must not be labeled Vulkan.

## 0. The one rule

The world is a simulation with multiple cameras and render styles, **not** a 2D game sending pretend screenshots to an unrelated 3D cutscene app. World truth lives only in versioned deterministic TypeScript life/narrative simulation and its persisted domain data. A native GPU renderer can display/interpolate/pick, but can never invent trust, money, age, NPC identity, human contacts, authored branches, legitimate inventory, mortality or saved scene state.

A user should:

- walk a hand-authored 16px tile town;
- enter a walkable home or café;
- approach a named NPC, see a short pixel-world prompt;
- engage in true-3D facially animated dialogue with that **same** NPC;
- choose a meaningful authored response using accessible controls and a confirmed haptic;
- observe **persisted** trust/money/memory changes in an outcome widget;
- return to the original valid pixel-world tile, same outfit/age, without restart or hidden time-skip;
- reload and find the life/scene/outcome correctly reconstructed.

Any engine implementation that cannot complete this loop is a prototype, not the final gameplay renderer.

## 1. Reality baseline and migration discipline

| Current on feature branch | Existing implementation                                                                                                                                                          | Required future destination                                                                                                                |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| World and choices         | packages/simulation-core, narrative-core, save-system; day/world data and identity                                                                                               | preserve them, add persisted location, tile pose and collision/interaction state without deleting legacy saves                             |
| City graphics             | apps/player/src/CityMap.tsx & CityWorld.tsx illustrate/choose districts, no walking                                                                                              | introduce atlas-based top-down walkable, navigable actual pixel city and interiors                                                         |
| GPU proof                 | native/city-vulkan is a C++17 headless Vulkan compute CLI and pixel-buffer PPM output; shaders/city.comp raycasts rough city and shaders/actors.comp draws procedural 2.5D faces | reusable swapchain renderer and **two real-time graphics passes**: tile/sprite raster world plus true mesh/skeletal 3D cinema              |
| Story UI                  | StoryPlayer.tsx, GameStage.tsx, AvatarPortrait.tsx are RN art placeholders                                                                                                       | keep functioning story state and accessible dialogue while replacing actor stage with native 3D viewport                                   |
| Appearance                | world-schema/src/appearance.ts has saved cosmetic enums; buildVisualScene creates canonical actor appearances                                                                    | deterministic appearance resolver into artist-approved 2D sprite variants and 3D mesh/rig/material slots                                   |
| Pack handling             | visual-assets.ts schemas, prepareVisualPackActivation validates SHA-256 byte sizes/dep graph; 51 procedural recipe metadata items                                                | signed/versioned pack publication, real atlases/models and on-device downloaded storage with atomic activation and rollback                |
| Rendering ABI             | world-schema/src/render-contract.ts and simulation-core/src/render-adapter.ts added in Step 3                                                                                    | live native Expo module, queue/frame IPC, GPU asset resource binding, actual click/gesture events and lifecycle integration                |
| Social/messaging          | no real multiplayer or server AI chat                                                                                                                                            | explicit separately labeled AI and human systems; separate secure transport, identity/consent and moderation, always outside render engine |

Never call CI-rendered PPM screenshots proof that an iPhone has shown a Vulkan frame. Do not delete useful existing components before the real replacement passes device QA; fallback and feature flags remain available during transition.

## 2. System decomposition and ownership

    user input / controller / gesture / accessible native button
             |
             v
    React Native GameShell: navigation, HUD, permissions, focus management
             |
             v
    IntentCoordinator: sequence/revision, route/game command authorization
             |
             v
    Deterministic Domain: simulation-core + narrative-core + NPC rules
             |
             v
    SaveCoordinator: validate, commit, persist, emit revision/event receipt
             |
             +------> OutcomeWidget Queue + optional Haptics / Audio
             |
             v
    SceneBuilder: verified world revision + actual navigation pose
             |
             v
    Validated GameRenderFrame (pixel-overworld OR cinematic-3d)
             |
             v
    NativeBridge: bounded command/snapshot mailbox, capabilities
             |
             v
    C++ RenderHost: GPU resources, shader cache, renderer frame graph
            /                                  \
    OverworldPass                              CinematicPass
    chunk tile atlas + entity sprite           mesh skinning + material pass
    shadows, weather, pixel lighting           depth/shadow, face, PBR/toon lighting
    nearest-neighbor logical render             dynamic-resolution physical render
            \                                  /
             +------> TransitionComposite / Present ------+
                         |
              Android Vulkan swapchain
              iOS MoltenVK over CAMetalLayer
                         |
              native accessible text/controls
                         |
              real pixels and user-visible UI

Rendering is **read-only** relative to the life simulation. An NPC AI may suggest speech/expression intents, but those are data under moderation and author-schema constraints, not arbitrary GPU shader snippets or game commands.

Boundaries:

- Domain may be run headless and tested on Node, independent of GPU, clock, network, Android, React or Xcode.
- Navigation grid/collision and bounded movement are domain/gameplay; the renderer may predict cosmetic interpolation only.
- Native code owns GPU device, texture allocation, animation interpolation, frame pacing and pointer ray tests; does not own authoritative stats or story choices.
- Native HUD text and accessible controls may overlay Vulkan image(s) through React Native. The user wants shader-rendered gameplay graphics, not inaccessible all-rasterized app text.
- Downloaded assets never contain executable shader binaries or arbitrary scripts. Precompiled shader variants ship with signed app builds; downloadable resource packs contain validated data/images/meshes/animations only.

## 3. Project layout (existing vs proposed)

    apps/
      player/
        App.tsx                         EXISTING | entry, save queue and shell
        src/CityMap.tsx                 EXISTING | temporary fallback
        src/StoryPlayer.tsx             EXISTING | story/dialogue controller
        src/gameTheme.ts               EXISTING | HUD tokens
        src/AvatarEditor.tsx            EXISTING | cosmetic editor
        src/game/                        PROPOSED
          GameViewport.tsx              native availability fallback
          PixelHud.tsx                  accessible overlay, controls
          CinematicHud.tsx              dialogue dock and choice card
          OutcomeQueue.tsx              authoritative receipts only
          InputCoordinator.ts           mapping touch, pad, keyboard, gestures
          NativeRenderView.tsx          typed Expo module manager
          SceneHandoff.ts              cinematic transition state machine
        modules/liveit-render/           PROPOSED local Expo module
          src/                           types, callbacks, render modes
          ios/                           ExpoView Swift + ObjC++ wrapper
          android/                       ExpoView Kotlin + JNI
    native/
      city-vulkan/                       EXISTING offscreen testing prototype
      liveit-render/                     PROPOSED reusable native engine
        include/liveit/
          FrameProtocol.hpp             verified ABI and version
          RenderHost.hpp                lifecycle and frame scheduler
          Resources.hpp                 atlas/mesh and GPU ownership
          PixelWorld.hpp                chunk map and sprite API
          CinematicStage.hpp            rig/skinning/camera API
          PlatformSurface.hpp           iOS/Android swapchain factory
        src/
          core/, pixel/, cinematic/, effects/, platform/
        shaders/
          pixel/{tiles,sprites,palette,lighting,composite}
          cinematic/{skinning,depth,material,face,lighting,grade}
          common/{id-pass,tonemap,blit}
        tests/                            software Vulkan unit/integration
    packages/
      world-schema/src/render-contract.ts   IMPLEMENTED v1 message schemas
      simulation-core/src/render-adapter.ts  IMPLEMENTED world-state adapters
      simulation-core/src/world-navigation.ts  PROPOSED seeded static and authored tile movement domain
      save-system/src/                      upgrade old saves with optional navigation state
      narrative-core/src/                   continue using authored scene/choice authority
    content/
      visual-packs/core/                    EXISTING manifest (51 metadata recipes)
      world-packs/                          PROPOSED original tile + collision maps
      rigs/                                 PROPOSED original glTF/mesh and sprite rig registry
      fx/                                   PROPOSED app-bundled shader material presets
    tools/
      asset-pipeline/                       PROPOSED atlas/glTF/KTX2 packing, license/hashes
    docs/
      LIVEIT_RENDER_ENGINE_ARCHITECTURE_V1.md   THIS CONTRACT
      design/LIVEIT_RENDER_GRAPH.mmd        architecture sequence visualization

The module names/paths are proposed next implementation locations, not claims those directories exist now. Do not commit partially wired iOS podspec or Android gradle hacks and then mark builds complete.

## 4. Renderer schema: what is already executable in Step 3

The new world-schema/render-contract.ts defines:

- PixelRenderFrameSchema: protocolVersion=1, timelineId, sceneRevision, day, playerEntityId, resource location ID, 16px tiles, logical camera, map ID, actor stable IDs, ages, saved appearance, facing, sprite atlas/pose, ambient lighting.
- CinematicRenderFrameSchema: identical world stamp plus existing VisualSceneSchema (actors, place, age, outfit/appearance, expression, camera, lighting, props), checked against player identity and world day.
- GameRenderFrameSchema: validated union of both visual registers; no GPU execution occurs during validation.
- RenderUserIntentSchema: cardinal walking, target interaction and authored choice requests with player ID, scene revision and strictly ordered input sequence; native is not permitted to commit a life action.
- OutcomeReceiptSchema: pending/committed/failed, category, event ID and factual deltas. A confirmation haptic is forbidden while pending/failed. The SaveCoordinator must update receipt status after actual storage acknowledgment.
- RenderQualitySchema: battery/balanced/quality, fps budget, 3D resolution scaling, reduced motion and haptic strength.
- planPixelViewport: deterministic integer scale/viewport policy that does not bilinear-blur logical pixels.
- isFreshRendererIntent: basic stale-revision/player check; runtime must additionally enforce monotonically increasing inputSequence, collider checks, authoritative availability and pause/screen focus.

The simulation-core/render-adapter.ts supplies buildPixelRenderFrame and buildCinematicRenderFrame. The former requires an **explicit real navigation pose argument** because current World v1 does not persist x/y or facing; it MUST NOT invent a supposedly saved location. The latter reuses buildVisualScene to keep the same saved identity and appearance in story and chat. These are data-contract helpers, NOT an iOS/Android native renderer.

Production hardening before binary/FFI binding:

- Add stable scene-pack and tile collision-map hash, tile/world-space coordinate conventions and authoritative NPC roster.
- Add strict resource ID resolution against installed asset index; current adapter uses expected future tilemap/atlas IDs that may not yet exist; fail visibly, never secretly pretend a missing pack rendered.
- Bound frame actor counts and payload bytes; reject NaN/Infinity, oversized ID lists, duplicate actor IDs, invalid choice ID and cross-timeline snapshots.
- Add a scene content revision and generation token to reject late GPU and asset callbacks from a previous world/tab.
- Migrate JSON to versioned compact binary/struct mailboxes ONLY when profiling proves bridge cost; avoid runtime reflection of every frame.
- Maintain explicit state version compatibility; unknown incompatible version triggers readable fallback and leaves saved world intact.

Sample transport snapshot, illustrative fields only:

    {
      "protocolVersion": 1,
      "mode": "pixel-overworld",
      "sceneRevision": 73,
      "timelineId": "main",
      "gameDay": 9,
      "playerEntityId": "main:player",
      "locationId": "liveit.location.bellweather-market",
      "tileSizePx": 16,
      "tileMap": "liveit.tilemap.market-core",
      "camera": {"centerX": 8, "centerY": 8, "zoom": 1},
      "ambient": "dusk",
      "actors": [
        {
          "entityId": "main:player",
          "appearance": {"...":"full saved appearance"},
          "ageYears": 23,
          "position": {"x":8,"y":8},
          "facing": "south",
          "animation": "idle",
          "spriteAtlas": "liveit.atlas.player-core"
        }
      ]
    }

Do not treat this abbreviated illustrative appearance object as valid schema input. Actual schema validation requires all appearance enum properties.

## 5. Coordinate systems and precision

World:

- Pixel town uses authored TileCoord (int32 x/y), world positions in tile units (float/fixed) with x east, y south. Sprite anchors at feet, not texture top-left.
- Logical art pixels = tile coordinate * 16 + offset; camera centers in logical art pixels, rendered with end-of-frame pixel snap to avoid shimmering.
- Collider footprints are smaller than visual sprites; actor world position and collision resolution do not derive from GPU alpha.
- 3D cinematic uses meters and right-handed x-right, y-up, z-forward convention with positive height. A scene attachment holds canonical actor identity and rig root; do not interpolate the 2D x/y directly into facial bones.

Pixel camera:

- GDS-001: 320×256 nominal viewport and 16×16 source tiles, dynamically extend/crop by device ratio. Baseline is a visual design frame, not Game Boy 160×144 resolution.
- Example target 960×768 physical viewport => scale 3, visible 320×256 art pixels. A taller display can expose more vertical world area while maintaining integer nearest-neighbor scaling.
- Compute viewport and safe area in **device physical pixels**, not CSS dp. The phone's notch and bottom HUD are excluded before scale selection. Place any fractional remainder as an even letterbox inset/crop (never stretch).
- A player walk can update physics at fixed tick step and interpolated camera/world positions at subpixel precision; final sprite pixel alignment happens only when rasterizing. The camera follows with a bounded damping spring measured in world logical pixels while keeping nearest texture sampling.
- Do not use TAA, FXAA, bilinear atlas filtering or mip filtering on pixel-layer art unless an isolated optional effect does not blur edges.

Cinema camera:

- Perspective/orthographic authorable camera, true 3D transform hierarchy; sampled in physical device resolution with dynamic render resolution 0.7–1.0 as chosen.
- World-space actor positions and camera are used for geometric ray picking; character heads are protected in safe framing when dialogue docks expand or keyboard appears.
- Smooth sRGB/linear lighting pipeline, standard tonemap and artist controls; do not pixelate 3D cinema to imitate overworld.

## 6. Pixel Overworld GPU pass graph

A frame command goes through:

    DirtyChunkUpload (if world tiles changed)
     -> VisibleChunkCull and SortedAtlasInstances
     -> PixelTileColor (R8G8B8A8_UNORM, logical size)
     -> EntitySpriteColor and DepthSort (same logical render target)
     -> PixelWorldOcclusion (roof overlays, wall masking)
     -> LightAndWeather (logical/pixel-aware, tunable quality)
     -> CrispPresentationBlit (NEAREST to device render viewport)
     -> NativeHUDOverlay (real accessible controls)

Asset format:

- Author original environment tiles 16×16, pack to GPU RGBA atlas with padding and controlled UVs (2–4px border extrusion / guard pixels if required); no texel bleeding or half-pixel UV mistakes.
- Sprite animation atlas: named entities with four cardinal directions and four walks per direction initially, plus idle/interaction; animation frame via fixed gameplay elapsed time, not independent desynchronized frame clocks.
- Region chunking: suggested 32×32 tiles per chunk with 1-tile overdraw margin; maintain resident center chunks + neighboring chunks; shader draws visible tiles via instancing rather than 2000 draw calls per tile.
- GPU tile shader: instanced quad with atlas UV, material/palette index, transform; batched by texture/pipeline; correct alpha sorting with roofs, vegetation and actor feet. Transparent windows/particles use defined layer order; no unspecified z fighting.
- Nearest rendering: VkSampler magFilter/minFilter=VK_FILTER_NEAREST, mipmapMode=VK_SAMPLER_MIPMAP_MODE_NEAREST for sprite textures, clamp/wrap as intended, output target sampled nearest at exact integer ratio; disable unwanted display transform filtering.
- Interior roofs that obscure the avatar may fade only while the player passes under an authored occlusion mask; the pixel silhouettes remain comprehensible.
- Palette/weather: region palette LUT, light/color ramps and tile-aware dither; stars/fireflies, rain droplets and window emissive under caps. No full-scene blur, noisy CRT distortion or overbright neon overriding original tiles.
- Picking: convert tap from device-local viewport coordinate to integer logical pixel -> world camera -> tile grid; collision map resolves target. Name/ID validation happens in domain after native renderer emits interact intent. GPU ID buffer can optimize visual selection, but is never authoritative game state.

Example shader/pipeline intent (not a claim that the shader has been implemented):

    layout(set=0,binding=0) uniform sampler2D uSpriteAtlas;
    // Fragment shader input: UV from instanced tile/sprite quad
    vec4 texel = texture(uSpriteAtlas, uv);
    // GPU pixel target is logical resolution; the presentation blit uses NEAREST

Shader compilation: GLSL/HLSL authored under native/liveit-render/shaders, checked into source; build compiles to SPIR-V at packaging time, validates with spirv-val, records shader module hashes and licensed includes. CI tests white/black edges, seams and palette comparison against golden images. Runtime variants are compiled/cache-populated before warm scene transition, never downloaded as executable shader from an asset pack.

### Movement/collision/navigation domain details

Input sampling is render-frame independent, but game movement uses a fixed timestep (recommended 30 or 60Hz) on the authoritative player-state reducer. For grid feel, move one tile over 160–220ms after acceptance; visual interpolation makes it smooth, without changing the tile-collision outcome. Direction state machine: Idle -> Turn -> Walking -> Arrived; bumping solid geometry triggers Blocked -> Idle. No haptics every step. Support screen pad, touch-to-route and hardware keys/controllers; keyboard focus on message composer takes priority over movement.

Collision layers: solid ground obstacle, walkable ground, doorway, interactive front collider, actor physical footprint, dynamic blocked area and transit/water. Door triggers real location transitions; indoors have distinct collision maps and return points. A* on bounded logical grid for tap route, with maximum node/path budget, recompute when NPC obstruction changes. NPC navigation and crowds simulate deterministically from seeds and time-of-day schedules, but NPC AI text generation does not drive movement physics directly.

**Persisted movement is missing in current WorldSchema v1.** The upgrade is explicitly deferred to implementation: add an optional well-typed worldPosition object with region ID, x/y tile, facing, building entrance ID and revision; validate on load and choose valid default spawn for legacy saves; do not break existing saves or overwrite player day/relationships. A sprite walking loop with no persistent x/y is **not acceptable final Free Roam**.

## 7. True 3D cinematic render graph

Do not confuse native/city-vulkan/shaders/actors.comp (procedural GPU 2.5D face shapes) with a shipping 3D skeletal actor. Real 3D requires authored GLB/glTF meshes, skeletons and facial animation blendshape targets with physically coherent environment geometry and GPU draw passes.

A cinema frame:

    SceneReady + VerifiedAssetRefs
      -> AnimatedSkeletonPose (CPU or compute skinning)
      -> GPUCharacterSkinning / MorphTargetPose (blendshapes)
      -> EnvironmentAndPropVisibilityCull (LOD / frustum)
      -> ShadowAtlasDepth (scene lights, contact)
      -> OpaqueEnvironment PBR/toon-lit base color
      -> CharacterSkinHairClothMaterials (subtle SSS, anisotropic hair as supported)
      -> FacialExpressionEyesLips + Gesture (same rig, animation blend)
      -> Transparent/Particles and optional depth atmosphere
      -> ArtistGrade, Tonemap, Glow and selective Outline
      -> CinemaComposite (dialogue safe area and color conversion)
      -> NativeDialogueDock/Text/ChoiceWidgets (separate view layer)

Character requirements:

- Model/rig family with consistent named joints (hips/spine/chest/neck/head/arms/hands and facial controls), eyes gaze, eyelids, brow shapes, mouth/lips/cheeks, fingers, hair attachments and cloth/outfit parts.
- Existing 12 expression names map to a set of weighted facial morph targets and body expression cues. Time-aligned phoneme/viseme mouth blending can be derived from text duration until licensed voice/dialogue exists. Expressions cannot assign XP, trust or change scene speaker.
- Animations state machine includes idle, listen, speak, laugh, cry, anger, worry, shy, gesture and age/posture variations. Crossfade 100–300ms where emotionally appropriate; no hard snap between poses.
- Camera rigs: establishing, medium 2-shot, over-the-shoulder, close-up, dramatic push, reaction cut and shared group composition. Framing constrained by eye/head bounds and adaptable text dock height.
- Skin tones are validated under changing daylight, candlelight and studio lighting without reducing darker skin to black or blowing out lighter skin. Facial acting must remain legible in low quality.
- Outfit geometry/materials resolved from the same appearance enums that select pixel sprites. Invalid rig combinations fallback to approved safe default with a clear content issue recorded.
- PBR/illustrated stylization is controlled through shader layer: roughness, diffuse ramps, rim, constrained outlines and artist-authored palettes, rather than brute photorealism. The scene's color palette should be local to location/time/life stage.
- Cinema uses linear filtering, anisotropy where available, mip LOD, compressed textures, stable shadow maps and motion interpolation. Unlike pixel mode, it can use TAA or temporal reconstruction selectively if measured/shipped without ghosting facial expressions and hair.

World/cinema parity: 2D footprint x/y is resolved to a cinematic scene anchor, **not** assumed to be an exact 3D mesh coordinate for every café. Scene contents are authored set IDs with all present entities, valid wardrobe, right day/weather, and a link back to the player's over-world location.

## 8. Cross-mode character asset resolver

One stable CharacterIdentity ID and Appearance struct resolve two visual representations:

    Canonical CharacterIdentity (saved player/NPC stable ID)
      + Appearance enums (skin/eyes/hair/body/outfit/accessories)
      + AgeDays + current equipped items
      + event-memory and mood context
                |
       CharacterVisualResolver
         /                 \
    PixelAssembly         CinematicAssembly
    sprite family         rig family
    body silhouette       skeleton/mesh
    facing frame          joint/face animation
    outfit palette        actual outfit mesh/material
    age sprite layer      age morph/material layer
         \                 /
          VisualParity QA / animation continuity

Every authored part has semantic slot; material palette/color tokens matched across both representations. The registry needs a stable mapping from each canonical cosmetic enum to sprite region set AND 3D slot/variant, plus fallback availability and rig compatibility. This should be versioned data from asset manifests and tested against every enum key. The same person must have a recognizable hairstyle, skin, accessory and signature outfit in the world, editor, stories, phone and legacy flashbacks. The current manifest has only shader-backed procedural **recipes**, not actual sprite atlases or glTF rigs.

Key age thresholds are driven by actual simulation age (0–12 child, 13–19 teen, 20–35 young adult, 36–61 midlife, 62+ elder art grade) as design default; do not back-compute aging from screen/camera. Facial/body morphs and clothes may transition gradually; avoid assigning an emotionally bleak palette to every older person.

Additional behaviors: outfit purchase does not equip automatically unless the economy rule says so; scene assets remain valid if an NPC is absent/deceased; a past-memory cinematic can use archived appearance based on past event metadata (with limitations disclosed), never pretend present clothing existed decades earlier.

## 9. World-to-3D handoff and lifecycle

Define explicit orchestration with monotonically increasing generation tokens and one controlling focus stack:

    PixelActive
       | interact deep / authored scene
       v
    LockPlayerAction (requires entity and validated interaction radius)
       v
    PrefetchCinematicAssets (bounded timeout / cancel)
       v
    FreezePixelPresentation (remember x/y/facing, camera, relevant asset refs)
       v
    FadePixelToCinema (reduced-motion alternative)
       v
    CinemaActive (story scene, facial emotion, choices and talking)
       |
       +-> ChoicePending -> DomainCommit -> SaveAck
       |                        |
       |                        +-> Outcome widget/haptic
       |
       +-> ExitRequested -> CinemaCleanup -> UnfreezePixelAtValidCoord
                               -> PixelActive

On every asynchronous completion, compare generation and sceneRevision with active token, or silently discard stale result. The first successful scene retains the pixel renderer resources warm for quick return if memory permits. When memory pressure is high, release noncritical 3D resources first and reconstruct only after identity and scene packet validation; never discard the authoritative world.

Errors:

- Could not prefetch 3D: keep player position, show accessible dialogue fallback or explicit retry/return—not fake 3D.
- User cancels before start: discard pending scene and don't commit a choice.
- GPU device lost mid-dialogue: preserve scene/story choice progress; suspend 3D view, show readable fallback; recreate GPU resources after OS allows.
- App backgrounds mid-transition: stop frame submission; store return token and domain state; rehydrate from authoritative save. Do not dispatch duplicate choose command on restore.
- User opens chat while walking: lock movement only if an interactive text/composer overlay has focus, following GDS-002 focus rules.

Transitions should visually use pixel iris/ink/mosaic and a smooth 3D scene reveal. Target warm latency under 750ms, cold load with explicit progress rather than invisible blank frame. Time targets are design goals, not measured. Retain a set of prewarmed common actor/room resources within memory limits.

## 10. Native bridge: explicit ABI, threading and ownership

Use a local Expo Modules API module as a native view. The official Expo native-view guide demonstrates ExpoView on iOS/Android, requireNativeViewManager, Prop setters and event forwarding through nativeEvent. Do not use Expo Go to test custom native modules: build a proper dev client/native install using expo run:ios and expo run:android or equivalent.

Proposed JS API interface:

    type RendererMode = "pixel-overworld" | "cinematic-3d";
    type NativeFrameEvent = {
      generation: number;
      sceneRevision: number;
      kind: "ready" | "pick" | "device-lost" | "stats" | "error";
      rendererMode: RendererMode;
    };
    interface LiveitRendererProps {
      snapshot: GameRenderFrame;
      quality: RenderQuality;
      onRendererEvent(event: {nativeEvent:NativeFrameEvent}): void;
    }

The actual generated implementation binds the existing Zod-validated Frame/Quality schema before sending across FFI. Do not pass a new huge JSON frame on every vsync: send whole immutable snapshots only on scene/identity changes, small pose/direction diffs on gameplay fixed ticks, and let the native frame scheduler extrapolate/interpolate presentation. Batch messages and cap queue length (max latest snapshot + bounded priority commands). Render thread never blocks on JS callbacks, networking, disk or React layout.

Platform:

- Kotlin ExpoView wraps an Android SurfaceView. SurfaceHolder.Callback.surfaceCreated/surfaceChanged/surfaceDestroyed owns and transfers ANativeWindow to C++ via JNI. Acquire/release references correctly. On main/UI thread, create/destroy view only, enqueue renderer operations, receive bounded events; on background thread, create Vulkan instance/device/queues/surface/swapchain and render. Surface pause/resume and orientation changes force swapchain rebuild only when safe.
- Android Vulkan requires extensions VK_KHR_surface, VK_KHR_android_surface, VK_KHR_swapchain (plus device-required supported extensions) and correct transfer to ANativeWindow. Vulkan device and present queue capability checks must succeed; discover formats and present modes, prefer FIFO for safe pacing; handle OUT_OF_DATE/SUBOPTIMAL.
- iOS Swift ExpoView hosts a CAMetalLayer on UIView. Objective-C++ bridge provides the CAMetalLayer pointer to shared C++ code, creates VkSurfaceKHR using VK_EXT_metal_surface and handles display drawable scale, resize and detach. The view must have correct layer lifecycle/delegate association. MoltenVK.xcframework is bundled/link-verified with correct simulator/device slices and license. Vulkan portability enumeration/subset is probed and enabled **when advertised**, not blindly assumed. See official MoltenVK runtime guide.
- Vulkan code is common C++17/23 source; platform adapters provide only surface, storage and event callbacks. Do not link desktop Vulkan SDK into iPhone app as if it were iOS native library. Build via platform CocoaPods/Xcode linking and Android NDK/CMake.
- The renderer maintains a unique surface generation, guards against double-init/double-dispose; any object held across native view destruction has explicit ownership and no raw UI pointer after detach. CPU/GPU ring buffers are bounded; mapping a GPU result back to CPU every frame (as the current headless PPM tester does) is forbidden for live rendering.
- Use separate command buffer resources per in-flight frame, fences and per-frame semaphores; present semaphore use/reuse must follow actual swapchain image acquisition and display-release contracts. Use synchronization2 or validated core barriers where supported, no guessing image layouts.
- Renderer returns capability flags: surfaceAvailable, pixelPassAvailable, cinematicPassAvailable, downloadedAssetsReady, actual device name/tier, and current fallback reason. Expo view activates only when capabilities have been positively checked.
- Web uses a functional browser/canvas/RN fallback without claiming Vulkan; arbitrary copied native APIs must never be attempted on web.

Pseudocode C++ class sketch; file ownership planned, not compiled:

    class RenderHost {
     public:
      void attachSurface(PlatformSurface surface, uint64_t generation);
      void submitSnapshot(const ValidatedFrame& snapshot);
      void enqueueInput(const NativeInput& input);
      void setQuality(const Quality& quality);
      void resize(uint32_t drawableWidth, uint32_t drawableHeight);
      void suspend();
      void resume();
      void renderFrame(FrameClock& clock);
      void detachSurface(uint64_t generation);
     private:
      DeviceResources gpu_; // RAII: destroy only after device synchronization
      PixelWorldRenderer pixel_;
      CinematicRenderer cinema_;
      AssetCache assets_;
      BoundedMailbox commands_;
      uint64_t generation_ = 0;
    };

The actual Vulkan presentation logic must use swapchain images, acquire/present, explicit barriers and per-frame fences; GPU frame captures recorded from the installed simulator/phone are the evidence. Avoid a separate native scene engine recreating life/NPC simulation logic.

## 11. Timing, animation and frame scheduler

Simulation tick is **authoritative**, rendering interpolation is ephemeral:

- Life/day/annual ticks occur only via explicit player action, never because the app produced 60 frames. No background simulator autonomously drains money because a view kept running.
- Movement animation fixed tick (recommend 30/60Hz) independent of Vulkan display frame; stable delta-time and cap maximum catch-up ticks after resume to avoid huge teleport loops.
- Presentation maxFPS configurable 60/30 and respect system power/reduce motion; animation time in render packet uses monotonic frame-time local to view, not absolute Date.now() as a world clock.
- UI choice acknowledgements should appear within p95 50ms on test hardware while action commit/save takes as long as needed and is honest.
- Dialogue typewriter speed, mouth movement and gestures are controlled by storyboard timers from a deterministic scene director; remote AI tokens may stream into accessible text but no arbitrary shader code.
- Frame scheduler time-to-first-frame, CPU submit, GPU duration, display latency and present mode are separately measured. Frame time 16.67ms for 60fps and 33.33ms for 30fps; do not infer FPS from a successful offscreen shader dispatch.

In cinematic mode 3D animation can continue during dialogue card view only when authorized; menu pause may freeze presentation, but should not accidentally alter game time, story state or NPC simulation. Focus states: gameplay locomotion and chat composer cannot both accept WASD/arrow keys.

## 12. HUD, authoritative widgets, haptics and event ordering

HUD is not a shader-only texture if it contains essential text, screen-reader controls, report/block controls or user-supplied text. The GPU can draw decorative panel skins, cinematic transitions, pixel-shaped icons, particles and maps, while an accessible RN/native layer handles text and semantic interaction.

Event command flow:

    press(choiceId, sequence, current sceneRevision)
      -> immediately show pressed visual state (no consequence yet)
      -> domain validates choice against current saved world / story
      -> produce pending save revision
      -> save coordinator serially persists validated new world
      -> confirmed revision, exact eventId, actual calculated deltas
      -> OutcomeReceipt(status=committed, real deltas and category)
      -> HUD queues the widget + one permitted haptic
      -> scene may change, but receipt remains available in journal
    on failure:
      -> OutcomeReceipt(status=failed, no success haptic)
      -> show precise failure/retry; preserve last saved state

Native renderer intents have sceneRevision, entity ID, inputSequence; enforce increasing sequence per generation and actor, reject stale commands and duplicate submissions. Hash/event ID is not an authoritative security token; real account/server human messages need separate auth, moderation and network policies.

Outcome widgets contain title, type, actual stats/relationship deltas, source event/time and actions "view journal" / "dismiss." If save coordinator uses optimistic UI, temporary visuals must be marked pending and be reversible. The proposed OutcomeReceiptSchema refuses a confirmation haptic unless status=committed. It does not itself call haptic APIs. Add a haptic service in Step 4/implementation that respects OS capabilities and preference Off/Subtle/Full; no per-step/vsync vibration, no celebrations for death, grief or serious harm.

## 13. Audio and action-to-motion timing

Game UI tactile grammar from GDS-001:

- touch acknowledgment 0–50ms target, short press spring 80–140ms;
- menus/drawers 160–340ms with semantic focus;
- warm pixel→cinematic handoff 450–750ms;
- milestone time-advance 600–1400ms with skip;
- scripted cut/reaction emotion as scene director decides, with reduced-motion simple crossfade.

Use haptic selection for discrete menu focus, confirmation after persisted meaningful choice, warning for relevant error only, quiet for background graphics and distressing milestones. Audio independently adjustable music/sfx/ambience/notification; compile an original licensed audio pack and track voice/music legal rights. Motion/time settings survive restart and apply to both rendering modes.

## 14. Saved location, appearances and future migration

Current WorldSchema schemaVersion=1 and save-system persist main/standalone narrative state, but there is no authoritative walking position or interactable town graph yet. Migration required:

    world.visualNavigation? = {
      regionId: "liveit.region.market",
      mapRevision: 1,
      tileX: 9,
      tileY: 7,
      facing: "south",
      interiorId: null,
      returnPortalId: null
    }

The above is a PROPOSED v1-compatible optional field. Do not add it to current saves or claim migration completed in this step. Final policy:

- optional default for old lives, valid authored entrance/spawn selected once by deterministic rule; no forced new life;
- serialized world references content-pack version, scene IDs and current story progress by stable IDs; avoid plain string open-coded arbitrary names in production;
- save snapshots/ledger use revision monotonicity and idempotency keys. For meaningful choices, use atomic update of world and event metadata or app-level transaction/recovery journal; a screen-only animation does not imply durable save.
- if content pack is uninstalled/missing, retain world identity and asset reference; show safe default face/outfit and an explicit install action if authorized. No silent mutation of original saved appearance enum to "default".
- old memories and past character outfits can be replayed only if historically recorded; otherwise an archive card explicitly says original look unavailable.
- an NPC memory provider must be filtered/permissioned; generated prose cannot directly execute DomainChoice or stat changes.

## 15. Growing asset/publisher pipeline (the only way to scale)

Asset authoring to device:

    Original authored 2D/3D sources (licensed and attributed)
       -> source validation (license, pixels/model glTF, shader/material policy)
       -> semantic slot + canonical appearance ID mapping
       -> 2D nearest-neighbor atlas build / 3D mesh compression
       -> 3D texture KTX2/BasisU transcode profiles (ASTC/ETC2/device)
       -> skeleton/bone morph and outfit compatibility smoke
       -> pack manifest: version/deps/path/bytes/SHA-256/rig slot
       -> QA: pixel at 1x/3x and 3D face at medium tier
       -> signature and immutably versioned index
       -> app-gated authorized staged download
       -> SHA-256 + size + dependencies + game minVersion + signature validation
       -> atomic activation / last-known-good pack pointer
       -> GPU upload/cache/eviction; offline fallback and attribution access

Validation already has a preliminary prepareVisualPackActivation function that checks sizes/hash/dependencies/version and returns a candidate index. **It does not implement digital signature checking, on-device storage transaction, transport, on-demand loading, license auditing or native GPU atlas upload.** Those are implementation gates.

Commercially distributable content must not be harvested from Nintendo/Episode games or reverse-engineered proprietary app assets. Existing licensed Kenney CC0 placeholders can be a temporary technical stand-in where appropriate, but final retro tile atlas should be original and self-consistent, and 3D faces require actually modeled character art.

Quality/storage budget from original brief: under about 150 MB core where practical, texture atlases around 2048 pixel max per page, <=600MB total runtime memory mid-range target, with content streaming and a user-visible eviction/storage panel. These are acceptance targets, not measured. Avoid using React/JS memory for full uncompressed texture assets if GPU-native loader and streaming can do so efficiently.

Do not permit content packs to ship runtime SPIR-V/MSL/JNI/Swift scripts. New visual materials must be instance parameterizations of vetted app-bundled shader families. Signed downloads do not make arbitrary executable code safe.

## 16. Real-time performance budget / quality tiers

Targets for first profiled GPU device class (provisional, never asserted measured):

- 60fps target: 16.67ms total frame. Plan CPU game/input/handoff ~1.5–3ms, GPU pixel-world + weather/composite <=5ms, 3D cinema GPU <=9–11ms high tier, headroom for OS/UI/present. These components may overlap, so sum is diagnostic, not arithmetic guarantee.
- Battery tier: max 30fps, cinematic internal scale ~0.7, simpler shadows/skin/hair, no expensive bloom/DOF. **Pixel layer stays crisp and tile-aligned** (integer world scaling).
- Balanced tier: target 60fps only when thermal headroom exists; cinema internal scale ~0.85, normal shadows/FX.
- Quality tier: target 60fps, cinema internal scale 1.0, preferred shadow quality and full facial animation.
- Memory: bounded GPU resource manager, staging ring, atlas residency cap, VRAM and CPU caches. GPU resource destruction after fences. Pooled framebuffers sized by viewport/quality; resize triggers only necessary reallocations.
- Avoid uploading new full tile atlases every frame; dirty rectangles/visible chunks only. Idle NPC crowd animation budget bounded by visible actors and LOD. Named closeups high detail, distant NPCs cheap.
- Renderer posts anonymized local diagnostic samples in debug builds: device, mode, scene ID, fps distribution p50/p95/p99, CPU and GPU durations, frame misses, uploaded MB, evictions, allocation failures, present/out-of-date counts and swapchain recreate count. Never send private dialogue/real chat content with analytics.
- Treat thermals seriously: measure 10-minute exploration and 10-minute conversation on a low-spec Android test device and a physical iPhone. Xcode simulator success alone is not a real phone performance result.

## 17. Device, safety, resilience and permissions

- Screen reader labels and keyboard focus for all HUD controls, captions and chat. Native shaders can draw visual skins but not replace semantic text, legal terms or report/block actions.
- Landscape/tablet layouts from GDS-002; cameras preserve eyes and gameplay tile visibility, controls do not overlap safe areas. Multiple panels close through system back and Esc.
- World can operate offline (life progression, authored story, local assets), AI NPC chat declares provider/network dependencies and offers honest fallback. Real-player social never silently substitutes an AI NPC or fabricates online status. Clearly separate real and AI in both view and protocol.
- iOS distribution concern: platform rules restricting apps primarily for anonymous/random chat mean original "AnonChat" must be an optional, context-based, safety-governed social experience (or omitted on platforms where not permitted), not a random chat product hidden behind a life-game shell. Consent, moderation/report/block and age restrictions are architectural external requirements, not shader tasks.
- GPU crash/driver issue: store last good save, exit renderer thread safely, release swapchain/attachments, show readable fallback and explicit retry. Never destroy saved world to "fix" a renderer.
- Shader and native packages carry reproducible version, licenses and checksums; run Vk validation layers in debug and AddressSanitizer/UndefinedBehaviorSanitizer on supported development platforms. CI must not distribute developer validation layers as if required for consumers.

## 18. Verification matrix, CI and QA

| Layer          | Deterministic test                                                                                      | Required release evidence                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Schema/ABI     | Vitest validates frame versions, actor identity parity, invalid inputs, stale scenes and receipt states | tests/render-contract.test.ts passing, TypeScript and lint green                         |
| World movement | fixed-step collision, doorway/return, tap-route A*, save/restore, blocked/multitouch                    | scripted seeded action trace and screenshots                                             |
| Pixel GPU      | nearest atlas filtering, no seams at 1x/2x/3x, palette/shadow/weather                                   | PNG/golden captures from true Vulkan and pixel equality/approved tolerance               |
| Cinematic GPU  | actual skinned glTF rig and 12 expressions, different outfit/lighting                                   | GPU captures from scene with true 3D geometry, not actors.comp procedural faces          |
| Bridge         | native device/swapchain init, resize, background/foreground, loss/rebuild, stale event                  | iOS simulator + physical iPhone; Android emulator + physical device native logs/captures |
| Handoff        | player↔NPC identity parity, pixel location preserved, exact return                                      | scripted mobile E2E video with real UI interactions                                      |
| Persistence    | idempotency, failed AsyncStorage write, duplicate choice, crash after commit and before widget          | durable journal/recovery tests                                                           |
| Assets         | pack hashes, license metadata, truncation, duplicate/cycle, budget caps, rollback, offline              | validated install/uninstall on actual devices                                            |
| Haptics / HUD  | semantic actions, disabled/reduced motion, focus/accessibility                                          | device haptic instrumentation and TalkBack/VoiceOver manual QA                           |
| Performance    | frame-time distributions, thermals, memory, power, 10-minute play                                       | measured device reports, not source-code promises                                        |
| Safety/social  | real-vs-AI labeling, no fake contacts, report/block, abuse fallback                                     | QA with multi-client test accounts and policy review                                     |

**Existing CI:** .github/workflows/city-vulkan.yml compiles and runs the headless Vulkan compute PPM previews using Mesa Lavapipe, with pixel-change assertions. This is retained as a GPU regression suite but cannot prove the above release gates.

**Step 3 newly added and unit-tested code:** render-contract.ts, render-adapter.ts and tests/render-contract.test.ts; in CI the normal npm run check covers lint/types/Vitest and metro exports. Stop short of saying native Expo module exists or simulator installed until separate native test logs substantiate that.

Recommended proof commands:

    npm ci
    npm run check
    cmake -S native/city-vulkan -B build/city-vulkan -DCMAKE_BUILD_TYPE=Release
    cmake --build build/city-vulkan --parallel 4
    ctest --test-dir build/city-vulkan --output-on-failure

Following native module integration (these commands will NOT verify it yet):

    npm run ios
    npm run android
    # capture real simulator/device frame and input E2E with test fixtures
    # record names/versions/hashes of downloaded source artwork and native SDK

Test with 4 representative devices: small/older Android, mid Android, physical iPhone, iOS simulator; and layouts narrow portrait, standard portrait, tablet/landscape. Explicit tests for missing mesh/atlas and pressing home button mid-conversation. User must not lose progress due to rendering failure.

## 19. Implementation dependency graph and executable milestones

This section identifies **future engineering implementation**, not work completed by writing Step 3.

**R0 — World/navigation authority:** define optional persisted world tile coordinate/location/facing, collision map manifest, fixed-step input reducer, event sequencing and old-save migration. 2D navigation tests green. A free-roaming avatar must actually move through Bellweather.

**R1 — Real pixel GPU path:** produce one original tilemap + one original 4-direction actor atlas. Build Vulkan tile/sprite raster pass + nearest presentation, scene camera, independent UI overlay. Capture screen on Android phone.

**R2 — Native iOS/Android bridge:** package Expo native view + shared Vulkan core, correct MoltenVK Xcode linkage and Android NDK; actual swapchains, lifecycle, fallback, safe-area resizing. Confirm both native platforms render the same pixel town rather than a CPU screenshot.

**R3 — NPC/tile interaction and scene handoff:** approach named NPC, authorize interaction in deterministic domain, preserve tile location, warm asset scene and open dialogue with controls that can be dismissed without duplicate consequence.

**R4 — True 3D actor vertical slice:** import one legitimate rigged character plus second NPC, approved clothing/hair materials, real scene geometry, face 12-expression demonstration, 2-shot/close-up camera, lip/eye animations. Render actual GPU frames on both platforms, not just a PPM.

**R5 — Shared appearance resolver:** matching hair/outfit/skin/age across pixel and 3D; editor changes persist after app kill/relaunch. Automated identity parity test over at least 12 representative combinations.

**R6 — HUD and outcome/haptics:** choice dock, bounded native event feed, save acknowledgment and factual receipts, haptic settings, journal link, interaction focus arbitration. Prove relationship trust delta correctly appears and remains after restart.

**R7 — Expand city and interiors:** collision/pathfinding, distinct 5 neighborhoods, home/school/work/market, NPC scheduling, weather and day/night with actual world time, district travel and assets streamed.

**R8 — Growing content packs:** actual 2D atlases, glTF models/animations/textures, license hashes, signed publication and on-demand downloads, safe atomic install/rollback, creator preview.

**R9 — Production quality/safety/release:** 200 locations/400 part targets progressively fulfilled through real content, large story chapters, truthful notification systems, actual AI and permitted contextual social systems, accessibility/thermal/metrics playtest.

The first meaningful playable **release gate** is not R9. It is R0–R6 together for one narrow Bellweather street and café: user walks four tiles, hits one blocker, enters café, talks to Amelia in genuine 3D, chooses one branch, sees the real outcome widget/haptic, returns to the same valid world tile, closes app, reopens, and sees the same identity and persisted trust result. Only then should a release note call LIVEIT "hybrid graphics playable on mobile." Until that gate is actually captured on physical iPhone and Android, the status remains architecture/prototypes.

## 20. Architectural decision records

**ADR-001 — Single Vulkan render core:** Keep C++ renderer platform independent and use Android Vulkan and iOS MoltenVK. Accepted because code and shader families are shared, with actual native swapchain/platform differences isolated. Cost is nontrivial iOS linkage and Vulkan portability verification; do not pretend development is free or already done.

**ADR-002 — Separate pixel and cinema pipelines:** Accepted because nearest-neighbor 2D and filtered/3D smooth imagery have incompatible quality needs. They coexist under a single frame orchestration protocol and GPU cache, rather than forcing pixel sprites into 3D closeups.

**ADR-003 — Domain remains in TypeScript:** Existing deterministic world tests and saves matter more than engine rewrite. Renderer should not duplicate money/aging/relationship rules. Performance-critical NPC sprite animation and camera can run natively while simulation actions stay authoritative.

**ADR-004 — UI accessibility stays native:** A heavy shader-drawn all-text UI undermines input, translations, dynamic type, captions and moderation accessibility. Decorative HUD pixel skins can be Vulkan, text/controls remain true semantic UI components.

**ADR-005 — Asset packs are untrusted data:** App-bundled vetted shader families, signed versioned immutable downloaded content, hash/size/dep verification and staged atomic activation. Data-driven growth does not permit executing newly downloaded SPIR-V or arbitrary plug-ins.

**ADR-006 — No silent content-completion inflation:** 51 pack definitions are shader recipe records, not 51 complete visual artworks. Current actors.comp is a 2.5D procedural render test, not the requested stylized 3D face rig. Legacy CityMap is an illustrated selection view, not Pokémon-style roaming.

**ADR-007 — Gameplay intent always validated:** Renderer clicks emit bounded typed intents and IDs; the authoritative game checks collision/choice availability, idempotency and saves. UI consequences/haptics correspond to actual committed state.

**ADR-008 — Recoverable mobile lifecycle first-class:** Scene generation IDs prevent stale events. Recreate/destroy native swapchains correctly on pause, resize and device loss; preserve player identity, return tile and choice state; safe fallback rather than crash/black screen.

## 21. Exact source verification and official technical references

First-party Expo Native View Tutorial: https://docs.expo.dev/modules/native-view-tutorial/ (ExpoView, Prop, Events and requireNativeViewManager).
Expo Modules Overview: https://docs.expo.dev/modules/overview/ .
MoltenVK Runtime Guide: https://github.com/KhronosGroup/MoltenVK/blob/main/Docs/MoltenVK_Runtime_UserGuide.md (Apple CAMetalLayer, VK_EXT_metal_surface, portability enumeration, XCFramework linkage and device limitations).
Vulkan Guide / Specification: https://docs.vulkan.org/guide/latest/ .
Vulkan Tutorial: https://docs.vulkan.org/tutorial/latest/ .
Khronos glTF 2.0: https://www.khronos.org/gltf/ .
Khronos KTX: https://www.khronos.org/ktx/ .
Expo Haptics: https://docs.expo.dev/versions/latest/sdk/haptics/ .
iOS content/social policy: https://developer.apple.com/app-store/review/guidelines/ .
World/source of truth: packages/world-schema, packages/simulation-core, apps/player, native/city-vulkan from LIVEIT feature branch and GDS-001/GDS-002.

The expected code already committed for Step 3 is the _typed architecture boundary_ (render-contract, render-adapter, tests). The actual mobile swapchain, pixel GPU atlas renderer, 3D rigged actors, haptics, motion stack and storage/location migration are implementation milestones to execute in future steps after this design is accepted. Do not conflate a complete engineering specification with completed application graphics.

## 22. Handoff to remaining user-requested steps

Step 1 completed: GDS-001 visual style specification.  
Step 2 completed: GDS-002 43-screen design and interactive atlas.  
**Step 3 completed by this document + typed testable protocol foundation:** engineering/rendering architecture.  
Step 4 NOT YET done by this step: update older conflicting LIVEIT repo vision/art/agent docs and implement the selected integration plan without erasing prior saves.  
Step 5 NOT YET done by this step: full genuine, license-reviewed pixel sprite, 3D rig/model, 3D interior and UI/widget/VFX asset inventory, pack acquisition and production schedule.

**Definition of done for Step 3:** all architecture decisions, contracts, platform hooks, GPU pass graph, world-authority/movement requirements, testing and migration gates are explicit; repo interface code validates, format/type/unit CI green. This does not require (and must not claim) iOS/Android live Vulkan functionality at this stage.
