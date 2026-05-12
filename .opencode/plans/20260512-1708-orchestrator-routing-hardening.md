# Goal

Memperbaiki workflow routing `@orchestrator` agar lebih disiplin mendelegasikan discovery, planning, implementation, dan review ke lane yang tepat, sekaligus menurunkan kecenderungan orchestrator melakukan read-heavy discovery dan multi-file implementation secara langsung.

# Non-goals

- Tidak mendesain ulang seluruh arsitektur agent.
- Tidak menambah agent baru.
- Tidak mengubah policy yang sudah benar hanya demi konsistensi wording.
- Tidak mengimplementasikan perubahan pada plan ini di fase artifact planning.

# Scope

- Menetapkan rule operasional yang lebih tegas untuk direct work vs delegation oleh `@orchestrator`.
- Menentukan perubahan docs, skill prompt, dan guardrail/check yang diperlukan.
- Menentukan validation path agar perbaikan routing bisa diverifikasi setelah implementasi.
- Menentukan evidence yang harus tersedia agar claim “routing improved” tidak hanya normatif.

# Requirements

1. Workflow harus mempertahankan `@orchestrator` sebagai router/integrator utama, bukan worker dominan.
2. Non-trivial task harus lebih dini diarahkan ke `@artifact-planner`.
3. Unknown-scope discovery harus default ke `@explorer`.
4. Bounded implementation multi-file harus default ke `@fixer`.
5. Final signoff untuk perubahan material harus default ke `@quality-gate`.
6. Harus ada threshold operasional yang jelas untuk tiny direct tasks yang masih boleh dikerjakan orchestrator.
7. Harus ada rubric/checklist yang bisa dipakai untuk menilai kualitas routing pada workflow nyata.
8. Harus ada minimal satu guardrail yang membuat anti-pattern routing lebih sulit terjadi tanpa terdeteksi.

# Acceptance Criteria

- Terdapat policy tertulis yang eksplisit tentang kapan orchestrator boleh read/edit langsung dan kapan wajib delegate.
- Terdapat rubric scoring atau checklist audit yang dapat dipakai reviewer untuk menilai workflow orchestrator.
- Terdapat update pada skill/prompt orchestrator agar delegation threshold muncul sebagai instruksi utama, bukan implicit preference.
- Terdapat rencana penambahan doctor/check atau evidence contract yang memaksa bukti routing pada task non-trivial.
- Terdapat validation plan yang menjalankan checks docs/agents/skills/evidence terkait.
- Terdapat contoh anti-pattern dan expected remediation path di dokumen final.

# Existing Patterns/Reuse

- Reuse `Default flow` dan `Primary lanes` dari `.opencode/docs/AGENT_ROUTING.md`.
- Reuse `preferred/permitted/fallback` model dari `.opencode/docs/AGENT_TOOL_ACCESS.md`.
- Reuse `role-appropriate tool paths` dan anti-pattern guidance dari `.opencode/docs/TOOL_USAGE.md`.
- Reuse `Standard agent loop` dan `Evidence contract` dari `.opencode/docs/QUALITY.md`.
- Belum ditemukan utility/rubric lokal yang sudah secara spesifik mengukur orchestrator overreach; area ini perlu dibuat/ditambahkan, bukan di-reimplement dari utility yang sudah ada.

# Constraints

- Perubahan harus menjaga tugas trivial tetap cepat dan tidak memaksa delegation berlebihan.
- Dokumen utama tetap harus pendek, tegas, dan bisa dipakai sebagai rule operasional.
- Jika check baru direncanakan, check tersebut harus bisa dijalankan lewat jalur harness yang ada atau ditambahkan secara minimal.
- Plan ini hanya mengatur perbaikan repo policy/skill/check; tidak mencakup perubahan pada platform eksternal `opncd.ai`.

# Risks

- Rule terlalu longgar → perilaku lama tetap terjadi.
- Rule terlalu kaku → tiny tasks menjadi lambat dan agent terlihat birokratis.
- Rubric tanpa enforcement → hanya menjadi dokumen pasif.
- Check heuristik yang terlalu naif → false positive pada workflow kecil yang valid.

# Decisions/Assumptions

## Decisions
- Gunakan pendekatan `Reuse > Extend > Create`.
- Fokus perbaikan pada tiga lapis: policy docs, orchestrator skill prompt, dan validation/evidence checks.
- Anggap masalah utama bukan ketiadaan lane, melainkan kurang tegasnya threshold dan enforcement.

## Assumptions / Open Questions
- Diasumsikan maintainers ingin mempertahankan `@orchestrator` sebagai lane yang tetap boleh mengerjakan tiny direct task.
- Diasumsikan perubahan perilaku paling efektif datang dari kombinasi docs + prompt + check, bukan dari docs saja.
- Tidak ada open question material yang memblokir plan awal ini; jika maintainers ingin mode yang lebih ketat, threshold tiny task dapat diperkecil saat implementasi.

# TDD/Test Plan

## TDD required?
Ya, untuk logic perubahan guardrail/check dan regression behavior pada docs/skill validation.

## Reason
Perubahan menyasar behavior harness/policy yang mudah regress jika tidak ada bukti otomatis.

## Existing test patterns
- Harness checks via scripts di `package.json`.
- Prompt gate regression melalui `npm run test:prompt-gates`.
- Docs/agents/skills/evidence checks melalui script integrity yang sudah ada.

## First failing/regression test
- Tambahkan regression expectation bahwa orchestrator guidance wajib memuat threshold direct-work vs delegation yang eksplisit.
- Tambahkan expectation bahwa docs routing/quality/agent boundary menyebut planner-first untuk non-trivial work dan implementer-lane untuk bounded implementation.
- Jika doctor/check baru dibuat, mulai dengan failing case berupa contoh workflow metadata atau static fixture yang menunjukkan orchestrator overreach tanpa delegation.

## Green step
- Update docs dan skill prompt agar semua assertions lulus.
- Tambahkan check/fixture minimum untuk mendeteksi missing routing guardrail atau missing routing evidence pada task non-trivial.

## Refactor step
- Sederhanakan wording yang duplikatif antar `AGENT_ROUTING.md`, skill orchestrator, dan `QUALITY.md`.
- Pastikan satu source of truth utama untuk threshold, lalu dokumen lain merujuk atau merangkum secara konsisten.

## Edge cases
- Tiny single-file doc patch yang tetap sah dikerjakan orchestrator.
- Discovery kecil untuk verifikasi satu file sesudah hasil `@explorer` datang.
- Specialist unavailable: fallback tetap boleh, tetapi harus dicatat sebagai limitation dan bukan default habit.

## Commands
- `npm run test:prompt-gates`
- `npm run check:docs`
- `npm run check:agents`
- `npm run check:skills`
- `npm run check:evidence`
- `npm run check:harness`

# Implementation Steps

1. **Audit dan source-of-truth alignment**
   - Tentukan dokumen utama threshold routing, disarankan `.opencode/docs/AGENT_ROUTING.md`.
   - Petakan bagian mana di skill orchestrator, `QUALITY.md`, dan `AGENT_TOOL_ACCESS.md` yang perlu diringkas/dirujuk ulang.

2. **Tambahkan aturan threshold direct vs delegate**
   - Tambahkan rule eksplisit untuk:
     - tiny direct tasks,
     - unknown-scope discovery,
     - bounded multi-file implementation,
     - required final gate untuk material changes.
   - Sertakan anti-pattern seperti “delegate discovery lalu tetap baca banyak file sendiri”.

3. **Masukkan rubric audit routing**
   - Tambahkan rubric 0–5 atau checklist audit ke docs operasional, kemungkinan di `.opencode/docs/QUALITY.md` atau dokumen turunan yang dirujuk dari sana.
   - Pastikan rubric bisa dipakai pada post-task review dan contoh workflow share.

4. **Perketat prompt/skill orchestrator**
   - Update skill `opencode-orchestrator` agar delegation threshold menjadi instruksi operasional eksplisit.
   - Tambahkan larangan soft terhadap multi-file read-heavy discovery langsung oleh orchestrator kecuali verifikasi minimum.

5. **Rencanakan enforcement minimal**
   - Tambahkan atau perluas doctor/check untuk mendeteksi setidaknya satu dari berikut:
     - missing planner-first reminder,
     - missing implementation-lane wording,
     - missing routing rubric reference,
     - evidence task non-trivial tanpa jejak routing yang memadai.
   - Jika runtime workflow lint penuh terlalu mahal, mulai dari static doc/skill assertions plus evidence contract checks.

6. **Tambahkan evidence contract untuk routing quality**
   - Pada task non-trivial, final summary/evidence harus menyebut:
     - agent yang dipakai,
     - alasan delegation,
     - validation lane,
     - limitation bila orchestrator terpaksa fallback.

7. **Siapkan exemplar / regression fixture**
   - Buat satu contoh “bad routing” dan satu “good routing” sebagai fixture doc atau test input untuk menjaga perilaku review tetap konsisten.

8. **Run validation dan review akhir**
   - Jalankan semua commands validation.
   - Minta `@quality-gate` review pada implementasi material nanti sebelum claim selesai.

# Expected Files to Change

- `.opencode/docs/AGENT_ROUTING.md`
- `.opencode/docs/QUALITY.md`
- `.opencode/docs/AGENT_TOOL_ACCESS.md`
- `.opencode/docs/TOOL_USAGE.md` (hanya jika guidance selection perlu dirapikan)
- `skills/opencode-orchestrator/SKILL.md`
- `scripts/doctor.mjs` atau script integrity/doctor lain yang relevan
- `scripts/prompt-gate-regression.mjs` atau file regression terkait
- File docs generated/check bila repo memang menjaga turunan generated docs dari perubahan policy

# Agent/Tool Routing

- `@artifact-planner`:
  - menulis plan dan evidence artifact.
- `@explorer`:
  - bila implementer perlu memetakan semua file policy/skill/check yang terkena.
- `@fixer`:
  - melakukan perubahan bounded pada docs, skill, scripts, dan regression checks.
- `@oracle`:
  - optional jika terjadi tradeoff antara flexibility vs enforcement atau false positive risk pada check.
- `@quality-gate`:
  - wajib untuk final conformance review karena perubahan ini material terhadap workflow repo.

Tool path yang disarankan:
- discovery: `glob` + `grep` + `read`
- edits: `apply_patch`
- validation: `bash`

# Validation Commands

- `npm run test:prompt-gates`
- `npm run check:docs`
- `npm run check:agents`
- `npm run check:skills`
- `npm run check:evidence`
- `npm run check:harness`

# Evidence Requirements

Implementasi nanti harus menghasilkan minimal:

1. `discovery.md` yang mencatat file policy, skill, dan scripts yang disentuh.
2. `verification.md` yang mencatat hasil command validation.
3. Ringkasan routing decision yang menyebut:
   - kapan orchestrator delegate,
   - lane apa yang dipilih,
   - alasan fallback bila tidak delegate.
4. Jika check baru dibuat, bukti bahwa bad fixture gagal sebelum fix dan lulus sesudah fix.
5. Jika exemplar workflow ditambahkan, link/path ke contoh good vs bad routing.

Jika evidence runtime workflow belum otomatis tersedia, limitation itu harus disebut eksplisit di final summary.

# Done Criteria

- Policy threshold direct-vs-delegate tertulis jelas dan konsisten.
- Skill orchestrator memuat guardrail routing yang lebih tegas.
- Regression checks relevan diperbarui dan lulus.
- Validation harness lulus minimal pada scope perubahan terkait.
- `@quality-gate` memberikan verdict final yang bukan `BLOCKED`.
- Final summary implementasi menyertakan evidence routing, bukan hanya klaim policy.

# Final Planning Summary

- **Artifacts created:**
  - `.opencode/plans/20260512-1708-orchestrator-routing-hardening.md`
  - `.opencode/evidence/20260512-1708-orchestrator-routing-hardening/discovery.md`
- **Key decisions:** fokus pada docs + skill prompt + enforcement minimal; tidak membuat lane baru.
- **Assumptions:** tiny direct task tetap diperbolehkan; kombinasi docs/prompt/check dianggap jalur perubahan paling efektif.
- **Open questions:** tidak ada blocker material untuk memulai implementasi.
- **Readiness for implementation:** siap diimplementasikan oleh lane `@fixer` dengan review akhir `@quality-gate`.
- **Cleanup performed:** tidak ada draft terpisah yang dipertahankan; detail discovery sudah dikonsolidasikan ke evidence dan primary plan.
- **Source of truth:** file primary plan ini adalah sumber kebenaran implementasi.
