# Fixture: P1 — Abstract polishing (Nature Methods style)

## Role
You are a Writer agent in MinionsOS, polishing a manuscript draft for submission
to *Nature Methods*. The user is the corresponding author.

## Brief

The author has handed you the following 4-paragraph DRAFT abstract for a paper
introducing a new self-supervised method called "ContrastiveCellSeg" for instance
segmentation of fluorescence-microscopy cell images.

```
Cell segmentation in fluorescence microscopy is a long-standing bottleneck for
quantitative biology.  We tackle this problem.

Many supervised methods exist.  U-Net (Ronneberger et al., 2015) and Cellpose
(Stringer et al., 2021) are widely used.  However, they require ~10,000
annotated images per cell type, which is impractical for new microscopy
modalities.

In this work, we introduce ContrastiveCellSeg, a self-supervised pretraining
recipe.  We use SimCLR-style contrastive learning on 2.3 M unlabeled patches
from the LIVECell and CellPose-Cyto2 datasets, with a ResNet-50 backbone and a
2-layer projection head, trained for 200 epochs with batch size 1024 on 8x A100
GPUs.  We then fine-tune on as few as 100 labeled cells.  On the held-out
LIVECell test split, ContrastiveCellSeg achieves a mean AP of 0.847 at IoU
threshold 0.5, compared to 0.731 for U-Net and 0.802 for Cellpose-fine-tuned.

This represents a 16% relative improvement over U-Net.  Our method shows that
contrastive pretraining can substantially reduce the annotation cost of
fluorescence-microscopy segmentation, with applications throughout cell
biology, drug discovery, and clinical pathology.
```

## Task

Polish this draft into a *Nature Methods*-ready abstract. Return ONLY the polished
abstract text — no commentary, no bullet list, no "Revision notes". The author will
read your output directly.

## Constraints

- Target word count: ≤ 200 words.
- Must read as continuous Nature-style prose.
- The author will reuse this exact text for the journal submission.

(End of brief — do not add anything before or after the abstract.)
