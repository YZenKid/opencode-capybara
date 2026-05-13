---
name: opencode-product-systems-architect
description: Merged read-only product systems architecture workflow for PRD-to-production and SaaS boundary decisions.
---

# OpenCode Product Systems Architect Skill

Use this skill for read-only product-system analysis when product and SaaS boundaries are materially relevant.

## Scope

- PRD/MVP slicing, epics, user flows, acceptance criteria, product ambiguity resolution
- SaaS system boundaries: tenancy, workspace/team model, RBAC, billing/subscription, usage limits, audit surfaces

## Posture

- Read-only advisory lane.
- Do not edit source files, tests, configs, or assets.
- Prefer concise evidence-backed recommendations and explicit tradeoffs.

## Routing guidance

- Use this merged lane by default for product/SaaS risk triggers.
- Keep `@artifact-planner` triggered/conditional; planner remains artifact writer.
- `@librarian` remains a supporting docs helper when version-sensitive product/platform behavior requires verification.

## Compatibility

- Supersedes the earlier split product/SaaS skills.
