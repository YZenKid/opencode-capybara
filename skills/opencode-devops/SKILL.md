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
- Minimize secret exposure; never write tokens/keys/real `.env` values.
- Record rollback, blast radius, observability, and approval needs for release-affecting work.

## Senior heuristics / checklist
- CI: least-permission `GITHUB_TOKEN`, pinned actions where policy expects, cache keys scoped, concurrency cancels stale runs, artifacts named/retained intentionally.
- Docker: small deterministic builds, non-root when possible, `.dockerignore`, healthcheck, no secrets in layers, correct signal handling, reproducible build args.
- Env: example values only, required vars documented, prod/stage/dev separation clear.
- Release: migration order, rollback path, feature flags, smoke checks, logs/metrics/alerts, owner/on-call handoff.
- Safety: classify destructive commands; ask before deploy/delete/rotate/migrate prod.

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

## Escalation
- Ask explicit approval before deploy, prod migration, delete, credential rotation, public release, or external service mutation.
- Route `@architect` for platform topology, IaC strategy, scaling, multi-env redesign.
- Route `@quality-gate` for production/release/security-sensitive completion.

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


## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
