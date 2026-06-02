---
description: Critique UI/design work without editing by default, using evidence, severity, score, and mechanical anti-slop checks
agent: designer
model: 9router/high
---

Critique target UI/design surface. Do not edit files unless user explicitly asks after critique.

Arguments from user, if any:

```text
$ARGUMENTS
```

Workflow:

1. Read target project `DESIGN.md` first; fallback to `design-system/DESIGN.md` or documented equivalent.
2. Capture/inspect supplied screenshots, URLs, references, code, and user acceptance criteria.
3. Write `Design Read`: `Reading this as: <surface> for <audience>, with <vibe>, leaning toward <design system/aesthetic family>.`
4. Set/read dials: `DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY`.
5. Score 0-10 across Philosophy, Hierarchy, Detail, Function, Innovation; state what 10/10 requires.
6. Run mechanical preflight: hero fit, nav single-line, CTA contrast/wrap/duplicate intent, eyebrow restraint, layout repetition, image strategy, motion motivation, reduced-motion.
7. Report issues by severity: `BLOCKER`, `HIGH`, `MEDIUM`, `LOW`, `INFO`.
8. Distinguish mechanical/evidence failures from pure taste preferences. Pure preference should be `LOW` or follow-up.
9. Provide next actions, required evidence, and whether `@quality-gate` handoff is needed.

Output: concise findings, locations/sections, evidence used, score, preflight result, and prioritized fix list.
