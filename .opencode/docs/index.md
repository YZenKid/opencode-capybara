# Documentation Index

This directory is the **system of record** for `opencode-capybara`.

## Canonical docs
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [AGENT_ROUTING.md](./AGENT_ROUTING.md)
- [AGENT_LEGIBILITY.md](./AGENT_LEGIBILITY.md)
- [QUALITY.md](./QUALITY.md)
- [QUALITY_SCORE.md](./QUALITY_SCORE.md)
- [SECURITY.md](./SECURITY.md)
- [PROMPT_GATES.md](./PROMPT_GATES.md)
- [SKILLS.md](./SKILLS.md)
- [MCP.md](./MCP.md)
- [TOOL_USAGE.md](./TOOL_USAGE.md)
- [AGENT_TOOL_ACCESS.md](./AGENT_TOOL_ACCESS.md)
- [EVALS.md](./EVALS.md)
- [GOLDEN_PRINCIPLES.md](./GOLDEN_PRINCIPLES.md)
- [DECISIONS.md](./DECISIONS.md)
- [RELEASE.md](./RELEASE.md)
- [GC_WORKFLOW.md](./GC_WORKFLOW.md)

## Planning and execution artifacts
- Plan artifacts live under `.opencode/plans/`.
- Task evidence lives under `.opencode/evidence/<task-id>/`.
- Use `.opencode/docs/QUALITY.md` as the canonical contract for evidence and replay expectations.

## Generated docs
Generated docs are advisory artifacts produced by `npm run docs:generate`. They are not the canonical source of policy.

- [generated/agent-matrix.md](../../docs/generated/agent-matrix.md)
- [generated/prompt-gate-report.md](../../docs/generated/prompt-gate-report.md)
- [generated/docs-integrity-report.md](../../docs/generated/docs-integrity-report.md)

## Reference docs
- [references/opencode.md](../../docs/references/opencode.md)
- [references/mcp.md](../../docs/references/mcp.md)

## Freshness rules
- `AGENTS.md` should point here, not duplicate policy detail.
- `README.md` should remain onboarding-oriented and link here for deeper detail.
- When policy changes, update the canonical doc and the relevant mechanical checks together.
- When repeated failures reveal a gap, add or update docs, gates, skills, or scripts rather than relying on memory.
