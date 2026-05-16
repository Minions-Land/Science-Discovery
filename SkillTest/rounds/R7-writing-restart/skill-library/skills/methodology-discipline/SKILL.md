---
name: methodology-discipline
description: 撰写 Method / Approach section 时，确保符号定义在前、算法伪代码、模块化描述、claim-evidence 对齐。
triggers:
  - "写方法"
  - "draft method"
  - "写 methodology"
  - draft_section in [method, approach]
outputs: 结构清晰的 Method section（1.5–2 页）
scope:
  section: [method, approach]
  paper_type: [CNS, conference]
---

# Methodology Discipline

Method section 是论文技术核心，必须做到：

| 规则 | 要求 |
|---|---|
| R1 符号定义在前 | 开头定义 notation（引用 math_commands.tex） |
| R2 模块化描述 | 每个模块一个 subsection，含输入/输出/核心公式 |
| R3 算法伪代码 | 如有多步流程，用 algorithm2e / algorithmic 环境 |
| R4 Claim-evidence 对齐 | 每个 claim 在 Experiments 有对应验证 |
| R5 不要重复 Intro | Method 不重述动机，直接进技术 |

详细规则见 `rules/`。
