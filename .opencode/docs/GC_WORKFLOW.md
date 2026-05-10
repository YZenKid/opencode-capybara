# Capybara GC Workflow

Run periodically or after repeated failures.

## Checks
- stale docs,
- duplicated instructions,
- conflicting policy,
- overlong prompts,
- missing output contracts,
- broken links,
- weak evidence templates,
- untested prompt gates,
- unsafe lifecycle hooks,
- unclear MCP boundaries,
- read-only/write boundary violations.

## Expected output
- small targeted patch,
- updated quality score,
- new regression case if needed,
- summary of removed/merged stale instructions.
