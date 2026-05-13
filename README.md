# opencode-capybara

<p align="center">
  <img src="assets/opencode-capybara-icon.png" alt="opencode-capybara capybara mascot icon" width="128" height="128" />
</p>

Standalone OpenCode multi-agent configuration designed for calm, directed, safety-gated work across coding, docs, UI, browser validation, security scanning, GitHub context, and visual asset workflows.

`opencode-capybara` is a configuration layer for **OpenCode as the primary runtime/platform**, with synchronization support for **OpenChamber as a companion application**. This repo helps organize agents, workflows, validation, and documentation so OpenCode usage stays cleaner and safer.

Internally, this repo uses local Markdown agents, standalone `opencode-*` skills, prompt gates, MCP, and structured documentation under `.opencode/docs/`.

This repository is also positioned as a **local harness engineering system**.

## Start here

If you are seeing this repo for the first time, treat it as:

- **not a typical end-user application**, but rather
- **configuration and workflow for OpenCode**, with integration support for OpenChamber when used.

This repo is best suited for:

- users who work with OpenCode regularly, including through OpenChamber,
- people who want stricter agent-based workflows,
- maintainers who need structured docs, quality gates, and evidence.

This repo is **less suitable** if you expect:

- a visual application opened directly in the browser,
- a simple frontend/backend boilerplate,
- setup without API keys or additional tools.

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

`AGENTS.md` is now a table of contents plus non-negotiable rules.
Detailed policy lives in `.opencode/docs/`.
Plans are first-class artifacts under `.opencode/plans/`.

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

### What is CLIProxyAPI in this repo?

In this repo, **CLIProxyAPI** is the primary model provider used by OpenCode to run local agents.

- `CLIPROXYAPI_BASE_URL` → base URL endpoint OpenAI-compatible
- `CLIPROXYAPI_API_KEY` → API key for authentication with that provider

If these two values are wrong or empty, agents may fail to call models even if the rest of the configuration looks correct.

Copy `.env.example` to `.env` and set every `OPENCODE_MODEL_*` value before launching OpenCode. Missing env vars resolve to an empty string, which can break OpenCode model routing.

Model routing is currently applied through two paths:

- `opencode.json` uses `OPENCODE_MODEL_DEFAULT` for the default runtime model
- `scripts/sync-agent-models.mjs` synchronizes literal `model:` values in `agents/*.md` with `OPENCODE_MODEL_*` values from `.env`

If you change `OPENCODE_MODEL_*`, run:

```bash
npm run sync:agent-models
```

### Model routing table

| Env var | Default / recommended model | Used by / capability | Cost guidance |
|---|---|---|---|
| `OPENCODE_MODEL_DEFAULT` | `cliproxyapi/gpt-5.3-codex` | Top-level default model and general fallback | Use Codex lane as balanced default for coding-heavy work while keeping specialist high-risk lanes stronger. |
| `OPENCODE_MODEL_ORCHESTRATOR` | `cliproxyapi/gpt-5.4` | `@orchestrator` primary routing/integration | Keep high quality for delegation, coordination, and final synthesis. |
| `OPENCODE_MODEL_PLANNER` | `cliproxyapi/gpt-5.3-codex` | `@artifact-planner`, `modes/plan.md`, `agents-disabled/plan.md` | Planning is codebase-heavy and can use Codex to reduce cost while keeping structure strong. |
| `OPENCODE_MODEL_DESIGN` | `cliproxyapi/gpt-5.4` | `@designer` | UI and visual reasoning are higher-value, so keep quality high. |
| `OPENCODE_MODEL_REVIEW` | `cliproxyapi/gpt-5.4` | `@oracle`, `@quality-gate`, `@council` | Review lanes should stay strict and high quality; optimize for correctness over cost. |
| `OPENCODE_MODEL_ADVISORY` | `cliproxyapi/gpt-5.4` | `@architect` | Advisory work is often high-stakes; keep the stronger model unless cost pressure is extreme. |
| `OPENCODE_MODEL_EXECUTION` | `cliproxyapi/gpt-5.3-codex` | `@fixer` | Use Codex for bounded implementation/testing because this lane is code-edit heavy. |
| `OPENCODE_MODEL_DISCOVERY` | `cliproxyapi/gpt-5.4-mini` | `@explorer`, `@librarian` | Discovery and read-only analysis can usually use the lower-cost model. |
| `OPENCODE_MODEL_DOCUMENTS` | `cliproxyapi/gpt-5.4-mini` | Reserved compatibility lane (document-centric work now routes via `@librarian`) | Keep for env compatibility; active document support is merged into librarian. |
| `OPENCODE_MODEL_IMPROVEMENT` | `cliproxyapi/gpt-5.4-mini` | `@skill-improver` | Small prompt/skill refinements should stay on the cheaper lane. |

## Domain specialist and workflow summary

Domain helper/advisory lanes are conditional.
Tiny UI polish still goes to `@designer`, and isolated bugfixes still go to `@fixer`.

- `@skill-improver` is used for non-trivial follow-up, repeated failures, policy gaps, or explicit requests.
- no blind external updates.
- `@quality-gate` returns statuses such as `PASS_WITH_RISKS`, `NEEDS_FIX`, and `BLOCKED`.
- Redundant `build` and `general` local agents have been removed.

## Important scripts

- `npm run setup:tools`
- `npm run doctor`
- `npm run post:update`
- `npm run sync:agent-models`
- `npm run test:prompt-gates`

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

Additional harness checks:

```bash
npm run check:docs
npm run check:agents
npm run check:skills
npm run check:evidence
```

## Validation and auto-commit summary

Auto-commit defaults to ON for local commits only; never push automatically.

- Run only after a **plan-bound non-trivial task is complete**, **validation passes**, and `@quality-gate` returns `PASS` or `PASS_WITH_RISKS` without a blocker.
- Review `git status`/`git diff`, then **stage only relevant files**.
- Auto-generated commit messages use a **short subject plus bullet-point body**.
- Never stage `.env`, secrets, tokens, credentials, unrelated untracked files, or generated/vendor files unless the plan/user explicitly approves them.
- Never use `--no-verify`, `--no-gpg-sign`, `amend`, force push, or destructive git commands.
- If scope or staging is unclear, stop and ask.

## Internal workflow summary

- Redundant `build` and `general` local agents have been removed.
- `@skill-improver` is used for non-trivial follow-up, repeated failures, policy gaps, or explicit requests.
- `@quality-gate` returns statuses such as `PASS_WITH_RISKS`, `NEEDS_FIX`, and `BLOCKED`.

Full details remain in `.opencode/docs/` and the related agent/skill files.

## References

- OpenCode — the main platform and runtime targeted by this repo configuration:
  - https://github.com/sst/opencode
- Slim preset ancestor — the preset/ancestor that served as the starting point before this repo evolved into `opencode-capybara`:
  - https://github.com/YZenKid/oh-my-opencode-slim-preset
- RTK AI — the primary toolchain for token compression / context packing, used together with Caveman according to the repo workflow:
  - https://github.com/rtk-ai/rtk
- Caveman — the companion workflow used together with RTK, not a separate alternative path:
  - https://github.com/JuliusBrussee/caveman
- GPT Harness Engineering — conceptual reference for evals, replayability, evidence, and harness hardening:
  - https://openai.com/index/harness-engineering/
