---
name: theoretical-justification
description: 撰写理论推导 / Theoretical Analysis section 时，确保 theorem-proof 结构、proof sketch 在正文、完整证明在 appendix。
triggers:
  - "写理论"
  - "draft theory section"
  - "理论推导"
  - draft_section in [theory, theoretical_analysis, analysis]
outputs: 结构化的 Theorem + Proof sketch section
scope:
  section: [theory, theoretical_analysis]
  paper_type: [conference]
---

# Theoretical Justification Discipline

理论 section 的核心是**让读者相信你的方法有理论保障**。

| 规则 | 要求 |
|---|---|
| R1 Theorem 环境 | 核心结论用 `\begin{theorem}` 正式陈述 |
| R2 Proof sketch 在正文 | 正文放 proof sketch（关键步骤 + 直觉），完整证明放 Appendix |
| R3 对比表 | 如果有 prior bounds，做一个 comparison table（our bound vs prior） |
| R4 假设回溯 | 每个 theorem 显式引用 Preliminary 里的 assumption |
| R5 Remark 解读 | 每个 theorem 后跟一个 Remark 解释实际含义（"This implies…"） |

详细规则见 `rules/`。
