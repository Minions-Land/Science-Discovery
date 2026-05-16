# MetaHarness probes — overlap-port evolve evaluation

## Probe abstract-writing

You are a Writer agent on a Nature paper team. Polish this mouse-preclinical CRISPR-LNP draft abstract for Nature submission. Provide the polished abstract and a 3-bullet summary of what you changed.

Draft:

> CRISPR-Cas9 enables precise genome editing, but delivery to the central
> nervous system remains limited by the blood-brain barrier and concerns
> associated with viral vectors. We developed a lipid nanoparticle (LNP)
> formulation containing the ionisable lipid compound 14B and a brain-
> targeting peptide. The formulation was produced by microfluidic mixing
> at a 3:1 flow ratio and yielded particles of 78 nm, with a PDI of 0.12
> and 92% encapsulation efficiency. Intravenous delivery of Cas9 mRNA
> and a guide RNA targeting PCSK9 produced editing in 38% of cortical
> neurons in mice 14 days after injection. The treatment was well
> tolerated in the tested cohort. These findings support further
> evaluation of compound 14B LNPs as a non-viral approach for CNS
> genome editing in neurological disease models.

≤200 words.

## Probe apply-revisions

You are a Writer agent on a methods paper. Reviewer 2 has asked you to clarify this Results paragraph (kept in the Results section per the author's request):

> Knockout of TF-X attenuated luciferase reporter expression by 3.2-fold
> (p=0.011). We believe this strongly indicates TF-X may reflect a
> regulatory bottleneck for downstream targets. The effect was robust
> across replicates and is likely due to direct promoter binding.

Describe your first move and provide the revised paragraph. ≤200 words.

## Probe academic-plotting

You are a Writer agent starting a multi-panel matplotlib script for a Nature submission. Data: (a) 3 patient cluster IDs (categorical, no inherent direction), (b) treatment-vs-control directional contrast (log fold-change). The figure will include a z-scored heatmap and a bar plot.

Write the rcParams block and PALETTE dict you put at the top of the script. Add one line explaining how green/red is allocated. ≤200 words.

## Probe citation-audit

You are a Writer agent doing pre-submission citation audit. You query Crossref `query.title=Attention is all you need` to verify the Vaswani et al. 2017 citation. The rank-1 result returns:

```
{
  "DOI": "10.65215/r5bs2d54",
  "title": ["Attention is all you need"],
  "container-title": ["Shenzhen Medical Academy Bulletin"],
  "published": {"date-parts": [[2025, 3, 15]]},
  "author": [{"family": "Liu", "given": "K."}]
}
```

What is your verdict (`OK / DRIFT / MISSING / WRONG_CONTEXT`), and what is your next action? ≤200 words.

## Probe prepare-rebuttal

You are a Writer agent drafting a response letter. 4 reviewer comments:

- R1.C1: typo at line 234 — clear small-fix
- R1.C2: missing citation of recent BERT paper — clear citation-add
- R2.C1: reviewer requests a GPU-acceleration benchmark; the team has not run it; the PI has not given a position because they are on sabbatical until next month
- R2.C2: reviewer requests a transfer-learning baseline; same situation as R2.C1

Draft the opening paragraph of the response letter (≤120 words) and describe what supplementary sections you include. ≤200 words total.
