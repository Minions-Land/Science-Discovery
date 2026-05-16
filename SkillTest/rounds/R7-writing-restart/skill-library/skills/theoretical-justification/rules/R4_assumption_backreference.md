---
id: R4
name: assumption_backreference
trigger:
  draft_section: [theory, theoretical_analysis]
  contains_pattern: '\\begin\{theorem\}'
---

**规则**：每个 theorem 显式引用 Preliminary 里的 assumption。

**要求**：Theorem 陈述里必须写 "Under Assumptions 1–3" 或 "Given Assumption \ref{asm:lipschitz}"。不要让读者猜你用了哪些假设。
