---
id: R5
name: no_intro_repeat
trigger:
  draft_section: [method, approach]
  contains_pattern: '(motivation|background|why this is important|gap in)'
---

**规则**：Method 不重述动机。

**触发**：检测到 Method section 里出现动机/背景类语言。

**修复**：直接进技术。如果需要 context，一句话引用 Intro（"As discussed in §1, …"），不要重写一段动机。

**原因**：读者已经读过 Intro，重复动机浪费篇幅且显得不自信。
