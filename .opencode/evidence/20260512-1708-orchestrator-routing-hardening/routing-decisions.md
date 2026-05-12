## Routing Decision Summary

### Kapan orchestrator delegate pada task ini
- **Planning non-trivial** dikerjakan melalui lane artifact planning lebih dulu, sesuai plan-bound workflow.
- **Bounded implementation** didelegasikan ke lane implementasi karena perubahan menyentuh banyak file policy/skill/check.
- **Final conformance review** didelegasikan ke `@quality-gate` karena perubahan ini material terhadap workflow repo.

### Lane yang dipilih dan alasannya
- **`@artifact-planner`**
  - Alasan: task bersifat non-trivial, butuh primary plan, evidence path, dan acceptance criteria yang eksplisit.
- **`@fixer`**
  - Alasan: implementasi menyentuh lebih dari dua file dan termasuk docs, skill prompt, serta check scripts; ini tepat untuk bounded implementation lane.
- **`@quality-gate`**
  - Alasan: repo policy berubah secara material dan perlu final conformance verdict read-only sebelum dianggap selesai.

### Validation lane
- Validasi dijalankan di orchestrator menggunakan command harness repo:
  - `npm run test:prompt-gates`
  - `npm run docs:generate`
  - `npm run check:docs`
  - `npm run check:agents`
  - `npm run check:skills`
  - `npm run check:evidence`
  - `npm run doctor`

### Fallback dan limitation
- **Tidak ada fallback specialist yang dipakai** untuk implementasi utama; lane yang direncanakan tersedia.
- Orchestrator hanya melakukan inspeksi minimum, menjalankan validasi, dan mengintegrasikan hasil.
- Limitation residu tetap ada: enforcement routing masih lebih kuat di level docs/prompt/check statis daripada transcript runtime evaluator.
