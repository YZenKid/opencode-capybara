---
name: opencode-devops
description: Senior DevOps playbook for GitHub Actions, Docker, env config, deploy, monitoring, release scripts, rollback planning, and destructive-action approval gates.
---

# OpenCode DevOps Skill

Use for bounded CI/CD, containers, environment, deployment, monitoring, and release work. Detect actual project runtimes, build tools, and deploy targets from repo evidence; local project conventions win; make no stack assumptions.

## Trigger / skip
- Trigger: GitHub Actions, Dockerfile/Compose, build scripts, env templates, release/rollback docs, deploy config, monitoring checks, CI failure fixes.
- Skip: production deploy/delete/secret rotation without explicit approval; architecture-level platform design → `@architect`; security/release final signoff → `@quality-gate`.

## Stack detection
- Inspect `.github/workflows`, `Dockerfile*`, `docker-compose*`, `Makefile`, package scripts, language/tool manifests, build commands, deploy docs, env examples.
- Identify runtime image, build cache, healthcheck, ports, volumes, env injection, secrets source, migrations in release path.
- Detect CI triggers, branch filters, permissions, concurrency, artifacts, caches, matrix, deployment environments.

## Responsibilities
- Reuse existing CI/CD, Docker, env, release, and monitoring conventions.
- Greenfield App Accelerator: support preview/dev/prod readiness for the first slice without forcing premature full production rollout.
- Maintenance Stability Mode: keep ops changes minimal, rollback-aware, and evidence-backed.
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
1. Inspect workflows, Docker, scripts, env docs, deploy/release path.
2. Mark destructive, credential, production, and migration boundaries.
3. Reproduce failure locally or via read-only CI evidence when possible.
4. Implement minimal config/script/doc change.
5. Validate with safe syntax/build/test/dry-run commands.
6. Report rollback, monitoring, and residual risk.

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
