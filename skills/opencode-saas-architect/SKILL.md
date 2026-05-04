# Skill: opencode-saas-architect

Read-only SaaS architecture workflow for multi-tenant production apps. Use this only when tenancy, workspaces, RBAC, billing, subscription limits, audit, admin, onboarding, or SaaS data lifecycle decisions are material.

## Trigger / skip

- Trigger for SaaS, B2B, multi-workspace, team roles, subscription tiers, usage metering, invoices, organization settings, tenant isolation, or admin surfaces.
- Skip for single-user apps, static sites, tiny UI polish, isolated bugfixes, or features with no SaaS boundary impact.
- If a tradeoff is high-stakes or cross-system, recommend `@oracle` review.

## Workflow

1. Define tenancy model: single-tenant, multi-tenant shared schema, schema-per-tenant, or hybrid.
2. Define workspace/org model, membership lifecycle, invitations, roles, and permission boundaries.
3. Define billing/subscription model, feature gates, usage limits, trials, grace periods, and upgrade/downgrade behavior.
4. Define audit logs, admin surfaces, data export/deletion, and tenant lifecycle.
5. Identify risks: cross-tenant leakage, inconsistent roles, billing bypass, migration complexity, operational burden.

## Output contract

- Recommended tenancy/RBAC/billing model.
- Key entities and boundaries.
- Permission matrix outline.
- SaaS lifecycle flows.
- Risks, assumptions, and migration notes.
- Validation checklist for implementation and tests.

## Quality bar

- Prefer the simplest tenancy model that protects data correctly.
- Do not design billing or permissions as UI-only checks.
- Require server-side enforcement and auditability for sensitive actions.
- Readiness level: `ready-for-blueprint`, `needs-saas-decisions`, or `blocked`.
