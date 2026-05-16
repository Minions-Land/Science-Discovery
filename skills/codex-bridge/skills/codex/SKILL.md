---
name: codex
description: "Delegate a task to Codex GPT-5.5 (or fall back to Claude subagent). Use when you need a second brain for complex debug, refactor, review, or implementation."
---

# /codex — Delegate to Codex GPT-5.5

Usage: `/codex <task description>`

Example: `/codex Fix the race condition in src/server.ts — tests are flaky under concurrent load`

---

## Your Role

You are a task dispatcher. Compose the delegation to Codex, execute it, and present the results. If Codex is unavailable, fall back to a Claude subagent seamlessly.

---

## Step 1 — Call the `codex` MCP tool

```
codex(
  task: "<clear task description>",
  cwd: "<absolute path to working directory>"
)
```

That's it. Do not pass other parameters unless the user explicitly asks to change them.

### Defaults (do NOT override):
- `model`: gpt-5.5
- `sandbox`: danger-full-access
- `reasoning_effort`: xhigh

### Optional parameters (only when needed):
- `sandbox: "read-only"` — for analysis in non-git directories
- `skip_git_check: true` — when cwd is not a git repo
- `add_dirs: [...]` — extra directories Codex can access
- `timeout_seconds: N` — extend beyond default 600s for large tasks

### Tips for good task prompts:
- State the goal clearly in one sentence
- Include what "done" looks like (e.g., "tests pass", "type-checks clean")
- Mention relevant files if the task is scoped
- Include constraints (don't touch X, must be backwards-compatible, etc.)

---

## Step 2 — Fallback to Claude subagent

If `codex` returns `CODEX_UNAVAILABLE` or `CODEX_ERROR`, fall back immediately without asking the user.

```
Agent(
  description: "<3-5 word summary>",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "<same task prompt, plus: specific files to read, commands to run, what success looks like>",
  mode: "auto"
)
```

---

## Step 3 — Present results

1. Summarize what was done in 2-3 sentences
2. Show files changed and key findings
3. If the task failed, explain why and suggest next steps
