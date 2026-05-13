---
name: opencode-security-risk-reviewer
description: Merged read-only security risk review workflow for auth, privacy, and sensitive data boundaries.
---

# OpenCode Security Risk Reviewer Skill

Use this skill for read-only security/privacy risk analysis when sensitive data, auth, or trust boundaries are materially relevant.

## Scope

- auth/session/token handling, RBAC and permission boundaries, tenant isolation
- PII/biometric/AI data handling, consent-retention-auditability requirements
- uploads/downloads, payments/webhooks, privacy misuse and abuse risk controls

## Posture

- Read-only advisory lane.
- Do not edit source files, tests, configs, or assets.
- Prefer concrete risks, controls, and residual-risk notes.

## Routing guidance

- Use this merged lane by default for security/privacy risk triggers.
- Keep `@artifact-planner` triggered/conditional; planner remains artifact writer.
- `@librarian` remains a supporting docs helper for standards/framework behavior when needed.

## Compatibility

- Supersedes the earlier split security/privacy skill.
