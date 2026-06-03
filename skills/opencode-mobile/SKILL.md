---
name: opencode-mobile
description: Senior stack-agnostic mobile implementation playbook for native or hybrid apps, permissions, navigation, offline, push, camera, deep links, store constraints, and device validation.
---

# OpenCode Mobile Skill

Use for bounded native or hybrid mobile implementation. Detect actual project stack from repo evidence before edits; local project conventions win; make no Flutter, React Native, Expo, or native default assumptions.

## Trigger / skip
- Trigger: Flutter/RN screens, navigation, state, platform config, permissions, offline sync, push, camera, deep links, build/test/device validation.
- Skip: product flow ambiguity → `@system-analyst`; app architecture/platform strategy → `@architect`; backend/API/data contract change → `@backend`/`@fullstack`; privacy/biometric/final permission signoff → `@quality-gate`.

## Stack detection
- Flutter: `pubspec.yaml`, `lib/`, `android/`, `ios/`, `integration_test/`, `flutter_test`, state libs (`bloc`, `riverpod`, `provider`, `get_it`).
- React Native/Expo: `app.json`, `expo`, `metro.config.*`, `ios/`, `android/`, React Navigation/Expo Router.
- Native signals: iOS `*.xcodeproj`/`*.xcworkspace`/Swift/Objective-C, Android `build.gradle*`/Kotlin/Java, Kotlin Multiplatform, Capacitor/Ionic, or other repo-specific setup.
- Identify target platforms, min SDK/iOS version, app flavors, env config, CI build path, native modules, permissions, and store constraints.

## Responsibilities
- Reuse navigation, state, theming, localization, platform services, build flavors, test patterns, and error handling.
- Keep native changes minimal and explicit; document permission/store/build impact.
- Preserve offline, lifecycle, back navigation, deep-link, and accessibility behavior.
- Validate on safe simulator/emulator/unit commands when available; record device limits.

## Senior heuristics / checklist
- UX states: loading, empty, error, retry, offline, permission denied, background/foreground, interrupted flows.
- Platform: iOS/Android differences, safe areas, keyboard, back button, orientation, text scaling, screen readers.
- Permissions: request at point of need, graceful denial, rationale copy, Info.plist/AndroidManifest parity.
- Data: cache invalidation, retry/backoff, idempotency, conflict handling, network timeout.
- Performance: avoid jank on main isolate/JS thread, excessive rebuilds/renders, large images, unbounded lists.
- Releases: app identifiers, signing, build numbers, store review sensitive APIs.

## Workflow
1. Detect stack, platforms, and build/test commands.
2. Inspect navigation, state, config, permissions, native modules, and existing tests.
3. Confirm user flow, API contract, offline/lifecycle needs, and platform impact.
4. Red: add widget/unit/integration test or reproduce bug where feasible.
5. Green: implement smallest app/native/config change.
6. Refactor: align with project architecture and platform conventions.
7. Validate with focused tests/build/analyzer/simulator checks.

## Validation
- Run detected-stack validation from repo scripts/docs; examples include Flutter `flutter analyze`/`flutter test`, RN/Expo `test`/`lint`/`typecheck`, native iOS/Android build/test commands when configured.
- Device validation: state simulator/emulator/device used; if unavailable, document limitation and remaining risk.

## Escalation
- Route `@architect` for new native dependency strategy, offline architecture, push/deep-link platform design, or store-release strategy.
- Route `@quality-gate` for biometric, privacy, permissions, production release, or security-sensitive changes.

## Output contract
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence`. Include platforms affected, validation commands/results, and device/simulator limits.

## Domain references
- `.opencode/docs/SENIOR_SKILLS_REFERENCES.md`.
- Relevant inspiration: `vercel-labs/agent-skills/vercel-react-native-skills` for RN/Expo only when detected stack matches.
- For Flutter/native, prefer project-local and official docs; no external install.
