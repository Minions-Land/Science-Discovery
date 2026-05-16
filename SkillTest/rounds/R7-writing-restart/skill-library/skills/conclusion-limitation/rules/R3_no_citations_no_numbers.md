---
id: R3
name: no_citations_no_numbers
trigger:
  draft_section: [conclusion]
  contains_pattern: '(\\cite|\\d+\.\d+|\d+%|\d+-fold)'
---

**规则**：Conclusion 无引用、无具体数字。

**触发**：检测到 cite 或精确数值。

**修复**：同 abstract-discipline 的 R2/R3。Conclusion 用定性语言。
