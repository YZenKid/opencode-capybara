# Golden Principles

## 1. Calm orchestration over aggressive automation
Pilih rute yang aman, jelas, dan reversible daripada aksi cepat yang tidak terverifikasi.

## 2. Evidence before confidence
Final summary harus menyertakan evidence: test, command output, screenshot, lint, diff, atau risk note.

## 3. Boundaries are product features
Setiap agent punya scope jelas. Implementer, reviewer, planner, dan gatekeeper tidak boleh dicampur sembarangan.

## 4. No hidden side effects
Tidak boleh ada install hook tersembunyi, auto-enable risky rewriting, atau network action diam-diam.

## 5. Prompt rules must be testable
Jika sebuah aturan penting, ia harus punya regression case, lint, script, atau checklist.

## 6. Prefer small enforceable rules over long prose
Instruksi panjang harus dipromosikan menjadi script, gate, template, atau skill contract.

## 7. Repo-local knowledge wins
Jika keputusan penting hanya ada di chat, issue, atau kepala manusia, agent harus menganggap knowledge tersebut belum stabil sampai didokumentasikan di repo.

## 8. Cleanup is continuous
AI slop dan prompt drift harus dibersihkan secara berkala melalui small targeted changes.

## 9. Humans steer. Agents execute.
Manusia menetapkan intent, prioritas, acceptance criteria, dan keputusan produk. Agent mengeksekusi dalam batas harness.

## 10. Harness constrains. Evidence proves.
Kontrol preventif, checks mekanis, dan evidence replayable harus lebih dipercaya daripada keyakinan lisan.

## 11. Compression follows the approved toolchain
Jika token compression atau context packing dibutuhkan, gunakan RTK dan Caveman secara bersamaan sesuai workflow yang sudah disetujui oleh repo. Jangan membuat jalur compression lokal paralel atau memperlakukan RTK dan Caveman sebagai pilihan salah satu di luar setup, docs, dan gates resmi.
