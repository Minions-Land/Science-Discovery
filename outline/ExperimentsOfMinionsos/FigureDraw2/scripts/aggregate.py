#!/usr/bin/env python3
"""FigureDraw2 aggregate: per-arm 8-axis means, per-fig winners, paper-page metrics, borrow-list seeds."""
import json, pathlib, statistics, re
from collections import defaultdict

ROOT = pathlib.Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2")
ARMS = ["minionsos","ml-paper-writing","latex-document","academic-paper-imbad",
        "scientific-writing-kdense","stat-writing-fuhaoda","composer-lishix","awesome-writing-prompts"]
AXES = ["scientific_clarity","typography","palette","layout_density",
        "reviewer_readiness","vector_fidelity","file_format","caption_quality"]
FIGS = ["grouped-bar","line-errband","scatter-fit","heatmap","box-violin",
        "4panel-hero","architecture","roc-prc","ridgeline","dual-axis-time",
        "stacked-bar","forest-plot","sankey","volcano","network-graph",
        "latex-table","equation-block"]

data = defaultdict(dict)
errors = []
for arm in ARMS:
    for jf in sorted((ROOT/"grader"/arm).glob("*.json")):
        fig = jf.stem
        try:
            blob = json.loads(jf.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"{arm}/{fig}: parse {e}"); continue
        if "error" in blob:
            errors.append(f"{arm}/{fig}: {blob.get('error')}"); continue
        if "scores" not in blob:
            errors.append(f"{arm}/{fig}: no scores"); continue
        if not all(a in blob["scores"] for a in AXES):
            errors.append(f"{arm}/{fig}: missing axes"); continue
        data[arm][fig] = blob

total_cells = sum(len(v) for v in data.values())
print(f"Parsed {total_cells} cells, {len(errors)} errors")
for e in errors[:10]: print(" -", e)

print("\n=== Per-arm 8-axis means (out of 3) ===")
print(f"{'arm':32s} " + " ".join(f"{a[:10]:>10s}" for a in AXES) + "  total/24")
arm_total = {}
arm_axis_means = {}
for arm in ARMS:
    cells = list(data[arm].values())
    if not cells:
        print(f"{arm:32s} (no cells)"); continue
    means = {a: statistics.mean(c["scores"][a] for c in cells) for a in AXES}
    total = sum(means.values())
    arm_total[arm] = total
    arm_axis_means[arm] = means
    print(f"{arm:32s} " + " ".join(f"{means[a]:>10.2f}" for a in AXES) + f"  {total:>5.2f}")

print("\n=== Per-fig per-arm total (sum of 8 axes; max 24) ===")
header = "fig".ljust(18) + " " + " ".join(arm[:10].rjust(10) for arm in ARMS)
print(header)
for fig in FIGS:
    row = [fig.ljust(18)]
    for arm in ARMS:
        if fig in data[arm]:
            row.append(f"{sum(data[arm][fig]['scores'].values()):>10d}")
        else:
            row.append("     -")
    print(" ".join(row))

print("\n=== Per-fig winner / runner-up / loser ===")
winners = {}
for fig in FIGS:
    items = []
    for arm in ARMS:
        if fig in data[arm]:
            items.append((arm, sum(data[arm][fig]["scores"].values())))
    items.sort(key=lambda x: -x[1])
    if items:
        winners[fig] = items[0]
        if len(items) >= 2:
            print(f"  {fig:18s} {items[0][0]:32s}({items[0][1]})  vs  loser {items[-1][0]}({items[-1][1]})")

# Paper-page summary: pages, size, macro count, compile cleanliness
print("\n=== Paper-page (8 arms) ===")
pp_summary = {}
for arm in ARMS:
    sess = list((ROOT/"sessions"/arm).glob(f"paper-page-{arm}/*/workspace"))
    if not sess:
        pp_summary[arm] = {"status":"no_workspace"}
        print(f"  {arm:32s} NO WORKSPACE")
        continue
    ws = sorted(sess)[-1]
    main_pdf = ws/"main.pdf"
    main_tex = ws/"main.tex"
    main_log = ws/"main.log"
    fig_pdf = ws/"figure.pdf"
    if not main_pdf.exists():
        if fig_pdf.exists():
            pp_summary[arm] = {"status":"misinterpreted_as_figure"}
            print(f"  {arm:32s} MISINTERPRETED (produced figure.pdf instead of main.pdf)")
        else:
            pp_summary[arm] = {"status":"no_output"}
            print(f"  {arm:32s} NO OUTPUT")
        continue
    size_kb = main_pdf.stat().st_size//1024
    macros = 0
    if main_tex.exists():
        tex_text = main_tex.read_text(encoding="utf-8", errors="replace")
        macros = len(re.findall(r"\\newcommand", tex_text))
    errs, undefs = 0, 0
    if main_log.exists():
        log_text = main_log.read_text(encoding="utf-8", errors="replace")
        errs = len(re.findall(r"^!", log_text, re.MULTILINE))
        undefs = len(re.findall(r"undefined", log_text, re.IGNORECASE))
    # pdf info via py call - count pages from PDF header
    pages = 0
    pdf_text = main_pdf.read_bytes()
    pages = pdf_text.count(b"/Type /Page\n") + pdf_text.count(b"/Type/Page\n") or len(re.findall(rb"/Type\s*/Page\b", pdf_text))
    pp_summary[arm] = {"status":"ok", "pages": pages, "size_kb": size_kb,
                       "macros": macros, "errors": errs, "undefs": undefs}
    print(f"  {arm:32s} pages={pages} size={size_kb}KB macros={macros} err={errs} undef={undefs}")

out = {
    "by_arm_total": arm_total,
    "by_arm_mean": arm_axis_means,
    "by_arm_per_fig": {arm: {fig: data[arm][fig]["scores"] for fig in data[arm]} for arm in ARMS if data[arm]},
    "by_fig_total": {fig: {arm: (sum(data[arm][fig]["scores"].values()) if fig in data[arm] else None) for arm in ARMS} for fig in FIGS},
    "winners": {fig: w[0] for fig,w in winners.items()},
    "paper_page": pp_summary,
    "errors": errors,
}
p = ROOT/"grader/_aggregate.json"
p.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"\nSaved aggregate -> {p}")

# Save evidence + strengths/weaknesses per cell
ev_out = {}
for arm in ARMS:
    ev_out[arm] = {}
    for fig, blob in data[arm].items():
        ev_out[arm][fig] = {
            "total": sum(blob["scores"].values()),
            "scores": blob["scores"],
            "strengths": blob.get("overall_strengths") or [],
            "weaknesses": blob.get("overall_weaknesses") or [],
            "evidence": blob.get("evidence", {}),
        }
p2 = ROOT/"grader/_evidence.json"
p2.write_text(json.dumps(ev_out, indent=2), encoding="utf-8")
print(f"Saved evidence -> {p2}")
