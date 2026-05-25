#!/usr/bin/env python3
"""gen_figure.py — RetroDiff architecture diagram. Data source: data.json"""
import json, pathlib, subprocess, sys, re
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

PALETTE = {
    "input_bg":  "#DBEAFE", "input_bd":  "#1D4ED8",
    "module_bg": "#EDE9FE", "module_bd": "#5B21B6",
    "store_bg":  "#D1FAE5", "store_bd":  "#065F46",
    "output_bg": "#FEF3C7", "output_bd": "#92400E",
    "ret_fill":  "#EBF5FB", "ret_edge":  "#2980B9",
    "gen_fill":  "#FDF2F8", "gen_edge":  "#7D3C98",
    "arrow_data": "#1A1A2E",
    "arrow_ctrl": "#888888",
    "text":       "#1A1A2E",
}

data = json.loads(pathlib.Path("data.json").read_text())

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis("off")

# (cx, cy, w, h)
POS = {
    "input":    (1.1,  2.5,  1.2,  0.65),
    "retrieve": (3.6,  3.2,  1.5,  0.65),
    "db":       (3.6,  1.8,  1.5,  0.65),
    "diff":     (6.6,  3.2,  1.8,  0.65),
    "prior":    (6.6,  1.8,  1.8,  0.65),
    "output":   (9.1,  2.5,  1.5,  0.65),
}
LABELS = {
    "input":    "Query",
    "retrieve": "Retriever",
    "db":       "KB",
    "diff":     "Diffusion\nDecoder",
    "prior":    "Prior\nNetwork",
    "output":   "Generated\nSample",
}
KIND_STYLE = {
    "input":     ("input_bg",  "input_bd"),
    "module":    ("module_bg", "module_bd"),
    "datastore": ("store_bg",  "store_bd"),
    "output":    ("output_bg", "output_bd"),
}

# ── Group backgrounds ──────────────────────────────────────────────────────
for grp_label, fk, ek, x1, y1, x2, y2 in [
    ("Retrieval",  "ret_fill", "ret_edge", 2.7,  1.15, 4.65, 3.85),
    ("Generation", "gen_fill", "gen_edge", 5.55, 1.15, 7.75, 3.85),
]:
    ax.add_patch(FancyBboxPatch(
        (x1, y1), x2-x1, y2-y1,
        boxstyle="round,pad=0.12", linewidth=1.5, linestyle="--",
        edgecolor=PALETTE[ek], facecolor=PALETTE[fk], alpha=0.55, zorder=0,
    ))
    ax.text(x1+0.13, y2-0.13, grp_label,
            fontsize=8, fontweight="bold", color=PALETTE[ek], va="top", zorder=1)

# ── Nodes ──────────────────────────────────────────────────────────────────
kind_map = {s["id"]: s["kind"] for s in data["stages"]}
for nid, (cx, cy, w, h) in POS.items():
    bg_k, bd_k = KIND_STYLE[kind_map[nid]]
    ax.add_patch(FancyBboxPatch(
        (cx-w/2, cy-h/2), w, h,
        boxstyle="round,pad=0.08", linewidth=1.8,
        edgecolor=PALETTE[bd_k], facecolor=PALETTE[bg_k], zorder=2,
    ))
    ax.text(cx, cy, LABELS[nid], ha="center", va="center",
            fontsize=9, fontweight="bold", color=PALETTE["text"],
            linespacing=1.3, zorder=3)

# ── Arrow helper ───────────────────────────────────────────────────────────
def arrow(x1, y1, x2, y2, dashed=False):
    c = PALETTE["arrow_ctrl"] if dashed else PALETTE["arrow_data"]
    ls = (0, (4, 2)) if dashed else "solid"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=c, lw=1.5,
                        linestyle=ls, mutation_scale=12,
                        connectionstyle="arc3,rad=0.0"),
        zorder=4)

def cx(n): return POS[n][0]
def cy(n): return POS[n][1]
def rx(n): return POS[n][0] + POS[n][2]/2
def lx(n): return POS[n][0] - POS[n][2]/2
def top(n): return POS[n][1] + POS[n][3]/2
def bot(n): return POS[n][1] - POS[n][3]/2

OFF = 0.12

# data flow (solid)
arrow(rx("input"),    cy("input"),    lx("retrieve"), cy("retrieve"))
arrow(cx("retrieve")-OFF, bot("retrieve"), cx("db")-OFF,       top("db"))
arrow(cx("db")+OFF,       top("db"),       cx("retrieve")+OFF, bot("retrieve"))
arrow(rx("retrieve"), cy("retrieve"), lx("diff"),     cy("diff"))
arrow(rx("diff"),     cy("diff"),     lx("output"),   cy("output"))

# control/feedback (dashed)
arrow(cx("diff")-OFF,  bot("diff"),  cx("prior")-OFF, top("prior"), dashed=True)
arrow(cx("prior")+OFF, top("prior"), cx("diff")+OFF,  bot("diff"),  dashed=True)

# ── Legend ─────────────────────────────────────────────────────────────────
for i, (label, dashed) in enumerate([("data flow", False), ("control / feedback", True)]):
    y = 0.52 - i * 0.30
    c = PALETTE["arrow_ctrl"] if dashed else PALETTE["arrow_data"]
    ls = "--" if dashed else "-"
    ax.plot([0.15, 0.68], [y, y], ls, color=c, lw=1.5, zorder=5)
    ax.annotate("", xy=(0.68, y), xytext=(0.58, y),
        arrowprops=dict(arrowstyle="-|>", color=c, lw=1.5, mutation_scale=10), zorder=5)
    ax.text(0.78, y, label, fontsize=7.5, va="center", color=c)

plt.tight_layout(pad=0.3)

out = pathlib.Path(".")
fig.savefig(out / "figure.pdf", bbox_inches="tight")
fig.savefig(out / "figure.png", dpi=300, bbox_inches="tight")
fig.savefig(out / "figure.svg", bbox_inches="tight")
print("Saved figure.pdf / figure.png / figure.svg")

# ── Font verification ──────────────────────────────────────────────────────
pdf_path = out / "figure.pdf"
res = subprocess.run(["pdffonts", str(pdf_path)], capture_output=True, text=True, check=False)
if res.returncode == 0:
    if "Type 3" in res.stdout:
        sys.stderr.write(f"FATAL: Type-3 fonts in figure.pdf\n{res.stdout}\n"); sys.exit(2)
    print("[fonttype-check] OK — no Type 3 fonts")
else:
    raw = pdf_path.read_bytes()
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write("FATAL: /Type3 in figure.pdf\n"); sys.exit(2)
    print("[fonttype-check] OK (raw-bytes fallback)")
