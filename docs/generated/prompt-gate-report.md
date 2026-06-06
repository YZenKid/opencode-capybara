# Generated: Prompt Gate Report

Generated inventory of deterministic prompt-gate checks. This file is advisory and must not replace canonical policy in `.opencode/docs/PROMPT_GATES.md`.

- Gate count: 122
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
12. **artifact planner plan execution fidelity gate** — `agents/artifact-planner.md`
13. **model routing documentation gate** — `README.md`
14. **artifact planner standalone skill gate** — `skills/opencode-artifact-planner/SKILL.md`
15. **artifact planner skill plan execution fidelity gate** — `skills/opencode-artifact-planner/SKILL.md`
16. **artifact planner language split gate** — `agents/artifact-planner.md`
17. **orchestrator reference depth and anti-slop gate** — `agents/orchestrator.md`
18. **orchestrator plan execution fidelity gate** — `agents/orchestrator.md`
19. **orchestrator requested aesthetic fidelity gate** — `agents/orchestrator.md`
20. **orchestrator skill reference depth and anti-slop gate** — `skills/opencode-orchestrator/SKILL.md`
21. **orchestrator skill plan execution fidelity gate** — `skills/opencode-orchestrator/SKILL.md`
22. **orchestrator skill requested aesthetic fidelity gate** — `skills/opencode-orchestrator/SKILL.md`
23. **routing docs plan execution fidelity gate** — `.opencode/docs/AGENT_ROUTING.md`
24. **quality docs plan compliance evidence gate** — `.opencode/docs/QUALITY.md`
25. **artifact planner reference depth and anti-slop gate** — `agents/artifact-planner.md`
26. **artifact planner material grammar translation gate** — `agents/artifact-planner.md`
27. **artifact planner skill reference depth and anti-slop gate** — `skills/opencode-artifact-planner/SKILL.md`
28. **artifact planner skill material grammar translation gate** — `skills/opencode-artifact-planner/SKILL.md`
29. **designer workflow gate** — `agents/designer.md`
30. **frontend implementation-basis gate** — `agents/frontend.md`
31. **quality gate source-trace gate** — `agents/quality-gate.md`
32. **quality gate remediation worklist gate** — `agents/quality-gate.md`
33. **designer source-pack and anti-generic gate** — `skills/opencode-designer/SKILL.md`
34. **designer material grammar and mechanical UI gates** — `skills/opencode-designer/SKILL.md`
35. **frontend implementation-basis skill gate** — `skills/opencode-frontend/SKILL.md`
36. **frontend style grammar blocker gate** — `skills/opencode-frontend/SKILL.md`
37. **quality gate source-basis skill gate** — `skills/opencode-quality-gate/SKILL.md`
38. **quality gate requested aesthetic mechanical failure gate** — `skills/opencode-quality-gate/SKILL.md`
39. **quality gate remediation worklist skill gate** — `skills/opencode-quality-gate/SKILL.md`
40. **orchestrator primary mode gate** — `agents/orchestrator.md`
41. **orchestrator quality remediation execution gate** — `agents/orchestrator.md`
42. **orchestrator indonesian user-facing policy gate** — `skills/opencode-orchestrator/SKILL.md`
43. **orchestrator planner invocation gate** — `skills/opencode-orchestrator/SKILL.md`
44. **orchestrator delegation threshold skill gate** — `skills/opencode-orchestrator/SKILL.md`
45. **orchestrator document fallback skill gate** — `skills/opencode-orchestrator/SKILL.md`
46. **council language split gate** — `agents/council.md`
47. **canonical execution posture gate** — `.opencode/docs/AGENT_ROUTING.md`
48. **canonical planner invocation gate** — `.opencode/docs/AGENT_ROUTING.md`
49. **orchestrator direct-vs-delegate threshold gate** — `.opencode/docs/AGENT_ROUTING.md`
50. **canonical document fallback routing gate** — `.opencode/docs/AGENT_ROUTING.md`
51. **mcp state terminology gate** — `.opencode/docs/MCP.md`
52. **tool usage mcp state gate** — `.opencode/docs/TOOL_USAGE.md`
53. **agent tool access mcp state gate** — `.opencode/docs/AGENT_TOOL_ACCESS.md`
54. **golden principles finish-first gate** — `.opencode/docs/GOLDEN_PRINCIPLES.md`
55. **quality gate subagent gate** — `agents/quality-gate.md`
56. **redundant build agent removed gate** — `agents/build.md`
57. **redundant general agent removed gate** — `agents/general.md`
58. **skill improver subagent gate** — `agents/skill-improver.md`
59. **skill improver standalone skill gate** — `skills/opencode-skill-improver/SKILL.md`
60. **designer signoff contract** — `skills/opencode-designer/SKILL.md`
61. **designer design-guide contract** — `skills/opencode-designer/SKILL.md`
62. **designer general design readiness gate** — `skills/opencode-designer/SKILL.md`
63. **orchestrator UI hard stop** — `agents/orchestrator.md`
64. **orchestrator general design blueprint hard stop** — `agents/orchestrator.md`
65. **orchestrator auto-commit gate** — `agents/orchestrator.md`
66. **orchestrator standalone parity contract** — `skills/opencode-orchestrator/SKILL.md`
67. **orchestrator standalone general design blueprint gate** — `skills/opencode-orchestrator/SKILL.md`
68. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
69. **quality gate standalone skill** — `skills/opencode-quality-gate/SKILL.md`
70. **redundant build skill removed gate** — `skills/opencode-build/SKILL.md`
71. **redundant general skill removed gate** — `skills/opencode-general/SKILL.md`
72. **fixer skill UI pause gates** — `skills/opencode-fixer/SKILL.md`
73. **unified architect subagent gate** — `agents/architect.md`
74. **unified architect skill gate** — `skills/opencode-architect/SKILL.md`
75. **conditional domain specialist routing gate** — `agents/orchestrator.md`
76. **orchestrator conditional domain skill gate** — `skills/opencode-orchestrator/SKILL.md`
77. **artifact planner domain advisory gate** — `agents/artifact-planner.md`
78. **artifact planner production blueprint skill gate** — `skills/opencode-artifact-planner/SKILL.md`
79. **global conditional domain specialist gate** — `.opencode/docs/AGENT_ROUTING.md`
80. **readme conditional domain specialist gate** — `README.md`
81. **readme docs system-of-record gate** — `README.md`
82. **tool setup script contract gate** — `package.json`
83. **rtk caveman onboarding docs gate** — `README.md`
84. **rtk opt-in policy gate** — `AGENTS.md`
85. **setup-dev-tools contract gate** — `scripts/setup-dev-tools.mjs`
86. **doctor read-only contract gate** — `scripts/doctor.mjs`
87. **docs integrity contract gate** — `scripts/docs-integrity-check.mjs`
88. **docs index system-of-record gate** — `.opencode/docs/index.md`
89. **harness evals gate** — `.opencode/docs/EVALS.md`
90. **visual asset generator manifest and icon rules** — `agents/visual-asset-generator.md`
91. **visual asset generator standalone manifest rules** — `skills/opencode-visual-asset-generator/SKILL.md`
92. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
93. **skill improver documentation gate** — `README.md`
94. **auto-commit policy readme gate** — `README.md`
95. **explorer agent gate** — `agents/explorer.md`
96. **librarian agent gate** — `agents/librarian.md`
97. **oracle agent gate** — `agents/oracle.md`
98. **designer agent gate** — `agents/designer.md`
99. **fixer agent gate** — `agents/fixer.md`
100. **standalone identity gate** — `README.md`
101. **artifact planner env routing gate** — `agents/artifact-planner.md`
102. **package identity gate** — `package.json`
103. **runtime plugin removal gate** — `opencode.json`
104. **runtime dependency removal gate** — `package.json`
105. **lockfile dependency removal gate** — `package-lock.json`
106. **tui plugin removal gate** — `tui.json`
107. **runtime plugin wording gate** — `README.md`
108. **obsolete bun lockfile removed gate** — `bun.lock`
109. **manual commit message format gate** — `commands/commit-message.md`
110. **retired workflow command removed gate** — `commands/tdd.md`
111. **retired UI workflow command removed gate** — `commands/replicate-ui.md`
112. **retired revamp workflow command removed gate** — `commands/revamp-like.md`
113. **quality-gate merged review lanes gate** — `skills/opencode-quality-gate/SKILL.md`
114. **mode-aware greenfield maintenance routing gate** — `.opencode/docs/AGENT_ROUTING.md`
115. **mode-aware quality evidence gate** — `.opencode/docs/QUALITY.md`
116. **orchestrator mode selection gate** — `skills/opencode-orchestrator/SKILL.md`
117. **artifact planner creative depth gate** — `skills/opencode-artifact-planner/SKILL.md`
118. **fullstack greenfield slice gate** — `skills/opencode-fullstack/SKILL.md`
119. **orchestrator quality remediation skill gate** — `skills/opencode-orchestrator/SKILL.md`
120. **quality docs remediation worklist gate** — `.opencode/docs/QUALITY.md`
121. **ui slop package script wiring gate** — `package.json`
122. **ui slop quality contract gate** — `.opencode/docs/QUALITY.md`
