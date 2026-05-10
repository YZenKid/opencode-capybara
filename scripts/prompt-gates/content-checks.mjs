import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { hasHeadings } from "../evals/lib.mjs";

export function createReader(root, state) {
  return function read(file) {
    const absolute = resolve(root, file);
    if (!existsSync(absolute)) {
      state.failures += 1;
      console.error(`✗ ${file}: file missing`);
      return null;
    }
    return readFileSync(absolute, "utf8");
  };
}

export function runContentChecks({ checks, read, root, state }) {
  for (const check of checks) {
    if (check.mustBeMissing) {
      const absolute = resolve(root, check.file);
      if (existsSync(absolute)) {
        state.failures += 1;
        console.error(`✗ ${check.file} (${check.name}) should be removed`);
      } else {
        console.log(`✓ ${check.file} (${check.name})`);
      }
      continue;
    }

    const content = read(check.file);
    if (content === null) continue;
    const mustInclude = check.mustInclude ?? [];
    const mustNotInclude = check.mustNotInclude ?? [];
    const requiredHeadings = check.requiredHeadings ?? [];

    const missing = mustInclude.filter((needle) => !content.includes(needle));
    const missingHeadings = requiredHeadings.length > 0 ? hasHeadings(content, requiredHeadings).map((item) => `heading:${item}`) : [];
    const forbiddenHits = mustNotInclude.filter((needle) => content.includes(needle));

    if (missing.length > 0 || missingHeadings.length > 0 || forbiddenHits.length > 0) {
      state.failures += 1;
      console.error(`✗ ${check.file} (${check.name}) ${missing.length > 0 ? "missing" : "forbidden"}:`);
      for (const item of missing) console.error(`  - missing: ${item}`);
      for (const item of missingHeadings) console.error(`  - missing: ${item}`);
      for (const item of forbiddenHits) console.error(`  - forbidden: ${item}`);
    } else {
      console.log(`✓ ${check.file} (${check.name})`);
    }
  }
}

export function runDuplicateChecks({ duplicates, read, state }) {
  for (const check of duplicates) {
    const content = read(check.file);
    if (content === null) continue;
    const count = content.split(check.text).length - 1;
    if (count > check.max) {
      state.failures += 1;
      console.error(`✗ ${check.file}: duplicate phrase appears ${count} times (max ${check.max})`);
      console.error(`  - ${check.text}`);
    } else {
      console.log(`✓ ${check.file} duplicate guard (${count}/${check.max})`);
    }
  }
}
