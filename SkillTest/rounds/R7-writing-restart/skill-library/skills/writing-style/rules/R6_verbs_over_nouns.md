---
id: R6
name: verbs_over_nouns
trigger:
  section: [global]
  contains_pattern: '(perform (a|an) \w+tion|make (a|an) \w+tion|conduct (a|an) \w+sis|carry out (a|an))'
---

**规则**：用动词代替名词化。

**触发**：检测到 "perform an analysis" / "make a comparison" 等名词化结构。

**修复**：
- "perform an analysis" → "analyze"
- "make a comparison" → "compare"
- "conduct an evaluation" → "evaluate"
- "carry out an investigation" → "investigate"
- "provide a description" → "describe"

**原则**：动词让句子更短、更有力、更清晰。
