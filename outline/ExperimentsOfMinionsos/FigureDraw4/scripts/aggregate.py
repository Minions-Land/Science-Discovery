#!/usr/bin/env python3
"""FD4 aggregation + diff vs FD3 v3 baseline (minionsos-v3 arm) + FD2 best-of-baselines."""
import json, pathlib, statistics, re

FD4 = pathlib.Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw4")
FD3 = pathlib.Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw3")
FD2 = pathlib.Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2")

AXES = ["scientific_clarity","typography","palette","layout_density",
        "reviewer_readiness","vector_fidelity","file_format","caption_quality"]

FIGS_COMMON = ["grouped-bar","line-errband","scatter-fit","heatmap","box-violin",
        "4panel-hero","architecture","roc-prc","ridgeline","dual-axis-time",
        "stacked-bar","forest-plot","sankey","volcano","network-graph",
        "latex-table","equation-block"]
FIGS_NEW_FD3 = ["cns-graphical-abstract","imrad-section"]
FIGS_ALL = FIGS_COMMON + FIGS_NEW_FD3

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

def total(cell):
    return sum(cell["scores"].values()) if cell else None

v4_dir = FD4/"grader/minionsos-v4"
v3_dir = FD3/"grader/minionsos-v3"
v2_dir = FD2/"grader/minionsos"

# FD2 had 7 baseline arms; compute the best (max) score per fig across all baselines
FD2_BASELINE_ARMS_DIR = FD2/"grader"
def best_baseline_per_fig():
    out = {}
    if not FD2_BASELINE_ARMS_DIR.exists():
        return out
    for fig in FIGS_COMMON:
        best = None
        best_arm = None
        for arm_path in FD2_BASELINE_ARMS_DIR.iterdir():
            if not arm_path.is_dir(): continue
            cell = load(arm_path, fig)
            t = total(cell)
            if t is not None and (best is None or t > best):
                best = t
                best_arm = arm_path.name
        if best is not None:
            out[fig] = (best, best_arm)
    return out

best_base = best_baseline_per_fig()

# === Per-fig: v4 vs v3 baseline vs FD2 best-of-baselines ===
print("=== FD4 per-fig (8-axis sum, max 24) ===")
print(f"{'fig_type':22s} {'v3':>4s} {'v4':>4s} {'Δv3':>5s} {'best-base':>10s} {'(arm)':>22s} {'Δbase':>6s}")
v4_totals, v3_totals = {}, {}
beat_baseline_count = 0
matched_baseline_count = 0
for fig in FIGS_ALL:
    v4 = load(v4_dir, fig)
    v3 = load(v3_dir, fig)
    v4_t = total(v4)
    v3_t = total(v3)
    if v4_t is not None: v4_totals[fig] = v4_t
    if v3_t is not None: v3_totals[fig] = v3_t
    delta_v3 = (v4_t - v3_t) if (v4_t is not None and v3_t is not None) else None
    base_t, base_arm = best_base.get(fig, (None, None))
    delta_base = (v4_t - base_t) if (v4_t is not None and base_t is not None) else None
    if delta_base is not None:
        if delta_base > 0: beat_baseline_count += 1
        elif delta_base == 0: matched_baseline_count += 1
    s_v3 = f"{v3_t}" if v3_t is not None else "  -"
    s_v4 = f"{v4_t}" if v4_t is not None else "  -"
    s_dv3 = f"{delta_v3:+d}" if delta_v3 is not None else "  -"
    s_b = f"{base_t}" if base_t is not None else "  -"
    s_ba = f"({base_arm})" if base_arm else ""
    s_db = f"{delta_base:+d}" if delta_base is not None else " NEW"
    print(f"  {fig:22s} {s_v3:>4s} {s_v4:>4s} {s_dv3:>5s} {s_b:>10s} {s_ba:>22s} {s_db:>6s}")

# Per-axis means (v4 vs v3)
print("\n=== FD4 vs FD3 per-axis means (out of 3) ===")
v4_cells = [c for c in (load(v4_dir, f) for f in FIGS_ALL) if c]
v3_cells = [c for c in (load(v3_dir, f) for f in FIGS_ALL) if c]
print(f"{'axis':24s} {'v3':>6s} {'v4':>6s} {'Δ':>7s}")
for a in AXES:
    if not v3_cells or not v4_cells: continue
    v3m = statistics.mean(c["scores"][a] for c in v3_cells)
    v4m = statistics.mean(c["scores"][a] for c in v4_cells)
    print(f"  {a:24s} {v3m:>6.2f} {v4m:>6.2f} {v4m-v3m:+7.3f}")

# Common-17 average (apples-to-apples over all 3 rounds)
print("\n=== Common-17 average across rounds ===")
v4_common = [c for c in (load(v4_dir, f) for f in FIGS_COMMON) if c]
v3_common = [c for c in (load(v3_dir, f) for f in FIGS_COMMON) if c]
v2_common = [c for c in (load(v2_dir, f) for f in FIGS_COMMON) if c]
def avg(cells): return statistics.mean(total(c) for c in cells) if cells else None
v4_avg17 = avg(v4_common)
v3_avg17 = avg(v3_common)
v2_avg17 = avg(v2_common)
print(f"  v2 (FD2 minionsos): {v2_avg17:.2f}/24" if v2_avg17 is not None else "  v2: -")
print(f"  v3 (FD3 minionsos): {v3_avg17:.2f}/24" if v3_avg17 is not None else "  v3: -")
print(f"  v4 (FD4 minionsos): {v4_avg17:.2f}/24" if v4_avg17 is not None else "  v4: -")
if v4_avg17 is not None and v3_avg17 is not None:
    print(f"  Δ v4-v3: {v4_avg17-v3_avg17:+.2f}")
if v4_avg17 is not None and v2_avg17 is not None:
    print(f"  Δ v4-v2: {v4_avg17-v2_avg17:+.2f}  ({(v4_avg17-v2_avg17)/v2_avg17*100:+.1f}%)")

# Beat-baselines summary
total_with_base = sum(1 for fig in FIGS_COMMON if fig in best_base and fig in v4_totals)
print(f"\n=== Beat-of-baselines summary (FD2 best per cell) ===")
print(f"  cells where v4 > best-baseline: {beat_baseline_count}/{total_with_base}")
print(f"  cells where v4 = best-baseline: {matched_baseline_count}/{total_with_base}")
print(f"  cells where v4 < best-baseline: {total_with_base - beat_baseline_count - matched_baseline_count}/{total_with_base}")

# New fig types
print("\n=== NEW (post-FD2) fig_types ===")
for fig in FIGS_NEW_FD3:
    v4 = load(v4_dir, fig)
    v3 = load(v3_dir, fig)
    if v4 or v3:
        v4_t = total(v4); v3_t = total(v3)
        print(f"  {fig:24s} v3={v3_t}/24  v4={v4_t}/24  Δ={(v4_t-v3_t) if (v4_t is not None and v3_t is not None) else '?':+d}" if (v4_t is not None and v3_t is not None) else f"  {fig:24s} v3={v3_t} v4={v4_t}")

# Paper-page comparison
print("\n=== Paper-page comparison ===")
def pp_meta(arm_dir, arm_name, base_root):
    candidates = sorted(base_root.glob(f"sessions/{arm_name}/paper-page*/2*/workspace/main.pdf"))
    if not candidates: return None
    pdf = candidates[-1]; ws = pdf.parent
    main_tex = ws/"main.tex"; main_log = ws/"main.log"
    macros = 0
    if main_tex.exists():
        macros = len(re.findall(r"\\newcommand", main_tex.read_text(encoding="utf-8", errors="replace")))
    pages = len(re.findall(rb"/Type\s*/Page\b", pdf.read_bytes()))
    errs = undefs = 0
    if main_log.exists():
        log = main_log.read_text(encoding="utf-8", errors="replace")
        errs = len(re.findall(r"^!", log, re.MULTILINE))
        undefs = len(re.findall(r"undefined", log, re.IGNORECASE))
    return {"pages": pages, "size_kb": pdf.stat().st_size//1024, "macros": macros, "errs": errs, "undefs": undefs}

v2_pp = pp_meta(v2_dir, "minionsos", FD2)
v3_pp = pp_meta(v3_dir, "minionsos-v3", FD3)
v4_pp = pp_meta(v4_dir, "minionsos-v4", FD4)
for label, meta in [("v2 (FD2 minionsos)", v2_pp), ("v3 (FD3 minionsos-v3)", v3_pp), ("v4 (FD4 minionsos-v4)", v4_pp)]:
    if meta:
        print(f"  {label}: pages={meta['pages']} size={meta['size_kb']}KB macros={meta['macros']} err={meta['errs']} undef={meta['undefs']}")
    else:
        print(f"  {label}: NO main.pdf")

# Save aggregate
out = {
    "v2_per_fig": {f: total(load(v2_dir,f)) for f in FIGS_COMMON if total(load(v2_dir,f)) is not None},
    "v3_per_fig": v3_totals,
    "v4_per_fig": v4_totals,
    "v2_avg17": v2_avg17,
    "v3_avg17": v3_avg17,
    "v4_avg17": v4_avg17,
    "delta_v4_v3": (v4_avg17 - v3_avg17) if (v4_avg17 is not None and v3_avg17 is not None) else None,
    "delta_v4_v2": (v4_avg17 - v2_avg17) if (v4_avg17 is not None and v2_avg17 is not None) else None,
    "best_baselines_per_fig": {fig: {"score": b[0], "arm": b[1]} for fig, b in best_base.items()},
    "beat_baseline_count": beat_baseline_count,
    "matched_baseline_count": matched_baseline_count,
    "total_with_base": total_with_base,
    "v2_paper_page": v2_pp, "v3_paper_page": v3_pp, "v4_paper_page": v4_pp,
    "v3_axis_means": {a: statistics.mean(c["scores"][a] for c in v3_cells) for a in AXES} if v3_cells else {},
    "v4_axis_means": {a: statistics.mean(c["scores"][a] for c in v4_cells) for a in AXES} if v4_cells else {},
}
p = FD4/"grader/_aggregate.json"
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"\nSaved -> {p}")

# Per-cell evidence dump for the report
ev_out = {}
for fig in FIGS_ALL:
    v4 = load(v4_dir, fig)
    if not v4: continue
    ev_out[fig] = {
        "total": total(v4),
        "scores": v4["scores"],
        "strengths": v4.get("overall_strengths") or [],
        "weaknesses": v4.get("overall_weaknesses") or [],
        "evidence": v4.get("evidence", {}),
    }
(FD4/"grader/_evidence.json").write_text(json.dumps(ev_out, indent=2), encoding="utf-8")
