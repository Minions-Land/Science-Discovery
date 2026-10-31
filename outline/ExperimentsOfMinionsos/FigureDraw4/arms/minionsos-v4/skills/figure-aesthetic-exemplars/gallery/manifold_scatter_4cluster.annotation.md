# Annotation — manifold_scatter_4cluster

**Source:** SkillTest self-generated (R-future-3 Task 1 candidate v2 — passed
user grading after the v3 hull-shading attempt was rejected as
"not very meaningful").

**Archetype:** 2D embedding scatter with N=4 clusters, each as a distinct
pastel hue. Use when data is naturally a manifold / embedding and clusters
are the primary information.

**User grade (R-future-3-final):** "v2 works... reference is also fine."
Acceptable;
distinct from `diffusion_swiss_roll` (manifold-as-curve) — this is
manifold-as-discrete-clusters.

## Extracted palette

4 distinct pastel hues from the same temperature family:
- `#7eb4d6` azure (progenitor)
- `#7ec8a8` mint (intermediate)
- `#d8a0a0` rose (terminal A)
- `#b09bc8` violet (terminal B)

All ~25-30% saturation. P1-corrected: 4 hues, NOT 4 saturation levels of
one hue. Distinguishability comes from hue diversity within the family.

## What works

1. **Cluster identity via 4 distinct hues** (P1 corrected interpretation).
   With 4 clusters, saturation gradient on single hue would be unreadable.
2. **White marker edges** keep dot boundaries crisp on overlapping regions.
3. **Inline cluster labels with white halo** (per fig4 annotation pattern).
   No legend block competing with the data.
4. **Marker size s=12-15** — small enough that clusters with N=250 don't
   over-saturate visual area; large enough that individual points are
   visible.
5. **No artificial visual area filler** — the data IS scattered, and the
   figure honestly shows that. Adding convex-hull shading was tested
   (v3) and rejected as "not very meaningful — it actually got uglier.
   The data was naturally scattered, and now it kind of looks like a
   polygon."

## What this exemplar EXPLICITLY does NOT do

- Connect points with trajectory lines (P8: 1-2 info dim max)
- Show pseudotime gradient on top of cluster identity (would be 3 info dims)
- Mark bifurcation point with arrow / annotation (extra dim)
- Apply convex-hull / KDE / density-shading to "fill canvas" (rejected)
- Change marker size to compensate for sparse distribution (the
  scatteredness IS the message)

## When to use

For 2D embedding data with discrete cluster identity AND no continuous
secondary information dimension. If the data has a continuous trajectory
(pseudotime, density gradient), use `diffusion_swiss_roll` archetype
instead — that's manifold-as-curve, this is manifold-as-clusters.

## R-future-3 lesson encoded

Honest sparse scatter > artificially filled canvas. When user said
"blowing this thing up is pointless. The data was naturally scattered,
and you've made it look kind of like a polygon — what's the point of
that?" —
the lesson is: do not visually inflate sparse data. Show the data as it is,
let the eye process the empty space.
