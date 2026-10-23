import { createDashboardServer } from "./server.mjs";
const portArg = process.argv.indexOf("--port");
const port = Number(portArg === -1 ? 4327 : process.argv[portArg + 1]);
if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error("Invalid port");
createDashboardServer().listen(port, "127.0.0.1", () =>
  console.log(`Local: http://127.0.0.1:${port}/`),
);
