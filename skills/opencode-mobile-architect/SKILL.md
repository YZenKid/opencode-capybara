# Skill: opencode-mobile-architect

Read-only mobile and hybrid app architecture workflow. Use this only when native mobile, React Native/Expo, Flutter, Capacitor, PWA, offline behavior, push, deep links, camera/QR, device permissions, app-store readiness, or mobile performance materially affects the task.

## Trigger / skip

- Trigger for mobile/hybrid app plans, native device APIs, offline sync, camera/QR scanner, push notifications, deep links, app-store constraints, mobile release, or platform-specific performance.
- Skip for responsive web-only layout polish that `@designer` can handle, tiny UI fixes, ordinary web bugfixes, or non-mobile backend work.
- For visual direction, coordinate with `@designer`; do not replace designer signoff.

## Workflow

1. Identify platform target: responsive web, PWA, Capacitor, Expo/React Native, bare React Native, Flutter, or native.
2. Review device requirements: camera, QR, files/photos, push, biometrics, location, offline, background tasks, deep links.
3. Define state/sync model: offline queue, conflict resolution, cache, retry, auth/session persistence.
4. Define performance constraints: startup, bundle size, image handling, list virtualization, network conditions.
5. Define mobile validation: simulator/device flows, permissions, reduced motion, accessibility, app-store constraints.
6. Identify platform-specific risks and handoff to designer/fixer/release/security as needed.

## Output contract

- Platform recommendation and rationale.
- Mobile capability checklist.
- Data sync/offline and permission strategy.
- Validation matrix by platform/device.
- Risks and implementation handoff.
- Readiness status: `ready-for-blueprint`, `needs-mobile-decisions`, or `blocked`.

## Quality bar

- Do not use web-only libraries for native mobile unless target is webview/PWA.
- Validate important mobile behavior on simulator/device when runnable.
- Keep mobile UX fast, accessible, and resilient to poor networks.
