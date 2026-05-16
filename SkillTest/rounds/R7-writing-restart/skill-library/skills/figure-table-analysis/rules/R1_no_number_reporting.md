---
id: R1
name: no_number_reporting
trigger:
  draft_section: [experiments, results]
  contains_pattern: '(shows that|achieves|obtains|reaches)\s+\d+\.\d+'
---

**规则**：禁止纯数字报告。

**触发**：检测到 "Table X shows our method achieves 94.7%" 这种纯报数模式。

**修复**：把数字报告改为分析性陈述：
- ❌ "Table 1 shows our method achieves 94.7% accuracy."
- ✅ "The 3.4-point gap over DiffSeg-XL on mAP reflects our module Z's ability to capture fine-grained boundaries that diffusion-based refinement misses at object edges."
