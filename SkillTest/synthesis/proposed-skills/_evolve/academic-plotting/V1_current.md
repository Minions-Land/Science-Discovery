---
slug: academic-plotting
summary: Standards for publication-quality figures — matplotlib for numerical axes, diagram tools for structure, venue-standard styling, colorblind-safe palette, vector + raster outputs.
layer: logical
tools:
version: 2
status: active
supersedes:
references: figure-spec, interactive-figure-prototype
provenance: human
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
3. **Apply publication defaults** (font, sizes, line widths, figure dimensions).
4. **Use colorblind-safe palettes** with one reserved accent for "our method".
5. **Keep plotting scripts checked in.** `branches/writer/paper/figures/gen_fig_<name>.py` reads from a concrete data file under `branches/experimenter/experiments/` or `artifacts/exp-{id}/`. No hardcoded numbers. Re-run reproduces byte-identical output modulo font rendering.
6. **Export both formats.** `fig.savefig(path.pdf)` for LaTeX inclusion; `fig.savefig(path.png, dpi=300)` for slide / web reuse. Verify LaTeX includes the PDF without font warnings.

Each figure ships as: `gen_fig_<name>.py`, `fig_<name>.pdf`, `fig_<name>.png`, plus a one-line provenance docstring citing the source data file.

## Pitfalls

- Auto-generated defaults (blue / orange / green) that are not colorblind-safe.
- Hardcoding numbers into plotting scripts — breaks reproducibility and evidence trace.
- Over-decorating: gradients, 3D bars, drop shadows. The consequence is reviewer distrust ("if the figure is decorated, what is being hidden?") and venue rejection on raster reproducibility — flat beats fancy.
- Tiny axis labels unreadable at column width.
