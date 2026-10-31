# Skill-Forge changelog — FigureDraw3 → FigureDraw4

**Date**: 2026-05-25
**Driver**: FigureDraw3 self-eval (single-arm `minionsos-v3` vs FD2 `minionsos` anchor) — 19 figures + 1 paper-page, with 3 regressions identified in `FigureDraw3/reports/NEXT_FORGE_PLAN.md`.

## What FD3 won (kept untouched in FD4)

- Common-17 average **18.71 → 21.18** (+2.47, +13.2%)
- typography +0.89, vector_fidelity +0.88, palette +0.62
- 5 fig_types now max 24/24 (grouped-bar, scatter-fit, forest-plot, heatmap-class, plus the new `cns-graphical-abstract` 22/24)

These wins came from the FigureDraw2 → FigureDraw3 Forge:

- `figure-aesthetic-exemplars/SKILL.md` paradigm — gallery diff + iteration
- `figure-chart-atlas/` 19-archetype reference (Family A-E)
- `cns-paper-discipline/` umbrella with imrad / reporting-guidelines / graphical-abstract sub-refs
- `caption-revision.md` adversarial-pass loop
- macro-discipline lint in `paper-compile`
- Sankey source-color consistency rule in `figure-spec`

The FD4 changes are **regression repair only**, not paradigm churn. Nothing in the wins-list above was rewritten.

## What FD4 changed (5 actions)

### Action 1 — network-graph-tuning opt-in gate

Added `scope: graph-network-only` header. Rule set now applies only when archetype is network/graph AND `len(G.nodes) >= 20`.

Replaced unconditional `node_size ∝ degree` with degree-conditional rule: scale only when `max_degree / min_degree > 3`; otherwise constant `node_size = 120`. The FD3 fixture had `ratio ≈ 1.5` which produced near-identical bubbles — proportional sizing on a flat-degree graph kills hierarchy worse than constant sizing.

Layout iterations now scale with node count: 100 for ≤ 50 nodes, 200 for 50-100. Caption requirements extended to declare which `node_size` mode was used.

**File**: `minions/roles/writer/skills/figure-aesthetic-exemplars/network-graph-tuning.md`
**Mirror**: `FigureDraw3/arms/minionsos-v3/skills/figure-aesthetic-exemplars/network-graph-tuning.md` (synced)

### Action 2 — figure-aesthetic-exemplars `scope:` field + dispatch table

Added `scope:` declaration to `ml-paper-idioms.md` (`ml-paper-only`) and `network-graph-tuning.md` (`graph-network-only`). Master `SKILL.md` now carries a "Sub-skill scope matching" section with a 3-row dispatch table — agent must match `scope:` against figure archetype + venue *before* loading a sub-ref.

**File**: `minions/roles/writer/skills/figure-aesthetic-exemplars/{SKILL.md, ml-paper-idioms.md, network-graph-tuning.md}`
**Version bump**: `figure-aesthetic-exemplars` v2 → v3

This is the structural fix for the FD3 misfire where stacked-bar was hit by ColorBrewer Set2 rules from network-graph-tuning. The agent could already see the rule was meant for graphs, but the SKILL didn't tell it *not to apply* outside that scope.

### Action 3 — volcano annotation discipline

In `figure-chart-atlas/references/19-archetypes.md`, replaced the loose "annotate top hits" pitfall with explicit budget rules: 3-5 labels max if visually well-separated; 3-up + 3-down extremes if cluster-y; hard cap at 10. Required use of `adjustText` or hand-tuned offsets for ≥ 5 labels.

**File**: `minions/roles/writer/skills/figure-chart-atlas/references/19-archetypes.md`

### Action 4 — caption-revision don't-modify-figure

Caption-revision was the proximal cause of volcano's -4 in FD3 — the reviewer-pass added inline labels to the figure. Skill now scoped explicitly to *caption text only*; figure-shape problems must escalate to `academic-plotting` / `figure-spec` / `figure-chart-atlas`, not be patched with in-figure annotation.

**File**: `minions/roles/writer/skills/caption-revision.md`
**Version bump**: `caption-revision` v1 → v2

### Action 5 — regression-core evals subset

New 5-cell evals subset at `FigureDraw4/evals/regression-core.txt`: `stacked-bar`, `volcano`, `network-graph` (the three regressions) + `4panel-hero`, `sankey` (anchors that were strong in FD3 — drift here means a fix bled into adjacent cells).

Driver script `FigureDraw4/scripts/regression_core_diff.py` runs the 5 cells, sums 8-axis grader scores, diffs against `FigureDraw3/grader/_aggregate.json::v3_per_fig`, and exits non-zero if any cell drops ≥ 3 vs baseline. Run this **before** any broader sweep to catch SKILL-change bleed.

### Action 6 — imrad-discipline output-format

`cns-paper-discipline/references/imrad-discipline.md` ends with a new "Output-format discipline (figure of record)" section that cross-links to `paper-compile` (Type-1 fonts, macro lint, vector-fidelity check) and `latex-typography` (booktabs grouping, dash discipline). The FD3 imrad-section scored 19/24 with `typography = 2 / vector_fidelity = 2` because the prose was correct but the rendered PDF had Type-3 fonts and no macros.

**File**: `minions/roles/writer/skills/cns-paper-discipline/references/imrad-discipline.md`

## Deferred to FD5 (per NEXT_FORGE_PLAN.md)

- **Action 7** — sub-skill split of `cns-paper-discipline` by venue (Cell / Nature / NEJM). The single `imrad-discipline.md` file is at ~150 lines and adding more evidence will push it past the readable budget. Wait until FD4 has fresh evidence to decide which venue distinctions actually matter.

## What to test

1. Mirror updated skills to `FigureDraw4/arms/minionsos-v4/skills/` (same layout as v3 sandbox).
2. Run `regression-core` 5 cells, then grade.
3. Run the rest of the FD3 19-cell + paper-page on the v4 arm.
4. Re-run aggregate to confirm: regressions recover (stacked-bar ≥ 19, volcano ≥ 22, network-graph ≥ 19) AND no new -3 drops on the 14 untouched cells.

## Mid-FD4 additions (8-10) — discovered during regression-core launch

After Actions 1-6 landed, an FD3 evidence audit revealed that 4 of 17 cells (ridgeline, stacked-bar, volcano, network-graph) all clustered at typo=1/vec=1 because of the same Type-3 font failure mode. The agent applied `pdf.fonttype=42` correctly on common archetypes but forgot it on niche ones. Three more actions added:

### Action 8 — `academic-plotting.md` post-save fonttype=42 verification gate (v4 → v5)

Added `ps.fonttype: 42` to the rcParams block. More importantly, added a mandatory **post-save Python verification block** that runs `pdffonts` (or a byte-scan fallback for `/Type3`) on every saved PDF; if Type-3 is detected, the script `sys.exit(2)`. Turns a silent typography regression into a hard script failure. FD4 first-3 cells confirmed: every PDF now embeds CID TrueType (Type-42), no Type-3 anywhere.

### Action 9 — Ridgeline palette discipline in `figure-chart-atlas/references/19-archetypes.md`

FD3 ridgeline used `RdYlBu_r` (yellow midpoint = colorblind-unsafe band right where the eye compares cluster shapes). New rule: **default to perceptually-uniform sequential palette (viridis / cividis / mako)**. Diverging palette only when groups have a true zero / midpoint where direction reverses. Never `RdYlBu_r`.

### Action 10 — Stacked-bar palette + legend discipline

FD3 stacked-bar used seaborn defaults (red+green adjacent — colorblind fail) and put the legend outside the axes (wasted right margin). New rules: **Tableau-10 or Okabe-Ito explicit `colors=` argument**, and **legend INSIDE the axes** unless ≥ 6 stack layers or visible overlap with the tallest bar. Layer order in legend must match stack order, not alphabetical.

## What FD4 produced (regression-core gate, ahead of grading)

- All 6 cells produced `figure.{pdf,png,svg}` + `caption.tex` + `gen_figure.py` in ~4 min wall-clock.
- All 6 PDFs embed CID TrueType (Action 8 verified working).
- Network-graph applied degree-conditional `node_size` rule and the seed=42, iterations=100 layout from Action 1.
- Volcano had only 3 annotations (Action 3 worked; FD3 had >5 with collisions).
- Ridgeline used a sequential blue gradient (Action 9 worked; no RdYlBu_r yellow midpoint).
- **Stacked-bar (first run, before Action 10) shipped legend outside axes — re-run launched after Action 10 mirror**.

## To do

- Wait for grader (regression_core_diff vs FD3 baseline + best-of-baselines)
- Run aggregate.py
- Triage any remaining gaps; if all clean, fold Action 11+ into FD5 (ride the win-train, sub-skill split)

## Late-FD4 actions (11-14) — discovered during full sweep

### Action 11 — `figure-chart-atlas/SKILL.md` v1 → v2: NON-SKIPPABLE PREAMBLE

FD4 first sweep: scatter-fit and sankey both shipped Type-3 PDFs because the agent skipped `academic-plotting`, judging "trivial archetype, no rules needed." Atlas SKILL.md now leads with a non-skippable preamble that enforces the rcParams + post-save fonttype-42 check at the *root* of the skill graph, not at a leaf where it can be pruned.

Result after rerun: scatter-fit 17→24 (+7), sankey 18→23 (+5).

### Action 12 — network-graph caption modularity Q

FD4 first sweep: network-graph 22/24 with `caption_quality = 2` because caption listed only layout parameters. Now requires Modularity Q (Newman's), inter-intra-edge ratio, OR largest-component density. Even Q=-0.16 (no community structure) is a valid finding.

Result after rerun: network-graph 20→22 (+2 caption + scientific clarity).

### Action 13 — equation-block PDF trim discipline (paper-compile step 9)

FD4 first sweep: equation-block 21/24 with `layout_density = 2` because letter-size PDF had 47% blank space below the derivation. Added geometry `paperheight=auto` + `pdfcrop` post-build rule. Partial application after rerun (agent set margins but not paperheight; equation-block stayed 22/24, ties baseline).

### Action 14 — grouped-bar per-bar value-label offset

FD4 first sweep: grouped-bar 23/24 with `layout_density = 2` because labels used `max(stds)` constant offset, floating high above low-variance bars. Now per-bar `mean[i] + std[i] + pad`. Constant offset acceptable only when stds within 1.2× of each other.

Result after rerun: grouped-bar 23→24 (perfect).

## Final tally

- WIN: 16/17
- TIE: 1/17 (equation-block 22 = baseline 22)
- LOSE: 0/17
- v4 common-17 avg 23.12/24 vs best-baseline 20.06 → **+3.06 (+15.2%)**
- v4 vs FD2 minionsos: **+4.41 (+23.6%)** cumulative across 2 Forge rounds

See `REPORT.md` for the full per-cell scoreboard and per-axis improvement table.
