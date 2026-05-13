# Generated: Prompt Gate Report

Generated inventory of deterministic prompt-gate checks. This file is advisory and must not replace canonical policy in `.opencode/docs/PROMPT_GATES.md`.

- Gate count: historical snapshot; regenerate with `npm run test:prompt-gates` for current inventory
- Unique files covered: 67
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
46. **ui system architect skill gate** — `skills/opencode-ui-system-architect/SKILL.md`
47. **product systems architect subagent gate** — `agents/product-systems-architect.md`
48. **ai systems architect subagent gate** — `agents/ai-systems-architect.md`
49. **security risk reviewer subagent gate** — `agents/security-risk-reviewer.md`
50. **platform architect subagent gate** — `agents/platform-architect.md`
51. **product systems architect skill gate** — `skills/opencode-product-systems-architect/SKILL.md`
52. **ai systems architect skill gate** — `skills/opencode-ai-systems-architect/SKILL.md`
53. **security risk reviewer skill gate** — `skills/opencode-security-risk-reviewer/SKILL.md`
54. **platform architect skill gate** — `skills/opencode-platform-architect/SKILL.md`
55. **conditional domain specialist routing gate** — `agents/orchestrator.md`
56. **orchestrator conditional domain skill gate** — `skills/opencode-orchestrator/SKILL.md`
61. **artifact planner domain advisory gate** — `agents/artifact-planner.md`
62. **artifact planner production blueprint skill gate** — `skills/opencode-artifact-planner/SKILL.md`
63. **global conditional domain specialist gate** — `.opencode/docs/AGENT_ROUTING.md`
64. **readme conditional domain specialist gate** — `README.md`
65. **readme docs system-of-record gate** — `README.md`
66. **tool setup script contract gate** — `package.json`
67. **rtk caveman onboarding docs gate** — `README.md`
68. **rtk opt-in policy gate** — `AGENTS.md`
69. **setup-dev-tools contract gate** — `scripts/setup-dev-tools.mjs`
70. **doctor read-only contract gate** — `scripts/doctor.mjs`
71. **docs integrity contract gate** — `scripts/docs-integrity-check.mjs`
72. **docs index system-of-record gate** — `.opencode/docs/index.md`
73. **harness evals gate** — `.opencode/docs/EVALS.md`
74. **visual asset generator manifest and icon rules** — `agents/visual-asset-generator.md`
75. **visual asset generator standalone manifest rules** — `skills/opencode-visual-asset-generator/SKILL.md`
76. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
77. **skill improver documentation gate** — `README.md`
78. **auto-commit policy readme gate** — `README.md`
79. **explorer agent gate** — `agents/explorer.md`
80. **librarian agent gate** — `agents/librarian.md`
81. **oracle agent gate** — `agents/oracle.md`
82. **designer agent gate** — `agents/designer.md`
83. **fixer agent gate** — `agents/fixer.md`
84. **standalone identity gate** — `README.md`
85. **artifact planner env routing gate** — `agents/artifact-planner.md`
86. **document specialist env routing gate** — `agents/document-specialist.md`
87. **package identity gate** — `package.json`
88. **runtime plugin removal gate** — `opencode.json`
89. **runtime dependency removal gate** — `package.json`
90. **lockfile dependency removal gate** — `package-lock.json`
91. **tui plugin removal gate** — `tui.json`
92. **runtime plugin wording gate** — `README.md`
93. **obsolete bun lockfile removed gate** — `bun.lock`
94. **manual commit message format gate** — `commands/commit-message.md`
95. **retired workflow command removed gate** — `commands/tdd.md`
96. **retired UI workflow command removed gate** — `commands/replicate-ui.md`
97. **retired revamp workflow command removed gate** — `commands/revamp-like.md`
98. **visual parity agent gate** — `agents/visual-parity-auditor.md`
99. **motion specialist agent gate** — `agents/motion-specialist.md`
100. **accessibility reviewer agent gate** — `agents/accessibility-reviewer.md`
101. **ui system architect agent gate** — `agents/ui-system-architect.md`
102. **visual parity skill gate** — `skills/opencode-visual-parity-auditor/SKILL.md`
103. **motion specialist skill gate** — `skills/opencode-motion-specialist/SKILL.md`
104. **accessibility reviewer skill gate** — `skills/opencode-accessibility-reviewer/SKILL.md`
