---
name: experiments-completeness
description: 撰写 Experiments section 时，确保主实验 + 消融 + 超参 + Case Study + 每图每表配分析。
triggers:
  - "写实验"
  - "draft experiments"
  - draft_section == experiments
outputs: 完整的 Experiments section（2.5–3 页）
scope:
  section: [experiments]
  paper_type: [CNS, conference]
---

# Experiments Completeness

Experiments 必须包含以下子部分：

| 规则 | 要求 |
|---|---|
| R1 主实验 | vs 最经典 baselines + 最新 SOTA |
| R2 消融实验 | 证明每个模块最优；包含相邻模块增/减；加了变差也要写 |
| R3 超参数实验 | 报告不同超参数下的结果 |
| R4 Case Study | 展示真实案例上为什么我们的预测更好 |
| R5 每图每表配分析 | 不只报数字，要分析 WHY baselines 这样 + WHY we 更好 |
| R6 Setup 在前 | 开头写 datasets / baselines / metrics / implementation details |

详细规则见 `rules/`。

## Fitness (R7 Stage 1, n=5)

| 指标 | 值 |
|---|---|
| Skill 胜 | 3 |
| 平局 | 0 |
| Baseline 胜 | 2 |
| **净分** | **+1** |

**进化算法推荐**：
- 保留（validated）：R2, R3
- 停用/修改（anti-validated）：_general
