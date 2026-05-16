---
name: conclusion-limitation
description: 撰写 Conclusion 和 Limitation section 时，确保单段 conclusion + 诚实 limitation + 具体 future work。
triggers:
  - "写结论"
  - "draft conclusion"
  - "写 limitation"
  - draft_section in [conclusion, limitation]
outputs: Conclusion（~0.5 页）+ Limitation 段落
scope:
  section: [conclusion, limitation]
  paper_type: [CNS, conference]
---

# Conclusion & Limitation Discipline

| 规则 | 要求 |
|---|---|
| R1 单段 Conclusion | 跟 Abstract 一样，Conclusion 只有 1 段（参见 abstract-discipline） |
| R2 不复制 Intro | 重新表述 contribution，不要 copy-paste |
| R3 无引用无数字 | 同 abstract-discipline 的 R2/R3 |
| R4 诚实 Limitation | 必须写 limitation（reviewer 看重这个）；不要用"future work"掩盖已知缺陷 |
| R5 具体 Future Work | 1–2 个具体方向（不要"exciting new avenues"这种空话） |
| R6 Ethics / Reproducibility | 如果 venue 要求，加 ethics statement 和 reproducibility statement |

详细规则见 `rules/`。
