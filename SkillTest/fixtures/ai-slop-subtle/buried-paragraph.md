# Fixture: ai-buried-slop

**Type:** writing — paragraph with AI-trace patterns BURIED in mostly-clean prose
**Use in:** R6.C deslop hard probe
**Purpose:** R3.C / R4.C used a saturated-slop fixture (every sentence had a slop
pattern) and showed deslop skills do not bite at Opus / Haiku scale. R6.C tests
the hypothesis "skills might bite if the slop is subtler — interspersed in
otherwise-clean prose where lazy editing leaves it standing." If the deslop
family still doesn't bite here, the skip recommendation is final.

## Source paragraph (deliberately mixed clean + buried slop)

> Recent advances in single-cell RNA-seq have made it possible to characterise
> rare cell populations with unprecedented resolution. Vento-Tormo et al. (2018)
> profiled the maternal-fetal interface and identified a previously uncharacterised
> decidual-NK subset, demonstrating that immune cell heterogeneity in this niche
> is far richer than bulk transcriptomics had suggested. This kind of high-
> resolution mapping has, in turn, paved the way for several therapeutic
> hypotheses now under clinical investigation. Building on these foundations,
> our work characterises a similar subset in the spleen, where conventional
> dendritic cells exhibit a transcriptional signature that may shed light on
> their role during chronic infection. We sequenced 12,400 splenic dendritic
> cells from C57BL/6 mice across three infection timepoints. Differential
> expression analysis revealed 47 genes that were upregulated specifically in
> the late-infection cluster, including markers indicative of metabolic stress.
> These findings underscore the importance of high-resolution profiling for
> understanding immune cell adaptation, and we anticipate that this approach
> will be transformative for related fields.

## Brief for the runner

Polish the paragraph above into clean academic English for a Nature
Immunology Introduction or early Discussion paragraph. Maintain factual
content. Cut anything that doesn't serve a reader's understanding.

## Failure modes the runner should fix (buried in otherwise-clean prose)

The slop is INTERSPERSED, not saturated:

- "with unprecedented resolution" — soft cliche; reads as 1980s-vintage filler
- "immune cell heterogeneity ... is far richer than bulk transcriptomics had
  suggested" — rhetorical inflation
- "paved the way for" — single instance, easy to miss
- "shed light on" — single instance
- "Building on these foundations" — common transition; debatably fine
- "These findings underscore the importance of high-resolution profiling for
  understanding immune cell adaptation" — generic sycophantic close
- "we anticipate that this approach will be transformative for related fields"
  — overclaim closer
- "have made it possible to" — passive throat-clearing

The TECHNICAL content is clean and specific:
- Vento-Tormo et al. 2018 reference
- 12,400 cells, C57BL/6, 3 timepoints
- 47 differentially expressed genes, late-infection cluster
- Markers indicative of metabolic stress

A passing rewrite should:

1. Remove "unprecedented", "paved the way for", "shed light on",
   "underscore the importance", "transformative for related fields".
2. Cut the closing two sentences that don't add factual content.
3. Keep all technical specifics (cell count, strain, timepoints, gene
   counts, named comparisons).
4. Keep ≤30-word sentences.
5. Vary sentence length — at least one short (<15 words) and one longer
   (>25 words) sentence.
