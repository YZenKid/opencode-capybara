## Discovery

### Tujuan
- Menyusun roadmap lengkap agar kualitas routing orchestrator dan evaluator pendukung bisa realistis naik ke target `5/5`.

### File yang diinspeksi
- `.opencode/docs/AGENT_ROUTING.md`
- `.opencode/docs/EVALS.md`
- `scripts/evals/lib.mjs`
- `.opencode/evidence/20260512-1708-orchestrator-routing-hardening/verification.md`

### State saat ini
- Policy routing sudah punya threshold direct-vs-delegate yang eksplisit.
- Ada anti-pattern dan compact checklist untuk audit routing.
- Evals sudah mencakup:
  - static deterministic gates,
  - task-shaped behavioral fixtures,
  - transcript-shaped fixtures,
  - raw transcript/tool-trace-like normalization,
  - routing score deterministik 0–5.
- Evidence task hardening routing sudah cukup baik dan replayable.

### Kekuatan yang sudah ada
- Rule routing inti sudah jelas dan terdokumentasi.
- Enforcement tidak lagi static-only; sudah ada task-shaped dan transcript-shaped replayable checks.
- Transcript evaluator sudah bisa mendeteksi empat pola overreach utama.
- Harness report sudah bisa menampilkan source mode dan routing score.

### Gap menuju 5/5
- Parser transcript masih heuristik dan belum mendukung format runtime nyata secara robust.
- Normalization masih berbasis inferensi string, belum ada schema adapter untuk source nyata seperti tool trace / session export.
- Scoring 0–5 masih proxy-based dan belum menggabungkan adjudication semantik untuk kasus ambigu.
- Belum ada corpus/golden dataset workflow nyata dengan label good/bad/borderline.
- Belum ada drift watch yang memonitor trend score dari waktu ke waktu.
- Belum ada release gate yang mensyaratkan target minimum transcript score aggregate.

### Reuse candidates
- Reuse struktur fixture JSON yang sudah ada di `scripts/evals/task-fixtures/` dan `scripts/evals/transcript-fixtures/`.
- Reuse harness report pipeline di `scripts/evals/harness-eval-runner.mjs`.
- Reuse checklist/rubric dari `.opencode/docs/AGENT_ROUTING.md` sebagai dasar scoring dimensions.
- Reuse evidence bundle contract yang sudah ada untuk menyimpan hasil evaluasi.

### Constraint
- Perubahan harus tetap deterministic-first; jangan langsung meloncat ke judge-heavy pipeline untuk semua kasus.
- Repo saat ini belum punya parser baku untuk raw session export platform eksternal.
- Roadmap harus menjaga biaya maintenance tetap wajar dan tidak membuat harness terlalu rapuh.

### Risiko utama
- Overfitting evaluator pada fixture sintetis, bukan workflow nyata.
- Parser raw transcript menjadi terlalu spesifik pada satu format dan gagal portabel.
- Scoring menjadi terlihat presisi padahal sinyal dasarnya masih terbatas.
