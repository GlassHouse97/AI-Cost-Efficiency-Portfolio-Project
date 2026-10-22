import { readFile, mkdir, cp } from "node:fs/promises";
import { prepare } from "../dashboard/metrics.mjs";
const data = JSON.parse(await readFile("dashboard/demo-data.json", "utf8"));
const model = prepare(data);
if (model.tasks.length !== 240) throw new Error("Expected 240 clean tasks");
for (const name of ["mru-quick-challenge.zip", "mru-portfolio-project.zip"])
  await readFile(`dashboard/downloads/${name}`);
await mkdir("dist", { recursive: true });
await cp("dashboard", "dist", { recursive: true });
console.log(
  `Built static dashboard: ${model.tasks.length} tasks, ${model.usage.length} prompts. Output: dist/`,
);
