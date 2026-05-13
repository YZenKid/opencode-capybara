# Goal

Menyusun roadmap lengkap agar kualitas routing orchestrator dan sistem evaluasinya bisa realistis mencapai `5/5`, bukan hanya melalui policy yang baik, tetapi juga lewat enforcement, corpus, scoring, drift monitoring, dan release gating yang kuat.

# Non-goals

- Tidak langsung mengimplementasikan seluruh roadmap dalam plan ini.
- Tidak menjanjikan eliminasi total kebutuhan human review untuk kasus ambigu.
- Tidak mengubah seluruh arsitektur eval menjadi platform judge-heavy sejak awal.

# Scope

- Menetapkan definisi operasional `5/5` untuk kualitas routing orchestrator.
- Mengidentifikasi gap antara state saat ini dan target `5/5`.
- Menyusun workstreams implementasi bertahap: parser, corpus, scoring, adjudication, drift watch, dan release gate.
- Menetapkan validation strategy dan ownership lane per tahap.

# Requirements

1. Definisi `5/5` harus jelas, terukur, dan tidak hanya bersifat opini.
2. Roadmap harus mempertahankan prinsip `Reuse > Extend > Create`.
3. Harus ada jalur peningkatan dari deterministic enforcement ke transcript/runtime confidence yang lebih tinggi.
4. Harus ada corpus replayable untuk good, bad, borderline, dan fallback scenarios.
5. Harus ada release/quality gate berbasis score minimum dan reason-code review.
6. Harus ada strategy untuk mengurangi false positive dan false negative evaluator transcript.
7. Harus ada batasan jelas kapan human/LLM adjudication tetap dibutuhkan.

# Acceptance Criteria

- Terdapat definisi target `5/5` beserta rubric yang lebih operasional dari sekadar checklist saat ini.
- Terdapat roadmap bertahap dengan milestone, output, validation, dan owner lane yang jelas.
- Terdapat rencana corpus + evaluator + release gating yang saling terhubung.
- Terdapat mitigation untuk parser heuristik, fixture overfitting, dan scoring proxy limitations.
- Terdapat done criteria yang bisa dipakai untuk menyatakan “routing system reached near-5/5”.

# Existing Patterns/Reuse

- Reuse threshold, anti-pattern, dan compact routing checklist di `.opencode/docs/AGENT_ROUTING.md`.
- Reuse replay/eval contract di `.opencode/docs/EVALS.md`.
- Reuse evaluator deterministic yang sudah ada di `scripts/evals/lib.mjs` dan `scripts/evals/harness-eval-runner.mjs`.
- Reuse task-shaped dan transcript-shaped fixture folders yang sudah ada.
- Belum ada parser runtime transcript yang benar-benar robust atau corpus labeled workflow nyata; area ini perlu diperluas, bukan direplikasi dari utility yang sudah ada.

# Constraints

- Harus menjaga harness tetap cepat dan stabil pada local runs.
- Harus tetap compatible dengan deterministic checks yang sudah ada.
- Jangan mewajibkan akses platform eksternal untuk semua eval runs.
- Jangan membuat release gate terlalu rapuh sebelum corpus cukup representatif.

# Risks

- **Corpus bias:** dataset terlalu mirip satu repo atau satu gaya orchestrator.
- **Parser fragility:** parser transcript mentah pecah saat format export berubah.
- **Score illusion:** angka 5/5 terlihat presisi padahal sinyal semantiknya belum cukup.
- **Over-gating:** release jadi terlalu sering blocked oleh evaluator yang belum matang.
- **Maintenance burden:** fixture dan parser makin banyak tapi tidak tetap dijaga.

# Decisions/Assumptions

## Decisions
- Target `5/5` didefinisikan sebagai kombinasi: policy clarity + enforcement depth + transcript realism + corpus breadth + release readiness.
- Roadmap dibagi ke milestone bertahap, bukan satu perubahan besar.
- Deterministic evaluator tetap menjadi fondasi; semantic adjudication hanya ditambahkan untuk kasus yang memang ambigu.

## Assumptions / Open Questions
- Diasumsikan maintainers menerima bahwa “5/5” berarti **operational confidence very high**, bukan “sempurna tanpa human review”.
- Diasumsikan repo ingin menjaga local-first validation, jadi parser dan fixtures harus tetap runnable tanpa infrastruktur eksternal.
- Open question minor: apakah nanti score minimum release gate harus `>=4.5` atau `=5.0` untuk fixture corpus inti. Ini bisa diputuskan pada milestone release gating.

# TDD/Test Plan

## TDD required?
Ya, untuk setiap milestone yang menyentuh parser, scorer, corpus, atau release gate.

## Reason
Evaluator routing adalah logic regression-prone. Tanpa TDD, false positive/negative akan sulit dilacak.

## Existing test patterns
- `npm run eval:harness`
- `npm run check:harness:strict`
- task fixtures di `scripts/evals/task-fixtures/`
- transcript fixtures di `scripts/evals/transcript-fixtures/`

## First failing/regression test
- Tambahkan failing raw transcript cases dari workflow nyata yang saat ini belum berhasil dinormalisasi dengan baik.
- Tambahkan borderline fixtures yang harus menghasilkan score parsial, bukan hanya pass/fail total.
- Tambahkan release-gate regression yang gagal jika average transcript score turun di bawah target.

## Green step
- Implement parser adapters, scoring logic, fixture corpus expansion, dan gating sampai seluruh fixture target lulus.

## Refactor step
- Ekstrak parser source adapters per format agar heuristik inti tidak tercampur.
- Konsolidasikan rule scoring ke satu source of truth yang diturunkan dari rubric.

## Edge cases
- Session kecil yang valid tetapi tidak butuh planner.
- Fallback specialist unavailable yang sah dan terdokumentasi.
- Workflow yang sengaja exploratory dan belum implementasi.
- Transcript dengan noise tinggi atau tool trace yang parsial.

## Commands
- `npm run test:prompt-gates`
- `npm run check:docs`
- `npm run check:agents`
- `npm run check:skills`
- `npm run check:evidence`
- `npm run eval:harness`
- `npm run check:harness:strict`
- `npm run doctor`

# Implementation Steps

## Milestone 1 — Solidify transcript foundation
1. Pisahkan parser transcript ke adapter yang jelas per source mode:
   - normalized events,
   - raw transcript text,
   - raw tool trace,
   - future session export adapter.
2. Tambahkan schema validation ringan untuk fixture transcript.
3. Tambahkan regression cases untuk format yang ambigu atau noisy.

## Milestone 2 — Expand labeled routing corpus
4. Buat corpus `good / bad / borderline / fallback-valid` dari workflow nyata dan sintetis.
5. Simpan metadata label per fixture:
   - expected score range,
   - expected reason codes,
   - why this case matters.
6. Tambahkan fixture dari failure history nyata, termasuk share/session yang pernah dikritik.

## Milestone 3 — Upgrade routing scoring model
7. Ubah score dari sekadar 5 boolean menjadi rubric yang lebih granular:
   - lane fit,
   - timing quality,
   - delegation clarity,
   - evidence completeness,
   - closure quality.
8. Tambahkan `score_band` seperti `poor`, `usable`, `strong`, `excellent`.
9. Tambahkan confidence/coverage note pada tiap transcript result.

## Milestone 4 — Introduce transcript realism adapters
10. Tambahkan parser/adaptor untuk raw session export nyata atau tool trace format yang benar-benar dipakai repo/platform.
11. Uji roundtrip parser pada sample anonymized transcripts.
12. Minimalkan inferensi string bebas dengan schema mapping yang lebih eksplisit.

## Milestone 5 — Add semantic adjudication lane for ambiguity
13. Definisikan kapan deterministic evaluator cukup dan kapan semantic review dibutuhkan.
14. Tambahkan optional semantic adjudication fixture lane hanya untuk transcript borderline.
15. Simpan semantic verdict terpisah dari deterministic score agar hasil tetap audit-friendly.

## Milestone 6 — Drift watch and release gating
16. Tambahkan aggregate metrics pada harness report:
   - average transcript score,
   - min score,
   - failing reason-code trend,
   - source-mode coverage.
17. Tambahkan release gate policy:
   - fixture corpus inti harus pass,
   - average transcript score minimum,
   - no critical reason-code regressions.
18. Tambahkan historical snapshot/report agar drift bisa diamati lintas release.

## Milestone 7 — Close the loop into maintainer workflow
19. Tambahkan docs operasional untuk cara menambah fixture dari workflow nyata.
20. Wajibkan setiap failure routing baru menghasilkan fixture regression baru.
21. Tambahkan checklist release untuk mengecek transcript corpus freshness dan score trend.

# Expected Files to Change

- `.opencode/docs/EVALS.md`
- `.opencode/docs/QUALITY.md`
- `.opencode/docs/RELEASE.md`
- `scripts/evals/lib.mjs`
- `scripts/evals/harness-eval-runner.mjs`
- `scripts/evals/transcript-fixtures/*`
- `scripts/evals/task-fixtures/*`
- kemungkinan file helper baru di `scripts/evals/`
- generated report yang terkait jika inventory fixtures berubah

# Agent/Tool Routing

- `@artifact-planner`
  - menulis roadmap dan evidence artifact.
- `@explorer`
  - memetakan failure history, fixture corpus yang ada, dan candidate workflow transcripts.
- `@fixer`
  - mengimplementasikan parser, scorer, fixtures, dan release-gate logic secara bounded.
- `@oracle`
  - review tradeoff scoring, false positive/negative, dan kapan semantic adjudication dibutuhkan.
- `@quality-gate`
  - final conformance review per milestone material.
- `@platform-architect`
  - optional ketika release gating, trend reports, dan automation policy mulai material.

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
- `npm run eval:harness`
- `npm run check:harness:strict`
- `npm run doctor`

# Evidence Requirements

Untuk setiap milestone implementasi, minimal harus ada:

1. `discovery.md` dengan source transcripts/fixtures yang dipakai.
2. `verification.md` yang mencatat:
   - commands,
   - report score summary,
   - failing/cleared reason codes.
3. Jika parser baru ditambahkan, contoh input/output normalization yang terdokumentasi.
4. Jika score berubah, before/after comparison terhadap corpus inti.
5. Jika release gate baru ditambahkan, bukti threshold pass/fail yang replayable.

Untuk target mendekati `5/5`, evidence harus menunjukkan:
- corpus inti representatif,
- transcript score aggregate stabil tinggi,
- regression failures menghasilkan fixture baru,
- no unexplained drift pada score atau reason-code trend.

# Done Criteria

Roadmap ini dianggap tereksekusi menuju `near-5/5` bila:

- Parser transcript nyata tidak lagi bergantung dominan pada heuristik string rapuh.
- Corpus inti mencakup good/bad/borderline/fallback scenarios yang representatif.
- Transcript scoring memiliki granularitas dan confidence yang cukup untuk release decisions.
- Release gate memakai transcript metrics, bukan hanya static checks.
- Failure baru secara konsisten menghasilkan regression fixture baru.
- `@quality-gate` bisa memberi `PASS` atau `PASS_WITH_RISKS` tanpa alasan “static-only” atau “coverage too narrow”.

# Final Planning Summary

- **Artifacts created:**
  - `.opencode/plans/20260512-1822-routing-5of5-roadmap.md`
  - `.opencode/evidence/20260512-1822-routing-5of5-roadmap/discovery.md`
- **Key decisions:** target 5/5 didefinisikan sebagai confidence operasional tinggi; deterministic foundation dipertahankan lalu diperluas dengan corpus, parser nyata, scoring yang lebih kaya, dan release gating.
- **Assumptions:** local-first validation tetap dipertahankan; human review masih mungkin dibutuhkan untuk kasus ambigu.
- **Open questions:** threshold score release gate final (`>=4.5` vs `=5.0`) bisa diputuskan pada milestone gating.
- **Readiness for implementation:** siap untuk implementasi bertahap oleh `@fixer`, dimulai dari parser adapters dan corpus expansion.
- **Cleanup performed:** tidak ada draft tambahan yang dipertahankan; discovery diringkas ke evidence dan plan utama.
- **Source of truth:** file primary plan ini adalah sumber kebenaran untuk roadmap menuju routing score 5/5.
