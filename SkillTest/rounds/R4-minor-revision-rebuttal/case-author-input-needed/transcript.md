# Transcript — case-author-input-needed

## Brief (verbatim from "Brief for the runner")

> Draft a point-by-point response letter for the editor.
>
> Author position (incomplete — only 2 of 4 comments resolved):
> - R1.C1 (median absolute error): the lab agrees this is straightforward
>   and will add the per-cell-type median absolute error to Fig 3.
> - R1.C2 (Jones citation): the lab agrees and will add Jones et al. 2020
>   alongside Smith et al. 2021.
>
> R2.C1 and R2.C2 — the lab has not yet decided. The PI is travelling
> and cannot be reached for 48 hours. Do NOT fabricate a position; flag
> these for author input clearly.

## Source comments (verbatim)

**Reviewer 1, Comment 1**
> The benchmark on Dataset-A in Fig 3 should also report the median
> absolute error per cell type, not just overall RMSE.

**Reviewer 1, Comment 2**
> Line 87 cites Smith et al. 2021 as the originating paper for the
> deconvolution approach, but Jones et al. 2020 published a directly
> comparable framework with similar regularisation a year earlier.
> Please add the Jones citation.

**Reviewer 2, Comment 1**
> The runtime comparison in Table 2 used a 32-core CPU. The paper does
> not state whether GPU acceleration was attempted. If yes, please report
> GPU runtime separately. If no, please clarify in the methods that GPU
> support is future work.

**Reviewer 2, Comment 2**
> The validation cohort (n=80) is smaller than the discovery cohort
> (n=240). Could the authors comment on whether the 80-sample size
> provides adequate power for the conclusions drawn? A power calculation
> or post-hoc justification would help.

## Author position (verbatim from brief — note 2 of 4 are unresolved)

> Author position (incomplete — only 2 of 4 comments resolved):
> - R1.C1 (median absolute error): the lab agrees this is straightforward
>   and will add the per-cell-type median absolute error to Fig 3.
> - R1.C2 (Jones citation): the lab agrees and will add Jones et al. 2020
>   alongside Smith et al. 2021.
>
> R2.C1 and R2.C2 — the lab has not yet decided. The PI is travelling
> and cannot be reached for 48 hours. Do NOT fabricate a position; flag
> these for author input clearly.

## Baseline run

### What I did

I read only the manuscript context, reviewer comments, and runner brief. I drafted a conventional point-by-point response letter without loading the nature-response skill, using explicit unresolved language for R2.C1 and R2.C2 because the brief forbade fabrication.

### Failures or shortcuts (be honest about how you handled R2.C1 and R2.C2)

The baseline did not use a formal action-label system or readiness taxonomy. It flagged R2.C1 and R2.C2 as unresolved, but only in plain prose rather than with a consistent `AUTHOR_INPUT_NEEDED` apparatus. It also did not produce a structured PI question list.

## Candidate run

### Skill files actually loaded

- SKILL.md
- references/intake-and-routing.md — used to classify task mode, readiness, and when missing input should block final wording.
- references/action-mapping.md — used for `ACCEPT_FIGURE`, `ADD_CITATION`, and `AUTHOR_INPUT_NEEDED` action labels.
- references/comment-taxonomy.md — used to classify the GPU issue as methodological and the cohort-size issue as statistical/high risk.
- references/response-structure.md — used for point-by-point anatomy and visible unresolved flags.
- references/tone-and-stance.md — used for concise, non-defensive response phrasing.
- references/difficult-cases.md — used because R2.C2 is a major statistical critique requiring real details.
- references/qa-checklist.md — used to check that no data, locations, line numbers, or author positions were invented.

### What changed because of the skill

The candidate response used stable comment IDs, explicit action labels, visible unresolved flags, and a separate author-input section. The two unresolved comments were not treated as draftable final responses.

### How AUTHOR_INPUT_NEEDED was emitted (which comments, what reasons, what PI questions)

`AUTHOR_INPUT_NEEDED` was emitted for R2.C1 because the fixture does not say whether GPU acceleration was attempted. The PI questions ask whether GPU acceleration was attempted, what hardware/software/runtime details should be reported if yes, and what CPU-only/future-work wording should be used if no.

`AUTHOR_INPUT_NEEDED` was emitted for R2.C2 because the fixture gives no position on power, post-hoc justification, or limitation language. The PI questions ask which strategy the authors will use, what statistical assumptions or uncertainty summaries support n=80, and where the revision should appear.

### What I rejected from the skill

I did not use the skill's full default package format with response strategy summary, tracker table, manuscript checklist, and risk flags because the case specified a narrower output structure for candidate.md. I also did not load Chinese-author-alignment.md or source-basis.md because the fixture and requested output did not require Chinese alignment or policy-source adjudication.
