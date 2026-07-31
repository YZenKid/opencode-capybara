# Validation, Memory, and Commit

Read this before factual claims, done claims, memory writes, or commits.

## Verify-before-claim

- No assertion without verification for code, runtime, environment, dependency, config, or external service behavior.
- Use tool output or subagent report from same response chain.
- Do not claim a file, service, or package state without checking it.

## Functional evidence rule

- Mechanical checks alone are not enough for strong completion claims.
- For app, release, API, or PWA work, run runtime verification when available and save output under `.opencode/evidence/<task-id>/`.

## Stack-drift rule

- If implemented stack, API, or asset format diverges materially from plan or project docs, resolve or escalate before completion.

## Project Memory Finalization Gate

- Before final summary for non-trivial work, persist a project-local memory entry through the wrapper.
- If finalize fails, surface failure and do not mark task done until memory write succeeds or user is informed.

## Commit posture

- Auto-commit default is ON for local commits only.
- Never push automatically.
- Never stage secrets, `.env`, unrelated untracked files, or generated/vendor files unless explicitly approved.

## Trigger phrases to preserve

- verify-before-claim
- Functional evidence rule
- Project Memory Finalization Gate
- auto-commit
- never push automatically
- stack-drift
