---
name: opencode-document-specialist
description: Standalone document-processing workflow for OpenCode. Use for PDF, XLS/XLSX/XLSM, CSV/TSV, DOC/DOCX, PPT/PPTX, ODS/ODT, RTF, Office Open XML, document extraction, transformation, validation, form filling, spreadsheet formula work, and document Q&A/summarization.
---

# OpenCode Document Specialist Skill

Use this as the single document-processing workflow. Do not load or depend on legacy `pdf` or `xlsx` skills.

## Scope and routing triggers

Use this workflow when the user provides or asks about:

- PDF files: read, extract text/tables/images, merge, split, rotate, watermark, optimize, repair, render, OCR, create, fill forms, inspect metadata, encrypt/decrypt.
- Spreadsheet files: XLS, XLSX, XLSM, CSV, TSV, ODS; data cleaning, formula creation, formatting, charting, model validation, conversion, recalculation.
- Office documents: DOC, DOCX, PPT, PPTX, Office Open XML packages; unpack/inspect/validate/pack, redline simplification, XML-level repair.
- Text/document formats: ODT, RTF, or mixed document sets for summarization, Q&A, comparison, extraction, or conversion.

Do not use this workflow for normal codebase search, library docs research, UI work, or app implementation unless a document file is the primary input/output.

## Safety rules

- Preserve original documents by default. Never modify the source file in place unless the user explicitly requests it and confirms overwrite/destructive behavior.
- Write generated and intermediate artifacts to copies under `.opencode/document-output/<task-id>/` by default.
- If tied to an existing plan/evidence flow, write document artifacts under `.opencode/evidence/<task-id>/documents/`.
- Ask before destructive edits, overwrites, lossy conversion, encryption/decryption, password removal, metadata stripping, document signing, or transformation of sensitive/personal/confidential documents.
- Do not read `.env`, credentials, keychains, secrets, or unrelated private files unless explicitly allowed.
- If a task requires a password, legal authorization, or data sensitivity decision, ask before proceeding.
- Preserve templates, tracked changes, comments, macros, formulas, formatting, and embedded objects unless the user asks otherwise.

## Resource map

All bundled resources are local to this skill:

- PDF form workflow: `references/pdf/forms.md`
- PDF advanced reference: `references/pdf/reference.md`
- Original PDF quick guide: `references/pdf/original-skill.md`
- Spreadsheet original guide: `references/spreadsheet/original-skill.md`
- PDF helper scripts: `scripts/pdf/`
- Spreadsheet recalculation: `scripts/recalc.py`
- Office Open XML tools and validators: `scripts/office/`

Run bundled scripts from this skill directory when relative imports are needed.

## Default workflow

1. Identify document type, user intent, desired output, and whether the operation is read-only or write/transform.
2. If write/transform, choose a safe output copy path before modifying anything.
3. Inspect structure before changing content:
   - PDF: page count, text availability, forms, encryption, metadata, scanned/image-only status.
   - Spreadsheet: workbook sheets, formulas, external links, styles, merged cells, macros, hidden sheets, dimensions.
   - Office XML: package structure, content types, relationships, comments/redlines/macros, schema validity where relevant.
4. Perform the smallest operation that satisfies the request while preserving source structure.
5. Validate output with format-specific checks.
6. Return concise results with output paths, validation status, and any limitations.

## PDF workflow

### Read/extract

- Prefer `pdftotext` for fast plain text extraction when available.
- Prefer `pdfplumber` for layout-aware text and table extraction.
- Prefer `pypdf` for page count, metadata, merge/split/rotate, and basic manipulation.
- Use OCR only when the PDF is scanned/image-based or text extraction is empty/garbled.
- For large PDFs, process in pages/chunks; avoid loading everything unnecessarily.

### Merge/split/rotate/watermark/create

- Use `pypdf` for common page operations.
- Use `qpdf` for robust command-line page ranges, optimization, linearization, encryption inspection, and repair.
- Use `reportlab` for creating new PDFs. Avoid Unicode subscript/superscript glyphs in built-in fonts; use ReportLab `<sub>` and `<super>` tags in `Paragraph` objects.

### PDF forms

Follow `references/pdf/forms.md` exactly for form-filling tasks.

High-level sequence:

1. Check fillable fields: `python scripts/pdf/check_fillable_fields.py <file.pdf>`.
2. If fillable:
   - Extract fields: `python scripts/pdf/extract_form_field_info.py <input.pdf> <field_info.json>`.
   - Render pages for visual context: `python scripts/pdf/convert_pdf_to_images.py <file.pdf> <output_dir>`.
   - Create `field_values.json`.
   - Fill: `python scripts/pdf/fill_fillable_fields.py <input.pdf> <field_values.json> <output.pdf>`.
3. If non-fillable:
   - Extract structure: `python scripts/pdf/extract_form_structure.py <input.pdf> form_structure.json`.
   - Use structure-based coordinates when possible, visual estimation only as fallback.
   - Validate boxes: `python scripts/pdf/check_bounding_boxes.py fields.json`.
   - Fill annotations: `python scripts/pdf/fill_pdf_form_with_annotations.py <input.pdf> fields.json <output.pdf>`.
4. Verify by rendering output pages to images.

### Encrypted or protected PDFs

- Do not attempt decryption, password removal, or permission bypass without explicit authorization and password/confirmation from the user.
- If authorized, write decrypted/modified copies only.

## Spreadsheet workflow

### Reading and analysis

- Use `pandas` for data analysis, cleaning, reshaping, statistics, and simple exports.
- Use `openpyxl` for XLSX formulas, styles, comments, sheet structure, template-preserving edits, and formatting.
- Use CSV/TSV parsers for plain tabular files, preserving delimiters/encoding when requested.

### Editing and creation

- Preserve existing workbook formatting and conventions when updating a template.
- Use a consistent professional font for new spreadsheets unless the existing template or user says otherwise.
- Use formulas instead of hardcoded Python-calculated values for spreadsheet deliverables when values should remain dynamic.
- For financial models, follow common conventions unless user/template overrides:
  - Blue text: hardcoded user-changeable inputs.
  - Black text: formulas/calculations.
  - Green text: links within the same workbook.
  - Red text: external file links.
  - Yellow fill: important assumptions/inputs requiring attention.
  - Use units in headers, parentheses for negatives, `-` for zeros when appropriate.

### Formula recalculation and validation

If formulas are created or modified, recalculation is mandatory:

```bash
python scripts/recalc.py <excel_file> [timeout_seconds]
```

The script uses LibreOffice and returns JSON with formula/error status. Deliver spreadsheet outputs only after fixing formula errors such as `#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, and `#NAME?`, or after explicitly documenting why a remaining error is intentional.

Important `openpyxl` warning: never save a workbook loaded with `data_only=True` unless the intent is to replace formulas with values.

## Office Open XML workflow

Use `scripts/office/` for Office package inspection and validation:

- Unpack: `python scripts/office/unpack.py <input.docx|pptx|xlsx> <output_dir>`
- Validate: `python scripts/office/validate.py <input_or_unpacked_dir>`
- Pack: `python scripts/office/pack.py <unpacked_dir> <output.docx|pptx|xlsx>`

Guidelines:

- Treat DOCX/PPTX/XLSX as ZIP packages with XML relationships and content types.
- Preserve `[Content_Types].xml`, `_rels`, relationships, media, comments, styles, numbering, theme, custom XML, macros, and embedded objects unless intentionally changed.
- Use validators under `scripts/office/validators/` for DOCX/PPTX-specific checks.
- For redlines/tracked changes, inspect carefully before simplifying; ask before accepting/rejecting changes.

## General document Q&A, summarization, extraction, comparison

- For Q&A/summarization, extract text with page/sheet/slide references when possible.
- For comparisons, identify the granularity first: text-only, visual layout, formulas, styles, metadata, comments/redlines, or package/XML structure.
- For batch jobs, produce a manifest listing input files, outputs, skipped files, failures, and validation status.
- For conversions, disclose lossiness risks and ask before lossy transformations.

## Validation checklist

- Original source files are preserved.
- Outputs are written to a safe copy path.
- PDF outputs open/render and page counts are expected.
- Filled PDF forms are visually verified when placement matters.
- Spreadsheet formulas are recalculated and zero formula errors are verified when formulas are present.
- Office Open XML packages validate or documented validation limitations are reported.
- Sensitive/destructive operations were confirmed before execution.
