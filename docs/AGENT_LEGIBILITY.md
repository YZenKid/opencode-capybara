# Agent Legibility

This repository optimizes for agent readability and safe autonomy.

Agents perform better when:
- entrypoints are short,
- docs are indexed,
- decisions are versioned,
- skills have contracts,
- validation is executable,
- errors include remediation steps,
- evidence is required,
- boundaries are enforced mechanically.

## Repository-local knowledge rule
Jika pengetahuan penting tidak bisa ditemukan di repo saat agent berjalan, pengetahuan tersebut secara praktis tidak tersedia.

## Legibility goals
- `AGENTS.md` menjadi map singkat.
- `docs/` menjadi system of record.
- `.opencode/plans/` menjadi tempat plan durable.
- `scripts/*check*.mjs` menjadi guardrails mekanis.
- Error messages harus memberi langkah remediation yang jelas.

## Improvement order after repeated failures
Jika agent gagal berulang, perbaiki harness dalam urutan ini:
1. clarify docs,
2. tighten skill contract,
3. add prompt regression,
4. add mechanical check,
5. improve tool wrapper,
6. update quality score.
