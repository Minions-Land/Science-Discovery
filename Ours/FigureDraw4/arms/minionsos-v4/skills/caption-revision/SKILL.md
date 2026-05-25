---
slug: caption-revision
summary: Single-pass revise loop for figure / table captions — simulate one harsh Reviewer 2 critique, address the *caption text*. Never modify the figure itself. Forces Writer's single-pass output to absorb a critic before the caption ships.
layer: logical
tools:
version: 2
status: active
supersedes:
references: academic-plotting, latex-typography, abstract-writing, cns-paper-discipline, figure-chart-atlas
provenance: FigureDraw2-evidence (borrow #6 — academic-paper-imbad 12-agent pipeline) + FigureDraw3-evidence (volcano regressed -4 from reviewer-pass adding inline annotations to figure; rule now scoped to caption text only)
---

# Skill — Caption Revision

MinionsOS Writer's caption.tex output is single-pass — one draft, ship. FigureDraw2 evidence (academic-paper-imbad arm 12-agent pipeline; awesome-writing-prompts arm reviewer_readiness 2.29 vs minionsos 2.13) shows that a single "adversarial reviewer" pass measurably improves caption quality without adding a full review round. This skill is that pass.

## When to invoke

- After [[academic-plotting]] writes the first caption.tex but before commit / before paper-compile.
- After [[latex-typography]] writes a table caption.
- After [[abstract-writing]] drafts an abstract (not just figure captions — same loop applies).
- Before submitting a figure to Reviewer / Expert in EACN — never let an unreviewed caption out of Writer.
- NOT when the user has already manually edited the caption — assume their version is the trusted one.

## Procedure (one pass, ~30 seconds wall-clock)

1. **Read** the draft caption.tex and the figure (or its rendered PNG).
2. **Simulate Reviewer 2** by writing one sharp criticism. The voice should be skeptical, specific, and ungenerous. Pick the *single weakest claim* in the caption — over-claim, under-specification, missing N, missing statistic, drift between figure and caption text, hand-wave palette explanation. One sentence.
   - Example seed: "Caption says 'OursModel achieves the highest accuracy' but does not state the seed count or the std overlap; this is the single weakest line and the one a reviewer will challenge first."
3. **Revise the caption text only** to address that one criticism. Do NOT rewrite the whole caption — surgical edit only. **Do NOT touch `gen_figure.py`, `figure.pdf`, the rendered PNG, or any in-figure annotation in this pass.** If the criticism reveals a figure-shape problem (missing dashed line, label collision, palette ambiguity, "should annotate top hits"), escalate to [[academic-plotting]] / [[figure-spec]] / [[figure-chart-atlas]] — do not paper over it with caption-side hand-waving and do not add `\node`/`\draw` in-figure overlays. The pass closes when the *caption text* criticism is no longer applicable.
4. **Diff log**: append the criticism + the revision intent to a one-line comment in the .tex source: `% revision: addressed reviewer-pass critique <date>: <one-line criticism>`. This makes the loop auditable.
5. **Stop**. Do not iterate further. The discipline is one critic, one fix — not unbounded polishing.

## Critic seed bank (use one, not all)

Ordered by frequency in real Reviewer 2 reports:

1. **Missing N / statistic**. "What's the sample size? What's the error bar — std, SE, 95% CI?"
2. **Vague qualitative claim**. "\"OursModel performs best\" — by how much? On which subset?"
3. **Visual encoding not explained**. "What does the dashed line / shaded band / asterisk mean?"
4. **Drift between caption and figure text**. The caption says "5 methods" but the legend has 4. Catch with `grep`-level checks.
5. **No take-home number**. "What's the one quantitative finding I should remember from this figure?"
6. **Palette not justified**. "Why is OursModel red? Is red carrying directional meaning here, and if so, of what?"

The pass picks the most cutting one *that actually applies* to the current caption. If none of the six applies, the caption is already fine — exit clean.

## What this skill does NOT do

- **Does not modify the figure itself.** This is the most-violated rule. The reviewer-pass critique addresses the *caption text only*. If the criticism reveals a figure flaw — missing dashed line, missing data point, palette ambiguity, "should annotate the top hits" — do NOT add inline `\node`/`\draw`/in-figure annotations to fix it inside this pass. **FD3 evidence**: volcano regressed -4 (FD2 23 → FD3 19) because the reviewer-pass added inline annotations to the figure, diluting visual density beyond what the original draft had. caption-revision touches `caption.tex`, never `gen_figure.py` or `figure.pdf`. Escalate figure-shape problems to [[academic-plotting]] / [[figure-spec]] / [[figure-chart-atlas]] instead.
- Does not rewrite figures. Same rule, restated: if the figure is wrong, escalate, don't patch.
- Does not multi-round. One critic, one fix. Multi-round caption iteration is reviewer's job, not Writer's.
- Does not invent data. If the seed count is unknown, the criticism becomes "add `\\todo{seed count}`", not "invent 5 seeds".
- Does not run on hero / Figure-1 illustrations. Hero captions are governed by [[hero-figure-prompt]] which has its own iteration cadence.

## Pitfalls

- Generating soft critiques ("the caption could be slightly clearer"). The whole point is the harshest single criticism. If the critic-voice goes hedgy, drop the whole pass and assume the caption is fine.
- Rewriting the entire caption instead of surgically addressing the one critique. That breaks the audit trail and tends to introduce new flaws.
- Running this pass on captions that have already been human-edited. The user is the trusted critic when they have engaged.
- Using this skill as a justification to skip the proper [[academic-plotting]] caption checklist. Caption-revision is the second pass; the checklist is the first.
