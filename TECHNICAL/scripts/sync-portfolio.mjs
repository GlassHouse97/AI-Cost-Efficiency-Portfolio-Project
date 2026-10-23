import { resolve, join, extname } from "node:path";
import {
  readFile,
  readdir,
  mkdir,
  writeFile,
  stat,
} from "node:fs/promises";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
const targetArg = process.argv[2];
if (!targetArg)
  throw new Error(
    "Usage: node TECHNICAL/scripts/sync-portfolio.mjs <portfolio-checkout>",
  );
const target = resolve(targetArg);
const pkg = JSON.parse(await readFile(join(target, "package.json"), "utf8"));
if (pkg.name !== "chris-delgado-portfolio")
  throw new Error("Target is not the expected existing portfolio");
const source = fileURLToPath(new URL("../dashboard/", import.meta.url));
const destination = join(target, "public", "ai-cost-efficiency");
await mkdir(destination, { recursive: true });
// Match Git's text normalization so published hashes are portable across OSes.
const textExtensions = new Set([".html", ".css", ".mjs", ".js", ".json", ".svg"]);
async function copyAndHash(dir, prefix = "") {
  const out = {};
  for (const entry of (await readdir(dir)).sort()) {
    const p = join(dir, entry),
      key = prefix + entry;
    if ((await stat(p)).isDirectory()) {
      await mkdir(join(destination, key), { recursive: true });
      Object.assign(out, await copyAndHash(p, key + "/"));
    } else {
      let bytes = await readFile(p);
      if (textExtensions.has(extname(p)))
        bytes = Buffer.from(bytes.toString("utf8").replace(/\r\n?/g, "\n"));
      await writeFile(join(destination, key), bytes);
      out[key] = createHash("sha256").update(bytes).digest("hex");
    }
  }
  return out;
}
const manifest = {
  source_repository:
    "https://github.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project",
  files: await copyAndHash(source),
};
await writeFile(
  join(destination, "source-manifest.json"),
  JSON.stringify(manifest, null, 2) + "\n",
);
console.log(`Copied verified app assets to ${destination}`);
