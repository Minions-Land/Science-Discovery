# Annotation — beeswarm_cohort_response

**Source:** SkillTest self-generated (R-future-3 Task 4).

**Archetype:** Beeswarm + median + IQR overlay. Use when each observation
matters AND a summary statistic per cohort is required.

**User grade (R-future-3):** "**左边好看**, 右边太普通了... 我挺喜欢这个
形式的: 箱线图加散点, 感觉还可以."

**Beat the reference** (`bars_ablation_Cancer.png` is rule-correct but
"普通"). Beeswarm with overlaid statistics is more information-dense than
bar-mean+errorbar at the same canvas size.

## Extracted palette

Single-blue family:
- Dot fill: `#406ac0` mid blue at alpha=0.6
- Dot edge: `#154095` deep blue at linewidth=0.4
- Median line: `#404040` ink (high contrast)
- IQR band: `#c0c0ea` pastel blue at alpha=0.4

## What works

1. Per-observation visibility. The reader sees the actual distribution shape,
   not just summary.
2. Median + IQR overlay supplements the dots without replacing them. Reader
   gets both summary AND full data.
3. Single-blue family (P1) — no hue confusion across cohorts; the cohort
   identity comes from x-axis position, not colour.
4. Median line stroke weight 2.0 (P2 sub-rule applied).
5. IQR band visible but pastel — supplements without dominating.

## When to use

For N=3-7 cohorts where individual observations matter (small / clinical
samples). Avoid for N>8 cohorts (jitter overlap becomes visually noisy).

## Recommended over alternatives

vs box plot only: beeswarm shows distribution SHAPE not just quartiles.
vs bar + errorbar: beeswarm shows actual sample size and outliers.
vs violin: violin smooths data; beeswarm preserves individual observations.
