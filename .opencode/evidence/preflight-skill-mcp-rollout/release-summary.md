# Release Summary: Pre-flight Skill & MCP Discovery Rollout to All Agents/Skills

## User request

> Pastikan Pre-flight Skill & MCP Discovery di gunakan disemua agent lainnya juga.

Context from prior turn: the user reviewed a confusing OpenCode session (`opncd.ai/share/fppnDa05`) where the agent:
- solved issues in a meandering, unclear way,
- had skills available but did not appear to use them,
- had good MCP tools available but did not use them,
- confused the user because answers were not sharp / on-point.

The first slice fixed only `@orchestrator` + `opencode-orchestrator` skill + a transcript audit helper. This slice rolls the same contract out to the whole active library.

## What changed

### 1) Class-wide rollout: all 22 agents
Inserted `## Pre-flight Skill & MCP Discovery` into every file under `agents/*.md`.

New contract in every agent:
- before the first substantial answer / diagnosis / plan / implementation step on non-trivial work,
- load the lane's primary skill first,
- explicitly state `Skill I'm using`, `MCPs I'm using`, `What I'm checking first`,
- use or explicitly skip obvious MCPs (`sequential-thinking`, `context7`, `grep_app`, `github`, `semgrep`, `playwright`),
- loaded-but-unused skill is a process defect,
- final summary must name one concrete thing the skill changed about execution.

Files touched (22):
- agents/architect.md
- agents/artifact-planner.md
- agents/backend.md
- agents/council.md
- agents/design-system-engineer.md
- agents/designer.md
- agents/devops.md
- agents/explorer.md
- agents/fixer.md
- agents/frontend.md
- agents/fullstack.md
- agents/librarian.md
- agents/mobile.md
- agents/oracle.md
- agents/orchestrator.md
- agents/plan-reviewer.md
- agents/project-manager.md
- agents/quality-gate.md
- agents/skill-improver.md
- agents/system-analyst.md
- agents/visual-asset-generator.md
- agents/visual-context-extractor.md

### 2) Class-wide rollout: all 22 skills
Inserted the same `## Pre-flight Skill & MCP Discovery` contract into every `skills/opencode-*/SKILL.md`.

Skill-side contract is shorter and lane-focused:
- name the skill explicitly,
- decide MCP applicability explicitly,
- obvious MCP requires use or explicit skip reason,
- final summary must name one concrete thing the skill changed.

Files touched (22):
- skills/opencode-architect/SKILL.md
- skills/opencode-artifact-planner/SKILL.md
- skills/opencode-backend/SKILL.md
- skills/opencode-council/SKILL.md
- skills/opencode-design-system-engineer/SKILL.md
- skills/opencode-designer/SKILL.md
- skills/opencode-devops/SKILL.md
- skills/opencode-explorer/SKILL.md
- skills/opencode-fixer/SKILL.md
- skills/opencode-frontend/SKILL.md
- skills/opencode-fullstack/SKILL.md
- skills/opencode-librarian/SKILL.md
- skills/opencode-mobile/SKILL.md
- skills/opencode-oracle/SKILL.md
- skills/opencode-orchestrator/SKILL.md
- skills/opencode-plan-reviewer/SKILL.md
- skills/opencode-project-manager/SKILL.md
- skills/opencode-quality-gate/SKILL.md
- skills/opencode-skill-improver/SKILL.md
- skills/opencode-system-analyst/SKILL.md
- skills/opencode-visual-asset-generator/SKILL.md
- skills/opencode-visual-context-extractor/SKILL.md

### 3) Mechanical helper: session-trace audit
Added:
- `scripts/session-trace-audit.py`
- `scripts/tests/session-trace-audit.test.py`
- package.json scripts:
  - `check:session-trace`
  - `test:session-trace`

This helper is an advisory heuristic audit that flags the exact failure mode the user described:
- missing skill/MCP orientation,
- loaded-but-unused skill,
- obvious MCP silently skipped,
- missing `sequential-thinking` in multi-issue debugging,
- missing `context7` in version-sensitive framework/API/library work.

It ships with a fixture modeled after the `fppnDa05` failure pattern:
- broken transcript -> WARN
- fixed transcript -> PASS

### 4) Canonical doc reference
Updated `.opencode/docs/PROMPT_GATES.md` to list the new checker:
- `npm run check:session-trace <transcript>` -> `scripts/session-trace-audit.py`

## Verification

### Idempotent rollout
`python3 scripts/_rollout_preflight.py` first run:
- agent files scanned: 22
- agent files changed: 22
- skill files scanned: 22
- skill files changed: 22

Second run:
- agent files changed: 0
- skill files changed: 0

### Tests
- `python3 scripts/tests/session-trace-audit.test.py` -> **6/6 OK**
- `python3 scripts/tests/rules-harmonizer.test.py` -> **16/16 OK**
- `npm run test:verify-claim` -> **22/22 OK**
- `npm run check:agents` -> **PASS**
- `npm run check:skills` -> **PASS**

### Invariants preserved
- `/init-harness` reference consistency remains aligned:
  - `/init-harness`: 29
  - `single entrypoint`: 29
  - `commands/init-harness.md`: 29

## What did NOT change
- `npm run test:prompt-gates` still fails with **6 pre-existing issues** on this repo baseline.
  - Important: the baseline still failed after stashing this rollout, so these are **not introduced by this change**.
  - Current failures are in existing designer/frontend/orchestrator prompt-gate expectations and were already present before this slice.

## Behavioral impact

Before:
- only `@orchestrator` explicitly knew it had to do skill/MCP orientation.
- any specialist lane (`@backend`, `@fixer`, `@frontend`, etc.) could still answer or implement without making the skill/MCP choice visible.

After:
- every active lane and every active `opencode-*` skill now carries the same pre-flight contract.
- the user can expect the same answer shape across lanes:
  - `Skill I'm using: ...`
  - `MCPs I'm using: ...`
  - `What I'm checking first: ...`
- silent skill loading and silent obvious-MCP skip are now explicit process defects across the whole library, not just in orchestrator.

## Follow-ups (not done in this slice)
- Turn the advisory session-trace audit into a hard runtime blocker once transcript hooks are first-class.
- Add semantic transcript-eval fixtures to the harness (not just unit tests) so session-level failures like `fppnDa05` become regression tests in `scripts/evals/`.
- Fix the 6 baseline `test:prompt-gates` failures separately (they predate this rollout).
- Remove helper script `scripts/_rollout_preflight.py` after the rollout lands if the repo owner prefers not to keep one-off migration helpers.

## Why this matters
The user's ask was not "make orchestrator better". It was: **make this behavior consistent in every lane**.

This slice converts `Pre-flight Skill & MCP Discovery` from a single-orchestrator policy into a **library-wide policy**.

That is the minimum needed so future sessions do not regress into:
- unclear solve path,
- hidden skill loading,
- silently skipped MCPs,
- user confusion about what the agent is actually doing.

ponytail: This slice enforces the contract textually across all lanes. The next upgrade is to make transcript-level activation checking part of the release/harness path once the transcript schema is stable.
