# Generated: Prompt Gate Report

Generated inventory of deterministic prompt-gate checks. This file is advisory and must not replace canonical policy in `.opencode/docs/PROMPT_GATES.md`.

- Gate count: 132
- Unique files covered: 48
- Primary implementation: `scripts/prompt-gate-regression.mjs`

## Commands referenced
- `npm run test:prompt-gates`
- `npm run check:docs`
- `npm run check:agents`
- `npm run check:skills`
- `npm run check:evidence`
- `npm run check:verify-claim`
- `npm run check:verify-claim:strict`
- `npm run check:rules-source`
- `npm run init:rules-harmonize`
- `npm run init:rules-harmonize:forward-all`
- `npm run init:stack-suggest`
- `npm run check:session-trace <transcript>`
- `npm run check:template-source`
- `npm run check:legal-source`
- `npm run check:handoff`
- `npm run check:handoff:plan`
- `npm run test:delegation-log`
- `npm run test:plan-compliance`
- `npm run test:session-trace-strict`
- `npm run test:backup-cleanup`
- `npm run cleanup:backups:scan|trash|purge|apply`
- `npm run docs:generate:check`
- `npm run test:graphify-wrapper-path`
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
14. **agent architecture selection gate** — `opencode.json`
15. **agents toc and docs system-of-record gate** — `AGENTS.md`
16. **agents non-negotiable rules gate** — `AGENTS.md`
17. **agents harness posture gate** — `AGENTS.md`
18. **agents planner invocation expectation gate** — `AGENTS.md`
19. **agents risk trigger gate** — `AGENTS.md`
20. **artifact planner design readiness gate** — `agents/artifact-planner.md`
21. **artifact planner plan execution fidelity gate** — `agents/artifact-planner.md`
22. **model routing documentation gate** — `README.md`
23. **artifact planner standalone skill gate** — `skills/opencode-artifact-planner/SKILL.md`
24. **artifact planner skill plan execution fidelity gate** — `skills/opencode-artifact-planner/SKILL.md`
25. **artifact planner language split gate** — `agents/artifact-planner.md`
26. **orchestrator reference depth and anti-slop gate** — `agents/orchestrator.md`
27. **orchestrator plan execution fidelity gate** — `agents/orchestrator.md`
28. **orchestrator requested aesthetic fidelity gate** — `agents/orchestrator.md`
29. **orchestrator skill reference depth and anti-slop gate** — `skills/opencode-orchestrator/SKILL.md`
30. **orchestrator skill plan execution fidelity gate** — `skills/opencode-orchestrator/SKILL.md`
31. **orchestrator skill requested aesthetic fidelity gate** — `skills/opencode-orchestrator/SKILL.md`
32. **routing docs plan execution fidelity gate** — `.opencode/docs/AGENT_ROUTING.md`
33. **quality docs plan compliance evidence gate** — `.opencode/docs/QUALITY.md`
34. **artifact planner reference depth and anti-slop gate** — `agents/artifact-planner.md`
35. **artifact planner material grammar translation gate** — `agents/artifact-planner.md`
36. **artifact planner skill reference depth and anti-slop gate** — `skills/opencode-artifact-planner/SKILL.md`
37. **artifact planner skill material grammar translation gate** — `skills/opencode-artifact-planner/SKILL.md`
38. **designer workflow gate** — `agents/designer.md`
39. **quality gate source-trace gate** — `agents/quality-gate.md`
40. **quality gate remediation worklist gate** — `agents/quality-gate.md`
41. **designer source-pack and anti-generic gate** — `skills/opencode-designer/SKILL.md`
42. **designer material grammar and mechanical UI gates** — `skills/opencode-designer/SKILL.md`
43. **frontend implementation-basis skill gate** — `skills/opencode-frontend/SKILL.md`
44. **frontend style grammar blocker gate** — `skills/opencode-frontend/SKILL.md`
45. **quality gate source-basis skill gate** — `skills/opencode-quality-gate/SKILL.md`
46. **quality gate requested aesthetic mechanical failure gate** — `skills/opencode-quality-gate/SKILL.md`
47. **quality gate remediation worklist skill gate** — `skills/opencode-quality-gate/SKILL.md`
48. **orchestrator primary mode gate** — `agents/orchestrator.md`
49. **orchestrator quality remediation execution gate** — `agents/orchestrator.md`
50. **orchestrator indonesian user-facing policy gate** — `skills/opencode-orchestrator/SKILL.md`
51. **orchestrator planner invocation gate** — `skills/opencode-orchestrator/SKILL.md`
52. **orchestrator delegation threshold skill gate** — `skills/opencode-orchestrator/SKILL.md`
53. **orchestrator document fallback skill gate** — `skills/opencode-orchestrator/SKILL.md`
54. **canonical execution posture gate** — `.opencode/docs/AGENT_ROUTING.md`
55. **canonical planner invocation gate** — `.opencode/docs/AGENT_ROUTING.md`
56. **orchestrator direct-vs-delegate threshold gate** — `.opencode/docs/AGENT_ROUTING.md`
57. **canonical document fallback routing gate** — `.opencode/docs/AGENT_ROUTING.md`
58. **mcp state terminology gate** — `.opencode/docs/MCP.md`
59. **tool usage mcp state gate** — `.opencode/docs/TOOL_USAGE.md`
60. **agent tool access mcp state gate** — `.opencode/docs/AGENT_TOOL_ACCESS.md`
61. **golden principles finish-first gate** — `.opencode/docs/GOLDEN_PRINCIPLES.md`
62. **quality gate subagent gate** — `agents/quality-gate.md`
63. **redundant build agent removed gate** — `agents/build.md`
64. **redundant general agent removed gate** — `agents/general.md`
65. **skill improver standalone skill gate** — `skills/opencode-skill-improver/SKILL.md`
66. **designer signoff contract** — `skills/opencode-designer/SKILL.md`
67. **designer design-guide contract** — `skills/opencode-designer/SKILL.md`
68. **designer general design readiness gate** — `skills/opencode-designer/SKILL.md`
69. **orchestrator UI hard stop** — `agents/orchestrator.md`
70. **orchestrator general design blueprint hard stop** — `agents/orchestrator.md`
71. **orchestrator auto-commit gate** — `agents/orchestrator.md`
72. **orchestrator standalone parity contract** — `skills/opencode-orchestrator/SKILL.md`
73. **orchestrator standalone general design blueprint gate** — `skills/opencode-orchestrator/SKILL.md`
74. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
75. **quality gate standalone skill** — `skills/opencode-quality-gate/SKILL.md`
76. **redundant build skill removed gate** — `skills/opencode-build/SKILL.md`
77. **redundant general skill removed gate** — `skills/opencode-general/SKILL.md`
78. **fixer skill UI pause gates** — `skills/opencode-fixer/SKILL.md`
79. **unified architect subagent gate** — `agents/architect.md`
80. **unified architect skill gate** — `skills/opencode-architect/SKILL.md`
81. **conditional domain specialist routing gate** — `agents/orchestrator.md`
82. **orchestrator conditional domain skill gate** — `skills/opencode-orchestrator/SKILL.md`
83. **artifact planner domain advisory gate** — `agents/artifact-planner.md`
84. **artifact planner production blueprint skill gate** — `skills/opencode-artifact-planner/SKILL.md`
85. **global conditional domain specialist gate** — `.opencode/docs/AGENT_ROUTING.md`
86. **readme conditional domain specialist gate** — `README.md`
87. **readme docs system-of-record gate** — `README.md`
88. **tool setup script contract gate** — `package.json`
89. **support tooling onboarding docs gate** — `README.md`
90. **support tooling policy gate** — `AGENTS.md`
91. **setup-dev-tools contract gate** — `scripts/setup-dev-tools.mjs`
92. **doctor read-only contract gate** — `scripts/doctor.mjs`
93. **docs integrity contract gate** — `scripts/docs-integrity-check.mjs`
94. **docs index system-of-record gate** — `.opencode/docs/index.md`
95. **harness evals gate** — `.opencode/docs/EVALS.md`
96. **visual asset generator standalone manifest rules** — `skills/opencode-visual-asset-generator/SKILL.md`
97. **orchestrator auto-commit skill gate** — `skills/opencode-orchestrator/SKILL.md`
98. **skill improver documentation gate** — `README.md`
99. **auto-commit policy readme gate** — `README.md`
100. **explorer agent gate** — `agents/explorer.md`
101. **librarian agent gate** — `agents/librarian.md`
102. **oracle agent gate** — `agents/oracle.md`
103. **designer agent gate** — `agents/designer.md`
104. **fixer agent gate** — `agents/fixer.md`
105. **standalone identity gate** — `README.md`
106. **artifact planner env routing gate** — `agents/artifact-planner.md`
107. **package identity gate** — `package.json`
108. **runtime plugin preset safety gate** — `opencode.json`
109. **package dependency identity gate** — `package.json`
110. **lockfile dependency identity gate** — `package-lock.json`
111. **tui plugin removal gate** — `tui.json`
112. **runtime plugin wording gate** — `README.md`
113. **obsolete bun lockfile removed gate** — `bun.lock`
114. **retired workflow command removed gate** — `commands/tdd.md`
115. **retired UI workflow command removed gate** — `commands/replicate-ui.md`
116. **retired revamp workflow command removed gate** — `commands/revamp-like.md`
117. **quality-gate merged review lanes gate** — `skills/opencode-quality-gate/SKILL.md`
118. **mode-aware greenfield maintenance routing gate** — `.opencode/docs/AGENT_ROUTING.md`
119. **mode-aware quality evidence gate** — `.opencode/docs/QUALITY.md`
120. **orchestrator mode selection gate** — `skills/opencode-orchestrator/SKILL.md`
121. **artifact planner creative depth gate** — `skills/opencode-artifact-planner/SKILL.md`
122. **fullstack greenfield slice gate** — `skills/opencode-fullstack/SKILL.md`
123. **orchestrator quality remediation skill gate** — `skills/opencode-orchestrator/SKILL.md`
124. **quality docs remediation worklist gate** — `.opencode/docs/QUALITY.md`
125. **ui slop package script wiring gate** — `package.json`
126. **ui slop quality contract gate** — `.opencode/docs/QUALITY.md`
127. **plan reviewer skill phase 3 gate** — `skills/opencode-plan-reviewer/SKILL.md`
128. **plan validation package script wiring gate** — `package.json`
129. **shared policies document gate** — `.opencode/docs/SHARED_POLICIES.md`
130. **orchestrator references shared policies gate** — `agents/orchestrator.md`
131. **designer references shared policies gate** — `agents/designer.md`
132. **quality-gate references shared policies gate** — `agents/quality-gate.md`
