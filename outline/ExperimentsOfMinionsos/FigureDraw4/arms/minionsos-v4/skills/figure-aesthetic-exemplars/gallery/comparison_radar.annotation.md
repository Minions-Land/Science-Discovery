# Annotation — comparison_radar

**Source:** figures4papers `figure_VIGIL/figures/comparison_radar.png`.
Real research figure from a multi-method comparison study.

**Archetype:** Polar / radar plot. Multi-axis cross-method comparison.
Use when methods need to be compared on N≥3 metrics simultaneously.

**User grade (R-future-2):** "very beautiful! This figure is genuinely
beautiful — it looks really proper, really professional. The only thing
missing is that the coloured outer stroke around each method polygon
could be a bit thicker."

## Extracted palette

| Hex | % | Role |
|---|---|---|
| `#eaeaea` | 32.4 | background |
| `#c0c0c0` | 20.2 | grey grid (radar axis lines) |
| `#959595` | 17.0 | mid grey |
| `#6a6a6a` | 7.7 | text |
| `#c0eac0` | 3.3 | soft mint (method 1) |
| `#eac0c0` | 3.1 | soft red-pink (method 2) |
| `#c0eaea` | 2.3 | soft cyan (method 3) |
| `#95ea95` | 1.8 | mint signal |
| `#6a95c0` | 1.8 | blue accent |
| `#ea9595` | 1.7 | red signal |

**Critical observation:** **77% grey foreground**, only 23% colour.
The colour is distributed across 3-5 method polygons in soft pastel
tones (`#c0eac0`, `#eac0c0`, `#c0eaea` — all at ~25-30% saturation).

This is the strict execution of Principles 1+2 simultaneously: low
saturation pastels (Principle 2) within a constrained hue family
(Principle 1, mint/red-pink/cyan all on the cool-warm axis with no
saturated colours).

## Why this is "beyond human"

1. **Radar form is naturally information-dense.** N methods × M metrics
   visualised in ONE polygon-overlay. Human matplotlib plotter typically
   uses N separate bar charts (M*N panels) for the same data.

2. **77% grey foreground.** Most amateur radar plots use saturated
   distinct hues for each polygon, fighting visually. This exemplar
   reserves grey for the radar grid + axis labels and gives only the
   polygon outlines + soft fills the small remaining colour budget.

3. **Soft pastels, not full saturation.** Method 1 = `#c0eac0` mint
   pastel, NOT `#00ff00` lime. The colour is identifiable without being
   visually loud.

4. **Radar grid values labelled inline.** The 0.2 / 0.4 / 0.6 / 0.8 / 1.0
   tick labels sit on the radial axis — no separate legend needed for
   the scale.

## User-flagged refinement

> The only thing missing is that the coloured outer stroke around each
> method polygon could be a bit thicker.

**Fix:** in matplotlib polar, set the polygon outline `linewidth=2.0`
or `2.5` instead of default `1.0`. The pastel fill is so pale that the
polygon boundary needs MORE stroke weight, not less, to read as a
distinct shape.

```python
ax.fill(theta, values, color=method_color, alpha=0.25)
ax.plot(theta, values, color=method_color, linewidth=2.2)  # was 1.0; bump for pastel fill
```

This is a Principle 2 EXCEPTION: when fill saturation is low, stroke
weight must compensate. Without stroke compensation, the polygon
outline gets visually lost.

## What makes this beyond-human

Standard plotters reach for:
- Multi-bar charts (N*M panels for N methods × M metrics) — wastes canvas
- Stacked bar (everything in one bar) — unreadable when M>4
- Heatmap (methods × metrics) — loses the "shape signature" each method has

The radar form gives each method a distinctive POLYGON SHAPE which is
easy to remember and compare. "Method 1 has a tall thin polygon vs
Method 2 has a balanced polygon" is information you cannot get from
a bar chart.

## Recommended use

When your data is N methods × M metrics with M ≥ 3, default to radar
form FIRST. Apply the soft-pastel + grey-dominant palette. Bump
polygon stroke to 2-2.5px to compensate for low fill saturation.
