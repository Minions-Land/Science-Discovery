---
id: R3
name: contribution_itemize
trigger:
  draft_section: [intro]
  task: [draft]
---

**规则**：Introduction 末尾必须有 2–4 条 contribution bullets。

**触发**：撰写 Intro 时。

**格式要求**：
- 用 `\begin{itemize}` 环境
- 每条是 noun-phrase（不是完整句子）
- 2–4 条（不要超过 4 条）
- 放在 Intro 最后一段之后

**正确示例**：
```latex
\begin{itemize}
  \item A hybrid architecture combining diffusion priors with retrieval-augmented decoding.
  \item Empirical validation on CASP15 showing competitive accuracy at 30× lower cost.
\end{itemize}
```

**注意**：这是全文**唯一允许 itemize** 的地方（参见 latex-typography R2）。
