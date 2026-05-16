---
slug: academic-plotting
summary: Standards for publication-quality figures — matplotlib for numerical axes, diagram tools for structure, venue-standard styling, colorblind-safe palette, vector + raster outputs.
layer: logical
tools:
version: 3
status: active
supersedes:
references: figure-spec, interactive-figure-prototype, figure-layout-defaults
provenance: human + SkillTest-R1.A+R1.B
---

# Skill — Academic Plotting

Numbers → matplotlib; structure → diagram. Then style to venue, highlight "our method" deliberately, ship vector + raster reproducibly from a checked-in script.

## When to invoke

- Before every new figure goes into `branches/writer/paper/figures/`.
- When polishing a figure Coder produced — improve readability without changing scientific meaning.
- Before camera-ready, audit every figure against this checklist.

## Structure

Tool choice by figure shape:

| Figure shape | Tool |
|---|---|
| Numerical axes (bars, lines, scatter, heatmap, violin) | matplotlib / seaborn |
| Boxes-and-arrows (architecture, pipeline, workflow, cascade) | diagram tool — see `figure-spec` |

Chart-type-from-data-shape: time / step on x → line; N methods × M benchmarks → grouped bar; single ranking → horizontal bar; two continuous vars → scatter; square matrix → heatmap; proportions → stacked bar (avoid pie in ML papers).

Publication defaults: font matching venue (Times / Computer Modern for most; sans-serif if allowed); axis label 9–10 pt; tick label 8 pt; line width ≥ 1.5 pt; marker size ≥ 5 pt; figure size single-column ~3.3", full-width ~7". Colorblind-safe palette default: Okabe-Ito `#E69F00 #56B4E9 #009E73 #F0E442 #0072B2 #D55E00 #CC79A7`. One distinct accent reserved for "our method".

## Procedure

1. **Classify the figure** (numerical axes vs structure).
2. **Pick the chart type from data shape** per the table above.
3. **Apply rcParams discipline FIRST** in any plotting script:
   ```python
   import matplotlib as mpl
   mpl.rcParams.update({
       "font.family": "sans-serif",
       "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
       "svg.fonttype": "none",     # editable text in SVG (NOT rasterised paths)
       "pdf.fonttype": 42,         # editable TrueType in PDF
       "axes.spines.right": False,
       "axes.spines.top": False,
       "axes.linewidth": 0.8,
       "legend.frameon": False,
   })
   ```
   Editable text in vector outputs is a HARD submission requirement for Nature-family venues. Rasterised text is not editable by copy-editors and will be flagged.

4. **Apply publication defaults** (font sizes, line widths, figure dimensions in INCHES, not millimetres).
   - Single panel: `figsize=(6, 4)` inches.
   - 2-panel side-by-side: `figsize=(10, 4)`.
   - 4-panel hero: `figsize=(11, 6)` (see `figure-layout-defaults`).
   Compress to exact mm only at submission packaging stage, AFTER the layout has been visually confirmed in PNG preview.

5. **Define a single PALETTE dict at the top of any multi-panel script.** Thread it through every panel:
   ```python
   PALETTE = {
       "signal": "#0F4D92",       # intervention / treatment / KO direction
       "signal_soft": "#B4C0E4",  # subordinate signal
       "neutral": "#767676",      # control / WT / non-direction
       "neutral_light": "#D8D8D8",
       "accent": "#E4CCD8",       # secondary discriminator
       "accent_dark": "#9A4D8E",
       "black": "#272727",
   }
   ```
   Reserve **green and red for directional signals only** (gain / loss / up / down). Use neutrals (grey, single-blue family, faint pink, faint purple) for non-directional categorical labels. Do NOT use a saturated 3-or-4 hue cycle for a cluster sidebar or category labels — it burns the green/red pair on labels that don't carry direction.

6. **Use TwoSlopeNorm for any diverging colormap** (RdBu_r, BrBG, PiYG, etc):
   ```python
   norm = mpl.colors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
   im = ax.imshow(data, cmap="RdBu_r", norm=norm)
   ```
   The zero line on a z-score or log-fold-change heatmap is load-bearing; do NOT rely on `vmin/vmax` symmetry by data luck.

7. **Outside-tick discipline:**
   ```python
   ax.tick_params(direction="out", length=2.2, width=0.6)
   ```
   Inside ticks fight the data; outside ticks read as instrument-style chrome.

8. **Keep plotting scripts checked in.** `branches/writer/paper/figures/gen_fig_<name>.py` reads from a concrete data file under `branches/experimenter/experiments/` or `artifacts/exp-{id}/`. No hardcoded numbers. Re-run reproduces byte-identical output modulo font rendering.

9. **Export both formats.** `fig.savefig(path.pdf)` for LaTeX inclusion; `fig.savefig(path.png, dpi=300)` for slide / web reuse. Verify LaTeX includes the PDF without font warnings, and verify the SVG has non-zero `<text>` nodes.

Each figure ships as: `gen_fig_<name>.py`, `fig_<name>.pdf`, `fig_<name>.png`, plus a one-line provenance docstring citing the source data file.

## What this skill does NOT cover

Multi-panel layout (4-panel hero default, no empty quadrants, no over-stretched panels, layout-budget triage) lives in `figure-layout-defaults`. This skill covers content discipline (palette, fonts, ticks, vector output); layout discipline lives separately.

## Pitfalls

- Auto-generated defaults (blue / orange / green) that are not colorblind-safe.
- Hardcoding numbers into plotting scripts — breaks reproducibility and evidence trace.
- Over-decorating: gradients, 3D bars, drop shadows. The consequence is reviewer distrust ("if the figure is decorated, what is being hidden?") and venue rejection on raster reproducibility — flat beats fancy.
- Tiny axis labels unreadable at column width.
- Saving SVG without `svg.fonttype="none"` — text is rasterised to path geometry; copy-editors cannot edit.
- Leading with `figsize=(width_mm/25.4, height_mm/25.4)` — produced unreadable cramming in SkillTest fixtures. Mm conversion is a packaging-stage move, not a draft-stage move.
- Burning green/red on a categorical cluster bar that has no direction — that pair belongs on directional signals only.
