---
id: R4
name: honest_limitation
trigger:
  draft_section: [conclusion, limitation]
  task: draft
---

**规则**：必须写 Limitation，且要诚实。

**要求**：
- 至少 2–3 个具体 limitation
- 不要用 "future work" 掩盖已知缺陷
- 不要写空泛的 limitation（"our method may not generalize to all domains"）

**正确示例**：
> "Our retrieval index is fixed at training time; adapting to new protein families requires re-indexing, which takes ~2 hours."

**错误示例**：
> "A limitation is that more work is needed to fully explore the potential of our approach."
