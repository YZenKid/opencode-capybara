
    import { appendFileSync, existsSync, mkdirSync, readFileSync, renameSync, rmSync, writeFileSync, readdirSync } from "node:fs";
    import { dirname, resolve } from "node:path";

    export function ensureDir(dir) {
      mkdirSync(dir, { recursive: true });
      return dir;
    }

    export function writeJsonAtomic(file, data) {
      const target = resolve(file);
      ensureDir(dirname(target));
      const temp = `${target}.tmp-${process.pid}`;
      writeFileSync(temp, `${JSON.stringify(data, null, 2)}
`, "utf8");
      renameSync(temp, target);
      return data;
    }

    export function readJson(file, fallback = null) {
      if (!existsSync(file)) return fallback;
      return JSON.parse(readFileSync(file, "utf8"));
    }

    export function removeFile(file) {
      rmSync(file, { force: true });
    }

    export function appendNdjson(file, entry) {
      ensureDir(dirname(resolve(file)));
      appendFileSync(file, `${JSON.stringify(entry)}
`, "utf8");
    }

    export function listJson(dir) {
      if (!existsSync(dir)) return [];
      return readdirSync(dir)
        .filter((file) => file.endsWith('.json'))
        .sort()
        .map((file) => ({ file, data: readJson(resolve(dir, file)) }));
    }
