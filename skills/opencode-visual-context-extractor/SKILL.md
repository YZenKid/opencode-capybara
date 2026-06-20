---
name: opencode-visual-context-extractor
description: Standalone read-only workflow for the visual context extractor helper lane. Use for extracting observable visual context (layout, visible text, components, color palette, UI state, error messages, flow cues) from image, screenshot, mockup, diagram, and other visual inputs, then returning a structured JSON summary (visual_context_extractor.v1) to the caller. Do not use for image generation, design direction, or source editing.
---

# OpenCode Visual Context Extractor Skill

Use this skill when a caller agent needs structured observable context from a visual input. This skill describes *only the visual extraction contract*; it never generates images, never critiques design, and never edits source.

## Reference-first creativity contract
- Prefer repo-local evidence, official docs, upstream source/examples, screenshots/references, and runtime/browser evidence before inventing material details.
- If a reasonable source exists, use it or explicitly record why it was skipped.
- Treat creativity as grounded option generation: for greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with tradeoff rationale.
- Do not present assumptions as facts. Label assumptions explicitly, keep them reversible, and route/ask when they affect architecture, product behavior, UX direction, data, security, or release risk.
- Do not follow the workflow mechanically when stronger repo/reference evidence points elsewhere; adapt and record the reason.
- In outputs/evidence, name the key references used or state that the result is based on repo-local evidence only.

## Role
Read-only helper lane. Receives an image attachment or local path plus an intent, returns a structured JSON summary describing only what is observable in the image.

## Boundary table

| Need | Route |
| --- | --- |
| Extract observable context from an image | `@visual-context-extractor` (this skill) |
| Generate or plan image assets | `@visual-asset-generator` |
| Design direction, visual critique, UX grade | `@designer` |
| Visual parity or "matches the design" signoff | `@designer` + `@quality-gate` |
| Source code edits triggered by the visual | `@fixer` |
| Architecture or tradeoff decision | `@architect` / `@oracle` |
| PDF / DOCX / XLSX / PPT text extraction | `@librarian` (text-first, not visual) |

## Anti-overlap rules
- This skill returns *description only*, never recommendation.
- Never include phrases such as "should be", "improve", "redesign", "grade", "score", "matches the design". Those belong to `@designer` / `@quality-gate`.
- Never claim to read text in blurry, cropped, or off-frame regions. Add an `uncertainty[]` entry instead.
- Never emit image files. Generation belongs to `@visual-asset-generator`.
- Never edit application source. Implementation belongs to `@fixer`.

## When to use
- Caller supplies an image attachment or local path and asks for layout, visible text, components, color palette, UI state, error messages, or flow cues.
- A non-vision agent needs shared evidence from a visual input.
- `@orchestrator`, `@designer`, `@frontend`, `@backend`, `@mobile`, `@fullstack`, `@fixer`, `@oracle`, `@quality-gate`, `@system-analyst`, `@project-manager`, `@architect`, `@visual-asset-generator`, `@skill-improver`, `@council`, `@artifact-planner`, or `@explorer` needs structured visual context (always route via `@orchestrator` unless the caller's `task` permission allows direct delegation).

## When not to use
- No image attachment and no local path provided.
- Host model reports no vision input (`attachment: false` or `modalities.input` lacks `image`).
- Caller wants visual critique, recommendation, design score, or parity verdict.
- Caller wants image generation, image planning, or asset manifest creation.
- Caller wants source code changes in response to the visual.

## Input contract
- `image_path` or image attachment (screenshot, mockup, diagram, photo, wireframe).
- `intent`: what to extract (`"layout and components"`, `"error message and state"`, `"flow cues"`, etc.).
- `focus` (optional): section, region, or component to emphasize.
- `locale` (optional): expected language for visible text.

## Output contract
Return JSON conforming to `visual_context_extractor.v1`:

```json
{
  "schema": "visual_context_extractor.v1",
  "status": "ok|partial|unavailable|error",
  "image_type": "screenshot|mockup|diagram|photo|wireframe|unknown",
  "observable_only": true,
  "summary": "One-sentence summary of what the image shows.",
  "visible_text": ["..."],
  "layout_summary": "Concise description of layout, regions, hierarchy.",
  "components": [
    { "name": "primary-nav", "kind": "navigation", "notes": "horizontal links top-left" }
  ],
  "color_palette": ["#0f172a", "#f8fafc"],
  "ui_state": "loading|empty|error|success|populated|unknown",
  "issues_observed": [
    { "type": "layout|overflow|truncation|missing-asset|color-contrast|other", "region": "top-right", "description": "..." }
  ],
  "uncertainty": [
    { "claim": "...", "reason": "blurry|cropped|outside-frame|inferred", "region": "..." }
  ],
  "pii_detected": [
    { "kind": "email|phone|name|address|api_key|token|password|other", "region": "...", "redacted_to": "***" }
  ],
  "redaction_applied": true,
  "redaction_failed": false,
  "next_actions": [
    "Concrete follow-up for the caller (no design critique, no source edit)."
  ],
  "evidence": [
    "image path or attachment name",
    "model used for vision"
  ]
}
```

Fallback shapes:

```json
{
  "schema": "visual_context_extractor.v1",
  "status": "unavailable",
  "image_type": "unknown",
  "observable_only": true,
  "summary": "Vision input is not available in this session.",
  "fallback_suggestion": "Route image to a vision-capable host model, or supply a text transcript / OCR text instead.",
  "uncertainty": [],
  "pii_detected": [],
  "redaction_applied": false,
  "redaction_failed": false,
  "next_actions": ["..."],
  "evidence": ["..."]
}
```

```json
{
  "schema": "visual_context_extractor.v1",
  "status": "error",
  "image_type": "unknown",
  "observable_only": true,
  "summary": "Image is corrupt, unsupported, or could not be read.",
  "error_detail": "...",
  "uncertainty": [],
  "pii_detected": [],
  "redaction_applied": false,
  "redaction_failed": false,
  "next_actions": ["..."],
  "evidence": ["..."]
}
```

## Redaction policy
- Always mask before return: emails, phone numbers, full names paired with sensitive context, addresses, API keys, tokens, passwords, private URLs.
- Masking format: `***` or partial mask (`j***@example.com`).
- Never echo raw PII/secrets in `evidence[]`, `components[].notes`, `next_actions[]`, or `summary`.
- If the image is too small/blurry to confidently detect PII, list the region in `pii_detected[]` with `kind: "unknown"` and `redacted_to: "***"`, and add a matching `uncertainty[]` entry.
- If redaction cannot be performed safely, set `redaction_failed: true` and halt before returning. Do not emit any field that may carry the unredacted value.

## Workflow
1. Validate the input: image present, format supported, host model vision available.
2. If validation fails, return the appropriate fallback (`unavailable` or `error`) and stop.
3. Set `observable_only: true` and `image_type`.
4. Extract observable facts into `visible_text`, `layout_summary`, `components[]`, `color_palette[]`, `ui_state`, `issues_observed[]`.
5. Apply redaction. Update `visible_text`, redact notes inside `components[].notes`, and populate `pii_detected[]` / `redaction_applied` / `redaction_failed`.
6. Populate `uncertainty[]` for any claim that goes beyond the visible frame, is blurry, cropped, or inferred.
7. Suggest concrete `next_actions[]` for the caller (no design critique, no source edit).
8. Emit JSON only. No prose preamble, no closing prose.

## Validation
- Confirm `schema: "visual_context_extractor.v1"` and `status` present on every response.
- Confirm `observable_only: true` and `redaction_applied: true` when status is `ok` or `partial`.
- Confirm `uncertainty[]` is non-empty whenever any claim could be misread (blurry text, cropped region, inferred color).
- Confirm `pii_detected[]` is non-empty whenever `visible_text` contains masked values; otherwise the entry is `[]`.
- Confirm `status: "unavailable"` is used when no vision input is available; never fabricate understanding.

## Failure / limitation handling
- No image supplied -> `status: "unavailable"` with `fallback_suggestion` asking the caller to attach an image.
- Unsupported format -> `status: "error"` with a clear `error_detail` and `next_actions`.
- Vision disabled on host model -> `status: "unavailable"` with a `fallback_suggestion` naming a vision-capable model or asking for OCR/text.
- Caller requests design recommendation -> return `status: "error"` with `error_detail` describing the refusal and `next_actions[]` pointing to `@designer`.

## Source strategy
- Repo-local evidence: the image itself plus any project docs the caller attached.
- No external web research is required for visual extraction itself.
- If a UI library / design system is referenced, defer to caller-provided docs; this lane does not run extra research.

## Reasoning Tag Output Rule
- Do not write literal `<think>...</think>` or similar fake reasoning tags in user-visible output.
- If reasoning/thinking tool exists, call tool through OpenCode/MCP only.
- If native provider reasoning exists, let provider emit reasoning parts.
- Otherwise keep private reasoning hidden and output only final user-facing content.
