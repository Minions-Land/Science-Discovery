---
id: R4
name: no_random_bold
trigger:
  section: [global]
  contains_pattern: '\\textbf\{(the|our|this|we|a |an )'
---

**规则**：不要乱加粗。

**触发**：检测到对普通词汇的加粗（"**the** key insight"、"**our** method"）。

**修复**：删除加粗。只在以下情况使用 `\textbf{}`：
- 首次定义术语（"We define the **retrieval score** as…"）
- 表格中的最佳结果

**注意**：强调用句子结构和位置来实现，不要用字体。
