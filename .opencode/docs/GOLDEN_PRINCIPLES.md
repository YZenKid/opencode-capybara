# Golden Principles

## 1. Calm orchestration over aggressive automation
Choose the safe, clear, and reversible path over fast but unverified action.

## 2. Evidence before confidence
Final summaries must include evidence: tests, command output, screenshots, lint, diff, or an explicit risk note.

## 3. Boundaries are product features
Each agent has a clear scope. Implementer, reviewer, planner, and gatekeeper roles must not be mixed casually.

## 4. No hidden side effects
Do not allow hidden install hooks, silently enabled risky rewriting, or invisible network actions.

## 5. Prompt rules must be testable
If a rule matters, it should have a regression case, lint rule, script, or checklist.

## 6. Prefer small enforceable rules over long prose
Long instructions should be promoted into a script, gate, template, or skill contract.

## 7. Repo-local knowledge wins
If an important decision exists only in chat, an issue, or someone’s head, agents should treat that knowledge as unstable until it is documented in the repo.

## 8. Cleanup is continuous
AI slop and prompt drift should be cleaned continuously through small targeted changes.

## 9. Humans steer. Agents execute.
Humans set intent, priorities, acceptance criteria, and product decisions. Agents execute within harness boundaries.

## 10. Finish first, ask at the edge
For execution requests, agents should complete as much work as possible first. Non-blocking questions, minor preferences, and residual decisions are deferred to the end; mid-run interruption is reserved for truly material, irreversible, or high-risk blockers.

## 11. Harness constrains. Evidence proves.
Preventive controls, mechanical checks, and replayable evidence should be trusted more than verbal confidence.

## 12. Compression follows the approved toolchain
If token compression or context packing is needed, use RTK and Caveman together according to the repo-approved workflow. Do not create a parallel local compression path or treat RTK and Caveman as either/or choices outside the official setup, docs, and gates.

## 13. One prose language per context
Default operational prose, instructions, and agent-internal coordination should stay in English. Use Bahasa Indonesia only for artifact-planner plan output and for final user-facing conclusions, unless the user explicitly requests a different language policy. Avoid mixed English/Indonesian prose blocks outside technical literals.
