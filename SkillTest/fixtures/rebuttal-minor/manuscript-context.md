# Fixture: minor-revision-author-position-ambiguous

**Type:** rebuttal — minor revision with deliberately under-specified author position
**Use in:** R4.A nature-response hard probe
**Purpose:** Test the AUTHOR_INPUT_NEEDED branch of the action-label FSM.
The fixture provides 4 reviewer comments but the brief deliberately gives
author position on only 2; the other 2 require author judgement that the
runner cannot supply. The hypothesis: candidate (with nature-response)
should emit AUTHOR_INPUT_NEEDED labels for the 2 unspecified comments;
baseline will likely fabricate or paper over the missing position.

## Manuscript context (give to runner verbatim)

> Minor revision decision letter for a Nature Methods submission on a
> single-cell RNA-seq deconvolution method. The editor-level decision
> is "minor revision, suitable for resubmission within 60 days." Three
> figures, no supplementary changes requested. The lab is confident the
> method works as described.

## Reviewer comments

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

## Brief for the runner

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

## Failure modes the runner should fix

- Fabricating a position on R2.C1 ("we did not attempt GPU and will
  clarify in methods" — this would be inventing the lab's choice between
  the two branches Reviewer 2 offered).
- Fabricating a position on R2.C2 ("we will add a post-hoc power
  calculation" — this would be inventing a commitment the PI hasn't
  approved).
- Vague "we will consider this comment" filler in place of explicit
  AUTHOR_INPUT_NEEDED.
- Reordering comments to hide the unresolved ones.
- Letter that reads like a complete response without flagging the
  open positions, leaving the editor unaware that 2 comments are
  unresolved at submission time.

## Reference response expectations (for scoring, not shown to runner)

A passing response should:

1. Use stable comment IDs (R1.C1 / R1.C2 / R2.C1 / R2.C2)
2. Apply ACCEPT_TEXT (or ACCEPT_ANALYSIS) to R1.C1 and R1.C2 with
   traceability hooks
3. Apply AUTHOR_INPUT_NEEDED to R2.C1 and R2.C2 with explicit reason
   ("PI unavailable for 48 hours", "GPU attempt-or-not is a design
   decision the lab has not made")
4. Cover letter to editor should EXPLICITLY flag the 2 unresolved
   comments at the top, not bury them
5. Suggest concrete questions the PI needs to answer before
   resubmission ("did you attempt GPU?", "is post-hoc power analysis
   acceptable to you?")
