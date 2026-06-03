---
name: opencode-devops
description: Devops workflow for GitHub Actions, Docker, env config, deploy, monitoring, release scripts, rollback planning, and destructive-action approval gates.
---

# OpenCode Devops Skill

Use for bounded CI/CD, Docker, environment, deployment, monitoring, and release work.

## Duties
- Reuse existing workflows, Docker config, env conventions, release scripts, and docs.
- Prefer dry-run/read-only/local validation before mutation.
- Record rollback and monitoring evidence for release-affecting changes.

## Forbidden
- Do not deploy, delete, rotate credentials, or mutate production without explicit approval.
- Do not write tokens, keys, or `.env` secrets.
- Do not add token/key MCPs unless user explicitly configures them.

## Senior reference knowledge
- See `.opencode/docs/SENIOR_SKILLS_REFERENCES.md`.
- Relevant reference: `xixu-me/skills/github-actions-docs`.
- Use as non-authoritative inspiration for GitHub Actions syntax/checklists; local CI config and approval gates win.

## Workflow
1. Inspect CI/CD, Docker, env, deploy, and monitoring patterns.
2. Mark destructive/credential boundaries.
3. Implement minimal config/script/doc change.
4. Validate with safe commands.
5. Report rollback, observability, and secret risks.

## Output
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence` plus validation commands/results.
