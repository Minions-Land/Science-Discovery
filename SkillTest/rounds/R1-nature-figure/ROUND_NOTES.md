# Round Notes — R1.A nature-figure  (REVISED 2026-05-16)

**Cases:** case-bar, case-heatmap, case-multi-panel
**Status:** Revised after user visual review (initial verdict was based on
code-layer evidence + structural inspection only; user opened the figures and
called out layout failures that the structural rubric missed).

## Headline

The skill teaches **content discipline** but not **layout slack**. Two of
three cases ended up unsubmittable because the runner applied mm-precision
figsize without giving legend/caption/density their breathing room. The
heatmap case (where canvas size was naturally generous) is the only one
where the skill was a clean win.

User's verbatim assessment:

- case-bar: "candidate 完全就挤在了一起，丝毫都没有排版，根本用不了 啊，太垃圾了。
  baseline 还能用啊，虽然非常的朴素，颜色也很磨人，但是起码显示是正常的。"
- case-multi-panel: "baseline 的排版是最正确的，非常合理！超级厉害，但是颜色比较朴素。
  candidate 颜色可能稍微漂亮点，但是排版全错。"
- case-heatmap: "candidate 这次排版会更好一点，但是颜色两者没啥质的差别。"

## Aggregate scores (revised)

| Case | Baseline | Candidate | Δ | Bucket |
|---|---|---|---|---|
| case-bar | 12 / 19 | 13 / 19 | +1 | Overreaches (partial) |
| case-heatmap | 13 / 19 | 18 / 19 | +5 | Calibrates response |
| case-multi-panel | 15 / 22 | 15 / 22 | 0 | Overreaches |
| **Mean (normalised /22)** | **70%** | **78%** | **+8 pp** |

(Initial scoring without visual evidence had this at 47% → 100%, +53 pp. The
gap between code-layer and visual-layer evidence is exactly what the skill's
structural-only rubric needed — and what the user caught when I missed it.)

## What the skill actually delivers (revised)

Real wins that hold up visually:

1. **Editable text in vector outputs** (`svg.fonttype="none"` + `pdf.fonttype=42`
   + explicit `font.sans-serif`). Pure win on every case.
2. **PALETTE dict pattern for cross-panel colour coherence.** Pure win on
   multi-panel, irrelevant on single-panel.
3. **`TwoSlopeNorm(vcenter=0)` for diverging colormaps.** Pure win on heatmap.
4. **Outside-tick discipline** (`direction="out", length=2.2-2.5, width=0.6-0.7`).
   Pure win where applied.
5. **Statistical-annotation recipes** (CI bands, EC50 inline labels, pairwise
   significance). Pure wins where applied.

Things the skill caused that hurt:

1. **mm-precision figsize without slack budget.** When the brief says "single
   column ~85 mm wide", the skill's literal `(85/25.4, 58/25.4)` translation
   crammed legend + caption + density into 58 mm height. `constrained_layout
   collapsed to zero` warning was the canary; I missed it.
2. **Asymmetric L-shaped gridspec for "hero panel".** The simpler
   `width_ratios=[2,1,1] + bottom-spanning D` (which baseline used by
   accident) is the standard 4-panel hero. The skill nudged the runner to a
   gs with empty quadrants.
3. **Hatch + alpha-graded single-hue at 7-pt body for 4-series bar.**
   Greyscale-safe in theory, visually noisy in practice at small canvas.

## Token economics

Unchanged. Candidate ~23x baseline input, ~1.5x output. The premium would be
worth it if the layout were submittable. With the current skill, it's not on
2 of 3 cases.

## Recommendation (revised)

`fork-narrowly`. Take the **content discipline**, leave the **layout
discipline** behind:

### Port into `minions/roles/writer/skills/academic-plotting.md`

- The rcParams block: `font.family/sans-serif`, `svg.fonttype="none"`,
  `pdf.fonttype=42`, top/right spines off, axis linewidth, legend frame off.
- A PALETTE-dict pattern for cross-panel colour coherence with the
  "reserve green/red for directional signals" rule.
- `TwoSlopeNorm(vcenter=0)` recipe for diverging heatmaps.
- Outside-tick discipline.
- CI band, EC50 inline label, pairwise-vs-control significance recipes
  (panel-level, not figsize-coupled).

### Do NOT port

- mm-precision `figsize=(width_mm/25.4, height_mm/25.4)` patterns. Keep
  inches-default, compress to mm only at submission packaging stage,
  after layout is visually confirmed.
- Asymmetric L-shape `gs[0:2, 0:2] + gs[1:, 2:]` "hero" recipe. Default
  hero pattern for 4-panel composites should be
  `width_ratios=[2,1,1] + bottom-spanning panel D`.
- Hatch + 4-series single-hue gradient at body fontsize <= 7-pt.

### Add as a new rule (not in nature-figure)

- "Tight figsize requires layout-budget triage": choose at most one of
  {above-axes legend, below-axes caption, in-axes significance brackets}
  per figure. The default for tight figsize is "legend in-axes, caption
  external in figure metadata or paper text".
- "No empty quadrants in gridspec": if the chosen grid leaves a cell with
  no panel, either extend a panel or pick a smaller grid.
- "`constrained_layout collapsed to zero` is a hard fail, not cosmetic":
  re-render at a larger figsize before saving.

## Methodology lesson (for the benchmark itself)

The R1.A failure of my own evaluation was: I trusted code-layer evidence
(rcParams set correctly, palette dict present, gridspec asymmetric) over
the rendered output. The user did the right thing by opening the SVGs and
calling out what was actually wrong.

Updates to `SkillTest/README.md`:

1. **Visual inspection is mandatory before scoring**, not optional. Code-
   layer evidence is necessary but not sufficient for figure rounds. If
   Read tool's image rendering is unavailable, save full-page Playwright
   screenshots and compare side-by-side, or generate `pdftotext` /
   image-diff metadata.
2. **`constrained_layout collapsed to zero` is a hard fail**, not a
   cosmetic warning. Re-render or fail the case.
3. **Score by rendered artefact, not by code intent.**

## Open questions for next round

- Does `scientific-figure-making` (R1.B) have the same layout-overshoot
  failure mode at small figsize, or does its lighter rule set leave more
  layout slack?
- For R1.C (text-only), the layout overshoot failure mode doesn't apply.
  Visual inspection is less critical there. But the equivalent — "the skill
  applied prescriptively when the brief didn't ask" — should be watched.
