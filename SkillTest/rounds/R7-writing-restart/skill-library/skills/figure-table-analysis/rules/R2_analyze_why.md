---
id: R2
name: analyze_why
trigger:
  draft_section: [experiments, results]
  task: [draft, review]
---

**规则**：分析 WHY，不只报 WHAT。

**要求**：每个图/表的分析段落必须回答：
1. 为什么 baselines 表现如此？（设计缺陷 / 数据不匹配 / 任务特性）
2. 为什么我们更好？（哪个设计选择 / 哪个模块带来了提升）

**正确示例**：
> "DiffSeg-XL's lower mAP on small objects stems from its fixed-resolution diffusion process, which cannot adapt to varying object scales. Our multi-scale module Z addresses this by…"

**错误示例**：
> "Our method outperforms DiffSeg-XL by 3.4 points."（只说了 what，没说 why）
