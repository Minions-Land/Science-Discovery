---
id: R5
name: remark_interpretation
trigger:
  draft_section: [theory, theoretical_analysis]
  contains_pattern: '\\end\{theorem\}'
---

**规则**：每个 theorem 后跟 Remark 解释实际含义。

**要求**：
```latex
\begin{remark}
Theorem \ref{thm:convergence} implies that with $T = O(1/\epsilon^2)$ iterations, we achieve $\epsilon$-accuracy. In practice, this means...
\end{remark}
```

**原因**：纯数学陈述对非理论 reviewer 不友好。Remark 把定理翻译成"这对实践意味着什么"。
