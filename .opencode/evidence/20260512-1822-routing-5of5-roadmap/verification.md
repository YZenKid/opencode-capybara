## Summary
- Roadmap menuju routing score 5/5 berhasil diterjemahkan menjadi peningkatan konkret pada parser transcript, scoring, corpus, drift-watch, dan release gating lokal.

## Changes
- Menambahkan schema validation ringan untuk transcript fixtures.
- Menambahkan source adapters yang lebih eksplisit untuk `events`, `rawTranscript`, `rawToolTrace`, dan `shareExport`.
- Mengekstrak parser `shareExport` ke util terpisah agar heuristik adapter tidak terus menumpuk di `scripts/evals/lib.mjs`.
- Menambahkan scoring yang lebih kaya: `score_band`, `confidence`, `coverage`, `classification`, dan `release_critical`.
- Memperketat scoring transcript sparse agar `shareExport` yang hanya menghasilkan satu cue/line tidak otomatis tampak planner-first dan final-gate complete.
- Menambahkan corpus transcript baru untuk `borderline`, `fallback-valid`, dan `shareExport` real-session style scenarios, termasuk noisy-negative, malformed-partial, dan keyword-noise boundary coverage.
- Menambahkan drift summary dan release-gate readiness ke harness eval report.
- Menambahkan `scripts/evals/release-gate-check.mjs` dan script package `check:routing-release` / `check:release`.
- Memperbarui docs `.opencode/docs/EVALS.md`, `.opencode/docs/QUALITY.md`, dan `.opencode/docs/RELEASE.md` untuk workflow maintainer dan release gating.
- Memperbarui `package.json` untuk mengekspose release gate baru dalam workflow lokal.
- Memperluas `scripts/evidence-contract-check.mjs` agar replay bundle juga mensyaratkan `drift_summary` dan `release_gate_readiness`.
- Memperbarui `.opencode/evidence/20260512-1708-orchestrator-routing-hardening/verification.md` agar capability transcript terbaru tercatat konsisten lintas task.

## Evidence
- Command: `npm run test:prompt-gates`
- Result: PASS

- Command: `npm run check:docs`
- Result: PASS

- Command: `npm run check:agents`
- Result: PASS

- Command: `npm run check:skills`
- Result: PASS

- Command: `npm run eval:harness`
- Result: PASS

- Command: `npm run check:harness:strict`
- Result: PASS

- Command: `npm run check:routing-release`
- Result: PASS

- Command: `npm run check:release`
- Result: PASS

- Command: `npm run check:evidence`
- Result: PASS setelah report harness terbaru dan evidence roadmap ini tersedia.

## Parser Example
- Input source mode baru: `shareExport` dengan payload HTML/share export lokal yang memuat string transcript-like di dalam `<script>` payload.
- Normalization strategy: ekstraksi string candidate dari field seperti `content`, `message`, `notes`, `summary`, atau quoted text yang memuat cue agent/action; decode escape JS umum (`\n`, `\xNN`, `\uNNNN`); dedupe; saring hanya candidate yang tampak seperti line transcript terstruktur (agent/action cues + ordering/prefix transcript-like); lalu turunkan ke event via heuristik `inferAgent`, `inferAction`, `inferFileCount`, `inferMaterial`, dan `inferNonTrivial`.
- Scoring guardrail tambahan: transcript yang terlalu sparse (`event_count < 2`) tidak boleh otomatis mendapat kredit penuh untuk `planner_first` dan `final_gate_presence`.
- Representative fixtures:
  - `scripts/evals/transcript-fixtures/routing-share-export-compliant-positive.json`
  - `scripts/evals/transcript-fixtures/routing-share-export-noisy-negative.json`
  - `scripts/evals/transcript-fixtures/routing-share-export-malformed-partial.json`
  - `scripts/evals/transcript-fixtures/routing-share-export-keyword-noise-boundary.json`

## Risks / Limitations
- Target `5/5` kini jauh lebih dekat secara operasional, tetapi adapter `shareExport` masih berbasis ekstraksi heuristik dari payload HTML/script dan belum menjadi schema runtime final lintas environment.
- Semantic adjudication untuk kasus sangat ambigu masih belum otomatis; deterministic + fixture corpus tetap menjadi fondasi utama.

## Next Steps
- Tambahkan adapter parser untuk format export/session nyata ketika format tersebut sudah distabilkan.
- Tambahkan corpus workflow nyata yang lebih beragam agar release-critical score threshold makin representatif.
