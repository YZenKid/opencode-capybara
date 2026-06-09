# Security

## Non-negotiables
- Never commit `.env`, secrets, tokens, or credentials.
- Never widen permissions casually for read-only reviewer agents.
- Never rely on hidden lifecycle install hooks.
- Never bypass validation or quality gating for risky changes.

## Review triggers
Use `@architect` for security/privacy architecture decisions and `@quality-gate` for final security/privacy signoff when the work touches:
- auth,
- PII,
- session/token handling,
- tenant isolation,
- uploads/downloads,
- payments/webhooks,
- biometric/photo/AI data,
- consent or retention,
- RBAC or permission boundaries.

## Creativity Fast Path hard-rail note
`Creativity Fast Path` is never a security bypass. Even for draft/prototype/exploration work, fast-path routing must exit immediately and return to normal guarded flow when the request touches:
- auth, session/token handling, tenant isolation, RBAC, or permission widening;
- PII, consent/retention, biometric/photo/AI data privacy;
- payments/webhooks, uploads/downloads, or credential/secrets handling;
- destructive operations, deploy, release, production mutation, or rollback-sensitive work.

Prototype wording such as “cepat”, “draft”, atau “sekadar contoh” does not relax these boundaries.

## Harness-specific safeguards
- `doctor` should warn on local `.env` presence.
- prompt gates should catch wording drift on secrets policy.
- evidence summaries should mention security limitations if relevant.
