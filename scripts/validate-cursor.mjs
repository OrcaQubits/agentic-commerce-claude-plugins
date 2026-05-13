#!/usr/bin/env node
/**
 * Local mirror of Cursor's CI validator
 * (https://github.com/cursor/plugins/blob/main/scripts/validate-plugins.mjs).
 *
 * Validates every dist/cursor/<plugin>/.cursor-plugin/plugin.json and the
 * root .cursor-plugin/marketplace.json against the official schemas at
 * https://github.com/cursor/plugins/tree/main/schemas .
 *
 * Usage:
 *   node scripts/validate-cursor.mjs
 *
 * Exits 0 on success, 1 on validation failure. Run before tagging a release.
 */

import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, "..");
const CURSOR_DIST = join(REPO_ROOT, "dist", "cursor");

let Ajv, addFormats;
try {
  Ajv = (await import("ajv")).default;
  addFormats = (await import("ajv-formats")).default;
} catch {
  console.error(
    "ERROR: ajv + ajv-formats not installed. Run:\n" +
      "  npm install --no-save ajv ajv-formats"
  );
  process.exit(1);
}

const PLUGIN_SCHEMA_URL =
  "https://raw.githubusercontent.com/cursor/plugins/main/schemas/plugin.schema.json";
const MARKETPLACE_SCHEMA_URL =
  "https://raw.githubusercontent.com/cursor/plugins/main/schemas/marketplace.schema.json";

async function fetchSchema(url) {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch ${url}: ${res.status}`);
  }
  return res.json();
}

console.log("Fetching official Cursor schemas...");
const pluginSchema = await fetchSchema(PLUGIN_SCHEMA_URL);
const marketplaceSchema = await fetchSchema(MARKETPLACE_SCHEMA_URL);

const ajv = new Ajv({ strict: false, allErrors: true });
addFormats(ajv);
const validatePlugin = ajv.compile(pluginSchema);
const validateMarketplace = ajv.compile(marketplaceSchema);

let errors = 0;
let checked = 0;

function check(label, validator, data) {
  checked++;
  const ok = validator(data);
  if (ok) {
    console.log(`  [OK]    ${label}`);
  } else {
    errors++;
    console.log(`  [FAIL]  ${label}`);
    for (const e of validator.errors ?? []) {
      console.log(
        `          ${e.instancePath || "/"}: ${e.message}` +
          (e.params ? ` ${JSON.stringify(e.params)}` : "")
      );
    }
  }
}

console.log("\nValidating root .cursor-plugin/marketplace.json...");
const marketplacePath = join(REPO_ROOT, ".cursor-plugin", "marketplace.json");
const marketplace = JSON.parse(readFileSync(marketplacePath, "utf-8"));
check(".cursor-plugin/marketplace.json", validateMarketplace, marketplace);

console.log("\nValidating each plugin manifest...");
for (const entry of readdirSync(CURSOR_DIST).sort()) {
  const dir = join(CURSOR_DIST, entry);
  if (!statSync(dir).isDirectory()) continue;
  const pluginPath = join(dir, ".cursor-plugin", "plugin.json");
  let plugin;
  try {
    plugin = JSON.parse(readFileSync(pluginPath, "utf-8"));
  } catch {
    console.log(`  [SKIP]  ${entry} (no plugin.json)`);
    continue;
  }
  check(`dist/cursor/${entry}/.cursor-plugin/plugin.json`, validatePlugin, plugin);
}

console.log("\nValidating marketplace source paths exist...");
for (const p of marketplace.plugins) {
  const fullPath = join(REPO_ROOT, p.source);
  const pluginManifest = join(fullPath, ".cursor-plugin", "plugin.json");
  try {
    statSync(pluginManifest);
    console.log(`  [OK]    ${p.name} -> ${p.source}/.cursor-plugin/plugin.json`);
  } catch {
    errors++;
    console.log(`  [FAIL]  ${p.name} -> ${p.source}/.cursor-plugin/plugin.json (missing)`);
  }
}

console.log(`\nChecked: ${checked}    Errors: ${errors}`);
process.exit(errors === 0 ? 0 : 1);
