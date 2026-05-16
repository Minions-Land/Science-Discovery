---
id: R2
name: modular_subsections
trigger:
  draft_section: [method, approach]
  task: draft
---

**规则**：每个模块一个 subsection。

**要求**：如果方法有多个组件（encoder + decoder + loss），每个组件用 `\subsection{}` 分开。每个 subsection 包含：
- 输入/输出定义
- 核心公式
- 设计动机（1–2 句 why this design choice）

**注意**：不要把所有公式堆在一个大段里。
