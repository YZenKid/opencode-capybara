---
name: taste-overlay
description: Taste-inspired UI quality overlay for substantial web or mobile UI work. Use after local DESIGN.md and Open Design catalog selection to set bounded variance, motion, density, and run anti-slop preflight; never use as a replacement design authority.
license: MIT
metadata:
  upstream: https://github.com/Leonxlnx/taste-skill
  revision: 7c397f22d3af6f2b3f1925eb147d8e8801086151
  adaptation: local-overlay
---

# Taste Overlay

Local adaptation of selected `gpt-taste` ideas. Upstream snapshot and MIT notice: [SOURCE.md](./SOURCE.md).

## Authority

1. User instruction, safety/license rules, project `DESIGN.md`, and cited Open Design system/template win.
2. Existing lane contracts win over this overlay.
3. This skill supplies bounded craft checks only. It does not prescribe framework, font, animation library, asset provider, or page formula.

## Workflow

1. Read target `DESIGN.md`, catalog citation, existing tokens/components, and reference evidence.
2. Set explicit, reversible dials: `DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY` (1–10). Explain each from product and reference evidence.
3. For greenfield or taste-sensitive work, produce 2–3 bounded section directions when evidence does not already select one. Choose one with tradeoffs.
4. Check hierarchy, heading wrapping at target widths, spacing rhythm, intentional grid occupancy, legible controls, domain-specific imagery, and authentic content.
5. Run local anti-slop and accessibility gates before implementation claim. Use motion only when it communicates state, continuity, or hierarchy; honor reduced motion.
6. Record source decisions, evidence, dials, rejected directions, and remaining assumptions in task evidence.

## Quality checklist

- [ ] `DESIGN.md` + Open Design citation remain visual/token authority.
- [ ] Headings fit intended viewport without accidental text-wall wrapping.
- [ ] Grid/cell spans intentional; no empty decorative bento cells.
- [ ] Content and imagery are real, source-backed, or clearly labeled unavailable; no fake metrics/testimonials/placeholders.
- [ ] Motion has purpose, respects reduced motion, and uses installed/native capability only.
- [ ] Buttons meet contrast and target-size requirements.
- [ ] Evidence names source, dials, rejected direction, and assumptions.

## Anti-patterns

- Forced deterministic randomization or invented novelty.
- Mandatory AIDA, GSAP, pinned scroll, hover effects, or huge spacing.
- `picsum`, fake testimonials/metrics, synthetic stock substitution, or design labels as filler.
- Auto-installing packages, running auth, publishing, or bypassing license checks.
- Replacing project font/tokens/catalog anatomy without a documented deviation.

## Output example

```yaml
design_read:
  source_authority: "DESIGN.md + Open Design catalog citation"
  dials: { design_variance: 4, motion_intensity: 2, visual_density: 5 }
checks:
  heading_wrap: "desktop/mobile verified"
  imagery: "real project assets required; no placeholder fallback"
rejected:
  - "motion-heavy pinned gallery: no product evidence"
assumptions:
  - "final photography pending owner-supplied source"
```

## Graphify query-first contract

For code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes, query fresh available Graphify first. Use narrow query/path/explain. Direct source reading + tests/runtime still required. Missing/stale/unsupported fallback must be recorded. Tiny known-file and non-code skip only with explicit reason.
