# Graphify Discovery Coverage + Sequential Thinking Cap Plan

- Task ID: `graphify-discovery-coverage`
- Plan ID: `graphify-discovery-coverage`
- Mode: `Maintenance Stability Mode`
- Plan Quality Gate: `PASS_FOR_SLICE`
- Status: `PASS_FOR_SLICE`
<!-- auto-fixed by plan-validator: added explicit status line required by execution-readiness validator at 2026-07-22 -->

plan_status: PASS_FOR_SLICE
preflight_disposition: preset-self
<!-- auto-fixed by plan-validator: added execution-readiness metadata for maintenance plan validation at 2026-07-22 -->
- Claim scope: rencana perubahan artefak kebijakan/dokumen/check saja untuk memperluas pewarisan aturan Graphify ke semua agent/skill lokal dan menurunkan batas prompt `sequential_thinking` dari 3 ke 2 langkah untuk kerja non-trivial/ambigu/risky. Artefak ini hanya plan/evidence; tidak mengubah source/config implementasi pada slice ini.

## Goal

Buat rencana maintenance yang siap-eksekusi untuk dua hasil sempit: (1) memastikan pengetahuan/policy Graphify diwariskan secara terpusat ke semua local agents dan skills tanpa duplikasi prose yang tidak perlu, dan (2) memastikan cap prompt-policy `sequential_thinking` turun dari 3 ke 2 langkah pada semua lokasi kebijakan aktif yang relevan. Hasil plan harus memberi source of truth, diff boundary, mekanisme audit mekanis lintas-agent/lintas-skill, exact validation path, dan handoff yang bisa dijalankan tanpa menebak.

## Non-goals

- Tidak mengubah `opencode.json`, `scripts/graphify-mcp-wrapper`, `.git/hooks/**`, `graphify-out/**`, `commands/init-harness.md`, atau secret/env.
- Tidak mengklaim Graphify menjadi mandatory, write-capable, networked, semantic, atau pengganti source reading/tests/runtime verification.
- Tidak mengklaim cap 2 sebagai enforcement server-side; ini prompt-policy/documentation/check contract saja.
- Tidak mewajibkan menambah prose Graphify ke setiap agent/skill bila inheritance terpusat + audit mekanis sudah cukup.
- Tidak menjalankan implementasi, staging, commit, atau delegation pada slice ini.

## Scope

In scope:
- audit source of truth Graphify dan Sequential Thinking cap yang aktif di repo,
- rencana perubahan canonical docs/skills/check scripts/generated-doc freshness yang perlu,
- strategi coverage lintas semua `skills/opencode-*` dan lane docs,
- exact validation commands,
- execution-ready worklist untuk implementer lanjutan.

Out of scope:
- edit implementasi nyata pada docs/skills/scripts/generated outputs,
- perubahan MCP/server behavior,
- perubahan hook Graphify,
- perluasan ke marketplace skills non-local.

## Requirements

1. Plan harus menetapkan `Maintenance Stability Mode` dan tetap regression-first/minimal.
2. Plan harus mempertahankan Graphify sebagai optional, local, code-only, read-only discovery context.
3. Plan harus mempertahankan rule query-first hanya untuk broad architecture/dependency discovery saat graph fresh tersedia.
4. Plan harus mempertahankan `INFERRED` dan `AMBIGUOUS` sebagai lead, bukan fakta; direct source/tests/runtime verification tetap mandatory.
5. Plan harus mengidentifikasi canonical policy surfaces aktif untuk Graphify: `AGENTS.md`, `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`, `.opencode/docs/SKILLS.md`, dan `skills/graphify-discovery/SKILL.md`.
6. Plan harus mengidentifikasi canonical cap surfaces aktif untuk Sequential Thinking, termasuk docs dan semua skill files lokal yang masih menyebut batas 3.
7. Plan harus memilih inheritance-first strategy: ubah central docs + duplicated local skill snippets hanya bila memang menjadi authoritative runtime guidance atau checked contract.
8. Plan harus mendefinisikan mechanical coverage strategy untuk semua local agents/skills tanpa inventing redundant prose.
9. Plan harus menamai exact validation commands: `npm run check:agents`, `npm run check:skills`, `npm run docs:generate:check`, targeted grep untuk cap 3 aktif, dan audit coverage Graphify.
10. Plan harus menamai exact implementation touch set yang diizinkan dan diff boundary yang dilarang.
11. Plan harus memuat worklist atomic dengan owner lane, depends_on, validation, exit_criteria, evidence_path, `must_preserve`, dan `do_not_touch`.
12. Plan harus memuat handoff blocks valid untuk tiap task worker-sized.
13. Plan harus memuat progress tracking contract lengkap untuk semua worklist ids.
14. Plan harus menyatakan generated docs/risk-matrix sebagai derived output yang mungkin perlu refresh/check bila canonical source berubah.
15. Plan harus memetakan exact cap locations ditemukan saat discovery: `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`, `docs/generated/mcp-risk-matrix.md`, dan 18 `skills/opencode-*` files yang memakai snippet cap 3.

## Acceptance Criteria

- Ada satu plan utama di `.opencode/plans/graphify-discovery-coverage.md` dengan semua heading kontrak execution-ready.
- Plan membedakan source of truth vs derived/generated surfaces.
- Plan menyebut strategi coverage Graphify yang tidak memaksa prose redundant di semua agent/skill.
- Plan menyebut exact active cap-of-3 locations yang perlu diturunkan menjadi 2 pada fase implementasi.
- `subagent-handoff-check.py --plan .opencode/plans/graphify-discovery-coverage.md` lulus.
- `plan-compliance-check.py --project-root . --plan .opencode/plans/graphify-discovery-coverage.md --task-id graphify-discovery-coverage` lulus.
- `validate-plan-depth.py .opencode/plans/graphify-discovery-coverage.md --mode maintenance --score` tidak menghasilkan `NEEDS_DEPTH`.
- Future executor bisa mulai dari `start_with` tanpa perlu infer scope dari chat.
- Status plan menyebut `Maintenance Stability Mode` dan memakai validator maintenance, bukan threshold greenfield.
<!-- auto-fixed by plan-validator: aligned acceptance criteria with maintenance-mode validator at 2026-07-22 -->

## Existing Patterns/Reuse
<!-- auto-fixed by plan-validator: normalized heading for validator recognition at 2026-07-22 -->

- Global inheritance pattern sudah dipakai lewat root `AGENTS.md` dan canonical docs di `.opencode/docs/`.
- `skills/graphify-discovery/SKILL.md` sudah menjadi skill khusus untuk Graphify discovery posture.
- `scripts/agent-boundary-check.mjs` dan `scripts/skill-contract-check.mjs` sudah menjadi mechanical check entry points untuk agents/skills.
- `docs/generated/mcp-risk-matrix.md` adalah derived artifact dari capability registry, bukan canonical policy surface.
- `graphify-opencode-integration.md` memberi pola plan maintenance lengkap dengan handoff, progress tracking, dan validators.

## Constraints

- Slice ini plan/evidence only.
- Tidak boleh edit source/config implementasi.
- Tidak boleh claim server enforcement untuk cap 2.
- Harus hormati centralized inheritance bila cukup.
- Harus pakai validator mekanis sebelum verdict.

## Risks

- Ada banyak duplicate cap snippets di skill files; jika central docs diubah tanpa skill updates, policy drift tetap hidup.
- Jika generated docs tidak di-refresh setelah source berubah, `docs:generate:check` bisa gagal.
- Jika Graphify coverage hanya didokumentasikan global tanpa mechanical scan, future drift bisa lolos.
- Jika implementer mengubah too many files di luar policy/check surfaces, diff boundary pecah.

## Decisions/Assumptions
<!-- auto-fixed by plan-validator: normalized heading for validator recognition at 2026-07-22 -->

- `confirmed_repo`: root `AGENTS.md` sudah memuat rule Graphify broad-architecture/discovery dan optional/read-only boundary.
- `confirmed_repo`: `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`, `.opencode/docs/SKILLS.md`, dan `skills/graphify-discovery/SKILL.md` sudah memuat Graphify policy dasar.
- `confirmed_repo`: 18 local `skills/opencode-*` files masih memakai snippet cap `3`; ini lokasi aktif policy drift untuk Sequential Thinking.
- `confirmed_repo`: `docs/generated/mcp-risk-matrix.md` juga menyebut cap `3`, tetapi statusnya derived/advisory.
- `assumption`: `npm run check:agents` dan `npm run check:skills` belum menegakkan coverage Graphify inheritance atau cap `2` secara spesifik; implementasi mungkin perlu tambah assertions/check logic.
- `assumption`: “Graphify coverage audit command” paling aman diwujudkan sebagai check baru atau extension pada existing check script, bukan manual grep permanen.

## Source Anatomy

- `AGENTS.md` — aturan global Graphify untuk semua lane.
- `.opencode/docs/MCP.md` — inventory + normative Graphify/Sequential Thinking guidance.
- `.opencode/docs/TOOL_USAGE.md` — operational use rules untuk Graphify dan `sequential_thinking`.
- `.opencode/docs/AGENT_TOOL_ACCESS.md` — cross-lane permission/boundary wording.
- `.opencode/docs/SKILLS.md` — registry/index skill termasuk Graphify skill dan maintenance mode notes.
- `skills/graphify-discovery/SKILL.md` — dedicated Graphify discovery workflow.
- `skills/opencode-*.SKILL.md` — duplicate Sequential Thinking gate snippets yang perlu harmonisasi ke cap 2.
- `scripts/agent-boundary-check.mjs` — candidate location untuk mechanical Graphify coverage assertions.
- `scripts/skill-contract-check.mjs` — candidate location untuk mechanical Sequential Thinking snippet assertions.
- `scripts/generate-generated-docs.mjs` — generated docs refresh/check path.
- `docs/generated/mcp-risk-matrix.md` — derived output expected to change after canonical source updates.

## Reference Map

- Local source of truth: `AGENTS.md`, `.opencode/docs/{MCP.md,TOOL_USAGE.md,AGENT_TOOL_ACCESS.md,SKILLS.md}`.
- Skill source: `skills/graphify-discovery/SKILL.md`.
- Check surfaces: `scripts/{agent-boundary-check.mjs,skill-contract-check.mjs,generate-generated-docs.mjs}`.
- Related exemplar/pattern: `.opencode/plans/graphify-opencode-integration.md`.
- Derived evidence source: `docs/generated/mcp-risk-matrix.md`.
- Handoff source: `.opencode/state/graphify-discovery-coverage/planner-handoff.json`.

## Grounding Contract

Semua klaim material di plan ini harus diberi label `confirmed_repo`, `confirmed_runtime`, `confirmed_docs`, `user_confirmed`, `assumption`, atau `unverified` sesuai sumber bukti. Tidak ada claim runtime/server enforcement baru. Graphify policy di plan ini hanya berdasarkan repo-local evidence yang dibaca pada sesi ini. Exact cap locations berasal dari grep repo-local, bukan asumsi. Generated doc dianggap derived output, bukan sumber kebijakan utama.
<!-- auto-fixed by plan-validator: expanded grounding labels to validator-recognized set at 2026-07-22 -->

## Execution Source of Truth

Precedence untuk implementasi nanti:
1. instruksi user terbaru: execute only payload `.opencode/state/graphify-discovery-coverage/plan-remediation-handoff.json`; planning/evidence only; no implementation edits/staging/commit/delegation; Maintenance Stability Mode.
2. batasan keselamatan/permission dari handoff `must_preserve` dan `do_not_touch`.
3. canonical repo policy pada `AGENTS.md` dan `.opencode/docs/{MCP.md,TOOL_USAGE.md,AGENT_TOOL_ACCESS.md,SKILLS.md}`.
4. plan ini sebagai kontrak eksekusi slice.
5. generated docs hanya sebagai freshness/consistency evidence.

preset-self purpose evidence: target hanya plan/evidence readiness untuk policy maintenance lokal di `.opencode/plans/graphify-discovery-coverage.md`, dengan validator exact commands dari handoff `.opencode/state/graphify-discovery-coverage/plan-remediation-handoff.json` dan planning basis `.opencode/evidence/graphify-discovery-coverage/planning.md`.
<!-- auto-fixed by plan-validator: aligned source-of-truth payload path and added preset-self evidence line for execution-readiness validator at 2026-07-22 -->

## Non-negotiable Implementation Invariants

1. Graphify tetap optional, local, code-only, read-only discovery only.
2. Graphify query-first hanya untuk broad architecture/dependency discovery dengan fresh graph.
3. `INFERRED` dan `AMBIGUOUS` tetap leads; direct source/tests/runtime verification mandatory.
4. Jangan tambah prose Graphify redundant ke setiap agent/skill jika centralized inheritance + mechanical audit sudah cukup.
5. Sequential Thinking cap `2` adalah prompt-policy cap saja; jangan klaim server-enforced tanpa evidence terpisah.
6. Tiny fast path tetap `1` brief thought.
7. Generated docs harus di-refresh/check bila canonical text berubah.
8. Tidak menyentuh `opencode.json`, `scripts/graphify-mcp-wrapper`, `.git/hooks/**`, `graphify-out/**`, `commands/init-harness.md`, atau secret/env.

## Do Not / Reject If

- Reject perubahan yang menjadikan Graphify mandatory atau authoritative over source code.
- Reject perubahan yang memperluas scope ke runtime/config/hook implementation.
- Reject duplikasi prose Graphify ke semua skills bila tidak diperlukan oleh inheritance/check contract.
- Reject claim bahwa cap `2` enforced oleh MCP server.
- Reject penyelesaian yang hanya mengubah generated docs tanpa canonical source change.
- Reject validator pass yang masih menyisakan cap `3` aktif di authoritative skill/docs surfaces.

## Diff Boundary

Allowed future implementation surfaces:
- `AGENTS.md`
- `.opencode/docs/{MCP.md,TOOL_USAGE.md,AGENT_TOOL_ACCESS.md,SKILLS.md,AGENT_ROUTING.md,PROMPT_GATES.md}`
- `skills/graphify-discovery/SKILL.md`
- `skills/opencode-*.SKILL.md`
- `scripts/{agent-boundary-check.mjs,skill-contract-check.mjs,generate-generated-docs.mjs,prompt-gate-regression.mjs}`
- `docs/generated/mcp-risk-matrix.md`
- `.opencode/plans/graphify-discovery-coverage.md`
- `.opencode/evidence/graphify-discovery-coverage/**`
- `.opencode/state/graphify-discovery-coverage/**`

Forbidden by this plan:
- `opencode.json`
- `scripts/graphify-mcp-wrapper`
- `.git/hooks/**`
- `graphify-out/**`
- `commands/init-harness.md`
- `secrets/env`

## TDD / Test Plan

Maintenance slice ini plan-only. TDD exemption berlaku untuk artefak plan, tetapi future implementation wajib regression-first lewat existing checks.

Planned Red/Green path untuk implementer:
1. Red: targeted grep masih menemukan cap `3` di authoritative docs/skills; coverage Graphify audit belum ada/masih gagal.
2. Green: canonical docs + required duplicated skill snippets pindah ke cap `2`; Graphify coverage audit/check pass.
3. Refactor: reduce redundant wording, keep centralized inheritance, refresh generated docs, rerun checks.

## Implementation Steps

1. Konfirmasi source of truth Graphify dan cap surfaces aktif dari repo-local evidence.
2. Tentukan canonical vs derived surfaces; ubah canonical dulu pada future implementation, baru refresh generated docs.
3. Terapkan inheritance-first Graphify coverage strategy: pertahankan root docs + Graphify skill sebagai pusat, lalu tambahkan/extend mechanical checks agar semua local agents/skills dianggap covered tanpa prose spam.
4. Harmonisikan semua skill/doc Sequential Thinking snippets aktif dari cap `3` ke cap `2`, sambil menjaga tiny path tetap `1`.
5. Update prompt-gate/check logic bila perlu agar drift Graphify coverage dan cap snippets terdeteksi otomatis.
6. Refresh generated docs, rerun validators, record evidence bundle dan residual risk bila ada.

## Expected Files to Change

Future implementation expected:
- `AGENTS.md`
- `.opencode/docs/MCP.md`
- `.opencode/docs/TOOL_USAGE.md`
- `.opencode/docs/AGENT_TOOL_ACCESS.md`
- `.opencode/docs/SKILLS.md`
- `.opencode/docs/AGENT_ROUTING.md` (hanya bila Sequential Thinking wording perlu sinkronisasi)
- `.opencode/docs/PROMPT_GATES.md` (bila audit/check command perlu didokumentasikan)
- `skills/graphify-discovery/SKILL.md`
- subset atau seluruh `skills/opencode-*.SKILL.md` yang masih punya cap `3`
- `scripts/agent-boundary-check.mjs`
- `scripts/skill-contract-check.mjs`
- `scripts/prompt-gate-regression.mjs` bila fixture/gate perlu update
- `docs/generated/mcp-risk-matrix.md`

## Agent / Tool Routing

- `@artifact-planner`: ownership untuk plan ini. Selesai pada artefak planning/evidence.
- Validator mode: `Maintenance Stability Mode`; gunakan `validate-plan-depth.py --mode maintenance --score`, bukan threshold greenfield.
<!-- auto-fixed by plan-validator: made maintenance validator mode explicit in routing section at 2026-07-22 -->
- `@explorer`: audit canonical Graphify coverage surfaces dan enumerate exact cap-of-3 locations.
- `@fixer`: lakukan perubahan docs/skills/scripts minimal pada fase implementasi nanti.
- `@quality-gate`: final read-only conformance setelah implementasi.
- Preferred tools: `read`, `grep`, `glob`, `scripts_plan_validate`, `bash` untuk package/check commands fallback.
- Skipped MCPs: `context7` tidak perlu karena ini repo policy lokal; `browseros` tidak perlu karena tidak ada UI/runtime browser flow; `github` tidak perlu karena remote state tidak dibutuhkan.

## Executor Handoff Prompt

Kerjakan hanya slice `graphify-discovery-coverage` sesuai plan ini. Ubah seminimal mungkin pada canonical docs/skills/check scripts untuk: (1) menjadikan coverage Graphify inheritance auditable lintas local agents/skills tanpa prose spam, dan (2) menurunkan semua active prompt-policy cap `sequential_thinking` dari 3 ke 2 sambil menjaga tiny path tetap 1. Jangan sentuh `opencode.json`, `scripts/graphify-mcp-wrapper`, `.git/hooks/**`, `graphify-out/**`, `commands/init-harness.md`, atau secret/env. Jalankan validation yang tercantum, refresh generated docs bila canonical text berubah, lalu laporkan changed files, exact command results, evidence paths, dan residual risks. Jangan delegasi ulang tanpa handoff valid baru.

## Execution-ready Worklist / Handoff Contract

1. **G1** | `@explorer` | Audit active Graphify coverage surfaces dan enumerate all active cap-of-3 locations | depends_on: none | validation: targeted grep + source readback | evidence: `.opencode/evidence/graphify-discovery-coverage/discovery.md`
2. **G2** | `@fixer` | Apply minimal canonical policy/doc/skill wording updates for Graphify inheritance and Sequential Thinking cap 2 | depends_on: G1 | validation: targeted grep clean on active cap 3 surfaces | evidence: `.opencode/evidence/graphify-discovery-coverage/implementation-notes.md`
3. **G3** | `@fixer` | Extend mechanical checks/generated-doc freshness path for Graphify coverage and cap drift | depends_on: G1 | validation: `npm run check:agents`, `npm run check:skills`, `npm run docs:generate:check` | evidence: `.opencode/evidence/graphify-discovery-coverage/verification.md`
4. **G4** | `@quality-gate` | Validate conformance, diff boundary, residual drift, and final gate | depends_on: G2,G3 | validation: full listed commands + evidence review | evidence: `.opencode/evidence/graphify-discovery-coverage/quality-gate.md`

### G1 — Discovery audit
- Owner: `@explorer`
- Depends on: none
- Validation: targeted grep for `Graphify` and cap `3` language; read canonical files and sampled skill files.
- Exit criteria: exact authoritative surfaces, derived surfaces, and cap locations documented.
- Evidence path: `.opencode/evidence/graphify-discovery-coverage/discovery.md`
- must_preserve: maintain Graphify optional/read-only/query-first posture and cap-as-prompt-policy only.
- do_not_touch: implementation source/config outside planning evidence.

### G2 — Canonical wording updates
- Owner: `@fixer`
- Depends on: G1
- Validation: targeted grep no longer finds active cap `3` in authoritative docs/skills; wording still preserves tiny=1 and non-enforcement language.
- Exit criteria: canonical docs and required local skill snippets harmonized to cap `2`; Graphify inheritance wording minimal and centralized.
- Evidence path: `.opencode/evidence/graphify-discovery-coverage/implementation-notes.md`
- must_preserve: no redundant prose explosion; no Graphify scope expansion.
- do_not_touch: `opencode.json`, `scripts/graphify-mcp-wrapper`, `.git/hooks/**`, `graphify-out/**`, `commands/init-harness.md`, secret/env.

### G3 — Mechanical check updates
- Owner: `@fixer`
- Depends on: G1
- Validation: `npm run check:agents`, `npm run check:skills`, `npm run docs:generate:check`, targeted grep, Graphify coverage audit command.
- Exit criteria: checks detect future drift for Graphify inheritance/cap policy or explicitly document why one check remains advisory.
- Evidence path: `.opencode/evidence/graphify-discovery-coverage/verification.md`
- must_preserve: reuse existing checks where possible; shortest diff.
- do_not_touch: forbidden paths above; no runtime/config changes.

### G4 — Final gate
- Owner: `@quality-gate`
- Depends on: G2, G3
- Validation: review evidence bundle, rerun listed commands as needed, confirm diff boundary and no active cap `3` drift.
- Exit criteria: `PASS` or explicit remediation list.
- Evidence path: `.opencode/evidence/graphify-discovery-coverage/quality-gate.md`
- must_preserve: verdict evidence-only; no overclaim.
- do_not_touch: implementation files during review.

### Task G1 handoff
```yaml
task_id: graphify-discovery-coverage
plan_id: graphify-discovery-coverage
caller: orchestrator
callee: explorer
scope: Audit canonical Graphify policy surfaces and enumerate all active Sequential Thinking cap-of-3 locations.
claim_level: partial
claim_scope: Discovery findings only; no edits.
source_basis:
  - AGENTS.md
  - .opencode/docs/MCP.md
  - .opencode/docs/TOOL_USAGE.md
  - .opencode/docs/AGENT_TOOL_ACCESS.md
  - .opencode/docs/SKILLS.md
  - skills/graphify-discovery/SKILL.md
  - skills/opencode-*.SKILL.md
  - docs/generated/mcp-risk-matrix.md
must_preserve:
  - Graphify remains optional, local, code-only, read-only discovery only
  - Graphify query-first only for broad architecture/dependency discovery with fresh graph
  - INFERRED and AMBIGUOUS remain leads; direct source/tests/runtime verification mandatory
  - Sequential Thinking cap is prompt-policy only, not server enforcement claim
do_not_touch:
  - opencode.json
  - scripts/graphify-mcp-wrapper
  - .git/hooks/**
  - graphify-out/**
  - commands/init-harness.md
  - secrets/env
validation:
  - targeted grep for Graphify surfaces
  - targeted grep for cap 3 wording
  - exact file readback for authoritative and derived locations
exit_criteria:
  - authoritative surfaces documented
  - derived surfaces documented
  - exact cap locations documented
evidence_required:
  - .opencode/evidence/graphify-discovery-coverage/discovery.md
depends_on:
  - none
context_bundle:
  - .opencode/state/graphify-discovery-coverage/planner-handoff.json
  - .opencode/plans/graphify-discovery-coverage.md
# auto-fixed by plan-validator: lifted handoff payload fields to YAML root for schema validity at 2026-07-22
```

### Task G2 handoff
```yaml
task_id: graphify-discovery-coverage
plan_id: graphify-discovery-coverage
caller: orchestrator
callee: fixer
scope: Apply minimal policy wording updates for Graphify inheritance and lower active Sequential Thinking cap text from 3 to 2.
claim_level: partial
claim_scope: Canonical docs/skills wording only; no runtime/config behavior claims.
source_basis:
  - AGENTS.md
  - .opencode/docs/MCP.md
  - .opencode/docs/TOOL_USAGE.md
  - .opencode/docs/AGENT_TOOL_ACCESS.md
  - .opencode/docs/SKILLS.md
  - skills/graphify-discovery/SKILL.md
  - skills/opencode-*.SKILL.md
  - .opencode/evidence/graphify-discovery-coverage/discovery.md
must_preserve:
  - Graphify remains optional, local, code-only, read-only discovery only
  - Do not add Graphify prose redundantly to every agent/skill if centralized inheritance plus mechanical audit is sufficient
  - Sequential Thinking cap exactly 2 for non-trivial/ambiguous/risky work; tiny stays 1
  - Cap is prompt-policy only, not server enforcement claim
do_not_touch:
  - opencode.json
  - scripts/graphify-mcp-wrapper
  - .git/hooks/**
  - graphify-out/**
  - commands/init-harness.md
  - secrets/env
validation:
  - targeted grep finds no active cap of 3 on authoritative surfaces
  - readback confirms tiny path still 1
exit_criteria:
  - canonical wording updated
  - required duplicated skill snippets updated
  - no forbidden scope expansion
evidence_required:
  - .opencode/evidence/graphify-discovery-coverage/implementation-notes.md
depends_on:
  - G1
context_bundle:
  - .opencode/evidence/graphify-discovery-coverage/discovery.md
  - .opencode/plans/graphify-discovery-coverage.md
# auto-fixed by plan-validator: lifted handoff payload fields to YAML root for schema validity at 2026-07-22
```

### Task G3 handoff
```yaml
task_id: graphify-discovery-coverage
plan_id: graphify-discovery-coverage
caller: orchestrator
callee: fixer
scope: Extend or document mechanical checks so Graphify inheritance coverage and Sequential Thinking cap drift are auditable.
claim_level: partial
claim_scope: Check/gate/doc freshness updates only.
source_basis:
  - scripts/agent-boundary-check.mjs
  - scripts/skill-contract-check.mjs
  - scripts/generate-generated-docs.mjs
  - scripts/prompt-gate-regression.mjs
  - .opencode/docs/PROMPT_GATES.md
  - .opencode/evidence/graphify-discovery-coverage/discovery.md
must_preserve:
  - reuse existing checks before adding new ones
  - shortest diff
  - generated docs remain derived outputs
do_not_touch:
  - opencode.json
  - scripts/graphify-mcp-wrapper
  - .git/hooks/**
  - graphify-out/**
  - commands/init-harness.md
  - secrets/env
validation:
  - npm run check:agents
  - npm run check:skills
  - npm run docs:generate:check
  - targeted grep finds no active cap of 3
  - Graphify coverage audit command
exit_criteria:
  - drift becomes mechanically detectable or advisory status explicitly documented
  - validation command list stays exact and runnable
evidence_required:
  - .opencode/evidence/graphify-discovery-coverage/verification.md
depends_on:
  - G1
context_bundle:
  - .opencode/evidence/graphify-discovery-coverage/discovery.md
  - .opencode/plans/graphify-discovery-coverage.md
# auto-fixed by plan-validator: lifted handoff payload fields to YAML root for schema validity at 2026-07-22
```

### Task G4 handoff
```yaml
task_id: graphify-discovery-coverage
plan_id: graphify-discovery-coverage
caller: orchestrator
callee: quality-gate
scope: Validate final conformance for Graphify inheritance coverage and Sequential Thinking cap-2 policy slice.
claim_level: done
claim_scope: Final verdict for this policy/documentation/check slice only.
source_basis:
  - .opencode/plans/graphify-discovery-coverage.md
  - .opencode/evidence/graphify-discovery-coverage/discovery.md
  - .opencode/evidence/graphify-discovery-coverage/implementation-notes.md
  - .opencode/evidence/graphify-discovery-coverage/verification.md
must_preserve:
  - verdict based on evidence only
  - no overclaim about server enforcement or runtime changes
do_not_touch:
  - all implementation/config files during review
validation:
  - python3 ~/.config/opencode/scripts/validate-plan-depth.py .opencode/plans/graphify-discovery-coverage.md --mode maintenance --score
  - python3 ~/.config/opencode/scripts/plan-compliance-check.py --project-root . --plan .opencode/plans/graphify-discovery-coverage.md --task-id graphify-discovery-coverage
  - python3 ~/.config/opencode/scripts/subagent-handoff-check.py --plan .opencode/plans/graphify-discovery-coverage.md
  - npm run check:agents
  - npm run check:skills
  - npm run docs:generate:check
exit_criteria:
  - PASS or explicit remediation list
evidence_required:
  - .opencode/evidence/graphify-discovery-coverage/quality-gate.md
depends_on:
  - G2
  - G3
context_bundle:
  - .opencode/plans/graphify-discovery-coverage.md
  - .opencode/evidence/graphify-discovery-coverage/verification.md
# auto-fixed by plan-validator: lifted handoff payload fields to YAML root for schema validity and aligned maintenance validator at 2026-07-22
```

start_with: G1

## Progress Tracking

- tracker_path: `.opencode/state/graphify-discovery-coverage/progress.json`
- init_command: `python3 ~/.config/opencode/scripts/task-progress.py graphify-discovery-coverage --init --plan .opencode/plans/graphify-discovery-coverage.md`
- summary_command: `python3 ~/.config/opencode/scripts/task-progress.py graphify-discovery-coverage --summary`
- checklist_command: `python3 ~/.config/opencode/scripts/task-progress.py graphify-discovery-coverage --checklist`
- update_rules:
  - `in_progress`: set saat owner mulai task dan evidence target sudah diketahui.
  - `completed`: set hanya setelah validation task lulus dan evidence file di-refresh.
  - `blocked`: set saat dependency atau validator menghalangi; sertakan blocker note.
  - `cancelled`: set hanya oleh orchestrator atau explicit scope stop.
  - `evidence_refresh`: setiap perubahan status harus refresh evidence path atau jelaskan kenapa belum berubah.
- task_map:

| Task ID | Owner | Status | Depends On | Evidence Path | Update Command |
|---|---|---|---|---|---|
| `G1` | `@explorer` | pending | none | `.opencode/evidence/graphify-discovery-coverage/discovery.md` | `python3 ~/.config/opencode/scripts/task-progress.py graphify-discovery-coverage --update G1 --status <status> --owner explorer --evidence .opencode/evidence/graphify-discovery-coverage/discovery.md` |
| `G2` | `@fixer` | pending | G1 | `.opencode/evidence/graphify-discovery-coverage/implementation-notes.md` | `python3 ~/.config/opencode/scripts/task-progress.py graphify-discovery-coverage --update G2 --status <status> --owner fixer --depends-on G1 --evidence .opencode/evidence/graphify-discovery-coverage/implementation-notes.md` |
| `G3` | `@fixer` | pending | G1 | `.opencode/evidence/graphify-discovery-coverage/verification.md` | `python3 ~/.config/opencode/scripts/task-progress.py graphify-discovery-coverage --update G3 --status <status> --owner fixer --depends-on G1 --evidence .opencode/evidence/graphify-discovery-coverage/verification.md` |
| `G4` | `@quality-gate` | pending | G2,G3 | `.opencode/evidence/graphify-discovery-coverage/quality-gate.md` | `python3 ~/.config/opencode/scripts/task-progress.py graphify-discovery-coverage --update G4 --status <status> --owner quality-gate --depends-on G2,G3 --evidence .opencode/evidence/graphify-discovery-coverage/quality-gate.md` |
<!-- auto-fixed by plan-validator: converted task_map to execution-readiness table format at 2026-07-22 -->

## Validation Commands

- `python3 ~/.config/opencode/scripts/validate-plan-depth.py .opencode/plans/graphify-discovery-coverage.md --mode maintenance --score`
<!-- auto-fixed by plan-validator: switched plan depth command to maintenance mode at 2026-07-22 -->
- `python3 ~/.config/opencode/scripts/plan-compliance-check.py --project-root . --plan .opencode/plans/graphify-discovery-coverage.md --task-id graphify-discovery-coverage`
- `python3 ~/.config/opencode/scripts/subagent-handoff-check.py --plan .opencode/plans/graphify-discovery-coverage.md`
- `npm run check:agents`
- `npm run check:skills`
- `npm run docs:generate:check`
- `grep -R "at most 3 thought steps total\|totalThoughts no higher than \\`3\\`" skills/opencode-* .opencode/docs docs/generated/mcp-risk-matrix.md`
- `grep -R "Graphify" AGENTS.md .opencode/docs skills/graphify-discovery/SKILL.md`

## Evidence Requirements

- `.opencode/evidence/graphify-discovery-coverage/planning.md` — planning basis, source strategy, exact cap locations, chosen coverage strategy.
- `.opencode/evidence/graphify-discovery-coverage/check-plan/*.txt` — validator outputs for this remediation pass.
- `.opencode/evidence/graphify-discovery-coverage/discovery.md` — authoritative vs derived surfaces dan cap-location inventory.
- `.opencode/evidence/graphify-discovery-coverage/verification.md` — validator results untuk plan dan, nanti, implementer validation summary.
- `.opencode/evidence/graphify-discovery-coverage/index.json` — manifest replay minimal.
- Optional future implementation evidence: `.opencode/evidence/graphify-discovery-coverage/implementation-notes.md`, `.opencode/evidence/graphify-discovery-coverage/quality-gate.md`.

## Done Criteria

- Plan execution-ready tersedia di `.opencode/plans/graphify-discovery-coverage.md`.
- Source of truth, diff boundary, exact cap locations, dan mechanical coverage strategy terdokumentasi.
- Worklist atomic dengan handoff valid dan progress tracking lengkap tersedia.
- Plan validators lulus dengan status `PASS` atau `PASS_FOR_SLICE`.
- Evidence manifest dan planning evidence tersedia di task evidence directory.
- Claim tetap sempit: plan/evidence only, bukan implementation complete.

## Final Planning Summary

Artefak utama untuk task ini adalah plan maintenance yang siap dipakai orchestrator/implementer tanpa replanning. Discovery repo-local menunjukkan Graphify policy pusat sudah ada di root/canonical docs + dedicated skill, sedangkan drift terbesar ada pada snippet Sequential Thinking cap `3` yang tersebar di banyak `skills/opencode-*` file dan satu generated risk matrix. Strategi yang dipilih: inheritance-first untuk Graphify, harmonisasi prompt cap aktif ke `2`, dan audit mekanis supaya drift future terdeteksi. Generated docs diperlakukan sebagai derived output yang harus di-refresh setelah source canonical berubah. Slice ini berhenti di plan/evidence; implementasi tidak dilakukan.
