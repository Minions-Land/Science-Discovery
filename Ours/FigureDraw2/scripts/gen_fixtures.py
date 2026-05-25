#!/usr/bin/env python3
"""Generate FigureDraw2 fixtures: copy 15 existing + add latex-table, equation-block, paper-page."""
import shutil, pathlib, json, random
random.seed(11)
SRC = pathlib.Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2/fixtures")
DST = pathlib.Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2/fixtures")
DST.mkdir(parents=True, exist_ok=True)

FIGS = ["grouped-bar","line-errband","scatter-fit","heatmap","box-violin",
        "4panel-hero","architecture","roc-prc","ridgeline","dual-axis-time",
        "stacked-bar","forest-plot","sankey","volcano","network-graph"]
for fig in FIGS:
    s = SRC/fig
    d = DST/fig
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(s, d)
print("OK copied", len(FIGS), "fixtures")

# === New fixture: latex-table ===
latex_dir = DST/"latex-table"
latex_dir.mkdir(exist_ok=True)
ltex_brief = """# Fixture: latex-table

## Task
Produce a publication-quality booktabs comparison table comparing 4 methods on 5 metrics, render it as a standalone PDF (figure.pdf) AND save the underlying LaTeX source as table.tex. Then also produce figure.png by rasterizing the PDF.

## Inputs
- data.json: {methods, metrics, values[method][metric] = {mean, std}, units[metric]}
- All values are realistic ML benchmark numbers.

## Outputs (cwd)
- figure.pdf, figure.png  (the rendered table as a single-page PDF + raster preview)
- table.tex   (the standalone .tex source - must compile with pdflatex)
- caption.tex (the LaTeX caption text only)
- gen_figure.py  (the script that produced figure.pdf - should call pdflatex on table.tex)

## Hints
- Use booktabs (\\toprule, \\midrule, \\bottomrule). NO vertical lines.
- Bold the best per column. If a method has highest mean and overlaps with another within 1 std, bold both.
- mean +/- std formatting: "$72.4_{\\pm 1.2}$" subscript style is preferred for camera-ready compactness.
- Add a column-spanning grouping if methods naturally fall into baseline / ours.
- Caption should explain bold convention and seed count.
"""
(latex_dir/"brief.md").write_text(ltex_brief, encoding="utf-8")

methods = ["Baseline","Method-A","Method-B","OursModel"]
metrics = ["MMLU","HumanEval","GSM8K","MATH","GPQA"]
base = {
    "Baseline":  [65.4, 48.2, 72.1, 31.5, 36.4],
    "Method-A":  [71.0, 55.6, 78.3, 37.2, 41.8],
    "Method-B":  [73.5, 59.4, 80.7, 39.8, 44.1],
    "OursModel": [76.8, 64.7, 84.2, 44.6, 49.3],
}
values = {}
for m in methods:
    values[m] = {}
    for i, b in enumerate(metrics):
        values[m][b] = {"mean": base[m][i], "std": round(random.uniform(0.6, 2.4), 2)}
units = {}
for m in metrics:
    units[m] = "%"
ltex_data = {"methods": methods, "metrics": metrics, "values": values, "n_seeds": 5,
             "units": units,
             "groups":[{"label":"baselines","members":["Baseline","Method-A","Method-B"]},
                        {"label":"ours","members":["OursModel"]}]}
(latex_dir/"data.json").write_text(json.dumps(ltex_data, indent=2)+"\n", encoding="utf-8")

# === New fixture: equation-block ===
eq_dir = DST/"equation-block"
eq_dir.mkdir(exist_ok=True)
eq_brief = """# Fixture: equation-block

## Task
Produce a single-page "derivation block" - render 3 numbered display equations with derivation chain, plus surrounding prose that cross-references them. Output as figure.pdf (a real PDF rendered by pdflatex from your equations.tex) plus figure.png raster.

The content is RetroDiff's training objective derivation:
  1. Variational lower bound (ELBO) of the diffusion model
  2. Decomposition into reconstruction + KL terms
  3. The retrieval-augmented variant (the new contribution): conditioning on retrieved exemplars

This tests both LaTeX math typesetting AND mathematical typography (align, cases, qed-style derivations, equation numbering, \\eqref).

## Inputs
- claim.json: {variables, equations, prose_hints}
  variables tells you what each symbol stands for; equations are the canonical TeX source for each numbered equation.

## Outputs (cwd)
- figure.pdf, figure.png   (a single-page PDF rendered from the equations + prose)
- equations.tex            (the standalone .tex with the three numbered equations + prose)
- caption.tex              (the LaTeX caption)
- gen_figure.py            (calls pdflatex)

## Hints
- Use align or align* environments; number equations with \\label{eq:...}.
- Cross-reference with \\eqref{eq:...}.
- Variables should be italic (default LaTeX behaviour); operators (log, KL) upright.
- Use \\mathbb{E}, \\mathcal{L}, \\mathrm{KL} for stylistic distinctions.
- The prose between equations should describe the derivation step, not just say "by Jensen".
"""
(eq_dir/"brief.md").write_text(eq_brief, encoding="utf-8")

eq_data = {
    "system_name": "RetroDiff",
    "variables": [
        {"symbol": "x", "meaning": "clean data sample"},
        {"symbol": "x_t", "meaning": "noised version of x at diffusion step t"},
        {"symbol": "R(x)", "meaning": "set of k retrieved exemplars conditioned on x"},
        {"symbol": "theta", "meaning": "model parameters"},
        {"symbol": "q", "meaning": "forward noising distribution"},
        {"symbol": "p_theta", "meaning": "learned reverse distribution"},
        {"symbol": "T", "meaning": "total diffusion steps"},
    ],
    "equations": [
        {"label": "eq:elbo",
         "latex": "\\log p_\\theta(x) \\geq \\mathbb{E}_{q(x_{1:T}|x)}\\!\\left[\\log\\frac{p_\\theta(x_{0:T})}{q(x_{1:T}|x)}\\right] = -\\mathcal{L}_{\\mathrm{ELBO}}"},
        {"label": "eq:decomp",
         "latex": "\\mathcal{L}_{\\mathrm{ELBO}} = \\underbrace{\\mathbb{E}_q[-\\log p_\\theta(x_0|x_1)]}_{\\text{reconstruction}} + \\sum_{t=2}^{T} \\underbrace{\\mathrm{KL}\\!\\left(q(x_{t-1}|x_t,x) \\,\\|\\, p_\\theta(x_{t-1}|x_t)\\right)}_{\\text{step-}t \\text{ denoising}}"},
        {"label": "eq:retro",
         "latex": "\\mathcal{L}_{\\mathrm{RetroDiff}}(\\theta) = \\mathbb{E}_{x \\sim p_{\\mathrm{data}}}\\!\\left[\\mathcal{L}_{\\mathrm{ELBO}}\\!\\left(x \\,\\big|\\, R(x)\\right)\\right]"}
    ],
    "prose_hints": [
        "Equation 1 is the standard ELBO; the inequality is by Jensen.",
        "Equation 2 is the canonical decomposition - reconstruction + per-step KL.",
        "Equation 3 is RetroDiff's contribution: the per-sample objective is conditioned on a retrieved exemplar set R(x)."
    ]
}
(eq_dir/"claim.json").write_text(json.dumps(eq_data, indent=2)+"\n", encoding="utf-8")

# === paper-page seed (figs assembled per arm later) ===
pp_dir = DST/"paper-page"
pp_dir.mkdir(exist_ok=True)
shutil.copyfile(SRC/"paper-page/brief.md", pp_dir/"brief.md")
shutil.copyfile(SRC/"paper-page/claim.json", pp_dir/"claim.json")
print("OK new fixtures: latex-table, equation-block, paper-page seeded")

import os
for d in sorted(os.listdir(DST)):
    p = DST/d
    if p.is_dir():
        print("  ", d, sorted(os.listdir(p)))
