# Planning Evidence — graphify-discovery-coverage

## Mode
- `Maintenance Stability Mode`

## Source strategy
- `confirmed_repo`: `AGENTS.md`, `.opencode/docs/{MCP.md,TOOL_USAGE.md,AGENT_TOOL_ACCESS.md,SKILLS.md}`, `skills/graphify-discovery/SKILL.md`, `scripts/{agent-boundary-check.mjs,skill-contract-check.mjs,generate-generated-docs.mjs}`, `package.json`, `docs/generated/mcp-risk-matrix.md`
- External docs skipped: tidak perlu. Tugas ini policy lokal repo, bukan version-sensitive library behavior.
- Browser/runtime UI skipped: tidak ada UI/runtime browser surface.

## Verified findings
1. `confirmed_repo`: root `AGENTS.md` sudah memuat rule Graphify broad architecture/dependency discovery dan optional/read-only boundary.
2. `confirmed_repo`: `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`, `.opencode/docs/SKILLS.md`, dan `skills/graphify-discovery/SKILL.md` sudah memuat policy Graphify pusat.
3. `confirmed_repo`: `package.json` menyediakan `npm run check:agents`, `npm run check:skills`, `npm run docs:generate:check`.
4. `confirmed_repo`: `scripts/agent-boundary-check.mjs`, `scripts/skill-contract-check.mjs`, dan `scripts/generate-generated-docs.mjs` ada dan menjadi check surfaces relevan.
5. `confirmed_repo`: grep menemukan cap `3` aktif pada `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`, `docs/generated/mcp-risk-matrix.md`, dan 18 `skills/opencode-*` files.
6. `confirmed_repo`: tidak ada existing plan file untuk `graphify-discovery-coverage`; plan baru perlu dibuat.
7. `assumption`: current `check:agents`/`check:skills` belum memaksa Graphify inheritance/cap-2 drift check secara spesifik.

## Exact active cap-of-3 locations found
- `.opencode/docs/MCP.md`
- `.opencode/docs/TOOL_USAGE.md`
- `.opencode/docs/AGENT_TOOL_ACCESS.md`
- `docs/generated/mcp-risk-matrix.md`
- `skills/opencode-plan-reviewer/SKILL.md`
- `skills/opencode-visual-context-extractor/SKILL.md`
- `skills/opencode-visual-asset-generator/SKILL.md`
- `skills/opencode-devops/SKILL.md`
- `skills/opencode-system-analyst/SKILL.md`
- `skills/opencode-skill-improver/SKILL.md`
- `skills/opencode-designer/SKILL.md`
- `skills/opencode-librarian/SKILL.md`
- `skills/opencode-orchestrator/SKILL.md`
- `skills/opencode-backend/SKILL.md`
- `skills/opencode-project-manager/SKILL.md`
- `skills/opencode-artifact-planner/SKILL.md`
- `skills/opencode-quality-gate/SKILL.md`
- `skills/opencode-mobile/SKILL.md`
- `skills/opencode-fullstack/SKILL.md`
- `skills/opencode-fixer/SKILL.md`
- `skills/opencode-architect/SKILL.md`
- `skills/opencode-frontend/SKILL.md`
- `skills/opencode-council/SKILL.md`
- `skills/opencode-oracle/SKILL.md`
- `skills/opencode-explorer/SKILL.md`

## Chosen strategy
- Graphify: centralized inheritance first. Pertahankan root/canonical docs + dedicated skill sebagai pusat. Tambah/extend mechanical audit daripada copy prose ke semua local agents/skills.
- Sequential Thinking: harmonisasi semua authoritative duplicated snippets dari 3 ke 2. Generated risk matrix ikut refresh sebagai derived output.
- Checks: reuse `check:agents`, `check:skills`, `docs:generate:check`; tambah drift assertion hanya bila existing checks belum cukup.

## Residual uncertainty
- `assumption`: implementer mungkin perlu memperluas `prompt-gate-regression.mjs` atau check scripts agar “Graphify coverage audit command” menjadi mekanis dan stabil.
