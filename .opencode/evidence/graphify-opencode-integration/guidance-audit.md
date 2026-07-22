# Graphify Guidance Audit

- Task: `graphify-opencode-integration`
- Slice: G3 agent and skill guidance
- Claim level: `scoped`
- Scope: prompt, docs, and skill guidance only

## Changed files

- `AGENTS.md` — inherited query-first Graphify policy for broad architecture/dependency discovery.
- `.opencode/docs/MCP.md` — Graphify optional/read-only boundary and rejected integration modes.
- `.opencode/docs/TOOL_USAGE.md` — query-first workflow, narrow request rule, fallback and verification.
- `.opencode/docs/AGENT_TOOL_ACCESS.md` — cross-lane Graphify access boundary and role invariants.
- `.opencode/docs/SKILLS.md` — `graphify-discovery` index entry.
- `skills/graphify-discovery/SKILL.md` — dedicated workflow, exact commands vocabulary, boundaries, and output contract.
- `.opencode/evidence/graphify-opencode-integration/guidance-audit.md` — this evidence.

## Validation

- `npm run check:docs` — PASS, docs integrity check passed.
- `npm run check:agents` — PASS, agent boundary check passed.
- `npm run check:skills` — PASS, skill contract check passed for 23 existing skills.
- Inheritance scan — PASS, 49 active agent/skill files inherit `AGENTS.md` guidance containing `Graphify`, `graphify-out/graph.json`, `INFERRED`, and `AMBIGUOUS`.
- `git diff --check` — PASS.

## Preserved invariants

- Graphify remains optional, local, code-only, and read-only.
- Graph output never replaces direct source reading, tests, or runtime checks.
- `INFERRED` and `AMBIGUOUS` edges remain leads, not facts.
- Missing or stale graph falls back to normal repository discovery or approved refresh.
- No semantic LLM extraction, HTTP server, unapproved scheduler, strict source-read blocking, package installation, or config edit was performed by this slice. Later user-approved repository-local detached post-commit/post-checkout hooks are documented separately.
- `commands/init-harness.md` was not touched by this slice.

## Working-tree note

Pre-existing/out-of-scope changes remain unmodified: `commands/init-harness.md`, `opencode.json`, and `scripts/graphify-mcp-wrapper`. They are not part of G3 evidence.

## Residual risk

Runtime Graphify installation, wrapper behavior, MCP startup, graph freshness, and config parse remain G2/runtime scope and are unverified here.
