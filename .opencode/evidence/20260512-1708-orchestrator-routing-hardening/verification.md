## Summary
- Validasi hardening routing orchestrator berhasil setelah memperketat docs/skill/check, menyegarkan generated docs, dan melengkapi evidence task agar sesuai dengan diff final.

## Changes
- Menambahkan threshold direct-vs-delegate di `.opencode/docs/AGENT_ROUTING.md`.
- Menambahkan anti-pattern dan compact routing checklist di `.opencode/docs/AGENT_ROUTING.md`.
- Memperketat `skills/opencode-orchestrator/SKILL.md` agar multi-file discovery/implementation tidak tetap tinggal di orchestrator.
- Menambahkan invariant routing di `.opencode/docs/PROMPT_GATES.md`.
- Menambah enforcement pada `scripts/prompt-gate-regression.mjs` dan `scripts/doctor.mjs`.
- Menyegarkan `docs/generated/prompt-gate-report.md` melalui `npm run docs:generate` agar freshness check lulus.
- Menambahkan behavioral task fixture `scripts/evals/task-fixtures/orchestrator-routing-discipline-20260512-1708.json` untuk memvalidasi bundle workflow routing secara lebih end-to-end.
- Memperbarui `.opencode/docs/EVALS.md` agar fixture behavioral baru terdaftar dalam suite runnable repo.
- Menambahkan transcript-level evaluator pada `scripts/evals/lib.mjs` dan `scripts/evals/harness-eval-runner.mjs`.
- Menambahkan transcript fixtures `scripts/evals/transcript-fixtures/routing-overreach-negative.json` dan `scripts/evals/transcript-fixtures/routing-compliant-positive.json`.
- Menambahkan parser input transcript mentah (`rawTranscript` dan `rawToolTrace`) ke evaluator transcript.
- Menambahkan scoring routing otomatis 0–5 pada hasil transcript eval.
- Menambahkan transcript fixtures `scripts/evals/transcript-fixtures/routing-raw-overreach-negative.json` dan `scripts/evals/transcript-fixtures/routing-raw-compliant-positive.json`.
- Menambahkan schema validation ringan untuk transcript fixtures sebelum evaluasi dijalankan.
- Menambahkan score band, confidence/coverage metadata, drift summary, dan release-gate readiness pada harness eval report.
- Menambahkan transcript fixtures baru untuk `borderline` dan `fallback-valid` scenarios.
- Menambahkan release gate lokal `npm run check:routing-release` dan agregasi `npm run check:release`.
- Memperbarui docs maintainer workflow di `.opencode/docs/EVALS.md`, `.opencode/docs/QUALITY.md`, dan `.opencode/docs/RELEASE.md`.

## Evidence
- Command: `npm run test:prompt-gates`
- Result: PASS

- Command: `npm run check:docs`
- Result: PASS

- Command: `npm run check:agents`
- Result: PASS

- Command: `npm run check:skills`
- Result: PASS

- Command: `npm run check:evidence`
- Result: PASS setelah artifact `verification.md` dan `index.json` ditambahkan.

- Command: `npm run doctor`
- Result: PASS

- Command: `npm run eval:harness`
- Result: PASS

- Command: `npm run check:harness:strict`
- Result: PASS

- Command: `npm run check:routing-release`
- Result: PASS

- Command: `npm run check:release`
- Result: PASS

- Additional validation:
  - `npm run docs:generate` dijalankan untuk memperbarui generated docs yang stale.
  - Behavioral eval baru memverifikasi bahwa task bundle `20260512-1708-orchestrator-routing-hardening` benar-benar plan-bound, memiliki routing decision artifact, merekam quality outcome, dan selaras dengan policy/skill routing.
  - Transcript evaluator baru mendeteksi pola overreach seperti redundant orchestrator discovery setelah explorer delegation, direct multi-file edit oleh orchestrator, missing planner-first, dan missing quality-gate sebelum material completion claim.
  - Transcript evaluator kini menerima `events`, `rawTranscript`, dan `rawToolTrace`, lalu mengeluarkan `transcript_source_mode` serta `routing_score` 0–5.
  - Transcript evaluator kini juga memberi schema validation ringan, `score_band`, `confidence`, `coverage`, dan aggregate drift / release-gate readiness di harness report.
  - Final changed-file set yang tervalidasi untuk hardening ini kini mencakup parser, scorer, release gate, corpus transcript yang lebih luas, dan docs maintainer workflow terkait.

## Risks / Limitations
- Enforcement kini tidak hanya statis; repo sudah memiliki behavioral eval task-shaped dan transcript-shaped yang replayable.
- Transcript evaluator kini bisa mem-parse transcript mentah dan tool-trace-like fixtures ke normalized events, tetapi belum parser otomatis untuk seluruh format transcript runtime nyata yang mungkin bervariasi antar lingkungan.
- Scoring dan release gating kini jauh lebih kuat, tetapi semantic adjudication untuk kasus sangat ambigu masih belum otomatis.

## Next Steps
- Jika maintainers ingin coverage lebih jauh lagi, langkah berikutnya adalah menambah fixture good-vs-bad routing berbasis transcript atau evaluator semantic untuk tool trace nyata.
