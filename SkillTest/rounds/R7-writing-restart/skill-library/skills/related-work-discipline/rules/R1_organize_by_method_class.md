---
id: R1
name: organize_by_method_class
trigger:
  draft_section: [related_work]
  contains_pattern: '(firstly|secondly|thirdly|\[\d+\] proposed|\[\d+\] introduced)'
---

**规则**：按方法类组织，不要逐篇综述。

**触发**：检测到逐篇列举模式（"[1] proposed…, [2] introduced…"）。

**修复**：重组为每段一个方法类：
- ❌ "[1] proposed X. [2] extended X to Y. [3] applied Z."
- ✅ "Diffusion-based generative models (RFdiffusion [1], FrameDiff [2]) learn a prior over backbone space…"

**原则**：Related Work 是一篇 synthesized essay，不是 annotated bibliography。
