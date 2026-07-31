---
name: opencode-devops
description: Senior DevOps playbook for GitHub Actions, Docker, env config, deploy, monitoring, release scripts, rollback planning, and destructive-action approval gates.
---

# OpenCode DevOps Skill

Use for bounded CI/CD, containers, environment, deployment, monitoring, and release work. Detect actual project runtimes, build tools, and deploy targets from repo evidence; local project conventions win; make no stack assumptions.

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

## Internet-reference default
- Treat internet-backed lookup (`context7_*`, `websearch_*`, `webfetch`, upstream provider docs, GitHub examples) as the default for version-sensitive or best-practice-sensitive CI/CD, Docker, deploy, observability, or runtime decisions.
- If project-local stack/playbook docs already settle the question, cite them and skip the external call. Otherwise, do not rely on memory when a live lookup would materially improve safety or correctness.

## Finish-first + question batching
- See `.opencode/docs/EXECUTION_CONDUCT.md` for the source-of-truth contract. The short version:
  - If ambiguity is not `hard_stop`, complete the safest reversible scoped change, prefer dry-run/read-only validation first, and report residual items as `deferred_question` / `follow_up`.
  - Do not stop mid-task for internal execution choices. Group residual user decisions instead of dripping confirmations.

## Trigger / skip
- Trigger: GitHub Actions, Dockerfile/Compose, build scripts, env templates, release/rollback docs, deploy config, monitoring checks, CI failure fixes.
- Skip: production deploy/delete/secret rotation without explicit approval; architecture-level platform design → `@architect`; security/release final signoff → `@quality-gate`.

## Stack detection
- Inspect `.github/workflows`, `Dockerfile*`, `docker-compose*`, `Makefile`, package scripts, language/tool manifests, build commands, deploy docs, env examples.
- Identify runtime image, build cache, healthcheck, ports, volumes, env injection, secrets source, migrations in release path.
- Detect CI triggers, branch filters, permissions, concurrency, artifacts, caches, matrix, deployment environments.

## Responsibilities
- Reuse existing CI/CD, Docker, env, release, and monitoring conventions.
- Before framework-managed ops edits, read `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when present.
- Greenfield App Accelerator: support preview/dev/prod readiness for the first slice without forcing premature full production rollout.
- Maintenance Stability Mode: keep ops changes minimal, rollback-aware, and evidence-backed.
- Prefer documented project commands and official workspace/tooling generators first for existing apps too when relevant.
- Manual framework/tool-managed artifact creation is allowed only when the command/tool is unavailable or not permitted, the command failed with evidence, the project intentionally avoids the generator, the task customizes existing generated files, or the user explicitly asks for manual edits. Record the attempted or skipped command and reason in evidence.
- If framework/library command behavior is version-sensitive and the project docs do not already settle it, route to `@librarian` for official docs/context7 before coding.
- Prefer dry-run/local validation before remote mutation.
- Permit writing a user-supplied secret only when user explicitly provides exact local Git-ignored env-file path and exact key; use safe file write, never expose, log, upload, stage, commit, or place values in `.env.example`, and require separate explicit approval for external, staging, production, deploy, service mutation, or credential rotation.
- Record rollback, blast radius, observability, and approval needs for release-affecting work.

## Senior heuristics / checklist
- CI: least-permission `GITHUB_TOKEN`, pinned actions where policy expects, cache keys scoped, concurrency cancels stale runs, artifacts named/retained intentionally.
- Docker: small deterministic builds, non-root when possible, `.dockerignore`, healthcheck, no secrets in layers, correct signal handling, reproducible build args.
- Env: example values only, required vars documented, prod/stage/dev separation clear.
- Release: migration order, rollback path, feature flags, smoke checks, logs/metrics/alerts, owner/on-call handoff.
- Safety: classify destructive commands; ask before deploy/delete/rotate/migrate prod.

## Pre-flight Skill & MCP Discovery
Before the first substantial answer, diagnosis, route, or implementation step on non-trivial work:
- Name the skill explicitly (`Skill I'm using: ...`).
- Decide MCP applicability explicitly (`MCPs I'm using: ...`, `What I'm checking first: ...`).
- If an MCP is obviously applicable, use it or record a concrete skip reason. Silent skip is a defect.
- At final summary time, name one concrete thing this skill changed about execution. Loaded-but-unused skill is a process defect.

ponytail: This is a behavioral contract. Use `scripts/session-trace-audit.py` as the advisory checker until transcript hooks become first-class.

## Workflow
1. Read `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when present.
2. Inspect workflows, Docker, scripts, env docs, deploy/release path.
3. Mark destructive, credential, production, and migration boundaries.
4. Reproduce failure locally or via read-only CI evidence when possible.
5. TDD where relevant: add or identify failing config/test/check evidence before changing behavior.
6. Use documented project commands or official generators/scripts first where relevant; if manual fallback is used, record the exact command/tool and reason.
7. Implement minimal config/script/doc change.
8. Validate with safe syntax/build/test/dry-run commands.
9. Report rollback, monitoring, residual risk, and any generator fallback evidence.

## Validation
- GitHub Actions: YAML syntax/reusable workflow consistency; use existing CI checks/logs if available.
- Docker: `docker build`/Compose config only when safe and expected; avoid pushing images.
- App builds: run targeted build checks per repo conventions and detected stack.
- Secrets: confirm no `.env`, keys, tokens, or credentials added to diff.

## Output example

```yaml
status: PASS
files_changed:
  - docker-compose.yml
  - .github/workflows/deploy.yml
validation:
  commands:
    - "docker compose config"
    - "yamllint docker-compose.yml"
  results: "valid config, no lint errors"
evidence:
  approval: "user approved deployment changes"
  rollback_plan: "git revert + docker compose down"
```

## Escalation
- Ask explicit approval before deploy, prod migration, delete, credential rotation, public release, or external service mutation.
- Route `@architect` for platform topology, IaC strategy, scaling, multi-env redesign.
- Route `@quality-gate` for production/release/security-sensitive completion.

## Delegation Input Understanding Contract

Before acting on a delegated task, reconstruct the request from the handoff payload rather than from memory alone.

Minimum understanding checklist:
- `task_id` / `plan_id`: what task this belongs to
- `scope`: single concrete outcome you own
- `claim_level` + `claim_scope`: what you may report as done
- `source_basis`: the files/docs/refs you must treat as authority
- `must_preserve`: invariants that cannot be broken even if a shortcut seems easier
- `do_not_touch`: paths/scopes that are out of bounds
- `validation`: what you must run/check before reporting done
- `evidence_required`: what artifacts/logs/screenshots must exist before you return
- `open_assumptions`: what is still uncertain and must stay uncertain

If any of these are missing from the handoff for non-trivial work, stop and report `blocked: incomplete handoff contract` back to `@orchestrator`. Do not fill the gaps with intuition.

### Return contract
Your return report should mirror the handoff:
- what you changed or discovered,
- which `must_preserve` items were maintained,
- which validation checks you ran,
- which evidence paths now exist,
- what remains `assumption` / `unverified`.

ponytail: This is a soft discipline first. The upgrade path is a session-trace/delegation-log audit that flags workers who routinely act on incomplete handoffs.

## Output contract
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence`. Include approval gates, rollback notes, validation commands/results, and skipped unsafe actions.

## Domain references
- `.opencode/docs/SENIOR_SKILLS_REFERENCES.md`.
- Relevant inspiration: `xixu-me/skills/github-actions-docs` for GitHub Actions syntax/checklists.
- Local workflows, approval gates, and secrets policy win.

## Quality checklist
- [ ] Destructive/credential boundaries identified before commands.
- [ ] Stack docs read and current ops/tooling best practice verified.
- [ ] Safe validation or dry-run attempted first when possible.
- [ ] Rollback path documented.
- [ ] Secret handling remains safe.
- [ ] User-facing operational risk clearly stated.
- [ ] Evidence names exact validation command or dry-run used.

## Anti-patterns
- Applying ops changes with no rollback note.
- Changing credential-sensitive flows without explicit approval.
- Treating green CI output as full operational proof.
- Expanding bounded config change into architecture redesign.
- Editing deployment config from memory without current provider/tooling verification.
- Calling a workflow production-ready without rollback and observability notes.


## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.


<!-- scripts-mcp-pointer -->
`mcp.scripts` is a configured local read/check/query-only governance tool. This implementation skill should prefer it for matching validation and readiness checks when connected, usable, and permitted; no write operations exist in this slice. `caller_lane` in the tool payload is policy attestation only, not real authorization; this skill’s existing read/write boundaries still control what it may do. Canonical CLI fallback remains valid: `python3 ~/.config/opencode/scripts/<name>.py ...` when MCP is disconnected, unavailable, returns `tool_pending`, or is not permitted. Full policy: `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`.
## Graphify query-first contract

For code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes, query fresh available Graphify first. Use narrow query/path/explain. Direct source reading + tests/runtime still required. Missing/stale/unsupported fallback must be recorded. Tiny known-file and non-code skip only with explicit reason.

## Code and source search replacement contract

- Local code investigation: query fresh Graphify first when qualifying, then verify with built-in `grep`, `glob`, and `read`.
- Public/upstream code search: use `github_search_code`.
- Official or version-sensitive library/API docs: use `context7`.
- General current web facts: use `9router.web_search`, then `9router.web_fetch`.
