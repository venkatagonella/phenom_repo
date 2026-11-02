import { executeTool } from "./src/tools/index.ts";

const [, , toolName, jsonInput] = process.argv;
const input = JSON.parse(jsonInput || "{}");
const out = await executeTool({ name: toolName, input } as any);
process.stdout.write(typeof out === "string" ? out : JSON.stringify(out, null, 2));
