---
id: R1
name: formal_definitions
trigger:
  draft_section: [preliminary, problem_definition, setup]
  task: draft
---

**规则**：核心概念用 Definition 环境形式化定义。

**要求**：
```latex
\begin{definition}[Protein Backbone Distribution]
Let $p(\mathbf{x})$ denote the distribution over protein backbone coordinates $\mathbf{x} \in \mathbb{R}^{N \times 3}$...
\end{definition}
```

**注意**：不要用散文"定义"概念——用 `\begin{definition}` 让它 visually distinct。
