import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

import { isCodexAvailable, runCodexAgent, summarizeEvents } from "./codex-cli.js";

const server = new McpServer({
  name: "codex-bridge",
  version: "1.1.0",
});

const InputSchema = {
  task: z.string()
    .min(1, "Task description is required")
    .describe("Clear task description — what Codex should accomplish"),
  cwd: z.string()
    .min(1, "Working directory is required")
    .describe("Working directory for Codex (absolute path)"),
  add_dirs: z.array(z.string())
    .optional()
    .describe("Additional directories Codex may access beyond cwd"),
  model: z.string()
    .optional()
    .describe("Model override (default: gpt-5.5)"),
  sandbox: z.enum(["read-only", "workspace-write", "danger-full-access"])
    .default("danger-full-access")
    .describe("Sandbox level. Use 'read-only' for analysis in non-git dirs, 'danger-full-access' for full execution"),
  reasoning_effort: z.enum(["low", "medium", "high", "xhigh"])
    .default("xhigh")
    .describe("Reasoning effort level (default: xhigh)"),
  skip_git_check: z.boolean()
    .optional()
    .describe("Skip git repo check — required for non-git directories"),
  timeout_seconds: z.number()
    .int()
    .min(10)
    .max(3600)
    .optional()
    .describe("Timeout in seconds (default: 600, max: 3600)"),
};

const OutputSchema = {
  status: z.enum(["success", "error", "timeout"]),
  exit_code: z.number(),
  files_changed: z.array(z.string()),
  commands_run: z.array(z.object({
    command: z.string(),
    exit_code: z.number().optional(),
  })),
  tokens: z.object({
    input: z.number(),
    output: z.number(),
    cached: z.number().optional(),
  }).optional(),
  message: z.string(),
};

server.registerTool(
  "codex",
  {
    title: "Codex GPT-5.5 Sub-Agent",
    description: `Delegate a task to Codex GPT-5.5 as a full-access sub-agent. Codex can read/write files, run shell commands, and execute autonomously within the specified working directory.

Args:
  - task (string, required): Clear description of what Codex should accomplish
  - cwd (string, required): Absolute path to the working directory
  - add_dirs (string[]): Additional directories Codex may access
  - model (string): Model override (default: gpt-5.5)
  - sandbox ('read-only' | 'workspace-write' | 'danger-full-access'): Permission level (default: danger-full-access)
  - reasoning_effort ('low' | 'medium' | 'high' | 'xhigh'): Reasoning depth (default: xhigh)
  - skip_git_check (boolean): Skip git repo validation for non-git directories
  - timeout_seconds (number): Execution timeout, 10-3600 (default: 600)

Returns:
  Structured result with:
  - status: 'success' | 'error' | 'timeout'
  - exit_code: Codex process exit code
  - files_changed: Array of modified file paths
  - commands_run: Array of {command, exit_code} executed by Codex
  - tokens: {input, output, cached} token usage
  - message: Codex's final summary message

Examples:
  - Fix failing tests: task="Fix the failing test in test_auth.py", cwd="/path/to/project"
  - Code review: task="Review src/server.ts for concurrency bugs", cwd="/path/to/project", sandbox="read-only"
  - Refactor: task="Extract the validation logic into a shared module", cwd="/path/to/project"
  - Non-git analysis: task="Analyze this log file", cwd="/tmp/logs", sandbox="read-only", skip_git_check=true

Error Handling:
  - CODEX_UNAVAILABLE: codex CLI not installed — fall back to Claude subagent (Agent tool, model=sonnet)
  - CODEX_ERROR: execution failed — includes error details and fallback suggestion
  - Timeout: task exceeded timeout_seconds — consider breaking into smaller tasks`,
    inputSchema: InputSchema,
    outputSchema: OutputSchema,
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: false,
      openWorldHint: true,
    },
  },
  async (params) => {
    if (!(await isCodexAvailable())) {
      const output = {
        status: "error" as const,
        exit_code: -1,
        files_changed: [],
        commands_run: [],
        message: "CODEX_UNAVAILABLE: codex CLI not found. Fall back to a Claude subagent (Agent tool with model=sonnet) for this task.",
      };
      return {
        structuredContent: output,
        content: [{ type: "text" as const, text: output.message }],
        isError: true,
      };
    }

    const timeout = Math.min((params.timeout_seconds || 600) * 1000, 3_600_000);

    try {
      const result = await runCodexAgent({
        prompt: params.task,
        cwd: params.cwd,
        addDirs: params.add_dirs,
        sandbox: params.sandbox as "read-only" | "workspace-write" | "danger-full-access",
        model: params.model,
        reasoningEffort: params.reasoning_effort as "low" | "medium" | "high" | "xhigh",
        skipGitCheck: params.skip_git_check,
        timeout,
        ephemeral: true,
      });

      const summary = summarizeEvents(result.events);

      const status = result.exitCode === 0 ? "success" as const : "error" as const;
      const message = result.lastMessage || summary.messages[summary.messages.length - 1] || "(no final message captured)";

      const output = {
        status,
        exit_code: result.exitCode,
        files_changed: summary.filesChanged,
        commands_run: summary.commandsRun.map((c) => ({
          command: c.command,
          exit_code: c.exitCode,
        })),
        ...(summary.usage ? {
          tokens: {
            input: summary.usage.input_tokens,
            output: summary.usage.output_tokens,
            ...(summary.usage.cached_input_tokens ? { cached: summary.usage.cached_input_tokens } : {}),
          },
        } : {}),
        message,
      };

      // Build human-readable text representation
      const parts: string[] = [];
      parts.push(status === "success" ? "[Codex completed successfully]" : `[Codex exited with code ${result.exitCode}]`);
      if (result.error) parts.push(`Error: ${result.error.slice(0, 500)}`);
      parts.push("");

      if (summary.filesChanged.length > 0) {
        parts.push("## Files changed");
        for (const f of summary.filesChanged) parts.push(`- ${f}`);
        parts.push("");
      }

      if (summary.commandsRun.length > 0) {
        parts.push("## Commands executed");
        for (const c of summary.commandsRun) {
          const exit = c.exitCode !== undefined ? ` (exit ${c.exitCode})` : "";
          parts.push(`- \`${c.command}\`${exit}`);
          if (c.output && c.output.trim()) {
            parts.push(`  \`\`\`\n  ${c.output.trim().slice(0, 500)}\n  \`\`\``);
          }
        }
        parts.push("");
      }

      if (summary.usage) {
        const cached = summary.usage.cached_input_tokens ? ` cached=${summary.usage.cached_input_tokens}` : "";
        parts.push(`[tokens: in=${summary.usage.input_tokens}${cached} out=${summary.usage.output_tokens}]`);
        parts.push("");
      }

      parts.push("## Codex final message");
      parts.push(message);

      return {
        structuredContent: output,
        content: [{ type: "text" as const, text: parts.join("\n") }],
      };
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      const output = {
        status: "error" as const,
        exit_code: -1,
        files_changed: [],
        commands_run: [],
        message: `CODEX_ERROR: ${msg}\n\nFall back to a Claude subagent (Agent tool with model=sonnet, mode=auto) for this task.`,
      };
      return {
        structuredContent: output,
        content: [{ type: "text" as const, text: output.message }],
        isError: true,
      };
    }
  },
);

async function main() {
  console.error("[codex-bridge] Starting MCP server v1.1.0...");

  const codexOk = await isCodexAvailable();
  console.error(`[codex-bridge] codex CLI: ${codexOk ? "available" : "NOT FOUND"}`);

  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("[codex-bridge] Connected via stdio");
}

main().catch((err) => {
  console.error("[codex-bridge] Fatal:", err);
  process.exit(1);
});
