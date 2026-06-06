# Greenfield Starter

Canonical starter contract for `Greenfield App Accelerator` work.

Use this doc for new apps, blank repos, MVPs, SaaS/product builds, and major product revamps before first implementation slice.

## Starter matrix

Classify each material decision with one state: `answered`, `deferred`, `slice-safe`, or `blocked`.

| Area | Question | State | Evidence / note |
|---|---|---|---|
| Product | Target user, pain, success metric | `answered` / `deferred` / `slice-safe` / `blocked` | Source or assumption |
| UX | First user journey and core screens | `answered` / `deferred` / `slice-safe` / `blocked` | Reference, design doc, or first-principles note |
| Data | Entities and ownership boundaries | `answered` / `deferred` / `slice-safe` / `blocked` | Schema/contracts note |
| Auth/RBAC | Identity, roles, access rules | `answered` / `deferred` / `slice-safe` / `blocked` | Security basis |
| Privacy | PII, retention, consent, regional constraints | `answered` / `deferred` / `slice-safe` / `blocked` | Privacy basis |
| Payments/Billing | Paid flows, entitlements, invoices | `answered` / `deferred` / `slice-safe` / `blocked` | Billing basis |
| Platform | Hosting, runtime, storage, queues, jobs | `answered` / `deferred` / `slice-safe` / `blocked` | Ops basis |
| Release | Deploy path, observability, rollback | `answered` / `deferred` / `slice-safe` / `blocked` | Release basis |
| UI system | Visual direction, components, accessibility | `answered` / `deferred` / `slice-safe` / `blocked` | Design basis |
| Tests | First-slice test strategy | `answered` / `deferred` / `slice-safe` / `blocked` | Validation basis |

State meanings:
- `answered`: decision is made with enough evidence for implementation.
- `deferred`: decision remains open and first slice intentionally avoids depending on it.
- `slice-safe`: provisional decision is reversible and does not lock material future choices.
- `blocked`: no safe implementation slice exists until decision/access/evidence is resolved.

## Security/privacy blocking rule

Any first slice that collects, stores, transmits, displays, exports, or grants access to PII, credentials, payment data, tenant data, regulated data, or user-generated private content is `blocked` until security/privacy ownership, access rules, retention, and validation expectations are `answered`.

`slice-safe` cannot be used to bypass security/privacy decisions when the slice touches sensitive data or permissions.

## First-slice template

```md
# First Slice

## Goal
- User-visible outcome:
- Non-goals:

## Readiness
- Plan Quality Gate: `PASS` / `PASS_FOR_SLICE` / `NEEDS_DEPTH` / `BLOCKED`
- Starter matrix summary:
- Security/privacy status:

## Options considered
1. Option:
   - Pros:
   - Cons:
2. Option:
   - Pros:
   - Cons:
3. Option:
   - Pros:
   - Cons:

## Chosen slice rationale
- Why this slice first:
- Why unresolved decisions remain safe:
- Reversibility notes:

## Mapping
- User journey:
- Data model:
- API/contracts:
- UI screens:
- Tests:

## Validation
- Commands:
- Manual/browser checks:
- Evidence path: `.opencode/evidence/<task-id>/`

## Claim level
- `prototype`, `draft`, `MVP slice complete`, or whole-app complete only when true.
```

## First-slice claim rules

- Use `PASS` only when material decisions for the planned implementation scope are answered.
- Use `PASS_FOR_SLICE` when whole-product decisions remain open, but the first slice is explicit, reversible, validated, and does not lock those decisions.
- `PASS_FOR_SLICE` permits only first-slice implementation and claim. It does not permit whole-app completion claims.
- Claim `MVP slice complete` only after slice validation passes and evidence is retained under `.opencode/evidence/<task-id>/`.
- Claim whole-app complete only when all product, data, auth/RBAC, privacy, billing, platform, UI, release, and validation requirements for the whole app are answered and verified.

## Deferred decisions

Deferred decisions must include:
- owner or lane for follow-up;
- trigger that forces decision;
- why current slice does not lock or depend on it;
- evidence needed before it becomes implementation-ready.
