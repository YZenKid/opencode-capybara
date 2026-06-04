# skills.sh inspirations for opencode-librarian

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### pdf — anthropics/skills
- URL: https://www.skills.sh/anthropics/skills/pdf
- Directory description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple…
- Local adaptation: Use as inspiration for PDF ingestion, extraction, and transformation workflows.

### docx — anthropics/skills
- URL: https://www.skills.sh/anthropics/skills/docx
- Directory description: Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word…
- Local adaptation: Use as inspiration for Word-document reading and editing tasks.

### pptx — anthropics/skills
- URL: https://www.skills.sh/anthropics/skills/pptx
- Directory description: Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations;…
- Local adaptation: Use as inspiration for slide-deck creation, inspection, and transformation tasks.

### xlsx — anthropics/skills
- URL: https://www.skills.sh/anthropics/skills/xlsx
- Directory description: Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing…
- Local adaptation: Use as inspiration for spreadsheet-centric reading, editing, and analysis tasks.

### to-prd — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/to-prd
- Directory description: Turn the current conversation context into a PRD and publish it to the project issue tracker. Use when user wants to create a PRD from the current context.
- Local adaptation: Use as inspiration for turning extracted source material into structured product artifacts.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
