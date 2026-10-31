---
slug: figure-layout-defaults
summary: Default 4-panel hero is width_ratios=[2,1,1] + bottom-spanning D; figsize in inches first, mm only at submission; no empty quadrants, no over-stretched panels, no constrained_layout collapse.
layer: logical
tools:
version: 2
status: active
supersedes:
references: academic-plotting, pdf-vector-layout
provenance: SkillTest-R1.A-and-R1.B-case-multi-panel
---

# Skill — Figure Layout Defaults

Layout discipline that two existing CNS figure skills (nature-figure,
scientific-figure-making) both fail to teach. The content-discipline rules
they DO teach (rcParams, palette, editable text) are covered separately in
[[academic-plotting]]; this skill covers the geometry decisions both skills
get wrong on multi-panel composites.

## When to invoke

- Any multi-panel figure (≥2 panels) for a paper, not a quick exploratory plot.
- Any single-panel figure where the brief specifies submission dimensions
  (single-column ~85 mm, two-column ~180 mm) — the figsize-vs-density rule applies.
- Whenever a figure script includes legend + caption + statistical brackets
  in the same axes.

## Procedure

### Step 1 — Pick the right grid before the figsize

For 2-panel: side-by-side (`subplots(1, 2)`) is almost always right.

For 3-panel: row of 3 (`subplots(1, 3)`) or 2-on-top + 1-below is almost
always right.

For 4-panel: **default to `gridspec(2, 3, width_ratios=[2,1,1],
height_ratios=[1.4, 1])` with `ax_d = gs[1, :]`.** A wide A on the upper-left,
B and C beside it on the upper-right, D spanning the bottom row.

```python
fig = plt.figure(figsize=(11, 6))   # inches; tune later
gs = fig.add_gridspec(2, 3, width_ratios=[2, 1, 1], height_ratios=[1.4, 1])
ax_a = fig.add_subplot(gs[0, 0])     # hero
ax_b = fig.add_subplot(gs[0, 1])     # subordinate
ax_c = fig.add_subplot(gs[0, 2])     # subordinate
ax_d = fig.add_subplot(gs[1, :])     # bottom-spanning
```

This is the layout SkillTest R1.A and R1.B baselines used by accident, and
the user confirmed both as "very polished and refined".

For 5-panel: **default to `gridspec(3, 3)` with hero=`gs[0:2, 0:2]`**
(R4.B confirmed: user called this layout "remarkably good-looking and accurate"):

```python
fig = plt.figure(figsize=(11, 7.5))  # inches; tune later
gs = fig.add_gridspec(3, 3)
ax_a = fig.add_subplot(gs[0:2, 0:2])  # hero — 4 cells, dominant
ax_b = fig.add_subplot(gs[0, 2])      # subordinate top-right
ax_c = fig.add_subplot(gs[1, 2])      # subordinate mid-right
ax_d = fig.add_subplot(gs[2, 0])      # bottom-left single
ax_e = fig.add_subplot(gs[2, 1:])     # bottom-spanning 2 cells
```

For 6-panel and beyond, the rule generalises: designate a 4-cell hero
region, arrange subordinates around it as a contiguous remainder, no
empty cells, no over-stretching.

Custom asymmetric grids (`gs[0:2, 0:2] + gs[1:, 2:]`, etc) are NOT the
default. Only design a custom grid if:
1. The default has been tried and demonstrably fails for the specific brief, OR
2. The brief explicitly requests a non-standard layout.

### Step 2 — Pick figsize in inches first

Default sizes:
- single panel: `figsize=(6, 4)` inches
- 2-panel side-by-side: `figsize=(10, 4)`
- 4-panel hero (above): `figsize=(11, 6)`

Compress to exact mm only at submission packaging stage, AFTER the layout
has been visually confirmed. Do NOT lead with `figsize=(85/25.4, 58/25.4)`
when the figure has legend, caption, and significance brackets to fit —
that produced unreadable cramming in SkillTest R1.A.

### Step 3 — Layout-budget triage when figsize is tight

When figsize is journal-strict (single column ~85 mm wide, ~60-80 mm tall)
you cannot fit all of:
- above-axes legend
- below-axes caption
- in-axes significance brackets
- 4-series hatched bars at 7-pt body

Pick at most one of (legend / caption / sig brackets) inside the figure;
move the others external (caption goes to figure metadata or paper text;
significance summary goes to caption). The default for tight figsize is
"legend in-axes, caption external."

### Step 4 — Sanity-check before declaring done

After saving:
- Open the rendered PNG. Don't trust the script — open the file.
- Verify legend doesn't overlap data.
- Verify all axis labels are visible (no truncation at the figure edge).
- Verify no font fallback you didn't intend (`fc-list :family | grep Arial`
  on Linux CI; on macOS Arial is usually resident).
- Verify hero panel is genuinely dominant by area, not just width.
- Verify no quadrant is empty whitespace.
- Verify no panel is over-stretched (3 categorical bars in a 180 mm-wide
  panel is the failure case).

### Step 5 — Pack nested 2x2 sub-regions tightly

When 4 single-cell subordinate panels would share a 2x2 sub-region of a
larger grid (e.g. B/C/D/E at gs[0,2], gs[0,3], gs[1,2], gs[1,3] within
a 4x4 grid), the matplotlib default wspace/hspace is proportional to the
FULL grid (4 columns) and produces visible whitespace between the 4
related panels. The visual effect is "scattered" rather than packed.

**Fix:** wrap the 2x2 sub-region in its own subgridspec:

```python
sub_BCDE = gs[0:2, 2:4].subgridspec(2, 2, wspace=0.4, hspace=0.4)
ax_b = fig.add_subplot(sub_BCDE[0, 0])
ax_c = fig.add_subplot(sub_BCDE[0, 1])
ax_d = fig.add_subplot(sub_BCDE[1, 0])
ax_e = fig.add_subplot(sub_BCDE[1, 1])
```

This packs B/C/D/E with their own (tighter) spacing while preserving the
larger grid's wspace/hspace for the hero+subordinate boundary.

User-confirmed at R6.A: without this rule, "the upper-right region had loose, drifting chart elements with too much whitespace in the middle".

### Step 6 — Tune y-axis range to data density, not nominal range

When a bar / dot / violin / box plot's data spans less than ~70% of the
default axis range, the rendered figure has visible empty space above
or below the data. The default axis range is for the wrong message:
it shows "scale" but the panel's job is to show "difference."

**Default rule:** if `(data_max - data_min) / nominal_range < 0.7`
**OR data spans both negative and positive values**, re-scale axis to
`[data_min - 0.1*span, data_max + 0.15*span]`.

```python
data_min, data_max = bar_values.min(), bar_values.max()
span = data_max - data_min
ax.set_ylim(data_min - 0.1 * span, data_max + 0.15 * span)
```

**Important: never default to `set_ylim(0, ytop)` when data includes
negative values.** That clips the negative bars to zero height — they
disappear visually. R-future validation R5.C 7-panel and R-future
aesthetic-polished both hit this bug: Vehicle data was -3% (negative
tumour reduction), CompoundX was 65%, both candidates used `(0, ytop)`
floor and the Vehicle bars vanished. User explicitly flagged: "the gray bars
became completely invisible — the y-axis range was wrong".

The 0-floor applies ONLY when data is naturally non-negative AND the
absolute level is part of the message. Negative-value bars require
data-range scaling.

The 15% top headroom leaves room for significance-marker brackets above
the highest bar.

**Counter-rule:** if the y-axis is a probability or fraction (0 to 1)
and the data is naturally near the boundaries, AND the absolute level
is part of the scientific claim (e.g. "achieved 95% accuracy"), keep
the full 0-1 range. The rule applies when the visual emphasis IS the
difference between groups, not the absolute level.

User-confirmed at R6.A: bar chart with values ~65 and ~-3 on y-axis 0-100
leaves ~35% empty top — "those bars are drawn so long they convey nothing".
The right visual is "the shortest bar should be barely visible; even a small
extra height makes the difference legible".

If any check fails:
- `constrained_layout collapsed to zero` warning fired? **Hard fail.**
  Re-render at larger figsize. Do not save it; do not assume `bbox_inches="tight"`
  recovers (in SkillTest R1.A it didn't).
- Legend overlapping bars? Move it above or below the axes, or make the
  figure taller.
- Empty quadrant? Either extend an existing panel into the empty cell or
  pick a smaller grid.

## Pitfalls

- Designing a custom asymmetric `gridspec` because it "looks more
  sophisticated." SkillTest R1.A nature-figure produced a grid with empty
  `gs[2, 0:2]`; R1.B scientific-figure-making produced cramped B/C and
  over-stretched D. Both lost to baseline's standard pattern.
- Treating `constrained_layout collapsed to zero` as a cosmetic warning.
  It means matplotlib could not fit the requested elements at the requested
  figsize and gave up. `bbox_inches="tight"` may save a file but the
  rendered figure will be cramped beyond legibility.
- Setting `figsize=(85/25.4, 58/25.4)` because the brief says "single
  column ~85 mm" without checking whether 58 mm of height has room for
  legend + caption + density. The brief specifies *width*; height needs
  to be derived from content density.
- Allocating equal panel area to panels with very different data density.
  3 categorical bars do NOT need a 180 mm-wide panel. Match panel size to
  what the panel has to show.
- Letting the legend shrink to 5-pt to fit the squeezed B/C corner.
  Sub-spec text undermines the editable-text rcParams gain.

## Output habit

When delivering a figure, include in the script comments or accompanying
`figure_spec.json`:

```
# layout: gridspec(2, 3, width_ratios=[2,1,1], height_ratios=[1.4, 1])
# figsize: 11x6 inches (= 280 x 152 mm; tune to 180 x 100 mm at submission packaging)
# layout-budget choice: legend above-axes, caption external in paper text
# sanity checks passed: no overlap, no truncation, hero dominant by area
```

This makes the layout reasoning legible to the next editor or reviewer.

## Provenance

Distilled from SkillTest R1 visual-review evidence:
- R1.A nature-figure: case-bar (mm-figsize cramming, `constrained_layout
  collapsed to zero`), case-multi-panel (empty `gs[2, 0:2]` quadrant).
- R1.B scientific-figure-making: case-bar (lighter rule set avoided
  cramming), case-multi-panel (cramped B/C, over-stretched D).

Both R1.A and R1.B baselines on case-multi-panel used the
`width_ratios=[2,1,1] + gs[1, :]` pattern by default. The user confirmed
both as the correct layout. Neither nature-figure nor scientific-figure-making
explicitly teaches this default; both nudge runners toward custom grids
that produce worse rendered figures.
