#!/usr/bin/env python3
"""Stage all 136 figure PNGs into reports/assets/ for HTML embed."""
import shutil, pathlib
ROOT = pathlib.Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2")
ASSETS = ROOT/"reports/assets"
ASSETS.mkdir(parents=True, exist_ok=True)
ARMS = ["minionsos","ml-paper-writing","latex-document","academic-paper-imbad",
        "scientific-writing-kdense","stat-writing-fuhaoda","composer-lishix","awesome-writing-prompts"]
FIGS = ["grouped-bar","line-errband","scatter-fit","heatmap","box-violin",
        "4panel-hero","architecture","roc-prc","ridgeline","dual-axis-time",
        "stacked-bar","forest-plot","sankey","volcano","network-graph",
        "latex-table","equation-block"]
copied = 0
missing = []
for fig in FIGS:
    for arm in ARMS:
        runs = sorted((ROOT/"sessions"/arm/fig).glob("2*/workspace/figure.png"))
        if not runs:
            missing.append(f"{fig}/{arm}"); continue
        src = runs[-1]
        dst = ASSETS/f"{fig}__{arm}.png"
        shutil.copyfile(src, dst)
        copied += 1
print(f"OK staged {copied} figure PNGs, {len(missing)} missing")
for m in missing[:20]: print("  miss:", m)
print("Total assets size:", sum(p.stat().st_size for p in ASSETS.iterdir())//1024, "KB")
