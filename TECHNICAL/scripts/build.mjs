import { readFile, mkdir, cp } from "node:fs/promises";
import { prepare } from "../dashboard/metrics.mjs";
const source = new URL("../dashboard/", import.meta.url);
const output = new URL("../dist/", import.meta.url);
const data = JSON.parse(await readFile(new URL("demo-data.json", source), "utf8"));
const model = prepare(data);
if (model.tasks.length !== 240) throw new Error("Expected 240 clean tasks");
for (const name of ["mru-quick-challenge.zip", "mru-portfolio-project.zip"])
  await readFile(new URL(`downloads/${name}`, source));
await mkdir(output, { recursive: true });
await cp(source, output, { recursive: true });
console.log(
  `Built static dashboard: ${model.tasks.length} tasks, ${model.usage.length} prompts. Output: TECHNICAL/dist/`,
);
