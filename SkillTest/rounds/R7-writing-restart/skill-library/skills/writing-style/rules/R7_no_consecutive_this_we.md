---
id: R7
name: no_consecutive_this_we
trigger:
  section: [global]
  contains_pattern: '(\. This .+\. This |\. We .+\. We )'
---

**规则**：不要连续两句以 "This" 或 "We" 开头。

**触发**：检测到连续句子同一开头。

**修复**：变换句子结构。选项：
- 合并两句
- 用被动语态（偶尔）
- 用具体名词替代 "This"（"This result" → "The 30× speedup"）
- 倒装（"Particularly effective is…"）
