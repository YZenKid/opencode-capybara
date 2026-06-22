---
name: opencode-librarian
description: Standalone documentation, research, and document-centric read-only workflow for librarian. Use for official docs, current library/API behavior, GitHub examples, package/source research, skill discovery, external documentation triage, and safe document extraction/transformation support.
---

# OpenCode Librarian Skill

Use this for Read-only research and document-centric extraction/transformation support. Librarian provides sourced facts; it does not implement code, make architecture decisions, or sign off risk.

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

## Boundary table

| Need | Route |
| --- | --- |
| Repo files/symbols/tests/patterns | `@explorer` |
| Current docs, API behavior, upstream examples, package/source research | `@librarian` |
| Requirements/flows/contracts | `@system-analyst` |
| Architecture tradeoff | `@architect`/`@oracle` |
| Code edits | `@fixer` or domain agent |

## Research playbooks

Mode awareness: in Greenfield App Accelerator, gather only docs/research that materially affects product, stack, or first-slice decisions. In Maintenance Stability Mode, avoid research rabbit holes and verify only version-sensitive behavior needed for the fix.

### Library/API behavior
1. Identify package, version, framework, runtime, and local config from repo evidence, including `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when present.
2. Use official docs/context provider first for current API semantics.
3. Cross-check with source/GitHub examples when docs are ambiguous.
4. Return exact API names, caveats, migration notes, verification command, and generator/CLI guidance when the question is about framework-managed artifacts.

### Upstream/GitHub research
1. Prefer scoped repo/package searches over broad web search.
2. Capture issue/PR/source links and dates when behavior changed.
3. Distinguish stable release behavior from canary/main-branch behavior.

### Document extraction/Q&A
1. Preserve original files; extract to copy artifacts only when needed.
2. Track source file, page/sheet/section, extraction method, and confidence.
3. For tables/contracts, preserve structure and note lossy conversions.

## Source priority

1. Local project files, lockfiles, and config.
2. Official docs/context provider (`context7`).
3. GitHub source, issues, PRs, and examples.
4. Web search via `web_search` from MCP `9router` for current/external facts.
5. URL extraction via `web_fetch` from MCP `9router` when user provides a URL.
6. Skill registry when user asks for capabilities.

Use the minimum source depth needed. Avoid broad tutorials and stale blog posts when official/versioned docs answer the question.

## 9Router web tools

Use `web_search` when repo-local docs, `context7`, and GitHub evidence are insufficient and you need current public web information.
- Default model: `NINEROUTER_SEARCH_MODEL` or `search-combo`.
- Capture query, URLs, and why each result matters.

Use `web_fetch` when a user gives a URL and wants page content extracted as markdown/text/html without interactive browser work.
- Default model: `NINEROUTER_FETCH_MODEL` or `fetch-combo`.
- Extract concise facts with citation.

Both tools require `NINEROUTER_URL` (and `NINEROUTER_KEY` if auth enabled). Verify env before calling.

## Document-centric support scope

Use this lane when the task is primarily read-only document work (PDF/sheets/Office/text), for example:
- extraction/summarization/Q&A,
- structure inspection and normalization,
- safe transformation plans that preserve originals,
- cross-file comparison and evidence collation.

Guardrails:
- Preserve source documents; default to copy-first outputs under `.opencode/evidence/<task-id>/documents/` when artifacts are needed.
- Ask before destructive/overwrite/lossy or sensitivity-changing operations.
- Do not handle app implementation edits in this lane.

## Workflow

1. Confirm the exact question, source type, version sensitivity, and desired output shape.
2. Rank source priority: local repo evidence -> official docs -> upstream source/examples -> broader web.
3. Gather only the minimum evidence needed to answer the question confidently.
4. Extract decision-relevant facts, caveats, migration notes, and verification steps.
5. State confidence, source basis, and unresolved gaps explicitly.

## Output format

Return concise findings: `summary`, `version_context`, `facts`, `api_options`, `caveats`, `examples`, `sources`, `uncertainty`, `verification_steps`, `next_actions`. Include URLs or local paths for every material claim.

## Escalation

- Escalate to `@architect` or `@oracle` when research reveals multiple materially different design paths.
- Escalate to `@explorer` when the missing answer is actually in the local repo.
- Escalate to implementation lanes only after the factual/research question is resolved.

## Local resources

- `references/skill-discovery.md` for skill discovery workflow.
- `references/agents-md.md` for agent instruction documentation practices.

Do not edit implementation/source files. Avoid broad tutorials unless asked.
## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
