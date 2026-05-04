# Skill: opencode-security-privacy-reviewer

Read-only security and privacy review workflow. Use this when PII, auth/session, RBAC, tenant isolation, payments/webhooks, uploads/downloads, AI data, biometric/face/photo data, consent, retention, or auditability materially affects the work.

## Trigger / skip

- Trigger for security-sensitive changes, privacy-sensitive product features, AI data handling, file uploads, payments, webhooks, auth, authorization, tenant isolation, export/delete, and biometric/face matching.
- Skip for trivial CSS, copy-only edits, docs without policy impact, or local-only throwaway prototypes unless a risk trigger applies.
- Do not read secrets or `.env` files. Do not run destructive, exploitative, or external attack actions.

## Workflow

1. Identify assets/data classes: public, internal, PII, sensitive PII, biometric, financial, secrets.
2. Review access boundaries: auth, RBAC, tenant isolation, object ownership, server-side checks, audit logs.
3. Review data lifecycle: collection, consent, retention, deletion, export, backups, third-party sharing.
4. Review common app risks: injection, IDOR, CSRF/session, upload abuse, signed URL leakage, webhook verification, rate limits.
5. Review AI risks when relevant: prompt injection, tool abuse, training/retention, data exfiltration, hallucinated actions.
6. Classify findings and required mitigations.

## Output contract

- Risk summary with severity: `critical`, `high`, `medium`, `low`, `note`.
- Required mitigations and tests.
- Privacy/consent/retention checklist.
- Security acceptance criteria.
- Readiness status: `pass`, `pass-with-risks`, `needs-fix`, or `blocked`.

## Quality bar

- Server-side enforcement over UI-only controls.
- Least privilege and explicit consent.
- No production claim when sensitive data flow is untested.
- Escalate high-stakes tradeoffs to `@oracle` and final evidence to `@quality-gate`.
