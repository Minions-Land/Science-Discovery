---
id: R4
name: citation_format_consistency
trigger:
  section: [global]
  contains_pattern: '(\\citep|\\citet|\\cite)\{'
---

**规则**：引用格式全文一致。

**要求**：
- ML 会议（NeurIPS/ICLR/ICML/CVPR/ACL）：用 `\citep{}` / `\citet{}`（natbib）
- IEEE 会议/期刊：用 `\cite{}`（numeric）
- **不混用**

**检查**：grep 全文，确认只用了一种 citation 命令族。
