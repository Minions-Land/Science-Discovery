# Transcript — case-9panel

## Brief

> 9-panel composite for full preclinical-to-clinical pipeline. Test whether
> figure-layout-defaults' "designate 4-cell hero + contiguous remainder"
> generalisation holds at 9 panels.

## Baseline run

### What I did
- figsize=(10.2, 12.3) inches
- gridspec(4, 4) with A=gs[0:2,0:2], B=[0,2], C=[0,3], D=[1,2], E=[1,3],
  F=[2,0:2], G=[2,2:4], H=[3,0:2], I=[3,2:4]
- rcParams: Arial / DejaVu Sans, svg.fonttype=none, pdf.fonttype=42
- 147 `<text>` nodes in SVG (editable text)

### Layout sanity checks
- constrained_layout: no warnings
- legible: yes
- hero dominant: yes (A occupies 4/16 cells = 25% area)
- empty quadrants: none

## Candidate run

### Skill files actually loaded
- /Users/mjm/Skill/SkillTest/synthesis/proposed-skills/figure-layout-defaults.md

### What changed because of the skill
- Added comment "# layout: gridspec(4, 4), hero=gs[0:2,0:2], contiguous
  remainder fills every cell" — documenting the pattern source.
- Slightly larger figsize (10.5, 12.5 vs 10.2, 12.3).
- IDENTICAL grid topology to baseline. The skill's generalisation IS
  what Codex naive baseline produced.

### Chosen 9-panel grid pattern
gridspec(4, 4):
- A = gs[0:2, 0:2]    (4-cell hero)
- B = gs[0, 2]         (top-right cell)
- C = gs[0, 3]
- D = gs[1, 2]
- E = gs[1, 3]
- F = gs[2, 0:2]       (mid-row, 2 cells wide)
- G = gs[2, 2:4]
- H = gs[3, 0:2]
- I = gs[3, 2:4]

### Layout sanity checks
- constrained_layout: no warnings
- legible: yes (per code; user judged font size "肉眼看得很费劲")
- hero dominant: yes
- empty quadrants: none
- BUT: user identified that B/C/D/E in their own 2×2 corner produces
  whitespace between them (matplotlib default wspace/hspace too loose
  for a 2×2 subregion). NOT caught by the sanity check.
- ALSO: user identified that the bar chart (A) wastes vertical space
  because y-axis 0-100 + bars at 65% leaves 35% empty top.
