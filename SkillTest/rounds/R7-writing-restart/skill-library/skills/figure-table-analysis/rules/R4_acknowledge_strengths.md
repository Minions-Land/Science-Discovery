---
id: R4
name: acknowledge_strengths
trigger:
  draft_section: [experiments, results]
  task: [draft, polish]
---

**规则**：如果某个 baseline 在某维度更强，诚实承认。

**要求**：不要回避 baseline 的优势。如果 DiffSeg-XL 在 latency 上更好，要承认并解释 trade-off：
> "DiffSeg-XL achieves 4× lower latency due to its single-pass architecture; our method trades this for a 3.4-point mAP gain through iterative refinement."

**原因**：诚实让论文更可信。reviewer 能看到数字，你不承认他们也会指出来。
