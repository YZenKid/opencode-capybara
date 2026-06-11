# UI Slop Evaluation Report

Status: PASS
Mode: check
Fixtures/sources: 6

## abstract-hero-filler-failure

Status: FAIL
Expected: FAIL
Average score: 4.46

Findings:
- BLOCKER abstract-hero-filler (hero_specificity) [hero section]: Hero relies on generic abstract composition rather than domain-specific content. Remediation: Replace generic blobs/floating cards with product/domain-specific hero composition.
- HIGH placeholder-visual (hero_specificity) [visual placeholder]: Placeholder visual/copy remains in UI. Remediation: Replace placeholder visual content with domain-specific imagery, illustration, or honest empty state.

## clay-glass-neon-card-spam

Status: FAIL
Expected: FAIL
Average score: 3.58

Findings:
- HIGH requested-aesthetic-mismatch (style_fidelity) [style/class tokens]: Requested clay/glass aesthetic is dominated by neon/glow language. Remediation: Translate requested aesthetic into concrete material tokens and remove conflicting style families.
- HIGH material-grammar-missing (style_fidelity) [style/class tokens]: Requested material family lacks soft clay/glass grammar tokens. Remediation: Add requested material grammar: surfaces, depth, translucency, shadows, and color roles.
- HIGH card-spam-repetition (layout_variety) [card grid]: Repeated card anatomy count: 6. Remediation: Replace repeated card-grid anatomy with purpose-specific hierarchy and section composition.
- MEDIUM generic-neon-glass-overuse (style_fidelity) [style/class tokens]: Generic neon/glass token count: 15. Remediation: Remove generic neon/glow/glass defaults unless requested and domain-relevant.
- BLOCKER debug-copy-user-facing (debug_artifact_hygiene) [text copy]: Internal/debug copy appears in user-facing text. Remediation: Remove localhost, TODO, debug, mock, internal state, and implementation copy from user-facing UI.
- BLOCKER fake-metric (content_humanity) [metrics text]: Arbitrary metric or demo number appears without source framing. Remediation: Remove arbitrary metrics or label data as real source-backed/demo-only with context.

## debug-internal-copy-failure

Status: FAIL
Expected: FAIL
Average score: 4.54

Findings:
- BLOCKER debug-copy-user-facing (debug_artifact_hygiene) [text copy]: Internal/debug copy appears in user-facing text. Remediation: Remove localhost, TODO, debug, mock, internal state, and implementation copy from user-facing UI.
- MEDIUM missing-state-evidence (state_accessibility_evidence) [dashboard state copy]: Dashboard lacks visible state or data-scope evidence. Remediation: Add visible loading/empty/error/success state evidence for substantial UI.

## fake-metric-failure

Status: FAIL
Expected: FAIL
Average score: 4.33

Findings:
- BLOCKER fake-metric (content_humanity) [metrics text]: Arbitrary metric or demo number appears without source framing. Remediation: Remove arbitrary metrics or label data as real source-backed/demo-only with context.
- HIGH placeholder-visual (hero_specificity) [visual placeholder]: Placeholder visual/copy remains in UI. Remediation: Replace placeholder visual content with domain-specific imagery, illustration, or honest empty state.
- MEDIUM missing-state-evidence (state_accessibility_evidence) [dashboard state copy]: Dashboard lacks visible state or data-scope evidence. Remediation: Add visible loading/empty/error/success state evidence for substantial UI.

## good-clay-glass-sample

Status: PASS
Expected: PASS
Average score: 5

Findings:
- none

## legitimate-dashboard-pass

Status: PASS
Expected: PASS
Average score: 5

Findings:
- none

