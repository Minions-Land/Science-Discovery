---
id: R2
name: subsequent_use_short
trigger:
  section: [global]
  contains_pattern: '(Convolutional Neural Network|Generative Adversarial Network|Long Short-Term Memory)'
---

**规则**：定义后只用简写。

**触发**：检测到已定义缩写的全称再次出现。

**修复**：替换为简写。定义过 CNN 之后，不要再写 "Convolutional Neural Network"。

**原因**：重复全称浪费篇幅且显得不专业。
