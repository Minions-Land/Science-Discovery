---
name: related-work-discipline
description: 撰写 Related Work 时，按方法类组织（非逐篇综述），每段含 model + algorithm + implementation + 与本文的关系。最少 1 整页。
triggers:
  - "写 related work"
  - "draft related work"
  - draft_section == related_work
outputs: 按方法类组织的 Related Work section
scope:
  section: [related_work]
  paper_type: [CNS, conference]
---

# Related Work Discipline

Related Work 是**唯一应该写具体方法细节**的地方。

| 规则 | 要求 |
|---|---|
| R1 按方法类组织 | 每段一个方法类（不是逐篇 mini-summary） |
| R2 每段三要素 | model + algorithm + 实现方式 |
| R3 连接本文 | 每段结尾说明 prior work 为什么不够 + 本文如何不同 |
| R4 最少 1 页 | 会议论文 ≥1 整页（3–4 substantive paragraphs） |
| R5 不用 itemize | 全部散文，不要列表 |

详细规则见 `rules/`。

## Fitness (R7 Stage 1, n=8)

| 指标 | 值 |
|---|---|
| Skill 胜 | 4 |
| 平局 | 2 |
| Baseline 胜 | 2 |
| **净分** | **+2** |

**进化算法推荐**：
- 保留（validated）：R2, R3
- 停用/修改（anti-validated）：R5
