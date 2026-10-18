# LIVEIT City Sim: Vulkan renderer + retro-native UI

## What is implemented (2026-10-18)

- The player uses the new **Arcade After Dark** palette in `apps/player/src/gameTheme.ts`, with built-in OS fonts: Avenir Next Condensed (iOS)/sans-serif-condensed (Android) for prominent game headings, Menlo/monospace for arcade telemetry, accessible modern body copy. No unlicensed fonts have been added.
- The Free Life city viewport in `apps/player/src/CityMap.tsx` has a reworked illustrated isometric map, five real district travel targets, camera zoom (80–140%), lighting preview, true in-game day count, and pins for currently available city events. Map controls work offline; night/day here changes VISUAL PREVIEW, not the saved calendar.
- `packages/simulation-core/src/city-scene.ts` generates a stable 9×9 block layout with dedicated crossed road corridors, parks, buildings with dimensions/heights, material identifiers and deterministic seed 0xb311. Its geometry and safety constraints have unit tests.
- `native/city-vulkan/` contains actual Vulkan code: GLSL compute shader raycasts block AABBs, renders roads, facades, roofs, basic windows and water/ground into a device-visible host-coherent storage buffer; the C++17 host enumerates devices, finds a compute queue, allocates and binds storage buffers, creates descriptors and a compute pipeline, dispatches and reads back pixels into a PPM file. It probes `VK_KHR_portability_enumeration` and `VK_KHR_portability_subset` when supported, to accommodate MoltenVK.
- `.github/workflows/city-vulkan.yml` installs Mesa software Vulkan (Lavapipe), compiles GLSL with glslc, builds C++ with CMake and tests both day and night; verifies image dimensions, non-flat RGB output, distinct lighting and uploads the genuine generated PPM files. **This workflow passed on 2026-10-18** (GitHub Actions run `39101544442`). This proves the Vulkan *compute preview renderer*, not that Vulkan is already inside the Expo app.

## Explicit limitation

The running phone application still displays the illustrated React Native isometric **fallback**. It does not yet create a `VkSurfaceKHR`, Vulkan swapchain, CAMetalLayer-backed MoltenVK surface or Android ANativeWindow inside the player. The C++ renderer is currently an **off-screen prototype**, and CI uses a Vulkan software driver, not an iPhone GPU. Do not call this a fully integrated native 3D viewport or a populated city simulation with agents/pathfinding. Do not hide the gap by labeling 2D sprites "live Vulkan".

The saved city decisions and daily event opportunities are real LIVEIT simulation data; camera and lighting are presentation-only. Any further city economic/traffic/population simulation should have separate deterministic domain tests, never arbitrary client-local world mutations.

## Build and reproduce Vulkan renderer

Requirements: Vulkan SDK/headers + loader/library + `glslc`, a Vulkan device or software ICD, CMake >= 3.20, C++17 compiler. On macOS, install a compatible current Khronos Vulkan SDK with MoltenVK or existing correctly configured loader and `glslc`; test `vulkaninfo --summary` first. Do not assume the public App Store iOS distribution includes desktop Vulkan libraries.

```sh
cd ~/Desktop/projects/living-universe
cmake -S native/city-vulkan -B build/city-vulkan -DCMAKE_BUILD_TYPE=Release
cmake --build build/city-vulkan --parallel 4
ctest --test-dir build/city-vulkan --output-on-failure

# Offscreen images, true SPIR-V shader dispatched using Vulkan:
./build/city-vulkan/city_vulkan build/city-vulkan/bellweather-night.ppm 512 320 night
./build/city-vulkan/city_vulkan build/city-vulkan/bellweather-day.ppm 512 320 day
```

Use Preview/ImageMagick/GIMP to view or convert PPM. The CLI prints which actual Vulkan physical device ran. Generated images stay in `build/` and can be fetched as CI artifacts, not committed into the React Native build by default. Set `VK_ICD_FILENAMES` only to a verified available ICD JSON if no device enumerates. `xcrun` alone does not provide desktop Vulkan.

## Required native in-app implementation (next build gate)

The iPhone and Android renderer surface cannot be a conventional `expo-gl`/WebGL view; that would render via OpenGL ES, **not Vulkan**. Build a local **Expo Modules API** view using the official tutorials: <https://docs.expo.dev/modules/native-view-tutorial/> and <https://docs.expo.dev/more/create-expo-module/>.

1. Create a local module (proposed `apps/player/modules/liveit-city-vulkan`) with a TypeScript interface accepting `CityScene`, `day`, `selectedDistrict`, camera orbit/zoom and lighting. It returns events for district hit selection and device/error/readiness. Default to the current accessible `CityMap` until compiled native capability is positively detected.
2. **Android**: Kotlin `ExpoView` wraps an owned `SurfaceView`. Native/JNI takes `ANativeWindow`; Vulkan enables `VK_KHR_surface`, `VK_KHR_android_surface` and `VK_KHR_swapchain`; create, acquire, render, present and resize swapchain images. Explicit ownership/lifecycle: render thread, resize, app pause/resume, lost surface, device lost and JNI exception boundaries. Avoid doing synchronous GPU work on React UI thread.
3. **iOS**: Swift `ExpoView` or UIView exposes a `CAMetalLayer`; Objective-C++ bridge invokes the same C++ Vulkan renderer through MoltenVK and `VK_EXT_metal_surface`, `VK_KHR_swapchain` and portability enumeration/subset. Link correctly licensed `MoltenVK.xcframework` through the module's Podspec and correct simulator/device slices. Follow the [Khronos MoltenVK runtime guide](https://github.com/KhronosGroup/MoltenVK/blob/main/Docs/MoltenVK_Runtime_UserGuide.md), including the layer delegate and portability surface configuration. Xcode linker, code signing, simulator + physical phone must pass.
4. Refactor the compute preview to render per-frame to swapchain-compatible targets (or present via a verified copy/transfer path), share city block uploads between platforms and do not map GPU-to-CPU pixel buffers every frame. Maintain clear separation: deterministic world data → scene layout → graphics representation → user interaction → authorized state mutation in TypeScript.
5. Implement camera yaw/orbit, pinch zoom, panning, district ray-pick, physically meaningful day/night response, walking citizens and traffic driven by a deterministic seed, culling and LOD; keep native FPS high while preserving low-power modes, safe areas and touch accessibility. The player map must be useful even with GPU unavailable; test graceful fallback and offline play.
6. Add native iOS/Android simulator E2E: view mounts; known building geometry is visible; selecting district applies a saved travel operation; it persists after force-close; zoom and lighting update frames and respect Reduce Motion; errors show fallback. Compare native screenshots to reference art in both portrait and landscape. Conduct device telemetry for at least 10-minute sessions, startup, frame pacing, GPU memory, thermal impact and rebuild after device loss.

**Do not claim the above six tasks are implemented until verified.**

## Art direction: 60% modern indie / 40% arcade nostalgia

- Shape language: compact beveled-looking panels, 1–2px borders, small 3–5px radii for HUD buttons; preserve readable touch targets (44px minimum).
- Palette: background `#101827`, raised `#223449`, neon `#97E6AC`, amber `#FFD28A`, coral `#F49A82`, text `#F5F2D9`, muted `#B6C6C8`, border `#507174`. City water `#2B617A`, parks `#427969`.
- Font policy: use legible condensed bold headings, mono all-caps on compact readouts only, comfortably sized human dialogue text. A pixel font is an optional *future* branded accent, not a substitute for accessible body text. Should custom fonts be selected, use licensed local `.ttf/.otf` with Expo SDK 58's `expo-font` config plugin and preserve notices; do not download/use font files without license tracking.
- 3D aesthetic: stylized low-poly materials, sharp silhouettes, slightly exaggerated facades, warm window emissives, atmospheric dawn/night and distinct recognizable landmarks for each neighborhood. Do not chase photo-realism on phone.
- Camera: isometric by default; smooth orbit and zoom only when live native 3D is integrated. Selected neighborhood must match the source-of-truth CityState after relaunch.

## Sources

- <https://www.khronos.org/blog/developing-with-vulkan-on-apple-ios>
- <https://github.com/KhronosGroup/MoltenVK/blob/main/Docs/MoltenVK_Runtime_UserGuide.md>
- <https://docs.expo.dev/modules/overview/>
- <https://docs.expo.dev/modules/native-view-tutorial/>
- <https://docs.expo.dev/develop/user-interface/fonts/>

## Ownership, QA and release boundary

All code, shaders, scene generation and palette in this sprint are original. Isometric fallback building sprites remain existing Kenney CC0-provenance assets, referenced in the repository asset registry. No competitor code or proprietary art is imported. The engine uses basic no-cost platform fonts. The Vulkan renderer should eventually be packaged as source or reproducible artifacts with license records for any third-party Vulkan/MoltenVK components. Never ship the Vulkan CI output as misleading proof of fully integrated native graphics.
