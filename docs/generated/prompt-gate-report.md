# Generated: Prompt Gate Report

Generated inventory of deterministic prompt-gate checks. This file is advisory and must not replace canonical policy in `.opencode/docs/PROMPT_GATES.md`.

- Gate count: 98
- Unique files covered: 52
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
16. **frontend implementation-basis gate** — `agents/frontend.md`
17. **quality gate source-trace gate** — `agents/quality-gate.md`
18. **designer source-pack and anti-generic gate** — `skills/opencode-designer/SKILL.md`
19. **frontend implementation-basis skill gate** — `skills/opencode-frontend/SKILL.md`
20. **quality gate source-basis skill gate** — `skills/opencode-quality-gate/SKILL.md`
21. **orchestrator primary mode gate** — `agents/orchestrator.md`
22. **orchestrator indonesian user-facing policy gate** — `skills/opencode-orchestrator/SKILL.md`
23. **orchestrator planner invocation gate** — `skills/opencode-orchestrator/SKILL.md`
24. **orchestrator delegation threshold skill gate** — `skills/opencode-orchestrator/SKILL.md`
25. **orchestrator document fallback skill gate** — `skills/opencode-orchestrator/SKILL.md`
26. **council language split gate** — `agents/council.md`
27. **canonical execution posture gate** — `.opencode/docs/AGENT_ROUTING.md`
28. **canonical planner invocation gate** — `.opencode/docs/AGENT_ROUTING.md`
29. **orchestrator direct-vs-delegate threshold gate** — `.opencode/docs/AGENT_ROUTING.md`
30. **canonical document fallback routing gate** — `.opencode/docs/AGENT_ROUTING.md`
31. **mcp state terminology gate** — `.opencode/docs/MCP.md`
32. **tool usage mcp state gate** — `.opencode/docs/TOOL_USAGE.md`
33. **agent tool access mcp state gate** — `.opencode/docs/AGENT_TOOL_ACCESS.md`
34. **golden principles finish-first gate** — `.opencode/docs/GOLDEN_PRINCIPLES.md`
35. **quality gate subagent gate** — `agents/quality-gate.md`
36. **redundant build agent removed gate** — `agents/build.md`
37. **redundant general agent removed gate** — `agents/general.md`
38. **skill improver subagent gate** — `agents/skill-improver.md`
39. **skill improver standalone skill gate** — `skills/opencode-skill-improver/SKILL.md`
40. **designer signoff contract** — `skills/opencode-designer/SKILL.md`
41. **designer design-guide contract** — `skills/opencode-designer/SKILL.md`
42. **designer general design readiness gate** — `skills/opencode-designer/SKILL.md`
43. **orchestrator UI hard stop** — `agents/orchestrator.md`
44. **orchestrator general design blueprint hard stop** — `agents/orchestrator.md`
45. **orchestrator auto-commit gate** — `agents/orchestrator.md`
46. **orchestrator standalone parity contract** — `skills/opencode-orchestrator/SKILL.md`
47. **orchestrator standalone general design blueprint gate** — `skills/opencode-orchestrator/SKILL.md`
48. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
49. **quality gate standalone skill** — `skills/opencode-quality-gate/SKILL.md`
50. **redundant build skill removed gate** — `skills/opencode-build/SKILL.md`
51. **redundant general skill removed gate** — `skills/opencode-general/SKILL.md`
52. **fixer skill UI pause gates** — `skills/opencode-fixer/SKILL.md`
53. **unified architect subagent gate** — `agents/architect.md`
54. **unified architect skill gate** — `skills/opencode-architect/SKILL.md`
55. **conditional domain specialist routing gate** — `agents/orchestrator.md`
56. **orchestrator conditional domain skill gate** — `skills/opencode-orchestrator/SKILL.md`
57. **artifact planner domain advisory gate** — `agents/artifact-planner.md`
58. **artifact planner production blueprint skill gate** — `skills/opencode-artifact-planner/SKILL.md`
59. **global conditional domain specialist gate** — `.opencode/docs/AGENT_ROUTING.md`
60. **readme conditional domain specialist gate** — `README.md`
61. **readme docs system-of-record gate** — `README.md`
62. **tool setup script contract gate** — `package.json`
63. **rtk caveman onboarding docs gate** — `README.md`
64. **rtk opt-in policy gate** — `AGENTS.md`
65. **setup-dev-tools contract gate** — `scripts/setup-dev-tools.mjs`
66. **doctor read-only contract gate** — `scripts/doctor.mjs`
67. **docs integrity contract gate** — `scripts/docs-integrity-check.mjs`
68. **docs index system-of-record gate** — `.opencode/docs/index.md`
69. **harness evals gate** — `.opencode/docs/EVALS.md`
70. **visual asset generator manifest and icon rules** — `agents/visual-asset-generator.md`
71. **visual asset generator standalone manifest rules** — `skills/opencode-visual-asset-generator/SKILL.md`
72. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
73. **skill improver documentation gate** — `README.md`
74. **auto-commit policy readme gate** — `README.md`
75. **explorer agent gate** — `agents/explorer.md`
76. **librarian agent gate** — `agents/librarian.md`
77. **oracle agent gate** — `agents/oracle.md`
78. **designer agent gate** — `agents/designer.md`
79. **fixer agent gate** — `agents/fixer.md`
80. **standalone identity gate** — `README.md`
81. **artifact planner env routing gate** — `agents/artifact-planner.md`
82. **package identity gate** — `package.json`
83. **runtime plugin removal gate** — `opencode.json`
84. **runtime dependency removal gate** — `package.json`
85. **lockfile dependency removal gate** — `package-lock.json`
86. **tui plugin removal gate** — `tui.json`
87. **runtime plugin wording gate** — `README.md`
88. **obsolete bun lockfile removed gate** — `bun.lock`
89. **manual commit message format gate** — `commands/commit-message.md`
90. **retired workflow command removed gate** — `commands/tdd.md`
91. **retired UI workflow command removed gate** — `commands/replicate-ui.md`
92. **retired revamp workflow command removed gate** — `commands/revamp-like.md`
93. **quality-gate merged review lanes gate** — `skills/opencode-quality-gate/SKILL.md`
94. **mode-aware greenfield maintenance routing gate** — `.opencode/docs/AGENT_ROUTING.md`
95. **mode-aware quality evidence gate** — `.opencode/docs/QUALITY.md`
96. **orchestrator mode selection gate** — `skills/opencode-orchestrator/SKILL.md`
97. **artifact planner creative depth gate** — `skills/opencode-artifact-planner/SKILL.md`
98. **fullstack greenfield slice gate** — `skills/opencode-fullstack/SKILL.md`
