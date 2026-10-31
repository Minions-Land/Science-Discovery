#!/usr/bin/env python3
"""FD3 aggregation + diff vs FD2 v2 anchor (minionsos arm)."""
import json, pathlib, statistics, re
from collections import defaultdict

FD3 = pathlib.Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw3")
FD2 = pathlib.Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2")
AXES = ["scientific_clarity","typography","palette","layout_density",
        "reviewer_readiness","vector_fidelity","file_format","caption_quality"]
FIGS_COMMON = ["grouped-bar","line-errband","scatter-fit","heatmap","box-violin",
        "4panel-hero","architecture","roc-prc","ridgeline","dual-axis-time",
        "stacked-bar","forest-plot","sankey","volcano","network-graph",
        "latex-table","equation-block"]
FIGS_NEW = ["cns-graphical-abstract","imrad-section"]
FIGS_ALL = FIGS_COMMON + FIGS_NEW

def load(arm_dir, fig):
    p = arm_dir/f"{fig}.json"
    if not p.exists(): return None
    try:
        b = json.loads(p.read_text(encoding="utf-8"))
        if "scores" in b and all(a in b["scores"] for a in AXES):
            return b
    except Exception as e:
        print(f"  parse fail {p}: {e}")
    return None

v3_dir = FD3/"grader/minionsos-v3"
v2_dir = FD2/"grader/minionsos"

# Per-fig totals
print("=== FD3 vs FD2 per-fig (8-axis sum, max 24) ===")
print(f"{'fig_type':22s} {'v2':>5s} {'v3':>5s} {'Δ':>6s}")
v3_totals, v2_totals = {}, {}
for fig in FIGS_ALL:
    v3 = load(v3_dir, fig)
    v2 = load(v2_dir, fig) if fig in FIGS_COMMON else None
    v3_t = sum(v3["scores"].values()) if v3 else None
    v2_t = sum(v2["scores"].values()) if v2 else None
    if v3_t is not None: v3_totals[fig] = v3_t
    if v2_t is not None: v2_totals[fig] = v2_t
    delta = (v3_t - v2_t) if (v3_t is not None and v2_t is not None) else None
    v2s = f"{v2_t}" if v2_t is not None else "  -"
    v3s = f"{v3_t}" if v3_t is not None else "  -"
    ds = f"{delta:+d}" if delta is not None else " NEW"
    print(f"  {fig:22s} {v2s:>5s} {v3s:>5s} {ds:>6s}")

# Per-axis means
print("\n=== FD3 vs FD2 per-axis means (out of 3) ===")
v3_cells = [load(v3_dir, f) for f in FIGS_ALL]; v3_cells = [c for c in v3_cells if c]
v2_cells = [load(v2_dir, f) for f in FIGS_COMMON]; v2_cells = [c for c in v2_cells if c]
print(f"{'axis':24s} {'v2':>6s} {'v3':>6s} {'Δ':>7s}")
for a in AXES:
    v2m = statistics.mean(c["scores"][a] for c in v2_cells)
    v3m = statistics.mean(c["scores"][a] for c in v3_cells)
    print(f"  {a:24s} {v2m:>6.2f} {v3m:>6.2f} {v3m-v2m:+7.3f}")

# Total averages (just the common 17 for fair comparison)
print("\n=== Common-17 average (apples-to-apples) ===")
v3_common = [load(v3_dir, f) for f in FIGS_COMMON]; v3_common = [c for c in v3_common if c]
v3_avg17 = statistics.mean(sum(c["scores"].values()) for c in v3_common)
v2_avg17 = statistics.mean(sum(c["scores"].values()) for c in v2_cells)
print(f"  v2 (FD2 minionsos): {v2_avg17:.2f} / 24")
print(f"  v3 (FD3 minionsos): {v3_avg17:.2f} / 24")
print(f"  Δ: {v3_avg17-v2_avg17:+.2f}  ({(v3_avg17-v2_avg17)/v2_avg17*100:+.1f}%)")

# New fig types
print("\n=== NEW fig_types (FD3 only) ===")
for fig in FIGS_NEW:
    v3 = load(v3_dir, fig)
    if v3:
        scores = v3["scores"]
        total = sum(scores.values())
        axes_str = " ".join(f"{a[:3]}:{scores[a]}" for a in AXES)
        print(f"  {fig:24s} {total}/24    {axes_str}")

# Paper-page comparison
print("\n=== Paper-page comparison (FD3 vs FD2 minionsos) ===")
def pp_meta(arm_dir, arm_name, base_root):
    candidates = sorted(base_root.glob(f"sessions/{arm_name}/paper-page*/2*/workspace/main.pdf"))
    if not candidates: return None
    pdf = candidates[-1]
    ws = pdf.parent
    main_tex = ws/"main.tex"
    main_log = ws/"main.log"
    macros = 0
    if main_tex.exists():
        macros = len(re.findall(r"\\newcommand", main_tex.read_text(encoding="utf-8", errors="replace")))
    pages = 0
    pdf_text = pdf.read_bytes()
    pages = len(re.findall(rb"/Type\s*/Page\b", pdf_text))
    errs = undefs = 0
    if main_log.exists():
        log = main_log.read_text(encoding="utf-8", errors="replace")
        errs = len(re.findall(r"^!", log, re.MULTILINE))
        undefs = len(re.findall(r"undefined", log, re.IGNORECASE))
    return {"pages": pages, "size_kb": pdf.stat().st_size//1024, "macros": macros, "errs": errs, "undefs": undefs}

v2_pp = pp_meta(v2_dir, "minionsos", FD2)
v3_pp = pp_meta(v3_dir, "minionsos-v3", FD3)
for label, meta in [("v2 (FD2 minionsos)", v2_pp), ("v3 (FD3 minionsos-v3)", v3_pp)]:
    if meta:
        print(f"  {label}: pages={meta['pages']} size={meta['size_kb']}KB macros={meta['macros']} err={meta['errs']} undef={meta['undefs']}")
    else:
        print(f"  {label}: NO main.pdf")

# Save aggregate
out = {
    "v2_per_fig": v2_totals,
    "v3_per_fig": v3_totals,
    "v2_avg17": v2_avg17,
    "v3_avg17": v3_avg17,
    "delta_avg17": v3_avg17 - v2_avg17,
    "v2_paper_page": v2_pp,
    "v3_paper_page": v3_pp,
    "v3_axis_means": {a: statistics.mean(c["scores"][a] for c in v3_cells) for a in AXES},
    "v2_axis_means": {a: statistics.mean(c["scores"][a] for c in v2_cells) for a in AXES},
}
p = FD3/"grader/_aggregate.json"
p.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"\nSaved -> {p}")

# Per-cell evidence dump for the report
ev_out = {}
for fig in FIGS_ALL:
    v3 = load(v3_dir, fig)
    if not v3: continue
    ev_out[fig] = {
        "total": sum(v3["scores"].values()),
        "scores": v3["scores"],
        "strengths": v3.get("overall_strengths") or [],
        "weaknesses": v3.get("overall_weaknesses") or [],
        "evidence": v3.get("evidence", {}),
    }
(FD3/"grader/_evidence.json").write_text(json.dumps(ev_out, indent=2), encoding="utf-8")
