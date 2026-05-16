---
id: R6
name: model_name_font
trigger:
  section: [global]
  contains_pattern: '\\texttt\{[A-Z][a-z]'
---

**规则**：模型名用 `\textsc{}` 或自定义字体，不用 `\texttt{}`。

**触发**：检测到模型名用了 monospace（`\texttt{RetroDiff}`）。

**修复**：改用 small caps（`\textsc{RetroDiff}`）或在宏里定义 nice 字体。

**原因**：`\texttt{}` 是代码字体，用于代码片段和文件名。模型名不是代码——它是一个品牌名，应该用更优雅的字体处理。
