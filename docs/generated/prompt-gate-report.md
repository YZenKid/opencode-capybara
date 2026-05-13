# Generated: Prompt Gate Report

Generated inventory of deterministic prompt-gate checks. This file is advisory and must not replace canonical policy in `.opencode/docs/PROMPT_GATES.md`.

- Gate count: 86
- Unique files covered: 48
- Primary implementation: `scripts/prompt-gate-regression.mjs`

## Commands referenced
- `npm run test:prompt-gates`
- `npm run check:docs`
- `npm run check:agents`
- `npm run check:skills`
- `npm run check:evidence`
- `npm run docs:generate:check`
- `npm run check:harness`

## Gate inventory
1. **model routing env example gate** — `.env.example`
2. **project design init command gate** — `commands/init-design.md`
3. **project harness init command gate** — `commands/init-harness.md`
4. **local council subagent gate** — `agents/council.md`
5. **agent architecture selection gate** — `opencode.json`
6. **agents toc and docs system-of-record gate** — `AGENTS.md`
7. **agents non-negotiable rules gate** — `AGENTS.md`
8. **agents harness posture gate** — `AGENTS.md`
9. **agents planner invocation expectation gate** — `AGENTS.md`
10. **agents risk trigger gate** — `AGENTS.md`
11. **artifact planner design readiness gate** — `agents/artifact-planner.md`
12. **model routing documentation gate** — `README.md`
13. **artifact planner standalone skill gate** — `skills/opencode-artifact-planner/SKILL.md`
14. **artifact planner language split gate** — `agents/artifact-planner.md`
15. **designer workflow gate** — `agents/designer.md`
16. **orchestrator primary mode gate** — `agents/orchestrator.md`
17. **orchestrator language split gate** — `skills/opencode-orchestrator/SKILL.md`
18. **orchestrator planner invocation gate** — `skills/opencode-orchestrator/SKILL.md`
19. **orchestrator delegation threshold skill gate** — `skills/opencode-orchestrator/SKILL.md`
20. **council language split gate** — `agents/council.md`
21. **canonical execution posture gate** — `.opencode/docs/AGENT_ROUTING.md`
22. **canonical planner invocation gate** — `.opencode/docs/AGENT_ROUTING.md`
23. **orchestrator direct-vs-delegate threshold gate** — `.opencode/docs/AGENT_ROUTING.md`
24. **mcp state terminology gate** — `.opencode/docs/MCP.md`
25. **tool usage mcp state gate** — `.opencode/docs/TOOL_USAGE.md`
26. **agent tool access mcp state gate** — `.opencode/docs/AGENT_TOOL_ACCESS.md`
27. **golden principles finish-first gate** — `.opencode/docs/GOLDEN_PRINCIPLES.md`
28. **quality gate subagent gate** — `agents/quality-gate.md`
29. **redundant build agent removed gate** — `agents/build.md`
30. **redundant general agent removed gate** — `agents/general.md`
31. **skill improver subagent gate** — `agents/skill-improver.md`
32. **skill improver standalone skill gate** — `skills/opencode-skill-improver/SKILL.md`
33. **designer signoff contract** — `skills/opencode-designer/SKILL.md`
34. **designer design-guide contract** — `skills/opencode-designer/SKILL.md`
35. **designer general design readiness gate** — `skills/opencode-designer/SKILL.md`
36. **orchestrator UI hard stop** — `agents/orchestrator.md`
37. **orchestrator general design blueprint hard stop** — `agents/orchestrator.md`
38. **orchestrator auto-commit gate** — `agents/orchestrator.md`
39. **orchestrator standalone parity contract** — `skills/opencode-orchestrator/SKILL.md`
40. **orchestrator standalone general design blueprint gate** — `skills/opencode-orchestrator/SKILL.md`
41. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
42. **quality gate standalone skill** — `skills/opencode-quality-gate/SKILL.md`
43. **redundant build skill removed gate** — `skills/opencode-build/SKILL.md`
44. **redundant general skill removed gate** — `skills/opencode-general/SKILL.md`
45. **fixer skill UI pause gates** — `skills/opencode-fixer/SKILL.md`
46. **unified architect subagent gate** — `agents/architect.md`
47. **unified architect skill gate** — `skills/opencode-architect/SKILL.md`
48. **conditional domain specialist routing gate** — `agents/orchestrator.md`
49. **orchestrator conditional domain skill gate** — `skills/opencode-orchestrator/SKILL.md`
50. **artifact planner domain advisory gate** — `agents/artifact-planner.md`
51. **artifact planner production blueprint skill gate** — `skills/opencode-artifact-planner/SKILL.md`
52. **global conditional domain specialist gate** — `.opencode/docs/AGENT_ROUTING.md`
53. **readme conditional domain specialist gate** — `README.md`
54. **readme docs system-of-record gate** — `README.md`
55. **tool setup script contract gate** — `package.json`
56. **rtk caveman onboarding docs gate** — `README.md`
57. **rtk opt-in policy gate** — `AGENTS.md`
58. **setup-dev-tools contract gate** — `scripts/setup-dev-tools.mjs`
59. **doctor read-only contract gate** — `scripts/doctor.mjs`
60. **docs integrity contract gate** — `scripts/docs-integrity-check.mjs`
61. **docs index system-of-record gate** — `.opencode/docs/index.md`
62. **harness evals gate** — `.opencode/docs/EVALS.md`
63. **visual asset generator manifest and icon rules** — `agents/visual-asset-generator.md`
64. **visual asset generator standalone manifest rules** — `skills/opencode-visual-asset-generator/SKILL.md`
65. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
66. **skill improver documentation gate** — `README.md`
67. **auto-commit policy readme gate** — `README.md`
68. **explorer agent gate** — `agents/explorer.md`
69. **librarian agent gate** — `agents/librarian.md`
70. **oracle agent gate** — `agents/oracle.md`
71. **designer agent gate** — `agents/designer.md`
72. **fixer agent gate** — `agents/fixer.md`
73. **standalone identity gate** — `README.md`
74. **artifact planner env routing gate** — `agents/artifact-planner.md`
75. **package identity gate** — `package.json`
76. **runtime plugin removal gate** — `opencode.json`
77. **runtime dependency removal gate** — `package.json`
78. **lockfile dependency removal gate** — `package-lock.json`
79. **tui plugin removal gate** — `tui.json`
80. **runtime plugin wording gate** — `README.md`
81. **obsolete bun lockfile removed gate** — `bun.lock`
82. **manual commit message format gate** — `commands/commit-message.md`
83. **retired workflow command removed gate** — `commands/tdd.md`
84. **retired UI workflow command removed gate** — `commands/replicate-ui.md`
85. **retired revamp workflow command removed gate** — `commands/revamp-like.md`
86. **quality-gate merged review lanes gate** — `skills/opencode-quality-gate/SKILL.md`
