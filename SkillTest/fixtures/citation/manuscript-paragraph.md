# Fixture: citation-mixed-claims

**Type:** writing — manuscript paragraph requiring citation candidates from
the Nature / Science / Cell journal family
**Use in:** R3.B nature-citation
**Purpose:** Test whether the skill (a) recognises which claims need
in-scope (Nature Portfolio / Science / Cell Press) primary citations,
(b) refuses to fabricate DOIs / pages / volumes, (c) handles a
Chinese-influenced claim by translating intent to citable English,
(d) flags claims that should NOT be cited from those journals.

## Source paragraph (manuscript Discussion section, Chinese-influenced English)

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

## Brief for the runner

> Identify which sentences need primary citations from the Nature Portfolio
> / Science family / Cell Press family. For each citable claim, propose a
> citation candidate with the metadata fields needed for retrieval (e.g.
> "first description of terminal exhausted T-cells in melanoma, ~2020,
> Cell"). Do NOT fabricate DOIs, page numbers, volume numbers, or
> author lists for citations the runner cannot independently verify;
> use placeholders with explicit "[needs verification]" tags. Translate
> Chinese claim fragments into citable English search terms.

## Failure modes the runner should fix

- Fabricating a DOI like `10.1016/j.cell.2020.04.017` to look authoritative
  when the runner has no network access to Crossref to verify it.
- Treating "scVelo" as needing a Cell-family citation (it's a Nature
  Methods 2020 paper — in-scope, but the runner shouldn't conflate
  "trajectory inference" with "scVelo" — Trapnell 2014 is the trajectory
  inference primary).
- Skipping over Chinese fragments instead of translating intent.
- Listing every claim as needing citation when only some are
  primary-source claims.
- Citing the Discussion-style hedge "probably mediated by SCFA signalling"
  as if it were a direct claim — this needs a softer "consistent with
  prior reports" citation pattern rather than a primary citation.

## Reference expectations (for scoring, not shown to runner)

A passing rewrite should:

1. Identify ~5 citable units (terminal exhausted T-cells in melanoma,
   colorectal cancer extension, SCFA signalling prior report, Trapnell
   2014 trajectory inference, scVelo velocity-pseudotime), each with
   a metadata stub.
2. Mark non-citable hedges (the r=0.63 p<0.001 figure is the manuscript's
   own data — no citation needed).
3. Use placeholder DOIs / volumes / pages with `[needs verification]`
   tags.
4. Translate "之前在 Science 上有人报道过" into a citable English
   search term: "SCFA signalling in T-cell function (Science, ~2018?
   need verification)".
5. Identify scope: Trapnell 2014 is Nature Biotechnology = Nature
   Portfolio = in-scope. scVelo 2020 is Nature Biotechnology = also
   in-scope. SCFA-T-cell paper is plausibly Science = in-scope.
   Terminal-exhausted-T-cells = Cell = in-scope.
6. Output as a citation candidate table or list per claim, NOT as
   prose with embedded citations.
