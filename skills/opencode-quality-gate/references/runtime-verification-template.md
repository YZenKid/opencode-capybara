# Runtime Verification Template

Use for non-trivial app/release/API/PWA tasks. Fill or adapt before final `PASS` claim.

## Required checks

### 1. Route checks
Run:
```bash
python3 ~/.config/opencode/scripts/runtime-verify.py \
  --project-root . \
  --base-url "$BASE_URL" \
  --route / \
  --route /health \
  --route /api/health \
  --output .opencode/evidence/<task-id>/runtime-verify.json
```

Add more `--route` flags for every core user-facing route/API promised in scope.

### 2. Asset checks
Run:
```bash
python3 ~/.config/opencode/scripts/runtime-verify.py \
  --project-root . \
  --asset public/manifest.webmanifest \
  --asset public/apple-touch-icon.png \
  --asset public/icon-192.png \
  --asset public/icon-512.png \
  --output .opencode/evidence/<task-id>/asset-verify.json
```

Add every required icon/audio/image asset. 0-byte files fail.

### 3. Env checks
Run:
```bash
python3 ~/.config/opencode/scripts/runtime-verify.py \
  --env OPENAI_API_KEY \
  --env DATABASE_URL \
  --output .opencode/evidence/<task-id>/env-verify.json
```

If env absent, feature cannot be claimed complete. Mark `not-ready` or block for user config.

## Gate rule
- `PASS`: all required route/asset/env checks green for claimed scope.
- `NEEDS_FIX`: missing routes, missing assets, 0-byte assets, wrong manifest paths, missing env for claimed feature.
- `BLOCKED`: runtime unavailable and no equivalent direct-source proof exists.

## Notes
- Mechanical checks alone (`build`, `lint`, `grep`, test counts) are not sufficient.
- Verification artifact path must be referenced in final evidence.
- Use task-specific routes/assets/env list, not generic defaults.
