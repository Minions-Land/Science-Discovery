---
id: R2
name: three_elements_per_paragraph
trigger:
  draft_section: [related_work]
  task: [draft, review]
---

**规则**：每段必须包含 model + algorithm + 实现方式。

**触发**：撰写或审查 Related Work 时。

**检查清单**（每段）：
1. ✅ 这类方法用了什么 **model**？（e.g., diffusion U-Net, transformer, GNN）
2. ✅ 核心 **algorithm** 是什么？（e.g., score matching, contrastive learning, MCMC sampling）
3. ✅ 具体怎么 **实现** 的？（e.g., trained on X dataset, uses Y architecture, indexed by Z）

**注意**：这是 Introduction 不允许写的内容——Related Work 是唯一该写这些的地方。
