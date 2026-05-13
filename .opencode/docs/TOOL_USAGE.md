# Tool Usage Handbook

This document is the canonical operational guide for choosing and using tools in this repository.

Use it for **when/why/how** decisions. Do **not** treat this as a schema dump.

Related docs:
- MCP inventory: [MCP.md](./MCP.md)
- Agent boundary matrix: [AGENT_TOOL_ACCESS.md](./AGENT_TOOL_ACCESS.md)
- Role routing: [AGENT_ROUTING.md](./AGENT_ROUTING.md)

Model note: this handbook is tool-heuristics only. Core/specialist ownership and planner triggering rules are defined in `AGENT_ROUTING.md`.

## Vocabulary (normative)

- **available**: tool exists in the runtime/session.
- **preferred**: first choice for a task category.
- **permitted**: allowed for the current agent/skill boundary.
- **fallback**: next safe option when preferred tool is unavailable or not permitted.

Rule: a tool must be both **available** and **permitted** before use. If not, use documented **fallback**.

## MCP state model (normative)

When reasoning about configured MCP tools, use the same state terms as [MCP.md](./MCP.md):
- configured
- auth-blocked/unauthenticated
- authenticated
- connected
- usable
- read-only/unsupported

Operational rule: configured does not imply usable.

### Figma quick interpretation
- `figma` present in inventory only proves **configured**.
- If OAuth/session is missing or blocked, treat as **auth-blocked/unauthenticated** and use fallback workflow.
- Treat as **usable** only when the required capability works in the current client/server/role context.
- If a capability is not supported (for example canvas-write in current environment), classify it as **read-only/unsupported** for that action.

## Tool classes

### 1) Built-in OpenCode tools
Primary examples used in this repo:
- Local code/docs work: `read`, `glob`, `grep`, `apply_patch`
- Command execution and validation: `bash`
- Structured clarification: `question`
- Skill loading/routing support: `skill`

### 2) Configured MCP tools
See [MCP.md](./MCP.md) for the active inventory.

Commonly used categories:
- Official docs lookup (`context7`)
- Web/current information (`brave-search`)
- GitHub APIs/search/PR workflows (`github`)
- Browser/runtime UI evidence (`playwright`)
- Security scans/findings (`semgrep`)
- Design-generation surfaces (`figma`, image tooling)
- Time/locality helpers (`time`)

## Selection heuristics

1. **Prefer repo-local evidence first** for codebase questions.
   - Preferred: `read` + `glob` + `grep`
   - Fallback: `bash` for execution-only needs

2. **Use external sources only when local context is insufficient or version-sensitive.**
   - Preferred: `context7` for library/API behavior
   - Fallback: `github` examples/source, then `brave-search`

3. **Use role-appropriate tool paths.**
   - If tool is available but outside role boundary, delegate to the permitted agent.

4. **Use automation evidence for UI/runtime claims.**
   - Preferred: `playwright` with stable capture workflow
   - Anti-pattern: one-shot screenshot claims for animated/lazy pages

5. **Choose least-risk write path.**
   - Preferred: minimal file edits with `apply_patch`
   - Anti-pattern: broad unrelated edits or bypassing repo conventions

## Common workflows

### A) Local code/docs update
1. Discover files (`glob`, `grep`)
2. Read exact context (`read`)
3. Edit minimally (`apply_patch`)
4. Validate (`bash` running project checks)

### B) Library behavior verification
1. Check local usage first (`grep`, `read`)
2. Resolve and read official docs (`context7`)
3. Use GitHub/source examples only if still ambiguous (`github`)

### C) PR/issue/release operations
1. Prefer `github` MCP operations for structured GitHub tasks
2. Use local `bash` git commands for local repository state and commits
3. Keep safety rules (no force actions unless explicitly requested)

### D) UI/reference validation
1. Use `playwright` for deterministic capture/evidence
2. Use matching viewport + wait/stabilize/scroll/settle across reference/current/final
3. Record rendering-affecting console/network issues when material

## Anti-patterns

- Using external search when repo-local docs/code already answer the question.
- Treating tool availability as implicit permission for every agent.
- Dumping raw parameter schemas into canonical policy docs.
- Doing destructive git/runtime actions without explicit user intent.
- Claiming parity/quality without runnable evidence.

## Fallback rules

When preferred tool is unavailable, not permitted, or fails:

1. **Retry strategy:** prefer same-class alternative first (local→local, docs→docs).
2. **Role strategy:** delegate to agent with permitted access.
3. **Evidence strategy:** state limitation explicitly in summary/evidence.
4. **Safety strategy:** do not substitute with risky/destructive operations.

Examples:
- `context7` unavailable → local code evidence + `github` source/docs + note limitation.
- `playwright` unavailable for UI claim → provide bounded claim level and record missing runtime evidence.
- Write tool not permitted in current lane → route to implementing lane (`@fixer`) instead of forcing edits.

## Maintenance rules

When tools/MCP inventory changes:

1. Update [MCP.md](./MCP.md) inventory.
2. Update this handbook only where behavior/selection guidance changes.
3. Update [AGENT_TOOL_ACCESS.md](./AGENT_TOOL_ACCESS.md) when role boundary or preferred paths change.
4. Run docs checks and keep index links current.
