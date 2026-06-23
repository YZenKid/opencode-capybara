# Generated: Prompt Gate Report

Generated inventory of deterministic prompt-gate checks. This file is advisory and must not replace canonical policy in `.opencode/docs/PROMPT_GATES.md`.

- Gate count: 132
- Unique files covered: 53
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
2. **project consolidated harness/design init command gate** — `commands/init-harness.md`
3. **project harness init command gate** — `commands/init-harness.md`
4. **project framework playbook default gate** — `commands/init-harness.md`
5. **framework playbook routing gate** — `.opencode/docs/AGENT_ROUTING.md`
6. **framework generator-first tool usage gate** — `.opencode/docs/TOOL_USAGE.md`
7. **framework manual artifact quality gate** — `.opencode/docs/QUALITY.md`
8. **local council subagent gate** — `agents/council.md`
9. **agent architecture selection gate** — `opencode.json`
10. **agents toc and docs system-of-record gate** — `AGENTS.md`
11. **agents non-negotiable rules gate** — `AGENTS.md`
12. **agents harness posture gate** — `AGENTS.md`
13. **agents planner invocation expectation gate** — `AGENTS.md`
14. **agents risk trigger gate** — `AGENTS.md`
15. **artifact planner design readiness gate** — `agents/artifact-planner.md`
16. **artifact planner plan execution fidelity gate** — `agents/artifact-planner.md`
17. **model routing documentation gate** — `README.md`
18. **artifact planner standalone skill gate** — `skills/opencode-artifact-planner/SKILL.md`
19. **artifact planner skill plan execution fidelity gate** — `skills/opencode-artifact-planner/SKILL.md`
20. **artifact planner language split gate** — `agents/artifact-planner.md`
21. **orchestrator reference depth and anti-slop gate** — `agents/orchestrator.md`
22. **orchestrator plan execution fidelity gate** — `agents/orchestrator.md`
23. **orchestrator requested aesthetic fidelity gate** — `agents/orchestrator.md`
24. **orchestrator skill reference depth and anti-slop gate** — `skills/opencode-orchestrator/SKILL.md`
25. **orchestrator skill plan execution fidelity gate** — `skills/opencode-orchestrator/SKILL.md`
26. **orchestrator skill requested aesthetic fidelity gate** — `skills/opencode-orchestrator/SKILL.md`
27. **routing docs plan execution fidelity gate** — `.opencode/docs/AGENT_ROUTING.md`
28. **quality docs plan compliance evidence gate** — `.opencode/docs/QUALITY.md`
29. **artifact planner reference depth and anti-slop gate** — `agents/artifact-planner.md`
30. **artifact planner material grammar translation gate** — `agents/artifact-planner.md`
31. **artifact planner skill reference depth and anti-slop gate** — `skills/opencode-artifact-planner/SKILL.md`
32. **artifact planner skill material grammar translation gate** — `skills/opencode-artifact-planner/SKILL.md`
33. **designer workflow gate** — `agents/designer.md`
34. **frontend implementation-basis gate** — `agents/frontend.md`
35. **quality gate source-trace gate** — `agents/quality-gate.md`
36. **quality gate remediation worklist gate** — `agents/quality-gate.md`
37. **designer source-pack and anti-generic gate** — `skills/opencode-designer/SKILL.md`
38. **designer material grammar and mechanical UI gates** — `skills/opencode-designer/SKILL.md`
39. **frontend implementation-basis skill gate** — `skills/opencode-frontend/SKILL.md`
40. **frontend style grammar blocker gate** — `skills/opencode-frontend/SKILL.md`
41. **quality gate source-basis skill gate** — `skills/opencode-quality-gate/SKILL.md`
42. **quality gate requested aesthetic mechanical failure gate** — `skills/opencode-quality-gate/SKILL.md`
43. **quality gate remediation worklist skill gate** — `skills/opencode-quality-gate/SKILL.md`
44. **orchestrator primary mode gate** — `agents/orchestrator.md`
45. **orchestrator quality remediation execution gate** — `agents/orchestrator.md`
46. **orchestrator indonesian user-facing policy gate** — `skills/opencode-orchestrator/SKILL.md`
47. **orchestrator planner invocation gate** — `skills/opencode-orchestrator/SKILL.md`
48. **orchestrator delegation threshold skill gate** — `skills/opencode-orchestrator/SKILL.md`
49. **orchestrator document fallback skill gate** — `skills/opencode-orchestrator/SKILL.md`
50. **council language split gate** — `agents/council.md`
51. **canonical execution posture gate** — `.opencode/docs/AGENT_ROUTING.md`
52. **canonical planner invocation gate** — `.opencode/docs/AGENT_ROUTING.md`
53. **orchestrator direct-vs-delegate threshold gate** — `.opencode/docs/AGENT_ROUTING.md`
54. **canonical document fallback routing gate** — `.opencode/docs/AGENT_ROUTING.md`
55. **mcp state terminology gate** — `.opencode/docs/MCP.md`
56. **tool usage mcp state gate** — `.opencode/docs/TOOL_USAGE.md`
57. **agent tool access mcp state gate** — `.opencode/docs/AGENT_TOOL_ACCESS.md`
58. **golden principles finish-first gate** — `.opencode/docs/GOLDEN_PRINCIPLES.md`
59. **quality gate subagent gate** — `agents/quality-gate.md`
60. **redundant build agent removed gate** — `agents/build.md`
61. **redundant general agent removed gate** — `agents/general.md`
62. **skill improver subagent gate** — `agents/skill-improver.md`
63. **skill improver standalone skill gate** — `skills/opencode-skill-improver/SKILL.md`
64. **designer signoff contract** — `skills/opencode-designer/SKILL.md`
65. **designer design-guide contract** — `skills/opencode-designer/SKILL.md`
66. **designer general design readiness gate** — `skills/opencode-designer/SKILL.md`
67. **orchestrator UI hard stop** — `agents/orchestrator.md`
68. **orchestrator general design blueprint hard stop** — `agents/orchestrator.md`
69. **orchestrator auto-commit gate** — `agents/orchestrator.md`
70. **orchestrator standalone parity contract** — `skills/opencode-orchestrator/SKILL.md`
71. **orchestrator standalone general design blueprint gate** — `skills/opencode-orchestrator/SKILL.md`
72. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
73. **quality gate standalone skill** — `skills/opencode-quality-gate/SKILL.md`
74. **redundant build skill removed gate** — `skills/opencode-build/SKILL.md`
75. **redundant general skill removed gate** — `skills/opencode-general/SKILL.md`
76. **fixer skill UI pause gates** — `skills/opencode-fixer/SKILL.md`
77. **unified architect subagent gate** — `agents/architect.md`
78. **unified architect skill gate** — `skills/opencode-architect/SKILL.md`
79. **conditional domain specialist routing gate** — `agents/orchestrator.md`
80. **orchestrator conditional domain skill gate** — `skills/opencode-orchestrator/SKILL.md`
81. **artifact planner domain advisory gate** — `agents/artifact-planner.md`
82. **artifact planner production blueprint skill gate** — `skills/opencode-artifact-planner/SKILL.md`
83. **global conditional domain specialist gate** — `.opencode/docs/AGENT_ROUTING.md`
84. **readme conditional domain specialist gate** — `README.md`
85. **readme docs system-of-record gate** — `README.md`
86. **tool setup script contract gate** — `package.json`
87. **rtk caveman onboarding docs gate** — `README.md`
88. **rtk opt-in policy gate** — `AGENTS.md`
89. **setup-dev-tools contract gate** — `scripts/setup-dev-tools.mjs`
90. **doctor read-only contract gate** — `scripts/doctor.mjs`
91. **docs integrity contract gate** — `scripts/docs-integrity-check.mjs`
92. **docs index system-of-record gate** — `.opencode/docs/index.md`
93. **harness evals gate** — `.opencode/docs/EVALS.md`
94. **visual asset generator manifest and icon rules** — `agents/visual-asset-generator.md`
95. **visual asset generator standalone manifest rules** — `skills/opencode-visual-asset-generator/SKILL.md`
96. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
97. **skill improver documentation gate** — `README.md`
98. **auto-commit policy readme gate** — `README.md`
99. **explorer agent gate** — `agents/explorer.md`
100. **librarian agent gate** — `agents/librarian.md`
101. **oracle agent gate** — `agents/oracle.md`
102. **designer agent gate** — `agents/designer.md`
103. **fixer agent gate** — `agents/fixer.md`
104. **standalone identity gate** — `README.md`
105. **artifact planner env routing gate** — `agents/artifact-planner.md`
106. **package identity gate** — `package.json`
107. **runtime plugin preset safety gate** — `opencode.json`
108. **package dependency identity gate** — `package.json`
109. **lockfile dependency identity gate** — `package-lock.json`
110. **tui plugin removal gate** — `tui.json`
111. **runtime plugin wording gate** — `README.md`
112. **obsolete bun lockfile removed gate** — `bun.lock`
113. **retired workflow command removed gate** — `commands/tdd.md`
114. **retired UI workflow command removed gate** — `commands/replicate-ui.md`
115. **retired revamp workflow command removed gate** — `commands/revamp-like.md`
116. **quality-gate merged review lanes gate** — `skills/opencode-quality-gate/SKILL.md`
117. **mode-aware greenfield maintenance routing gate** — `.opencode/docs/AGENT_ROUTING.md`
118. **mode-aware quality evidence gate** — `.opencode/docs/QUALITY.md`
119. **orchestrator mode selection gate** — `skills/opencode-orchestrator/SKILL.md`
120. **artifact planner creative depth gate** — `skills/opencode-artifact-planner/SKILL.md`
121. **fullstack greenfield slice gate** — `skills/opencode-fullstack/SKILL.md`
122. **orchestrator quality remediation skill gate** — `skills/opencode-orchestrator/SKILL.md`
123. **quality docs remediation worklist gate** — `.opencode/docs/QUALITY.md`
124. **ui slop package script wiring gate** — `package.json`
125. **ui slop quality contract gate** — `.opencode/docs/QUALITY.md`
126. **plan reviewer phase 3 gate** — `agents/plan-reviewer.md`
127. **plan reviewer skill phase 3 gate** — `skills/opencode-plan-reviewer/SKILL.md`
128. **plan validation package script wiring gate** — `package.json`
129. **shared policies document gate** — `.opencode/docs/SHARED_POLICIES.md`
130. **orchestrator references shared policies gate** — `agents/orchestrator.md`
131. **designer references shared policies gate** — `agents/designer.md`
132. **quality-gate references shared policies gate** — `agents/quality-gate.md`
