# Project Knowledge Memory Template

Use when a task produces reusable knowledge for future project work.

## Storage

Knowledge is per-project at `.opencode/memory/knowledge.json`.

## Save workflow

After a task completes (or when a useful insight appears during work), run:

```bash
python3 ~/.config/opencode/scripts/project-memory.py --save \
  --task <task-id> \
  --category <category> \
  --lesson "concise reusable lesson" \
  --context "what triggered this" \
  --tags "tag1,tag2,tag3"
```

## Categories

- `pitfall`: something that failed and how to avoid it
- `pattern`: a reusable implementation or design pattern
- `decision`: an architectural/product decision and its rationale
- `workaround`: temporary fix with conditions
- `architecture`: structural approach for the project
- `testing`: testing strategy, fixture, or mock pattern
- `deployment`: deploy, env, or operational note
- `performance`: perf finding or optimization
- `security`: security/auth/privacy note
- `ux`: UX/usability/a11y learning

## Retrieval workflows

### Before planning
```bash
python3 ~/.config/opencode/scripts/project-memory.py --load \
  --context "build PWA with offline audio assets" \
  --tags "pwa,assets" \
  --limit 5
```

### During debugging
```bash
python3 ~/.config/opencode/scripts/project-memory.py --search "manifest"
```

### Periodic review
```bash
python3 ~/.config/opencode/scripts/project-memory.py --list
python3 ~/.config/opencode/scripts/project-memory.py --export > .opencode/memory/README.md
```

## Required memory triggers

Save memory when any of these happen:
1. Task took a non-obvious fix or workaround.
2. Stack/library behavior differed from expectation.
3. User explicitly corrected or clarified a decision.
4. A security, deploy, or operational constraint was discovered.
5. A reusable component/pattern was established.
6. A previous assumption was proven wrong.

## Gate requirement

For non-trivial work, `@orchestrator` and `@fixer` must:
- search existing project memory before starting the task,
- save only important new memories before final completion claim,
- include memory IDs or relevant findings in evidence when they materially affected the task,
- run `python3 ~/.config/opencode/scripts/project-memory.py --cleanup` before final completion so low-value entries do not accumulate.

## Importance policy

Default retrieval should use `--importance high`.

Save `high`:
- recurring pitfall,
- project-specific invariant,
- security/deploy constraint,
- expensive workaround,
- user correction that will matter again.

Save `medium`:
- useful pattern likely to recur, but not critical.

Propose `medium`:
- when the agent is unsure if the lesson is broadly reusable or similar to existing memory.

Avoid `low`:
- routine implementation notes,
- obvious library/API usage,
- one-off debugging trivia,
- temporary noise.

## Proposal flow

Implementation lanes can propose memories instead of saving directly when unsure:
```bash
python3 ~/.config/opencode/scripts/project-memory.py --propose \
  --task <task-id> \
  --category pattern \
  --importance medium \
  --lesson "..." \
  --context "..." \
  --tags "..."
```

`@quality-gate` reviews pending proposals during final signoff:
- apply if reusable and not duplicate,
- leave pending if user decision is needed,
- archive if outdated.

## Cleanup

```bash
python3 ~/.config/opencode/scripts/project-memory.py --cleanup --archive-old
```

This removes low-importance memories and archives old unused entries.
