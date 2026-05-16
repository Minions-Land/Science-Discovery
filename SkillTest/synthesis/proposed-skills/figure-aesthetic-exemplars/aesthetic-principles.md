# Aesthetic Principles (R-future-2 from user feedback)

User-articulated 3-point principle, R-future-2 round 2026-05-17:

## Principle 1: 色调一致性 (Hue coherence)

**Pick ONE hue family per figure.** All non-grey signals should be hue-
coherent: e.g. all blue-cyan-teal, OR all red-pink-magenta, OR all
green-mint-yellow. Mixing red AND blue AND green at full saturation in
one figure breaks coherence.

The exception is **directional contrast**: a grey-dominant figure may use
ONE complementary signal hue for the contrast direction. Example: fig3
exemplar uses mostly grey + ONE red `#c04040` for treatment direction.

Cross-figure exemplars confirming this principle:
- diffusion_swiss_roll: pure cyan-teal family (#15c0c0/#15eac0/#15c095)
- manifold_holes: mint + cyan family (#c0eac0/#c0eaea)
- cellsplicenet_ablation: blue + mint + cyan (all cool family)
- fig4-single-cell-systems: warm signal #ea6a40 vs cool signal #6ac0c0
  (these ARE directional opposites, intentional diverging cmap)

Anti-exemplars (figures that VIOLATE coherence):
- Default matplotlib Tab10 cycle (blue/orange/green/red/purple) — every
  hue is a distinct hue family. This is what amateur figures default to.
- Bar chart with red/blue/green/orange — 4 hue families competing.

## Principle 2: 饱和度淡一点 (Reduced saturation)

**Saturated colours are visual noise.** Most exemplar figures use
~50-70% saturation, not 100%. Specifically:

| Element type | Saturation guideline |
|---|---|
| Background tint | 0-5% saturation (near-white off-white) |
| Neutral data (control, baseline) | 0-15% saturation (grey family) |
| Signal data (treatment, intervention) | 50-75% saturation, NOT full |
| Highlight / emphasis | 75-90%, only when truly directional |

The mint family (`#c0eac0`) at ~25% saturation, sitting next to neutral
grey, reads CLEAN. The same data plotted in fully saturated `#00ff00`
green reads CHEAP.

Cross-figure exemplars: diffusion_swiss_roll's #15c0c0 cyan is around
60% saturation; manifold_holes' #c0eac0 mint is around 25% saturation;
cellsplicenet's #154095 deep blue is around 80% saturation but balanced
by surrounding mint and grey neutrals.

## Principle 3: 有效显示面积 (Effective display area)

**Match the visual area of each subplot to the information it carries.**
A subplot showing 3 categorical bars does NOT need 180 mm of width.
A subplot showing a 30-row heatmap DOES need substantial vertical
extent.

Two specific failure modes:

### 3a: Bar charts wasting axis range
The y-axis 0-100 with bars at 60% leaves 40% empty. The user-articulated
rule: 假设数值越高越好，最低柱多出一点点就行 (lowest bar visible by a
small margin is enough). Implement via `set_ylim(data_min - 0.1*span,
data_max + 0.15*span)`. With negative values, NEVER use `(0, ytop)`.

### 3b: Subplots over-allocated to data they don't have
A bar plot with 3 categories doesn't need a wide canvas. A small bar
plot is more honest. Match panel width to data density:

```
panels with N categorical units: width ~ N * 0.5-0.8 inches
panels with longitudinal data (continuous x): width ~ 2-4 inches
panels with high-row count (heatmap, raster): height ~ 2-5 inches
```

Anti-exemplars: R5.C 7-panel candidate's panel D (3 categorical bars in
a wide-spanning panel — wasted 60% of horizontal space).

## Principle 4 (BACKPACK PROBLEM): Tight composition packing

After Principles 1-3 are satisfied per panel, arrange panels in the
composite via "backpack packing":

- Each panel claims its minimum-needed visual area (Principle 3).
- The composite tries to fit all panels into one rectangle with NO empty
  cells, NO over-stretched panels, MINIMAL inter-panel gutter (~5% canvas).
- Panel hierarchy comes from area allocation: hero panel gets ~30-45%
  of canvas; subordinates fill the remainder contiguously.
- gridspec subgridspec for nested 2x2 sub-regions tightens spacing when
  4 single-cell panels share a corner.

This is the layout discipline already encoded in figure-layout-defaults
Steps 1-6, with the addition of "minimum-area-per-panel" as the
optimisation target.

## Principle 5: 形式新颖 (Novel forms)

**Beyond bar / line / heatmap / box / violin lies a wider form
vocabulary.** When the data has structure that fits a non-standard form,
use that form. Examples:

- Manifold visualisation (diffusion_swiss_roll, manifold_holes): show
  the data's actual geometric structure
- Network / matrix combo (atlas-network-matrix): nodes + edges + matrix
  in one visual unit
- Image plate composite (atlas-image-plates): microscopy + annotation
  + scale bar overlay
- Radar / polar (atlas-radar-polar, comparison_radar): cross-method
  comparison along multiple axes
- Forest plot (atlas-forest-interval): per-subset effect + confidence
  interval at a glance

Form novelty WITHOUT information density is decoration. Form novelty WITH
high information density is what makes "human-can't-easily-do-this" figures.

## How these principles compose

The R-future-2 hierarchy:

1. Principle 5 first (pick the right form)
2. Principle 3 next (match visual area to information)
3. Principle 4 (compose the composite)
4. Principles 1+2 (apply hue coherence + reduced saturation)

Principles 1+2 alone give "色彩规范"; Principles 3+4 alone give
"排版规整"; Principle 5 alone gives "新颖形式." All five together
approach the user's "美感 / 超越人类" target.


---

## R-future-2 user feedback updates (2026-05-17)

User graded 6 novel-form exemplars. New sub-rules distilled:

### Principle 1 sub-rule: red-vs-teal is a known bad pairing

User-flagged on `atlas-network-matrix.png`: heatmap with red and "湖水绿"
(teal `#95c0c0`-ish) at the same saturation reads as ugly. Avoid this
specific high-complementary pair when both colours are at >40% saturation.

Fix when matrix accompanies a network: keep the matrix in the network's
hue family (single-hue diverging within teal: `#154040` → `#c0eaea`
via TwoSlopeNorm) rather than introducing a complementary signal hue.

### Principle 2 sub-rule: stroke weight compensates for low saturation

Pastel fills (`#c0eac0`, `#eac0c0`, etc at ~25% saturation) need
DOUBLED stroke weight to keep the polygon / shape boundary visible.

```python
# pastel fill + bumped stroke
ax.fill(x, y, color=pastel, alpha=0.25)
ax.plot(x, y, color=pastel, linewidth=2.2)  # NOT default 1.0
```

User-confirmed on `comparison_radar.png`: 唯一美中不足的是外围边可以再
粗一点.

### Principle 3 sub-rule: legend packing for hybrid composites

When a multi-form panel uses a legend, prefer ncol≥2 (multi-column)
legend over default single-column. Single-column legend in upper-left
of a hybrid panel creates whitespace gap above the data.

User-feedback on `cellsplicenet_ablation.png`: 注意一下 Legend 的设置，
可以分成两列，这样就能取消掉左上角的一些留白.

```python
ax.legend(ncol=2, loc='upper left', frameon=False)
```

### Principle 4 sub-rule: image plate inter-panel gutter ≤ 2%

Standard chart inter-panel gutter is ~5-6% canvas. Image plates
(microscopy, spatial transcriptomics, A-Z grid composites) tighten
this to ≤2% because the panels are spatially related and the data
is the IMAGE itself, not a chart.

User-feedback on `atlas-image-plates.png`: A 到 P 的排列可以再紧凑一点.

### Principle 5 sub-rule: manifold visualisation > flat chart when geometry IS the message

When data has natural 2D/3D geometric structure (manifold, embedding,
trajectory, branching tree), default to the geometric form FIRST.
Flatten to bar/line ONLY when the geometric structure is irrelevant
or unavailable.

User-confirmed on `diffusion_swiss_roll.png` and `manifold_holes.png`:
整个流形系列我觉得都挺不错.

This is the form-novelty axis: data with manifold structure → manifold
visualisation, not "PCA-reduce then bar chart of cluster means."

### Principle 6 (NEW): polar plot for N×M cross-comparison

When data is N methods × M metrics with M ≥ 3, default to polar /
radar form. The shape signature each method generates carries
information that bar charts cannot.

User-confirmed on `comparison_radar.png`: 这张图真的太漂亮了，看起来
非常正规、正经.

Apply with: low-saturation pastel polygon fills + grey-dominant radar
grid + bumped stroke weight (Principle 2 sub-rule) + radial axis
labels inline.

## Updated grading rubric (R-future-2)

| User grade | Aesthetic-principle compliance |
|---|---|
| 非常漂亮 / 真的太漂亮 | ALL of P1-P6, with appropriate sub-rules |
| 还不错 / 挺好看 | 4-5 of P1-P6 satisfied |
| 中规中矩 / 规整但缺色彩 | P3-P4 satisfied, P1-P2 partial |
| 一般 / 还可以 | 2-3 of P1-P6 |
| 显得很普通 / normal | <2 of P1-P6 |


---

## R-future-3 user feedback corrections (2026-05-17)

User R-future-3 grading exposed 4 hard rules I had encoded incorrectly:

### CORRECTION to Principle 1 (色调一致性)

**WRONG interpretation:** P1 means "single hue + saturation gradient
within one hue."

**CORRECT interpretation:** P1 means "all hues within a coherent
**family** (e.g. all cool, or all warm, or all neutral with one accent),
but ≥ 3 distinct hues are FINE if they are family-coherent."

User-articulated R-future-3: "颜色一致性强但区分度不够 — 用深浅做区分
根本区分不了，尤其是 parallel coords 有这么多线再用深浅就更乱了."

The reference `comparison_radar.png` (user-graded "最完美") uses:
- Mint pastel `#c0eac0`
- Red-pink pastel `#eac0c0`
- Cyan pastel `#c0eaea`

These are 3 DIFFERENT hues — but all at ~25-30% saturation, all in the
"cool-warm pastel" family. Hue diversity gives DISTINGUISHABILITY;
saturation discipline gives COHERENCE.

**Implementation rule:**
- For data with N≥3 categories, use N hues from the SAME saturation
  band (all ~25-30% sat OR all ~70-80% sat) within the same temperature
  family (all cool OR all warm).
- NEVER use saturation-gradient-of-single-hue when the user must
  distinguish ≥ 3 categories. The eye cannot reliably distinguish
  4 levels of "blue" the way it distinguishes "blue / mint / cyan."

### Principle 7 (NEW): legend placement off the data plot

User R-future-3 on radar candidate: "底下的 Legend 和数据集重叠了."

**Rule:** for polar / radar / network / dense-overlay plots, the legend
MUST sit outside the data plot region. Default `loc="lower center"`
or `loc="best"` often falls inside the data region.

Use:
```python
ax.legend(bbox_to_anchor=(1.05, 0.5), loc="center left", frameon=False)
# OR
ax.legend(bbox_to_anchor=(0.5, -0.15), loc="upper center", ncol=N, frameon=False)
```

For polar plots specifically, `bbox_to_anchor=(1.15, 0.5), loc="center left"`
positions the legend cleanly to the right of the polygon.

### Principle 8 (NEW): manifold figures carry 1-2 information dimensions max

User R-future-3 on manifold candidate: "好乱，奇怪的线条，颜色太亮丽。
整体太乱了，乱七八糟的."

**Cause:** I had Codex stack trajectory + pseudotime gradient + cluster
labels + bifurcation marker + connecting lines all on one panel. Five
information dimensions on one geometric structure = visual chaos.

**Rule:** a manifold visualisation should carry ONE primary information
(the geometric structure itself) PLUS at most ONE secondary information
(pseudotime gradient via colour, OR cluster identity via colour, OR
expression value via colour — not all of them).

If you need 2+ secondary dimensions, split into 2 panels:
- Panel left: manifold + colour by pseudotime
- Panel right: same manifold + colour by cluster

The reference `diffusion_swiss_roll` carries exactly ONE secondary
dimension (saturation gradient) on the manifold. That is what makes
it readable.

### Principle 9 (NEW): comparison_radar is the SkillTest "beyond human" anchor

User R-future-3: "comparison_radar 是今晚最完美的图. 这张图真的太漂亮了."

This figure is the empirical anchor for what "beyond human" means in
SkillTest. Specifically:

- 77% grey foreground (Principle 1 family + Principle 2 saturation)
- 3 distinct hue pastels for distinguishability (corrected P1 family rule)
- Polygon stroke 2-2.5x default for pastel-fill compensation (P2 sub-rule)
- Radial axis labels inline (P3 effective area)
- 5+ methods overlapped (high information density per area)
- No legend block competing (Principle 7 sub-rule, legend off-plot)

When in doubt, ask: "is this getting closer to comparison_radar's
visual quality?" If no, the candidate is not yet beyond-human.

## Updated grading anchors (R-future-3)

| User grade | Aesthetic-principle compliance |
|---|---|
| 最完美 / 真的太漂亮 (= comparison_radar tier) | ALL of P1-P9 + matches Principle 9 anchor |
| 非常漂亮 / 真的太漂亮 | ≥7 of P1-P9 |
| 还不错 / 挺好看 | 5-6 of P1-P9 |
| 中规中矩 / 规整 | 3-4 of P1-P9 |
| 太普通 / 一般 | 2-3 of P1-P9 |
| 太乱 / 一坨大垃圾 | <2 of P1-P9 OR contradicts a principle |


---

## R-future-3-final user feedback corrections (2026-05-17)

After v2 grading round, user articulated 2 more rules:

### Principle 3 sub-rule (REVISED after v3 rejection): honest sparse scatter

User R-future-3-final v3 rejection: "你扩大这玩意儿没什么用. 本来很散的
东西，你变得好像有点像多边形了，这有什么用呢? 还变得更丑了."

**Rule:** when the data IS scattered, do NOT visually inflate it. Default
marker size `s=12-15` for hero scatter is correct. Do NOT add convex-hull
shading, KDE density bands, or other "fill the canvas" decorations.

The Principle 3 (effective display area) DOES NOT mean "make sparse data
look dense." It means:
- Match panel size to data density (small bar plot for 3 categorical bars,
  large heatmap for 30+ rows).
- Tighten axis range to data span (the negative-value patch).
- Don't waste 35% of bar-chart canvas on empty axis range.

But when data is GENUINELY sparse, the sparseness is the information.
A scatter plot that LOOKS scattered tells the truth; one with hull shading
tells a lie.

**Correct manifold-scatter exemplar:** `manifold_scatter_4cluster.png`
in the gallery. Marker `s=12-15`, no hull shading, tight axes, 4 distinct
pastel hues for cluster identity, inline labels with white halo.

**Anti-exemplar (rejected v3):** `case-manifold/candidate_v3.png` with
convex-hull shading was rejected by user. Don't repeat.

### Principle 9 reaffirmed: comparison_radar is the module template

User R-future-3-final on radar: "对于 Radar，你可以直接把 Reference 当成
模板了，不需要再讨论别的. 在其他方案上改来改去，颜色都不如 Reference 好看."

**Rule:** for polar / radar plots specifically, do NOT attempt to
generate a new exemplar. Use `comparison_radar.png` as the literal
template. Diff your candidate's polygon palette against
comparison_radar's pastel hex values; replicate them.

This is the empirical limit case: when an exemplar is "as good as it
gets," exemplar-driven workflow says copy, don't innovate.

## R-future-3 final principle list

The skill now has:
- P1 hue coherence (corrected: family-coherent, ≥3 distinct hues OK)
- P2 reduced saturation (with stroke compensation sub-rule)
- P3 effective display area (with negative-value patch + scatter-point-size sub-rule)
- P4 backpack packing (with image-plate-gutter sub-rule)
- P5 form novelty (manifold > flat when geometry is the message)
- P6 polar > grouped bar for N×M cross-comparison
- P7 legend off-plot for polar / dense overlay
- P8 manifold carries 1-2 information dimensions max
- P9 comparison_radar is the "beyond human" anchor (literal template for radar)

9 principles + ~12 sub-rules. The skill is now mature for the SkillTest
port plan.
