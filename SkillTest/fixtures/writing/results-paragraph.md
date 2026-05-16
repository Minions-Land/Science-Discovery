# Fixture: results-paragraph

**Type:** writing — Results section paragraph with mixed tense and Discussion creep
**Use in:** R1.C nature-polishing, R2 research-paper-writing
**Purpose:** Test whether the skill (a) detects Results-vs-Discussion mixing,
(b) corrects tense (Results = past tense), (c) trims interpretive verbs.

## Source paragraph (deliberately mixed)

> Treated cells show a 3.2-fold increase in expression of the target gene compared
> to control (Fig. 2c, n=4 per group, two-tailed t-test, p=0.011), and we believe
> this may reflect activation of the upstream regulatory module that we previously
> hypothesised. We then perform single-cell RNA-seq on the same population and
> identify a rare subset (~4% of cells) that strongly expresses both the target
> and a known co-activator, suggesting the regulatory module operates in a cell-
> type-specific manner. The fact that this subset is enriched in the treated
> condition (1.8-fold, hypergeometric p=0.003) is likely due to selective
> proliferation rather than a transcriptional state change, although further
> evidence is needed to confirm this. Finally, knocking down the co-activator
> abolishes the response, which strongly indicates the regulatory module is
> required.

## Brief for the runner

> Polish the paragraph above as the second paragraph of a Results section in a
> Nature-family cell biology paper. The lab convention is past tense for Results
> and reserved hedging for Discussion.

## Failure modes the runner should fix

- Tense: `show / perform / identify` should be past
- Discussion creep: `we believe`, `may reflect`, `likely due to`, `strongly indicates` belong in Discussion
- Long sentence (`The fact that ...`) — 35 words, two propositions
- "Believe" as evidential verb in Results — replace with the actual measurement
- "We previously hypothesised" — fine if cited; otherwise drop

## Reference rewrite expectations

1. All main verbs past tense
2. Each sentence reports `was observed / increased / decreased / detected` rather than `may / could / suggests`
3. Single-claim sentences (split the long one)
4. Numbers and statistics in every claim that has them
5. No interpretive verbs except where labelled as a transition into Discussion (none here)
