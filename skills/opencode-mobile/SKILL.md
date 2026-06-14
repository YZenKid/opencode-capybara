---
name: opencode-mobile
description: Senior stack-agnostic mobile implementation playbook for native or hybrid apps, permissions, navigation, offline, push, camera, deep links, store constraints, and device validation.
---

# OpenCode Mobile Skill

Use for bounded native or hybrid mobile implementation. Detect actual project stack from repo evidence before edits; local project conventions win; make no Flutter, React Native, Expo, or native default assumptions.

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

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
- Before framework-managed mobile edits, read `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when present.
- Greenfield App Accelerator: build the mobile part of a ready first slice without locking unresolved platform/store/privacy decisions.
- Maintenance Stability Mode: preserve existing mobile UX/native behavior and fix the smallest reproducible issue.
- Prefer official generators and framework commands first for new mobile artifacts in existing apps too when tooling is detected and permitted.
- Manual framework artifact creation is allowed only when the command/tool is unavailable or not permitted, the command failed with evidence, the project intentionally avoids the generator, the task customizes existing generated files, or the user explicitly asks for manual edits. Record the attempted or skipped command and reason in evidence.
- If framework/library command behavior is version-sensitive and the project docs do not already settle it, route to `@librarian` for official docs/context7 before coding.
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
1. Read `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when present.
2. Detect stack, platforms, and build/test commands.
3. Inspect navigation, state, config, permissions, native modules, and existing tests.
4. Confirm user flow, API contract, offline/lifecycle needs, and platform impact.
5. For new framework-managed mobile artifacts, use the documented official generator/CLI path first; if manual fallback is used, record the exact command/tool and reason.
6. TDD where relevant: Red by adding widget/unit/integration test or reproducing bug where feasible.
7. Green: implement smallest app/native/config change.
8. Refactor: align with project architecture and platform conventions.
9. Validate with focused tests/build/analyzer/simulator checks.

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
## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
