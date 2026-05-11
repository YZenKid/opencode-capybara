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

## 10. Harness constrains. Evidence proves.
Preventive controls, mechanical checks, and replayable evidence should be trusted more than verbal confidence.
