---
id: R2
name: method_class_description
trigger:
  draft_section: [intro]
  task: [draft, polish]
---

**规则**：Introduction 只在「类」层面描述方法。

**触发**：撰写或润色 Intro 时。

**正确示例**：
- "We combine a diffusion-based generative prior with retrieval-augmented decoding."
- "Our approach leverages contrastive pre-training followed by task-specific fine-tuning."

**错误示例**：
- "We train a 350M-parameter U-Net on 450k PDB chains…"（这是 Method 的内容）
- "We use FAISS HNSW indexing with ESM-2 embeddings…"（实现细节）

**原则**：读者读完 Intro 应该知道你用了「什么类型的方法」，但不需要知道「具体怎么实现的」。
