# Generated: Capability Matrix

Generated from `.opencode/capabilities/registry.json`. Advisory only; canonical policy remains in `.opencode/docs/`.

- Agents: 12
- Skills: 12

| Type | Name | Owner lane | Status | Risk | Fallback |
| --- | --- | --- | --- | --- | --- |
| agent | architect | @architect | active | architecture-advice, read-only-boundary | @oracle for review or @artifact-planner for plan artifacts |
| agent | artifact-planner | @artifact-planner | active | plan-artifact-write, scope-bloat | @orchestrator direct routing for tiny reversible work |
| agent | council | @council | active | expensive-consensus, read-only-boundary | @oracle single-review lane |
| agent | designer | @designer | active | ui-change, accessibility, visual-parity | @fixer for non-UI implementation |
| agent | explorer | @explorer | active | read-only-discovery, stale-map | targeted glob/grep/read by @orchestrator |
| agent | fixer | @fixer | active | code-edit, test-impact | @artifact-planner if scope becomes ambiguous |
| agent | librarian | @librarian | active | external-research, read-only-boundary | local docs first, then no external lookup |
| agent | oracle | @oracle | active | review-advice, read-only-boundary | @quality-gate for final conformance |
| agent | orchestrator | @orchestrator | active | routing, integration, scope-control | specialist lane or user clarification |
| agent | quality-gate | @quality-gate | active | final-signoff, read-only-boundary | block completion and return residual risks |
| agent | skill-improver | @skill-improver | active | prompt-change, routing-drift | document finding without prompt edits |
| agent | visual-asset-generator | @visual-asset-generator | active | image-generation, legal-style-equivalent, asset-write | asset manifest only; orchestrator executes image endpoint |
| skill | opencode-architect | @architect | active | architecture-advice | @oracle review |
| skill | opencode-artifact-planner | @artifact-planner | active | plan-artifact-write | @orchestrator routing |
| skill | opencode-council | @council | active | expensive-consensus | @oracle review |
| skill | opencode-designer | @designer | active | ui-change, accessibility | @fixer |
| skill | opencode-explorer | @explorer | active | read-only-discovery | targeted local search |
| skill | opencode-fixer | @fixer | active | code-edit, test-impact | @artifact-planner |
| skill | opencode-librarian | @librarian | active | external-research | local docs only |
| skill | opencode-oracle | @oracle | active | review-advice | @quality-gate |
| skill | opencode-orchestrator | @orchestrator | active | routing, integration | user clarification |
| skill | opencode-quality-gate | @quality-gate | active | final-signoff | block completion |
| skill | opencode-skill-improver | @skill-improver | active | prompt-change, routing-drift | record improvement note only |
| skill | opencode-visual-asset-generator | @visual-asset-generator | active | image-generation, legal-style-equivalent | asset manifest only |
