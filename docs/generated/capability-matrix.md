# Generated: Capability Matrix

Generated from `.opencode/capabilities/registry.json`. Advisory only; canonical policy remains in `.opencode/docs/`.

- Agents: 10
- Skills: 23

| Type | Name | Owner lane | Status | Risk | Fallback |
| --- | --- | --- | --- | --- | --- |
| agent | architect | @architect | active | architecture-advice, read-only-boundary | @oracle for review or @artifact-planner for plan artifacts |
| agent | artifact-planner | @artifact-planner | active | plan-artifact-write, scope-bloat | @orchestrator routing or retained specialist lane |
| agent | designer | @designer | active | ui-change, accessibility, visual-parity | @orchestrator routing or retained specialist lane |
| agent | explorer | @explorer | active | read-only-discovery, stale-map | targeted glob/grep/read by @orchestrator |
| agent | fixer | @fixer | active | code-edit, test-impact | @orchestrator routing or retained specialist lane |
| agent | librarian | @librarian | active | external-research, read-only-boundary | local docs first, then no external lookup |
| agent | oracle | @oracle | active | review-advice, read-only-boundary | @quality-gate for final conformance |
| agent | orchestrator | @orchestrator | active | routing, integration, scope-control | specialist lane or user clarification |
| agent | quality-gate | @quality-gate | active | final-signoff, read-only-boundary | block completion and return residual risks |
| agent | visual-context-extractor | @visual-context-extractor | active | read-only-boundary, pii-handling, overclaim | return status:unavailable when no vision input; orchestrator routes critique to @designer and source edits to @fixer |
| skill | opencode-architect | @architect | active | architecture-advice | @oracle review |
| skill | opencode-artifact-planner | @artifact-planner | active | plan-artifact-write | @orchestrator routing |
| skill | opencode-backend | @fixer | active | api-change, data-change, auth-integration | @artifact-planner on-demand owner |
| skill | opencode-council | @artifact-planner | active | expensive-consensus | @artifact-planner on-demand owner |
| skill | opencode-design-system-engineer | @designer | active | shared-ui-foundation, token-primitive-api-change | @artifact-planner on-demand owner |
| skill | opencode-designer | @designer | active | ui-change, accessibility | @frontend/@mobile/@design-system-engineer for implementation |
| skill | opencode-devops | @fixer | active | deploy, destructive-infra, secrets | @artifact-planner on-demand owner |
| skill | opencode-explorer | @explorer | active | read-only-discovery | targeted local search |
| skill | opencode-fixer | @fixer | active | code-edit, test-impact | @artifact-planner |
| skill | opencode-frontend | @fixer | active | web-ui-change, accessibility, api-integration | @artifact-planner on-demand owner |
| skill | opencode-fullstack | @fixer | active | cross-layer-change, scope-creep | @artifact-planner on-demand owner |
| skill | opencode-librarian | @librarian | active | external-research | local docs only |
| skill | opencode-mobile | @fixer | active | native-permissions, privacy, mobile-runtime | @artifact-planner on-demand owner |
| skill | opencode-oracle | @oracle | active | review-advice | @quality-gate |
| skill | opencode-orchestrator | @orchestrator | active | routing, integration | user clarification |
| skill | opencode-plan-reviewer | @artifact-planner | active | requirements-ambiguity, read-only-boundary | @artifact-planner on-demand owner |
| skill | opencode-plan-validator | @artifact-planner | active | plan-artifact-write, contract-drift | @artifact-planner on-demand owner |
| skill | opencode-project-manager | @artifact-planner | active | delivery-plan, read-only-boundary | @artifact-planner on-demand owner |
| skill | opencode-quality-gate | @quality-gate | active | final-signoff | block completion |
| skill | opencode-skill-improver | @artifact-planner | active | prompt-change, routing-drift | @artifact-planner on-demand owner |
| skill | opencode-system-analyst | @artifact-planner | active | requirements-ambiguity, read-only-boundary | @artifact-planner on-demand owner |
| skill | opencode-visual-asset-generator | @designer | active | image-generation, legal-style-equivalent | @artifact-planner on-demand owner |
| skill | opencode-visual-context-extractor | @visual-context-extractor | active | read-only-boundary, pii-handling, overclaim | orchestrator routes critique to @designer and source edits to @fixer |
