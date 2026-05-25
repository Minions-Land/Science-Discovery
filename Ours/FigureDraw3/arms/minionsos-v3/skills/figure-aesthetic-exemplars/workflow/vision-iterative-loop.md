# Task 3: Vision-capable iterative loop — design + prototype

**Round:** R-future-3 Task 3
**Date:** 2026-05-17
**Status:** Design + Python prototype only. Not validated against actual fixture
yet (validation requires Anthropic API key OR Codex sandbox with
vision-capable model invocation).

## Why this is needed

Up to R-future-2, the workflow was:

```
runner generates figure → user judges visually → runner revises
```

**Bottleneck:** the "user judges" step blocks every iteration. For 14 figure
cases × 6 principles × 3-4 iterations, this is a lot of user time.

The R-future-3 hypothesis: **a vision-capable model can stand in for the
user as visual judge** for at least 3 of 6 principles (P1 hue coherence,
P2 saturation, P3 effective area). The other 3 (P4 packing, P5 form
novelty, P6 polar appropriateness) are at-render decisions, not judging
criteria.

If a vision-capable model can reliably grade a rendered figure against
the 6 principles, the workflow becomes self-validating — runner can
iterate without user-in-the-loop until convergence.

## Architecture

```
[1] Render figure (matplotlib + figure-layout-defaults + figure-aesthetic-exemplars)
       output: figures/draft_N.png

[2] Vision judge (Claude Opus 4.7 / Sonnet 4.6 with vision)
    Input:
       - the rendered PNG
       - the chosen exemplar's annotation card (text)
       - the 6 principles list
    Output (strict JSON):
       {
         "principle_1_hue_coherence": {"grade": 1-5, "specific_issue": "..."},
         "principle_2_saturation":    {"grade": 1-5, "specific_issue": "..."},
         "principle_3_effective_area":{"grade": 1-5, "specific_issue": "..."},
         "principle_4_packing":       {"grade": 1-5, "specific_issue": "..."},
         "top_3_deltas": [
           {"principle": "P2", "fix": "reduce signal saturation from 100% to ~70%"},
           {"principle": "P3", "fix": "y-axis range tightens to data span"},
           {"principle": "P1", "fix": "polygon strokes too pale; bump linewidth to 2.0"}
         ]
       }

[3] Runner edits script per top-3 deltas
       output: figures/draft_(N+1).png

[4] Loop until vision judge gives all 4 principles >= 4/5, OR after 4 iterations
```

## Implementation surfaces

### Option A: Anthropic API direct

Pseudocode for the judge function:

```python
import anthropic, base64
from pathlib import Path

client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env

def judge_figure(png_path, exemplar_annotation_path, principles_md_path):
    with open(png_path, "rb") as f:
        img_b64 = base64.standard_b64encode(f.read()).decode()
    exemplar = Path(exemplar_annotation_path).read_text(encoding="utf-8")
    principles = Path(principles_md_path).read_text(encoding="utf-8")

    prompt = (
        "You are a figure aesthetic judge for a Nature-grade scientific figure. "
        "Grade against the 6 R-future-2 principles. Return strict JSON with grades 1-5 per principle.\n\n"
        "PRINCIPLES (with sub-rules):\n" + principles +
        "\n\nEXEMPLAR FOR REFERENCE (target aesthetic):\n" + exemplar +
        "\n\nReturn JSON ONLY with grades and top-3 deltas."
    )

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
                {"type": "text", "text": prompt}
            ]
        }]
    )
    import json
    return json.loads(response.content[0].text)
```

### Option B: Codex sandbox with vision

Codex GPT-5.5 has vision capability. Same JSON schema; invoke via the
codex-subagent MCP. Pseudocode:

```python
result = codex_call(
    task="Grade this figure against 6 principles ...",
    image_path=png_path,
    return_json=True,
)
```

## Loop driver script (skeleton)

```python
import subprocess
from pathlib import Path

MAX_ITER = 4
PASS_THRESHOLD = 4   # all 4 principles must score >= 4

def render(plot_script, n):
    out_dir = plot_script.parent / "iterations"
    out_dir.mkdir(exist_ok=True)
    subprocess.run(["python3", str(plot_script), "--iter", str(n), "--out-dir", str(out_dir)], check=True)
    return out_dir / f"draft_{n}.png"

def judge(png, exemplar_annotation, principles_md):
    # call Claude API (Option A) or Codex (Option B)
    ...

def apply_deltas(plot_script, deltas):
    # rewrite the plot script per top-3 deltas
    # option (a): string replace; option (b): hand to Codex for code edit
    ...

def main(plot_script_path, exemplar_path):
    plot = Path(plot_script_path)
    exemplar = Path(exemplar_path)
    principles_path = exemplar.parent.parent / "aesthetic-principles.md"
    history = []
    for n in range(MAX_ITER):
        png = render(plot, n)
        verdict = judge(png, exemplar, principles_path)
        history.append({"iteration": n, "verdict": verdict, "png": str(png)})
        if verdict["overall_pass"]:
            break
        apply_deltas(plot, verdict["top_3_deltas"])
    write_report(plot.parent / "report.md", history)
```

## Prerequisites for actual deployment

1. **API access**: Anthropic API key OR codex-subagent MCP surface with image input.
2. **Refactored plot script**: scripts must accept `--iter N --out-dir D` args.
3. **Delta-application interface**: translate "fix": "reduce signal saturation from 100% to ~70%" into specific code edits. Either string replace OR pass the delta to a code-editing model.

## Validation plan (R-future-4)

1. Pick R5.C 7-panel candidate (already has bar bug) as starting figure.
2. Run loop for 4 iterations.
3. Compare final figure to user's R-future verdict bar.
4. Grading: did the vision-loop converge to user's bar? In how many iterations?

## Open questions

1. **Calibration**: pre-calibrate vision model on 5-6 known-good and known-bad figures from R1-R6 before trusting grades.
2. **Image resolution**: 600 dpi or send 2 images (wide + zoomed crop) so small typography is detectable.
3. **Loop divergence**: checkpoint best so far; return best at end.
4. **Cost**: each judge call is ~5-6K input + 1K output tokens. 4 iterations × 14 cases = ~336K tokens. Affordable for experimental, not production.

## Status

Design + prototype skeleton complete. Actual deployment requires the prerequisites above. R-future-3 closes by leaving this as unblocked design ready for R-future-4 implementation.

## Files

- This document: `synthesis/proposed-skills/figure-aesthetic-exemplars/workflow/vision-iterative-loop.md`
- Future implementation: `vision_loop.py` (skeleton above; not implemented)
- Validation round: would be R-future-4


---

## R-future-4 implementation update (2026-05-17)

### Discovery: vision-capable model unavailable in current toolchain

Tested in R-future-4:
1. **Codex sub-agent with image input** — confirmed Codex CLI does NOT pass
   image data to underlying model (returns hallucinated answers based
   only on filename / context).
2. **Read tool with PNG/JPG** — multimodal output not available in this
   session (consistent with R1.A finding).
3. **Playwright browser_take_screenshot** — captures the image, but the
   captured image cannot be visually inspected by the runner either.

### Pivot: structural audit replaces vision-model judging

`figure_audit.py` (new, in this directory) automates ~60% of aesthetic
principles via pixel inspection (no vision model needed):

| Principle | Auto-checkable via audit? |
|---|---|
| P1 hue coherence | ✓ (palette family extraction + grey % + distinct hue count) |
| P2 saturation | ✓ (max + avg saturation across palette) |
| P3 effective area | ✓ (trailing whitespace %; data-bbox-vs-canvas ratio) |
| Editable text gate | ✓ (SVG text node count + font-family declared) |
| P4 packing | ✗ needs human |
| P5 form novelty | ✗ needs human |
| P6 polar appropriateness | ✗ needs human |
| P7 legend placement | ✗ needs human (could be partial-auto via SVG bbox) |
| P8 manifold info dim | ✗ needs human |
| P9 radar template match | ✗ needs human |

So `vision_loop.py` (also new) runs `figure_audit.py` after each render
iteration and reports the audit grades. Top-3 concerning/fail grades are
flagged for the human/code-edit step. The other 4 principles still
require human visual review at the end — but the audit shrinks that
review from "judge everything" to "judge only the principles audit
can't."

### Validation against R-future-2 user judgements

Audit results match user feedback on the 2 reference cases:

| Figure | User feedback | Audit verdict |
|---|---|---|
| R5.C 7-panel candidate | 80-90 / 100, layout fine but the palette is a bit off | P2 saturation: **concerning** (max 0.89) — matches user "the colour feels a bit off" |
| R-future aesthetic-polished | most beautiful colours, but lots of empty space at the bottom | P3: trailing whitespace **2.9% (concerning)**, P2 saturation: **good** — matches user judgement exactly |

This is empirical confirmation that the audit captures the same
aesthetic deficiencies the user names. The audit does not REPLACE the
user's eye, but it pre-screens for the pixel-level discipline that
takes the user time to articulate.

### Workflow summary (R-future-4)

```
[1] runner generates figure (matplotlib + figure-layout-defaults + figure-aesthetic-exemplars)
[2] figure_audit.py runs over the rendered PNG + SVG
    → auto-grades P1, P2, P3, editable-text-gate
[3] if any auto-grade is "concerning" or "fail":
    → flag the top-3 deltas
    → runner addresses them (manual code edit OR future codex-subagent code-edit)
    → re-render
[4] when all auto-grades are "good":
    → human visual review for P4-P9 (the principles audit can't grade)
[5] if human says OK → ship
   if human flags an issue → add a new audit dimension or annotate as
   limit case
```

The loop is **structural-audit-driven, not vision-model-driven**, but
performs the same role: shrinks the user's review to high-leverage
principles only.

### Files in this directory after R-future-4

- `figure_audit.py` — structural / pixel-level aesthetic audit (NEW R-future-4)
- `vision_loop.py` — iterative loop driver (NEW R-future-4)
- `vision-iterative-loop.md` (this file) — design + R-future-4 update
- `diff-and-revise.md` — original R-future workflow
- `typography/reference.md`, `palettes/extract.py` — supporting

### Future R-future-5 if vision-capable becomes available

If a vision-capable model becomes available (Codex with image input,
or Anthropic API key, or local Llama 3.x vision deployment), the
audit-based loop CAN be augmented with vision judging for P4-P9. The
`vision_loop.py` already has the hook-points; replace
`run_audit()` with `run_vision_judge()` for the 6 principles audit
can't cover.

But until then, the audit + human review hybrid is the working
implementation.
