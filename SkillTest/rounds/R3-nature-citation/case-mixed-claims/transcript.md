# Transcript — case-mixed-claims

## Brief (verbatim from "Brief for the runner" only)

> Identify which sentences need primary citations from the Nature Portfolio
> / Science family / Cell Press family. For each citable claim, propose a
> citation candidate with the metadata fields needed for retrieval (e.g.
> "first description of terminal exhausted T-cells in melanoma, ~2020,
> Cell"). Do NOT fabricate DOIs, page numbers, volume numbers, or
> author lists for citations the runner cannot independently verify;
> use placeholders with explicit "[needs verification]" tags. Translate
> Chinese claim fragments into citable English search terms.

## Source paragraph (verbatim)

> Single-cell transcriptomics has transformed our understanding of immune
> cell heterogeneity in tumour microenvironment, with multiple landmark
> studies showing CD8+ T-cell exhaustion as a key resistance mechanism in
> immunotherapy. The 第一篇 paper to characterise terminal exhausted T-cells
> in human melanoma was published in 2020 in Cell. Subsequent work in 2022
> in Nature Medicine extended this to colorectal cancer, identifying
> conserved exhaustion markers across solid tumours. Our findings build on
> these foundations and add a microbiome-derived signal that correlates
> with exhaustion (r=0.63, p<0.001 across 240 samples). The mechanism is
> probably mediated by short-chain fatty acid signalling 这个之前在 Science
> 上有人报道过. Methodologically, we follow the trajectory inference
> approach 与 Trapnell 在 2014 年 Nature Biotechnology 的工作 sharing the
> 核心 idea of pseudotime ordering, although our specific implementation
> uses scVelo for velocity-based pseudotime estimation.

## Baseline run

### What I did

Read only the source paragraph and runner brief. I extracted each citable claim, including Chinese fragments, and produced retrieval-oriented candidate descriptions without using the citation skill.

### Failures or shortcuts (be honest about anything you guessed at)

I did not verify any article metadata. Several rows rely on the paragraph's journal/year hints or broad topic descriptions, so they remain retrieval targets rather than confirmed citations.

## Candidate run

### Skill files actually loaded

- SKILL.md
- references/journal-scope.md (to apply Nature Portfolio / Science family / Cell Press boundaries)
- references/search-strategy.md (to segment claims, translate Chinese scientific concepts, and label support conservatively)
- references/ris-endnote.md (to confirm no missing bibliographic fields should be invented)

### What changed because of the skill

The candidate pass used stable segment IDs, separated broad background, method, internal-result and external-literature claims, applied CNS-family scope labels, and treated all unverified records as metadata-only candidates with `[needs verification]` placeholders.

### What I rejected from the skill

I did not run `scripts/nature_citation.py`, export RIS/ENW/RDF, or perform Crossref/PubMed/publisher searches because the case explicitly forbids network verification and the script requires network access.
