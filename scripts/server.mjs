import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { resolve, extname, sep } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = fileURLToPath(new URL("../dashboard/", import.meta.url));
const types = {
  ".html": "text/html; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".zip": "application/zip",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
};

export function createDashboardServer() {
  const base = resolve(root);
  return createServer(async (req, res) => {
    res.setHeader("X-Content-Type-Options", "nosniff");
    res.setHeader("Cache-Control", "no-cache");
    if (!["GET", "HEAD"].includes(req.method)) {
      res.writeHead(405, { Allow: "GET, HEAD", "Content-Type": "text/plain" });
      res.end("Method not allowed");
      return;
    }
    try {
      const pathname = decodeURIComponent(new URL(req.url, "http://localhost").pathname);
      if (pathname === "/health") {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(req.method === "HEAD" ? undefined : '{"status":"ok"}\n');
        return;
      }
      let path = resolve(base, "." + pathname);
      if (path !== base && !path.startsWith(base + sep)) throw new Error("Invalid path");
      if ((await stat(path)).isDirectory()) path = resolve(path, "index.html");
      const type = types[extname(path)];
      if (!type) throw new Error("Unsupported asset");
      const bytes = await readFile(path);
      res.writeHead(200, { "Content-Type": type, "Content-Length": bytes.length });
      res.end(req.method === "HEAD" ? undefined : bytes);
    } catch {
      res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      res.end(req.method === "HEAD" ? undefined : "Not found");
    }
  });
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const port = Number(process.env.PORT ?? 8080);
  if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error("Invalid PORT");
  const server = createDashboardServer();
  server.listen(port, "0.0.0.0", () => console.log(`Dashboard listening on port ${port}`));
  process.on("SIGTERM", () => server.close(() => process.exit(0)));
}
