# Nature/Science/Cell Sub-journal Style Checklist

This is the concrete, printable version of the typography and spacing rules that came up in the v8/v16 sessions. Use it as a pre-flight checklist before delivering a figure.

## Page geometry

- **Single column:** ≈ 88 mm (≈ 250 pt)
- **Double column:** ≈ 180 mm (≈ 510 pt)
- **Max height:** ≤ 240 mm (≈ 680 pt) for a full-page figure
- Most multi-panel figures are double column.

## Panel letters

- **Font:** Lowercase **bold sans-serif** (Helvetica/Arial)
- **Size:** 8–9 pt
- **Placement:** Top-left of each panel, **outside** the data area
  - x-offset: ≈ −6 pt from the left edge of the axes box
  - y-offset: ≈ +4 pt above the top edge of the axes box
- **Baseline:** Keep all panel letters on a uniform baseline across the figure
- **Never** place letters inside the plot area
- **Sequence:** Lowercase `a, b, c, ...` or `e, f, g, ...` depending on the figure's position in the paper. Do not mix uppercase and lowercase.

## Typography

### Axis labels
- **Font:** Sans-serif, regular weight (Helvetica/Arial)
- **Size:** 7 pt
- **Style:** Upright (roman), except for math symbols which should be italic

### Tick labels
- **Font:** Sans-serif, regular weight
- **Size:** 7 pt (can drop to 6 pt for dense axes, never below)
- **Rotation:** Avoid rotating x-axis labels unless absolutely necessary; if you must, rotate 45° or 90°, never arbitrary angles

### Legends
- **Font:** Sans-serif, regular weight
- **Size:** 6–7 pt
- **Placement:** Inside the data region, in the least-busy corner
- **Frame:** No frame, no background fill
- **Spacing:** 2–3 pt between legend entries

### Annotations & in-figure text
- **Font:** Sans-serif, regular weight
- **Size:** 6–7 pt
- **Placement:** Clear of data, with a 2 pt minimum clearance from any line or marker

### Internal section titles (in composite figures)
- **Font:** Sans-serif, **semibold** (not bold)
- **Size:** 7–8 pt
- **Spacing below title:** 6–8 pt before the panels start

## Spacing & margins

### Title-to-figure gap
- **Default:** 8 pt below a title row before the first panel starts
- **Tight (user requested "再紧凑一点"):** 4–6 pt
- **Never:** < 3 pt (text will visually collide with the panel)

### Inter-panel spacing (horizontal)
- **Between adjacent panels in a row:** 8–12 pt
- **Tight:** 6 pt (only if the user asks for tighter spacing)
- **Wide:** 15–18 pt (for panels with very different x-axis ranges, to avoid visual confusion)

### Inter-panel spacing (vertical)
- **Between rows of panels:** 10–15 pt
- **Tight:** 8 pt
- **With a section title between rows:** title gets its own 6–8 pt below it, then the usual 10–15 pt to the next row

### Panel-to-edge margins
- **Left margin:** 4–6 pt from the figure's left edge to the leftmost panel letter
- **Right margin:** 4–6 pt from the rightmost panel's right edge to the figure's right edge
- **Top margin:** 4–6 pt from the figure's top edge to the topmost panel letter
- **Bottom margin:** 4–6 pt from the lowest panel's bottom edge to the figure's bottom edge

### Clipping safety margins
- **Above the highest data point:** leave 4–6 pt of whitespace before the top of the clip box
- **Below the lowest data point:** leave 2–4 pt (less critical, but avoid cutting descenders like "g", "y", "p")
- **Left/right of data:** 2–3 pt on each side

## Line widths

- **Axes (spines):** 0.5 pt
- **Plot lines (data series):** 0.75–1.0 pt
- **Error bars:** 0.5 pt, with caps 1.5 pt wide
- **Grid lines (if used):** 0.25 pt, light gray (avoid unless the data is dense and needs a reference)

These are journal norms. Matplotlib's defaults (1.5 pt axes, 1.5 pt plot lines) look amateurish at journal scale.

## Color

- **Palette size:** Limit to 4–6 distinct hues across the entire figure
- **Recommended palettes:**
  - Okabe-Ito (8 colors, color-blind safe)
  - ColorBrewer "Set2" or "Dark2" (qualitative, 6–8 colors)
- **Saturation:** Moderate. Reserve high-saturation red only for emphasis (e.g. highlighting a significant result).
- **Color-blind check:** Always run a deuteranopia/protanopia simulation before delivery. Tools: `colorspacious`, online simulators, or Photoshop's "Proof Setup".
- **Avoid:** matplotlib's default `tab10` (too saturated, not color-blind safe), rainbow gradients (perceptually non-uniform).

## Font family

- **Preferred:** Helvetica (or Helvetica Neue)
- **Acceptable:** Arial
- **Avoid:** DejaVu Sans (matplotlib default — readers can identify it on sight and it screams "draft"), Comic Sans (obviously), Times New Roman for sans-serif contexts

### Math & symbols
- **Variables:** Italic (Times Italic or STIX)
- **Units & functions:** Upright (e.g. "sin", "log", "nm", "°C")
- **Greek letters:** Italic for variables (α, β), upright for constants (π, e)

## Export settings

### PDF
- **Vector:** All elements must remain vector (no rasterization)
- **Fonts:** Embedded as TrueType (Type 42), not outlined as paths
  - In matplotlib: `matplotlib.rcParams['pdf.fonttype'] = 42`
- **Resolution:** N/A (vector), but any embedded raster elements (photos, microscopy) should be ≥ 300 DPI at final size
- **Color space:** RGB for screen/web, CMYK for print (check journal guidelines)

### SVG
- **Text:** Keep as `<text>` elements, not `<path>` (preserves editability)
- **Tool:** `cairosvg` or matplotlib's `savefig('foo.svg')`
- **Avoid:** Inkscape's "text-to-path" unless the journal explicitly requires it

### PNG (for preview/web)
- **Resolution:** 300 DPI at final print size (e.g. 180 mm × 150 mm → 2126 × 1772 px)
- **Anti-aliasing:** On
- **Background:** Transparent if the figure will be placed on a colored background, white otherwise

## Common failure modes (from the v16 session)

1. **"g 被裁断了"** — The top of the letter "g" or a data point was clipped because the clip box was set too tight. Always leave 4–6 pt above the highest element.

2. **Two sets of panel letters visible** — The source PDF had `e/f/g/h/i`, the composite added `f/g/h/i/j`, and both were visible. Solution: vector white-fill rectangle over the source's letters, constrained to not bleed into the composite's labels.

3. **Title-figure gap too loose** — Default spacing was 12–15 pt; user asked for "再紧凑一点". Solution: reduce to 6–8 pt, re-render, confirm.

4. **Inter-panel spacing inconsistent** — Panels in the same row had different horizontal gaps (8 pt, 12 pt, 15 pt). Solution: measure all gaps, pick one target (e.g. 10 pt), adjust all panels to match.

5. **Panel letters not on a uniform baseline** — Letters `f, g, h` were at different y-coordinates because they were placed relative to different panel heights. Solution: compute a single `letter_baseline_y` for the entire row, place all letters at that y.

6. **Axis labels too large** — 9 pt axis labels looked fine in isolation but dominated the figure when placed next to 7 pt tick labels. Solution: drop axis labels to 7 pt, re-render.

7. **Legend overlaps data** — Legend was auto-placed in the top-right, but that corner had data. Solution: move legend to bottom-left (least-busy corner), or outside the axes if no corner is clear.

## Microadjustment workflow

When the user says "再紧凑一点" or "g 被切了一块", follow this loop:

1. **Identify the gap/clip in question.** Render the current PDF to PNG at 150 DPI, measure the gap in pixels, convert to points (1 pt = 150/72 px at 150 DPI ≈ 2.08 px).
2. **Decide the adjustment.** "再紧凑一点" → reduce by 4–8 pt. "g 被切了" → increase clip height by 4–6 pt and shift up by the same amount.
3. **Edit the coordinate in the script.** Do not guess — compute the new value, write it down, then change the script.
4. **Regenerate and re-render.** Check the PNG diff. If the change is too small or too large, iterate once more. Do not iterate more than twice without asking the user.
5. **Confirm with the user.** Show the new PNG, state the adjustment in points (e.g. "I reduced the title-figure gap from 10 pt to 6 pt"), ask if it's right.

## Pre-flight checklist (run before delivery)

- [ ] All panel letters are lowercase bold sans-serif, 8–9 pt, placed outside the data area, on a uniform baseline.
- [ ] Axis labels are 7 pt, tick labels are 6–7 pt, legend is 6–7 pt.
- [ ] Title-to-figure gap is 6–10 pt (not 15+ pt).
- [ ] Inter-panel spacing is consistent within each row (8–12 pt).
- [ ] No data is clipped (4–6 pt safety margin above the highest point).
- [ ] Only one set of panel letters is visible (no duplicates from source PDFs).
- [ ] Text is selectable in the PDF (`pdftotext out.pdf -` returns the expected strings).
- [ ] File size is plausible (50 KB–2 MB for a vector page; if > 10 MB, check for accidentally embedded rasters).
- [ ] Color-blind safe (run a deuteranopia simulation).
- [ ] Fonts are embedded as TrueType (Type 42), not outlined.
- [ ] SVG and PNG exported if requested.

## When to stop iterating

The user from the v16 session said:
> *少写代码，你可以写一点脚本进去，但是排版与多 pdf 矢量融合与微调等在里面做的事情是很宝贵的*

This means: **the judgment is the value, not the code volume.** After 2–3 rounds of spacing adjustments, if the figure is within 2 pt of the target and nothing is clipped, stop and ask the user if it's acceptable. Do not chase pixel-perfection unless the user explicitly asks for it.
