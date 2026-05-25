# Aesthetic Principles (R-future-2 from user feedback)

User-articulated 3-point principle, R-future-2 round 2026-05-17:

## Principle 1: Hue coherence

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

## Principle 2: Reduced saturation

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

## Principle 3: Effective display area

**Match the visual area of each subplot to the information it carries.**
A subplot showing 3 categorical bars does NOT need 180 mm of width.
A subplot showing a 30-row heatmap DOES need substantial vertical
extent.

Two specific failure modes:

### 3a: Bar charts wasting axis range
The y-axis 0-100 with bars at 60% leaves 40% empty. The user-articulated
rule: assuming higher is better, the lowest bar only needs to extend a
small amount (just enough to be visible). Implement via
`set_ylim(data_min - 0.1*span, data_max + 0.15*span)`. With negative
values, NEVER use `(0, ytop)`.

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

## Principle 5: Novel forms

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

Principles 1+2 alone give "disciplined colour"; Principles 3+4 alone give
"clean layout"; Principle 5 alone gives "novel form". All five together
approach the user's "beautiful / beyond-human" target.


---

## R-future-2 user feedback updates (2026-05-17)

User graded 6 novel-form exemplars. New sub-rules distilled:

### Principle 1 sub-rule: red-vs-teal is a known bad pairing

User-flagged on `atlas-network-matrix.png`: heatmap with red and lake-water
teal (`#95c0c0`-ish) at the same saturation reads as ugly. Avoid this
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

User-confirmed on `comparison_radar.png`: "the only thing missing is that the
outer polygon stroke could be a bit thicker."

### Principle 3 sub-rule: legend packing for hybrid composites

When a multi-form panel uses a legend, prefer ncol≥2 (multi-column)
legend over default single-column. Single-column legend in upper-left
of a hybrid panel creates whitespace gap above the data.

User-feedback on `cellsplicenet_ablation.png`: "watch the legend setting —
splitting it into two columns gets rid of the wasted whitespace in the
upper-left corner."

```python
ax.legend(ncol=2, loc='upper left', frameon=False)
```

### Principle 4 sub-rule: image plate inter-panel gutter ≤ 2%

Standard chart inter-panel gutter is ~5-6% canvas. Image plates
(microscopy, spatial transcriptomics, A-Z grid composites) tighten
this to ≤2% because the panels are spatially related and the data
is the IMAGE itself, not a chart.

User-feedback on `atlas-image-plates.png`: "the A-through-P arrangement
could be packed tighter."

### Principle 5 sub-rule: manifold visualisation > flat chart when geometry IS the message

When data has natural 2D/3D geometric structure (manifold, embedding,
trajectory, branching tree), default to the geometric form FIRST.
Flatten to bar/line ONLY when the geometric structure is irrelevant
or unavailable.

User-confirmed on `diffusion_swiss_roll.png` and `manifold_holes.png`:
"the entire manifold series is solid — I think they all look good."

This is the form-novelty axis: data with manifold structure → manifold
visualisation, not "PCA-reduce then bar chart of cluster means."

### Principle 6 (NEW): polar plot for N×M cross-comparison

When data is N methods × M metrics with M ≥ 3, default to polar /
radar form. The shape signature each method generates carries
information that bar charts cannot.

User-confirmed on `comparison_radar.png`: "this figure is genuinely
beautiful — it looks really proper, really professional."

Apply with: low-saturation pastel polygon fills + grey-dominant radar
grid + bumped stroke weight (Principle 2 sub-rule) + radial axis
labels inline.

## Updated grading rubric (R-future-2)

| User grade | Aesthetic-principle compliance |
|---|---|
| "very beautiful" / "genuinely beautiful" | ALL of P1-P6, with appropriate sub-rules |
| "pretty solid" / "looks good" | 4-5 of P1-P6 satisfied |
| "passable" / "tidy but lacks colour life" | P3-P4 satisfied, P1-P2 partial |
| "okay" / "fine" | 2-3 of P1-P6 |
| "very generic" / "normal" | <2 of P1-P6 |


---

## R-future-3 user feedback corrections (2026-05-17)

User R-future-3 grading exposed 4 hard rules I had encoded incorrectly:

### CORRECTION to Principle 1 (hue coherence)

**WRONG interpretation:** P1 means "single hue + saturation gradient
within one hue."

**CORRECT interpretation:** P1 means "all hues within a coherent
**family** (e.g. all cool, or all warm, or all neutral with one accent),
but ≥ 3 distinct hues are FINE if they are family-coherent."

User-articulated R-future-3: "the hue coherence is strong but the
distinguishability is not — using shade gradients alone can't separate
categories, especially for parallel coords with this many lines using
shade gets even messier."

The reference `comparison_radar.png` (user-graded "the most perfect") uses:
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

User R-future-3 on radar candidate: "the legend at the bottom is
overlapping with the dataset."

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

User R-future-3 on manifold candidate: "really messy, weird stray lines,
the colours are too garish. The whole thing is a chaotic mess."

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

User R-future-3: "comparison_radar is tonight's most perfect figure. This
figure is genuinely beautiful."

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
| "most perfect" / "genuinely beautiful" (= comparison_radar tier) | ALL of P1-P9 + matches Principle 9 anchor |
| "very beautiful" / "genuinely beautiful" | ≥7 of P1-P9 |
| "pretty solid" / "looks good" | 5-6 of P1-P9 |
| "passable" / "tidy" | 3-4 of P1-P9 |
| "too generic" / "okay" | 2-3 of P1-P9 |
| "too messy" / "a pile of garbage" | <2 of P1-P9 OR contradicts a principle |


---

## R-future-3-final user feedback corrections (2026-05-17)

After v2 grading round, user articulated 2 more rules:

### Principle 3 sub-rule (REVISED after v3 rejection): honest sparse scatter

User R-future-3-final v3 rejection: "blowing this thing up is pointless.
The data was naturally scattered, and you've made it look kind of like a
polygon — what's the point of that? It actually got uglier."

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

User R-future-3-final on radar: "for the radar, you can just treat the
reference as the template — there's nothing else to discuss. Anything
you tweak in other versions, the colours never look as good as the
reference."

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

---

## R-future-4 user feedback (2026-05-21, from EACN3 figure review)

### Principle 10: text economy — less annotation is more

User feedback on figureX_v4: "the text content is a bit too much".

**Rule:** every annotation, axis label, and in-panel text element must earn its place. Default to removing rather than adding.

Concrete checklist before finalising a figure:
- Can this annotation be replaced by a well-chosen axis tick or a legend entry? If yes, remove it.
- Does this label repeat information already in the panel title or caption? If yes, remove it.
- Are there more than 2 annotation arrows on a single panel? If yes, keep only the 2 most load-bearing events; move the rest to the caption.
- Is the annotation text longer than ~4 words? Shorten to a noun phrase or abbreviation.

**Anti-pattern (from figureX_v4):** panel b had 4 annotation arrows (Math joins, Immuno frozen, kNN bias, 4 version stars) plus a gap label — borderline too dense. Panel d had 3 annotation arrows + a v3.0 diamond label. Acceptable for a first draft; trim before camera-ready.

**Sub-rule — panel c sankey:** detector/item/artifact labels were shortened from full sentences to noun phrases (e.g. "Marker Jaccard claim" → "Marker Jaccard") specifically to respect this principle. Apply the same shortening discipline to any flow/sankey diagram.

### Principle 11: font unification — one font stack per figure, locked at script top

User feedback on figureX_v4: "fonts should be as unified as possible across every version of the figure".

**Rule:** the font stack is set ONCE in the `mpl.rcParams.update({...})` block at the top of the script and never overridden per-element. Every `ax.text`, `ax.annotate`, `ax.set_xlabel`, `ax.set_title`, and `fig.text` call inherits from rcParams — no `fontfamily=`, `fontname=`, or `font=` kwargs anywhere else in the script.

```python
# CORRECT — set once, inherit everywhere
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
})
```

**Anti-pattern:** calling `ax.set_title("...", fontfamily="Times New Roman")` or `ax.text(..., font="Courier")` anywhere in the script. These per-call overrides create font inconsistency that is invisible in the script but visible in the rendered PDF.

**Verification:** after rendering, run `grep -c '<text' fig.svg` to confirm all text nodes are present, then open the SVG in a text editor and spot-check that no `font-family` attribute appears on individual `<text>` elements (they should all inherit from the `<style>` block at the top).

**Cross-version consistency:** if the figure is regenerated across multiple sessions or by different people, the rcParams block is the single source of truth. Pin it in a comment:
```python
# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.
```

## Updated principle list (R-future-4)

- P1 hue coherence (family-coherent, ≥3 distinct hues OK)
- P2 reduced saturation (with stroke compensation sub-rule)
- P3 effective display area (with negative-value patch + scatter-point-size sub-rule)
- P4 backpack packing (with image-plate-gutter sub-rule)
- P5 form novelty (manifold > flat when geometry is the message)
- P6 polar > grouped bar for N×M cross-comparison
- P7 legend off-plot for polar / dense overlay
- P8 manifold carries 1-2 information dimensions max
- P9 comparison_radar is the "beyond human" anchor (literal template for radar)
- **P10 text economy — annotate less; every text element must earn its place**
- **P11 font unification — one font stack in rcParams, never overridden per element**

---

## R-future-5 user feedback (2026-05-21, second EACN3 figure review)

This round caught failure modes that programmatic text-bbox audits miss when
they only inspect `ax.texts`. The lessons feed both new principles (P12-P14)
and the visual-format-check skill's audit-coverage requirements.

### Principle 12: layout budgets reserve space for figure-level chrome BEFORE
laying out panels

User feedback: the global title "Eight-agent collaboration on EACN3..." and
its subtitle line ("T0=... TEND=... wall-clock 64.9 h ...") collided with
the top row's panel titles ("Eight-agent collaboration on EACN3" repeated
in panel a, "Real-time commit stream (n=487)" in panel b). All three layers
of text rendered into the same 2 % strip at the top of the figure and read
as visual mush.

**Rule:** when a figure has both a global `fig.text` title block AND
per-panel `ax.set_title` calls, the gridspec must reserve **at least
5 % of figure height** above the top row for the global block. Concretely:
`fig.add_gridspec(..., top=0.92)` or lower if the title block is
multi-line, NOT `top=0.965`. The default matplotlib `figure.subplotpars.top
= 0.88` is right; the temptation to push it higher to "use the space"
is wrong.

**Anti-pattern:** `top=0.965` + `fig.text(0.05, 0.985, ...)` (title) +
`fig.text(0.05, 0.972, ...)` (subtitle) + `ax.set_title(...)` per panel —
all four lines collapse into a 1.5 % strip. R-future-5 reproducer.

**Companion sub-rule for the audit pipeline:** any audit that only checks
`ax.texts`/`ax.title`/`ax.xaxis.label`/`ax.yaxis.label`/`ax.get_xticklabels`
will MISS this defect. The audit must also iterate `fig.texts` and check
each one against every panel's `get_window_extent()`. See the
`visual-format-check` skill's coverage requirement.

### Principle 13 (revised after R-future-5b): use auto-sizing boxes — never fixed-width Rectangle around variable text

User feedback on panel c: items were originally drawn as fixed-width
`mpatches.Rectangle((x_mid-0.13, y-0.022), 0.26, 0.044, ...)` with text
inside. Long labels ("Real-pancreas attrib.", "ref_subsample_kNN") visually
overflowed the rectangle.

First-attempt fix (DROP the box, use bare colored text): user rejected as
ugly — user said "removing the boxes makes it ugly too". Correct fix:

**Rule:** never draw a fixed-width Rectangle/FancyBboxPatch and then place
text inside via a separate `ax.text()` call. Always use the `bbox=` kwarg
on `ax.text()`, which auto-sizes the box around the rendered text width:

```python
# WRONG — fixed width, text overflows long labels
ax.add_patch(Rectangle((x-0.13, y-0.022), 0.26, 0.044,
                        facecolor="white", edgecolor=color, lw=0.7))
ax.text(x, y, name, fontsize=7, ...)

# RIGHT — auto-sized box hugs the text
ax.text(x, y, name, fontsize=7, color=text_color,
        ha="center", va="center", fontweight="bold",
        bbox=dict(facecolor=soft_fill, edgecolor=accent_color, lw=0.7,
                  boxstyle="round,pad=0.30"))
```

**The box still carries semantic meaning** when the encoding is per-item
kind (e.g. retracted-claim items wear a red soft-fill box, bug items wear
an amber soft-fill box). The box is not decoration — it is the kind
glyph. Removing it leaves only the text color encoding the kind, which
the user found visually empty.

**Soft-fill + dark-text pattern** for kind-coded items:
- Retracted claim: `facecolor="#f6dcd5"` (soft red), `edgecolor=ACCENT`,
  text color `"#7a2a20"` (dark red)
- Bug: `facecolor="#f3e3c5"` (soft amber), `edgecolor="#b07d2f"`,
  text color `"#6b4818"` (dark amber)

Soft fill keeps P2 (reduced saturation) compliant; dark text keeps
contrast readable; the auto-sized box can never overflow because it grows
with content.

### Principle 14 (revised after R-future-5b): legend swatch is a real filled patch, color-matched to the encoding

User feedback on panel c: "the legend has some issues".

The legend has to show "this red soft-fill box = retracted claim" — and
the user must read that mapping at a glance. Three failure modes accrue:

1. **Two separate primitives** (Rectangle + Text) drift apart on different
   matplotlib backends.
2. **Unicode swatch (▪)** is too small to read as a "swatch", and its
   antialiasing depends on the font.
3. **White-fill swatch + colored edge** doesn't match the actual item
   style (which uses soft fill + colored edge), so the reader has to
   re-derive the encoding.

**Rule:** the legend swatch must be drawn with the same primitive and
same fill/edge colors as the item it explains:

```python
# Item style:
ax.text(x, y, name, ..., bbox=dict(facecolor="#f6dcd5", edgecolor=ACCENT, ...))

# Legend swatch — same fill, same edge:
ax.add_patch(mpatches.FancyBboxPatch(
    (lx, ly - h/2), w, h,
    boxstyle="round,pad=0.005,rounding_size=0.005",
    facecolor="#f6dcd5", edgecolor=ACCENT, lw=0.7))
ax.text(lx + w + 0.02, ly, "retracted claim (4)", ...)
```

The reader sees a small chip in the same color and shape as the item
chips, with a label next to it. The mapping is now graphical, not
textual.

**Anti-patterns:**
- White-fill swatch ("two thin colored rectangles" with no fill).
- Unicode ▪ as swatch.
- Rectangle that doesn't match the item's `boxstyle` (e.g. sharp-cornered
  legend swatch when items use rounded corners).

## R-future-5 audit-coverage gap

This round revealed that the previous audit pass reported "0 defects"
while the figure had visible overflow. The audit was incomplete. Required
coverage:

| Coverage | Check |
|---|---|
| `ax.texts` | in-panel annotations |
| `ax.title` / `ax.xaxis.label` / `ax.yaxis.label` | titles + axis labels |
| `ax.get_xticklabels()` + `ax.get_yticklabels()` | tick labels (long compartment names cross neighboring panels) |
| `fig.texts` | global title/subtitle blocks (R-future-5 main miss) |
| Inter-panel collision | text from panel A's bbox overlapping panel B's bbox |
| Text-over-image | text from panel A overlapping an image in panel B |
| Auto-extending log axes | `ax.set_xscale("log")` adds 10^N ticks past `xlim` — pin ticks with `FixedLocator` |

Defect counts at any stage should not be trusted as "clean" unless ALL
seven coverage rows have fired their checks. See visual-format-check
skill's "Required coverage" appendix.

## R-future-5 final principle list

- P1 — P9 unchanged (hue / saturation / area / packing / form / polar /
  legend-off-plot / manifold-dim / radar template)
- P10 text economy
- P11 font unification (rcParams pinned, no per-element override)
- **P12 layout budget — reserve ≥5 % top for global chrome before panels**
- **P13 drop boxes when content overflows them — color text instead**
- **P14 legend swatch matches the encoding it explains (color-on-color, single bbox)**

Updated grading anchors:

| User grade | Aesthetic-principle compliance |
|---|---|
| "most perfect" / "genuinely beautiful" (= comparison_radar tier) | ALL of P1-P14 + matches P9 anchor |
| "very beautiful" / "genuinely beautiful" | ≥12 of P1-P14 |
| "pretty solid" / "looks good" | 8-11 of P1-P14 |
| "passable" / "tidy" | 5-7 of P1-P14 |
| "too generic" / "okay" | 3-4 of P1-P14 |
| "too messy" / "a pile of garbage" | <3 of P1-P14 OR contradicts a principle |
