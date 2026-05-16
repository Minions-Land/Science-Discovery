# Response to Reviewers

Dear Editor and Reviewers,

We thank the editor and reviewers for their careful evaluation of our manuscript. We have addressed the two reviewer requests for which author-approved actions are available below. Two points require further author input before a final submission-ready response can be drafted; these are marked explicitly as `AUTHOR_INPUT_NEEDED`.

## Response to Reviewer 1

**Reviewer comment R1.C1**
> The benchmark on Dataset-A in Fig 3 should also report the median absolute error per cell type, not just overall RMSE.

**Response**
We thank the reviewer for this constructive suggestion. We agree that per-cell-type median absolute error will make the Dataset-A benchmark easier to interpret. We will revise Fig. 3 to include the per-cell-type median absolute error alongside the overall RMSE.

**Reviewer comment R1.C2**
> Line 87 cites Smith et al. 2021 as the originating paper for the deconvolution approach, but Jones et al. 2020 published a directly comparable framework with similar regularisation a year earlier. Please add the Jones citation.

**Response**
We agree that Jones et al. 2020 is relevant prior work and should be cited. We will revise the text around line 87 to cite Jones et al. 2020 alongside Smith et al. 2021 and to avoid overstating the precedence of the Smith et al. framework.

## Response to Reviewer 2

**Reviewer comment R2.C1**
> The runtime comparison in Table 2 used a 32-core CPU. The paper does not state whether GPU acceleration was attempted. If yes, please report GPU runtime separately. If no, please clarify in the methods that GPU support is future work.

**Response**
`AUTHOR_INPUT_NEEDED`: The current author brief does not state whether GPU acceleration was attempted. A final response would require a real computational fact rather than an inferred position. Once the PI confirms the status, the response should either report the GPU runtime separately or clarify in the Methods that the current benchmark was CPU-only and that GPU support is future work.

**Reviewer comment R2.C2**
> The validation cohort (n=80) is smaller than the discovery cohort (n=240). Could the authors comment on whether the 80-sample size provides adequate power for the conclusions drawn? A power calculation or post-hoc justification would help.

**Response**
`AUTHOR_INPUT_NEEDED`: The current author brief does not provide a statistical position on the validation cohort size. Because this is a statistical adequacy concern, we cannot draft final wording without the PI's decision and supporting details. The final response should state whether the authors will add a power calculation, a post-hoc justification, or a calibrated limitation regarding the validation cohort.

## Revision notes

- R1.C1 follows `ACCEPT_FIGURE`: add per-cell-type median absolute error to Fig. 3.
- R1.C2 follows `ADD_CITATION`: add Jones et al. 2020 and adjust the positioning around the original citation.
- R2.C1 follows `AUTHOR_INPUT_NEEDED`: the GPU-attempt status is missing and must not be inferred.
- R2.C2 follows `AUTHOR_INPUT_NEEDED`: the statistical justification is missing, and the skill treats major statistical critiques as high risk until details are supplied.

## Author input needed (skill-driven open questions)

- R2.C1: Was GPU acceleration attempted for the method or runtime benchmark?
- R2.C1: If yes, what GPU hardware, software configuration, dataset, and runtime should be reported, and should it appear in Table 2, Methods, or both?
- R2.C1: If no, what exact Methods wording should state that the benchmark is CPU-only and that GPU support is future work?
- R2.C2: Will the revision include a formal power calculation, a post-hoc justification, or limitation language only?
- R2.C2: What statistical assumptions, effect size or performance target, replicate unit, and confidence interval or uncertainty summary support the adequacy of n=80?
- R2.C2: Where should the justification or limitation appear in the manuscript?
