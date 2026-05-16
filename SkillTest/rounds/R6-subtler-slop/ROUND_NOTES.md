# Round Notes — R6.C subtler-slop hard probe

**Cases:** case-buried-slop (1 fixture × 4 candidates + baseline, on Haiku 4.5)
**Date:** 2026-05-16

## Headline

**3rd consecutive deslop round confirming "skip" recommendation.**
Haiku 4.5 baseline removed all 5 buried slop terms without skill guidance.
4 candidate skills produced output statistically indistinguishable from
baseline.

## Cross-validation summary (R3.C + R4.C + R6.C)

| Round | Executor | Slop density | Baseline | Best candidate | Δ |
|---|---|---|---|---|---|
| R3.C | Opus 4.7 | saturated | 0 slop | 0 slop | 0 |
| R4.C | Haiku 4.5 | saturated | 0 slop | 0 slop | 0 |
| R6.C | Haiku 4.5 | buried | 0 slop | 0 slop | 0 |

3 rounds × 4 skills × 2 executor classes × 2 slop densities = 24
empirical data points. Zero differentiation across all of them.

## Bucket per skill (final, after 3 rounds)

| Skill | Bucket | Recommendation |
|---|---|---|
| skill-deslop | Matches baseline ×3 | skip (final) |
| avoid-ai-writing | Matches baseline ×3 | skip (final) |
| humanizer-academic | Matches baseline ×3 | skip (final) |
| stop-slop | Matches baseline ×2, marginal Calibrates ×1 | skip (final) |

## Recommendation

`skip` 4 of 4. The deslop family is empirically inert at any executor scale
or slop density that matters for MinionsOS Writer.

Update synthesis/what-to-skip.md entry #5 to "confirmed across 3 rounds,
24 data points, no differentiation." This question is now closed.

## What R6.C added beyond R3.C and R4.C

The R6.C fixture was specifically designed to be the worst case for the
"baseline already handles slop" hypothesis: slop interspersed in clean
prose where lazy editing might leave it standing. Even there, baseline
caught everything. The "skip" recommendation is no longer a calibration
of executor class or slop density; it's a structural fact about
2026-vintage instruction-tuned models.
