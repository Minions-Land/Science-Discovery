# Fixture: P5 — Per-figure / per-table analysis paragraph

## Role
You are a Writer agent in MinionsOS, drafting the Results subsection that
analyses **Table 2** of a manuscript intended for *Cell*.

## Brief

Table 2 (already typeset, do not redraw):

| Method                              | mAP↑    | F1↑    | Latency (ms)↓ |
|-------------------------------------|---------|--------|---------------|
| Baseline-1990 (template matching)   | 0.412   | 0.51   | 18            |
| Baseline-2024-SOTA (DiffSeg-XL)     | 0.847   | 0.87   | 412           |
| Ours (full)                         | 0.881   | 0.89   | 96            |
| Ours, no module Z (ablation)        | 0.853   | 0.86   | 88            |

Author's notes (from the Methods scratchpad):

- Module Z is a "topology-aware refinement head" that operates on the
  segmentation logits.
- DiffSeg-XL uses a 4-step diffusion process at inference; its latency is
  dominated by the diffusion steps.
- The 1990 baseline is included for historical context; nobody expects it to
  be competitive on mAP, but reviewers like to see it.
- Module Z adds ~8 ms of latency.

## Task

Draft the analysis paragraph for Table 2. Return ONLY the paragraph — no
heading, no commentary, no bullet list. The author will paste it directly
under the table.

## Constraints

- ≤ 180 words.
- Must acknowledge DiffSeg-XL's strength on mAP (it is genuinely strong, and
  reviewers know this).
- Must name the design reason for our improvement (not just report numbers).
- Must reference the "no module Z" row to show Z is the load-bearing module.

(End of brief.)
