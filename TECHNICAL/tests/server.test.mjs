import test from "node:test";
import assert from "node:assert/strict";
import { once } from "node:events";
import { readFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { createDashboardServer } from "../scripts/server.mjs";

test("production server serves the app and exact learner downloads without exposing repository files", async (t) => {
  const server = createDashboardServer();
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  t.after(() => new Promise(resolve => server.close(resolve)));
  const base = `http://127.0.0.1:${server.address().port}`;
  const health = await fetch(`${base}/health`);
  assert.deepEqual(await health.json(), { status: "ok" });
  const page = await fetch(base);
  assert.equal(page.status, 200);
  assert.match(page.headers.get("content-type"), /text\/html/);
  assert.match(await page.text(), /app.mjs/);
  const script = await fetch(`${base}/app.mjs`, { method: "HEAD" });
  assert.equal(script.status, 200);
  assert.match(script.headers.get("content-type"), /javascript/);
  assert.equal((await script.text()).length, 0);
  for (const name of ["mru-quick-challenge.zip", "mru-portfolio-project.zip"]) {
    const response = await fetch(`${base}/downloads/${name}`);
    assert.equal(response.status, 200);
    assert.equal(response.headers.get("content-type"), "application/zip");
    const hash = bytes => createHash("sha256").update(bytes).digest("hex");
    assert.equal(hash(Buffer.from(await response.arrayBuffer())), hash(await readFile(new URL(`../../DATA/downloads/${name}`, import.meta.url))));
  }
  for (const path of ["/README.md", "/.env", "/%2e%2e%2fscripts/server.mjs", "/missing.html", "/%zz"]) {
    assert.equal((await fetch(base + path)).status, 404, path);
  }
  assert.equal((await fetch(base, { method: "POST", body: "ignored" })).status, 405);
});
