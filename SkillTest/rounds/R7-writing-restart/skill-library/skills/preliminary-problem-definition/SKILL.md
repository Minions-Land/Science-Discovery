---
name: preliminary-problem-definition
description: 撰写 Preliminary / Problem Definition / Setup section 时，确保形式化定义清晰、假设显式列出、与 Method 衔接自然。
triggers:
  - "写 preliminary"
  - "写 problem definition"
  - "draft setup"
  - draft_section in [preliminary, problem_definition, setup]
outputs: 形式化的 Preliminary 或 Problem Definition section
scope:
  section: [preliminary, problem_definition, setup]
  paper_type: [conference]
---

# Preliminary / Problem Definition Discipline

这个 section 的职责是**把问题形式化**，让读者在进入 Method 之前知道：

| 规则 | 要求 |
|---|---|
| R1 形式化定义 | 用 Definition 环境定义核心概念 |
| R2 假设显式列出 | 用 Assumption 环境列出所有假设 |
| R3 符号表 | 如果符号多（>10 个），提供符号表或在 Appendix 放 notation table |
| R4 与 Method 衔接 | 最后一段自然过渡到 Method（"Given the above formulation, we now describe…"） |
| R5 不要证明 | 证明放 Theoretical Justification 或 Appendix，这里只放定义和假设 |

详细规则见 `rules/`。
