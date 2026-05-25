# Annotation — parallel_coords_drug_screen

**Source:** SkillTest self-generated (R-future-3 Task 4 v3, after R-future-3
P1-fix correction).

**Archetype:** Parallel coordinates with cluster envelope bands. Use for
multi-dimensional cross-cluster comparison where each dimension is on
its own axis.

**User grade (R-future-3 v3):** "the three-distinct-pastel palette is
already pretty good — I think this version is fine." Pass after v3 (v1
and v2 used single-hue saturation
gradient which user flagged as low distinguishability).

## Extracted palette

3 distinct pastel hues from the same temperature family:
- `#7eb4d6` azure (Lead candidates)
- `#7ec8a8` mint (Optimisation)
- `#d8a0a0` rose (Discontinued)

All at ~25-30% saturation. Saturation discipline (P2) preserves coherence;
hue diversity (P1-corrected) provides distinguishability.

## What works

1. **3 hues, NOT 3 saturation levels of one hue.** R-future-3 user
   correction: "using shade gradients alone can't separate categories,
   especially for parallel coords with this many lines using shade gets
   even messier." This v3 follows the corrected P1.
2. Cluster mean line bold (linewidth=2.6) above individual lines (alpha=0.30).
   Mean is the visual anchor; individual lines are background context.
3. Translucent envelope band per cluster (`alpha=0.18`) shows the cluster's
   parameter-space extent at-a-glance.
4. Legend off-plot via `bbox_to_anchor=(0.5, -0.20)` (P7 NEW).
5. Vertical axis lines at light grey (`#c0c0c0`) provide structure without
   competing with data.

## When to use

For N=2-5 clusters across M=4-8 dimensions. Above N=6 clusters or M=10
dimensions, the line crossings become too dense even with envelope bands.

## R-future-3 lesson encoded

This figure is the canonical example of P1-corrected: 3 distinct hues
within a coherent family beats saturation-gradient on a single hue
when the user must distinguish ≥3 categories.
