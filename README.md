# opencode-capybara

<p align="center">
  <img src="assets/opencode-capybara-icon.png" alt="opencode-capybara capybara mascot icon" width="128" height="128" />
</p>

Standalone OpenCode multi-agent configuration designed for calm, directed, safety-gated work across coding, docs, UI, browser validation, security scanning, GitHub context, and visual asset workflows.

`opencode-capybara` is a configuration layer for **OpenCode as the primary runtime/platform**, with synchronization support for **OpenChamber as a companion application**. This repo helps organize agents, workflows, validation, and documentation so OpenCode usage stays cleaner and safer.

Internally, this repo uses local Markdown agents, standalone `opencode-*` skills, prompt gates, MCP, and structured documentation under `.opencode/docs/`.

This repository is also positioned as a **local harness engineering system**.

## What's new in the latest release

The `2026.06.23-1` release hardens planning, execution, and policy across the entire agent + skill layer:

- **Plan-first execution** — non-trivial work must go through `@artifact-planner` first; `@orchestrator` executes only `PASS` or `PASS_FOR_SLICE` plans.
- **Execution handoff confidence** — plans now require an execution ownership table, worker-sized atomic tasks, a copy-pasteable handoff prompt, source anatomy breakdown per subsystem, and a reference map per feature.
- **Orchestrator execution tracking** — task-level tracking, worker contract enforcement, finish-first blocker taxonomy, plan compliance checkpoint, and quality-gate remediation loop.
- **Worker contract** — all 19 worker agents now execute scoped tasks and report back to `@orchestrator`; they do not reroute or delegate on their own.
- **Open source reuse policy** — permissive licenses (MIT, BSD, Apache-2.0, ISC, Unlicense, CC0, MPL-2.0) are preferred for reuse/adapt; no auto-replacement without license check.
- **Generator-first UI + anti-AI-slop gates** — shadcn/ui components must be fetched via CLI command (`npx shadcn@latest add <component>`), and generic AI-slop patterns are mechanically blocked.
- **Mandatory stack verification** — no stack recommendations from memory; planners and agents must verify current docs and best practices before converging.
- **Plan artifacts are first-class** — durable plans under `.opencode/plans/`, evidence under `.opencode/evidence/`, and runtime state under `.opencode/state/`.

See the full release notes at https://github.com/YZenKid/opencode-capybara/releases/tag/2026.06.23-1.

## Start here

If you are seeing this repo for the first time, treat it as:

- **not a typical end-user application**, but rather
- **configuration and workflow for OpenCode**, with integration support for OpenChamber when used.

This repo is best suited for:

- users who work with OpenCode regularly, including through OpenChamber,
- people who want stricter agent-based workflows,
- maintainers who need structured docs, quality gates, plans, and evidence.

This repo is **less suitable** if you expect:

- a visual application opened directly in the browser,
- a simple frontend/backend boilerplate,
- setup without API keys or additional tools.

## How work flows

```
User intent
  → @orchestrator
      → @artifact-planner (non-trivial work)
          → plan artifact: .opencode/plans/<task-id>.md
      → @orchestrator executes the plan
          → delegate atomic tasks to worker agents
          → track status per task
          → run validation + @quality-gate
      → final summary
```

- `@orchestrator` + `@artifact-planner` are the brain: routing, planning, coordination.
- Worker agents (`@fixer`, `@frontend`, `@backend`, `@designer`, `@explorer`, etc.) execute scoped tasks and report back.
- `@quality-gate` is the final signoff for non-trivial / risky / UI / security work.
- Plans live in `.opencode/plans/`, evidence in `.opencode/evidence/`, runtime state in `.opencode/state/`.

## Quick start for beginners

```bash
git clone <REPO_URL> ~/.config/opencode
cd ~/.config/opencode
bash scripts/install.sh
```

The installer will run:

- `npm install`
- explicit RTK setup inside the installer
- explicit Caveman setup inside the installer
- `npm run doctor`

This installer **requires network access** and runs **third-party tool setup** explicitly. If you need non-interactive mode, use `bash scripts/install.sh --yes`.

## User documentation

User-facing guides live under [`guide/`](./guide/README.md):

- [`guide/INSTALL.md`](./guide/INSTALL.md)
- [`guide/ENVIRONMENT.md`](./guide/ENVIRONMENT.md)
- [`guide/SCRIPTS.md`](./guide/SCRIPTS.md)
- [`guide/MODEL_ROUTING.md`](./guide/MODEL_ROUTING.md)
- [`guide/TROUBLESHOOTING.md`](./guide/TROUBLESHOOTING.md)

## Internal harness documentation

- `AGENTS.md` is the short map of repo rules
- `.opencode/docs/index.md` is the main entry point for policy and architecture
- `.opencode/state/` is the local runtime state root for durable runs, tasks, mailbox, memory, and worktree metadata

`AGENTS.md` is now a table of contents plus non-negotiable rules.
Detailed policy lives in `.opencode/docs/`.
Plans are first-class artifacts under `.opencode/plans/`.
Runtime execution state lives under `.opencode/state/` and complements plans/evidence rather than replacing them. Phase 2 adds JSON-first CLI entrypoints (`create`, `status`, `continue`, `dispatch`, `execute`); Phase 3 adds persisted dispatcher/executor records for worker launch plans and worktree-backed execution. Phase 4 adds bounded retry loops, mailbox consumption, process polling, and richer live runtime board summaries. Phase 5 adds bounded supervisor ticks/loops with board snapshot persistence. Phase 6 adds per-execution logs plus direct runtime CLI ops (`board`, `poll`, `retry`, `consume`, `supervise`). Phase 7 adds log tailing, retry backoff policy, worker lease locks for multi-consumer safety, and board watch mode that also works against arbitrary git repos using `--project-root`. Phase 8 adds `tail --follow`, lease heartbeat renewal, and deterministic jitter backoff while preserving cross-repo support. Phase 9 adds timeout-bounded live follow, supervisor auto-heartbeat renewal, and lease diagnostics / stale cleanup commands. Phase 10 adds persistent tail sessions, all-worker lease sweeps, and combined board+lease diagnostics reporting. Phase 11 adds diagnostics history snapshots, dashboard export, and tail session garbage collection.

## Project structure at a glance

If you are new here, start with these four areas:

- `README.md` → getting started guide
- `guide/` → repo usage guides
- `AGENTS.md` → short rules
- `.opencode/docs/` → detailed internal documentation

## Why capybara?

Capybara was chosen because it is calm, social, adaptable, and comfortable coexisting with many species—a metaphor for an orchestration layer that brings together many agents, skills, MCP tools, and safety gates without adding noise.

- **Calm orchestration** — `@orchestrator` absorbs multi-agent/multi-tool chaos.
- **Coexistence** — agents, docs, browser tooling, security, GitHub, documents, and image tooling coexist cleanly.
- **Social coordination** — multi-agent collaboration works better when roles are clear.
- **Low drama, high utility** — safety gates and validation matter more than aggressive action.
- **Adaptability** — one setup can move across code, docs, UI, security, and document work.

Capybara is not a symbol of “fast alone”; it is a symbol of “calm together until the result is right.”

## Model routing summary

### What is 9Router in this repo?

In this repo, **9Router** is the primary AI/web/image gateway used by OpenCode to run local agents and network-backed tools.

- `NINEROUTER_URL` → base URL for the 9Router endpoint
- `NINEROUTER_KEY` → API key for authentication with that gateway

If these two values are wrong or empty, agents and MCP tools may fail even if the rest of the configuration looks correct.

Copy `.env.example` to `.env` and set every `OPENCODE_MODEL_*` value before launching OpenCode. Missing env vars resolve to an empty string, which can break OpenCode model routing.

Model routing is currently applied through two paths:

- `opencode.json` uses `OPENCODE_MODEL_DEFAULT` for the default runtime model
- `scripts/sync-agent-models.mjs` synchronizes literal `model:` values in `agents/*.md` with `OPENCODE_MODEL_*` values from `.env`

If you change `OPENCODE_MODEL_*`, run:

```bash
npm run sync:agent-models
```

OpenChamber only supports global defaults such as `defaultModel`, `defaultAgent`, and `zenModel`. This repo sets OpenChamber `defaultAgent` to `orchestrator` and aligns OpenChamber `defaultModel` to `OPENCODE_MODEL_ORCHESTRATOR` so new sessions start as Orchestrator + its intended primary model. The repo also writes a metadata mirror named `opencodeAgentModelMap` into OpenChamber settings so the rest of the OpenCode per-agent routing remains visible even though OpenChamber does not enforce 1:1 per-agent model overrides at runtime.

Image asset generation defaults to `NINEROUTER_IMAGE_MODEL="gemini/gemini-3-pro-image-preview"` through the unified `9router` MCP surface.

Use `npm run compare:openchamber-models` to print the current OpenCode vs OpenChamber model/settings matrix.

### Model routing table

| Env var | Default / recommended model | Used by / capability | Cost guidance |
|---|---|---|---|
| `OPENCODE_MODEL_DEFAULT` | `9router/low` | Top-level default model and general fallback | Keep the baseline lane low-cost for broad default routing. |
| `OPENCODE_MODEL_ORCHESTRATOR` | `9router/medium` | `@orchestrator` primary routing/integration | Use a balanced lane for delegation, coordination, and synthesis. |
| `OPENCODE_MODEL_PLANNER` | `9router/high` | `@artifact-planner`, `modes/plan.md`, `agents-disabled/plan.md` | Keep planning on the strongest lane for higher-accuracy specs and execution handoffs. |
| `OPENCODE_MODEL_DESIGN` | `9router/high` | `@designer` | Keep substantial UI/design reasoning, motion, and accessibility work on the high lane. |
| `OPENCODE_MODEL_VISUAL_ASSET` | `9router/medium` | `@visual-asset-generator` | Keep visual asset manifest prep and style-equivalent fallback generation routing on medium while leaving designer on high. |
| `OPENCODE_MODEL_REVIEW` | `9router/medium` | `@oracle`, `@council` | Keep advisory/review reasoning on a balanced lane without degrading high-confidence review paths. |
| `OPENCODE_MODEL_QUALITY_GATE` | `9router/low` | `@quality-gate` | Final conformance gate stays cheap and explicit without forcing `@oracle`/`@council` down. |
| `OPENCODE_MODEL_ADVISORY` | `9router/medium` | `@architect` | Use a balanced lane for advisory and architecture guidance. |
| `OPENCODE_MODEL_EXECUTION` | `9router/low` | `@fixer` | Keep bounded implementation and testing on lower-cost lane. |
| `OPENCODE_MODEL_DISCOVERY` | `9router/low` | `@explorer` | Local discovery and read-only pattern analysis stay on the cheaper lane. |
| `OPENCODE_MODEL_DOCUMENTS` | `9router/low` | Reserved compatibility lane (document-centric work now routes via `@librarian`) | Keep for env compatibility on the cheaper lane. |
| `OPENCODE_MODEL_IMPROVEMENT` | `9router/fast` | Compatibility alias (agent mapping now uses `OPENCODE_MODEL_FAST`) | Kept for env compatibility; recommended default aligned to fast. |
| `OPENCODE_MODEL_FAST` | `9router/fast` | `@librarian`, `@skill-improver` | Docs/API lookup, summarization, and bounded prompt refinements are latency-sensitive and low-risk; use the fast lane. |

## Domain specialist and workflow summary

Domain helper/advisory lanes are conditional.
Tiny UI polish still goes to `@designer`, and isolated bugfixes still go to `@fixer`.

Current operating model:

- `@artifact-planner` is the required planning lane for non-trivial work.
- `@orchestrator` executes only from a plan (`PASS` / `PASS_FOR_SLICE`) and tracks progress per task.
- Worker agents execute only bounded tasks and report back; they do not reroute or delegate on their own.
- `@quality-gate` returns statuses such as `PASS`, `PASS_WITH_RISKS`, `NEEDS_FIX`, and `BLOCKED`, and its remediation items are executed finish-first before final claim.
- `@skill-improver` is used for non-trivial follow-up, repeated failures, policy gaps, or explicit requests.
- No blind external updates.
- Redundant `build` and `general` local agents have been removed.

UI / design policy:

- `@designer` owns substantial UI direction, motion, accessibility, and anti-slop review.
- `@frontend` implements web UI when design is clear.
- shadcn/ui follows generator-first rules: use `npx shadcn@latest add <component>` when the component exists in the registry.
- Generic AI-slop UI patterns (fake metrics, card spam, gradient-hero defaults, placeholder imagery, debug copy) are blocked by planner/designer/quality-gate rules.

## Important scripts

- `npm run setup:tools`
- `npm run doctor`
- `npm run post:update`
- `npm run sync:agent-models`
- `npm run test:prompt-gates`
- `npm run test:runtime-foundation`
- `npm run test:runtime-cli`
- `npm run test:runtime-ops`

See the full explanation in [`guide/SCRIPTS.md`](./guide/SCRIPTS.md).

## RTK and Caveman in brief

- if automatic setup is unavailable, the script will provide clear **manual fallback** commands
- this repo enforces a **no unsafe lifecycle install hooks policy**
- **OpenCode command rewriting** remains **opt-in**
- for **token compression / context packing**, use **RTK and Caveman together**

## Validation summary

Most common validation:

```bash
npm run test:prompt-gates
npm run check:harness
```

Plan quality checks:

```bash
npm run check:plans          # verify plan depth, sections, and handoff contract
npm run check:agents
npm run check:skills
npm run check:docs
npm run check:evidence
```

Runtime harness checks:

```bash
npm run test:runtime-foundation
npm run test:runtime-cli
npm run test:runtime-ops
npm run test:runtime-supervisor
npm run test:runtime-cli-ops
npm run test:runtime-phase7
```

## Validation and auto-commit summary

Auto-commit defaults to ON for local commits only; never push automatically.

Rules:

- Run only after a **plan-bound non-trivial task is complete**, **validation passes**, and `@quality-gate` returns `PASS` or `PASS_WITH_RISKS` without a blocker.
- Review `git status`/`git diff`, then **stage only relevant files**.
- Auto-generated commit messages use a **short subject plus bullet-point body**.
- Never stage `.env`, secrets, tokens, credentials, unrelated untracked files, or generated/vendor files unless the plan/user explicitly approves them.
- Never use `--no-verify`, `--no-gpg-sign`, `amend`, force push, or destructive git commands.
- If scope or staging is unclear, stop and ask.

## Internal workflow summary

- `@artifact-planner` writes durable `.opencode/plans/<task-id>.md` artifacts before implementation.
- `@orchestrator` loads the plan, tracks execution, enforces worker contract, and runs quality-gate remediation finish-first.
- Worker agents receive scoped tasks and report back to `@orchestrator`.
- `@quality-gate` is the final signoff for non-trivial/risky/UI/security work.
- `@skill-improver` handles non-trivial follow-up, repeated failures, policy gaps, or explicit requests.
- Redundant `build` and `general` local agents have been removed.

Full details remain in `.opencode/docs/`, the related agent/skill files, and the latest release notes at https://github.com/YZenKid/opencode-capybara/releases/tag/2026.06.23-1.

## References

- OpenCode — the main platform and runtime targeted by this repo configuration:
  - https://github.com/sst/opencode
- Slim preset ancestor — the preset/ancestor that served as the starting point before this repo evolved into `opencode-capybara`:
  - https://github.com/YZenKid/oh-my-opencode-slim-preset
- oh-my-pi (`omp`) — reference for deterministic edit, LSP-first workflow, debugger/runtime primitives, and eval-driven harness design that informed the OMP adoption roadmap:
  - https://github.com/can1357/oh-my-pi
- RTK AI — the primary toolchain for token compression / context packing, used together with Caveman according to the repo workflow:
  - https://github.com/rtk-ai/rtk
- Caveman — the companion workflow used together with RTK, not a separate alternative path:
  - https://github.com/JuliusBrussee/caveman
- GPT Harness Engineering — conceptual reference for evals, replayability, evidence, and harness hardening:
  - https://openai.com/index/harness-engineering/
