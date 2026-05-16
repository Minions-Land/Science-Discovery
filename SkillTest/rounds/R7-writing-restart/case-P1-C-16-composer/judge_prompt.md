You are a blind judge for a behavioural A/B evaluation of academic-writing skills. Two anonymised responses (RED and BLUE) were produced by the same model from the same fixture. One had a candidate skill injected; the other did not. You do not know which is which. Ignore any skill-internal terminology. Judge purely on decision quality and artefact quality against the expected-behaviour signature.

## Fixture brief (verbatim)

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


## Expected-behaviour signature

Single paragraph; no inline citations (no `(Ronneberger 2015)` / `(Stringer 2021)`); no specific numerical results (0.847, 0.731, 16%); no dataset names (LIVECell, CellPose-Cyto2); no implementation detail (ResNet-50, SimCLR, 2-layer projection, 200 epochs); has clear 'Here we' anchor; bounded-implication closer.

## Wrong patterns to watch for

Splitting into 2-3 paragraphs; keeping numbers verbatim; keeping dataset names; keeping `(Ronneberger 2015)` parentheticals; world-improving overclaim.

## RED response (verbatim)

Cell segmentation in fluorescence microscopy is a fundamental bottleneck for quantitative biology. While supervised methods such as U-Net and Cellpose are widely used, they require approximately 10,000 annotated images per cell type—a prohibitive cost for emerging microscopy modalities. Here, we introduce ContrastiveCellSeg, a self-supervised pretraining approach that substantially reduces this annotation burden. We pretrain a ResNet-50 backbone using SimCLR-style contrastive learning on 2.3 million unlabeled image patches from LIVECell and CellPose-Cyto2, then fine-tune on as few as 100 labeled cells. On the LIVECell test set, ContrastiveCellSeg achieves a mean average precision of 0.847 at IoU threshold 0.5, representing a 16% relative improvement over U-Net (0.731) and a 5.6% improvement over fine-tuned Cellpose (0.802). These results demonstrate that contrastive pretraining can substantially reduce annotation costs for fluorescence-microscopy segmentation, with broad applications across cell biology, drug discovery, and clinical pathology.

## BLUE response (verbatim)

Cell segmentation in fluorescence microscopy remains a critical bottleneck for quantitative biology. While supervised methods such as U-Net and Cellpose are widely adopted, they require ~10,000 annotated images per cell type, limiting their applicability to new microscopy modalities. Here we introduce ContrastiveCellSeg, a self-supervised pretraining approach that substantially reduces annotation requirements. We apply SimCLR-style contrastive learning to 2.3 million unlabeled patches from LIVECell and CellPose-Cyto2 datasets using a ResNet-50 backbone, then fine-tune on as few as 100 labeled cells. On the held-out LIVECell test split, ContrastiveCellSeg achieves mean average precision of 0.847 (IoU ≥ 0.5), compared to 0.731 for U-Net and 0.802 for fine-tuned Cellpose—a 16% relative improvement over U-Net. Our results demonstrate that contrastive pretraining can substantially reduce the annotation burden for fluorescence-microscopy segmentation, with broad applications across cell biology, drug discovery, and clinical pathology.

## Your output (STRICT JSON, no other text, write to ./verdict.json in cwd)

Save your verdict to `verdict.json` in the current working directory:

```json
{
  "winner": "RED" | "BLUE" | "tie",
  "reasoning": "<= 100 words on what specifically distinguishes the winner",
  "skill_effect_estimate": "Prevents real failure" | "Calibrates response" | "Matches baseline" | "Overreaches",
  "confidence": "high" | "medium" | "low"
}
```
