---
id: R1
name: model_name_macro
trigger:
  section: [global]
  contains_pattern: '(\\textbf\{[A-Z]|\\texttt\{[A-Z]|\\textsc\{[A-Z]).*\\text(bf|tt|sc)\{[A-Z]'
---

**规则**：模型名用 `\newcommand` 定义宏。

**触发**：检测到模型名在文中多次以 `\textbf{}`/`\texttt{}`/`\textsc{}` 出现。

**修复**：在 preamble 定义：
```latex
\newcommand{\methodname}{\textsc{RetroDiff}\xspace}
```
全文用 `\methodname` 调用。好处：
- 改名只改一处
- 字体统一
- 可以做 nice 的字体处理（small caps + 微调 kerning）
