---
name: figure-table-analysis
description: 撰写图表分析段落时，确保不只报数字，而是分析 WHY（设计原因 vs 数据原因），对比经典和 SOTA 的表现。
triggers:
  - "分析这个表"
  - "写 figure analysis"
  - "per-figure paragraph"
  - task == figure_table_analysis
outputs: 分析性段落（非数字报告）
scope:
  section: [experiments, results]
  paper_type: [CNS, conference]
---

# Figure / Table Analysis Discipline

每个图和表都必须配一段**分析性文字**（不是数字复述）。

| 规则 | 要求 |
|---|---|
| R1 不只报数字 | 禁止"Table 1 shows our method achieves 94.7%"这种纯报数 |
| R2 分析 WHY | 为什么 baselines 表现如此？为什么我们更好？是设计原因还是数据原因？ |
| R3 对比经典 + SOTA | 必须提到最经典 baseline 和最新 SOTA 的表现 |
| R4 承认 DiffSeg-XL 强项 | 如果某个 baseline 在某维度更强，要诚实承认并解释 trade-off |
| R5 无 heading | 分析段落不加标题，直接是散文段落 |

详细规则见 `rules/`。

## Fitness (R7 Stage 1, n=10)

| 指标 | 值 |
|---|---|
| Skill 胜 | 1 |
| 平局 | 0 |
| Baseline 胜 | 9 |
| **净分** | **-8** |

**进化算法推荐**：
- 保留（validated）：无
- 停用/修改（anti-validated）：R1, R3, R2, R4, R5
