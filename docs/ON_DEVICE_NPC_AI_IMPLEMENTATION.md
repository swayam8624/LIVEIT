# LIVEIT device-only NPC AI — implementation and native integration

## Current implementation (2026-10-21)

`apps/player/src/deviceCharacterInference.ts` provides a local GGUF chat runtime, token streaming, serialized inference, safe absent-model fallback, native context unload, bounded context and a strict boundary that forbids generated text from directly mutating simulation state. `deviceCharacterInference.test.ts` adds mocked native-runtime regression tests. **This is a committed native-inference service layer, not yet a working device feature.** No `llama.rn` package, model downloader, native UI bridge or game-screen consumer is installed by this change. No phone or simulator was tested.

## Native deployment choice

Prefer `llama.rn` (llama.cpp React Native binding) for iOS and Android. The documented API includes `initLlama({ model, n_ctx, n_gpu_layers, use_mlock })`, context `completion({messages,n_predict,temperature,stop}, callback)` and context `release()`. Use a custom Expo development build; Expo Go is not capable of loading this native package. Check Expo SDK 58 / React Native 0.88 compatibility and the native module's current New Architecture requirement before installing. Official source: https://github.com/mybigday/llama.rn .

To complete integration on a capable Mac with Xcode and Android SDK:

1. On this branch, run `npm install -w @living/player llama.rn` and `npx expo install expo-build-properties -w @living/player` (or install the compatible Expo package in the player workspace directly); commit **both** package manifests and the regenerated package lock. Do not hand-edit the lock.
2. Add the documented Expo `llama.rn` config plugin and compatible build properties in `apps/player/app.json`, then generate/rebuild native projects. Do not assume the example plugin options work with every supported chip.
3. In a native-only module, import `initLlama` from `llama.rn`, construct `new DeviceCharacterInference({initLlama})`, and connect it to NPC chat actions in the player. Keep web and unsupported devices on an honest unavailable-model path, never silently fall back to a cloud endpoint.
4. Implement user-consented model installation into app-private storage, with model license checks, HTTPS-only download, expected byte count and cryptographic digest verification. Use a curated small GGUF. A remote **model download** is allowed; remote **message inference** is not.
5. Persist installed model identifier/digest and resident memories locally. Deduplicate requests and manage cancellation, memory pressure, backgrounding, platform thermal states and model disposal.
6. Derive dialogue input from canonical NPC ID, current authoritative world snapshot, character relationship and retrieved saved memories. Never trust the LLM output as a gameplay state transition. Save any player action through the simulation/consequence engine first and show successful feedback only after state persistence.
7. Verify install -> airplane mode -> genuine token generation -> scene exit -> save -> kill/reopen -> persisted character continuity. Log time to first token, sustained tokens/sec, peak native RSS, battery/thermal behavior, fallback and storage on real budget and flagship phones.

## Important limitations

- Only the **adapter and tests** are in this PR. No actual native inference has run.
- Models are not bundled or downloaded. Neither the generated character art nor model weights become runtime-ready by being listed here.
- The existing `tools/check_local_llm.mjs` checks a **Mac's Ollama service** and is a developer diagnostic, **not on-device AI**. It must not be marketed as proof of offline-phone operation.
- A client-side model does not make arbitrary user-generated content automatically safe. Device-level privacy, consent, children's safety, reporting and app-store policy checks still matter.
