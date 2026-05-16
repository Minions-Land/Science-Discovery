---
id: R3
name: comparison_table
trigger:
  draft_section: [theory, theoretical_analysis]
  contains_pattern: '(prior bound|previous result|existing guarantee|known rate)'
---

**规则**：如果有 prior bounds，做对比表。

**触发**：提到了前人的理论结果。

**格式**：
| Method | Rate | Assumptions | Our improvement |
|---|---|---|---|
| Prior A | $O(1/\sqrt{T})$ | convex + Lipschitz | — |
| **Ours** | $O(1/T)$ | convex + smooth | $\sqrt{T}$× faster |

**原因**：表格让 reviewer 一眼看到你的理论贡献 vs prior art。
