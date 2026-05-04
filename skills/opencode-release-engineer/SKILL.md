# Skill: opencode-release-engineer

Read-only release engineering workflow for production readiness. Use this only when deployment, CI/CD, environment configuration, migrations, monitoring, logging, rollback, backup, or operational readiness materially affects the task.

## Trigger / skip

- Trigger for production launch, staging preview, CI failures, migration rollout, environment validation, monitoring, Sentry/logging, deployment platforms, rollback, backup/recovery, and release checklists.
- Skip for pre-implementation ideation, tiny UI polish, local-only prototypes, or isolated bugfixes unless release risk exists.
- Do not deploy, mutate cloud resources, rotate secrets, or run destructive commands without explicit orchestrator/user approval.

## Workflow

1. Identify target runtime, deployment platform, environments, config/secrets, and build commands.
2. Define CI/CD checks: lint, typecheck, unit/integration/e2e, security scan, migration dry run, smoke tests.
3. Define environment readiness: required variables, secrets ownership, preview/staging/prod separation.
4. Define rollout plan: migration order, feature flags, rollback, backups, data integrity checks.
5. Define observability: structured logs, metrics, tracing, error tracking, alerts, runbooks.
6. Define post-deploy validation and production readiness level.

## Output contract

- Release checklist and risk summary.
- Required validation commands and smoke tests.
- Env/deployment/rollback plan.
- Monitoring/logging/alerting requirements.
- Readiness status: `local-ready`, `staging-ready`, `production-candidate`, `needs-ops`, or `blocked`.

## Quality bar

- No “production ready” claim without deployment and observability evidence.
- Prefer reversible rollout and explicit rollback.
- Protect secrets and avoid device-specific paths.
- Final release claims require `@quality-gate` evidence review.
