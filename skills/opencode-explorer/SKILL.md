---
name: opencode-explorer
description: Standalone read-only codebase discovery workflow for explorer. Use for finding files, symbols, tests, fixtures, patterns, architecture maps, repository structure, and reuse candidates with fast targeted search.
---

# OpenCode Explorer Skill

Use this for read-only discovery.

## Search strategy

- Start with targeted glob/grep/AST searches.
- Read only relevant snippets.
- Use broad map/codemap only for unfamiliar repos or explicit mapping requests.
- Parallelize independent searches.

## Return

Relevant files/symbols, line ranges, patterns, test locations, reuse candidates, risks, and suggested next steps.

## Local resources

- `scripts/codemap/`, `references/codemap.md`, `references/codemap-README.md` for code maps.
- `scripts/cartography/`, `references/cartography-README.md` for hierarchical repo cartography.

Never edit files.
