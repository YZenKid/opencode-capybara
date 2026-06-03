# Generated: Prompt Gate Report

Generated inventory of deterministic prompt-gate checks. This file is advisory and must not replace canonical policy in `.opencode/docs/PROMPT_GATES.md`.

- Gate count: 93
- Unique files covered: 50
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
17. **orchestrator indonesian user-facing policy gate** — `skills/opencode-orchestrator/SKILL.md`
18. **orchestrator planner invocation gate** — `skills/opencode-orchestrator/SKILL.md`
19. **orchestrator delegation threshold skill gate** — `skills/opencode-orchestrator/SKILL.md`
20. **orchestrator document fallback skill gate** — `skills/opencode-orchestrator/SKILL.md`
21. **council language split gate** — `agents/council.md`
22. **canonical execution posture gate** — `.opencode/docs/AGENT_ROUTING.md`
23. **canonical planner invocation gate** — `.opencode/docs/AGENT_ROUTING.md`
24. **orchestrator direct-vs-delegate threshold gate** — `.opencode/docs/AGENT_ROUTING.md`
25. **canonical document fallback routing gate** — `.opencode/docs/AGENT_ROUTING.md`
26. **mcp state terminology gate** — `.opencode/docs/MCP.md`
27. **tool usage mcp state gate** — `.opencode/docs/TOOL_USAGE.md`
28. **agent tool access mcp state gate** — `.opencode/docs/AGENT_TOOL_ACCESS.md`
29. **golden principles finish-first gate** — `.opencode/docs/GOLDEN_PRINCIPLES.md`
30. **quality gate subagent gate** — `agents/quality-gate.md`
31. **redundant build agent removed gate** — `agents/build.md`
32. **redundant general agent removed gate** — `agents/general.md`
33. **skill improver subagent gate** — `agents/skill-improver.md`
34. **skill improver standalone skill gate** — `skills/opencode-skill-improver/SKILL.md`
35. **designer signoff contract** — `skills/opencode-designer/SKILL.md`
36. **designer design-guide contract** — `skills/opencode-designer/SKILL.md`
37. **designer general design readiness gate** — `skills/opencode-designer/SKILL.md`
38. **orchestrator UI hard stop** — `agents/orchestrator.md`
39. **orchestrator general design blueprint hard stop** — `agents/orchestrator.md`
40. **orchestrator auto-commit gate** — `agents/orchestrator.md`
41. **orchestrator standalone parity contract** — `skills/opencode-orchestrator/SKILL.md`
42. **orchestrator standalone general design blueprint gate** — `skills/opencode-orchestrator/SKILL.md`
43. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
44. **quality gate standalone skill** — `skills/opencode-quality-gate/SKILL.md`
45. **redundant build skill removed gate** — `skills/opencode-build/SKILL.md`
46. **redundant general skill removed gate** — `skills/opencode-general/SKILL.md`
47. **fixer skill UI pause gates** — `skills/opencode-fixer/SKILL.md`
48. **unified architect subagent gate** — `agents/architect.md`
49. **unified architect skill gate** — `skills/opencode-architect/SKILL.md`
50. **conditional domain specialist routing gate** — `agents/orchestrator.md`
51. **orchestrator conditional domain skill gate** — `skills/opencode-orchestrator/SKILL.md`
52. **artifact planner domain advisory gate** — `agents/artifact-planner.md`
53. **artifact planner production blueprint skill gate** — `skills/opencode-artifact-planner/SKILL.md`
54. **global conditional domain specialist gate** — `.opencode/docs/AGENT_ROUTING.md`
55. **readme conditional domain specialist gate** — `README.md`
56. **readme docs system-of-record gate** — `README.md`
57. **tool setup script contract gate** — `package.json`
58. **rtk caveman onboarding docs gate** — `README.md`
59. **rtk opt-in policy gate** — `AGENTS.md`
60. **setup-dev-tools contract gate** — `scripts/setup-dev-tools.mjs`
61. **doctor read-only contract gate** — `scripts/doctor.mjs`
62. **docs integrity contract gate** — `scripts/docs-integrity-check.mjs`
63. **docs index system-of-record gate** — `.opencode/docs/index.md`
64. **harness evals gate** — `.opencode/docs/EVALS.md`
65. **visual asset generator manifest and icon rules** — `agents/visual-asset-generator.md`
66. **visual asset generator standalone manifest rules** — `skills/opencode-visual-asset-generator/SKILL.md`
67. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
68. **skill improver documentation gate** — `README.md`
69. **auto-commit policy readme gate** — `README.md`
70. **explorer agent gate** — `agents/explorer.md`
71. **librarian agent gate** — `agents/librarian.md`
72. **oracle agent gate** — `agents/oracle.md`
73. **designer agent gate** — `agents/designer.md`
74. **fixer agent gate** — `agents/fixer.md`
75. **standalone identity gate** — `README.md`
76. **artifact planner env routing gate** — `agents/artifact-planner.md`
77. **package identity gate** — `package.json`
78. **runtime plugin removal gate** — `opencode.json`
79. **runtime dependency removal gate** — `package.json`
80. **lockfile dependency removal gate** — `package-lock.json`
81. **tui plugin removal gate** — `tui.json`
82. **runtime plugin wording gate** — `README.md`
83. **obsolete bun lockfile removed gate** — `bun.lock`
84. **manual commit message format gate** — `commands/commit-message.md`
85. **retired workflow command removed gate** — `commands/tdd.md`
86. **retired UI workflow command removed gate** — `commands/replicate-ui.md`
87. **retired revamp workflow command removed gate** — `commands/revamp-like.md`
88. **quality-gate merged review lanes gate** — `skills/opencode-quality-gate/SKILL.md`
89. **mode-aware greenfield maintenance routing gate** — `.opencode/docs/AGENT_ROUTING.md`
90. **mode-aware quality evidence gate** — `.opencode/docs/QUALITY.md`
91. **orchestrator mode selection gate** — `skills/opencode-orchestrator/SKILL.md`
92. **artifact planner creative depth gate** — `skills/opencode-artifact-planner/SKILL.md`
93. **fullstack greenfield slice gate** — `skills/opencode-fullstack/SKILL.md`
