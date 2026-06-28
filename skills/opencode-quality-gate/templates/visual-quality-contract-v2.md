# Visual Quality Contract v2

> **v2 extends v1** with the `catalog_citation` block. v1 is still valid for non-substantial UI.
> For substantial UI work (greenfield, design revamp, reference parity, image-heavy, taste-sensitive), **v2 is mandatory** and `@quality-gate` will return `NEEDS_FIX` if missing.
> Reference: `.opencode/plans/ui-ux-open-design-upgrade.md` and `.opencode/catalog/INDEX.md`.

**Task ID**: {{task_id}}
**Surface**: {{surface_name}}
**Owner**: {{owner_lane}}
**Schema version**: v2
**Required for**: substantial UI claims, greenfield, design revamp, reference parity

---

## 1. Intent & Meaning Source

**Emotional Goal**: What should this surface evoke in the user?

**Meaning Source**: What makes this surface meaningful (not decorative)?

**Reference Essence**: What real-world textures, activities, or contexts does this surface reference?

---

## 2. Catalog Citation (v2 — MANDATORY for substantial UI)

> **Mechanical check**: this block must be present and complete. Missing or incomplete → `NEEDS_FIX`.

```yaml
catalog_citation:
  design_system:
    name: "<e.g. Linear>"
    slug: "<e.g. linear>"
    source: "https://open-design.ai/plugins/systems/example-<slug>"
    license: "Apache-2.0"
    # When forked, also list:
    # fork_source_path: ".opencode/catalog/systems/<slug>/DESIGN.md"
    # project_fork_path: "<project>/DESIGN.md"
  template_pattern:
    name: "<e.g. SaaS Layout>"
    slug: "<e.g. example-saas-layout>"
    source: "https://open-design.ai/plugins/templates/<slug>"
    license: "Apache-2.0"
  pair_rationale: |
    <2-4 sentences explaining why this system + template pair was chosen over alternatives.
    Reference the catalog-search.py --pair result or list the rejected alternatives with reasons.>
  rejected_alternatives:
    - name: "<alternative system or template>"
      reason: "<why it was rejected>"
  deviation_audit:
    - what: "<e.g. ink token changed from #0d0e10 to #ff0066>"
      why: "<business / brand / accessibility reason>"
      risk: "<what could break, e.g. contrast on body text, brand consistency>"
      approved_by: "<name or 'pending review'>"
  must_use_tokens:
    - "<hex or token name, e.g. #0d0e10 or ink>"
    - "<e.g. #5e6ad2 or accent>"
  must_use_pattern:
    - "<e.g. 12-col grid, 96px section padding desktop>"
  must_avoid_token:
    - "<hex or pattern, e.g. #ffffff hero, neon accent>"
```

**Verification command**:
```bash
python3 ~/.config/opencode/scripts/visual-audit-check.py \
  --project-root . \
  --contract .opencode/evidence/<task-id>/visual-quality-contract.md
```

---

## 3. Structured Design Contract (from v1, still required)

### Must Show
Concrete elements that MUST appear in this surface:

- [ ] {{must_show_item_1}}
- [ ] {{must_show_item_2}}
- [ ] {{must_show_item_3}}

**Example for hero section (community/craft domain)**:
- [ ] Real photography of people working with hands
- [ ] Physical materials (wood, fabric, clay, plants)
- [ ] Natural lighting, not studio-perfect
- [ ] Environment context (workshop, field, kitchen)

### Must NOT Show
Concrete elements that MUST NOT appear:

- [ ] {{must_not_show_item_1}}
- [ ] {{must_not_show_item_2}}
- [ ] {{must_not_show_item_3}}

**Example**:
- [ ] Abstract gradient backgrounds
- [ ] Stock photos of smiling people in offices
- [ ] Generic icons without domain specificity
- [ ] "Foto menyusul" placeholders

### Reject If
Explicit failure conditions that trigger rejection:

- [ ] {{reject_if_condition_1}}
- [ ] {{reject_if_condition_2}}
- [ ] {{reject_if_condition_3}}

**Example**:
- [ ] Hero uses illustration when reference uses photography
- [ ] No hands/physical objects visible in craft domain
- [ ] Decorative stats without meaningful data
- [ ] Sterile/corporate feel in community domain

---

## 4. Anti-Pattern Detection (from v1)

### Fake Warmth Patterns
Patterns that LOOK warm but are actually template:

- {{fake_warmth_pattern_1}}
- {{fake_warmth_pattern_2}}

**Example**:
- Pastel gradient with no physical objects
- Cute mascot without behavioral grounding
- Symbolic garden without organic texture
- "Warm" typography but sterile layout

### Template Smells
Smells that indicate template-feel despite structural compliance:

- {{template_smell_1}}
- {{template_smell_2}}

**Example**:
- All sections use identical card layout
- Stats/metrics are decorative (5, 10, 100) without context
- Hero has no domain-specific content
- Images are abstract patterns, not real photography

---

## 5. Image Strategy

**Image Decision**: {{generate | use-provided-assets | licensed-existing-assets | no-generation-needed | direct-reuse-user-approved}}

**Real Photography Required**: {{yes | no}}

**Domain Texture Required**: {{yes | no}}

**Rationale**: Why this image strategy?

**Catalog cross-reference** (v2): if the chosen design system implies a photography style, link it here:
- e.g. "Per the `linear` system DESIGN.md §7, photography style is 'documentary, hands-on, real workspaces'."

---

## 6. Evidence Checklist (v2 — expanded)

- [ ] Reference essence extraction documented (warmth, humanity, texture, domain-specific content)
- [ ] **Catalog citation block complete** (section 2)
- [ ] **Catalog system DESIGN.md cited by URL** (open-design.ai)
- [ ] **Catalog template cited by URL** (open-design.ai)
- [ ] **Deviation audit populated** (or `deviation_audit: []` with explicit note "no deviations from base system")
- [ ] **must_use_tokens / must_avoid_token listed** (mechanical, not taste)
- [ ] Screenshot comparison: reference vs implementation
- [ ] Domain texture present (physical objects, hands, materials, environment)
- [ ] No placeholder text or decorative stats
- [ ] No fake warmth patterns
- [ ] No template smells
- [ ] Image strategy explicitly states "real photography required" if applicable

---

## 7. Lane Signoff

### Planner
- [ ] Per-surface reject_if documented in plan
- [ ] Reference essence extraction referenced
- [ ] **Catalog-decision.md exists** (or referenced) — see `.opencode/evidence/<task-id>/catalog-decision.md`

### Designer
- [ ] Structured fields (must_show, must_not_show, reject_if) filled with concrete items
- [ ] Reference-essence.md created
- [ ] Anti-pattern detection sections completed
- [ ] **Catalog citation block complete with pair_rationale and rejected_alternatives**
- [ ] **must_use_tokens / must_avoid_token declared**

### Frontend / Mobile
- [ ] Design handoff reviewed for domain texture
- [ ] Pushback applied if design feels template-ish (design_pushback.md if needed)
- [ ] No "foto menyusul" or placeholder text in production UI
- [ ] **Tokens loaded from `.opencode/catalog/<active-system>/tokens.{css,json,tailwind.config.js}`**
- [ ] **Catalog source cited in PR/evidence**

### Quality Gate
- [ ] **Catalog citation verified by `visual-audit-check.py`** (exit 0)
- [ ] Visual rubric completed (visual-rubric.md v2)
- [ ] Side-by-side screenshot comparison annotated
- [ ] All reject_if conditions verified absent
- [ ] **Token parity check passed** (tokens used vs tokens declared in section 2)

---

## Notes

Add any additional context, decisions, or open questions here.

---

## v1 → v2 migration notes

- v1 contracts without `catalog_citation` are still valid for **non-substantial UI** (tiny/reversible UI tweaks, non-visual changes).
- v2 is **mandatory** for substantial UI; the trigger list lives in `.opencode/docs/SKILLS.md` §"UI/UX design system source of truth".
- To upgrade a v1 contract to v2: add section 2 (Catalog Citation), expand section 6 (Evidence Checklist), and update section 7 (Lane Signoff) with the catalog-citation rows.
- If the project predates the catalog integration and the v1 contract is in use, mark it `schema: v1` at the top of the file and route to `@designer` for migration on the next substantial UI change.
