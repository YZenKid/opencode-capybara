---
description: Improve a UI/design surface with Designer using Design Read, craft dials, anti-slop preflight, and evidence
agent: designer
model: 9router/high
---

Improve target UI/design surface.

Arguments from user, if any:

```text
$ARGUMENTS
```

Workflow:

1. Read target project `DESIGN.md` first; fallback to `design-system/DESIGN.md` or documented equivalent.
2. If substantial UI work lacks project design guidance, recommend `/init-design` before inventing broad direction.
3. Lock brief: surface, audience, job-to-be-done, brand/product constraints, platform, content/assets, references, acceptance criteria.
4. Write `Design Read`: `Reading this as: <surface> for <audience>, with <vibe>, leaning toward <design system/aesthetic family>.`
5. Set dials: `DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY`.
6. Plan changes section-by-section: hierarchy, layout, type, color, states, responsive behavior, motion, image/asset strategy.
7. Run mechanical preflight before final: hero fit, nav single-line, CTA contrast/wrap/duplicate intent, eyebrow restraint, layout repetition, image strategy, motion motivation, reduced-motion.
8. Implement only requested/bounded design improvements; avoid role creep into product architecture or release signoff.
9. Validate if runnable with screenshots/notes for key viewports/states and accessibility/motion checks.
10. Return changed files, `Design Read`, dials, evidence, preflight result, critique score, and follow-ups.

Critique score rubric: Philosophy, Hierarchy, Detail, Function, Innovation. State current score and what would make it 10/10.
