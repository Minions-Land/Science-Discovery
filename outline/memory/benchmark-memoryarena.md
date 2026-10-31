# MemoryArena — 真实 agent 任务中的 memory 贡献

## Benchmark 定义

MemoryArena 不把 memory 当独立模块测，而是把它**嵌入真实智能体任务**，测量 memory 是否对最终决策有真实贡献。

是 4 个 benchmark 中最贴近 MinionsOS 自然评测姿态的——MinionsOS 的设计就是为 long-horizon multi-agent 项目服务，memory 不脱离 project 存在。

## 评测轴

| 轴 | 说明 |
|---|---|
| 任务成功率 (with vs without memory) | 同样任务，关闭 memory 子系统后的退化幅度 |
| 决策质量提升 | 关键决策点上，是否引用了 memory 中的事实 |
| 跨 session 成功率 | 多 session 任务中，memory 是否真的让后续 session 复用前面成果 |
| 预算下的胜出比例 | 在固定 token / wall-clock 预算内完成更多任务 |

## MinionsOS 对接方案

MinionsOS 的自然形态就是在 `project_{port}/` 下跑一个真实自主项目，role 之间通过 EACN 协作。MemoryArena 的"真实任务"可以直接对应到：

- **任务**：一个研究问题（例如 paper 复现、数据探索、ethics 审计）
- **Agent**：MinionsOS 的 role 矩阵（Gru / Noter / Coder / Writer / Ethics / Expert）
- **Memory**：完整 L0/L1/L2/L3 栈

控制变量做**消融**：

| 配置 | L0 | L1 | L2 | L3 | `hot.md` |
|---|---|---|---|---|---|
| 全开（baseline） | ✅ | ✅ | ✅ | ✅ | ✅ |
| 去 Shelf | ✅ | ✅ | ✅ | ☐ | ✅ |
| 去 Book | ✅ | ✅ | ☐ | ☐ | ☐ |
| 仅 Draft | ✅ | ✅ | ☐ | ☐ | ☐ |
| 仅 Reel | ✅ | ☐ | ☐ | ☐ | ☐ |
| 全关 | ☐ | ☐ | ☐ | ☐ | ☐ |

## 对比维度（屏蔽变量）

1. **任务长度**：1 周期 / 1 天 / 1 周（cross-session）
2. **任务类型**：纯文献 / 含代码实验 / 含 Ethics 审计
3. **Role 数**：单 Expert / 多 Expert / 完整 5 角色
4. **Model class**：所有 role 同 class，分别测 Haiku / Sonnet / Opus
5. **预算约束**：token budget / wall-clock budget

## 预期优势

- 这个 benchmark 是 MinionsOS 的"主场"——L0-L3 整套就是为这种 long-horizon、multi-session、multi-agent 场景设计的。
- `hot.md` 的 wake-up 注入对反复唤醒的 role 应有非常稳定的收益。
- Gru 的 `mos_project_bridge` 在 cross-project 任务上提供了其他 baseline 没有的能力。
- 任务成功率是有 ground-truth 的——可以直接对比有/无 memory 的 commit 历史和 artefact 产出（`project_{port}/branches/shared/` 全树）。

## 预期劣势

- "Fair comparison" 困难：MinionsOS 的 role 协议本身就和 memory 深度耦合，"关闭 memory" 会改变 role 行为模式，可能不是干净的消融——需要在跑评前明确"关闭"的精确语义。
- 跑一轮成本高（真实项目周期），样本数会少，统计功效受限；至少需要预先定义最小可接受样本数。
- 任务成功率的判定本身需要人工或额外 judge，引入主观性——可参照 `minions/review/` 的 review packet 机制做半自动判定。

## Evidence

TBD — 跑通后回填。Evidence 类型：

- 完整 `project_{port}/` artefact 包（每配置独立 port）
- 各配置的最终交付物对比（论文草稿 / 实验报告 / Ethics 报告）
- 关键决策点的 EACN 消息（带 `[evidence: ...]` 标签的引用次数 + 引用源分布）
- Token / wall-clock 消耗
- 配置之间的成对胜出表（pairwise win rate）
