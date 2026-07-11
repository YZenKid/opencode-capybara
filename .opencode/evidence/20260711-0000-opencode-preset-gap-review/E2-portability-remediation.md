# E2 — Quality-gate Remediation

## Scope

Menutup dua `required_before_PASS` dari `.opencode/evidence/20260711-0000-opencode-preset-gap-review/quality-gate.md`:

1. Portabilitas lima suite test yang masih memakai `/var/home/ujang`.
2. Bundle evidence minimal untuk plan aktif `ui-ux-open-design-upgrade` agar `check:evidence` dapat memvalidasi plan artifact yang dipilih checker.

## Confirmed runtime results

| Command | Result |
| --- | --- |
| `npm run test:memory-reuse` | exit 0 |
| `npm run test:session-trace-strict` | exit 0 |
| `npm run test:mcp-memory-store` | exit 0 |
| `npm run test:runtime-memory-finalize` | exit 0 |
| `npm run test:runtime-memory-reuse-loader` | exit 0 |
| `npm run check:evidence` | exit 0 |
| `npm run check:release` | exit 0 |

## Changes

- Five test suites use platform temporary-root APIs, preserving test behavior and removing host-specific `/var/home/ujang` dependence.
- `.opencode/evidence/ui-ux-open-design-upgrade/{discovery.md,verification.md,index.json}` added as mechanical evidence-contract bundle. Bundle status is `bundling_only`; no historic UI/UX slice claim was revalidated.

## Residual risks

- `npm run doctor` exits 0 but continues to report model-sync and OpenChamber home-directory warnings. They remain non-blocking operational follow-ups.
- No `.env`, credential, provider configuration, lockfile, node_modules, or external config changed.
