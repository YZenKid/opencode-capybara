---
name: opencode-platform-architect
description: Merged read-only platform architecture workflow for release/runtime and mobile-platform constraints.
---

# OpenCode Platform Architect Skill

Use this skill for read-only platform architecture analysis when runtime, release, or mobile constraints are materially relevant.

## Scope

- CI/CD, environment readiness, deployment and migration strategy, monitoring, rollback, production operations
- Mobile/hybrid/PWA/runtime constraints: offline behavior, push, deep links, camera/QR, permissions, app-store readiness

## Posture

- Read-only advisory lane.
- Do not edit source files, tests, configs, or assets.
- Prefer concise, risk-ranked recommendations with operational checks.

## Routing guidance

- Use this merged lane by default for platform/runtime risk triggers.
- Keep `@artifact-planner` triggered/conditional; planner remains artifact writer.
- `@librarian` remains a supporting docs helper when framework/runtime behavior must be verified.

## Compatibility

- Supersedes the earlier split platform skills.
