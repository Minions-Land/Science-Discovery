---
id: R2
name: no_fabricated_numbers
trigger:
  section: [experiments, results]
  contains_pattern: '(\d+\.\d{2,}|\d+%)'
---

**规则**：不编造实验数字。

**触发**：检测到精确数值。

**要求**：如果实验还没跑，用占位符：
- `[INSERT VALUE]`
- `XX.X%`
- `$\square$`

**绝不**编一个看起来合理的数字。reviewer 会要求 reproduce，编造的数字 = 学术不端。

**检查方式**：每个数字都应该能追溯到一个具体的实验 log / CSV / notebook。
