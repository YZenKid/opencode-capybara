---
name: opencode-plan-reviewer
description: Dedicated plan depth validation workflow for execution-ready plans.
---

# OpenCode Plan Reviewer

Use this skill to validate that a plan is deep enough before implementation.

## Purpose
Prevent shallow plans from reaching implementation even when they contain all required section headings.

## Workflow
1. Locate primary plan file at `.opencode/plans/<task-id>.md`
2. Run validation script:
   ```bash
   python3 scripts/validate-plan-depth.py .opencode/plans/<task-id>.md
   ```
3. Verify all metrics pass (depth, anti-generic, reference pack, design depth)
4. If any metric fails, return `NEEDS_DEPTH` with specific failures
5. If all metrics pass, return `PASS`

## Minimum depth requirements

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

## Anti-generic patterns (mechanical failures)

The validator checks for these patterns and fails if any are found:
- centered gradient hero
- generic "modern clean"
- fake dashboard metrics / arbitrary KPI
- emoji icons / numeric-only icons
- placeholder imagery / blank image frames
- repeated card/grid anatomy (card spam)
- abstract blobs / floating UI cards / CSS glass panels
- vague neon blobs / default purple/blue glow
- debug/internal copy / server labels / port numbers
- lorem text / placeholder copy
- missing hero composition
- missing image strategy
- missing motion motivation
- missing reduced-motion support

## Reference pack requirement

Plan must include:
- Minimum 3 reference screenshots/URLs, OR
- Explicit first-principles rationale

Reference pack must cover:
1. Visual direction / aesthetic family
2. Layout / composition patterns
3. Component / interaction patterns
4. Asset / image style
5. Motion / transition style

## Design depth keywords

Plan must contain these keywords:
- design read
- design_variance
- motion_intensity
- visual_density
- page-by-page
- section-level
- component inventory
- asset/image decision
- motion system
- reduced-motion
- accessibility gate
- validation evidence

## State coverage requirement
Every component must document: empty, loading, error, success states.

## Output contract
- Status: `PASS` or `NEEDS_DEPTH`
- Validation script output
- Specific failures if any
- Recommendation: expand plan or proceed

## Reference
- Validation script: `scripts/validate-plan-depth.py`
- Reference plan: `.opencode/docs/EXAMPLE_PLAN.md`

## Hard rule
Section presence alone is NOT sufficient. A plan with all required headings but shallow content must be rejected as `NEEDS_DEPTH`.
