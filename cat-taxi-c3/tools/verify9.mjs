// Structural + reference checks on the built project folder (c3build/check).
import { validateForEditor, detectReferenceIntegrity, parseProjectManifest, validateProjectManifest } from "@genvidtech/c3source";
import fs from "node:fs";
import path from "node:path";
const dir = process.argv[2] ?? "../c3build/check";
const raw = JSON.parse(fs.readFileSync(path.join(dir, "project.c3proj"), "utf8"));
const manifestCheck = validateProjectManifest(raw);
console.log("manifest check:", JSON.stringify(manifestCheck).slice(0, 300));
const manifest = parseProjectManifest(raw);
const ref = detectReferenceIntegrity(dir, manifest);
console.log("reference issues:", ref.issues.length, "ok:", ref.ok);
for (const i of ref.issues.slice(0, 20)) console.log("  ", i.kind, i.severity, i.name, i.file, i.jsonPath, "|", i.message);
let total = 0;
const sheetDir = path.join(dir, "eventSheets");
for (const f of fs.readdirSync(sheetDir).filter(f => f.endsWith(".json"))) {
  const sheet = JSON.parse(fs.readFileSync(path.join(sheetDir, f), "utf8"));
  const issues = validateForEditor(sheet);
  total += issues.length;
  console.log(f, "editor issues:", issues.length);
  for (const i of issues.slice(0, 10)) console.log("  ", i.rule, i.path, i.message);
}
console.log("TOTAL editor issues", total);
