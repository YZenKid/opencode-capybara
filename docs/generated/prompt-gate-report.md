# Generated: Prompt Gate Report

Generated inventory of deterministic prompt-gate checks. This file is advisory and must not replace canonical policy in `.opencode/docs/PROMPT_GATES.md`.

- Gate count: 102
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
19. **council language split gate** — `agents/council.md`
20. **canonical execution posture gate** — `.opencode/docs/AGENT_ROUTING.md`
21. **canonical planner invocation gate** — `.opencode/docs/AGENT_ROUTING.md`
22. **mcp state terminology gate** — `.opencode/docs/MCP.md`
23. **tool usage mcp state gate** — `.opencode/docs/TOOL_USAGE.md`
24. **agent tool access mcp state gate** — `.opencode/docs/AGENT_TOOL_ACCESS.md`
25. **golden principles finish-first gate** — `.opencode/docs/GOLDEN_PRINCIPLES.md`
26. **quality gate subagent gate** — `agents/quality-gate.md`
27. **redundant build agent removed gate** — `agents/build.md`
28. **redundant general agent removed gate** — `agents/general.md`
29. **skill improver subagent gate** — `agents/skill-improver.md`
30. **skill improver standalone skill gate** — `skills/opencode-skill-improver/SKILL.md`
31. **designer signoff contract** — `skills/opencode-designer/SKILL.md`
32. **designer design-guide contract** — `skills/opencode-designer/SKILL.md`
33. **designer general design readiness gate** — `skills/opencode-designer/SKILL.md`
34. **orchestrator UI hard stop** — `agents/orchestrator.md`
35. **orchestrator general design blueprint hard stop** — `agents/orchestrator.md`
36. **orchestrator auto-commit gate** — `agents/orchestrator.md`
37. **orchestrator standalone parity contract** — `skills/opencode-orchestrator/SKILL.md`
38. **orchestrator standalone general design blueprint gate** — `skills/opencode-orchestrator/SKILL.md`
39. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
40. **quality gate standalone skill** — `skills/opencode-quality-gate/SKILL.md`
41. **redundant build skill removed gate** — `skills/opencode-build/SKILL.md`
42. **redundant general skill removed gate** — `skills/opencode-general/SKILL.md`
43. **fixer skill UI pause gates** — `skills/opencode-fixer/SKILL.md`
44. **ui system architect skill gate** — `skills/opencode-ui-system-architect/SKILL.md`
45. **product architect subagent gate** — `agents/product-architect.md`
46. **saas architect subagent gate** — `agents/saas-architect.md`
47. **ai systems architect subagent gate** — `agents/ai-systems-architect.md`
48. **security privacy reviewer subagent gate** — `agents/security-privacy-reviewer.md`
49. **release engineer subagent gate** — `agents/release-engineer.md`
50. **mobile architect subagent gate** — `agents/mobile-architect.md`
51. **product architect skill gate** — `skills/opencode-product-architect/SKILL.md`
52. **saas architect skill gate** — `skills/opencode-saas-architect/SKILL.md`
53. **ai systems architect skill gate** — `skills/opencode-ai-systems-architect/SKILL.md`
54. **security privacy reviewer skill gate** — `skills/opencode-security-privacy-reviewer/SKILL.md`
55. **release engineer skill gate** — `skills/opencode-release-engineer/SKILL.md`
56. **mobile architect skill gate** — `skills/opencode-mobile-architect/SKILL.md`
57. **conditional domain specialist routing gate** — `agents/orchestrator.md`
58. **orchestrator conditional domain skill gate** — `skills/opencode-orchestrator/SKILL.md`
59. **artifact planner domain advisory gate** — `agents/artifact-planner.md`
60. **artifact planner production blueprint skill gate** — `skills/opencode-artifact-planner/SKILL.md`
61. **global conditional domain specialist gate** — `.opencode/docs/AGENT_ROUTING.md`
62. **readme conditional domain specialist gate** — `README.md`
63. **readme docs system-of-record gate** — `README.md`
64. **tool setup script contract gate** — `package.json`
65. **rtk caveman onboarding docs gate** — `README.md`
66. **rtk opt-in policy gate** — `AGENTS.md`
67. **setup-dev-tools contract gate** — `scripts/setup-dev-tools.mjs`
68. **doctor read-only contract gate** — `scripts/doctor.mjs`
69. **docs integrity contract gate** — `scripts/docs-integrity-check.mjs`
70. **docs index system-of-record gate** — `.opencode/docs/index.md`
71. **harness evals gate** — `.opencode/docs/EVALS.md`
72. **visual asset generator manifest and icon rules** — `agents/visual-asset-generator.md`
73. **visual asset generator standalone manifest rules** — `skills/opencode-visual-asset-generator/SKILL.md`
74. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
75. **skill improver documentation gate** — `README.md`
76. **auto-commit policy readme gate** — `README.md`
77. **explorer agent gate** — `agents/explorer.md`
78. **librarian agent gate** — `agents/librarian.md`
79. **oracle agent gate** — `agents/oracle.md`
80. **designer agent gate** — `agents/designer.md`
81. **fixer agent gate** — `agents/fixer.md`
82. **standalone identity gate** — `README.md`
83. **artifact planner env routing gate** — `agents/artifact-planner.md`
84. **document specialist env routing gate** — `agents/document-specialist.md`
85. **package identity gate** — `package.json`
86. **runtime plugin removal gate** — `opencode.json`
87. **runtime dependency removal gate** — `package.json`
88. **lockfile dependency removal gate** — `package-lock.json`
89. **tui plugin removal gate** — `tui.json`
90. **runtime plugin wording gate** — `README.md`
91. **obsolete bun lockfile removed gate** — `bun.lock`
92. **manual commit message format gate** — `commands/commit-message.md`
93. **retired workflow command removed gate** — `commands/tdd.md`
94. **retired UI workflow command removed gate** — `commands/replicate-ui.md`
95. **retired revamp workflow command removed gate** — `commands/revamp-like.md`
96. **visual parity agent gate** — `agents/visual-parity-auditor.md`
97. **motion specialist agent gate** — `agents/motion-specialist.md`
98. **accessibility reviewer agent gate** — `agents/accessibility-reviewer.md`
99. **ui system architect agent gate** — `agents/ui-system-architect.md`
100. **visual parity skill gate** — `skills/opencode-visual-parity-auditor/SKILL.md`
101. **motion specialist skill gate** — `skills/opencode-motion-specialist/SKILL.md`
102. **accessibility reviewer skill gate** — `skills/opencode-accessibility-reviewer/SKILL.md`
