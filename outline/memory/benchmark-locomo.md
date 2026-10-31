# LoCoMo — 超长对话记忆评测

## Benchmark 定义

LoCoMo (Long Conversational Memory) 测量 agent 在**超长对话**和**跨会话事实记忆**上的能力，重点考察 agent 是否能召回很久之前的细节。

> 评测细节须以原始 paper 为准；本文件先按用户描述的能力轴搭建对接方案，正式跑评前对照原始定义补全 / 修正。

## 评测轴

| 轴 | 说明 |
|---|---|
| 单 session 内长程召回 | 跨 N 轮对话后召回早期细节 |
| 跨 session 持久召回 | session 1 中的事实，session 5 仍可召回 |
| 细节粒度 | 粗略事实 vs 精确细节（数字、人名、日期） |
| 时序保留 | 多事件出现时顺序是否保留 |

## MinionsOS 对接方案

| LoCoMo 轴 | MinionsOS 落点 | 工具 / 路径 |
|---|---|---|
| 单 session 长程召回 | L0 Reel `transcripts/<task_id>.jsonl` | `mos_reel_window(ref, span)` |
| 跨 session 持久召回 | L1 Draft `draft.json`（事实节点） | `mos_draft_query` |
| 高频引用的事实 | L2 Book `hot.md`（wake-up 注入，~500 词） | `mos_book_hot_get` |
| 罕见但精确事实 | L2 Book `sources/{role}-{slug}.md` | `mos_book_query` |
| 时序保留 | Draft 节点的 timestamp + `reel_ref` | `mos_draft_query` 带 ordering |

### 跑评适配层

- 把 LoCoMo 的 "session" 映射为 MinionsOS 的 role wake-up 周期：每个 session 结束 = Noter 触发一次 commit，Draft 落盘。
- 跨 session 召回前强制调用 `mos_reset_context`（清空当前 transcript），只留持久层，避免假阳性命中。
- 召回链路：`hot.md` (free) → Draft query → Book query → Reel drill-down（按 token 成本递增）。每条召回路径需独立记录命中率。

## 对比维度（屏蔽变量）

1. **持久层使用范围**：仅 L0 / +L1 / +L2 / 全四层
2. **召回入口**：Draft query / `hot.md` 注入 / Book query / Reel drill-down
3. **`hot.md` 大小**：500 词（默认） / 0 / 1000
4. **Model class**：Haiku / Sonnet / Opus
5. **Session 间间隔**：紧接 / 1 项目周期 / 跨 project（需 `mos_project_bridge` 中继）

## 预期优势

- `hot.md` 的 wake-up 注入意味着**高频事实零检索成本**——LoCoMo 中反复被提及的事实应有结构性优势。
- Draft 的节点-边图谱保留了时序和因果关系，比纯 vector retrieval 在时序题上应更稳。
- Reel drill-down 提供 verbatim 兜底——即使 L1/L2 总结丢失细节，原始帧仍可追回（`reel_ref` 链路）。

## 预期劣势

- Draft commit 是周期性的（默认 3 min）；session 内紧密发生的事实可能未及落盘就被问到，会暴露 race window。
- Book ingest 由 Noter 主动触发；如果某事实未被认为值得 ingest，它只在 Reel 里——查询路径多一跳，token 成本上升。
- Reel 默认 role-private，跨 role 的事实必须经 Draft/Book 中转；跨角色超长召回有 token 损耗。

## Evidence

TBD — 首轮跑通后回填：

- 完整 run 命令 + 配置 hash + commit SHA
- 各轴得分（按 LoCoMo 原始 metric）
- 与 baseline 对比的差值
- 失败案例的 trace（含 `reel_ref` 指针）
