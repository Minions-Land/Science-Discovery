# Memory 模块 — Benchmark 评测计划

## 模块定位

MinionsOS 的 Memory 子系统采用 L0/L1/L2/L3 四层 + L4 愿景层的设计：

| Layer | 名称 | 位置 | 所有者 | 用途 |
|---|---|---|---|---|
| L0 | Reel | `branches/<role>/reel/<session_id>/` | 自动 hook 捕获 | 原始 verbatim 会话 transcript；drill-down only |
| L1 | Draft | `branches/shared/draft/draft.json` | Noter 维护 | 过程图谱；in-place 更新；周期性 commit |
| L2 | Book | `branches/shared/book/` | Noter-owned | 编译后的耐久知识；含 `hot.md` (~500 词) |
| L3 | Shelf | `branches/shared/shelf/shelf.json` + `~/.minionsos/shelf.json` | 结构索引 | Per-project + 全局 cross-project |
| L4 | Library (vision) | 待实现 | — | 联邦化全局 EACN3 网络 |

横向通过 `reel_ref` 把 L1/L2/L3 元数据指回 L0 原始帧，做 audit trail。

## 4 个对标 Benchmark

| Benchmark | 主要考察 | 主要触达 MinionsOS 层级 | 评测文件 |
|---|---|---|---|
| **LoCoMo** | 超长对话记忆 + 跨会话事实记忆 | L0 (drill-down) + L1 (Draft cross-session) + L2 (Book 耐久事实) | [benchmark-locomo.md](benchmark-locomo.md) |
| **MemBench** | 事实记忆 vs 反思记忆 + 操作效率 | L1 (事实) + L2 (反思/lesson) + `hot.md` (效率) | [benchmark-membench.md](benchmark-membench.md) |
| **MemoryAgentBench** | 精准检索 + 测试时学习 + 长程理解 + 选择性遗忘 | L3 (检索) + L1/L2 (学习) + L0 (长程) + Draft decay (遗忘) | [benchmark-memoryagentbench.md](benchmark-memoryagentbench.md) |
| **MemoryArena** | 在真实智能体任务中测量 memory 对决策的实际贡献 | 整个系统在真实 project 中的协作产出 | [benchmark-memoryarena.md](benchmark-memoryarena.md) |

## 评测维度（统一控制变量）

每个 benchmark 都按以下维度做交叉测试 / 屏蔽（ablation）：

1. **Model class**：Haiku / Sonnet / Opus（验证 memory 系统跨模型尺度的稳定性）
2. **任务跨度**：单 session / 多 session / 跨 project
3. **写入路径**：仅 L0 自动捕获 / 上至 L1 / 上至 L2 / 全四层
4. **检索方式**：Draft query / Book query / Shelf query / `hot.md` 直接注入
5. **Token 消耗**：injection 长度、命中缓存比、单步对话开销
6. **延迟**：写入延迟、查询延迟、Draft commit 延迟、Book ingest 延迟

## 对标基线（baselines）

| Baseline | 描述 |
|---|---|
| Raw context window | 完全不用持久 memory，只靠当前 transcript |
| Naive log | 纯 append-only flat JSONL，无结构、无 decay、无 hot cache |
| LangChain / LlamaIndex memory | 通用 vector store + summarizer 范式 |
| MemGPT-style | 分层 working/archival memory + tool-call 主动调取 |
| Letta / Mem0 | 托管的 long-term memory 服务 |

## 记录约定

每个 benchmark 文件都遵循以下结构：

1. **Benchmark 定义**（来源、原始 paper 描述）
2. **评测轴**（这个 benchmark 测什么）
3. **MinionsOS 对接方案**（每个轴落到哪个层、哪个工具）
4. **对比维度（屏蔽变量）**
5. **预期优势**
6. **预期劣势**
7. **Evidence** — TBD，首轮跑通后回填，严格只放真实运行得到的数字、artefact 路径、原始 log 引用

跨 benchmark 共享的脚本/数据/adapter 工作待并入 `shared-setup.md`（暂未建）。

## 当前状态

| Benchmark | 文档化 | 接入脚本 | 首轮跑通 | 完整 evidence |
|---|---|---|---|---|
| LoCoMo            | ✅ | ☐ | ☐ | ☐ |
| MemBench          | ✅ | ☐ | ☐ | ☐ |
| MemoryAgentBench  | ✅ | ☐ | ☐ | ☐ |
| MemoryArena       | ✅ | ☐ | ☐ | ☐ |

## 下一步

1. 取四份原始 paper / repo，核对每个 benchmark 文件中"评测轴"和原始 metric 的对应关系，把差异写进各自的 *跑评适配层* 段。
2. 起 `shared-setup.md`，统一 dataset 下载位置、adapter 接口、控制变量的实现方式。
3. 选第一个 benchmark（建议 **LoCoMo**，因为它最直接对应 L0/L1 已有能力，adapter 改动最小）跑通最小闭环，再扩到其他三个。
