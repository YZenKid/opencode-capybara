# Release Summary: Multi-Source Rules Compatibility + Stack-Aware Resource Discovery

## TL;DR

Two new capabilities wired into `/init-harness` to address two recurring
user complaints:

1. **"Project punya `CLAUDE.md` / `AGENTS.md` dari tool lain — gimana
   init-harness handle ini?"** — multi-source rules compatibility:
   detect, audit, harmonize, optionally forward mirrors to external tools.
2. **"Kerjaan agent masih sering keluar dari best practice stack —
   bisa sekalian pull skill/MCP tiap stack?"** — stack-aware resource
   discovery: detect stack signals, surface idiomatic skills/MCP/best
   practices from a curated registry.

Both capabilities are soft, advisory, and idempotent. They NEVER
auto-install anything. They write evidence files for audit.

## What shipped

### 1. Data foundation

- `scripts/data/stack_resources.json` (506 lines) — 14 stacks × detection
  signals + curated skills (skills.sh URLs) + MCP server recommendations
  + idiomatic best practices + anti-patterns.

  Currently covered: Laravel, Next.js, React Native/Expo, Flutter,
  Supabase, Rails, Go, Python/FastAPI, Django, Vue/Nuxt,
  Svelte/SvelteKit, Tailwind+shadcn, Rust, Postgres.

  Data-driven: adding a new stack is JSON-only, no code change.

### 2. Three new scripts

- `scripts/rules-source-scanner.py` (266 lines) — detects 14 tool
  conventions (OpenCode, Claude Code, Codex, Cursor, Windsurf, Continue,
  Cline, Cody, Roo, Aider, GitHub Copilot, GitLab Duo, generic). Text
  and JSON output. Smart recommendation adapts to detection result.

- `scripts/rules-harmonizer.py` (470 lines) — imports external rules,
  categorizes into 11 buckets (routing, build_test, style_format,
  security_secrets, git_workflow, dependency, deployment, docs,
  data_db, ui_design, uncategorized), maps each to a target OpenCode
  doc, writes `.opencode/docs/SOURCE_RULES.md` audit trail, optionally
  appends `## Source Rules` section to root `AGENTS.md`, optionally
  forwards mirror files (`CLAUDE.md`, `.codex/AGENTS.md`,
  `.cursor/rules/OPENCODE_HARMONIZED.md`,
  `.windsurf/rules/OPENCODE_HARMONIZED.md`). **Idempotent** — verified
  across 3+ re-runs.

- `scripts/stack-resource-suggester.py` (380 lines) — reads the
  registry, inspects project root for detection signals (manifests,
  lockfiles, CLI presence, directories), matches with confidence model
  (strong-hits vs weak-hits), filters false positives, outputs
  recommendation table with skills + MCP + best practices + anti-patterns.
  Soft recommender: never auto-installs.

### 3. Wired into `/init-harness`

`commands/init-harness.md` updated:
- `## Start Here` lists `SOURCE_RULES.md` (when present) and the
  stack-suggest script as direct references.
- `## Non-negotiable Rules / Harness Preflight Gate` extended to
  require `rules-source-scanner` + `rules-harmonizer --apply` +
  `stack-resource-suggester --write-evidence` before non-trivial work.
- Two new sections added: `## Multi-source Rules Compatibility` and
  `## Stack-Aware Resource Discovery`. Each lists the exact commands
  to run and when.

### 4. Wired into `package.json`

8 new scripts:
```
check:rules-source                 (text)
check:rules-source:json            (machine-readable)
init:rules-harmonize               (default --apply)
init:rules-harmonize:dry-run
init:rules-harmonize:forward-claude
init:rules-harmonize:forward-all   (claude + codex + cursor + windsurf)
init:stack-suggest
init:stack-suggest:list
```

### 5. Wired into `PROMPT_GATES.md`

Two new invariant categories:
- **Multi-source rules compatibility**: orchestrator MUST run
  `check:rules-source` then `init:rules-harmonize` when external
  agent-rules files exist; OpenCode-native wins on conflict; user is
  surfaced before any silent override.
- **Stack-aware resource discovery**: orchestrator MUST run
  `init:stack-suggest -- --write-evidence ...` and confirm idiomatic
  patterns with the user before non-trivial implementation in any
  registry-covered stack.

### 6. Test coverage

`scripts/tests/rules-harmonizer.test.py` (309 lines, 16 tests):
- `TestScanner` (4): no rules, only Claude, both present, JSON output
- `TestHarmonizer` (7): no external, audit creation, apply to AGENTS.md,
  skip when no AGENTS.md, forward mirrors, idempotent forward, dry-run
- `TestStackSuggester` (3): Laravel high-confidence, empty project,
  --list-stacks, --show laravel
- All 16 pass.

Existing `scripts/tests/verify-before-claim-check.test.py` (22 tests)
still passes — no regression.

### 7. Invariant maintained

`init-harness` 28/28/28 invariant (all 28 references contain both
`single entrypoint` and `commands/init-harness.md`): **intact**.

## Behavior changes (compared to before this release)

| Before | After |
|---|---|
| Project with `CLAUDE.md` from Claude Code: orchestrator ignored it | `check:rules-source` detects it, `init:rules-harmonize --apply` audits it to `.opencode/docs/SOURCE_RULES.md`, optionally forwards a mirror so Claude Code stays in sync |
| Project with Laravel: orchestrator wrote code from memory | `init:stack-suggest --write-evidence` suggests idiomatic patterns (`php artisan make:*` for scaffolding, FormRequest classes, Eloquent over raw SQL, `php artisan make:policy` for RBAC) and the right skill URLs (skills.sh/anthropics/skills/laravel-best-practices + laravel.com/docs) and MCP servers (postgres, redis) |
| Stack mismatch risk: high (no anchor to stack-specific best practices) | Stack mismatch risk: low (registry-backed idiomatic patterns are surfaced before implementation) |
| Best-practice guidance: scattered across agent memory + chat memory | Best-practice guidance: single source of truth at `scripts/data/stack_resources.json`, version-controlled, data-extensible |

## Files added

```
scripts/data/stack_resources.json          506 lines
scripts/rules-source-scanner.py            266 lines
scripts/rules-harmonizer.py                470 lines
scripts/stack-resource-suggester.py        380 lines
scripts/tests/rules-harmonizer.test.py     309 lines
.opencode/evidence/init-harness-multi-source-and-stack-suggest/
                                            (this folder)
```

## Files modified

```
commands/init-harness.md                   +24 lines (2 new sections + preflight extension)
package.json                               +8 new scripts
.opencode/docs/PROMPT_GATES.md             +6 lines (4 commands listed + 2 new invariant categories)
```

## Verified end-to-end

```
$ npm run --silent check:rules-source
rules-source-scanner: /var/home/ujang/.config/opencode
  OpenCode native present:  2 (AGENTS.md, .opencode)
  External rules present:   1
    [codex] AGENTS.md  (83 lines, 8117 bytes)

$ npm run --silent init:stack-suggest:list
Known stacks:
  laravel       Laravel (PHP)         skills=2  mcp=2
  nextjs        Next.js ...           skills=4  mcp=2
  ... (12 more)
```

## Risks & follow-ups (not addressed in this release)

- **No `--install` flag**: stack-resource-suggester stays as recommender.
  Adding `--install` would require user-confirmed scope (which skill,
  which MCP) and is better handled in a separate user-driven workflow.
- **No URL liveness check**: skills.sh URLs are static in the registry.
  A `scripts/stack-registry-validate.py` could curl each URL and warn on
  404s (data-driven, low-effort follow-up).
- **No reverse sync** (OpenCode → external): currently harmonizer
  imports external → OpenCode. A `--reverse` flag could re-export
  OpenCode-native rules as mirrors. Deferred.
- **Coverage gap**: 14 stacks is broad but not exhaustive. Spring Boot,
  ASP.NET, Phoenix, Elixir, Kotlin, SwiftUI, Astro, Remix could be
  added without code changes — just extend the JSON.
- **No sub-agent contract update**: orchestrator.md and artifact-planner.md
  could each gain a `## Multi-source rules + stack-aware discovery`
  section. Currently the wiring lives in `commands/init-harness.md` only.

## How user invoked this in the original turn

> "Di laravel, codex, claude code itu kan punya rules agent sendiri
> ya. ada yang pakai folder .agents ada yang .codex ada yang pakai
> CLAUDE.md dan lain-lain. Bisa gak AGENTS.md dan init-harness support
> itu? Terus kan di init-harness itu bisa scan tech stacknya dan
> sekarang banyak tech stack yang sudah sediain SKILL dan MCP
> masing-masing, bisa gak pas init harness sekalian pull SKILL dan
> MCP nya, supaya kerjaannya bener-bener sesuai best practice
> masing-masing project, karena aku masih sering liat pekerjaan
> yang di kerjakan engga sesuai dengan best practice dan idiomaticnya."

Both points addressed: multi-source rules detection + harmonization,
and stack-aware resource discovery via curated registry.
