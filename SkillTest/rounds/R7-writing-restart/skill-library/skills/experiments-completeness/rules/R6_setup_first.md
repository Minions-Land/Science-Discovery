---
id: R6
name: setup_first
trigger:
  draft_section: [experiments]
  task: draft
---

**规则**：Experiments 开头写 setup。

**要求**：第一个 subsection 是 "Experimental Setup" 或 "Implementation Details"，包含：
- Datasets（名称 + 规模 + split）
- Baselines（列出所有对比方法）
- Metrics（定义每个 metric）
- Implementation details（框架、硬件、关键超参）

**原因**：reviewer 需要先知道实验条件才能评判结果。
