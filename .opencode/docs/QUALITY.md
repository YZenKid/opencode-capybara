# Quality

## Quality gate statuses
- `PASS`
- `PASS_WITH_RISKS`
- `NEEDS_FIX`
- `BLOCKED`

## Evidence contract
Setiap perubahan material harus berakhir dengan evidence, bukan hanya klaim.

### Final summary template
```md
## Summary
- ...

## Changes
- ...

## Evidence
- Command: `npm run test:prompt-gates`
- Result: PASS
- Additional validation: ...

## Risks / Limitations
- ...

## Next Steps
- ...
```

Jika evidence tidak tersedia, tulis limitation note yang eksplisit.

## Replay bundle minimum
- `task_id`
- `timestamp`
- harness/prompt version metadata
- tool trace summary
- changed files summary
- validation outputs
- final verdict
- reason codes / failure category if not `PASS`

## Standard agent loop
1. `@orchestrator` memahami intent dan memilih route.
2. `@explorer` discovery bila konteks belum jelas.
3. `@artifact-planner` membuat plan untuk task non-trivial.
4. `@fixer` melakukan implementasi bounded.
5. Jalankan validation yang relevan.
6. `@oracle` meninjau architecture risk bila material.
7. Reviewer spesialis kondisional dipanggil bila ada risk trigger.
8. `@quality-gate` melakukan final read-only conformance review.
9. Final summary disusun dari evidence.

## Minimal atomic migration rule
Perubahan yang memindahkan policy antara `AGENTS.md`, `README.md`, `.opencode/docs/`, dan scripts harus mendarat bersama dengan update gate/doctor yang terkait.

## Remediation-oriented error standard
Error messages harus menyebut:
- invariant yang rusak,
- file/area terkait,
- langkah perbaikan spesifik.
