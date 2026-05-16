---
id: R2
name: no_citations
trigger:
  draft_section: [abstract, conclusion]
  contains_pattern: '\\cite[pt]?\{'
---

**规则**：Abstract / Conclusion 不可含 `\cite{}`、`\citep{}`、`\citet{}`。

**触发**：在 Abstract 或 Conclusion 检测到任何引用宏。

**修复**：移除引用宏；如果该处确实需要点出某项前人工作，将其表述为定性散文（"prior diffusion-based methods…"），把具体引用留到 Intro/Related Work。

**例外**：无。
