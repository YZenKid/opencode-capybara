# Tool and Source Policy

Read this before MCP selection, external source lookup, template/source discovery, or porting work.

## MCP Discovery Matrix

- Multi-issue debugging / cascading failures / 3+ inter-related symptoms -> `sequential-thinking`.
- Version-sensitive framework/API/library behavior -> `context7`.
- Broad code search / pattern hunt -> `grep_app` or repo search.
- Repo / PR / issue / commit / branch / file history -> `github`.
- Static pattern / security smell / anti-pattern scan -> `semgrep`.
- Browser/UI/runtime flow / reproduction / DOM evidence -> `browseros`.

## Reference-first execution

- For non-trivial work, source strategy is repo evidence -> official docs -> upstream source/examples -> GitHub/web search -> browser/reference capture.
- Do not invent library/API behavior, version-sensitive defaults, or current best practice when a current reference is reachable.

## Template/Source Discovery Hard Gate

- If the task mentions templates, clone, port, copy, replicate, or similar, run hard discovery before implementation.
- Treat file-system template discovery as mechanical, not taste.
- Stop and ask if user intent conflicts with a template/license constraint.

## Source-approved 1:1 Porting / Literal Porting Contract

- If user says `1:1`, `clone`, `port`, `copy`, or `make exactly like`, default to literal copy/adapt/prune/direct reuse instead of redesign.
- Route source inventory and parity mapping before implementation.

## Trigger phrases to preserve

- MCP Discovery Matrix
- sequential-thinking
- Template/Source Discovery Hard Gate
- Source-approved 1:1 Porting / Literal Porting Contract
- reference-first by default, not repo-only
- context7
- browser/screenshots/reference URLs
