# Shared Policies

This document contains policy blocks shared across multiple agents and skills. Agents should reference this document instead of duplicating content.

## Reference-first creativity contract

All agents must follow this contract when generating outputs:

- Prefer repo-local evidence, official docs, upstream source/examples, screenshots/references, and runtime/browser evidence before inventing material details.
- If a reasonable source exists, use it or explicitly record why it was skipped.
- Treat creativity as grounded option generation: for greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with tradeoff rationale.
- Do not present assumptions as facts. Label assumptions explicitly, keep them reversible, and route/ask when they affect architecture, product behavior, UX direction, data, security, or release risk.
- Do not follow the workflow mechanically when stronger repo/reference evidence points elsewhere; adapt and record the reason.
- In outputs/evidence, name the key references used or state that the result is based on repo-local evidence only.

## Anti-generic UI rules

For substantial UI work, these are mechanical failures (not taste preferences):

| Failure | Status |
|---|---|
| Centered gradient hero without product/domain composition | `blocked` |
| Generic "modern clean" without source-backed specifics | `blocked` |
| Fake dashboard metrics (arbitrary KPI numbers, 99%/24k/10x claims) | `needs-polish` |
| Emoji icons or numeric-only service icons | `needs-polish` |
| Placeholder imagery or blank image frames | `needs-polish` |
| Repeated card/grid anatomy across sections (card spam) | `needs-polish` |
| Abstract blobs, floating UI cards, CSS glass panels as hero | `blocked` |
| Vague neon blobs or default purple/blue glow | `needs-polish` |
| Debug/internal copy, server labels, port numbers in UI | `needs-polish` |
| Lorem text or placeholder copy in user-facing UI | `needs-polish` |
| Missing hero composition (no meaningful product/domain content) | `blocked` |
| Missing image strategy per visual section | `blocked` |
| Missing motion motivation (no explanation for non-trivial motion) | `needs-polish` |
| Missing reduced-motion support | `needs-polish` |

If any failure is present, return `needs-polish` or `blocked`. Do not mark substantial UI `ready` when these failures exist.

## Reference pack requirement

For greenfield/UI-heavy/substantial visual work, the plan must include:

- Minimum 3 reference screenshots/URLs, OR
- Explicit first-principles rationale explaining why reference-based design is not used.

Reference pack must cover:
1. Visual direction / aesthetic family
2. Layout / composition patterns
3. Component / interaction patterns
4. Asset / image style
5. Motion / transition style

Missing reference pack = automatic `NEEDS_DEPTH` or `BLOCKED`.

## Design depth requirements

Before marking design as `ready`, verify all minimums are met:

| Metric | Minimum |
|---|---|
| Design Read statement | Required for substantial work |
| Craft dials documented | DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY |
| Reference pack | Minimum 3 reference screenshots/URLs or explicit first-principles rationale |
| Page-by-page UX blueprint | Minimum 3 pages with full detail |
| Section-level visual spec | Minimum 5 sections per page with layout/hierarchy/spacing/typography/color/interaction/motion/responsive |
| Component system plan | Minimum 20 components with variants/states/accessibility/responsive/motion |
| Visual system | Palette roles, typography scale, spacing scale, radius, border, elevation, icon style, image style, grid, breakpoints, focus states |
| Asset/image decision | Per visual area: generate/use-provided/licensed/no-generation-needed with reason |
| Motion system | Purpose, API/library choice, per-page motion map, interaction motion, reduced-motion fallback |
| Interaction/state design | Default/hover/focus/active/disabled/loading/empty/error/success/permission/unauthenticated/offline/partial/skeleton/validation |
| Responsive plan | Mobile/tablet/desktop layout rules, nav changes, CTA placement, sticky behavior, data display adaptation |
| Accessibility gate | Semantic headings, keyboard support, visible focus, form labels, contrast, screen-reader, touch targets, reduced motion |
| Validation evidence | Screenshots by viewport and key states, interaction checks, motion/reduced-motion checks, accessibility notes |

**Auto-reject rules:**
- Missing Design Read = `blocked`
- Missing craft dials = `needs-polish`
- Missing reference pack (3+ references or first-principles rationale) = `blocked`
- Missing page-by-page blueprint (3+ pages) = `blocked`
- Missing section-level spec (5+ sections per page) = `needs-polish`
- Missing component system (20+ components) = `needs-polish`
- Missing visual system = `needs-polish`
- Missing asset/image decision = `blocked`
- Missing motion system = `needs-polish`
- Missing interaction/state design = `needs-polish`
- Missing responsive plan = `needs-polish`
- Missing accessibility gate = `needs-polish`
- Missing validation evidence = `blocked`

## Plan depth requirements

Before reviewing implementation, verify plan meets minimum depth:

| Metric | Minimum |
|---|---|
| Total plan lines | 5000 |
| Goal + Non-goals words | 200 |
| Requirements count | 10 |
| Requirements words | 500 |
| Acceptance Criteria count | 8 |
| Acceptance Criteria words | 300 |
| UI pages (greenfield) | 3 |
| Words per UI page | 1000 |
| Components in inventory | 20 |
| Implementation steps | 50 |
| Validation commands | 10 |

**State coverage requirement:**
Every component must have state coverage: empty, loading, error, success. Missing state coverage = `NEEDS_FIX`.

## Evidence contract

All material changes must end with evidence, not just claims.

Canonical task evidence path: `.opencode/evidence/<task-id>/`.

### Final summary template
```md
## Summary
- ...

## Changes
- ...

## Evidence
- Command: `npm run test:prompt-gates`
- Result: PASS
- Additional validation: ...

## Risks / Limitations
- ...

## Next Steps
- ...
```

If evidence is unavailable, write an explicit limitation note.

## Remediation worklist contract

For any status other than `PASS` (`NEEDS_FIX`, `BLOCKED`, or `PASS_WITH_RISKS`), include a structured remediation worklist. Quality gate stays read-only: prescribe fixes and validation, but do not edit, autofix, patch, commit, or execute remediation.

Each remediation item must include:

- `finding`: concise issue tied to evidence.
- `blocker_or_risk_class`: `hard_stop`, `soft_blocker`, `required_before_PASS`, or `non_blocking_follow_up`.
- `owner_lane`: target lane such as `@orchestrator`, `@fixer`, `@designer`, `@backend`, `@devops`, `@librarian`, or `user`.
- `action`: concrete remediation step.
- `validation`: command, review, evidence, or check needed after action.
- `exit_criteria`: condition that closes item.
- `requires_user_decision`: `yes` or `no`.

For `PASS_WITH_RISKS`, distinguish required-before-`PASS` work from non-blocking follow-ups.

## Source-approved 1:1 porting contract

When the user explicitly asks for `1:1`, `clone`, `port`, `copy`, `copy from`, `make exactly like`, or provides a source URL/repo/file plus explicit approval to reuse it, default to literal copy/adapt/prune/direct reuse rather than redesign or style-equivalent recreation.

Route `@explorer` for source inventory, `@artifact-planner` for copy/adapt/prune/create mapping, `@designer` for exact UI anatomy when visual, `@frontend`/`@fixer` for literal implementation, and `@quality-gate` for parity/reuse evidence.

Keep legal/security/scope safeguards: restricted assets, secrets, unsafe code, incompatible licenses, privacy hazards, fake testimonials/claims, logos/trademarks, and out-of-scope behavior still require blocking, pruning, or substitution with documented rationale.

## Mode-aware execution

Before non-trivial routing, classify the request into one mode and record the mode in evidence or handoff notes.

### Greenfield App Accelerator
Use for new apps, blank repos, MVPs, SaaS/product builds, or major product revamps.

- Always route new app/MVP/SaaS/product builds to `@artifact-planner` before implementation except explicitly tiny prototype-only work labeled `draft`/`prototype`.
- Optimize for the first usable vertical slice, not whole-app perfection.
- Explore 2-3 credible product/UX/architecture options, compare tradeoffs, then converge.
- Allow `PASS_FOR_SLICE` execution when whole-product decisions remain open but the selected slice avoids locking those decisions.
- Final claim should be `MVP slice complete` unless the whole app is actually finished and validated.

### Maintenance Stability Mode
Use for bugfixes, regressions, refactors, dependency updates, small features in existing apps, and incident follow-up.

- Maintenance work should not be forced through greenfield product thesis, 2-3 creative alternatives, or whole-app planning by default.
- Start with repro, regression test, targeted evidence, or clear failing behavior.
- Prefer the smallest safe diff and preserve existing architecture/UX unless the bug proves they are broken.
- Use `@explorer` for local facts, `@fixer` or the domain lane for implementation, and `@quality-gate` for material/risky changes.

### Creativity Fast Path
Use for explicit natural-language requests such as `brainstorm`, `explore options`, `generate ideas`, `sketch first`, `prototype cepat`, `draft UI`, `draft copy`, or `jangan terlalu production-grade dulu`.

- Opt-in and reversible, never default-on.
- Activated by explicit user intent, not by a dedicated command.
- For exploration output, not a production-bypass path.
- Label the result `draft`, `prototype`, or `exploration`.
- Record assumptions, confidence, and reversible scope.
- Exit Creativity Fast Path and return to normal routing when the user asks for permanent implementation, material source edits, commit, deploy, release, strong completion claims, or anything crossing a hard rail.
