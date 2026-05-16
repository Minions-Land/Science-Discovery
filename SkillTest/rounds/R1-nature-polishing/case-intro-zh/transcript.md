# Transcript — case-intro-zh

## Brief

> Polish the paragraph above into publication-ready English suitable for a Nature
> Communications introduction. Keep the technical content. The paragraph appears
> as the third paragraph of the introduction (after a broad-context opener and a
> related-work paragraph).

## Source paragraph

> 蛋白质语言模型 (PLMs) 在最近这几年里因为其强大的表征能力被广泛地应用于很多生物学任务中，并且在结构预测、功能注释、突变效应预测等下游任务上都表现出了非常优异的性能，这是非常 crucial 的 progress。然而尽管如此，目前主流的 PLM 训练范式严重依赖于大规模的序列数据集，并且这些数据集通常存在显著的物种偏差和功能注释不平衡的问题，从而限制了模型在罕见蛋白家族和未充分表征的功能类别上的泛化能力。在这项工作中，我们 delve into 这个问题，并且提出了一个新颖的训练框架，它能够 — through a series of careful design choices — 显著提升 PLM 在长尾蛋白家族上的鲁棒性，并且我们认为这个工作 is important to note 因为它可能会改变现有 PLM 训练的最佳实践。我们在六个 benchmark 上做了实验，结果表明我们的方法相比于现有的 baseline 都获得了 substantial 的提升。

## Baseline run

### What I did

- Rebuilt the paragraph into English rather than translating each mixed-language clause.
- Kept a conventional introduction flow from context to limitation to contribution.
- Removed obvious mixed-register wording and standardised technical terms.
- Avoided adding numerical performance claims that were not supplied.

### Failures or shortcuts

- I kept a broader context opener even though the brief said this was the third Introduction paragraph.
- I did not explicitly enforce the 30-word sentence rule.

## Candidate run

### Skill files actually loaded

- SKILL.md
- references/section-moves.md, for Introduction gap-before-aim ordering.
- references/phrasebank-playbook.md, for precise gap language and evidence calibration.
- references/style-guardrails.md, for academic register and mechanics.

### What changed because of the skill

- I removed the broad opener because the skill's hourglass check showed that this paragraph should narrow to the gap.
- I used Chinese-to-English mode and extracted the propositions before rewriting.
- I treated the unquantified benchmark improvement as a reporting boundary.
- I checked sentence length and removed dash punctuation.

### What I rejected from the skill

- I did not add stock phrases such as "few studies have examined" because the source did not establish a literature gap beyond data bias.
