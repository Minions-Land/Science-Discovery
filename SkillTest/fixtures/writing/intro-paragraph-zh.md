# Fixture: intro-paragraph-zh

**Type:** writing — Chinese-influenced English introduction paragraph
**Use in:** R1.C nature-polishing, R3 deslop family
**Purpose:** Test whether the skill can (a) reconstruct logic from Chinese-influenced
sentence flow, (b) keep technical terms stable, (c) cap sentence length, and (d)
position the gap before the contribution.

## Source paragraph (deliberately rough)

> 蛋白质语言模型 (PLMs) 在最近这几年里因为其强大的表征能力被广泛地应用于很多生物学任务中，并且在结构预测、功能注释、突变效应预测等下游任务上都表现出了非常优异的性能，这是非常 crucial 的 progress。然而尽管如此，目前主流的 PLM 训练范式严重依赖于大规模的序列数据集，并且这些数据集通常存在显著的物种偏差和功能注释不平衡的问题，从而限制了模型在罕见蛋白家族和未充分表征的功能类别上的泛化能力。在这项工作中，我们 delve into 这个问题，并且提出了一个新颖的训练框架，它能够 — through a series of careful design choices — 显著提升 PLM 在长尾蛋白家族上的鲁棒性，并且我们认为这个工作 is important to note 因为它可能会改变现有 PLM 训练的最佳实践。我们在六个 benchmark 上做了实验，结果表明我们的方法相比于现有的 baseline 都获得了 substantial 的提升。

## Brief for the runner

> Polish the paragraph above into publication-ready English suitable for a Nature
> Communications introduction. Keep the technical content. The paragraph appears
> as the third paragraph of the introduction (after a broad-context opener and a
> related-work paragraph).

## Failure modes the runner should fix

- Sentence ≥30 words (4 currently exceed)
- AI-trace vocabulary: `crucial`, `delve into`, `is important to note`, `substantial`
- Em-dash inside an English clause (`— through ... —`)
- Mixed register: some sentences narrative, some pitch-deck
- Claim without specifics: "six benchmarks", "substantial improvements" — no numbers
- Logic order: gap should precede contribution; contribution should precede results
- British vs American: `behaviour` vs `behavior` not present here, but `analyse` may show up in revision

## Reference rewrite (for scoring, not shown to runner)

A passing rewrite should:
1. Open with the gap (training-data bias and tail under-representation)
2. State the contribution in one ≤30-word sentence
3. Quantify the result (or flag that numbers belong to results section)
4. Not use `crucial / delve / important to note / substantial`
5. Use ≤2 em-dashes in the whole paragraph (none inside a clause)
6. Keep `protein language models` / `PLMs` / `long-tail families` stable across the paragraph
