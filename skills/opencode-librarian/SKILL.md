---
name: opencode-librarian
description: Standalone documentation, research, and document-centric read-only workflow for librarian. Use for official docs, current library/API behavior, GitHub examples, package/source research, skill discovery, external documentation triage, and safe document extraction/transformation support.
---

# OpenCode Librarian Skill

Use this for read-only research and document-centric extraction/transformation support.

## Source priority

1. Local project files, lockfiles, and config.
2. Official docs/context provider.
3. GitHub source, issues, PRs, and examples.
4. Web search for current/external facts.
5. Skill registry when user asks for capabilities.

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

## Output format

Return concise findings: version/context, relevant APIs/options, official caveats, examples, sources consulted, uncertainty, and verification steps.

## Local resources

- `references/skill-discovery.md` for skill discovery workflow.
- `references/agents-md.md` for agent instruction documentation practices.

Do not edit implementation/source files. Avoid broad tutorials unless asked.
