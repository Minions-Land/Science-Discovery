# MemBench — 事实 vs 反思 + 操作效率评测

## Benchmark 定义

MemBench 区分两类 memory：

- **事实记忆 (factual)**：客观事实、数据点、约定
- **反思记忆 (reflective)**：经验、教训、"上次这样做失败了" 类型的元学习

并额外测量**记忆操作的效率**——agent 不应随着 memory 增长而越跑越慢。

## 评测轴

| 轴 | 说明 |
|---|---|
| 事实召回准确率 | 给定问题，从 memory 中取出对应事实 |
| 反思应用准确率 | 给定新情境，应用过去的教训 |
| 写入延迟 | 每步写入耗时是否平稳 |
| 查询延迟 | 随 memory 规模增长，查询是否退化 |
| Token 开销 | 每步 memory 操作的 token 消耗，包括缓存命中率 |

## MinionsOS 对接方案

| MemBench 类别 | MinionsOS 落点 | 备注 |
|---|---|---|
| 事实记忆 | L1 Draft 的事实节点 + L2 Book `sources/` | Draft 是"过程图谱"，事实是其中一类节点 |
| 反思记忆 | L2 Book 的 synthesis page + governance signboard | Noter 通过 `mos_book_save_synthesis` 把跨多个 source 的总结固化 |
| 写入效率 | Draft 缓冲到 disk + 周期 commit；Book 走 `mos_book_ingest` | 关键分离："in-memory append" vs "git commit" |
| 查询效率 | `hot.md` 直接注入 + Book query 走 graphify 索引 | `hot.md` 是 O(1)；Book query 走结构索引 |
| 退化测量 | 随项目运行小时数累积 N=10/50/200/1000 个 Draft 节点 | 测量 query 延迟曲线 |

### 跑评适配层

| MemBench 操作 | MinionsOS 工具 |
|---|---|
| 事实写入 | `mos_draft_append (kind=fact)` |
| 反思写入 | `mos_book_save_synthesis` 或 `mos_draft_annotate` |
| 事实查询 | `mos_draft_query` 或 `mos_book_query` |
| 反思查询 | `mos_book_query`（优先 synthesis page） |

## 对比维度（屏蔽变量）

1. **Memory 规模**：N=10 / 100 / 1000 / 10000 个事实
2. **事实 vs 反思比例**：100/0 / 50/50 / 0/100
3. **`hot.md` 命中率**：高频事实 / 长尾事实
4. **Commit 频率**：3 min（默认） / 30 s / 即时
5. **Model class**：Haiku / Sonnet / Opus

## 预期优势

- 事实和反思在 MinionsOS 中是**结构上分开**的：Draft = 过程事实，Book synthesis = 反思——天然契合 MemBench 的二分。
- `hot.md` 把"反复被引用的反思"提前注入，反思应用的延迟应是 O(0)。
- Draft 的 "in-memory append + 周期 commit" 对写入延迟是最优的——单步 append 不涉及 git，git cost 摊到周期 flush。

## 预期劣势

- Noter 决定哪些事实 ingest 到 Book——如果 Noter 未察觉某事实重要，反思类查询会绕远路。
- 真正"很大量"（万级以上事实）时 Draft JSON 的 in-memory 表示和 query 复杂度待验证；可能需要分片或外挂索引。
- 反思的"判定"目前依赖 Noter 主观打分（governance signboard），benchmark 上需要客观转化（例如 ground-truth 标签）。

## Evidence

TBD — 跑通后回填，重点采集：

- 写入延迟随 N 增长的曲线
- 查询延迟随 N 增长的曲线
- 反思应用题命中率分项：`hot.md` / Book query / miss
- 每步 token 消耗 + prompt cache 命中率
