---
id: R3
name: no_specific_numbers
trigger:
  draft_section: [abstract, conclusion]
  contains_pattern: '\b(\d+\.\d+|\d+%|\d+\s*-?\s*fold|TM-score|F1|mAP|accuracy of \d|\d+M-parameter)'
---

**规则**：Abstract / Conclusion 不可含具体数字。

**触发**：检测到精确数值（小数、百分比、倍数、参数量、metric 名 + 数值）。

**修复**：替换为定性描述：
- `TM-score 0.71 vs 0.73` → `near-experimental accuracy`
- `30-fold reduction` → `order-of-magnitude reduction`
- `94.7% accuracy` → `high accuracy on standard benchmarks`

**边界 case**：「a 12-fold increase」也要抽象（→ `an order-of-magnitude increase`）。
