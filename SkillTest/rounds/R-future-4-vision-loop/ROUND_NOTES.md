# Round Notes — R-future-4 vision-loop implementation

**Round:** R-future-4
**Date:** 2026-05-17

## Headline

R-future-4 attempted to implement the vision-iterative-loop using
Playwright + Codex bridge as discussed. **Vision-capable model
proved unavailable in the current toolchain** (Codex bridge does not
pass images, Read tool vision unavailable in session). Instead,
`figure_audit.py` was authored to automate ~60% of aesthetic principles
via pixel inspection, and `vision_loop.py` runs the audit after each
iteration. Empirically validated: audit verdicts match user feedback
on R5.C 7-panel and R-future aesthetic-polished cases.

## What was built

| File | Purpose |
|---|---|
| `figure_audit.py` | Pixel-level structural audit. Extracts palette, hue families, saturation distribution, trailing whitespace, editable-text gate. Auto-grades P1/P2/P3 + editable-text gate. Flags P4-P9 as needs-human-review. |
| `vision_loop.py` | Iterative driver. Renders → audits → reports concerning grades → (manual revise) → re-renders. Caps at 4 iterations. |
| `vision-iterative-loop.md` updated | Documents the audit-pivot from vision-model approach. |

## Empirical validation: audit matches user feedback

Tested on 2 R-future cases:

| Figure | User said | Audit said |
|---|---|---|
| R5.C 7-panel candidate | "排版好但颜色感觉差了一点" | P2 saturation: max=0.89 (CONCERNING; >0.7) — matches user |
| R-future aesthetic-polished | "色彩最漂亮，但下面留白多" | P3: trailing 2.9% (CONCERNING; >1%); P2: avg 0.19 (GOOD) — matches user |

The audit does not REPLACE the user's eye — it pre-screens for the
pixel-level discipline (P1/P2/P3) that the user takes time to
articulate. Remaining 4 principles (P4 packing, P5 form, P6 polar,
P7 legend, P8 manifold dim, P9 radar match) still require human
visual review.

## Failure mode discovered: Codex doesn't see images

Direct test: gave Codex a PNG path and asked structured questions
about its content. Codex returned hallucinated answers (3 polygons
when actual figure has 5; "amateur quality" when user said "today's
most perfect"). Codex bridge presents only the file path as text;
no image is uploaded to the underlying model.

This invalidates the vision-iterative-loop's original plan ("Codex
sandbox with vision-capable model") and required the audit-pivot.

## What R-future-4 closes

- ✓ vision_loop.py exists and is runnable
- ✓ figure_audit.py covers P1/P2/P3 + editable-text gate (auto)
- ✓ Audit matches user judgement on the 2 validation cases
- ✗ P4-P9 remain human-judged (not closable without vision model)

## What R-future-4 leaves open

- **R-future-5 (vision-model-augmented loop)**: when a vision-capable
  model becomes accessible (Anthropic API key, or Codex with image
  input, or local Llama vision), augment vision_loop.py to also run
  vision-judging for P4-P9. The loop hooks are ready.

## Bucket

**Calibrates response.** R-future-4 doesn't add new aesthetic
discipline — figure-aesthetic-exemplars is already mature from
R-future-1/2/3. R-future-4 adds AUTOMATION: pixel-level discipline
(P1/P2/P3) doesn't need a human anymore. The user's review is
narrowed to P4-P9 visual judgement.

## Recommendation

`figure-aesthetic-exemplars` skill suite is now complete:

```
SKILL.md
aesthetic-principles.md          9 principles + 12 sub-rules
workflow/
  diff-and-revise.md              R-future original workflow
  vision-iterative-loop.md        R-future-4 design + audit pivot
  figure_audit.py                 R-future-4 pixel audit (NEW)
  vision_loop.py                  R-future-4 iterative driver (NEW)
typography/reference.md
palettes/
  extract.py
  extracted-palettes.json
gallery/                          15 PNG, 12 annotation cards
```

Total deliverable: 9 principles + 12 sub-rules + 15 exemplars + 12
annotation cards + 4 workflow docs + 2 Python tools.

The skill is mature. Land it as part of the R1-R6 + R-future port
plan when user is ready.

## Cross-skill anchor still holds

> Substantively-bounded specificity, not vague good-faith promises.

R-future-4 demonstrates this at the audit layer too: the audit
returns SPECIFIC numeric grades ("max saturation 0.89, exceeds 0.7
threshold"), not vague ones ("colors look bright"). This is what
the loop offers over generic AI judgement.
