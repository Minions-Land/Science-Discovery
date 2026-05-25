# ML-paper plot idioms

**scope**: `ml-paper-only` — load only when (a) the venue is an ML conference (NeurIPS / ICML / ICLR / ACL / CVPR / EMNLP) AND (b) the figure archetype is one of: training-curve (line + error band), ablation grouped-bar, ROC / PRC double-panel, or dual-axis time-series. Do NOT load for life-science / clinical / network / general bar-chart archetypes — the idioms below assume ML conventions (log-loss, seed-mean ± CI bands, AUROC in legend) that misfire elsewhere. (See [[figure-aesthetic-exemplars]] master SKILL.md "Sub-skill scope matching" for the dispatch rule.)

**Provenance**: FigureDraw2 borrow #1 — `ml-paper-writing` arm (Orchestra Research) won 4 fig_types in head-to-head comparison: grouped-bar 23, line-errband 23, 4panel-hero 18, roc-prc 19. Its 67-line SKILL leaned on real ICML/NeurIPS plot scripts. This file captures the imitation targets.

## Training-curve idioms (line + error band)

- **Y-axis**: log-scale for loss (always); linear for accuracy.
- **CI / std band**: `ax.fill_between(x, mean - ci, mean + ci, alpha=0.20, linewidth=0)`. Alpha must be ≤ 0.25 — at 0.30 the band overpowers the mean line at column width.
- **Mean line**: `linewidth = 1.6` (default 1.0 looks anemic at print). Marker on every 5th step is fine; never every step (raster mess).
- **Final-step gap annotation**: when the curves are monotone-converging, drop a small text annotation at the final step showing the gap, e.g. `ax.annotate(f"+{gap:.2f}", xy=(x[-1], ours[-1]), xytext=(8, 0), textcoords="offset points", fontsize=8)`.
- **Legend**: inside the axes, top-right or upper-center. `legend(frameon=False, fontsize=9, loc="upper right")`. Never above the figure (eats vertical space twice).
- **X-axis label**: "Training step", "Epoch", or "Tokens seen ($\\times 10^9$)" — be specific about units.

## Ablation grouped-bar idioms

- **Bar order**: full-method first (anchor), then ablations in the order they remove components, then a baseline at the right edge as a sanity floor. Do NOT alphabetize — the eye should walk the story.
- **Color**: full-method gets the accent color from the palette; every ablation uses a single neutral grey. Don't differentiate ablations by color — they share a category.
- **Width / spacing**: `bar_width = 0.7` of slot; `0.3` gutters. Tighter than this looks dense; wider looks like the data are sparse.
- **Error bars**: only if you have ≥ 3 seeds. Cap-style with `capsize=2.5`. Single-seed numbers go without error bars; the caption must say "single seed".
- **Y-range**: zoom to data — see [[figure-layout-defaults]] §6 for the exact rule. ML papers especially: don't waste 60% of the panel on the 0–best-method gap.
- **Value-label offset — per-bar, NOT max (FD4 evidence: grouped-bar lost layout_density 3→2 because value labels used `max(stds)` as a constant offset, floating high above low-variance bars)**: place each bar's value annotation at `mean[i] + std[i] + small_pad` (e.g., `0.5 * (y_max - y_min) * 0.02`), so the label hugs the top of *its own* error bar, not the tallest bar's error bar. Concretely:
```python
pad = (y_max - y_min) * 0.02
for i, (m, s) in enumerate(zip(means, stds)):
    ax.text(x[i], m + s + pad, f"{m:.2f}", ha="center", va="bottom", fontsize=8)
```
Constant offset is acceptable ONLY when stds are within 1.2× of each other across bars (visually nearly uniform). Otherwise the figure looks like it's hiding low-variance results behind floating labels.

## ROC / PRC double-panel idioms

- **Two side-by-side panels**: `subplots(1, 2, figsize=(8, 3.5))`. Square axes via `set_aspect("equal")` for ROC; default for PRC.
- **Per-method**: AUROC and AP go in the legend label, not in a side table: `f"{method} (AUROC={auroc:.3f})"`.
- **Reference lines**: dashed grey diagonal on ROC (random); dashed grey horizontal at prevalence on PRC. `linestyle="--", color="#888", linewidth=0.8`.
- **Corner labels** ("Random", "Perfect"): only if the panel is hero-sized (figsize ≥ (5, 5)). At column width they clutter.

## Dual-axis time-series idioms

- **Color-couple axis**: each axis spine + ticks + label uses the color of its series. Reader should never have to trace a line back to a tick to know which axis.
```python
color_loss, color_lr = "#0F4D92", "#9A4D8E"
ax1.set_ylabel("Loss (log)", color=color_loss)
ax1.tick_params(axis="y", colors=color_loss)
ax1.spines["left"].set_color(color_loss)
ax2 = ax1.twinx()
ax2.set_ylabel("LR", color=color_lr)
ax2.tick_params(axis="y", colors=color_lr)
ax2.spines["right"].set_color(color_lr)
```
- **Always declare which axis is which in the caption**: "Left axis (blue): validation loss. Right axis (purple): cosine-decay LR schedule."
- **Avoid using both axes for a "more is better" reading** — left axis loss (down=good), right axis LR (down=schedule, no quality semantics) is fine; left axis throughput, right axis accuracy is dangerous because the reader assumes both should rise together.

## Reference scripts (next round of FigureDraw)

The full reference scripts will be added to `gallery/ml-grouped-bar.py`, `gallery/ml-line-errband.py`, `gallery/ml-roc-prc.py`, `gallery/ml-dual-axis-time.py` after FigureDraw3 confirms these idioms produce a measurable win. Do NOT freeze a reference script before behavioural validation — the FigureDraw1+2 lesson is that *real demo code* moves the needle (ml-paper-writing won via 11 real demos, not via SKILL prose).
