# Visual Quality Contract

**Task ID**: {{task_id}}
**Surface**: {{surface_name}}
**Owner**: {{owner_lane}}

---

## 1. Intent & Meaning Source

**Emotional Goal**: What should this surface evoke in the user?

**Meaning Source**: What makes this surface meaningful (not decorative)?

**Reference Essence**: What real-world textures, activities, or contexts does this surface reference?

---

## 2. Structured Design Contract

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

## 3. Anti-Pattern Detection

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

## 4. Image Strategy

**Image Decision**: {{generate | use-provided-assets | licensed-existing-assets | no-generation-needed | direct-reuse-user-approved}}

**Real Photography Required**: {{yes | no}}

**Domain Texture Required**: {{yes | no}}

**Rationale**: Why this image strategy?

---

## 5. Evidence Checklist

- [ ] Reference essence extraction documented (warmth, humanity, texture, domain-specific content)
- [ ] Screenshot comparison: reference vs implementation
- [ ] Domain texture present (physical objects, hands, materials, environment)
- [ ] No placeholder text or decorative stats
- [ ] No fake warmth patterns
- [ ] No template smells
- [ ] Image strategy explicitly states "real photography required" if applicable

---

## 6. Lane Signoff

### Planner
- [ ] Per-surface reject_if documented in plan
- [ ] Reference essence extraction referenced

### Designer
- [ ] Structured fields (must_show, must_not_show, reject_if) filled with concrete items
- [ ] Reference-essence.md created
- [ ] Anti-pattern detection sections completed

### Frontend
- [ ] Design handoff reviewed for domain texture
- [ ] Pushback applied if design feels template-ish (design_pushback.md if needed)
- [ ] No "foto menyusul" or placeholder text in production UI

### Quality Gate
- [ ] Visual rubric completed (visual-rubric.md)
- [ ] Side-by-side screenshot comparison annotated
- [ ] All reject_if conditions verified absent

---

## Notes

Add any additional context, decisions, or open questions here.
