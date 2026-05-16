# codex-bridge

MCP server that gives Claude Code a Codex GPT-5.5 sub-agent with full execution access.

Claude Code handles orchestration and review. Codex GPT-5.5 handles high-intensity execution: complex debugging, cross-file refactoring, test failure fixes, implementation tasks.

## Tool: `codex`

One tool that does everything. Launches `codex exec` as a full-access sub-agent.

```
codex(
  task: "Fix the failing test — the mock is stale after the refactor",
  cwd: "/path/to/project",
  reasoning_effort: "xhigh"   # xhigh | high | medium | low
)
```

Defaults:
- **model**: gpt-5.5
- **sandbox**: danger-full-access (full read/write/execute)
- **reasoning_effort**: xhigh

Codex can read/write files, run shell commands, execute tests, and iterate autonomously.

Returns: files changed, commands run (with output), token usage, final message.

## Install

```bash
cd tools/codex-bridge
npm install
npm run build
```

## Setup

```bash
# Auto-register with Claude Code
npx codex-bridge setup

# Install the /delegate skill
npx codex-bridge install-skill

# Check everything works
npx codex-bridge diagnose
```

Or manually:
```bash
claude mcp add codex-bridge -s local -- node /path/to/codex-bridge/dist/server.js
```

## Share with others

```bash
# From npm (once published)
npm install -g codex-bridge
npx codex-bridge setup
npx codex-bridge install-skill

# From source
git clone https://github.com/DataLab-atom/codex-bridge.git
cd codex-bridge
npm install && npm run build
npx codex-bridge setup
npx codex-bridge install-skill
```

## Prerequisites

- `codex` CLI installed (`npm i -g @openai/codex`)
- OpenAI API key configured (`codex login` or `~/.codex/auth.json`)
- Node 18+
