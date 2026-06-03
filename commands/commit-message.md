---
description: Generate commit message from current git changes
agent: orchestrator
model: 9router/medium
---

Generate a commit message for the current repository changes.

This command is read-only and only provides manual commit-message suggestions. It does not run commits, does not override `@orchestrator` routing/integration, and does not change any orchestrator auto-commit policy.

Arguments from user, if any:

```text
$ARGUMENTS
```

Current git status:

```text
!`git status --short --branch`
```

Staged diff:

```diff
!`git diff --staged --stat && git diff --staged --`
```

Unstaged diff:

```diff
!`git diff --stat && git diff --`
```

Recent commit messages for style reference:

```text
!`git log --oneline -20`
```

Rules:

- Do not run git add, git commit, git push, or any command that mutates the repository.
- Respect current routing docs: `@orchestrator`/`opencode-orchestrator` owns routing and integration; this command only analyzes the diff text already shown here.
- Analyze staged changes first. If there are staged changes, generate the message for staged changes only.
- If there are no staged changes, generate the message for all unstaged tracked changes and clearly say that nothing is staged.
- If there are untracked files shown by git status, mention that they are not included in the diff unless they are staged.
- Follow the repository's recent commit message style when it is clear.
- If the repo appears to use Conventional Commits, prefer that format.
- If auto-commit guidance or repo style suggests a multi-line message, output a concise subject line followed by a bullet-point body that summarizes the most important changes.
- Keep prose in English.
- Keep commit messages themselves in English unless the repository history clearly uses Indonesian.
- Focus on why the change exists, not just what files changed.
- Warn if the diff appears to include secrets, credentials, `.env`, tokens, or generated/vendor files.
- Warn that prompt/config/security-sensitive changes should get `@quality-gate` review before any non-trivial completion or release claim.

Output format:

```text
Status: <staged|unstaged-only|no-changes|warning>

Recommended:
<single best commit message>

Alternatives:
1. <alternative concise message>
2. <alternative conventional commit message if useful>
3. <alternative more descriptive message if useful>

Notes:
- <brief notes about scope/style/warnings>
```

If there are no changes, respond only:

```text
Status: no-changes

There are no changes to generate a commit message for.
```
