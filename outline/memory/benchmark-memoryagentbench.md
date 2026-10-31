# MemoryAgentBench — 4 能力评测（含遗忘）

## Benchmark 定义

MemoryAgentBench 是 4 个对标 benchmark 中**唯一测选择性遗忘**的一个，共考察 4 项能力：

1. **精准检索 (Accurate Retrieval)** — 给定 query 取回正确条目
2. **测试时学习 (Test-Time Learning)** — 在 session 中学到新知识并在后续应用
3. **长程理解 (Long-Range Understanding)** — 跨大量上下文做整合
4. **选择性遗忘 (Selective Forgetting)** — 在指令下丢弃指定信息

## 评测轴 → MinionsOS 落点

| 能力 | MinionsOS 落点 | 工具 |
|---|---|---|
| 精准检索 | L3 Shelf (graphify 结构索引) | `mcp__graphify__*` + `mos_shelf_query` |
| 测试时学习 | L1 Draft append + L2 Book ingest（session 内） | `mos_draft_append`, `mos_book_ingest` |
| 长程理解 | L0 Reel window + L2 Book audit walk | `mos_reel_window`, `mos_book_audit_walk` |
| 选择性遗忘 | Draft decay + Book verified gating | `mos_draft_decay_compute`, `mos_book_promote_verified`（反向操作） |

### 选择性遗忘 — MinionsOS 的"软删除"语义

MinionsOS 目前有两种遗忘机制，**都不是硬删除**：

- **Draft decay** (`mos_draft_decay_compute`)：节点按时间衰减，权重低于阈值的退出热集；旧节点物理仍在文件里。
- **Book verified gating**：Book 的 source page 默认 unverified，只有显式 promote 才进入 `hot.md` 候选；这是"主动遗忘 unverified 信息"的姿态。

但 MinionsOS **没有** "forget this exact fact" 的显式硬删除操作——遗忘通过 decay + verified gating 间接实现。这是和 MemoryAgentBench 直觉的关键差异：

| MemoryAgentBench 假设 | MinionsOS 当前实现 | Gap |
|---|---|---|
| 显式遗忘指令 → 立刻 hidden | Decay 周期 + 重新 ingest 阶段才丢 | benchmark adapter 中可能需要加一个"假删除"工具，并在 Evidence 中标明它是 adapter 行为而非 MinionsOS native |

#### 三种处理策略（需在跑评前选择）

1. 放弃这一项，承认 MinionsOS 没有硬删除语义，在最终 evidence 中单列分项。
2. 开发一个 Noter-only 的 `mos_draft_hard_forget` 工具，使其语义干净对接 benchmark。
3. 用 adapter mock（不改 MinionsOS 本体），在评测脚本里维护一个"被忘记"标签集，事后过滤——但这等于绕过了真实的遗忘机制。

倾向方案 1+2：先单列分项跑（方案 1），同时评估方案 2 的工程成本。

## 对比维度（屏蔽变量）

1. **检索粒度**：Shelf node / Book page / Draft node / Reel frame
2. **遗忘语义**：硬删除 / decay-only / verified gate
3. **长程窗口大小**：Draft 全图 / Book audit walk / Reel session 全展开
4. **Model class**：Haiku / Sonnet / Opus
5. **Shelf 刷新延迟**：每次 append 后立即重跑 graphify / 周期刷新 / 仅在 session 末重跑

## 预期优势

- **精准检索**：Shelf 是 graphify 提取的结构图，对实体-关系类问题应明显优于 vector retrieval。
- **测试时学习**：Draft append 是 in-session 即生效的，下一步查询就能命中（无需重 index）。
- **长程理解**：L0 Reel 给了 ground-truth 兜底；Book audit walk 给了已编译知识——双轨可对照。

## 预期劣势

- **选择性遗忘**：见上面"Gap"段，本项几乎肯定丢分；evidence 中需要单独说明。
- Shelf 是 graphify 离线提取的；session 内新增的节点要等下次 graphify 重跑才进入 Shelf 索引——影响测试时学习的某些子集（结构化 query）。
- Book audit walk 的成本随 Book 规模增长；超长程理解题在大项目下 token 开销可能高于纯 vector retrieval。

## Evidence

TBD — 跑通后回填。每能力单列分项：

- 4 能力分项得分
- 选择性遗忘的实现策略（方案 1/2/3）与对应得分
- Shelf 刷新延迟对测试时学习子题的影响曲线
- 长程理解的 token 开销与命中率
