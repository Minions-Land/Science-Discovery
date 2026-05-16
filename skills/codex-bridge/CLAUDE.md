# codex-bridge

让 Claude Code 可以把任务委托给 Codex GPT-5.5 执行的 MCP server。

Codex 作为全权子 agent 启动，能读写文件、跑命令、跑测试、自主迭代。Claude 负责调度和审查结果。

## 前提条件

1. **Node 18+**
2. **Codex CLI** — `npm i -g @openai/codex`
3. **OpenAI API key** — 运行 `codex login` 或确保 `~/.codex/auth.json` 存在

## 安装步骤

```bash
# 1. 进入本目录
cd codex-bridge

# 2. 安装依赖
npm install

# 3. 构建
npm run build

# 4. 注册 MCP 到 Claude Code（二选一）
# 方式 A：自动注册（当前项目）
npx codex-bridge setup

# 方式 B：手动注册（全局）
claude mcp add codex-bridge -s user -- node $(pwd)/dist/server.js

# 5. 安装 /codex skill（可选但推荐）
npx codex-bridge install-skill

# 6. 验证
npx codex-bridge diagnose
```

## 安装后验证

重启 Claude Code session，然后：
- `/mcp` 应该能看到 `codex-bridge` 和 `codex` tool
- 输入 `/codex 你好` 测试是否能调通

## 使用方式

### 方式 1：通过 /codex skill

```
/codex Fix the failing test in tests/test_auth.py
```

### 方式 2：直接调用 MCP tool

Claude 会自动使用 `codex` tool，只需要两个参数：

- `task` — 任务描述
- `cwd` — 工作目录（绝对路径）

### 可选参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `sandbox` | `danger-full-access` | 改为 `read-only` 可在非 git 目录做分析 |
| `skip_git_check` | `false` | 非 git 目录时设为 `true` |
| `reasoning_effort` | `xhigh` | 不要改，除非明确要求降低 |
| `model` | `gpt-5.5` | 不要改，除非明确要求 |
| `timeout_seconds` | `600` | 大任务可以加长 |
| `add_dirs` | `[]` | 额外可访问的目录 |

## Fallback 机制

如果 Codex 不可用（CLI 未安装、API 挂了），MCP 会返回 `CODEX_UNAVAILABLE` 或 `CODEX_ERROR`。
`/codex` skill 会自动 fallback 到 Claude 自己的 subagent（Sonnet）执行，用户无感。

## 文件结构

```
codex-bridge/
├── dist/           # 编译产物（MCP server）
├── src/            # TypeScript 源码
├── scripts/        # CLI（setup / install-skill / diagnose）
├── skills/codex/   # /codex skill 文件
├── package.json
├── tsconfig.json
└── .mcp.json       # MCP 配置模板
```
