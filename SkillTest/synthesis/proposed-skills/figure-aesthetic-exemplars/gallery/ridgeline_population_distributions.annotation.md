# Annotation — ridgeline_population_distributions

**Source:** SkillTest self-generated (R-future-3 Task 4) applying R-future-2
Principles 1-6.

**Archetype:** Stacked distribution per category (joyplot variant). Use when
showing how N distributions shift across a parameter / time / treatment axis.

**User grade (R-future-3):** "整体很朴素... 还行吧." Acceptable but not
"非常漂亮" tier. Useful as reference for distribution-stacking pattern.

## Extracted palette

Single-blue family with saturation gradient: `#154095` → `#406ac0` → `#95c0ea`.
Middle population emphasised by stroke weight (`linewidth=1.4` vs default 0.8)
to anchor the visual.

## What works

1. Single-hue family (P1 cool variant) — eye doesn't have to resolve "which
   distribution maps to which category" from hue.
2. Saturation gradient encodes ordering. Position 1 (faded) → position N (deep)
   shows progression.
3. Stroke weight contrast for the central population draws focus to the
   distribution under interrogation.
4. Y-axis suppressed (no tick labels) — it's the position label that matters,
   not absolute density.

## Known limitations

User R-future-3: "非有效位置太多了，左右两边有很多没有分布、没有山岭的部分."
Distribution tails extend to plot bounds; trim x-axis range to where data
density is meaningful. Future Task 4 v3 could fix this.

## When to use

For showing how a distribution shifts across N categories (where N=4-8) —
ridgeline communicates "all distributions at once, with clear ordering"
better than violin-per-category panels.
