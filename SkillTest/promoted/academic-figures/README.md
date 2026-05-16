# Promoted — Academic Figures

Skills for figure rcParams, palette, layout, AND aesthetic exemplar
diffing. R1-R6 established that rule-based skills handle "correct /
submittable" but plateau there. R-future added the exemplar-driven
paradigm to close the "beautiful" gap.

## Skills inside

### Third-party (kept as reference, not duplicated)

- **nature-figure** — `/Users/mjm/Skill/nature-skills-main/skills/nature-figure/`
  - Tested: R1.A (3 cases), R4.B (5-panel), R5.C (6/7-panel)
  - Verdict: fork-narrowly (content discipline portable, layout patterns rejected)

- **scientific-figure-making** — `/Users/mjm/Skill/figures4papers-main/scientific-figure-making/`
  - Tested: R1.B (3 cases), R4.B (5-panel), R5.C (6/7-panel)
  - Verdict: fork-narrowly (same content discipline + lighter rule set)

### SkillTest drafts (authored from R1-R6 + R-future evidence)

- **figure-layout-defaults.md** -> `../../synthesis/proposed-skills/figure-layout-defaults.md`
  - Default 4-panel + 5-panel + 6-panel hero recipes
  - Step 6 y-axis range tuning (R6.A) + negative-value patch (R-future)
  - Subgridspec packing for nested 2x2 sub-regions (R6.A)
  - Status: import-strongly

- **figure-aesthetic-exemplars/** -> `../../synthesis/proposed-skills/figure-aesthetic-exemplars/`
  - NEW PARADIGM: reference-driven (annotation cards) instead of rules
  - 5 starter exemplars with extracted-palette annotation cards
  - Diff-and-revise workflow with current-rules audit (R-future patch)
  - Status: conditional-import-strongly (paired with figure-layout-defaults)

### Update plans for existing MinionsOS skills

- **academic-plotting.md.diff** -> `../../synthesis/proposed-updates/academic-plotting.md.diff`
  - rcParams discipline (Arial fallback, svg.fonttype=none, pdf.fonttype=42)
  - PALETTE-dict pattern + reserve-green/red rule
  - TwoSlopeNorm for diverging colormaps
  - Outside-tick discipline

## Rules / patterns extracted

### Content discipline (R1+R4 evidence; rule-based)

| Rule | Cases |
|---|---|
| `svg.fonttype="none"` + `pdf.fonttype=42` + Arial fallback chain | all 14 figure cases |
| PALETTE-dict pattern threaded across panels | multi-panel cases |
| Reserve green/red for directional signals only | heatmap cases |
| TwoSlopeNorm(vcenter=0) for diverging cmap | heatmap cases |
| Outside-tick discipline | all figure cases |

### Layout discipline (R1+R4+R5+R6 evidence; rule-based)

| Rule | Cases |
|---|---|
| 4-panel default: gridspec(2,3) width_ratios=[2,1,1] + bottom-D | R1.A + R1.B + R4.B |
| 5-panel default: gridspec(3,3) hero=gs[0:2,0:2] | R5.C |
| Subgridspec packing for nested 2x2 sub-regions | R6.A |
| Y-axis range to data density (incl. negative-value patch) | R6.A + R-future |
| No empty quadrants in gridspec | R1.A |
| Default figsize in inches, not mm | R1.A |
| `constrained_layout collapsed to zero` is hard fail | R1.A |
| Tight figsize requires layout-budget triage | R1.A |

### Aesthetic discipline (R-future evidence; reference-driven)

| Rule | Source |
|---|---|
| 50%+ grey foreground in figures, single signal hue at 5-8% | fig3 exemplar (Nature MI vintage) |
| Hue-shifted diverging cmap (#ea6a40 / #6ac0c0) over RdBu_r | fig4 exemplar |
| Single-hue alpha gradient for ablation bars (no hatches needed) | bars_ablation_Cancer exemplar |
| Soft red + soft green (~50-60% saturation) for 3-way categorical | correctness_by_category exemplar |
| Method labels at curve endpoints, not legend block | results_sweep exemplar |
| 4-step typography ladder (panel letters / labels / ticks / annotations / notes) | typography/reference.md cross-exemplar |

The aesthetic discipline is grounded in 5 published-figure exemplars
with palette-extracted hex values + ratios. Not generic guidance.

## Recommendation

`fork-narrowly + import-strongly` for the layered approach:

1. Update `minions/roles/writer/skills/academic-plotting.md` with
   content discipline rules.
2. New skill `minions/roles/writer/skills/figure-layout-defaults.md`
   with layout default recipes (4/5/6-panel) + 6 procedural steps
   incl. negative-value patch.
3. New skill (NEW PARADIGM) `minions/roles/writer/skills/figure-aesthetic-exemplars/`
   directory with SKILL.md + gallery/ + palettes/ + typography/ +
   workflow/. Discoverable via SKILL.md frontmatter.

Each skill loads independently; runner uses them as a chain:
brief -> academic-plotting -> figure-layout-defaults -> figure-aesthetic-
exemplars (when iteration budget allows).

## Open questions

- Heatmap-as-subordinate-panel (vs heatmap-as-hero) needs its own
  annotation card. R6.A and R-future both noted heatmaps in dense
  composites read as "古怪占位大信息量少."
- Vision-capable iterative loop: replace text-based diff with model
  + vision-judge. Future R-round.
- 8+ panel real published exemplars. Add to gallery when found.
