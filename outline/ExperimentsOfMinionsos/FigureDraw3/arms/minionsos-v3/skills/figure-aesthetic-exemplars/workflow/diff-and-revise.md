# Aesthetic Workflow

The diff-and-revise workflow this skill prescribes. 6 steps, capped at
4 iterations.

## Step-by-step

```
[1] Render figure with rule-based skills
       (figure-layout-defaults + academic-plotting)
       output: figures/draft1.png

[2] Pick closest exemplar from gallery/index.md
       output: chosen_exemplar.png + chosen_exemplar.annotation.md

[3] Open exemplar's annotation card
       read: extracted palette, typography ladder, white-space allocation,
             visual rhythm, "what makes it work" bullets

[4] DIFF your figure against the exemplar
       Open both in browser side-by-side (Playwright HTML is fine)
       Identify 3 BIGGEST visual deltas:
         - palette saturation ratio
         - typography hierarchy (number of distinct sizes/weights)
         - white-space allocation
         - inter-panel spacing
         - axis range tuning
         - signal-vs-context contrast

       Rank deltas by aesthetic impact (typography hierarchy and
       palette ratio are usually highest impact; precise hex values
       are lower impact).

[5] Revise script to address top-3 deltas
       DON'T re-do from scratch. Edit existing script.

       BEFORE editing: AUDIT the existing script against the CURRENT
       rule set (figure-layout-defaults Steps 1-6, academic-plotting
       updates), NOT just the rules that were in effect when the
       script was originally authored. Skills evolve; old scripts
       inherit old gaps.

       Common audit checks:
       - Step 6 y-axis range: does the script use `set_ylim(0, ymax)`
         when data includes negative values? Replace with
         `set_ylim(data_min - 0.1*span, data_max + 0.15*span)`.
       - Constrained_layout figsize: does the script's figsize match
         the content density, or does it leave 3%+ trailing whitespace?
         Reduce figsize height if so.
       - Subgridspec packing: are 4 single-cell subordinates inside
         a 2x2 sub-region using parent grid spacing? Wrap in subgridspec.
       - Editable text rcParams: is svg.fonttype set to 'none'?
       - PALETTE-dict pattern: is colour threaded through a single
         dict, or do panels use independent default cycles?

       output: figures/draft2.png

[6] Re-diff. If gap closed → stop. If 1-2 deltas remain → one more iteration.
       HARD CAP: 4 iterations total. Beyond 4, redesign rather than polish.
```

## What "diff" actually means in practice

A useful diff is concrete:

> Your fig: bars are #1f77b4, #ff7f0e, #2ca02c, #d62728 (matplotlib
> default Tab10), all at full saturation. Exemplar: bars are
> #406ac0, #6a95c0, #c0c0ea (single-blue alpha grade) plus 30% grey
> background. Delta: replace 4-hue palette with single-blue alpha grade.

Not useful:

> Your fig: looks bland. Exemplar: looks better. Delta: make yours
> better.

When the diff is concrete, the revision is mechanical. When the diff
is fuzzy, the revision is just generic polish that won't close the
gap.

## Iteration policy

- 1 iteration: should always close 60-80% of the gap if the chosen
  exemplar matches archetype.
- 2 iterations: enough for any gap closable by aesthetic adjustment alone.
- 3 iterations: the figure has a structural issue (wrong gridspec, wrong
  hero panel, wrong panel content) that aesthetic polish can't fix.
  Consider redesign.
- 4 iterations: cap. Beyond this, you're polishing what should have
  been replaced.

If after 4 iterations the user still says "doesn't look like the
exemplar," the issue is one of:

(a) Wrong exemplar choice — pick a closer archetype.
(b) Manuscript palette family genuinely incompatible with the
    exemplar's lessons (e.g. exemplar uses signal red but manuscript
    palette is blue-and-pink). Translate the LESSON not the literal
    palette.
(c) The figure needs a vision-capable iterative loop (model renders
    → vision model judges → model revises) which this skill doesn't
    provide. Future R-rounds may add this.

## When this workflow doesn't apply

- Single-pass deadline submission. Use rule-based skills only.
- Exploratory plots not destined for publication.
- Figure types not in the gallery (e.g. theorem proof diagrams,
  device schematics, microscopy plates at hero scale). Add an exemplar
  to the gallery first.
