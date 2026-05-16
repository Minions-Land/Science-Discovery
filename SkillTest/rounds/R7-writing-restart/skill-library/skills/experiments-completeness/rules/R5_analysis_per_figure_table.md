---
id: R5
name: analysis_per_figure_table
trigger:
  draft_section: [experiments]
  contains_pattern: '(Table|Figure|Fig\.|Tab\.)\s*\\?(ref|~)'
---

**规则**：每图每表必须配分析。

**触发**：引用了 Table/Figure。

**要求**：不只报数字。每个图/表后面必须有分析段落，回答：
1. 经典 baseline 和 SOTA 表现如何？
2. **为什么**它们表现如此？（设计原因 / 数据原因 / 任务特性）
3. **为什么**我们更好？（哪个设计选择带来了提升）

**参见**：`figure-table-analysis` skill 有更详细的指导。
