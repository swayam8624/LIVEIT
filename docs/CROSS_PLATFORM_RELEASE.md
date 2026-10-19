# LIVEIT cross-platform preview and release playbook

Last reviewed: 17 October 2026. This is a preparation document: **no production storefront account, public website, native device install or store submission has been completed by these changes**.

## Shared app architecture

The same framework-independent TypeScript life/narrative/consequence engine drives the Expo/React Native web, iOS and Android app. Creator Studio is a separate Next.js authoring application. The game itself is ad-free, and choices, life progression, imported stories and basic play are not gated by purchases, tickets, energy or real-time waits.

## Web preview (no production deployment yet)

```sh
npm ci
npm run check
npm run build:player
# Upload apps/player/dist/ to a static host (e.g. Cloudflare Pages).
```

The repository's `Package LIVEIT web preview` GitHub workflow also stores the static Expo web export as a downloadable Actions artifact. This is a build artifact, **not a hosted URL**. Static hosting requires a production domain, caching/HTTPS review, accessible media paths, privacy documents, analytics decision and a monitored error-reporting plan.

## Android physical-device internal APK

Install Expo/EAS CLI through your normal package management; then inside `apps/player`:

```sh
npx eas-cli login
npx eas-cli init
npx eas-cli build --platform android --profile preview
```

This uses the `preview` build profile in `apps/player/eas.json`: internal distribution with Android APK. Device signing keys are provisioned through EAS and must be protected. Verify from a **physical Android phone**: cold startup, all four tabs, story choices, local saves, no-network mode, UI scale/font settings, and suspension/resume.

## iOS simulator and real iPhone

```sh
cd apps/player
npx eas-cli build --platform ios --profile ios_simulator
# For ad hoc physical-device internal distribution:
npx eas-cli device:create
npx eas-cli build --platform ios --profile preview
```

Simulator builds are different from signed iPhone device builds. Ad hoc builds need Apple Developer provisioning and registered device IDs; iOS signing is **not** verified by the current Expo Hermes JavaScript export. Verify a genuine device as well as a simulator before public release.

## Store builds (DO NOT execute until release is approved)

```sh
cd apps/player
npx eas-cli build --platform android --profile production
npx eas-cli build --platform ios --profile production
# Later, with authenticated developer accounts and explicit consent:
npx eas-cli submit --platform android --profile production
npx eas-cli submit --platform ios --profile production
```

Production credentials, app identity, ownership of `studio.livinguniverse.player`, signing, export compliance and team permissions need human verification. Submitting requires an explicit decision to make a public or store-facilitated testing release. **No automation in this repository silently submits an app.**

## Required release gates

- Finish final app icons, splash/loading visuals, high-resolution scene plates, portrait/character rig improvements and style-consistency checks; current café/portrait are **prototype-resolution** in GitHub until the separately prepared high-resolution original concept pack is installed.
- Adopt a tested backup/save migration strategy; no local save data is ever promised safe from uninstall, device failure or storage clearing.
- Test cold install, upgrade, reinstall, permissions, Android back behavior, iPhone safe areas, offline startup, airplane mode, storage-full failures, low-memory devices, screen readers, reduced-motion preferences and font scaling.
- Finalize privacy policy and in-app privacy settings. Any future accounts, cloud sync, moderation logs or user-generated content processing change the personal-data map and require updated notices.
- Obtain legal review of artwork, AI-generation licenses, creator-upload rights, user-generated content moderation, reporting, takedowns/appeals and age classifications.
- Confirm app-store policies for UGC creation, payments, in-app purchases and family eligibility; no real-money paywalls, loot boxes or advertising SDKs should be introduced to normal progression.
- Produce approved screenshots from tested physical devices. Automated desktop/mobile _browser_ screenshots do not count as native-device tests.
- Confirm public hosting and service uptime monitoring before inviting outside creators.

## EAS configuration references

- https://docs.expo.dev/build/eas-json/
- https://docs.expo.dev/build/internal-distribution/
- https://docs.expo.dev/eas/cli/

Last verified by the pipeline: web/Studio production export, iOS/Android **Hermes bundles only**, and Playwright browser gameplay. Native binary installation remains a future human-assisted checkpoint.
