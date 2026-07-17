# Discovery — patch routing dan scope preset

- task_id: `20260716-1535-preset-scope-routing`
- status: `confirmed_repo` dan `confirmed_docs`
- target: `/var/home/ujang/.config/opencode`

## Files diperiksa

| Path | Bukti | Dampak pada rencana |
|---|---|---|
| `agents/orchestrator.md` | 655 baris; `Plan-first` memakai default ke planner saat ragu; preflight/MCP muncul dua kali; finish-first ada pada workflow implementasi | Core patch: klasifikasi intent sebelum size/risk; hilangkan duplikasi; pisahkan audit dari eksekusi. |
| `skills/opencode-orchestrator/SKILL.md` | 700+ baris; duplicate routing rules terlihat pada `Core routing`; policy memadukan audit dan implementasi | Jadikan skill ringkas sebagai referensi canonical docs, bukan policy copy. |
| `.opencode/docs/AGENT_ROUTING.md` | Ada rubric `tiny/small/material/greenfield`, Fast path, dan `tiny-readonly-compare` sudah tercatat pada evidence A1 | Jadikan satu source of truth untuk classifier, route, dan budget. |
| `agents/explorer.md` | Read-only lane sudah punya `stop discovery when answer is found`; namun preflight tetap wajib di luar fast class | Tambah `read_only_compare` protocol tanpa preflight/prompt-plan overhead. |
| `agents/artifact-planner.md` | Planner diinstruksikan triggered-only, tapi orchestrator masih default-plan pada keraguan | Tambah hard stop: planner hanya setelah intent implementation + trigger material. |
| `.opencode/plans/20260716-preset-fastpath.md` | Plan terdahulu sudah membuat class `tiny-readonly-compare`; A3/A4 diblokir karena planner read-only | Reuse keputusan/routing, tidak duplikasi class atau tambah lane. |
| `.opencode/plans/20260716-opencode-preset-optimization.md` | Workstream WS0–WS6, evaluasi, risk, rollback sudah ada | Plan ini mengoperasionalkan patch policy spesifik sebagai slice berikutnya. |
| `.opencode/evidence/20260716-preset-fastpath/A2-blocker.md` | 45 heading preflight; target global `<3` konflik dengan Diff Boundary | Dedupe hanya file allow-list, tidak cleanup global. |
| `.opencode/evidence/20260716-preset-fastpath/A3-blocker.md` | Planner tidak dapat edit script/test/config dan tidak dapat delegate ke fixer | Handoff eksekusi harus dimulai dari orchestrator ke fixer; planner tidak menerima tugas implementasi. |
| `scripts/session-trace-audit.py` | Saat ini audit heuristic untuk skill/MCP; tidak punya classifier intent, scope promotion, maupun budget pemeriksaan | Extend script + test existing, bukan script baru. |
| `scripts/tests/session-trace-audit.test.py` | Test harness Python sudah ada | Tambah fixtures/assertions di test lama. |
| `package.json` | Memiliki `test:session-trace`, `test:session-trace-strict`, `check:harness`, `check:docs`, `check:agents`, `check:skills` | Gunakan command existing; jangan tambah dependency. |
| `opencode.json` | `9router/fast` sudah terdaftar; default model env-based; built-in agents disabled | Per-agent `model` valid menurut docs, tetapi routing per-request tidak otomatis bisa memakai model berbeda tanpa command/agent khusus. Tidak ubah config dalam slice sampai behavior terbukti. |

## Reference eksternal

- `confirmed_docs`: https://opencode.ai/docs/agents/ menyatakan frontmatter agent mendukung `model`, `steps`, dan `permission`; `steps` membatasi iterasi agentik. Plan memakai ini hanya sebagai opsi setelah compatibility smoke, bukan fakta runtime preset.
- `confirmed_runtime`: session share `https://opncd.ai/share/3Zkecssn` mencatat 422 turn `tool-calls`, 489 pesan assistant, 49 turn stop, sekitar 34,5 jam wall-clock, dan 50 path file terdampak. Prompt awal adalah audit read-only PRD/SRD vs code.

## Confirmed vs Assumed Audit

| Klaim | Level | Bukti |
|---|---|---|
| `@orchestrator` terlalu besar dan memiliki duplicated preflight | `confirmed_repo` | `agents/orchestrator.md:221-245`, `233-245`; file 655 baris. |
| Planner sudah declared triggered-only | `confirmed_repo` | `agents/artifact-planner.md:96-99`. |
| Planner tetap mudah dipicu dari orchestrator | `confirmed_repo` | `agents/orchestrator.md:254-257`; `AGENT_ROUTING.md:25-32`. |
| Audit dapat melebar menjadi implementation bila tidak ada promotion gate | `confirmed_runtime` | share session awal read-only lalu payload mencatat source/test/plan paths. |
| `model` agent override adalah format resmi | `confirmed_docs` | OpenCode Agents docs, retrieved 2026-07-16. |
| `9router/fast` akan dipilih otomatis untuk classifier baru | `unverified` | inventory ada di `opencode.json`; runtime routing per request belum dibuktikan. |
| Max `steps` perlu dipakai pada existing primary agent | `assumption` | docs mendukung field, tetapi efek UX/cost harus dibenchmark sebelum config edit. |

## Reuse dan batas

- Reuse `tiny-readonly-compare`; tidak membuat lane `@reviewer` atau `@read-only-advisor`.
- Reuse `scripts/session-trace-audit.py` dan test existing.
- Reuse plan/evidence fastpath dan optimization; tidak rewrite sejarah A1/A2.
- Tidak ada source application, dependency, lockfile, atau MCP baru.

## Risiko

1. Rule keyword-only dapat salah klasifikasi security review sebagai audit kecil. Mitigasi: classifier menang bila explicit no-change *dan* tidak ada risk trigger; unknown selalu eskalasi read-only deep, bukan implementation.
2. Budget tool yang keras dapat merusak audit yang valid. Mitigasi: `tiny-readonly-compare` hard budget; `read-only-deep-review` advisory budget dan explicit stop/report checkpoint.
3. Dedupe global prompt membuat diff besar dan regresi lintas lane. Mitigasi: canonical docs + target allow-list; global cleanup diparkir.
4. Metrik durasi dari share session tidak membedakan waktu idle. Mitigasi: ukur active elapsed/tool count/token/turn pada paired run baru; baseline lama hanya referensi.
