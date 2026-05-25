---
slug: academic-plotting
summary: Publication-quality figure standards — rcParams + PALETTE-dict pattern + outside ticks + post-save fonttype-42 verification gate. Layout discipline lives in figure-layout-defaults. Caption checklist + ML-paper idioms + network-graph tuning live in this file from v4.
layer: logical
tools:
version: 5
status: active
supersedes:
references: figure-spec, interactive-figure-prototype, figure-layout-defaults, pdf-vector-layout, figure-chart-atlas, figure-aesthetic-exemplars, caption-revision
provenance: human + SkillTest-R1.A+R1.B-merged + FigureDraw2-evidence (borrow #2/#4 + anti-pattern #1) + FigureDraw3-evidence (4-cell typography-axis cluster failure → mandatory post-save pdffonts check)
---

# Skill — Academic Plotting

Two responsibilities: pick the right tool for the figure shape, and apply venue-grade content discipline. Layout (gridspec, panel hierarchy, no-empty-quadrants) lives in `figure-layout-defaults`.

## When to invoke

- Before every new figure goes into `branches/writer/paper/figures/`.
- When polishing a figure Coder produced — improve readability without changing scientific meaning.
- Before camera-ready, audit every figure against this checklist.

## When NOT to load (route elsewhere)

- Drawing a method overview / pipeline / architecture diagram (boxes-and-arrows) — load [[figure-spec]] instead. This skill assumes numerical axes.
- Producing a hero / Figure-1 conceptual illustration — load [[hero-figure-prompt]] instead. Hero figures use AI image generators with persistent prompts, not matplotlib.
- Compiling an entire paper / writing a multi-figure manuscript — load [[paper-compile]] + [[make-latex-model]] instead. This skill makes ONE figure at a time.
- Surgical edits on an already-compiled PDF (move panel, hide labels, vector-merge two PDFs) — load [[pdf-vector-layout]] instead.
- Picking the right archetype before drawing — load [[figure-chart-atlas]] first; come back here for content discipline.


## Tool by figure shape

| Figure shape | Tool |
|---|---|
| Numerical axes (bars, lines, scatter, heatmap, violin) | matplotlib / seaborn |
| Boxes-and-arrows (architecture, pipeline, workflow, cascade) | diagram tool — see `figure-spec` |

Chart-type-from-data-shape: time / step on x → line; N methods × M benchmarks → grouped bar; single ranking → horizontal bar; two continuous vars → scatter; square matrix → heatmap; proportions → stacked bar (avoid pie in ML papers).

## Content discipline (apply to every script)

### 1. rcParams block at the top

Every plotting script for a paper figure leads with:

```python
import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",     # editable text in SVG
    "pdf.fonttype": 42,         # editable TrueType in PDF
    "ps.fonttype": 42,          # editable TrueType in EPS
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})
```

Editable text in vector outputs is a HARD Nature-family submission requirement. Verify with `grep -c '<text' fig.svg` — 0 means rasterised paths, the figure will be flagged.

**This rcParams block is mandatory on EVERY archetype, with NO exceptions.** FD3 evidence: 4 fig_types (network-graph, ridgeline, stacked-bar, volcano) scored typo=1 / vec=1 *only* because the agent shipped without `pdf.fonttype=42` set. The rules in §1 are correct; the failure is forgetting to apply them on niche archetypes. The lesson: there is no "small enough script to skip rcParams". Even a 30-line gen_figure.py for a single ridgeline must lead with the full rcParams block before any plotting call.

**Mandatory post-save verification.** After `fig.savefig(...)` returns, the script MUST verify the PDF embeds Type-42 (or Type-1) fonts, NOT Type-3 bitmaps. Append this verification block to every gen_figure.py:

```python
import subprocess, sys, pathlib
pdf_path = pathlib.Path("figure.pdf")
out = subprocess.run(["pdffonts", str(pdf_path)], capture_output=True, text=True, check=False)
if "Type 3" in out.stdout:
    sys.stderr.write(f"FATAL: figure.pdf contains Type-3 bitmap fonts; rcParams not honored.\n{out.stdout}\n")
    sys.exit(2)
print(f"[fonttype-check] OK — no Type 3 fonts in {pdf_path}")
```

If `pdffonts` is not installed (rare on macOS / TeX-equipped systems), fall back to a Python-side check:

```python
import re
raw = pdf_path.read_bytes()
if re.search(rb"/Subtype\s*/Type3\b", raw):
    sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
    sys.exit(2)
```

The check is fast (< 100 ms), runs as the last line of every plotting script, and turns a silent typography-axis-1 regression into a hard script failure. **Do not skip it because the figure looks fine** — the typography axis is graded by font selectability, not visual appearance, and a Type-3 figure looks identical to a Type-42 figure in a PNG preview.

**Font unification discipline (R-future-4):** the font stack is set ONCE in this rcParams block and NEVER overridden per element. Every `ax.text`, `ax.annotate`, `ax.set_xlabel`, `ax.set_title`, and `fig.text` call inherits from rcParams — no `fontfamily=`, `fontname=`, or `font=` kwargs anywhere else in the script. This ensures cross-version consistency: if the figure is regenerated by different people or across sessions, the rcParams block is the single source of truth. Pin it in a comment:

```python
# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.
```

### 2. PALETTE-dict pattern, single dict per script

```python
PALETTE = {
    "signal": "#0F4D92",
    "signal_soft": "#B4C0E4",
    "neutral": "#767676",
    "neutral_light": "#D8D8D8",
    "accent": "#E4CCD8",
    "accent_dark": "#9A4D8E",
    "black": "#272727",
}
```

Discipline rule: **green and red are for directional signals only** (gain / loss / up / down / KO-vs-WT). Categorical labels (cluster IDs, condition names without direction) use neutrals — grey + single-blue family + faint pink. A saturated 3-or-4 hue cycle on a cluster sidebar burns the green/red pair on labels that carry no direction.

Default palette: Okabe-Ito `#E69F00 #56B4E9 #009E73 #F0E442 #0072B2 #D55E00 #CC79A7` is colorblind-safe and remains the right starting point when the figure has no directional split.

### 3. Figure size in inches, not millimetres

| Figure | Default figsize (inches) |
|---|---|
| Single panel | `(6, 4)` |
| 2-panel side-by-side | `(10, 4)` |
| 4-panel hero | `(11, 6)` (see `figure-layout-defaults`) |
| Single-column publication | `~3.3"` width |
| Full-width publication | `~7"` width |

Compress to exact mm only at submission packaging stage, AFTER layout is visually confirmed. Leading with `figsize=(width_mm/25.4, height_mm/25.4)` produces unreadable cramming.

### 4. TwoSlopeNorm for diverging colormaps

```python
norm = mpl.colors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
im = ax.imshow(data, cmap="RdBu_r", norm=norm)
```

The zero line on a z-score or log-fold-change heatmap is load-bearing. Do not rely on data-symmetric `vmin/vmax`.

### 5. Outside ticks

```python
ax.tick_params(direction="out", length=2.2, width=0.6)
```

Inside ticks fight the data; outside reads as instrument-style chrome.

### 6. Labels and weights

Axis label 9–10 pt; tick label 8 pt; line width ≥ 1.5 pt; marker size ≥ 5 pt. Reserve one distinct accent color for "our method" / the directional signal of interest.

## Reproducibility

Plotting scripts at `branches/writer/paper/figures/gen_fig_<name>.py` read concrete data files from `branches/coder/exp/` or `branches/shared/exp/exp-<id>/`. No hardcoded numbers. Re-run reproduces byte-identical output modulo font rendering.

Export both formats: `fig.savefig(path.pdf)` for LaTeX inclusion, `fig.savefig(path.png, dpi=300)` for slides / web. Verify LaTeX includes the PDF without font warnings; verify the SVG has non-zero `<text>` nodes.

Each figure ships as: `gen_fig_<name>.py`, `fig_<name>.pdf`, `fig_<name>.png`, plus a one-line provenance docstring citing the source data file.

## Caption checklist (FigureDraw2 borrow #2 — awesome-writing-prompts arm; reviewer_readiness 全场第一)

Before writing `caption.tex`, every figure caption must answer these four in order:

1. **First-sight sentence** — one clause telling the reader what the figure shows in plain language. Not "Method overview". Concrete: "4 methods on 5 reasoning benchmarks; OursModel wins all five".
2. **Take-home number bolded** — the single most important quantitative claim from the figure, set in `\textbf{...}`. If the figure does not have a take-home number, ask whether it should be in the paper at all.
3. **Visual-encoding key** — every non-default visual (hatching, stars, asterisks, dashed line, shaded band, panel letters) gets one phrase explaining what it means. "Error bars: std over 5 seeds. Hatching: greyscale legibility. ★: best per benchmark."
4. **N + statistic** — sample size and the statistic shown (mean, median, ±SD, ±SE, 95% CI). Reviewers will ask if it is missing.

This is a hard pre-export check. Run it before `caption.tex` is committed; reject the caption if any of the four lines is absent. Light enforcement of this rule was the single biggest reviewer_readiness lift in FigureDraw2 (awesome-writing-prompts arm 2.29 vs minionsos 2.13). Fold it back via [[caption-revision]] when the draft is also returned for revision.

## ML-paper idioms (FigureDraw2 borrow #1 — ml-paper-writing arm; 4 fig_type 冠军)

When the target venue is NeurIPS / ICML / ICLR / ACL / CVPR (or the figure type is the standard ML training-curve, ablation-bar, or ROC/PRC double-panel), apply these on top of the rcParams block:

- **Training curves**: y-axis log-scale by default for loss; linear for accuracy. CI shaded band uses `alpha ≤ 0.25`. Lines `linewidth ≥ 1.5pt`. Final-step gap is the headline — annotate it inline if the trend is monotone.
- **ROC / PRC double-panel**: AUROC and AP are reported in the legend, not as a side table. Diagonal reference on ROC; prevalence baseline on PRC. Label "Random" and "Perfect" corners only if the panel is hero-sized.
- **Ablation grouped bars**: legend goes inside the axes (top or bottom-left, away from data). NEVER above the figure or in a side column — it eats the plot area twice. `legend.frameon = False`, `legend.fontsize = 9`.
- **Dual-axis time series**: color-couple axis ticks/spines/labels to the line. Reader must never have to trace a line back to a tick to know which axis it lives on. `ax2.spines['right'].set_color(color2)` plus `ax2.tick_params(colors=color2)` plus `ax2.set_ylabel(..., color=color2)`.
- **Reference exemplars**: see `figure-aesthetic-exemplars/gallery/ml-*.py` for full scripts.

In FigureDraw2, ml-paper-writing arm beat minionsos by 5-6 points on `line-errband` (23 vs 17) and `dual-axis-time` (23 vs 18) primarily because it imitated real ICML/NeurIPS plot scripts. The fix is to bring the same exemplars into our gallery, not to grow this skill.

## Network / graph idioms (FigureDraw2 borrow #4 — scientific-writing-kdense arm; network-graph 冠军)

When drawing a graph / network figure, default to:

- `edge_alpha = 0.30` (dial up to 0.5 only if the graph has fewer than ~50 edges)
- `node_size ∝ degree`, never constant. Constant node size collapses to a hairball at N > 25.
- Community / cluster colors from ColorBrewer Set2 or Dark2 — never from `tab10` (too saturated) and never from any directional palette (no green/red on community labels).
- Use `nx.spring_layout(seed=...)` (or any deterministic force-directed layout). Never `random_layout`. Pin the seed in the script header so the figure is reproducible.
- Edge labels are usually noise — show edge weight only by `linewidth` or `alpha`, not text.

## Pitfalls

- 0 `<text>` nodes in saved SVG — copy-editors cannot edit, venue will flag.
- Saturated 3-or-4 hue cycle on a categorical cluster bar — burns green/red on direction-less labels.
- Hardcoding numbers into plotting scripts — breaks reproducibility and evidence trace.
- Over-decorating: gradients, 3D bars, drop shadows. Reviewer distrust ("if the figure is decorated, what is being hidden?") and venue raster-reproducibility issues.
- Tiny axis labels unreadable at column width.
- Mm-first figsize — drives cramming. Mm conversion is a packaging move.
- Inside ticks fighting the data.
- Diverging cmap without TwoSlopeNorm — zero line drifts off centre by data luck.
