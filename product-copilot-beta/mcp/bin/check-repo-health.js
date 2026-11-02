#!/usr/bin/env node
/**
 * Detect circular self-referencing symlinks in copilot config folders.
 * These appear when something runs `ln -s ../skills skills` inside skills/, etc.
 */
import { readdir, lstat, readlink } from "fs/promises";
import { join, dirname, resolve } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, "../..");
const WATCH_DIRS = ["skills", "policies", "agents", "knowledge"];

async function findSelfSymlinks() {
  const problems = [];

  for (const dirName of WATCH_DIRS) {
    const dirPath = join(REPO_ROOT, dirName);
    let entries;
    try {
      entries = await readdir(dirPath);
    } catch {
      continue;
    }

    for (const entry of entries) {
      const entryPath = join(dirPath, entry);
      let stat;
      try {
        stat = await lstat(entryPath);
      } catch {
        continue;
      }
      if (!stat.isSymbolicLink()) continue;

      const target = await readlink(entryPath);
      if (entry === dirName && (target === `../${dirName}` || target === dirName)) {
        problems.push({ path: entryPath, target, dirName });
      }
    }
  }

  return problems;
}

const problems = await findSelfSymlinks();
if (problems.length === 0) {
  console.log("✓ Repo health check passed (no circular config-folder symlinks).");
  process.exit(0);
}

console.error("✗ Repo health check failed — circular symlinks found:\n");
for (const p of problems) {
  console.error(`  ${p.path} -> ${p.target}`);
}
console.error(
  "\nRemove with: rm skills/skills policies/policies agents/agents" +
    "\nThese are not created by copilot setup — usually an agent ran ln -s from inside the folder."
);
process.exit(1);
