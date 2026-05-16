---
id: R2
name: explicit_assumptions
trigger:
  draft_section: [preliminary, problem_definition, setup]
  task: draft
---

**规则**：所有假设用 Assumption 环境显式列出。

**要求**：
```latex
\begin{assumption}[Lipschitz Continuity]
The score function $\nabla_x \log p_t(x)$ is $L$-Lipschitz for all $t \in [0, T]$.
\end{assumption}
```

**原因**：隐式假设是 reviewer 攻击的主要目标。显式列出让 reviewer 无法说"你没说清楚前提"。
