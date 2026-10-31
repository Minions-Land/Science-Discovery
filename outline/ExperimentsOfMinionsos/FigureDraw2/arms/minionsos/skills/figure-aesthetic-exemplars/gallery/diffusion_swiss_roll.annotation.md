# Annotation — diffusion_swiss_roll

**Source:** figures4papers `figure_Cflows/figures/diffusion_swiss_roll.png`.
Real research figure from a continuous-flow generative model paper.

**Archetype:** Manifold visualisation. The data's geometric structure
IS the visual subject. Use when your data has natural 2D / 3D structure
that bar / line / heatmap would flatten.

**User grade (R-future-2):** "the right side is very good-looking, this
figure is really well done... the spiral plot looks great, the palette is
also nice. I think the entire manifold series is solid."

## Extracted palette

| Hex | % | Role |
|---|---|---|
| `#15c0c0` | 9.5 | signal cyan (primary manifold) |
| `#15eac0` | 8.9 | signal mint-cyan (secondary manifold) |
| `#15c095` | 6.5 | signal mid (transition gradient) |
| `#15eaea` | 4.1 | signal pale cyan |
| `#95c0c0` | 4.6 | washed cyan (background data) |
| `#9595c0` | 3.8 | accent purple-blue |
| `#6a9595` | 3.8 | dark teal |
| `#c0c0c0` / `#eaeaea` | 24.0 | neutral background (combined) |
| `#959595` | 2.7 | text |

**Critical observation:** **Pure cyan-teal hue family.** All non-grey
foreground pixels are within a 60° arc on the colour wheel
(cyan 180° ↔ teal-mint 165° ↔ purple-cyan 200°). NO red, NO orange,
NO complementary opposite. The figure achieves Principle 1 (hue coherence)
strictly — one hue family carrying ALL information.

The visual hierarchy comes from saturation gradient WITHIN the cyan
family (deep `#15c0c0` for hot signal, washed `#95c0c0` for context).
Not from hue contrast.

## Why this works (user-confirmed)

1. **Geometric structure is the message.** The swiss roll's 3D-to-2D
   manifold IS the data; flattening it to a bar chart would lose 80%
   of the information. The form matches what the data IS.

2. **Pure hue family.** 100% within cyan-teal. The eye doesn't have to
   resolve "what does red mean vs blue mean" — there's only one signal.

3. **Saturation gradient within hue.** 4 levels of cyan from `#15c0c0`
   (75% sat) down to `#95c0c0` (15% sat) carry the temporal / density
   information without breaking hue coherence.

4. **High info density.** Every pixel of the manifold carries data —
   no wasted whitespace, no decorative elements. The "effective display
   area" Principle 3 is at maximum.

5. **No legend needed.** The cyan-saturation gradient is self-
   explaining: deeper = more, lighter = less. A legend block would be
   visual cost without information gain.

## What makes this beyond-human

A human matplotlib plotter typically:
- Reaches for `cmap='viridis'` or `cmap='plasma'` for manifolds
- Overlays a black-on-white axis grid that competes with the data
- Adds a legend block claiming canvas space
- Uses default tick labels at default density

This figure: explicit cyan-family palette with controlled saturation
gradient; minimal axis chrome (axis is barely visible); no legend; full
canvas given to the manifold.

## Diff against your figure (R-future-2 use)

If your manifold figure looks "rule-correct but bland" against this
exemplar, the most likely deltas:
- You're using `cmap='viridis'` (default) — 3-hue family. Switch to a
  single-hue `LinearSegmentedColormap` from a single signal hue.
- Your axis ticks are at default density — reduce to 2-3 per axis.
- Your figure has a colourbar legend block — make it inline (small bar
  in figure corner) or drop entirely if the saturation gradient is
  self-explaining.
