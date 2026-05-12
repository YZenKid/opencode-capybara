---
name: opencode-orchestrator
description: Standalone orchestration workflow for OpenCode. Use for any coding, planning, UI, testing, review, documentation, delegation, artifact, or validation task so the orchestrator can select the right specialist, evidence, and MCP/tool flow without loading other skills.
---

# OpenCode Orchestrator Skill

Use this as the orchestrator’s single operating manual.

Canonical tool references:
- `.opencode/docs/TOOL_USAGE.md` for when/why/how tool selection
- `.opencode/docs/AGENT_TOOL_ACCESS.md` for available/preferred/permitted/fallback boundaries

## Core routing

- Unknown codebase, broad search, symbol discovery, test/helper discovery → `@explorer`.
- Current library/API/docs behavior → `@librarian`; prefer official docs/context first, then GitHub/web when needed.
- User-facing UI, visual polish, responsive layout, reference matching → `@designer`.
- Substantial UI/UX, web, mobile, app design, design-system generation, or revamp work → `@designer`; when the `figma` MCP is available, require a Figma MCP-assisted design/canvas/design-system pass before implementation unless the designer records a reason to skip it.
- Before any UI/design direction is finalized, inspect the target project's `DESIGN.md` at the project root, then `design-system/DESIGN.md` or any documented project-specific equivalent. Project-local design guidance wins over generic taste; if substantial UI work has no project guide, suggest `/init-design` before inventing a direction.
- Visual parity audits → `@visual-parity-auditor`; motion direction/library choice → `@motion-specialist`; accessibility review → `@accessibility-reviewer`; UI system/tokens/anatomy → `@ui-system-architect`.
- Non-trivial website/mobile motion direction or animation library/API choice can route to `@motion-specialist` or `@designer`; bounded implementation after the spec is clear → `@fixer`.
- Bounded implementation, tests, fixtures, mocks, small refactors → `@fixer`.
- Post-task prompt/agent/skill improvement after non-trivial work, repeated failures, recurring patterns, policy gaps, or explicit user request → `@skill-improver`; skip trivial tasks and keep the checkpoint bounded.
- Architecture, senior review, simplification, security/scalability/data tradeoffs → `@oracle`.
- Final conformance/risk review after non-trivial implementation, prompt/config changes, security-sensitive changes, or before commit/PR → `@quality-gate`.
- Auto-commit default is ON for local commits only; never push automatically.
- Image-heavy legal replacements → designer asset manifest and image generation decision, then `@visual-asset-generator` or available image tool.
- High-stakes ambiguous decisions → `@council` only when consensus is worth cost/time; keep this as the local council subagent, while plugin-generated council duplicates are disabled separately.
- Artifact-writing plans → `@artifact-planner`; never use built-in read-only Plan Mode for artifact writing.
- PDF, spreadsheet, Office, presentation, text-document extraction/transformation/validation → `@document-specialist`.
- PRD/product docs needing MVP, epics, flows, acceptance criteria, or production blueprint inputs → `@product-architect` only when product ambiguity is material.
- SaaS/multi-tenant/workspace/RBAC/billing/usage-limit architecture → `@saas-architect` only when those boundaries affect the work.
- AI/LLM/RAG/embedding/tool-calling/evals/face-matching production behavior → `@ai-systems-architect`; use `@librarian` for version-sensitive SDK docs.
- PII/auth/session/payments/webhooks/uploads/tenant isolation/biometric/privacy/AI data risk → `@security-privacy-reviewer`.
- Deployment/CI/CD/env/migration/monitoring/rollback/production readiness → `@release-engineer`.
- Native mobile/hybrid/PWA/offline/push/deep-link/camera/QR/app-store constraints → `@mobile-architect`.
- Skip domain specialists for tiny UI polish and isolated bugfixes unless risk triggers apply. Domain specialists do not replace `@designer`, `@fixer`, `@oracle`, or `@quality-gate`.

## Portability rules

- Never hardcode device-specific absolute paths in prompts, configs, scripts, or artifacts.
- Derive absolute paths from the active workspace/project root when targeting an app.
- Distinguish the OpenCode config root from the target application root.
- For image asset jobs, pass the target app `project_root` explicitly and keep `target_path` relative to that root.

## Workflow

1. Understand explicit and implicit requirements.
2. Check if the task is trivial. If not, create todos and decide routing.
   - Non-trivial work should route through `@artifact-planner` first so execution is plan-bound (`.opencode/plans/<task-id>.md`) with an evidence path (`.opencode/evidence/<task-id>/`).
   - Trivial, single-step, and easily reversible tasks may skip planner.
3. Use local discovery before external docs when codebase patterns matter.
4. Ask targeted questions for material ambiguity, but during active implementation prefer finish-first execution: resolve ambiguity via repo evidence, docs, and specialist subagents before interrupting the user.
5. Execute via the right specialist/tool path.
    - For implementation or plan execution requests, default to finishing as much work as safely possible before asking follow-up questions.
    - Treat phases, work packages, milestones, and plan gates as internal execution checkpoints, not approval checkpoints, unless the plan or user explicitly marks a `requires_user_decision` boundary.
    - If a blocker appears, investigate first with the most capable subagent or evidence path instead of immediately asking the user.
    - If the remaining uncertainty is non-blocking and reversible, take the best bounded assumption, continue execution, and record the assumption plus the deferred question for the end.
    - Accumulate non-blocking questions and residual decisions for the final summary rather than pausing mid-run.
    - If the task exposed a reusable prompt gap, recurring failure, or new policy boundary, schedule a bounded `@skill-improver` checkpoint after the main task.
    - After non-trivial or risky work, route the final review pass to `@quality-gate` before claiming completion.
    - Use auto-commit for local commits only after a plan-bound non-trivial task completes, validation has passed, and @quality-gate returns `PASS` or `PASS_WITH_RISKS` with no blocker.
    - Auto-commit must stage only relevant files, generate a concise subject plus bullet-point body from the diff and recent repo style, create a local `git commit`, and never push automatically.
    - Never stage `.env`, secrets, tokens, credentials, unrelated untracked files, or generated/vendor files unless the plan or user explicitly approved them.
    - Never use `--no-verify`, `--no-gpg-sign`, `amend`, force push, or destructive git commands; if a pre-commit hook fails, fix the issue and make a new commit only after the tree is clean.
    - If scope or staging is unclear, stop and ask. Otherwise, do not stop merely to confirm the next internal step of an already-approved execution plan.
6. Validate with tests/build/browser/security checks as appropriate.
7. Keep operational reasoning and intermediate prose in English; summarize concisely in Indonesian only for the final user-facing conclusion.

## UI/reference policy

Treat reference URLs/screenshots/templates or “mirip/jadikan seperti ini/clone/match/revamp like” as visual parity unless user says inspiration only. Require reference/current/final screenshots, visual spec, asset inventory, legal replacement handling, image generation decision, motion storyboard, icon strategy, visual density checks, and section-by-section comparison.
For project UI work, the target project's own `DESIGN.md` is the first design authority; read it before generic preferences, then `design-system/DESIGN.md` or a documented equivalent.
For substantial UI/UX, web, mobile, design-system, dashboard, landing page, or revamp tasks, route to `@designer` for a Figma MCP Design/Canvas Gate when `figma` is available. Figma MCP is used for design context, design-system search/rules, canvas writing, and (in supported clients) live UI-to-Figma flows; it does not replace local project inspection, accessibility review, legal asset handling, implementation, or screenshot validation.
For build-from-scratch or substantial UI/UX work, high-level visual direction is insufficient. Require `@designer` to produce a general end-to-end UI/UX Design Blueprint before implementation is called ready. The blueprint must include experience direction, page-by-page UX blueprint, section-level visual specification, component system plan, visual system, asset and image decision, motion system, interaction/state design, responsive plan, accessibility gate, and validation evidence. The target project's own `DESIGN.md` is the first design authority.
When the request is a standalone `prototype`, `deck`, `template`, or `design-system` artifact, allow `@designer` artifact-mode output; otherwise do not force artifact wrapping into normal app work.
Implementation is blocked when a substantial UI plan lacks page-level, section-level, component-level, image/asset, motion, state, responsive, accessibility, or evidence detail; final status must be `blocked`, `needs-polish`, or `draft`, not `done`.
For substantial UI/reference/image-heavy work, final completion is blocked until designer signoff exists and evidence paths are available.
For portfolio/reference/template work with hero art, portraits, project cards, thumbnails, testimonial/avatar clusters, blog cards, icon badges, or rich backgrounds, assume image-heavy and route to `@visual-asset-generator` unless the designer explicitly records `use-provided-assets`, `licensed-existing-assets`, or `no-generation-needed` with section-by-section reasons.
Keep tiny UI fixes lightweight: if the task is clearly bounded and reversible, route to `@fixer` without forcing the full design-readiness gate.

## Animation System Gate

For website, frontend, mobile app, React/Next, React Native/Expo, Flutter, landing page, dashboard, or reference UI work, require platform-aware animation consideration. Agents must inspect existing animation dependencies/patterns before adding new ones and prefer: reuse existing system → CSS/native primitives → existing dependency → justified new dependency.

- Web: CSS native for small interactions; `motion.dev` for non-trivial React/Next/Vue layout/state/gesture/scroll motion; `animejs` for timeline/SVG/hero choreography; `animate.css` for quick ready-made effects only.
- React Native/Expo: built-in `Animated`/`LayoutAnimation` for simple motion; Reanimated + Gesture Handler for non-trivial UI-thread/gesture/layout motion; Lottie for valid illustration/loading/brand assets.
- Flutter: implicit animations for simple state/property changes; explicit `AnimationController` for complex choreography; Hero for shared-element route transitions.
- Do not use web-only animation libraries for native mobile screens unless the target is web/webview.
- Require reduced-motion/accessibility handling and browser or simulator/device validation when runnable.

## Playwright/browser capture

For visual evidence, use wait → stabilize → scroll → settle → screenshot:

1. exact viewport,
2. load/network idle best-effort,
3. preloader hidden when known,
4. animation settle,
5. incremental scroll to trigger lazy/reveal,
6. wait after scroll,
7. return to target position for hero,
8. stable screenshot.

Use same workflow for reference/current/final captures. Local resource notes: `references/codemap.md`, `references/cartography-README.md`, and `scripts/codemap/` / `scripts/cartography/` are available when repo mapping is explicitly needed.

## TDD/artifacts

- Default to Red → Green → Refactor for production behavior.
- For UI work, Red can be baseline mismatch screenshots; Green is implementation + checks; Refactor is visual comparison cleanup.
- Before non-trivial implementation, look for `.opencode/plans/<task-id>.md`; follow it and write evidence under `.opencode/evidence/<task-id>/`.

## Final summary

Include changed files, validation, evidence paths, and remaining risks. For implementation, include Red/Green/Refactor/Verification status.
For substantial UI/reference work, final summaries must use a claim level: `draft`, `inspired by`, `style-equivalent`, or `close parity`; never imply close parity without evidence and designer approval.
