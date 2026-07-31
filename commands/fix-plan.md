---
description: Apply scoped mechanical plan-contract repairs
agent: orchestrator
model: 9router/high
---

Run `/check-plan` first. Apply only deterministic, evidence-backed mechanical repairs to named plan under `.opencode/plans/`. Current planning owner is `@artifact-planner`; removed agent IDs are invalid.

Never edit source, provider config, `.env`, dependencies, runtime implementation, or unrelated files. Preserve plan scope and existing content. Re-run read-only validators after repair and report changed plan lines, remaining failures, and evidence paths.

Arguments:

```text
$ARGUMENTS
```
