# Response to Reviewers

Dear Editor,

We thank you and the reviewers for the constructive assessment of our manuscript. We are pleased that the manuscript is considered suitable for minor revision, and we have prepared the following point-by-point responses.

## Reviewer 1, Comment 1

> The benchmark on Dataset-A in Fig 3 should also report the median absolute error per cell type, not just overall RMSE.

We agree with the reviewer that reporting per-cell-type median absolute error will make the benchmark more informative. We will add these values to Fig. 3 so that readers can assess performance across individual cell types in addition to the overall RMSE.

## Reviewer 1, Comment 2

> Line 87 cites Smith et al. 2021 as the originating paper for the deconvolution approach, but Jones et al. 2020 published a directly comparable framework with similar regularisation a year earlier. Please add the Jones citation.

We thank the reviewer for identifying this omission. We will revise the citation at line 87 to include Jones et al. 2020 alongside Smith et al. 2021, and will adjust the surrounding wording so that the prior comparable framework is properly acknowledged.

## Reviewer 2, Comment 1

> The runtime comparison in Table 2 used a 32-core CPU. The paper does not state whether GPU acceleration was attempted. If yes, please report GPU runtime separately. If no, please clarify in the methods that GPU support is future work.

The author team has not yet confirmed whether GPU acceleration was attempted for this benchmark. This point should not be finalized until the PI confirms the actual computational setup. If GPU acceleration was attempted, the revised manuscript should report GPU runtime separately in Table 2 or the Methods. If it was not attempted, the Methods should state that the current implementation was benchmarked on CPU and that GPU support remains future work.

## Reviewer 2, Comment 2

> The validation cohort (n=80) is smaller than the discovery cohort (n=240). Could the authors comment on whether the 80-sample size provides adequate power for the conclusions drawn? A power calculation or post-hoc justification would help.

The author team has not yet provided a position or statistical justification for this point. We therefore cannot provide a final response without additional input. The PI should confirm whether a power calculation, post-hoc justification, or appropriately qualified limitation will be added, and the response should then point to the relevant Methods, Results, or Discussion revision.

## Revision notes

- Add per-cell-type median absolute error values to Fig. 3 for Dataset-A.
- Add Jones et al. 2020 alongside Smith et al. 2021 at the relevant citation point.
- R2.C1 remains unresolved until the PI confirms whether GPU acceleration was attempted.
- R2.C2 remains unresolved until the PI confirms the statistical justification or limitation language for the validation cohort size.
