---
id: R9
name: specific_nouns
trigger:
  section: [global]
  contains_pattern: '\b(this result|this approach|this method|this technique|this finding|this observation)\b'
---

**规则**：用具体名词替代模糊指代。

**触发**：检测到 "this result" / "this approach" 等模糊指代。

**修复**：
- "this result" → "the 30× speedup" / "the convergence guarantee"
- "this approach" → "retrieval-augmented decoding" / "our hybrid architecture"
- "this method" → "RetroDiff" / "the diffusion prior"

**原因**：模糊指代让读者回头找 antecedent。具体名词让每句话 self-contained。
