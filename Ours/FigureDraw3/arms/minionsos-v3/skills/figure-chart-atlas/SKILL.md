---
slug: figure-chart-atlas
summary: 19-archetype catalog mapping data shape → chart type → matplotlib idiom. Pre-plotting decision skill — pick archetype here, then go to academic-plotting for content discipline. Includes non-skippable rcParams + Type-42 preamble that fires for every archetype.
layer: logical
tools:
version: 2
status: active
supersedes:
references: academic-plotting, figure-aesthetic-exemplars, figure-spec
provenance: FigureDraw2-evidence (borrow synthesized from awesome-writing-prompts "实验绘图推荐" + nature-figure chart-atlas) + FigureDraw4-evidence (Action 11: scatter-fit + sankey skipped academic-plotting and lost typography+vector_fidelity — rcParams preamble now mandatory at atlas level)
---

# Skill — Figure Chart Atlas

When the data is in hand but the figure type is not yet decided, this is the first stop. The atlas catalogs 19 publication-quality archetypes and tells you which one fits the data shape and the scientific question. After the archetype is chosen, hand off to [[academic-plotting]] for content discipline (rcParams, palette, layout) and [[figure-aesthetic-exemplars]] for visual polish.

This skill is index-only. The 19 archetypes are documented in `references/19-archetypes.md`; rescue rules for tricky data scales (huge dynamic range, log-spread, normalised view) are in `references/scale-rescue.md`.

## NON-SKIPPABLE PREAMBLE — every gen_figure.py starts here

**Regardless of which archetype you pick — even a plain scatter-fit, even a stylised sankey, even a single-line training curve — `gen_figure.py` MUST start with the [[academic-plotting]] rcParams block AND end with the post-save Type-42 verification.** Do NOT skip these two gates because the figure "looks simple" or because you're using `matplotlib.patches` directly without standard plotting calls. The matplotlib PDF backend silently embeds Type-3 bitmap fonts unless `pdf.fonttype=42` is set, and a Type-3 PDF scores 0 on `vector_fidelity` and 1 on `typography` regardless of how good the figure looks visually.

**FD4 evidence**: scatter-fit dropped from v3 24/24 to v4 17/24 (-7) and sankey dropped from v3 23/24 to v4 18/24 (-5) because the agent judged "this is a trivial archetype, I don't need the full rules" and skipped `academic-plotting`. Both PDFs shipped with Type-3 fonts. Neither archetype is exempt from rcParams discipline.

The required preamble template (copy verbatim from [[academic-plotting]] §1):

```python
import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})
```

Plus the post-save check that fails the script if Type-3 leaked through:

```python
import subprocess, sys, pathlib
out = subprocess.run(["pdffonts", "figure.pdf"], capture_output=True, text=True, check=False)
if "Type 3" in out.stdout:
    sys.stderr.write(f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{out.stdout}\n")
    sys.exit(2)
```

A figure script that doesn't open with rcParams and doesn't end with the Type-42 check is not ready to ship — full stop. There is no archetype where this preamble is optional.

## When to invoke

- Before drafting a new figure, when the chart type is not obvious.
- When a reviewer asks "could you show this as a different plot?" — the atlas is the menu.
- During paper outlining, when figure slots need to be filled with archetypes that match each section's claim.

## When NOT to invoke

- Architecture / pipeline diagrams — that is [[figure-spec]]'s archetype-A.
- Hero / Figure-1 illustrations — that is [[hero-figure-prompt]].
- A figure whose archetype is already obvious (training curve → line+errband, ablation → grouped bar). Just go to [[academic-plotting]] directly.

## The four archetype families

| Family | Archetypes | When |
|---|---|---|
| **Numerical comparison** | grouped-bar · horizontal-bar · pareto-frontier · radar · stacked-bar | N methods × M metrics, or N points × 2 traded-off metrics |
| **Trend / convergence** | line+errband · zoomed-inset · scatter-fit | x is time / step / scale; want to show direction or law |
| **Classifier / matrix** | ROC · PRC · heatmap · scatter-vs-truth · bubble | binary classifier evaluation OR matrix data (confusion / similarity) |
| **Distribution / structure** | violin · box · ridgeline · pie/donut · sankey · network · forest · volcano | distribution comparison, flow, or structured relationships |
| **Composite layout** | dual-axis · bar+line · faceted-grid | mixed quantities or too many to fit one panel |

Full guidance per archetype — when to use, when NOT, the matplotlib / seaborn / `figure-spec` route, and the typical pitfall — lives in `references/19-archetypes.md`. Open that file when picking an archetype.

## Procedure

1. **State the scientific question in one sentence.** "Does Method A converge faster than Method B?" / "Are the four conditions distributionally distinct?" / "How does score scale with parameters?"
2. **Identify the data shape.** Number of variables, are they continuous or categorical, is there a directional axis (time / scale), is there structure (matrix, graph, flow)?
3. **Open `references/19-archetypes.md`** and find the archetype matching the (question, shape) pair. The reference recommends 1-2 archetypes per question; pick the simpler one unless the data demands otherwise.
4. **Check `references/scale-rescue.md`** if data has > 1 order-of-magnitude dynamic range (recommends broken axis vs log axis vs normalisation).
5. **Hand off** to [[academic-plotting]] with the archetype and scale decision in hand. Note the archetype choice in `gen_figure.py`'s docstring — provenance trail.

## Pitfalls

- Picking an archetype because it "looks fancy" (radar, sankey) when a humble bar would do. The reviewer will ask why.
- Skipping the scale-rescue step on data that spans 0–10 vs 70–80 — produces an unreadable bar plot.
- Using a pie / donut chart in an ML paper. Almost always wrong; recommended only for proportion data with ≤ 4 slices and large differences. Default to stacked bar.
- Picking an archetype before stating the question. The chart should serve the claim, not the other way around.
