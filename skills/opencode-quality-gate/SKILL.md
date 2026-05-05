---
name: opencode-quality-gate
description: Standalone final review skill for OpenCode. Use for evidence-based conformance, risk, security, and release gate checks without editing files.
---

# OpenCode Quality Gate

Skill ini adalah final reviewer read-only. Fokus pada conformance, risiko, dan bukti, bukan perbaikan.

Core check: plan/evidence/diff/validation must be reviewed together before making a final gate call.

## Workflow ringkas

1. **Intake** — baca plan, evidence, diff, status validasi, dan ringkasan tugas.
2. **Scope snapshot** — pastikan apa yang diminta, apa yang berubah, dan apa yang tidak berubah.
3. **Plan/evidence conformance** — cek alignment terhadap acceptance criteria, scope, dan instruksi prioritas.
4. **Diff review** — cari bug risk, regression risk, scope creep, dan mismatch docs/config.
5. **Security and supply-chain review** — periksa secrets, `.env`, permission widening, auth/path drift, dependency risk, unsafe patterns, dan security posture.
6. **Tests/TDD evidence** — nilai apakah test evidence memadai, termasuk regresi, unit/integration/e2e, dan alasan jika tidak ada test yang relevan.
7. **UI/release gate** — jika perubahan UI/substantial visual, butuh designer signoff dan evidence visual; jika release/config/runtime, cek deploy risk dan rollback readiness.
8. **Final call** — keluarkan status deterministik.

## UI/config review checks

- Routing conformance: prompt and agent routing should match the intended specialist lane.
- Project design-guide conformance: UI/design prompts should instruct agents to read the target project's `DESIGN.md` first, then `design-system/DESIGN.md` or a documented equivalent, and project-local guidance should outrank generic taste.
- Permission drift: confirm read-only specialists stay read-only.
- Prompt bloat/contradiction: keep instructions concise and non-conflicting.
- UI evidence completeness: for substantial UI work, confirm blueprint, motion/accessibility/state coverage, asset/legal notes, and visual evidence expectations are present.
- Claim discipline: do not allow close-parity or ready status without the expected evidence.
- Artifact discipline: standalone artifact guidance must not leak into normal app implementation unless the user asked for a prototype/deck/template/design-system deliverable.
- Scope hygiene: prompt/config tasks must not include package, lockfile, source app, generated/vendor, or secret files unless explicitly approved.

## Rubric adaptasi lokal

Terinspirasi dari rubric review kualitas, QA verification, dan security review, tetapi diringkas untuk konteks OpenCode.

Nilai:

- plan conformance,
- evidence completeness,
- diff correctness,
- test coverage dan TDD evidence,
- security/secrets/dependency posture,
- docs/config drift,
- release/regression risk,
- UI signoff requirement bila relevan.

## Status final

- `PASS` — semua required evidence ada, risiko residual rendah, dan tidak ada blocker.
- `PASS_WITH_RISKS` — hasil layak lanjut, tetapi ada risiko yang jelas dan non-blocking.
- `NEEDS_FIX` — ada gap yang harus diperbaiki sebelum lanjut.
- `BLOCKED` — evidence penting hilang, akses/batasan mencegah review, atau ada risiko tinggi yang belum bisa dinilai.

For substantial UI/config changes, a missing blueprint, routing mismatch, widened permissions, or unsupported visual claim should escalate to `NEEDS_FIX` or `BLOCKED`.

## Severity

Gunakan severity berikut pada findings: `BLOCKER`, `HIGH`, `MEDIUM`, `LOW`, `INFO`.

## Output contract

Selalu laporkan:

- `Status`
- `Scope Checked`
- `Decision`
- `Findings`
- `Required Before PASS`
- `Recommended Follow-ups`
- `Escalation`

## Safety gates

- Read-only only.
- No edit, no autofix, no patch, no commit.
- Jangan baca `.env` atau secret.
- Jangan memperluas scope tanpa evidence baru yang relevan.
- Jika bukti kurang, minta bukti atau tandai `BLOCKED`/`NEEDS_FIX` sesuai gap.
