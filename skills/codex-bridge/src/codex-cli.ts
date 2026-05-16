import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { mkdtemp, readFile, rm } from "node:fs/promises";

export async function isCodexAvailable(): Promise<boolean> {
  return new Promise((resolve) => {
    const proc = spawn("codex", ["--version"], { stdio: ["ignore", "pipe", "pipe"], timeout: 5000 });
    proc.on("error", () => resolve(false));
    proc.on("close", (code) => resolve(code === 0));
  });
}

export interface CodexExecOptions {
  prompt: string;
  cwd?: string;
  addDirs?: string[];
  sandbox?: "read-only" | "workspace-write" | "danger-full-access";
  model?: string;
  reasoningEffort?: "low" | "medium" | "high" | "xhigh";
  skipGitCheck?: boolean;
  timeout?: number;
  ephemeral?: boolean;
}

export interface CodexExecResult {
  exitCode: number;
  lastMessage: string;
  events: CodexEvent[];
  error?: string;
}

export interface CodexEvent {
  type: string;
  [key: string]: unknown;
}

export async function runCodexAgent(options: CodexExecOptions): Promise<CodexExecResult> {
  const {
    prompt,
    cwd = process.cwd(),
    addDirs = [],
    sandbox = "danger-full-access",
    model = "gpt-5.5",
    reasoningEffort = "xhigh",
    skipGitCheck = false,
    timeout = 600_000,
    ephemeral = true,
  } = options;

  const tempDir = await mkdtemp(join(tmpdir(), "codex-bridge-"));
  const outputFile = join(tempDir, "last-message.txt");

  const args: string[] = ["exec"];

  args.push("-s", sandbox);
  args.push("-C", cwd);
  args.push("-o", outputFile);
  args.push("--json");
  args.push("-c", `model_reasoning_effort="${reasoningEffort}"`);

  if (skipGitCheck) args.push("--skip-git-repo-check");
  if (ephemeral) args.push("--ephemeral");
  if (model) args.push("-m", model);
  for (const dir of addDirs) {
    args.push("--add-dir", dir);
  }

  args.push(prompt);

  console.error(`[codex-bridge] codex exec -m ${model} -s ${sandbox} effort=${reasoningEffort} cwd=${cwd}`);

  return new Promise((resolve) => {
    const proc = spawn("codex", args, {
      stdio: ["ignore", "pipe", "pipe"],
      env: process.env,
      timeout,
    });

    const events: CodexEvent[] = [];
    let stdout = "";
    let stderr = "";

    proc.stdout.on("data", (chunk: Buffer) => {
      const text = chunk.toString();
      stdout += text;
      for (const line of text.split("\n")) {
        if (!line.trim()) continue;
        try {
          const event = JSON.parse(line) as CodexEvent;
          events.push(event);
        } catch {
          // non-JSON line, ignore
        }
      }
    });

    proc.stderr.on("data", (chunk: Buffer) => {
      stderr += chunk.toString();
    });

    proc.on("error", (err) => {
      resolve({
        exitCode: 1,
        lastMessage: "",
        events,
        error: `Failed to spawn codex: ${err.message}`,
      });
      cleanup(tempDir);
    });

    proc.on("close", async (code) => {
      let lastMessage = "";
      try {
        lastMessage = await readFile(outputFile, "utf-8");
      } catch {
        // output file may not exist if codex crashed early
        lastMessage = extractLastMessageFromEvents(events) || stderr.slice(-2000);
      }

      resolve({
        exitCode: code ?? 1,
        lastMessage,
        events,
        error: code !== 0 ? stderr.slice(-1000) : undefined,
      });
      cleanup(tempDir);
    });

    // Hard kill after timeout + grace period
    setTimeout(() => {
      proc.kill("SIGTERM");
      setTimeout(() => proc.kill("SIGKILL"), 5000);
    }, timeout);
  });
}

function extractLastMessageFromEvents(events: CodexEvent[]): string {
  for (let i = events.length - 1; i >= 0; i--) {
    const e = events[i];
    if (e.type === "message" && typeof e.content === "string") return e.content;
    if (e.type === "agent_message" && typeof e.text === "string") return e.text;
  }
  return "";
}

async function cleanup(dir: string): Promise<void> {
  try {
    await rm(dir, { recursive: true, force: true });
  } catch {
    // best effort
  }
}

export function summarizeEvents(events: CodexEvent[]): {
  filesChanged: string[];
  commandsRun: Array<{ command: string; exitCode?: number; output?: string }>;
  messages: string[];
  usage?: { input_tokens: number; output_tokens: number; cached_input_tokens?: number };
} {
  const filesChanged = new Set<string>();
  const commandsRun: Array<{ command: string; exitCode?: number; output?: string }> = [];
  const messages: string[] = [];
  let usage: { input_tokens: number; output_tokens: number; cached_input_tokens?: number } | undefined;

  for (const e of events) {
    // codex exec --json format: item.completed events
    if (e.type === "item.completed") {
      const item = e.item as Record<string, unknown> | undefined;
      if (!item) continue;

      if (item.type === "file_change") {
        const changes = item.changes as Array<{ path?: string; kind?: string }> | undefined;
        if (changes) {
          for (const c of changes) {
            if (c.path) filesChanged.add(c.path);
          }
        }
      }

      if (item.type === "command_execution") {
        commandsRun.push({
          command: (item.command || "") as string,
          exitCode: item.exit_code as number | undefined,
          output: item.aggregated_output as string | undefined,
        });
      }

      if (item.type === "agent_message") {
        if (typeof item.text === "string") messages.push(item.text);
      }
    }

    if (e.type === "turn.completed") {
      const u = e.usage as Record<string, number> | undefined;
      if (u) {
        usage = {
          input_tokens: u.input_tokens || 0,
          output_tokens: u.output_tokens || 0,
          cached_input_tokens: u.cached_input_tokens,
        };
      }
    }
  }

  return { filesChanged: [...filesChanged], commandsRun, messages, usage };
}
