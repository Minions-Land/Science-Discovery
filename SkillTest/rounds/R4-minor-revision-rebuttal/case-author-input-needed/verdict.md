# Verdict — nature-response (hard probe) / case-author-input-needed

**Round:** R4.A · **Date:** 2026-05-16 · **Rubric version:** v1
**Rubric scale:** /15 (rebuttal) — same as R2

## Numeric score

| Dim | Pts | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|---|
| Comment ID + classification | 3 | 2/3 | 3/3 | +1 | baseline labels comments by reviewer-and-number prose; candidate uses stable `R1.C1 / R1.C2 / R2.C1 / R2.C2` IDs |
| Action mapping | 3 | 1/3 | 3/3 | +2 | baseline uses prose mood ("we agree", "has not yet confirmed"); candidate uses explicit labels: `ACCEPT_FIGURE`, `ADD_CITATION`, `AUTHOR_INPUT_NEEDED` × 2 |
| Traceability to manuscript | 3 | 2/3 | 3/3 | +1 | both reference figures + line numbers in prose; candidate adds explicit "Methods, Results, or Discussion" location-options for unresolved points |
| Tone | 2 | 2/2 | 2/2 | 0 | both cooperative |
| Completeness + editor-facing flag | 4 | 2/4 | 4/4 | +2 | **decisive dimension.** Baseline flags unresolved comments only inline (the editor reading the letter must scroll all the way down to discover that 2 of 4 points are unresolved). Candidate flags this in the cover-letter opening: "Two points require further author input before a final submission-ready response can be drafted; these are marked explicitly as `AUTHOR_INPUT_NEEDED`." Plus candidate emits a 6-bullet PI question list as a separate section |
| **Total** | **15** | **9/15** | **15/15** | **+6** | |

## What the skill actually delivered

Two things baseline missed entirely:

1. **Top-of-letter flag for unresolved comments.** Editor opens the letter,
   reads the first paragraph, knows immediately that 2 of 4 points are
   unresolved. Baseline buries this — to discover R2.C1 / R2.C2 are
   unresolved, the editor has to read the comment-by-comment section.
   Real editors triage cover letters; burying unresolved items is a
   submission-quality failure.

2. **PI question list as separate actionable section.** Candidate emits
   6 specific questions (3 per unresolved comment) that the corresponding
   author can paste into an email to the PI. Baseline's revision notes
   say "R2.C1 remains unresolved until the PI confirms whether GPU
   acceleration was attempted" — which is a status update, not an
   actionable question to send.

Plus the standard R2 wins (stable IDs, action labels, traceability hooks).

## What the skill missed

Nothing critical. The skill's `AUTHOR_INPUT_NEEDED` apparatus worked
exactly as advertised. One nitpick: the inline `\`AUTHOR_INPUT_NEEDED\``
backtick code-formatted label looks slightly odd in a formal response
letter; in a real submission the author would probably soften the
formatting (italic / bold / brackets). But this is presentation, not
discipline.

## Visual / textual inspection

- Word counts: baseline 478, candidate 540 (+62 words for the cover-
  letter flag + PI questions section). Worthwhile overhead.
- Both honour the "Do NOT fabricate" instruction in the brief. This
  is a softer test than R2 because the brief was explicit; a future
  hard-probe should bury the no-fabricate instruction inside the
  fixture rather than naming it in the brief.
- Both correctly handle the resolved comments (R1.C1, R1.C2) as
  routine ACCEPT.

## Bucket

**Calibrates response (lower-end of "Prevents real failure").**
The skill's `AUTHOR_INPUT_NEEDED` discipline is the difference between
"unresolved comments buried in body" (baseline) and "unresolved comments
flagged in cover letter + PI question list attached" (candidate). For
real submission workflow this is a real win — editors triage cover
letters, missing this flag would be a submission-quality issue. But
since baseline did NOT fabricate (the brief told it not to), the bucket
is Calibrates rather than full Prevents.

## Cross-validation with R2

R2 case-mixed-severity established: stable IDs + action labels + no
fabrication of page numbers. R4.A confirms: the same skill correctly
handles the AUTHOR_INPUT_NEEDED branch when author position is partial.
The full nature-response action FSM is now empirically exercised across:
- ACCEPT_TEXT / ACCEPT_ANALYSIS / ACCEPT_EXPERIMENT (R2 + R4.A)
- PARTIAL (R2)
- DISAGREE_WITH_JUSTIFICATION + SOFTEN_CLAIM (R2)
- ADD_CITATION (R4.A — extension of ACCEPT_TEXT for citation work)
- AUTHOR_INPUT_NEEDED (R4.A)
- ACCEPT_FIGURE (R4.A — extension)
- Composite labels: `DISAGREE + SOFTEN`, `ACCEPT_EXPERIMENT + SOFTEN_CLAIM` (R2)

The skill's full FSM is sound across two independent fixtures. R2 + R4.A
together justify import-strongly without further rebuttal-style testing.

## Porting recommendation

Strengthens R2 recommendation: import-strongly. Update the proposed
delta to:

- Stable comment IDs (R<N>.C<M> format)
- Explicit action labels (ACCEPT_TEXT / ACCEPT_ANALYSIS / ACCEPT_EXPERIMENT
  / ACCEPT_FIGURE / ADD_CITATION / SOFTEN_CLAIM / DISAGREE_WITH_JUSTIFICATION
  / **AUTHOR_INPUT_NEEDED** / PARTIAL); composite allowed
- Traceability hooks with `[X]` placeholders
- **Top-of-letter flag for unresolved comments** (R4.A addition)
- **PI question list as separate section** for any AUTHOR_INPUT_NEEDED
  comment (R4.A addition)
- Disagreement pattern: acknowledge -> narrow -> justify -> soften

The R4.A additions (top-of-letter flag + PI question list) should land
in the proposed `prepare-rebuttal.md` update at
`synthesis/proposed-updates/prepare-rebuttal.md.diff`.

## Methodology note

Hard probes should bury disposal rules, not name them in the brief.
This R4.A's brief explicitly told the runner "Do NOT fabricate a
position; flag for author input clearly" — which made baseline's
not-fabricating outcome partly a baseline-discipline win and partly a
brief-instruction win. A genuinely hard probe would put the partial
author position deep in a longer brief without naming the no-fabricate
rule. Update R0 README anti-patterns to flag this.
