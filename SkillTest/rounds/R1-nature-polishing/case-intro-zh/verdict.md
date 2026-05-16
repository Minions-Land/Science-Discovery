# Verdict — nature-polishing / case-intro-zh

**Round:** R1.C · **Date:** 2026-05-16 · **Rubric version:** v1

## Numeric score

| Dim | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|
| Argument clarity / paper-type fit | 2/4 | 4/4 | +2 | baseline keeps original draft order (context → limitation → contribution); candidate puts the gap first ("Current PLM training depends on ... uneven species coverage"), then bounds, then "Here, we introduce" — proper hourglass narrowing |
| Hedging calibration | 2/3 | 3/3 | +1 | baseline asserts "the method outperforms existing baselines" — unhedged, no numbers; candidate flags "the size of these gains should be reported in the Results" — refuses to fabricate quantification |
| Sentence rhythm | 3/3 | 3/3 | 0 | both ≤30 words |
| AI-trace removal | 3/3 | 3/3 | 0 | both removed crucial / delve into / important to note / substantial |
| Claim-evidence completeness | 2/4 | 4/4 | +2 | baseline silently dropped the original "six benchmarks" claim from prose without flagging the missing numbers; candidate keeps "Across six benchmarks" but adds the explicit limitation that the gain size belongs in Results — the right honest move |
| Citation hygiene | 2/3 | 2/3 | 0 | not exercised |
| House style consistency | 2/2 | 2/2 | 0 | both British |
| **Total** | **16/22** | **21/22** | **+5** | |

## What the skill actually changed

Three load-bearing changes:

1. **Hourglass restructure.** The baseline preserved the original Chinese draft order (broad context → limitation → contribution). The candidate flipped this to gap-first ("Current PLM training depends on...uneven species coverage and imbalanced functional annotation"), then named the consequence ("biases can limit generalisation"), then introduced the contribution ("Here, we introduce..."). This is what the skill calls "Chinese-to-English mode: reconstruct the logic first, the prose second."
2. **Refusal to fabricate.** Both runs faced the source claim "substantial improvements over baselines" without numbers. Baseline silently re-asserted "outperforms existing baselines" (slightly better — it dropped "substantial" — but still claims a result without evidence). Candidate flagged the missing numbers explicitly: "the size of these gains should be reported in the Results." This is the skill's "do not invent" rule biting.
3. **Explicit "Here, we" anchor.** Baseline says "In this study, we examine this problem and introduce..." — narrating. Candidate says "Here, we introduce..." — direct. The "Here, we" formula is named in the skill's section-moves reference.

## What the skill missed or hurt

Candidate's prose is slightly *terser* than ideal — 96 words vs baseline's 91 in the prose proper (the rest is notes). This is the skill's preference for compactness; for an Introduction paragraph in a Nature-family paper, the candidate could probably afford another sentence linking the contribution to a concrete output. Not a hurt, but a limit.

## Visual / textual inspection

Side-by-side reading — the candidate prose feels like an Introduction third paragraph in a published Nature Communications paper. The baseline prose feels like a competent translation of the original Chinese flow, which is exactly what the skill is supposed to break.

## Token cost

See `tokens.json`. Candidate input ~10–13× (skill SKILL.md alone, no extra references opened by the runner because the SKILL.md was self-contained for this case). Output 156 vs 133 words — 17% longer for the diagnosis footer.

## Bucket

**Prevents real failure.** Baseline-style output is publishable but signals the original Chinese draft order to a Nature reviewer; candidate output is restructured for the venue. For Chinese-author labs targeting CNS, this is the load-bearing skill use case.

## Porting recommendation

`import-as-is` for Chinese-to-English mode. The "reconstruct logic first, translate clauses second" rule plus the hourglass move set is the highest-ROI port from R1.C. Add to MinionsOS Writer's `paper-literature-search.md` peer skill or create a dedicated `cn-en-academic-polish.md`.
