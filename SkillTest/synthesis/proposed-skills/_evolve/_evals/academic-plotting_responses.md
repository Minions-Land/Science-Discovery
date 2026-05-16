# Probe — academic-plotting
## Skill role
Write the rcParams block + PALETTE dict for a multi-panel matplotlib script. Decidable: 3 patient cluster IDs are CATEGORICAL (no direction); treatment-vs-control IS directional. The right answer reserves green/red for the directional contrast and uses neutrals (grey + single-blue family) for cluster IDs. Editable text in vector outputs (`svg.fonttype="none"`, `pdf.fonttype=42`) is a hard rule.

## RED
```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 9,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'axes.linewidth': 1.5,
    'lines.linewidth': 1.5,
    'lines.markersize': 5,
    'figure.figsize': (3.3, 2.5),
    'savefig.dpi': 300,
    'savefig.format': 'pdf',
})

PALETTE = {
    'cluster_1': '#E69F00',      # orange
    'cluster_2': '#56B4E9',      # blue
    'cluster_3': '#009E73',      # teal
    'control': '#CCCCCC',        # neutral gray
    'treatment': '#D55E00',      # red-orange (reserved accent for directional contrast)
}
```
Green/red allocation: treatment (upregulation) → red-orange (#D55E00); control baseline → gray. Heatmap uses RdBu_r centered at z=0; red = positive (treatment effect).

## BLUE
```python
import matplotlib as mpl

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

PALETTE = {
    "signal": "#0F4D92",           # treatment (log fold-change direction)
    "signal_soft": "#B4C0E4",
    "neutral": "#767676",          # control baseline
    "neutral_light": "#D8D8D8",
    "cluster_1": "#56B4E9",        # patient clusters (non-directional)
    "cluster_2": "#009E73",
    "cluster_3": "#F0E442",
    "black": "#272727",
}
```
Green/red allocation: red and green are reserved for the diverging heatmap's TwoSlopeNorm (RdBu_r), where red = upregulated and blue = downregulated; patient cluster IDs use the Okabe-Ito colorblind-safe palette (teal, green, yellow) to avoid burning directional colors on non-directional categorical labels.

## GREEN
```python
import matplotlib as mpl

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

PALETTE = {
    "control": "#0F4D92",      # blue for baseline
    "treated": "#E4534D",      # red for treatment effect
    "cluster_1": "#767676",    # neutral grey
    "cluster_2": "#B4C0E4",    # soft blue
    "cluster_3": "#D8D8D8",    # light grey
}
```
Green/red allocation: red encodes positive log fold-change (treatment upregulation); blue encodes the control baseline. Cluster IDs use neutral greys and soft blue to avoid burning directional colors on categorical labels. Heatmap uses TwoSlopeNorm with RdBu_r cmap centered at zero.

## Mapping (DO NOT REVEAL TO JUDGE)
RED = V1_current, BLUE = V2_diff_applied, GREEN = V3_merged

## Right-answer notes for judge
- Hard rule: editable-text rcParams (`svg.fonttype="none"`, `pdf.fonttype=42`) — RED FAILS this hard rule entirely.
- Hard rule: green/red for directional only, neutrals for cluster IDs — RED uses orange + teal + green (Okabe-Ito) on cluster IDs, which assigns saturated hues to direction-less labels (anti-pattern). BLUE uses Okabe-Ito on cluster IDs too (same issue). GREEN uses neutrals only on cluster IDs (correct discipline).
- Diverging heatmap: GREEN explicit about TwoSlopeNorm; BLUE mentions; RED only references RdBu_r.
