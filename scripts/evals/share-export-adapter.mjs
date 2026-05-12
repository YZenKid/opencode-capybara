function decodeLooseEscapes(text) {
  return String(text ?? "")
    .replace(/\\n/g, "\n")
    .replace(/\\t/g, "\t")
    .replace(/\\r/g, "\r")
    .replace(/\\"/g, '"')
    .replace(/\\\\/g, "\\")
    .replace(/\\x([0-9A-Fa-f]{2})/g, (_, hex) => String.fromCharCode(Number.parseInt(hex, 16)))
    .replace(/\\u([0-9A-Fa-f]{4})/g, (_, hex) => String.fromCharCode(Number.parseInt(hex, 16)));
}

function isTranscriptLikeText(text) {
  const lower = text.toLowerCase();
  return [
    "orchestrator",
    "artifact-planner",
    "planner",
    "explorer",
    "fixer",
    "quality-gate",
    "delegate",
    "discover",
    "implement",
    "review",
    "complete",
    "final summary",
    "read ",
    "edit",
    "patch",
  ].some((needle) => lower.includes(needle));
}

function isStructuredTranscriptCandidate(text) {
  const normalized = String(text ?? "").replace(/\s+/g, " ").trim();
  if (!normalized) return false;

  const lower = normalized.toLowerCase();
  const hasAgentCue = ["orchestrator", "artifact-planner", "planner", "explorer", "fixer", "quality-gate"].some((needle) => lower.includes(needle));
  const hasActionCue = ["delegate", "discover", "implement", "review", "complete", "final summary", "read ", "edit", "patch", "plan"].some((needle) => lower.includes(needle));
  const hasPrefixLikeTranscript = /^[a-z0-9\-]+\s*:/.test(lower);
  const hasSequencedPhrase = /(delegate|discover|implement|review|complete|read|edit|patch|plan).{0,80}(artifact-planner|planner|explorer|fixer|quality-gate|orchestrator)/.test(lower)
    || /(artifact-planner|planner|explorer|fixer|quality-gate|orchestrator).{0,80}(delegate|discover|implement|review|complete|read|edit|patch|plan)/.test(lower);

  return hasAgentCue && hasActionCue && (hasPrefixLikeTranscript || hasSequencedPhrase);
}

function collectShareExportCandidates(text) {
  const candidates = [];
  const decoded = decodeLooseEscapes(text);

  const keyedStringPattern = /(?:content|text|body|message|notes|summary|label|title)\s*:\s*"((?:\\.|[^"\\])+)"/g;
  for (const match of decoded.matchAll(keyedStringPattern)) {
    candidates.push(decodeLooseEscapes(match[1]));
  }

  const quotedKeywordPattern = /"((?:\\.|[^"\\]){1,400})"/g;
  for (const match of decoded.matchAll(quotedKeywordPattern)) {
    const value = decodeLooseEscapes(match[1]);
    if (isStructuredTranscriptCandidate(value)) candidates.push(value);
  }

  return candidates
    .flatMap((candidate) => candidate.split("\n"))
    .map((line) => line.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim())
    .filter(Boolean)
    .filter(isTranscriptLikeText)
    .filter(isStructuredTranscriptCandidate);
}

export function normalizeShareExportFixture(shareExport, normalizeEntry) {
  const raw = typeof shareExport === "string"
    ? shareExport
    : shareExport?.html ?? shareExport?.payload ?? shareExport?.content ?? "";

  const scriptBodies = Array.from(raw.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)).map((match) => match[1]);
  const candidatePool = [raw, ...scriptBodies];
  const candidates = candidatePool.flatMap((entry) => collectShareExportCandidates(entry));
  const orderedEntries = [];
  const seen = new Set();

  for (const candidate of candidates) {
    const fingerprint = candidate.toLowerCase();
    if (seen.has(fingerprint)) continue;
    seen.add(fingerprint);
    orderedEntries.push(candidate);
  }

  return {
    sourceMode: "share-export",
    events: orderedEntries.map((entry, index) => normalizeEntry(entry, index)),
  };
}
