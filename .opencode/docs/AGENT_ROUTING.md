# Agent Routing

Capability registry: `.opencode/capabilities/registry.json`. Generated advisory view: `docs/generated/capability-matrix.md`.

## Default flow
User intent → `@orchestrator` → specialist agents → validation → `@quality-gate` → final summary.

## Execution posture
- Harness Preflight Gate: before non-trivial work, `@orchestrator` must verify the target project has a current root `AGENTS.md`, canonical `.opencode/docs/`, and root `DESIGN.md` when UI/design work is involved.
- For existing-app and greenfield framework-managed work, preflight also checks `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when present.
- If harness guidance is missing or stale, run `/init-harness` first, or ask the user to run `/init-harness` when command execution is unavailable.
- Do not start broad implementation until harness guidance is available, except for tiny, read-only, or emergency tasks. If skipped, record the reason in the final summary/evidence.
- For implementation requests or plan execution, `@orchestrator` should use a finish-first default: continue work as far as safely and feasibly possible before asking the user follow-up questions.
- Treat gates, phases, work packages, and milestones in a plan as internal checkpoints rather than approval checkpoints, unless an explicit marker such as `requires_user_decision` is present.
- When a blocker appears, investigate first through repo evidence, docs, tools, and the most capable subagent.
- Use blocker taxonomy:
  - `hard_stop`: destructive/irreversible approval boundary, security/privacy/secrets decision boundary, truly unavailable required access/dependency, contradictory requirements, or material non-reversible decision with no safe subset.
  - `soft_blocker`: continue safe subset and record risk.
  - `deferred_question`: queue to final summary.
  - `follow_up`: non-blocking continuation item.
- Advisory lanes are non-veto by default. Advisory labels (`needs-architect-decisions`, `blocked`, `Material block exists`) must be reclassified via taxonomy + repo evidence before stopping.
- Accumulate non-blocking questions and present them at the end together with assumption/risk notes rather than using them to interrupt execution momentum.
- Pause mid-run only for `hard_stop`.

Planner invocation expectation:
- `@artifact-planner` is a **triggered lane**, not default-first.
- Invoke it for multi-phase, spec-heavy, materially ambiguous, or evidence-heavy work.
- Trivial, single-step, and easily reversible tasks may execute directly without planner.
- Trivial, single-step, and easily reversible tasks may execute directly without planner.
- **Plan-first rule**: Non-trivial tasks should route through `@artifact-planner` first before implementation.
- Non-trivial tasks should route through `@artifact-planner` first before implementation.
- Planner handoff quality bar: non-trivial plans must include an explicit `Execution-ready Worklist / Handoff Contract` with ordered atomic tasks, dependencies, owner/lane, validation, exit criteria, blocking status, and a `start_with` first action for orchestrator.
- Handoff confidence bar: worklist tasks must be worker-sized, lane-owned, and executable without replanning; plans must include an execution ownership table, a copy-pasteable Executor Handoff Prompt, Source Anatomy Breakdown per major subsystem, and Reference Map per Feature.

## Compact routing quality checklist
- Non-trivial tasks should route through `@artifact-planner` first.
- Bounded multi-file implementation should route to `@fixer` or a domain lane.
- Final review pass to `@quality-gate` is required before material completion claims.
- Tiny direct orchestrator work is exception-only, not default behavior.

## Worker contract
- Worker agents execute only scoped tasks from `@orchestrator` / plan worklists.
- Workers do not reroute to other agents except explicit final signoff routing.
- Workers do not delegate subtasks.
- Workers report back to `@orchestrator` when done or blocked.

## Plan-bound execution contract (orchestrator)
- Before non-trivial plan-bound work, run a Plan Intake Protocol: read the primary plan and identify mode, Plan Quality Gate value, Execution Source of Truth, Non-negotiable Implementation Invariants, Do Not / Reject If, Diff Boundary, Executor Handoff Prompt, Execution-ready Worklist / Handoff Contract, validation commands, evidence path, and Done Criteria.
- Use Plan Execution Precedence Order when sections conflict: latest explicit user instruction; safety/security/permission rules; Non-negotiable Implementation Invariants; Execution-ready Worklist / Handoff Contract; Acceptance Criteria and Done Criteria; Implementation Steps; follow-ups/recommendations. Record conflicts in verification evidence.
- If a primary plan includes `Execution-ready Worklist / Handoff Contract`, treat it as execution source of truth.
- Start from `start_with` and run all non-blocked tasks in order using declared dependencies/lanes, one ready worklist task at a time.
- Verify each task exit criteria before moving to the next task, including task `must_preserve`, `do_not_touch`, `evidence_update`, and `exit_verification` fields when present.
- Treat milestones/phases as internal progress markers, not stop points.
- Stop only for `hard_stop` conditions or explicit `requires_user_decision` boundaries.
- Advisory/worklist labels using `blocked` must be normalized into the blocker taxonomy before orchestrator decides to stop.
- Multi-file plan-bound implementation routes to `@fixer` or a domain lane by default. Orchestrator direct implementation remains tiny-only except explicit fallback with evidence.
- Before final quality gate, run a Diff Boundary check against allowed file groups, generated-report exceptions, and evidence paths; revert or justify out-of-boundary diffs in verification evidence.
- Completion claim requires finishing every non-blocked task and satisfying plan done criteria. For plan-bound work, completion also requires a Plan Compliance Checkpoint: Done Criteria satisfied, Non-negotiable Implementation Invariants preserved, Do Not / Reject If avoided or remediated, validation recorded, evidence updated, Diff Boundary checked, and quality-gate status recorded.
- `PASS_FOR_SLICE` means slice completion only, not whole-system completion.

## Mode-aware execution contracts

Before non-trivial routing, classify the request into one mode and record the mode in evidence or handoff notes.

See [GREENFIELD_STARTER.md](./GREENFIELD_STARTER.md) for the canonical Greenfield App Accelerator starter matrix, first-slice template, first-slice claim rules, and blocking security/privacy rule.

## Task-size rubric

Use size before lane selection. Size does not override risk triggers.

| Class | Shape | Default route | Completion claim |
|---|---|---|---|
| `tiny` | Single-step, easily reversible, <=1 edited file, <=3 files read, no unknown-scope discovery, no risk trigger | `@orchestrator` may do direct work | Local claim only; no material completion claim |
| `small` | Bounded known-area edit, usually 1-3 files, clear acceptance criteria, no material ambiguity | `@fixer` or domain lane; `@explorer` only if local facts are missing | Claim scoped behavior and validation |
| `material` | Multi-file/cross-area change, public behavior shift, security/privacy/accessibility/release impact, or non-trivial completion claim | `@artifact-planner` when planning depth needed, specialist implementation, then `@quality-gate` | Requires evidence and final gate before completion claim |
| `greenfield` | New app, blank repo, MVP, SaaS/product build, or major product revamp | `@artifact-planner` first, then `@fullstack`/domain lanes from `PASS` or `PASS_FOR_SLICE` plan | Claim `MVP slice complete` unless whole product is truly complete |

## Fast path

Fast path exists for `tiny` work only. It cannot bypass:
- any risk trigger in `AGENTS.md` or this routing doc;
- multi-file thresholds, including code+test/docs pairs that make work `small` or `material`;
- unknown-scope discovery or read-heavy investigation;
- security/privacy/accessibility/release/destructive-action boundaries;
- material completion claims or `@quality-gate` requirements.

Allowed fast path sequence:
1. Confirm `tiny` by rubric.
2. Read only needed local file(s).
3. Make smallest reversible edit.
4. Run targeted validation when feasible.
5. Report scoped result and limits.

If scope grows beyond `tiny`, stop fast path and route to `@fixer`, domain lane, `@explorer`, or `@artifact-planner` as the new size/risk requires.

## Creativity Fast Path

Use for explicit natural-language requests such as `brainstorm`, `explore options`, `generate ideas`, `sketch first`, `prototype cepat`, `draft UI`, `draft copy`, or `jangan terlalu production-grade dulu`.

This mode is:
- opt-in and reversible, never default-on;
- activated by explicit user intent, not by a dedicated command;
- for exploration output, not a production-bypass path.

Allowed scope while the work remains exploratory and reversible:
- option generation, ideation, and bounded first-principles exploration;
- `draft`, `prototype`, or `exploration` artifacts such as copy, wireframes, UX notes, lightweight specs, or throwaway prototypes;
- isolated prototype source edits only when the user explicitly asks, the change is reversible, and no hard rail is touched.

Required output discipline:
- label the result `draft`, `prototype`, or `exploration`;
- record assumptions, confidence, and reversible scope;
- mention repo-local evidence used when it was cheap/relevant, or state that the result is first-principles-driven;
- name skipped heavy gates when the work intentionally stayed exploratory.

Creativity Fast Path cannot bypass:
- `tiny` Fast path limits; `tiny` Fast path stays tiny-only;
- `@artifact-planner` as a triggered lane for multi-phase, spec-heavy, materially ambiguous, or evidence-heavy work;
- `@quality-gate` for material/risky/prompt/config/security/UI completion claims;
- hard rails for secrets, `.env`, credentials, PII, auth/session/token, tenant isolation/RBAC, payments/webhooks, uploads/downloads, biometric/photo/AI data privacy, destructive ops, deploy/release, or permission widening.

Promotion and exit criteria:
- Exit Creativity Fast Path and return to normal routing when the user asks for permanent implementation, material source edits, commit, deploy, release, strong completion claims, or anything crossing a hard rail.
- Before any `done`, `ready`, `production-ready`, `close parity`, or release-ready claim, run a Promotion Gate: route through the normal implementation/validation flow, invoke `@artifact-planner` when the scope now needs it, and require `@quality-gate` wherever the usual material/risky rules apply.
- If the request becomes a new app/MVP/product build, switch to `Greenfield App Accelerator`; if it becomes an existing-app bugfix/refactor, switch to `Maintenance Stability Mode`.

Positive examples:
- `creative`: “brainstorm three onboarding concepts” -> fast exploratory options with assumptions/confidence.
- `prototype`: “draft a landing page hero dulu, belum final” -> labeled prototype output; no final parity claim.
- `creative -> promoted`: “prototype ini bagus, sekarang implementasikan permanen” -> exit fast path and route normally.

Negative examples:
- “bikin prototype login cepat” -> exit fast path because auth/session is a hard rail.
- “ship prototype ini ke production” -> promotion gate first; no direct fast-path completion claim.
- “hapus protections dulu biar cepat” -> reject as security/destructive bypass.

## Maintenance quick contract

Maintenance work defaults to regression-first and minimal:
- classify as `Maintenance Stability Mode`;
- start from repro, failing behavior, regression test, or targeted local evidence;
- preserve existing architecture and UX unless evidence proves they are broken;
- choose smallest safe diff, then validate the touched behavior;
- ask only for material behavior, product, security/privacy, or irreversible decisions;
- route material/risky completion through `@quality-gate`.

Positive examples:
- `tiny`: fix typo in one doc -> fast path okay if no policy/risk trigger.
- `tiny`: rename one local heading in one docs file -> direct edit plus targeted `check:docs`.
- `small maintenance`: update one parser and its unit test -> `@fixer`.
- `small maintenance`: fix one failing evidence manifest field -> regression-first `@fixer` with `check:evidence`.
- `material maintenance`: change routing policy plus docs checks -> plan-bound/specialist implementation and `@quality-gate`.
- `greenfield`: create MVP SaaS first slice -> `@artifact-planner` and [GREENFIELD_STARTER.md](./GREENFIELD_STARTER.md).
- `greenfield`: build public prototype explicitly labeled `prototype` -> may use slice plan/lightweight scaffold, but final claim must stay `prototype` or `MVP slice complete`.
- `UI-heavy`: replicate a reference landing page -> inspect `DESIGN.md`, route UI direction to `@designer`, require browser/reference evidence before done claim.
- `security/destructive`: deploy, rotate token, delete state, or touch PII/auth/payment/upload boundaries -> explicit approval or `hard_stop`; no fast path.

Negative examples:
- Do not use fast path for a 2-file code+test fix; route to `@fixer`.
- Do not skip security/privacy review because first slice is small; risk triggers still apply.
- Do not claim whole app complete from `PASS_FOR_SLICE`; claim only slice status.
- Do not force bugfixes through greenfield product thesis unless the bug requires product/UX decisions.

### Greenfield App Accelerator
Use for new apps, blank repos, MVPs, SaaS/product builds, or major product revamps.

- Always route new app/MVP/SaaS/product builds to `@artifact-planner` before implementation except explicitly tiny prototype-only work labeled `draft`/`prototype`.
- Optimize for the first usable vertical slice, not whole-app perfection.
- Explore 2-3 credible product/UX/architecture options, compare tradeoffs, then converge.
- Allow `PASS_FOR_SLICE` execution when whole-product decisions remain open but the selected slice avoids locking those decisions.
- Allow `@fullstack` to own one bounded greenfield vertical slice when FE/BE coupling is high and contracts are clear enough.
- Allow `@fixer` to scaffold or implement only from a ready slice plan, not from a vague product idea.
- Require enough design direction for MVP usefulness; require the full visual/reference gate only when the work is substantial UI, image-heavy, or parity-driven.
- Final claim should be `MVP slice complete` unless the whole app is actually finished and validated.

### Maintenance Stability Mode
Use for bugfixes, regressions, refactors, dependency updates, small features in existing apps, and incident follow-up.

- Maintenance work should not be forced through greenfield product thesis, 2-3 creative alternatives, or whole-app planning by default.
- Do not require product thesis, 2-3 creative alternatives, or greenfield gates by default.
- Start with repro, regression test, targeted evidence, or clear failing behavior.
- Prefer the smallest safe diff and preserve existing architecture/UX unless the bug proves they are broken.
- Use `@explorer` for local facts, `@fixer` or the domain lane for implementation, and `@quality-gate` for material/risky changes.
- Ask only for material behavior, security, privacy, product, or irreversible decisions.

## Best Practice Readiness Contract
Non-trivial work is not ready to implement until the handoff identifies the mode, goal, non-goals, constraints, acceptance criteria, owner/lane, validation path, evidence path, blocker class, and source strategy. Fresh app/product work must also identify material product, data, auth, payment, privacy, RBAC, platform, UI, and release decisions as answered, deferred, slice-safe, or blocked.

Generator-first readiness: if work creates new framework artifacts, handoff must identify detected stack, official CLI/scaffold/generator/MCP availability, intended generator command/tool path, or manual fallback reason. This applies to existing-app development as well as greenfield work. Use generator-first only when stack evidence supports it; existing generated/customized files may be edited directly for app-specific changes. Before framework-managed edits, handoff should name `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when present, or record `/init-harness` / discovery follow-up when they are missing or stale. Fallback evidence must name the unavailable/failed tool, attempted or skipped command, repo convention, or explicit project/user reason.

## Creative Depth Contract
For Greenfield App Accelerator work, plans must include: product thesis and target pain; 2-3 viable product/UX approaches before choosing one; architecture options with tradeoff scoring; first vertical slice options and chosen-slice rationale; `user journey → data model → API/contracts → UI screens → tests` mapping; design readiness summary; differentiation ideas bounded by MVP scope; reference pack or explicit first-principles rationale for major choices; and readiness status (`draft`, `blocked`, `ready-for-slice`, or `ready-for-implementation`). Plans missing this contract are not execution-ready.

## Plan Quality Gate
Before `@orchestrator` executes a non-trivial plan, classify readiness:

- `PASS`: plan has material decisions, creative alternatives where required, tradeoffs, TDD, validation, and worklist ready.
- `PASS_FOR_SLICE`: whole product has open questions, but the first slice is safe, explicit, and does not lock unresolved decisions.
- `NEEDS_DEPTH`: plan has sections but lacks substance, alternatives, mapping, evidence, or validation detail.
- `BLOCKED`: material decision missing and no safe slice exists.

Only `PASS` and `PASS_FOR_SLICE` may proceed to implementation. `NEEDS_DEPTH` goes back to planner/advisory lanes. `BLOCKED` asks the user or waits for required access/decision.

## Reference-first execution contract
Before planning, routing, implementation, or review on non-trivial work, explicitly decide which evidence sources are required:
- local repo evidence,
- official docs/versioned API references,
- upstream source/examples/issues,
- browser/screenshots/reference URLs,
- current web research.

Rules:
- If a reasonable source exists for a material claim or decision, use it or state why it was skipped.
- Do not present assumptions as facts.
- Record assumptions as `assumed`, `source-missing`, or `user-approved` in evidence/handoff notes.
- When references and repo/runtime evidence conflict, surface the conflict and prefer the most authoritative/current source rather than following the checklist mechanically.

## Verify-before-claim contract (orchestrator)
Default mode is no assertion without verification. Every factual claim about the user's code, runtime, environment, dependency state, configuration, or external service behavior MUST be backed by a tool call (or subagent report) that produced that fact in the same response or in a response the user can see. A bare prose answer about code or runtime state is a defect, not a stylistic choice.

Mandatory verification tool calls by claim class:
| Claim pattern | Required verification |
|---|---|
| "File X contains Y" / "config C is set to V" | `read_file` / `cat` / `grep` / `search_files` |
| "Function Z is defined in module M" | `grep -n` / `search_files` |
| "Service S runs on port P" | `ss -tlnp` / `curl localhost:P/health` |
| "Package P version is V" | `pip show` / `npm ls` / `cat package.json` |
| "Doc/source D says X" | `@librarian` / `web_extract` / `context7` |
| "Previous session/conversation did X" | `session_search` |
| "Reference R uses pattern P" | `@visual-context-extractor` (image) / `web_extract` (URL) |
| "Container C is running" | `docker ps` / `podman ps` / `systemctl status` |
| "Env var E is set" | `printenv` / `grep .env` |

Claim-level vocabulary (mandatory in evidence; preferred in user-facing prose where the distinction matters):
- `confirmed_repo` — backed by `read_file`/`grep`/`cat` result this response.
- `confirmed_runtime` — backed by `terminal` command output this response.
- `confirmed_docs` — backed by `@librarian`/`web_extract`/`context7`/`web_search` this response.
- `user_confirmed` — explicitly stated by the user in the current or recent session.
- `assumption` — orchestrator's inference, not yet verified.
- `unverified` — orchestrator could not verify but is forwarding the claim.

Anti-patterns (route back to planner or escalate when observed):
- Forwarding a subagent's prose as fact without independent verification. Subagent prose is `assumption` until spot-checked.
- Inventing file paths, function names, library APIs, package names, config keys, or env var names by intuition even when the gap "feels small". Use `clarify` with multiple-choice when ≥2 plausible matches exist.
- Stating "the file contains...", "the service is running...", or "the package is installed..." in user-facing prose without a tool call having produced that fact in the same response.
- Issuing a final completion claim without a screenshot or runtime output for visual changes, or without a build/test/lint pass for non-visual changes.

Mechanical helper: `python3 ~/.config/opencode/scripts/verify-before-claim-check.py <evidence-or-response-path>` flags confident claims that lack a matching tool call or self-label. Use it in audits and CI. Orchestrators should be able to defend any flagged claim.

## Adaptive creativity contract
Creativity is required for greenfield, ambiguous, or taste-sensitive work, but it must be grounded.
- Generate 2-3 bounded product/UX/architecture/design options when doing so materially improves quality.
- Score or compare options using references, constraints, and risks before converging.
- Do not confuse creativity with inventing APIs, product requirements, assets, or technical facts.
- If no reliable reference exists, say the output is first-principles-driven and keep the decision reversible.

## Direct-work thresholds for `@orchestrator`
`@orchestrator` is a router/integrator first, not the default worker. Direct execution is allowed only for tiny tasks.

`@orchestrator` may act directly only when **all** conditions are true:
- scope is trivial, single-step, and easily reversible,
- at most 1 file is edited,
- at most 3 files are read for local confirmation,
- no unknown-scope discovery is required,
- no risk trigger/domain specialist lane is required.

`@orchestrator` must delegate by default when one of these is true:
- discovery is unknown-scope, cross-area, or read-heavy (>3 files) → `@explorer`,
- implementation is bounded but touches 2+ files (including code+test/docs pair) → `@fixer`,
- work creates generator-backed framework artifacts → matching domain lane (`@backend`, `@frontend`, `@mobile`, `@devops`, or `@fullstack`) unless it only customizes existing files or generator is irrelevant,
- work is multi-phase, spec-heavy, materially ambiguous, or evidence-heavy → `@artifact-planner`,
- change is material and needs completion claim → final pass through `@quality-gate`.

Permitted fallback: if a specialist is unavailable, use the next safest lane and record the limitation explicitly in final evidence.

## Routing anti-patterns (and remediation)
- Anti-pattern: delegate discovery to `@explorer`, then `@orchestrator` still reads many files and redoes discovery.
  - Remediation: consume explorer output; only perform minimal spot-check reads.
- Anti-pattern: `@orchestrator` performs multi-file implementation directly because "it is faster".
  - Remediation: route bounded implementation to `@fixer`.
- Anti-pattern: complex/ambiguous work starts without a plan/evidence path.
  - Remediation: route to `@artifact-planner`, then implement plan-bound.
- Anti-pattern: completion claim on material change without `@quality-gate`.
  - Remediation: run final conformance gate before claiming done.

## Compact routing quality checklist
Use this quick rubric for real workflow audits:

- [ ] **Lane fit**: discovery/implementation/review went to the expected primary lanes.
- [ ] **Threshold compliance**: orchestrator direct work stayed within tiny-task limits.
- [ ] **Planner triggered correctly**: complex/ambiguous/evidence-heavy work is plan-bound before implementation.
- [ ] **Evidence legibility**: delegation choices and fallback reasons are explicitly recorded.
- [ ] **Final gate**: material changes include `@quality-gate` pass/verdict.

Score guidance: 5/5 = strong routing discipline; 3–4/5 = acceptable with minor drift; ≤2/5 = routing failure requiring remediation.

## Core agents (default operating model)

Cross-lane contract baseline (non-trivial work):
- Typed output schema fields: `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence`.
- Typed schema is internal coordination contract and non-user-facing.
- Orchestrator must normalize internal outputs before user-facing final response; never pass raw internal labels directly.
- Validation ladder: plan/handoff check → discovery/research evidence → implementation/docs change → diff review → targeted validation commands → `@quality-gate` for non-trivial/risky completion claims.
- LSP-first for rename/refactor/navigation/diagnostic-driven edits where available; fallback to `glob`/`grep`/`read` + minimal edits must be recorded in evidence when confidence drops.
- `@orchestrator` — router, integrator, final coordinator
- `@explorer` — codebase discovery and reuse mapping
- `@fixer` — bounded implementation, tests, Red/Green/Refactor
- `@designer` — UI/UX direction, blueprint, reference parity, motion strategy, accessibility expectations, and design handoff
- `@design-system-engineer` — tokens, primitives, theming, component APIs, and reusable UI foundations
- `@oracle` — architecture, maintainability, simplification, deep review
- `@quality-gate` — final conformance and risk review

## Triggered planning lane
- `@artifact-planner` — planning artifacts and evidence paths under `.opencode/`.
- Trigger only when scope/ambiguity/evidence needs justify planning overhead.

## Helper lanes (triggered)
- `@architect` — unified read-only advisory lane for product/SaaS, platform/runtime/release/mobile, AI/LLM/RAG/evals, and UI-system architecture boundaries.
- `@artifact-planner` — planning artifacts and evidence paths under `.opencode/`.
- `@librarian` — supporting docs/API research helper and document-centric read-only extraction/research/transformation support.
- `@skill-improver` — prompt/skill/routing improvements after repeated failure or evidence.

## Visual context extraction
- `@visual-context-extractor` is mandatory first lane for visual understanding from screenshots, images, mockups, diagrams, and other visual files.
- No agent except `@visual-context-extractor` may self-infer visual context from image input. Agents needing visual understanding must route/request extractor first, then continue with their own lane-specific decisions.
- Callable by all agents via `@orchestrator`. Direct call allowed only when caller `task` permission allows delegation to `visual-context-extractor`.
- Returns structured JSON (`visual_context_extractor.v1`) only. No design critique, no parity claim, no image generation, no source edits.
- If no vision input is available, helper must return `status: "unavailable"` with `fallback_suggestion`; it must not fabricate understanding.
- Downstream interpretation and decisions still belong to the receiving lane such as `@designer`, `@fixer`, `@frontend`, `@quality-gate`, or other relevant specialist.

| Caller | Callable? | Notes |
|---|---|---|
| All agents | via `@orchestrator` | Default supported path |
| `@orchestrator` | direct | Primary router/integrator |
| `@artifact-planner`, `@fixer`, `@designer`, `@frontend`, `@backend`, `@mobile`, `@fullstack`, `@oracle`, `@quality-gate`, `@system-analyst`, `@project-manager`, `@librarian`, `@skill-improver`, `@architect`, `@visual-asset-generator`, `@council`, `@explorer` | direct only if caller task permission allows | Otherwise route via `@orchestrator` |

## Domain subagents (triggered only)

These agents are `mode: subagent`. `@orchestrator` remains default. `@artifact-planner` remains triggered, not default-first.

| Agent | Owns | Route when | Do not route when |
|---|---|---|---|
| `@design-system-engineer` | Shared UI foundation | tokens, primitives, theme variables, reusable component APIs, icon grammar, `DESIGN.md`-aligned design-system implementation | Missing design grammar or visual direction -> `@designer`; app-screen implementation belongs downstream in `@frontend`/`@mobile` |
| `@frontend` | Web UI implementation | React/Next/Vue/Svelte components, pages, forms, state, routing, API integration, component tests, accessibility implementation | Read project stack/command/playbook docs first for framework-managed artifacts; visual direction is missing -> `@designer`; shared primitives/theme work -> `@design-system-engineer`; backend contract unclear -> `@backend`/`@system-analyst` |
| `@mobile` | Mobile implementation | React Native, Expo, Flutter, navigation, native permissions, offline, push, camera, deep links, mobile performance | Read project stack/command/playbook docs first for framework-managed artifacts; visual direction is missing -> `@designer`; shared primitives/theme work -> `@design-system-engineer`; mobile architecture/privacy/store boundary needs decision -> `@architect`/`@quality-gate` |
| `@backend` | API/server/data implementation | Endpoints, services, validation, auth integration, DB queries, migrations, jobs, queues, backend tests | Read project stack/command/playbook docs first for framework-managed artifacts; requirements/API contract unclear -> `@system-analyst`; major data/security architecture -> `@architect`/`@quality-gate` |
| `@devops` | CI/CD, Docker, env, deploy, monitoring | GitHub Actions, Dockerfile, compose, release scripts, observability config, rollback plans | Read project stack/command/playbook docs first for framework-managed artifacts; deploy/destructive/credential action lacks explicit approval; architecture/release boundary -> `@architect`/`@quality-gate` |
| `@system-analyst` | Read-only requirements/contracts | PRD, user flows, API contracts, data flows, edge cases, NFRs, acceptance criteria | Source edits or tests are requested -> implementation lane |
| `@project-manager` | Read-only delivery planning | Milestones, backlog, issue breakdown, dependency/risk register, release checklist, handoff | Requirements unclear -> `@system-analyst`; source edits requested -> implementation lane |
| `@fullstack` | Small vertical slice | Tight, clear FE/BE change with small scope and known contract | Broad scope, unknown contracts, or multi-subsystem work -> split `@frontend` + `@backend` or plan first |

Domain anti-overlap rules:
- UI/UX direction stays with `@designer`; `@frontend` and `@mobile` implement from direction.
- Shared tokens/primitives/themes/component APIs stay with `@design-system-engineer` before screen-level implementation.
- `@fullstack` is never catch-all/default. Split once scope grows or contracts are unclear.
- Read-only agents (`@system-analyst`, `@project-manager`) must not edit source.
- `@devops` must ask before deploy, destructive infra, credential, or production mutation commands.

Document fallback rule:
- If a user asks to read, summarize, compare, or transform PDF/DOCX/XLSX/PPT/Office input and the active model reports no direct attachment support (for example `input.pdf:false`), do not stop at the model capability check. Treat it as a direct-attachment limitation, check whether the file is available in the workspace, then route to `@librarian` for document-centric extraction. Ask the user to convert the file only after the `@librarian` lane or local extraction tools are unavailable or fail.

Helper lanes are conditional. Tiny UI polish still routes to `@designer`; isolated bugfixes still route to `@fixer` unless a risk trigger applies.

Global conditional specialist framing:
- PRD/product blueprint work, SaaS architecture, AI system design, Security/privacy review, Release/ops readiness, and Mobile/hybrid architecture can trigger `@architect`.
- Tiny UI polish still goes to `@designer`; broader design ambiguity still goes to `@designer`.
- Shared design-system/token/primitive/theme work goes to `@design-system-engineer`.
- Isolated bugfixes still go to `@fixer`.
- Web implementation with existing design direction can route to `@frontend`.
- Backend/API/data implementation can route to `@backend`.
- Mobile app implementation with existing design direction can route to `@mobile`.
- CI/CD/Docker/env/deploy work can route to `@devops` with approval gates.
- Requirements/contract clarification can route to `@system-analyst`.
- Milestone/backlog/release planning can route to `@project-manager`.
- Small FE/BE vertical slices can route to `@fullstack`; split when scope grows.

## UI and reference policy
- First inspect the target project's `DESIGN.md`.
- If missing, inspect `design-system/DESIGN.md` or equivalent.
- Suggest `/init-harness` for substantial UI work without project-local guidance so consolidated harness/design initialization can create or update `DESIGN.md`.
- Avoid generic UI, numeric-only service icons, and blank image frames.
- Require visual density, production-like screenshots, designer signoff, and reference/current/final evidence for substantial UI/reference work.
- Generic hover-only motion is not enough for substantial reference work.
- Treat image-heavy work explicitly with an image generation decision, direct reuse inventory, and style-equivalent generation fallback when needed.
- `@visual-asset-generator` is invoked by `@orchestrator`/`@designer` from an asset manifest or image-heavy UI plan; `@artifact-planner` does not invoke generation lanes.
- Do not leave final sections as CSS placeholders when imagery materially affects quality.

## General Design Readiness Gate
For substantial UI/UX work, high-level visual direction is not enough. Require a UI/UX Design Blueprint with:
- Experience direction
- Page-by-page UX blueprint
- Section-level visual specification
- Component system plan
- Visual system
- Asset and image decision
- Motion system
- Interaction and state design
- Responsive plan
- Accessibility gate
- Validation evidence

If the blueprint is incomplete, status must be `blocked`, `needs-polish`, or `draft`, not `done`.

## Risk triggers
- auth, PII, tenant isolation, payment, upload, secrets, token/session handling, biometric data, permission/RBAC → final security/privacy assessment in `@quality-gate`; use `@architect` for upstream architecture decisions
- architecture boundary, new abstraction, large refactor, dependency direction, data model change → oracle
- visual layout change, animation/motion direction, design token, screenshot/reference parity, responsive behavior → `@designer` for design direction; shared tokens/primitives/component APIs → `@design-system-engineer`; final accessibility/visual-parity signoff when material → `@quality-gate`
- CI/CD, deployment, env var, migration, monitoring, rollback, mobile/offline/push/deep-links/platform runtime constraints → `@architect`
