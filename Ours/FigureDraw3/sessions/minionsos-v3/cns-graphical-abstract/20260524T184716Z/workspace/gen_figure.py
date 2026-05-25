"""
RetroDiff graphical abstract — CNS-tier (Cell Reports / Nat Commun / Sci Adv)
Pattern: Workflow (Pattern 1) — left-to-right pipeline with embedded headline result
Layout: landscape 2:1, 12×6 inches (= 1200×600 px at 100 dpi; 300 dpi for print)

Aesthetic principles applied (from figure-aesthetic-exemplars skill):
  P1  hue coherence — cool family: teal / slate-blue / mint, one grey neutral
  P2  reduced saturation — fills ~25-40%, strokes ~65-75%
  P3  effective display area — bar axis range from data_min-0.1*span to data_max+0.15*span
  P4  backpack packing — 5 zones + metric strip with no empty cells
  P10 text economy — only load-bearing annotations
  P11 font unification — set once in rcParams, never overridden per element
  P12 layout budget — top 8% reserved for title chrome
  P13 auto-sizing bbox on all labeled text (no fixed-width rectangles)
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── P11: Font stack locked once, never overridden per element ─────────────────
# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
mpl.rcParams.update({
    "font.family":          "sans-serif",
    "font.sans-serif":      ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype":         "none",
    "pdf.fonttype":         42,
    "axes.spines.right":    False,
    "axes.spines.top":      False,
    "axes.linewidth":       0.8,
    "legend.frameon":       False,
    "xtick.direction":      "out",
    "ytick.direction":      "out",
})

# ── P1+P2: Cool-family palette, reduced saturation ────────────────────────────
# Primary signal: slate-blue ~70% sat; retrieval: teal ~65%; fills: ~25-35% sat
P = {
    "bg":          "#FFFFFF",
    "blue":        "#2B6CB0",     # slate-blue, ~70% sat — RetroDiff method
    "blue_soft":   "#CCDEED",     # ~25% sat fill
    "teal":        "#2A7A6C",     # teal, ~65% sat — retrieval / output
    "teal_soft":   "#BBDBD5",     # ~30% sat fill
    "mint":        "#4DAF8D",     # mint accent, ~55% sat — metric highlights
    "grey":        "#767676",     # neutral text / arrows
    "grey_lt":     "#D4D4D4",     # light separator
    "dark":        "#1A2234",     # near-black for labels
    # Metric accent colors (cool family, darker shades)
    "m1":          "#1B5E86",     # deep slate — affinity gain
    "m2":          "#1A6A58",     # deep teal — data efficiency
    "m3":          "#2E6B48",     # deep green-teal — scaling law
}

# ─────────────────────────────────────────────────────────────────────────────
# Figure canvas: 12×6 inches, white background
# P12: top 8% reserved for title chrome (FLOW_Y set accordingly)
# ─────────────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(12, 6), facecolor=P["bg"])

# Full-canvas overlay for diagram elements
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis("off")
ax.set_facecolor(P["bg"])

FLOW_Y = 3.55   # centerline of pipeline elements

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def fbox(ax, cx, cy, w, h, fc, ec, lw=1.5, pad=0.14):
    """Rounded FancyBboxPatch."""
    p = mpatches.FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle=f"round,pad={pad}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3,
    )
    ax.add_patch(p)
    return p


def arrow(ax, x0, x1, y, color=None, lw=1.8):
    """Horizontal flow arrow."""
    color = color or P["grey"]
    ax.annotate("",
        xy=(x1, y), xytext=(x0, y),
        arrowprops=dict(arrowstyle="-|>", color=color,
                        lw=lw, mutation_scale=13),
        zorder=5)


def label(ax, x, y, txt, **kw):
    """ax.text with no per-call font override (P11)."""
    return ax.text(x, y, txt, ha=kw.pop("ha", "center"),
                   va=kw.pop("va", "center"), **kw)


# ─────────────────────────────────────────────────────────────────────────────
# Element 1 — Protein Binding Pocket
# ─────────────────────────────────────────────────────────────────────────────
pc_x, pc_y = 1.35, FLOW_Y

# U-shaped pocket (concave top)
theta = np.linspace(np.pi, 2*np.pi, 60)
px = pc_x + 0.60 * np.cos(theta)
py = pc_y - 0.48 + 0.68 * np.sin(theta)
px = np.concatenate([[pc_x - 0.60], px, [pc_x + 0.60]])
py = np.concatenate([[pc_y + 0.58], py, [pc_y + 0.58]])
ax.fill(px, py, color=P["teal_soft"], alpha=0.8, zorder=2)
ax.plot(px, py, color=P["teal"], linewidth=2.0, zorder=3)

# Binding residues (dots inside pocket)
for dx, dy in [(-0.22, -0.08), (0.0, -0.32), (0.22, -0.08), (-0.10, 0.20), (0.16, 0.24)]:
    ax.plot(pc_x + dx, pc_y + dy, "o",
            color=P["teal"], markersize=5.5, zorder=4)

label(ax, pc_x, pc_y - 1.05, "Protein Pocket",
      fontsize=9, fontweight="bold", color=P["dark"])
label(ax, pc_x, pc_y - 1.38, "binding target",
      fontsize=7.5, color=P["grey"], style="italic")

# ─────────────────────────────────────────────────────────────────────────────
# Arrow 1 → 2
# ─────────────────────────────────────────────────────────────────────────────
arrow(ax, 2.05, 2.60, FLOW_Y)

# ─────────────────────────────────────────────────────────────────────────────
# Element 2 — ChEMBL Retrieval
# ─────────────────────────────────────────────────────────────────────────────
re_x, re_y = 3.30, FLOW_Y
fbox(ax, re_x, re_y, 1.50, 1.82, fc=P["teal_soft"], ec=P["teal"], lw=1.5)

# Database stack icon (3 layered ellipses)
for i, shade in enumerate(["#97CEC7", "#BBDBD5", "#D4EEEA"]):
    yy = re_y + 0.52 - i * 0.26
    e = mpatches.Ellipse((re_x, yy), 0.85, 0.22,
                         facecolor=shade, edgecolor=P["teal"],
                         linewidth=0.9, zorder=4)
    ax.add_patch(e)

label(ax, re_x, re_y - 0.45, "ChEMBL",
      fontsize=9.5, fontweight="bold", color=P["dark"])
label(ax, re_x, re_y - 0.78, "ECFP4 top-k exemplars",
      fontsize=7.5, color=P["grey"], style="italic")

# ─────────────────────────────────────────────────────────────────────────────
# Arrow 2 → 3  (+  "exemplars" label)
# ─────────────────────────────────────────────────────────────────────────────
arrow(ax, 4.10, 4.58, FLOW_Y)
label(ax, 4.34, FLOW_Y + 0.24, "exemplars",
      fontsize=7, color=P["grey"])

# ─────────────────────────────────────────────────────────────────────────────
# Element 3 — RetroDiff Decoder (hero box, slightly larger)
# ─────────────────────────────────────────────────────────────────────────────
rd_x, rd_y = 5.88, FLOW_Y
fbox(ax, rd_x, rd_y, 2.10, 2.10, fc=P["blue_soft"], ec=P["blue"], lw=2.2, pad=0.16)

label(ax, rd_x, rd_y + 0.60, "RetroDiff",
      fontsize=12.5, fontweight="bold", color=P["blue"])
label(ax, rd_x, rd_y + 0.20, "Retrieval-Augmented",
      fontsize=8.0, color=P["dark"])
label(ax, rd_x, rd_y - 0.08, "Diffusion Decoder",
      fontsize=8.0, color=P["dark"])

# Stylised denoising squiggle (noisy → clean)
t = np.linspace(0, 2*np.pi, 100)
sq_x = rd_x - 0.60 + 1.20 * (t / (2*np.pi))
sq_y = rd_y - 0.62 + 0.16 * np.sin(5*t) * np.exp(-0.35*t)
ax.plot(sq_x, sq_y, color=P["blue"], linewidth=1.6, alpha=0.75, zorder=4,
        solid_capstyle="round")
# Arrow tip at end of squiggle
ax.annotate("", xy=(sq_x[-1], sq_y[-1]), xytext=(sq_x[-5], sq_y[-5]),
            arrowprops=dict(arrowstyle="-|>", color=P["blue"],
                            lw=1.2, mutation_scale=8), zorder=5)

# ─────────────────────────────────────────────────────────────────────────────
# Arrow 3 → 4
# ─────────────────────────────────────────────────────────────────────────────
arrow(ax, 6.99, 7.45, FLOW_Y)

# ─────────────────────────────────────────────────────────────────────────────
# Element 4 — Generated Molecule
# ─────────────────────────────────────────────────────────────────────────────
mol_x, mol_y = 8.18, FLOW_Y
ring_r = 0.40
# Benzene ring
for k in range(6):
    a0 = np.pi/6 + k * np.pi/3
    a1 = np.pi/6 + (k+1) * np.pi/3
    ax.plot([mol_x + ring_r*np.cos(a0), mol_x + ring_r*np.cos(a1)],
            [mol_y + ring_r*np.sin(a0), mol_y + ring_r*np.sin(a1)],
            color=P["blue"], linewidth=2.3, zorder=4, solid_capstyle="round")
# Alternating double bonds
inner_r = 0.23
for k in range(0, 6, 2):
    a0 = np.pi/6 + k * np.pi/3
    a1 = np.pi/6 + (k+1) * np.pi/3
    ax.plot([mol_x + inner_r*np.cos(a0), mol_x + inner_r*np.cos(a1)],
            [mol_y + inner_r*np.sin(a0), mol_y + inner_r*np.sin(a1)],
            color=P["blue"], linewidth=1.2, alpha=0.55, zorder=4)
# Substituent chain (top-right)
ex1 = mol_x + ring_r * np.cos(np.pi/6)
ey1 = mol_y + ring_r * np.sin(np.pi/6)
ex2, ey2 = ex1 + 0.32, ey1 + 0.28
ex3, ey3 = ex2 + 0.32, ey2 - 0.10
ax.plot([ex1, ex2], [ey1, ey2], color=P["blue"], lw=2.1, zorder=4)
ax.plot([ex2, ex3], [ey2, ey3], color=P["blue"], lw=2.1, zorder=4)
# OH substituent (bottom-right)  — use teal for contrast (still cool family)
ox1 = mol_x + ring_r * np.cos(-np.pi/6)
oy1 = mol_y + ring_r * np.sin(-np.pi/6)
ax.plot([ox1, ox1 + 0.34], [oy1, oy1 - 0.28],
        color=P["teal"], lw=2.0, zorder=4)
# P13: auto-sizing bbox for "OH" label
ax.text(ox1 + 0.42, oy1 - 0.36, "OH",
        ha="left", va="center", fontsize=7.5,
        fontweight="bold", color=P["teal"], zorder=5)

label(ax, mol_x, mol_y - 1.00, "Generated Molecule",
      fontsize=9, fontweight="bold", color=P["dark"])
label(ax, mol_x, mol_y - 1.33, "novel drug candidate",
      fontsize=7.5, color=P["grey"], style="italic")

# ─────────────────────────────────────────────────────────────────────────────
# Arrow 4 → 5
# ─────────────────────────────────────────────────────────────────────────────
arrow(ax, 8.98, 9.40, FLOW_Y)

# ─────────────────────────────────────────────────────────────────────────────
# Element 5 — Hit-rate bar chart (hero result)
# P3: y-axis range = data_min - 0.1*span to data_max + 0.15*span
# ─────────────────────────────────────────────────────────────────────────────
ax_bar = fig.add_axes([0.812, 0.225, 0.168, 0.575])
ax_bar.set_facecolor(P["bg"])

bar_vals = [1.0, 2.0]
bar_cols = [P["grey_lt"], P["blue"]]
bar_ecs  = [P["grey"],    P["blue"]]
ax_bar.bar(["Baseline\nDiffusion", "RetroDiff"], bar_vals,
           color=bar_cols, edgecolor=bar_ecs, linewidth=1.2, width=0.52, zorder=3)

# P3 tight y-range: data spans 1.0-2.0 → min-0.1*span to max+0.15*span
span = 1.0
ax_bar.set_ylim(bar_vals[0] - 0.1*span, bar_vals[1] + 0.15*span)

# ×2 annotation arrow + label (P13: text with auto bbox)
ax_bar.annotate("", xy=(1, 2.0), xytext=(1, 1.0),
                arrowprops=dict(arrowstyle="-|>", color=P["blue"],
                                lw=1.4, mutation_scale=10), zorder=4)
ax_bar.text(1.30, 1.50, "×2", fontsize=11, fontweight="bold",
            color=P["blue"], va="center", zorder=5)

ax_bar.set_ylabel("Hit Rate (rel.)", fontsize=8, color=P["grey"], labelpad=3)
ax_bar.set_title("Hit Rate", fontsize=9, fontweight="bold",
                 color=P["dark"], pad=5)
ax_bar.tick_params(axis="both", labelsize=7.5, length=2.5, width=0.7)
ax_bar.set_yticks([1.0, 1.5, 2.0])
ax_bar.set_yticklabels(["1×", "1.5×", "2×"], fontsize=7.5)
ax_bar.spines["left"].set_linewidth(0.8)
ax_bar.spines["bottom"].set_linewidth(0.8)
ax_bar.spines["right"].set_visible(False)
ax_bar.spines["top"].set_visible(False)

# ─────────────────────────────────────────────────────────────────────────────
# Metrics strip — three key claims (bottom of figure)
# P10: noun-phrase labels only
# ─────────────────────────────────────────────────────────────────────────────
STRIP_Y = 1.52
# Thin separator rule
ax.plot([0.6, 9.2], [STRIP_Y + 0.72, STRIP_Y + 0.72],
        color=P["grey_lt"], lw=0.8, zorder=1)

for xm, val, desc, col in [
    (2.00, "+18%",   "binding affinity gain\n(Vina docking score)", P["m1"]),
    (4.80, "60%",    "data-efficient training\n(matches baseline loss)", P["m2"]),
    (7.55, "R²>0.9", "scaling law confirmed\n(5 model sizes)", P["m3"]),
]:
    ax.text(xm, STRIP_Y + 0.28, val,
            ha="center", va="center", fontsize=14,
            fontweight="bold", color=col, zorder=5)
    ax.text(xm, STRIP_Y - 0.22, desc,
            ha="center", va="center", fontsize=7.5,
            color=P["grey"], zorder=5)
    ax.plot([xm - 0.55, xm + 0.55], [STRIP_Y + 0.00, STRIP_Y + 0.00],
            color=col, lw=0.9, alpha=0.45, zorder=4)

# ─────────────────────────────────────────────────────────────────────────────
# Headline sentence (≤12 words, embedded in figure, P13 auto-bbox)
# ─────────────────────────────────────────────────────────────────────────────
HEADLINE = "RetroDiff doubles hit rate over baseline diffusion at fixed compute."
ax.text(4.90, 0.56, HEADLINE,
        ha="center", va="center", fontsize=10.5, fontweight="bold",
        color=P["blue"], zorder=7,
        bbox=dict(facecolor=P["blue_soft"], edgecolor=P["blue"],
                  linewidth=1.3, boxstyle="round,pad=0.35"))

# ─────────────────────────────────────────────────────────────────────────────
# P12: Title chrome in top 8% of canvas (y > 5.52)
# ─────────────────────────────────────────────────────────────────────────────
ax.text(0.22, 5.76, "RetroDiff",
        fontsize=13.5, fontweight="bold", color=P["blue"],
        ha="left", va="center", zorder=5)
ax.text(0.22, 5.42, "Retrieval-Augmented Diffusion for Structure-Based Drug Design",
        fontsize=8.5, color=P["grey"],
        ha="left", va="center", zorder=5)

# ─────────────────────────────────────────────────────────────────────────────
# Zone labels (top of pipeline)
# ─────────────────────────────────────────────────────────────────────────────
for xc, lbl in [(1.35, "INPUT"), (3.30, "RETRIEVAL"),
                (5.88, "GENERATION"), (8.18, "OUTPUT"), (10.7, "RESULT")]:
    ax.text(xc, 5.12, lbl,
            ha="center", va="center", fontsize=7, color=P["grey"],
            fontweight="bold", zorder=5)

# ─────────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", bbox_inches="tight", dpi=300, facecolor=P["bg"])
fig.savefig("figure.png", bbox_inches="tight", dpi=300, facecolor=P["bg"])
fig.savefig("figure.svg", bbox_inches="tight", dpi=300, facecolor=P["bg"])
print("Saved: figure.pdf, figure.png, figure.svg")
