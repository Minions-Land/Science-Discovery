---
id: R5
name: no_heading
trigger:
  draft_section: [experiments, results]
  contains_pattern: '(\\paragraph\{.*analysis|\\textbf\{.*Analysis)'
---

**规则**：分析段落不加独立标题。

**触发**：检测到 `\paragraph{Table 2 Analysis}` 这种模式。

**修复**：直接写散文段落，紧跟在 table/figure 之后。不需要给每个分析加 heading。

**例外**：如果 Experiments 有多个 subsection（Main Results / Ablation / Case Study），subsection 标题是允许的——但单个 table 的分析不需要自己的 heading。
