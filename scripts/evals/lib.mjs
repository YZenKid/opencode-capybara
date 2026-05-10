import { existsSync, readFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";

export function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8"));
}

export function readTextOrNull(file) {
  return existsSync(file) ? readFileSync(file, "utf8") : null;
}

export function extractHeadings(markdown) {
  return markdown
    .split("\n")
    .map((line, index) => ({ line, number: index + 1 }))
    .filter(({ line }) => /^#{1,6}\s+/.test(line))
    .map(({ line, number }) => {
      const [, hashes, text] = line.match(/^(#{1,6})\s+(.*)$/) ?? [];
      return {
        level: hashes.length,
        text: text.trim(),
        line: number,
      };
    });
}

export function hasHeadings(markdown, requiredHeadings) {
  const headings = extractHeadings(markdown).map((heading) => heading.text);
  return requiredHeadings.filter((heading) => !headings.includes(heading));
}

export function parseFrontmatter(markdown) {
  if (!markdown.startsWith("---\n")) return null;
  const end = markdown.indexOf("\n---\n", 4);
  if (end === -1) return null;
  const body = markdown.slice(4, end).split("\n");
  const result = {};
  for (const line of body) {
    const match = line.match(/^([A-Za-z0-9_\-]+):\s*(.*)$/);
    if (!match) continue;
    result[match[1]] = match[2];
  }
  return result;
}

export function missingKeys(obj, requiredKeys) {
  return requiredKeys.filter((key) => !(key in obj));
}

export function evaluateTextRules(content, rule) {
  const missing = (rule.mustInclude ?? []).filter((needle) => !content.includes(needle));
  const forbidden = (rule.mustNotInclude ?? []).filter((needle) => content.includes(needle));
  return { missing, forbidden };
}

export function loadFixtures(fixturesDir) {
  return readdirSync(fixturesDir)
    .filter((file) => file.endsWith(".json"))
    .sort()
    .map((file) => ({ file, fixture: readJson(resolve(fixturesDir, file)) }));
}

export function evaluateTaskFixture(root, fixture) {
  const checks = [];
  let failed = false;

  for (const artifact of fixture.artifacts ?? []) {
    const target = resolve(root, artifact.file);
    const content = readTextOrNull(target);

    if (content === null) {
      failed = true;
      checks.push({
        type: artifact.type ?? "artifact",
        file: artifact.file,
        status: "FAIL",
        reason_code: artifact.reasonCode ?? "missing-artifact",
      });
      continue;
    }

    let missing = [];
    let forbidden = [];

    if (artifact.requiredHeadings) {
      missing = [...missing, ...hasHeadings(content, artifact.requiredHeadings).map((item) => `heading:${item}`)];
    }

    if (artifact.requiredFrontmatterKeys) {
      const frontmatter = parseFrontmatter(content);
      if (frontmatter === null) {
        missing = [...missing, ...artifact.requiredFrontmatterKeys.map((item) => `frontmatter:${item}`)];
      } else {
        missing = [...missing, ...missingKeys(frontmatter, artifact.requiredFrontmatterKeys).map((item) => `frontmatter:${item}`)];
      }
    }

    if (artifact.requiredJsonKeys) {
      const parsed = JSON.parse(content);
      missing = [...missing, ...missingKeys(parsed, artifact.requiredJsonKeys).map((item) => `json:${item}`)];
    }

    const textRuleResult = evaluateTextRules(content, artifact);
    missing = [...missing, ...textRuleResult.missing];
    forbidden = [...forbidden, ...textRuleResult.forbidden];

    if (artifact.expectedReasonCodes) {
      const parsed = JSON.parse(content);
      const actual = new Set(parsed.reason_codes ?? []);
      const missingReasonCodes = artifact.expectedReasonCodes.filter((item) => !actual.has(item));
      missing = [...missing, ...missingReasonCodes.map((item) => `reason_code:${item}`)];
    }

    if (missing.length > 0 || forbidden.length > 0) {
      failed = true;
      checks.push({
        type: artifact.type ?? "artifact",
        file: artifact.file,
        status: "FAIL",
        reason_code: artifact.reasonCode ?? "task-artifact-mismatch",
        missing,
        forbidden,
      });
    } else {
      checks.push({
        type: artifact.type ?? "artifact",
        file: artifact.file,
        status: "PASS",
      });
    }
  }

  return {
    id: fixture.id,
    description: fixture.description,
    category: fixture.category ?? "behavioral-task",
    status: failed ? "FAIL" : "PASS",
    checks,
  };
}
