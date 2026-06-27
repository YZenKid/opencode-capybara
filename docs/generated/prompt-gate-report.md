# Generated: Prompt Gate Report

Generated inventory of deterministic prompt-gate checks. This file is advisory and must not replace canonical policy in `.opencode/docs/PROMPT_GATES.md`.

- Gate count: 138
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
7. **active lane refresh tool usage gate** — `.opencode/docs/TOOL_USAGE.md`
8. **active lane refresh boundary gate** — `.opencode/docs/AGENT_TOOL_ACCESS.md`
9. **orchestrator active lane refresh gate** — `agents/orchestrator.md`
10. **artifact planner handoff reset gate** — `agents/artifact-planner.md`
11. **orchestrator skill active lane workflow gate** — `skills/opencode-orchestrator/SKILL.md`
12. **artifact planner skill handoff reset gate** — `skills/opencode-artifact-planner/SKILL.md`
13. **framework manual artifact quality gate** — `.opencode/docs/QUALITY.md`
14. **local council subagent gate** — `agents/council.md`
15. **agent architecture selection gate** — `opencode.json`
16. **agents toc and docs system-of-record gate** — `AGENTS.md`
17. **agents non-negotiable rules gate** — `AGENTS.md`
18. **agents harness posture gate** — `AGENTS.md`
19. **agents planner invocation expectation gate** — `AGENTS.md`
20. **agents risk trigger gate** — `AGENTS.md`
21. **artifact planner design readiness gate** — `agents/artifact-planner.md`
22. **artifact planner plan execution fidelity gate** — `agents/artifact-planner.md`
23. **model routing documentation gate** — `README.md`
24. **artifact planner standalone skill gate** — `skills/opencode-artifact-planner/SKILL.md`
25. **artifact planner skill plan execution fidelity gate** — `skills/opencode-artifact-planner/SKILL.md`
26. **artifact planner language split gate** — `agents/artifact-planner.md`
27. **orchestrator reference depth and anti-slop gate** — `agents/orchestrator.md`
28. **orchestrator plan execution fidelity gate** — `agents/orchestrator.md`
29. **orchestrator requested aesthetic fidelity gate** — `agents/orchestrator.md`
30. **orchestrator skill reference depth and anti-slop gate** — `skills/opencode-orchestrator/SKILL.md`
31. **orchestrator skill plan execution fidelity gate** — `skills/opencode-orchestrator/SKILL.md`
32. **orchestrator skill requested aesthetic fidelity gate** — `skills/opencode-orchestrator/SKILL.md`
33. **routing docs plan execution fidelity gate** — `.opencode/docs/AGENT_ROUTING.md`
34. **quality docs plan compliance evidence gate** — `.opencode/docs/QUALITY.md`
35. **artifact planner reference depth and anti-slop gate** — `agents/artifact-planner.md`
36. **artifact planner material grammar translation gate** — `agents/artifact-planner.md`
37. **artifact planner skill reference depth and anti-slop gate** — `skills/opencode-artifact-planner/SKILL.md`
38. **artifact planner skill material grammar translation gate** — `skills/opencode-artifact-planner/SKILL.md`
39. **designer workflow gate** — `agents/designer.md`
40. **frontend implementation-basis gate** — `agents/frontend.md`
41. **quality gate source-trace gate** — `agents/quality-gate.md`
42. **quality gate remediation worklist gate** — `agents/quality-gate.md`
43. **designer source-pack and anti-generic gate** — `skills/opencode-designer/SKILL.md`
44. **designer material grammar and mechanical UI gates** — `skills/opencode-designer/SKILL.md`
45. **frontend implementation-basis skill gate** — `skills/opencode-frontend/SKILL.md`
46. **frontend style grammar blocker gate** — `skills/opencode-frontend/SKILL.md`
47. **quality gate source-basis skill gate** — `skills/opencode-quality-gate/SKILL.md`
48. **quality gate requested aesthetic mechanical failure gate** — `skills/opencode-quality-gate/SKILL.md`
49. **quality gate remediation worklist skill gate** — `skills/opencode-quality-gate/SKILL.md`
50. **orchestrator primary mode gate** — `agents/orchestrator.md`
51. **orchestrator quality remediation execution gate** — `agents/orchestrator.md`
52. **orchestrator indonesian user-facing policy gate** — `skills/opencode-orchestrator/SKILL.md`
53. **orchestrator planner invocation gate** — `skills/opencode-orchestrator/SKILL.md`
54. **orchestrator delegation threshold skill gate** — `skills/opencode-orchestrator/SKILL.md`
55. **orchestrator document fallback skill gate** — `skills/opencode-orchestrator/SKILL.md`
56. **council language split gate** — `agents/council.md`
57. **canonical execution posture gate** — `.opencode/docs/AGENT_ROUTING.md`
58. **canonical planner invocation gate** — `.opencode/docs/AGENT_ROUTING.md`
59. **orchestrator direct-vs-delegate threshold gate** — `.opencode/docs/AGENT_ROUTING.md`
60. **canonical document fallback routing gate** — `.opencode/docs/AGENT_ROUTING.md`
61. **mcp state terminology gate** — `.opencode/docs/MCP.md`
62. **tool usage mcp state gate** — `.opencode/docs/TOOL_USAGE.md`
63. **agent tool access mcp state gate** — `.opencode/docs/AGENT_TOOL_ACCESS.md`
64. **golden principles finish-first gate** — `.opencode/docs/GOLDEN_PRINCIPLES.md`
65. **quality gate subagent gate** — `agents/quality-gate.md`
66. **redundant build agent removed gate** — `agents/build.md`
67. **redundant general agent removed gate** — `agents/general.md`
68. **skill improver subagent gate** — `agents/skill-improver.md`
69. **skill improver standalone skill gate** — `skills/opencode-skill-improver/SKILL.md`
70. **designer signoff contract** — `skills/opencode-designer/SKILL.md`
71. **designer design-guide contract** — `skills/opencode-designer/SKILL.md`
72. **designer general design readiness gate** — `skills/opencode-designer/SKILL.md`
73. **orchestrator UI hard stop** — `agents/orchestrator.md`
74. **orchestrator general design blueprint hard stop** — `agents/orchestrator.md`
75. **orchestrator auto-commit gate** — `agents/orchestrator.md`
76. **orchestrator standalone parity contract** — `skills/opencode-orchestrator/SKILL.md`
77. **orchestrator standalone general design blueprint gate** — `skills/opencode-orchestrator/SKILL.md`
78. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
79. **quality gate standalone skill** — `skills/opencode-quality-gate/SKILL.md`
80. **redundant build skill removed gate** — `skills/opencode-build/SKILL.md`
81. **redundant general skill removed gate** — `skills/opencode-general/SKILL.md`
82. **fixer skill UI pause gates** — `skills/opencode-fixer/SKILL.md`
83. **unified architect subagent gate** — `agents/architect.md`
84. **unified architect skill gate** — `skills/opencode-architect/SKILL.md`
85. **conditional domain specialist routing gate** — `agents/orchestrator.md`
86. **orchestrator conditional domain skill gate** — `skills/opencode-orchestrator/SKILL.md`
87. **artifact planner domain advisory gate** — `agents/artifact-planner.md`
88. **artifact planner production blueprint skill gate** — `skills/opencode-artifact-planner/SKILL.md`
89. **global conditional domain specialist gate** — `.opencode/docs/AGENT_ROUTING.md`
90. **readme conditional domain specialist gate** — `README.md`
91. **readme docs system-of-record gate** — `README.md`
92. **tool setup script contract gate** — `package.json`
93. **rtk caveman onboarding docs gate** — `README.md`
94. **rtk opt-in policy gate** — `AGENTS.md`
95. **setup-dev-tools contract gate** — `scripts/setup-dev-tools.mjs`
96. **doctor read-only contract gate** — `scripts/doctor.mjs`
97. **docs integrity contract gate** — `scripts/docs-integrity-check.mjs`
98. **docs index system-of-record gate** — `.opencode/docs/index.md`
99. **harness evals gate** — `.opencode/docs/EVALS.md`
100. **visual asset generator manifest and icon rules** — `agents/visual-asset-generator.md`
101. **visual asset generator standalone manifest rules** — `skills/opencode-visual-asset-generator/SKILL.md`
102. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
103. **skill improver documentation gate** — `README.md`
104. **auto-commit policy readme gate** — `README.md`
105. **explorer agent gate** — `agents/explorer.md`
106. **librarian agent gate** — `agents/librarian.md`
107. **oracle agent gate** — `agents/oracle.md`
108. **designer agent gate** — `agents/designer.md`
109. **fixer agent gate** — `agents/fixer.md`
110. **standalone identity gate** — `README.md`
111. **artifact planner env routing gate** — `agents/artifact-planner.md`
112. **package identity gate** — `package.json`
113. **runtime plugin preset safety gate** — `opencode.json`
114. **package dependency identity gate** — `package.json`
115. **lockfile dependency identity gate** — `package-lock.json`
116. **tui plugin removal gate** — `tui.json`
117. **runtime plugin wording gate** — `README.md`
118. **obsolete bun lockfile removed gate** — `bun.lock`
119. **retired workflow command removed gate** — `commands/tdd.md`
120. **retired UI workflow command removed gate** — `commands/replicate-ui.md`
121. **retired revamp workflow command removed gate** — `commands/revamp-like.md`
122. **quality-gate merged review lanes gate** — `skills/opencode-quality-gate/SKILL.md`
123. **mode-aware greenfield maintenance routing gate** — `.opencode/docs/AGENT_ROUTING.md`
124. **mode-aware quality evidence gate** — `.opencode/docs/QUALITY.md`
125. **orchestrator mode selection gate** — `skills/opencode-orchestrator/SKILL.md`
126. **artifact planner creative depth gate** — `skills/opencode-artifact-planner/SKILL.md`
127. **fullstack greenfield slice gate** — `skills/opencode-fullstack/SKILL.md`
128. **orchestrator quality remediation skill gate** — `skills/opencode-orchestrator/SKILL.md`
129. **quality docs remediation worklist gate** — `.opencode/docs/QUALITY.md`
130. **ui slop package script wiring gate** — `package.json`
131. **ui slop quality contract gate** — `.opencode/docs/QUALITY.md`
132. **plan reviewer phase 3 gate** — `agents/plan-reviewer.md`
133. **plan reviewer skill phase 3 gate** — `skills/opencode-plan-reviewer/SKILL.md`
134. **plan validation package script wiring gate** — `package.json`
135. **shared policies document gate** — `.opencode/docs/SHARED_POLICIES.md`
136. **orchestrator references shared policies gate** — `agents/orchestrator.md`
137. **designer references shared policies gate** — `agents/designer.md`
138. **quality-gate references shared policies gate** — `agents/quality-gate.md`
