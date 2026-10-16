# Verification evidence — 16 October 2026

Executed on macOS with Node v22.23.2 and npm 10.9.8. A working Node 22 binary was selected explicitly for shell runs because the host’s default shell environment encountered an unrelated missing Homebrew dynamic library. No host library changes were made.

| Exact command                                                                                     | Actual result                                                                                                  |
| ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `npm install --no-fund --no-audit`                                                                | Installed the workspace dependencies and created the lockfile.                                                 |
| `npm install --package-lock-only --no-audit --no-fund`                                            | Updated lockfile metadata after setting the root package to ESM.                                               |
| `npm run format`                                                                                  | Applied Prettier formatting.                                                                                   |
| `npm run check`                                                                                   | Passed Prettier, ESLint, strict TypeScript for player/packages and Studio, and all 23 Vitest regression tests. |
| `npm run build:player`                                                                            | Passed; exported the Expo web player to `apps/player/dist`.                                                    |
| `npm run build:studio`                                                                            | Passed; Next.js built and prerendered the Studio route.                                                        |
| `npx expo export --platform ios --platform android --output-dir dist-native` (from `apps/player`) | Passed; generated both native Hermes bundles. This is not a signed native binary build or a device test.       |
| `npm run dev`                                                                                     | Started the Expo player at port 8081. HTTP 200 verified.                                                       |
| `npm run start -w @living/creator-studio`                                                         | Started the production Studio server at port 3000. HTTP 200 verified.                                          |
| `xcrun simctl list devices booted`                                                                | No booted iOS simulator. Native interactions were not exercised.                                               |
| `git init --initial-branch=main`                                                                  | Initialized the local repository. No commits, remote, push, or pull request.                                   |

## Regression coverage

23 tests cover deterministic outputs and input immutability; finances and promotion timing; bounded stats; invalid intervals/actions; NPC contact and drift; story-to-life trust and memories; each ending; mid-scene save/resume; conditional execution; stale choices; timeline isolation; incompatible protagonists; missing cast; atomic unauthorized-effect rejection; bounded permissions; executable/unknown field rejection; broken graph references, unreachable scenes, duplicate nodes and dead ends; fallback choices; storage round trips and failures; corrupt/newer saves; conflicting timeline IDs and duplicate relationships.

Initial runs caught an unused test import and an incorrect expected balance. Both were corrected. The seven-day work balance is £2,169: five freelance days and two employed days, including £28 daily costs. Subsequent complete checks passed. An explicit formatting invocation on `.gitignore` reported that it has no parser; normal repository-wide format checks correctly ignore that file and pass.

## Browser interactions

Used the Playwright CLI wrapper at `/Users/swayamsingal/.codex/skills/playwright/scripts/playwright_cli.sh` with isolated `living` and `studio` sessions. Commands used `open`, `snapshot`, `click`, `reload`, `resize`, `eval` for state verification, and `screenshot`.

- Created Alex Morgan through the player UI and entered the café encounter.
- Apologized: Amelia trust changed from 35 to 47 and the next scene appeared.
- Told the truth: trust changed to 57, two memories were persisted, and the story completed.
- Returned to Free Life and reloaded the page. Browser storage still contained trust 57, two memories, and completed progress.
- Started standalone Story Mode. Its initial trust was 35 while the main life retained 57.
- Chose the guarded branch: standalone trust became 27. Reload resumed the `distance` scene with the same branch history.
- Chose more time apart, completed the alternative ending, and switched back to the main life. Main trust remained 57.
- Inspected the player at a 390 × 844 browser viewport: document width was also 390, with no horizontal overflow. Captured the desktop and narrow layouts.
- Validated the Studio draft: seven scenes, three endings. Exercised JSON export.

Screenshots: `output/playwright/reunion.png`, `free-life.png`, `mobile-life.png`, and `creator-studio.png`. The Studio initially requested a missing favicon (404); an app icon was added. A web native-driver animation warning was observed and corrected by selecting the JavaScript driver on web. The reload after that correction produced no further animation warning.

## Unverified boundaries

No physical-device or native-simulator interaction tests, Xcode/Gradle binary builds, store submission, native accessibility/performance QA, public publishing, cloud synchronization, deployed backend, moderation service, or CI-host execution. Native bundle exports verify bundling only. Dependency installation emitted transitive deprecation notices; no dependency security audit was performed. No production readiness claim is made.
