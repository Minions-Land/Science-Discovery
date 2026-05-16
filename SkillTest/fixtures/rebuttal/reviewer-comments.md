# Fixture: rebuttal — mixed-severity reviewer block

**Type:** rebuttal — 5 reviewer comments spanning major / minor / disagree
**Use in:** R2 nature-response, future rebuttal-skill rounds
**Purpose:** Test whether the skill (a) tags every comment with a stable ID +
type, (b) maps each to an action class, (c) includes traceability hooks, (d)
handles a comment where authors should disagree.

## Manuscript context (give to runner verbatim)

> The submitted manuscript reports a CRISPR-Cas9 LNP delivery system targeting
> *PCSK9* in the central nervous system, achieving 38% editing efficiency in
> cortical neurons at 14 days post-injection in C57BL/6 mice (n=6 per group).
> Three figures: (Fig 1) formulation characterisation; (Fig 2) in vivo editing
> efficiency by region; (Fig 3) plasma cholesterol over 8 weeks. Supplementary
> figures cover histology, immunogenicity, and dose-response.

## Reviewer comments

**Reviewer 1, Comment 1**
> The 38% editing efficiency in cortical neurons is intriguing but the cohort is
> small (n=6). Please replicate in a second mouse strain with n≥12 to support the
> generality claim, and report editing efficiency stratified by neuron subtype
> (e.g. excitatory vs inhibitory).

**Reviewer 1, Comment 2**
> Fig 2c y-axis goes from 30% to 45%, which exaggerates the differences between
> regions. Please re-plot with a 0–100% scale or justify the truncation.

**Reviewer 1, Comment 3**
> The cholesterol reduction in Fig 3 (~22%) is modest. Statins routinely achieve
> 40–60%. The clinical relevance claim in the discussion is overstated and
> should be removed.

**Reviewer 2, Comment 1**
> Compound 14B has not been chemically characterised in this manuscript beyond
> a structural diagram. Please provide ¹H-NMR, mass spectrum, and HPLC purity
> data in the supplement.

**Reviewer 2, Comment 2**
> The authors claim the brain-targeting peptide enables BBB crossing, but no
> direct comparison to a peptide-free control is shown. Please add this control
> or remove the BBB-crossing-mechanism claim.

## Brief for the runner

> Draft a point-by-point response letter for the editor, classifying each comment,
> mapping to a concrete manuscript action, and showing where evidence will land.
> The authors' scientific position: comments 1.1, 2.1, and 2.2 are accepted;
> comment 1.2 should be partially accepted (replot is fine, but the truncation
> was justified by FDA-style guidance — explain in caption); comment 1.3 should
> be respectfully declined — the cholesterol effect is mechanistically novel
> (CNS-only PCSK9) regardless of magnitude.

## Failure modes the runner should fix

- Treating every comment as ACCEPT (sycophantic revision)
- Missing comment IDs (R1.C1, R1.C2, ... R2.C2) → cross-referencing breaks
- "We thank the reviewer..." filler with no actionable content
- Disagreeing without scientific justification (just "we disagree")
- Promising experiments without flagging timeline / cohort dependencies
- No traceability anchors (page X, Fig Y, line Z, supplement S2)

## Reference response expectations

1. Stable IDs (R1.C1 ... R2.C2) used throughout
2. Each reply tagged with action: ACCEPT_EXPERIMENT / ACCEPT_TEXT / SOFTEN_CLAIM
   / DISAGREE_WITH_JUSTIFICATION / AUTHOR_INPUT_NEEDED
3. Traceability per change: section, page, line, figure, or supplement
4. R1.C3 disagreed-with on scientific grounds (CNS-only PCSK9 is mechanistically
   distinct from systemic statins; not magnitude-equivalent)
5. R1.C2 partial acceptance with caption justification
6. Tone cooperative and evidence-forward
