# Scale rescue — when data has > 1 order of magnitude

Provenance: distilled from awesome-writing-prompts "实验绘图推荐" prompt — the "尺度适应性" rule.

When the data points span more than one order of magnitude (e.g., 0–10 vs 70–80, or 1ms vs 1s), a default linear axis collapses the smaller values into invisibility. The fix depends on which property of the data you want to preserve.

## Decision tree

```
Does the data span > 1 order of magnitude on the y-axis?
├── YES, but a single linear axis would still leave both ends readable (≤ 2× ratio)
│   → no rescue, leave linear.
│
├── YES, ratio > 10× and the small values matter
│   ├── Want to preserve absolute-value intuition ("the small one is 8, the big one is 80")?
│   │   → BROKEN AXIS. Two y-ranges with a visible break.
│   │
│   ├── Want to preserve order-of-magnitude relationships ("each step doubles")?
│   │   → LOG AXIS. `ax.set_yscale('log')`.
│   │
│   └── Want to preserve relative improvement ("method A is 12% better than B")?
│       → NORMALIZE. Divide all values by a baseline; plot as ratio.
│
└── NO
    → ignore this file.
```

## Recipe 1 — broken axis

Use for benchmark comparisons where small values exist (e.g., one weak baseline at 5%, others at 70-85%).

```python
from matplotlib.gridspec import GridSpec
fig = plt.figure(figsize=(6, 4))
gs = GridSpec(2, 1, height_ratios=[1, 3], hspace=0.05)
ax_top = fig.add_subplot(gs[0, 0])
ax_bot = fig.add_subplot(gs[1, 0])
ax_top.bar(...)
ax_bot.bar(...)
ax_top.set_ylim(70, 90)
ax_bot.set_ylim(0, 15)
ax_top.spines['bottom'].set_visible(False)
ax_bot.spines['top'].set_visible(False)
ax_top.tick_params(bottom=False)
ax_top.set_xticklabels([])
# Diagonal break marks
d = .015
kwargs = dict(transform=ax_top.transAxes, color='k', clip_on=False, linewidth=0.8)
ax_top.plot((-d, +d), (-d, +d), **kwargs)
ax_top.plot((1-d, 1+d), (-d, +d), **kwargs)
kwargs.update(transform=ax_bot.transAxes)
ax_bot.plot((-d, +d), (1-d, 1+d), **kwargs)
ax_bot.plot((1-d, 1+d), (1-d, 1+d), **kwargs)
```

Must label the break in caption: "Y-axis broken between 15 and 70 to accommodate Method-X."

## Recipe 2 — log axis

Use for training loss, latency benchmarks, scaling laws.

```python
ax.set_yscale('log')
ax.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter())  # 10^2 → 100 in tick labels
ax.set_ylim(bottom=max(0.001, data_min * 0.5))  # sanitize lower bound
```

Must label axis as `Loss (log)` or `Latency (log, ms)` so reader sees the scale immediately.

## Recipe 3 — normalize / relative

Use when the question is "how much better" not "how good".

```python
baseline_value = data['Baseline']
rel_data = {m: v / baseline_value for m, v in data.items()}
ax.bar(methods, [rel_data[m] for m in methods])
ax.axhline(1.0, color='grey', linestyle='--', linewidth=0.6)  # baseline = 1.0
ax.set_ylabel('Relative to Baseline (×)')
```

Must state in caption that values are normalised and against which baseline.

## Anti-pattern

Do NOT:
- Force a linear axis with values that span 0 to 10⁴ — small values become invisible.
- Use log axis on data that includes zero or negatives — log of 0 is undefined.
- Use broken axis on continuous time-series — it suggests discontinuity in the underlying signal.
- Normalize and forget to label — readers will misread "1.12" as a raw value.
