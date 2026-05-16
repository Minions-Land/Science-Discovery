---
name: abstract-discipline
description: 撰写或润色论文 Abstract 与 Conclusion 时，确保单段、无引用、无具体数字、无数据集名。CNS 严格执行；会议论文推荐执行。
triggers:
  - "写 abstract"
  - "polish abstract"
  - "润色摘要"
  - draft_section in [abstract, conclusion]
outputs: 符合 CNS/conference 规范的单段 Abstract 或 Conclusion
scope:
  section: [abstract, conclusion]
  paper_type: [CNS, conference]
---

# Abstract / Conclusion Discipline

论文 Abstract 与 Conclusion 必须满足以下硬约束：

| 规则 | 要求 |
|---|---|
| R1 单段落 | 只能有 1 段（150–250 词） |
| R2 无引用 | 不可含 `\cite{}` / `\citep{}` / `\citet{}` |
| R3 无具体数字 | TM-score 0.71 → near-experimental accuracy |
| R4 无数据集名 | CASP15 → established benchmarks |

保留五段式逻辑（what / why hard / how / evidence / strongest result），但全部用定性语言。

详细规则见 `rules/`。

## Fitness (R7 Stage 1, n=31)

| 指标 | 值 |
|---|---|
| Skill 胜 | 11 |
| 平局 | 9 |
| Baseline 胜 | 11 |
| **净分** | **+0** |

**进化算法推荐**：
- 保留（validated）：R4, R2
- 停用/修改（anti-validated）：R3, R1, _general
