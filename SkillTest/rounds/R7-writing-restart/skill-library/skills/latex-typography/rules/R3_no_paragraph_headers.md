---
id: R3
name: no_paragraph_headers
trigger:
  section: [global]
  contains_pattern: '\\paragraph\{[^}]{1,30}\}'
---

**规则**：不要用 `\paragraph{}` 做短标题。

**触发**：检测到 `\paragraph{Step 1.}` 或 `\paragraph{The reasoning gap.}` 这种模式。

**修复**：
- 如果内容足够长（>3 句），改用 `\subsection{}` 或 `\subsubsection{}`
- 如果只是想加粗开头，用 `\noindent\textbf{Step 1.}` 后面直接跟正文
- 如果内容只有 1 行，说明结构有问题——要么扩展内容，要么删掉这个 header

**原因**：`\paragraph{}` 在大多数模板里渲染成加粗 + 同行文字，看起来很差且不专业。
