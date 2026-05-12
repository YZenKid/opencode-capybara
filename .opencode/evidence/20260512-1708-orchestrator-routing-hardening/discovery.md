## Discovery

### Tujuan discovery
- Menentukan baseline policy dan gap praktik untuk memperbaiki kualitas routing workflow `@orchestrator`.

### File yang diinspeksi
- `.opencode/docs/AGENT_ROUTING.md`
- `.opencode/docs/TOOL_USAGE.md`
- `.opencode/docs/AGENT_TOOL_ACCESS.md`
- `.opencode/docs/QUALITY.md`
- `package.json`

### Pola dan aturan yang ditemukan
- `@orchestrator` didefinisikan sebagai `router, integrator, final coordinator`.
- Non-trivial work seharusnya melalui `@artifact-planner` terlebih dahulu.
- Discovery yang scope-nya belum jelas seharusnya ke `@explorer`.
- Bounded implementation seharusnya ke `@fixer`.
- Final conformance seharusnya ke `@quality-gate`.
- `TOOL_USAGE.md` menegaskan route-to-role dan anti-pattern menggunakan tool di lane yang salah.
- `QUALITY.md` sudah punya standard loop yang benar, tetapi belum cukup menjamin kepatuhan routing orchestrator pada workflow nyata.

### Reuse candidates
- Reuse definisi lane yang sudah ada di `.opencode/docs/AGENT_ROUTING.md`.
- Reuse boundary wording di `.opencode/docs/AGENT_TOOL_ACCESS.md`.
- Reuse evidence contract dan strict golden path di `.opencode/docs/QUALITY.md`.
- Reuse harness scripts yang sudah ada di `package.json`:
  - `npm run check:docs`
  - `npm run check:agents`
  - `npm run check:skills`
  - `npm run check:evidence`
  - `npm run check:harness`

### Gap yang teridentifikasi
- Belum ada rubric atau gate eksplisit untuk menilai kapan orchestrator overreach.
- Belum ada rule threshold operasional yang tegas untuk membedakan tiny direct task vs task yang wajib didelegasikan.
- Belum terlihat evidence/doctor check khusus yang mendeteksi anti-pattern seperti orchestrator membaca banyak file sendiri lalu tetap mengerjakan implementation lane.
- Standard loop sudah benar secara dokumen, tetapi belum cukup operasional untuk memaksa planner lebih awal dan implementer lane lebih disiplin.

### Constraint
- Planner hanya boleh menulis artifact di bawah `.opencode/`.
- Plan harus cukup konkret untuk dipakai implementer tanpa mencampur implementasi ke artifact planner.
- Perubahan yang direncanakan harus konsisten dengan docs of record yang sudah ada, bukan membuat lane baru yang bertentangan.

### Risiko
- Over-correction dapat membuat orchestrator terlalu kaku dan memperlambat tiny tasks.
- Rule yang terlalu abstrak tidak akan mengubah perilaku runtime nyata.
- Jika hanya docs yang diubah tanpa gate/check, perilaku lama kemungkinan akan kembali.

### Sumber tambahan
- Review workflow share `https://opncd.ai/share/XkQqzZPc` melalui ekstraksi session timeline dan analisis routing berbasis evidence percakapan.
