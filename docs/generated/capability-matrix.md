# Generated: Capability Matrix

Generated from `.opencode/capabilities/registry.json`. Advisory only; canonical policy remains in `.opencode/docs/`.

- Agents: 19
- Skills: 19

| Type | Name | Owner lane | Status | Risk | Fallback |
| --- | --- | --- | --- | --- | --- |
| agent | architect | @architect | active | architecture-advice, read-only-boundary | @oracle for review or @artifact-planner for plan artifacts |
| agent | artifact-planner | @artifact-planner | active | plan-artifact-write, scope-bloat | @orchestrator direct routing for tiny reversible work |
| agent | backend | @backend | active | api-change, data-change, auth-integration | @system-analyst for unclear contracts or @architect for data/security boundaries |
| agent | council | @council | active | expensive-consensus, read-only-boundary | @oracle single-review lane |
| agent | designer | @designer | active | ui-change, accessibility, visual-parity | @fixer for non-UI implementation |
| agent | devops | @devops | active | deploy, destructive-infra, secrets, ci-cd | @architect for platform decisions or @quality-gate for final release/security signoff |
| agent | explorer | @explorer | active | read-only-discovery, stale-map | targeted glob/grep/read by @orchestrator |
| agent | fixer | @fixer | active | code-edit, test-impact | @artifact-planner if scope becomes ambiguous |
| agent | frontend | @frontend | active | web-ui-change, accessibility, api-integration | @designer for missing visual direction or @backend for unclear contracts |
| agent | fullstack | @fullstack | active | cross-layer-change, scope-creep, contract-drift | split to @frontend and @backend or route @artifact-planner when scope grows |
| agent | librarian | @librarian | active | external-research, read-only-boundary | local docs first, then no external lookup |
| agent | mobile | @mobile | active | native-permissions, privacy, store-constraints, mobile-runtime | @architect for mobile architecture or @quality-gate for privacy/store signoff |
| agent | oracle | @oracle | active | review-advice, read-only-boundary | @quality-gate for final conformance |
| agent | orchestrator | @orchestrator | active | routing, integration, scope-control | specialist lane or user clarification |
| agent | project-manager | @project-manager | active | read-only-boundary, delivery-plan, tracker-write-risk | @system-analyst for unclear requirements or local artifact draft when tracker unavailable |
| agent | quality-gate | @quality-gate | active | final-signoff, read-only-boundary | block completion and return residual risks |
| agent | skill-improver | @skill-improver | active | prompt-change, routing-drift | document finding without prompt edits |
| agent | system-analyst | @system-analyst | active | read-only-boundary, requirements-ambiguity, contract-drift | @project-manager for delivery breakdown or implementation lane after handoff |
| agent | visual-asset-generator | @visual-asset-generator | active | image-generation, legal-style-equivalent, asset-write | asset manifest only; orchestrator executes image endpoint |
| skill | opencode-architect | @architect | active | architecture-advice | @oracle review |
| skill | opencode-artifact-planner | @artifact-planner | active | plan-artifact-write | @orchestrator routing |
| skill | opencode-backend | @backend | active | api-change, data-change, auth-integration | @system-analyst or @architect |
| skill | opencode-council | @council | active | expensive-consensus | @oracle review |
| skill | opencode-designer | @designer | active | ui-change, accessibility | @fixer |
| skill | opencode-devops | @devops | active | deploy, destructive-infra, secrets | @architect or @quality-gate |
| skill | opencode-explorer | @explorer | active | read-only-discovery | targeted local search |
| skill | opencode-fixer | @fixer | active | code-edit, test-impact | @artifact-planner |
| skill | opencode-frontend | @frontend | active | web-ui-change, accessibility, api-integration | @designer or @backend |
| skill | opencode-fullstack | @fullstack | active | cross-layer-change, scope-creep | split @frontend/@backend or @artifact-planner |
| skill | opencode-librarian | @librarian | active | external-research | local docs only |
| skill | opencode-mobile | @mobile | active | native-permissions, privacy, mobile-runtime | @architect or @quality-gate |
| skill | opencode-oracle | @oracle | active | review-advice | @quality-gate |
| skill | opencode-orchestrator | @orchestrator | active | routing, integration | user clarification |
| skill | opencode-project-manager | @project-manager | active | delivery-plan, read-only-boundary | local plan artifact draft |
| skill | opencode-quality-gate | @quality-gate | active | final-signoff | block completion |
| skill | opencode-skill-improver | @skill-improver | active | prompt-change, routing-drift | record improvement note only |
| skill | opencode-system-analyst | @system-analyst | active | requirements-ambiguity, read-only-boundary | implementation handoff only |
| skill | opencode-visual-asset-generator | @visual-asset-generator | active | image-generation, legal-style-equivalent | asset manifest only |
