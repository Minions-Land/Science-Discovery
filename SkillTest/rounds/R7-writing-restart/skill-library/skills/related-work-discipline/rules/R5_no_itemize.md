---
id: R5
name: no_itemize
trigger:
  draft_section: [related_work]
  contains_pattern: '\\begin\{(itemize|enumerate)\}'
---

**规则**：Related Work 全部用散文，不用列表。

**触发**：检测到 `\begin{itemize}` 或 `\begin{enumerate}`。

**修复**：把列表内容改写为散文段落。Related Work 是综述性质的 essay，列表会让它看起来像 bullet-point notes 而不是正式论文。

**例外**：无。
