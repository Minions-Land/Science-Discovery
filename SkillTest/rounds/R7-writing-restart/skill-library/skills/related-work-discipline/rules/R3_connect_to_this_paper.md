---
id: R3
name: connect_to_this_paper
trigger:
  draft_section: [related_work]
  task: [draft]
---

**规则**：每段结尾必须连接到本文。

**触发**：撰写 Related Work 时。

**模板**：每段最后 1–2 句说明：
- prior work 为什么不够（"However, these methods require…"）
- 本文如何不同（"In contrast, our approach…" / "We build upon X but differ in…"）

**正确示例**：
> "…achieving state-of-the-art on CASP14. However, these models require full retraining for each new design task. Our approach avoids retraining by combining a fixed diffusion prior with retrieval conditioning."

**错误示例**：
> "…achieving state-of-the-art on CASP14."（段落结束，没有连接本文）
