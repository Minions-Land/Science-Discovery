You are a Writer agent in an academic research system.

## Task

# Fixture: S1 — Abstract polish (Video Understanding)

## Role
You are a Writer agent polishing the Abstract of a manuscript for *Nature Machine Intelligence*.

## Brief
Polish the following draft Abstract for Nature Machine Intelligence submission. Apply CNS-style conventions.

## Draft Abstract

Recent advances in video understanding have demonstrated remarkable progress. Our method, TemporalFormer, combines a hierarchical vision transformer with temporal attention mechanisms to achieve state-of-the-art results on multiple benchmarks. Specifically, we train a 420M-parameter model on Kinetics-700 (650K video clips) and Something-Something V2 (220K clips), using a cosine learning rate schedule with AdamW optimizer (lr=3e-4, batch size 256). On Kinetics-700, TemporalFormer achieves 82.3% top-1 accuracy, surpassing the previous best (VideoMAE V2, 81.1%) by 1.2 points. On Something-Something V2, we achieve 73.8% accuracy compared to 72.1% for InternVideo (Zhu et al., 2023). Our temporal attention module reduces FLOPs by 35% compared to full space-time attention while maintaining accuracy. We also demonstrate strong transfer learning performance on ActivityNet (94.2% mAP) and EPIC-Kitchens (52.7% noun accuracy). These results suggest that hierarchical temporal modeling is a promising direction for efficient video understanding that could revolutionize how machines perceive dynamic visual content.

## Expected output
A single paragraph, CNS-style: no citations, no specific numbers, no dataset names, no implementation details. Qualitative descriptors only. "Here we" anchor present.

Produce ONLY the requested output. No commentary, no self-review, no checklist.
