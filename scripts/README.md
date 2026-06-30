# OpenCode Governance Scripts

These scripts live under `~/.config/opencode/scripts/` and are designed to be invoked from **any project directory**.

All scripts are self-contained Python files with no external package dependencies beyond the Python standard library.

## Cross-project usage pattern

From any project root, run scripts with the full path and pass `--project-root .` when supported:

```bash
python3 ~/.config/opencode/scripts/<script>.py --project-root .
```

When a command should operate on a specific task, pass the task id as required.

## Available scripts

### project-memory.py
Project knowledge memory. Stores reusable lessons, pitfalls, patterns, and decisions per project at `.opencode/memory/`.

**Files managed**:
- `.opencode/memory/knowledge.json` — active memories
- `.opencode/memory/archive.json` — archived memories
- `.opencode/memory/proposals.json` — pending proposals awaiting review

**Save a memory directly**:
```bash
python3 ~/.config/opencode/scripts/project-memory.py \
  --save \
  --task <task-id> \
  --category pitfall \
  --importance high \
  --lesson "Serwist route handler must wrap dynamic APIs; static export breaks /api/health" \
  --context "PWA Lighthouse audit failed because /api/health returned 404" \
  --tags "pwa,serwist,route"
```

**Propose a memory for review**:
```bash
python3 ~/.config/opencode/scripts/project-memory.py \
  --propose \
  --task <task-id> \
  --category pattern \
  --importance medium \
  --lesson "Use Dexie bulkPut for offline sync queue" \
  --context "Offline sync race condition" \
  --tags "dexie,sync,offline"
```

**List pending proposals**:
```bash
python3 ~/.config/opencode/scripts/project-memory.py --list-proposals
```

**Apply a proposal**:
```bash
python3 ~/.config/opencode/scripts/project-memory.py --apply-proposal prop-0001
```

**Load relevant memories**:
```bash
python3 ~/.config/opencode/scripts/project-memory.py \
  --load \
  --context "build PWA with offline audio assets" \
  --importance high \
  --tags "pwa,assets" \
  --limit 5
```

**Search memories**:
```bash
python3 ~/.config/opencode/scripts/project-memory.py --search "manifest"
```

**Mark memory as used**:
```bash
python3 ~/.config/opencode/scripts/project-memory.py --use --id mem-0003
```

**Cleanup low-value/old entries**:
```bash
python3 ~/.config/opencode/scripts/project-memory.py --cleanup --archive-old
```

**Export all memories to markdown**:
```bash
python3 ~/.config/opencode/scripts/project-memory.py --export > .opencode/memory/README.md
```

**Important policies**:
- Save only high-signal knowledge. Avoid `low` importance unless explicitly requested.
- Retrieval defaults should use `--importance high`.
- Save directly when a lesson is unambiguous and reusable. Propose when unsure.
- Run cleanup and review proposals before final completion claim.

---

### verify-visual-quality-evidence.py
Deterministic checker for experiential UI-quality evidence under `.opencode/evidence/<task-id>/`.

**What it verifies**:
- `visual-quality-contract.md`
- `visual-rubric.md`
- `design_pushback.md`
- `reference-essence.md`
- `template-extraction-trace.md` when the project has `templates/<dir>/`
- per-surface `reject_if` in plan
- **actual screenshot image files** (`.png`, `.webp`, `.jpg`, `.jpeg`) in evidence folder

**Usage**:
```bash
python3 ~/.config/opencode/scripts/verify-visual-quality-evidence.py \
  --project-root . \
  --task <task-id>
```

**Important policy**:
- Markdown notes, HTML diffs, and HTTP smoke tests are not substitutes for screenshot files on substantial UI work.
- If screenshot files are missing, the script returns warning/failure so quality-gate can block readiness claims.

---

### task-progress.py
Per-task worklist tracker. Maintains machine-readable execution progress at `.opencode/state/<task-id>/progress.json`.

**Initialize progress from a plan**:
```bash
python3 ~/.config/opencode/scripts/task-progress.py \
  --project-root . \
  --init \
  --task <task-id> \
  --plan .opencode/state/<task-id>/plan.md
```

**Update a step**:
```bash
python3 ~/.config/opencode/scripts/task-progress.py \
  --project-root . \
  --task <task-id> \
  --step A3 \
  --status done \
  --owner "@fixer"
```

**Read progress**:
```bash
python3 ~/.config/opencode/scripts/task-progress.py \
  --project-root . \
  --task <task-id>
```

**List tasks**:
```bash
python3 ~/.config/opencode/scripts/task-progress.py --project-root . --list
```

---

### pre-gate-smoke-check.py
Static checks that do not require a running server. Catches placeholder surfaces, missing assets, and manifest mismatches early.

**Run from project root**:
```bash
python3 ~/.config/opencode/scripts/pre-gate-smoke-check.py --project-root .
```

Typical checks:
- Zero-byte required assets (icons, manifests, hero images)
- Empty primary surfaces (homepage, landing)
- `manifest.json` references missing files
- Placeholder copy / debug text in user-facing UI
- Icon format and dimension expectations

Exit codes:
- `0`: no static smoke issues
- `1`: issues found, see report
- `2`: runtime error

---

### runtime-verify.py
Runtime verification of routes, endpoints, assets, and environment variables. Requires the project server to be running.

**Basic run**:
```bash
python3 ~/.config/opencode/scripts/runtime-verify.py --project-root .
```

**Specify base URL and environment**:
```bash
python3 ~/.config/opencode/scripts/runtime-verify.py \
  --project-root . \
  --base-url http://localhost:3000 \
  --env-file .env.local
```

Typical checks:
- HTTP route availability and status codes
- Required asset presence and non-empty bodies
- Environment variable presence
- Health endpoint response

Exit codes:
- `0`: all runtime checks pass
- `1`: one or more checks fail
- `2`: configuration/runtime error

---

### validate-plan-depth.py
Checks whether a plan artifact is deep enough for execution handoff. Operates on a generated plan `.md` file.

**Basic run**:
```bash
python3 ~/.config/opencode/scripts/validate-plan-depth.py .opencode/state/<task-id>/plan.md
```

**With score output**:
```bash
python3 ~/.config/opencode/scripts/validate-plan-depth.py .opencode/state/<task-id>/plan.md --score
```

Exit codes:
- `0`: plan depth sufficient
- `1`: plan needs more depth
- `2`: file/runtime error

---

### ui-polish-audit.py
Runs a polish-mode audit for visual slop, placeholder patterns, and finishing checklist gaps.

```bash
python3 ~/.config/opencode/scripts/ui-polish-audit.py --project-root .
```

### design-screenshot-compare.py
Builds before/after screenshot inventory evidence for visual review.

```bash
python3 ~/.config/opencode/scripts/design-screenshot-compare.py \
  --before-dir .opencode/evidence/<task-id>/before \
  --after-dir .opencode/evidence/<task-id>/after \
  --output .opencode/evidence/<task-id>/design-compare.md
```

---

### verify-visual-quality-evidence.py
Deterministic validator for experiential UI quality evidence across planner → designer → frontend → quality-gate.

Checks:
- `.opencode/evidence/<task-id>/visual-quality-contract.md`
- `.opencode/evidence/<task-id>/visual-rubric.md`
- `.opencode/evidence/<task-id>/design_pushback.md`
- `.opencode/evidence/<task-id>/reference-essence.md`
- per-surface `reject_if` presence in `.opencode/plans/<task-id>.md`

```bash
python3 ~/.config/opencode/scripts/verify-visual-quality-evidence.py \
  --project-root . \
  --task <task-id>
```

Verbose mode:
```bash
python3 ~/.config/opencode/scripts/verify-visual-quality-evidence.py \
  --project-root . \
  --task <task-id> \
  --verbose
```

Exit codes:
- `0`: all required evidence present
- `1`: missing/incomplete evidence
- `2`: runtime error

### design-system-docs.py
Generates docs for token/component candidates and registry follow-up.

```bash
python3 ~/.config/opencode/scripts/design-system-docs.py --project-root .
```

### design-token-generator.py
Extracts starter token files from `DESIGN.md`.

```bash
python3 ~/.config/opencode/scripts/design-token-generator.py --project-root .
```

### component-spec-generator.py
Generates starter component specs from source components.

```bash
python3 ~/.config/opencode/scripts/component-spec-generator.py --project-root .
```

### design-audit.py
Runs technical design audit checks for accessibility/theming/reduced-motion/token hygiene.

```bash
python3 ~/.config/opencode/scripts/design-audit.py --project-root .
```

### init-design-system.py
Seeds `DESIGN.md` and `.opencode/design-system/registry.md` into a project from canonical templates.

```bash
python3 ~/.config/opencode/scripts/init-design-system.py --project-root .
```

### design-debt-tracker.py
Builds a longitudinal design debt report from `.opencode/memory/knowledge.json`.

```bash
python3 ~/.config/opencode/scripts/design-debt-tracker.py --project-root .
```

---

## Consuming agents and skills

These scripts are referenced in agent and skill prompts. When an agent needs to run a script, use the full cross-project invocation:

```bash
python3 ~/.config/opencode/scripts/<script>.py --project-root . [script-specific-args]
```

| Script | Referenced by |
|---|---|
| `project-memory.py` | `@orchestrator`, `@fixer`, `@artifact-planner`, `@quality-gate`, `@librarian`, plus matching `opencode-*` skills |
| `task-progress.py` | `@orchestrator`, `@plan-reviewer`, plus matching skills |
| `pre-gate-smoke-check.py` | `@quality-gate`, `@orchestrator` |
| `runtime-verify.py` | `@quality-gate`, `@orchestrator` |
| `validate-plan-depth.py` | `@plan-reviewer` |
| `ui-polish-audit.py` | `@designer`, `@quality-gate` |
| `design-screenshot-compare.py` | `@designer`, `@quality-gate` |
| `design-system-docs.py` | `@design-system-engineer` |
| `design-token-generator.py` | `@design-system-engineer` |
| `component-spec-generator.py` | `@design-system-engineer` |
| `design-audit.py` | `@designer`, `@quality-gate` |
| `init-design-system.py` | `@designer`, `@orchestrator` |
| `design-debt-tracker.py` | `@designer`, `@quality-gate` |

When adding a new governance script, also update this README and wire the relevant agent/skill prompts with a concrete command example.

### visual-audit-check.py

Lightweight live-site fallback audit and v2 visual-quality-contract validator.

**Legacy URL mode**:

```bash
python3 ~/.config/opencode/scripts/visual-audit-check.py --url https://example.com --output .opencode/evidence/visual-audit.md
```

**Contract v2 mode (catalog + token parity)**:

```bash
python3 ~/.config/opencode/scripts/visual-audit-check.py \
  --project-root . \
  --contract .opencode/evidence/<task-id>/visual-quality-contract.md \
  --token-parity
```

**Contract v3 — content authenticity mode** (substantial UI):

```bash
python3 ~/.config/opencode/scripts/visual-audit-check.py \
  --project-root . \
  --contract .opencode/evidence/<task-id>/visual-quality-contract.md \
  --content-authenticity
```

This mode verifies:

- `## Content Provenance` (or `content_provenance`) block exists per section.
- `## Content Authenticity Checklist` (or `content_authenticity_checklist`) block exists with 8 rows (testimonial_real, pricing_real, faq_grounded, stats_meaningful, hero_shows_real_domain, copy_no_brochure_slogans, cta_routes_resolve, contact_real).
- No hard-fail content patterns (fabricated testimonials like `Maya R.` / `Andre F.` / `Nisa A.`, brochure slogans, `foto menyusul`, `kontak akan diperbarui`, `coming soon`, etc.).
- If the project contains `templates/<dir>/`, `.opencode/evidence/<task-id>/template-extraction-trace.md` exists and is non-empty.

Exit code `1` on any high-severity mechanical failure; `0` when only low/medium. Combine with `--token-parity` for full v2 + v3 coverage. Consumed by `@designer`, `@frontend`, `@artifact-planner`, and `@quality-gate`.
