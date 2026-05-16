# Verdict — &lt;skill-slug&gt; / &lt;case-name&gt;

**Round:** R&lt;N&gt; · **Date:** YYYY-MM-DD · **Rubric version:** v1

## Numeric score

(Use the rubric in `SkillTest/README.md`. Sum to total / 22 or 15.)

| Dim | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|
| (dim 1) | x/4 | y/4 | +/- | one-line reason |
| (dim 2) | x/3 | y/3 | +/- | |
| ...    | ... | ... | ... | |
| **Total** | **bx/22** | **cx/22** | **±k** | |

## What the skill actually changed

One paragraph. Concrete deltas only. No "looks better".

Example phrasing:
- Candidate identified the paper as a methods paper and reorganised section
  order accordingly. Baseline kept the chronological draft order.
- Candidate enforced ≤30-word sentences (longest 28); baseline had two 41- and 47-word sentences.

## Visual inspection (figure cases only)

(Skip for prose / rebuttal cases.)

Inspected via Playwright on rendered PNG/SVG. Both baseline and candidate
opened side-by-side or sequentially.

- **Palette as rendered:** ...
- **Text overlap / truncation:** ...
- **Caption-vs-figure consistency:** does the figure actually defend the brief's claim? ...
- **Geometry / hero panel:** ...
- **Findings that contradict the script's intent:** (e.g. script declared Arial but font fell back to DejaVu Sans because Arial was unavailable in the runtime; or palette was set but two adjacent colours were near-identical at this size)

## What the skill missed or hurt

What it overshot, what it lost, what it didn't notice. Be honest — this column
decides whether we fork or skip.

## Token cost

See `tokens.json`. Headline: candidate / baseline ratio.

## Blind judgement (Codex)

(Optional but recommended for writing / rebuttal cases. Skip when the rubric
already settles it — typically figure cases where information architecture is
quantitatively scoreable.)

- **Labels assigned:** baseline = `<RED|BLUE>`, candidate = `<the other>`
  (randomised per case so Codex cannot position-fingerprint)
- **Codex verdict:** `winner: <RED|BLUE|tie>`
- **skill_effect_estimate:** `<small | medium | large | overreach>`
- **confidence:** `<low | medium | high>`
- **Reasoning excerpt:** one or two lines from the Codex output

## Bucket (post-judgement)

One of: `Prevents real failure` / `Calibrates response` / `Matches baseline`
/ `Overreaches`. With one sentence justifying the bucket.

## Porting recommendation

One of: `import-as-is` / `fork-and-adapt` / `skip` / `defer`.
With one sentence justifying the choice.
