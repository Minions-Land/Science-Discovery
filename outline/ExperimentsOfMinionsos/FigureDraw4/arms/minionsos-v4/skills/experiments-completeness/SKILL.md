---
slug: experiments-completeness
summary: Experiments must include main comparison + ablation + hyperparameter sensitivity + case study + per-figure/table analysis (analyze WHY, not merely report numbers).
layer: logical
tools:
version: 2
status: active
supersedes:
references: end-to-end-paper-workflow
provenance: R7-evolved
---

# Skill — Experiments Completeness

A complete Experiments section answers three questions in sequence: what is the setup, does the method work, and why does it work. Each question maps to required subsections, and every figure or table must carry analytical prose that addresses causation, not merely reports numbers.

## When to invoke

- Drafting or reviewing the Experiments section.
- Checking whether ablation / hyperparameter / case study components are missing.

## Section structure

The first subsection is always Experimental Setup: datasets, baselines, metrics, and implementation details. This grounds everything that follows.

After setup, the section proceeds through four validation dimensions:

1. **Main experiment** — compare against both the most established classic baselines and the latest state-of-the-art. Benchmarking only against weak baselines undermines credibility.

2. **Ablation study** — provide ablation for every module. When combining multiple modules, demonstrate that the combination is optimal. Critically, report cases where adding a module degrades performance — selective reporting is a reviewer red flag.

3. **Hyperparameter sensitivity** — conduct sensitivity analysis on the 2–3 most critical hyperparameters.

4. **Case study** — include 1–3 representative cases with visualization, explaining WHY our predictions are superior in concrete terms.

## Analysis quality

Every figure and table must be accompanied by analytical prose. The standard is causal explanation, not numerical reporting.

- Prohibit bare statements such as "Table 1 shows our method achieves 94.7%".
- Analyze WHY baselines perform as they do and WHY our method is superior — distinguish design-driven reasons from data-driven reasons.
- Reference both the most established classic baseline and the latest SOTA in the analysis.
- If a baseline outperforms in some dimension, honestly acknowledge the trade-off and explain it.
- Analysis paragraphs are continuous prose; do not add independent headings such as `\paragraph{Table 2 Analysis}`.

## Pitfalls

- Only main experiment without ablation.
- Ablation only showing "removing module X degrades performance" without showing cases where adding a module also degrades.
- Figure/table followed by only "Table 1 shows our method achieves 94.7%".
- Stating "outperforms by X points" without explaining why.
- Avoiding acknowledgment of baseline strengths (reviewers can read the numbers).
- Adding independent headings for each table's analysis (appears fragmented).
