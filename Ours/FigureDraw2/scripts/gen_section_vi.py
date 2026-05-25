#!/usr/bin/env python3
"""Generate the 17x8 figure matrix for FigureDraw2 §VI."""
import json, pathlib, html, re

ROOT = pathlib.Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2")
ARMS = ["minionsos","ml-paper-writing","latex-document","academic-paper-imbad",
        "scientific-writing-kdense","stat-writing-fuhaoda","composer-lishix","awesome-writing-prompts"]
FIGS = ["grouped-bar","line-errband","scatter-fit","heatmap","box-violin",
        "4panel-hero","architecture","roc-prc","ridgeline","dual-axis-time",
        "stacked-bar","forest-plot","sankey","volcano","network-graph",
        "latex-table","equation-block"]

FIG_DECK = {
    "grouped-bar": "4 method × 5 benchmark 准确率 + std。",
    "line-errband": "3 method × 50 step 训练 loss + 95% CI。",
    "scatter-fit": "Scaling-law 80 点 + OLS + R²。",
    "heatmap": "10×10 confusion matrix。",
    "box-violin": "4 condition × 100 样本 violin + box。",
    "4panel-hero": "Hero gridspec(2,3) — A 概念,B/C/D 数据。",
    "architecture": "3-layer pipeline,boxes-and-arrows。",
    "roc-prc": "4 binary classifier 双面板 + AUROC/AP。",
    "ridgeline": "6-cluster expression ridge stack。",
    "dual-axis-time": "200 step training loss(log) + cosine LR。",
    "stacked-bar": "5 condition × 4-class proportion(每柱总和=1)。",
    "forest-plot": "12-study meta-analysis,带 CI + pooled diamond。",
    "sankey": "Dataset-prep flow,3 stage 5/4/3 分发。",
    "volcano": "~3000 gene log2FC vs −log10(p),阈值染色。",
    "network-graph": "30-node small-world,4 community 染色。",
    "latex-table": "4 method × 5 metric booktabs 比较表,渲染单页 PDF。",
    "equation-block": "3 个编号 ELBO 推导 display equation + \\eqref 跨引。",
}

def load_grade(arm, fig):
    p = ROOT/"grader"/arm/f"{fig}.json"
    if not p.exists(): return None
    try: return json.loads(p.read_text(encoding="utf-8"))
    except: return None

agg = json.loads((ROOT/"grader/_aggregate.json").read_text())
winners = agg["winners"]

def cell_html(arm, fig, grade, is_winner):
    img = f"assets/{fig}__{arm}.png"
    img_html = f'<img src="{img}" alt="{fig} {arm}"/>' if (ROOT/"reports"/img).exists() else '<div style="padding:30px;text-align:center;color:var(--faint)">(no image)</div>'
    if not grade or "scores" not in grade:
        return f'<div class="figcell">{img_html}<div class="meta"><span class="arm">{html.escape(arm)}</span><span class="total">— /24</span><div class="ev">no grade</div></div></div>'
    sc = grade["scores"]
    total = sum(sc.values())
    axes = " ".join(f"{k[:3]}:{v}" for k,v in [
        ("sci",sc.get("scientific_clarity","-")),("typ",sc.get("typography","-")),
        ("pal",sc.get("palette","-")),("lay",sc.get("layout_density","-")),
        ("rev",sc.get("reviewer_readiness","-")),("vec",sc.get("vector_fidelity","-")),
        ("fmt",sc.get("file_format","-")),("cap",sc.get("caption_quality","-"))])
    pos = (grade.get("overall_strengths") or [""])[0][:130]
    neg = (grade.get("overall_weaknesses") or [""])[0][:130]
    arm_class = "arm win" if is_winner else "arm"
    return (f'<div class="figcell">{img_html}<div class="meta">'
            f'<span class="{arm_class}">{html.escape(arm)}</span>'
            f'<span class="total"><b>{total}</b>/24</span>'
            f'<div class="axes">{axes}</div>'
            + (f'<div class="pn"><span class="plus">+ {html.escape(pos)}</span></div>' if pos else "")
            + (f'<div class="pn"><span class="minus">– {html.escape(neg)}</span></div>' if neg else "")
            + '</div></div>')

parts = []
parts.append('<section id="matrix" class="wide">')
parts.append('<h2 style="text-align:center;font-size:36px"><span class="roman" style="text-align:center">VI</span>17×8 全图矩阵</h2>')
parts.append('<p class="deck" style="text-align:center;max-width:680px;margin:0 auto 36px">每个 fig_type 一行,八个 arm 横排。每张图下显示 8 维分数 + 一句 strength + 一句 weakness。★ 是该题冠军。</p>')

for fig in FIGS:
    parts.append(f'<div class="figrow" id="fig-{fig}">')
    parts.append(f'<h3>{html.escape(fig)}</h3>')
    parts.append(f'<p class="figdeck">{html.escape(FIG_DECK.get(fig,""))}</p>')
    row = agg["by_fig_total"][fig]
    ranked = sorted([(arm, v) for arm,v in row.items() if v is not None], key=lambda x: -x[1])
    score_line = " · ".join(f"<b>{arm}</b>={v}" if arm==winners.get(fig) else f"{arm}={v}" for arm,v in ranked)
    parts.append(f'<p class="scoreline">{score_line}</p>')
    parts.append('<div class="figgrid">')
    for arm in ARMS:
        grade = load_grade(arm, fig)
        parts.append(cell_html(arm, fig, grade, arm==winners.get(fig)))
    parts.append('</div></div>')

parts.append('</section><p class="sep-ornament">❧</p>')
out = "\n".join(parts)
pathlib.Path("/tmp/figdraw2_section_vi.html").write_text(out, encoding="utf-8")
cells = out.count('<div class="figcell"')
print(f"OK: {len(out)} bytes, {cells} cells")
