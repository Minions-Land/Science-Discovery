---
id: R1
name: theorem_environment
trigger:
  draft_section: [theory, theoretical_analysis]
  task: draft
---

**规则**：核心结论用 `\begin{theorem}` 正式陈述。

**要求**：不要把定理写在散文里。用正式环境让它 visually distinct + 可引用（`\label{thm:main}`）。

**格式**：
```latex
\begin{theorem}[Convergence Guarantee]\label{thm:convergence}
Under Assumptions 1--3, Algorithm 1 converges to...
\end{theorem}
```
