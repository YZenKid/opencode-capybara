# A1 duplicate inventory

- task_id: `20260716-1535-preset-scope-routing`
- scope: allow-listed files only
- claim level: `confirmed_repo`

## Removed or constrained contradictions

| Path | Finding | Action |
|---|---|---|
| `.opencode/docs/AGENT_ROUTING.md` | Duplicate planner-first lines and contradictory triggered-only/default-first wording | Replaced with one conditional planner rule and explicit read-only prohibition |
| `agents/orchestrator.md` | Plan-first block defaulted uncertainty to planner; finish-first/remediation lacked read-only guard | Replaced block with canonical classifier pointer and read-only stop rule |
| `skills/opencode-orchestrator/SKILL.md` | Core routing repeated planner-first wording and lacked classifier-first step | Added canonical pointer; replaced workflow rule with intent-aware rule |
| `agents/explorer.md` | Read-only lane lacked explicit lite/deep route behavior | Added lane-specific lite/deep behavior and no promotion authority |
| `skills/opencode-explorer/SKILL.md` | Read-only discovery lacked canonical classifier and promotion boundary | Added canonical pointer and route behavior |
| `agents/artifact-planner.md` | Triggered-only rule lacked explicit read-only hard forbid | Added hard forbid and promotion/material trigger requirement |

## Explicit non-claims

- No global duplicate count.
- No edits outside A1 allow-list.
- No runtime performance or model behavior claim.
- `scripts/session-trace-audit.py`, tests, config, and application source were not changed in A1.
