---
id: R5
name: no_proofs_here
trigger:
  draft_section: [preliminary, problem_definition]
  contains_pattern: '\\begin\{proof\}|\\textit\{Proof'
---

**规则**：Preliminary 不放证明。

**触发**：检测到 proof 环境。

**修复**：证明移到 Theoretical Justification section 或 Appendix。Preliminary 只放定义和假设。
