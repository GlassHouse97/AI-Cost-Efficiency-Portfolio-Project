import { resolve, join } from "node:path";
import {
  readFile,
  readdir,
  mkdir,
  cp,
  writeFile,
  stat,
} from "node:fs/promises";
import { createHash } from "node:crypto";
const targetArg = process.argv[2];
if (!targetArg)
  throw new Error(
    "Usage: node scripts/sync-portfolio.mjs <portfolio-checkout>",
  );
const target = resolve(targetArg);
const pkg = JSON.parse(await readFile(join(target, "package.json"), "utf8"));
if (pkg.name !== "chris-delgado-portfolio")
  throw new Error("Target is not the expected existing portfolio");
const source = resolve("dashboard");
const destination = join(target, "public", "ai-cost-efficiency");
await mkdir(destination, { recursive: true });
await cp(source, destination, { recursive: true });
async function hashes(dir, prefix = "") {
  const out = {};
  for (const entry of (await readdir(dir)).sort()) {
    const p = join(dir, entry),
      key = prefix + entry;
    if ((await stat(p)).isDirectory())
      Object.assign(out, await hashes(p, key + "/"));
    else
      out[key] = createHash("sha256")
        .update(await readFile(p))
        .digest("hex");
  }
  return out;
}
const manifest = {
  source_repository:
    "https://github.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project",
  files: await hashes(source),
};
await writeFile(
  join(destination, "source-manifest.json"),
  JSON.stringify(manifest, null, 2) + "\n",
);
console.log(`Copied verified app assets to ${destination}`);
