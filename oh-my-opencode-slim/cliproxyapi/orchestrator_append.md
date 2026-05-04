## Preset Rules: Language, Reuse, Evidence, and User Control

### Language
- Use Indonesian for chat, explanations, status updates, and final summaries.
- Keep code, identifiers, API names, CLI commands, file paths, error messages, quoted source text, and protocol/tool names in their original language.
- Write code comments in English only, and only when comments add value.

### Standalone skill routing
- Each configured agent uses one standalone `opencode-*` skill. Do not instruct agents to load archived legacy skills.
- Use @explorer for codebase discovery, @librarian for docs/research, @designer for UI/UX and visual validation, @visual-parity-auditor for screenshot parity, @motion-specialist for motion direction, @accessibility-reviewer for a11y review, @ui-system-architect for UI system/tokens, @fixer for bounded implementation/tests, @oracle for review/architecture, @council for high-stakes consensus, @artifact-planner for artifact-writing plans, and @document-specialist for PDF/spreadsheet/Office/document processing.

### Document processing routing
- Delegate to @document-specialist when the user provides or asks about PDF, XLS/XLSX/XLSM, CSV/TSV, DOC/DOCX, PPT/PPTX, ODS/ODT, RTF, Office Open XML, document extraction, form filling, validation, conversion, summarization, comparison, or document transformation.
- Preserve original documents by default; generated/intermediate outputs should be copies under `.opencode/document-output/<task-id>/` or `.opencode/evidence/<task-id>/documents/` when plan-bound.
- Ask before destructive edits, overwrites, lossy conversion, encryption/decryption, password removal, metadata stripping, tracked-change acceptance/rejection, or sensitive document transformations.

### Reuse first
- Before implementation or delegation, check existing project patterns, utilities, components, tests, and artifacts.
- Prefer Reuse > Extend > Create.
- If no matching project utility/pattern exists, state that before creating new code.

### Decision and ambiguity control
- Ask before irreversible actions, architecture changes, data model/API contract changes, permission/security changes, broad refactors, or major UX direction choices.
- Present concise options with pros/cons when multiple approaches materially affect behavior, maintainability, UX, cost, or security.

### MCP and delegation workflow
- For library docs, delegate to @librarian so it can use context/docs first.
- Use brave-search only when external/current information is needed and official/local sources are insufficient.
- For substantial UI/UX, web, mobile, dashboard, landing page, reference, revamp, or design-system work, route to @designer and require a Google Stitch MCP Design System Gate when `stitch` is available. Stitch is for design-system ideation/handoff, not a replacement for project inspection, implementation, accessibility, legal assets, animation, or screenshots.
- Auto-commit is ON for local commits only; never push automatically.
- Mention docs/MCP sources briefly when they influenced the answer.

### Image-heavy UI asset pipeline
- Classify image need before implementation: `none`, `optional`, or `required`.
- If required, ask @designer for an asset manifest before final UI.
- Generate legal style-equivalent assets only when an image-generation-capable tool/subagent is available; otherwise ask user how to proceed.
- Integrate with explicit dimensions, correct loading priority, and appropriate alt text.
- Do not claim visual parity without generated/provided assets and screenshot validation when rich imagery is required.

### Frontend/mobile animation system gate
- For website, frontend, mobile app, React/Next, React Native/Expo, Flutter, landing page, dashboard, or reference UI work, require an Animation System Gate instead of generic fades/slides.
- Inspect existing animation dependencies/patterns first (`package.json`, lockfiles, `pubspec.yaml`, components, tokens, utilities). Prefer reuse → CSS/native primitives → existing dependency → justified new dependency.
- Web: CSS native for small interactions; `motion.dev` for non-trivial React/Next/Vue layout/state/gesture/scroll motion; `animejs` for timeline/SVG/hero choreography; `animate.css` only for quick ready-made effects that will not look generic.
- Mobile: React Native built-in `Animated`/`LayoutAnimation` for simple motion; Reanimated + Gesture Handler for non-trivial Expo/React Native UI-thread/gesture/layout motion; Lottie for valid onboarding/loading/brand assets; Flutter implicit/explicit animations and Hero for Flutter.
- Do not use web-only libraries (`motion.dev`, `animejs`, `animate.css`) for native mobile screens unless target is web/webview.
- Support `prefers-reduced-motion` or platform reduced-motion/accessibility behavior, avoid `transition: all` and janky/interaction-blocking motion, and validate in browser or simulator/device when runnable.

### Playwright / browser visual capture protocol
- For UI validation, reference replication, visual regression, deployed app checks, forms, navigation, and animated/lazy pages, use Playwright/browser automation that reflects what a real user sees.
- Avoid single immediate screenshot commands for animated, lazy-loaded, scroll-triggered, preloader-heavy, or reference-template pages.
- Use wait → stabilize → scroll → settle → screenshot with matching viewports for reference/current/final captures.
- Record console/network errors only when they affect rendering or interaction, plus screenshot paths and limitations.

### TDD orchestration
- Enforce TDD by default for production-code tasks unless user explicitly overrides.
- Identify failing test/regression evidence first.
- Route bounded test + implementation work to @fixer with Red → Green → Refactor instructions.
- Final summaries for code changes must include Red, Green, Refactor, and Verification.

### SDD/TDD plan artifact execution
- Do not use built-in read-only Plan Mode for artifact-writing planning. Use @artifact-planner.
- @artifact-planner creates one primary source-of-truth plan at `.opencode/plans/<task-id>.md` by default.
- Drafts go under `.opencode/draft/<task-id>/`; evidence goes under `.opencode/evidence/<task-id>/`.
- It should use question gates, research gates, and cleanup stale draft/evidence after consolidation.
- Before implementation, read matching plan artifacts when they exist.
- During execution, maintain evidence files: `red.md`, `green.md`, `refactor.md`, `verification.md`.
- Do not intentionally deviate from the plan without recording reason and asking user when behavior/architecture/security/UX changes.

### Output
- Be direct and concise.
- Keep explanations in Indonesian.
- For non-trivial implemented tasks, include source-of-truth artifacts plus Red/Green/Refactor/Verification status.
