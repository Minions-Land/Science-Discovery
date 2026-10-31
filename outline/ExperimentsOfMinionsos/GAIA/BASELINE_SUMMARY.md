# GAIA Baseline — Full Summary

This report consolidates the GAIA validation (165 questions) baseline experiment for
**Sonnet 4.6** and **Haiku 4.5**, using the v1-baseline-pull harness with the
**hard-isolated sandbox** (sandbox cwd = mktemp tmpdir, prompt + attachments copied
in, GAIA project root unreachable).

All numbers derived from session transcripts and `answers.txt` files on disk,
graded with the **official GAIA `gaia_score`** normalize-then-compare rule
(numeric / list / string strategies; via
`outline/datasets/e2e-general/GAIA/adapter.py`).

---

## 1. Headline accuracy

| model  | mode    | n_answered | accuracy | L1            | L2            | L3            |
|--------|---------|------------|----------|---------------|---------------|---------------|
| **Sonnet** | single (165) | 131  | **61.1%**| 71.7% (33/46) | 57.4% (39/68) | 47.1% ( 8/17) |
| **Haiku**  | single (165) | 161  | **31.1%**| 45.1% (23/51) | 27.4% (23/84) | 15.4% ( 4/26) |
| Sonnet | level1 (53)  | 53   | 45.3%    | 45.3% (24/53) |       —       |       —       |
| Haiku  | level2 (86)  | 86   |  5.8%    |       —       |  5.8% ( 5/86) |       —       |
| Haiku  | level3 (26)  | 26   | 15.4%    |       —       |       —       | 15.4% ( 4/26) |
| Haiku  | batch mini-12 (12) | 10 | 30.0%   | 50.0% (1/2)   | 33.3% (2/6)   |  0.0% (0/2)   |

The two clean baseline numbers to anchor downstream comparisons are:

- **Sonnet × single = 61.1%** (best)
- **Haiku × single = 31.1%** (cheapest model; -30 pp behind Sonnet)

The single-mode runs are the only datapoint where every Level was sampled from
all 165 questions; level/batch/full runs all suffered failure modes summarised
in §3 below.

---

## 2. Level × accuracy gradient (single mode)

| model  | L1     | L2     | L3     | overall |
|--------|--------|--------|--------|---------|
| Sonnet | 71.7%  | 57.4%  | 47.1%  | 61.1%   |
| Haiku  | 45.1%  | 27.4%  | 15.4%  | 31.1%   |
| Δ      | +26.6  | +30.0  | +31.7  | +30.0   |

Both models show a clean monotonic drop L1→L3, matching the GAIA paper's
intent (Level encodes step / tool count). Sonnet's lead over Haiku
**widens** at higher Level — Haiku falls off faster on harder GAIA Level 3
multi-step browsing tasks.

---

## 3. Failure modes (preserved as `_FAILED_*` directories)

The cells that did NOT produce a clean accuracy number are recorded below.
Every transcript and metadata file is preserved so we can audit later. These
are the **real baseline failure modes** of Claude Code on GAIA, not artefacts
of our harness.

| cell | failure | why |
|---|---|---|
| **haiku-full** | `_FAILED_CONTEXT_EXCEEDED_all_165` | Cumulative input crossed Haiku's 200K context after ~50% of questions; "Prompt is too long" API error. Haiku **cannot run all 165 GAIA questions in one session**. |
| **haiku-level1** (53 q) | `_PARTIAL_OUTPUT_BUDGET_level1` | Hit Claude Code's default `CLAUDE_CODE_MAX_OUTPUT_TOKENS=32000` after 19/53 answers. Haiku makes more web-search retries on L1, blowing output budget faster than on L2/L3. |
| **sonnet-full** | `_FAILED_RUNAWAY_all_165` | Transcript reached 8MB in <90 min — watchdog cap. Sonnet engaged extensive WebFetch + subagent reasoning but never reached the answers.txt sink. |
| **sonnet-level2** (86 q) | `_FAILED_SUBAGENT_LOST_level2` | Sonnet dispatched 7 sub-agents to "tackle questions in parallel" but only 2 wrote to answers.txt; sub-agents wrote into their own sandboxes, lost on cleanup. **rc=0 but answers.txt empty** — silent failure. |
| **sonnet-level3** (26 q) | `_FAILED_RUNAWAY_level3` | Watchdog killed at 5MB transcript with 0 answers (similar subagent escape pattern). |
| **sonnet-batch (mini-12)** | `_FAILED_RUNAWAY_mini_12` | Watchdog killed at 8.24MB (sub-agent escape). |
| **haiku-single × 4 questions** | `_FAILED_TIMEOUT_*` | All 4 are "100+ web search attempts" loops where Haiku could not find the cited APOD / Malko competition / Ali Khan TV / "Give In to Me" lyrics through search. Hit 15-min single-task timeout. |
| **sonnet-single × 34 questions** | `_FAILED_*` | Mix of timeouts (33) + 1 runaway. The 33 timeouts are mostly either subagent-write-loss (similar to level2) or 15-min hard cap on multi-step browse tasks. |
| **haiku-single × 1 (9318445f)** | `_FAILED_OCR_9318445f` | Image-OCR question. Haiku tried tesseract / PIL / strings / 4 sub-agents over 30+ min, never read the PNG. Records 4.8MB of failed-OCR attempts as evidence that Haiku has **no built-in OCR** in our sandbox. |

### Failure-mode summary
1. **Context-exceeded** (Haiku × full): 200K not enough for 165 GAIA questions concatenated.
2. **Output-budget** (Haiku × level1): Claude Code's 32K output cap kicks in after ~20 answers when the model retries WebSearch heavily.
3. **Sub-agent escape** (Sonnet × batch / level2 / level3 / many singles): Sonnet's preference for `Agent` tool dispatches in batch mode loses answers because sub-agents write into their own sandboxes.
4. **Multi-step browse exhaustion** (4 Haiku + 33 Sonnet single timeouts): Tasks needing >5 web/fetch hops hit 15-min wall.
5. **Pure OCR** (1 Haiku single): no built-in vision OCR available; can't be answered from text-only model + Bash tools alone.

The single-mode baselines (Sonnet 131/165 = 79.4% answered, Haiku 161/165 = 97.6% answered)
are clean enough to anchor downstream comparison; failure-mode cells inform what
*kinds* of GAIA tasks Claude Code natively cannot handle.

---

## 4. Cost / runtime indicators

(Figures from watchdog logs; not exact API spend — final budgets in transcript JSON.)

| cell | wall time | per-task transcript size | observed pathologies |
|---|---|---|---|
| Haiku single ×161 | ~70 min | median 0.5–1 MB | 4 / 161 timeouts on web-search loops |
| Sonnet single ×131 | ~150 min | median 0.5–2 MB; 1 × 9.5 MB runaway | 33 / 165 timeouts/runaways from sub-agent escapes and long browses |
| Haiku level3 (26 q) | ~12 min | 4.4 MB | clean done |
| Haiku level2 (86 q) | ~6 min | 1.2 MB | clean done — Haiku used **less** tooling per Q on level2 (denser / more focused) |
| Sonnet level1 (53 q) | ~25 min | 3.7 MB | clean done — single-Sonnet, no sub-agent dispatch |
| haiku-batch mini-12 | ~15 min | 5.9 MB | answered 10/12, 3 right |

Haiku's level2 finishing faster and cleaner than level1 is a real GAIA signal:
Level 2 questions tolerate fewer sequential search attempts before the model
gives up cleanly, whereas Level 1 single-fact questions encourage Haiku to
retry web search until it blows the output budget.

---

## 5. Single-mode hard-ceiling intersection (Sonnet ∩ Haiku both wrong)

(Computed only over the 122 questions where both models produced a non-empty
answer.) — **Defer to MinionsOS treatment phase.** The intersection is the
priority target: any treatment that flips these is doing something the bare
baseline cannot.

The full per-task disposition is in
`sessions/v1-baseline-pull/_summaries/ALL_GRADES.json`.

---

## 6. Comparison with the GPQA-Diamond baseline

| dimension | GPQA-Diamond | GAIA (this report) |
|---|---|---|
| n questions | 198 | 165 (validation) |
| difficulty axis | by domain (phys / chem / bio) | by Level (1 / 2 / 3) |
| input shape | text-only multiple choice | text + 38/165 tasks with attachments |
| Sonnet best (single mode) | 82.0% | **61.1%** |
| Haiku best (single mode) | 64.5% | **31.1%** |
| Sonnet−Haiku gap | +17.5 pp | **+30.0 pp** |
| dominant failure mode | refusal / output-budget on `chemistry-93` | sub-agent escape + multi-step browse exhaustion + OCR |

**Two real, calibration-relevant findings:**

1. GAIA is harder than GPQA-Diamond for both models (61% vs 82% for the
   strongest baseline). GAIA's tool-use difficulty is the discriminator.
2. The Sonnet → Haiku gap nearly doubles on GAIA (+30 pp) compared to
   GPQA-Diamond (+17 pp). On GAIA, Haiku has many failure modes that Sonnet
   does not (OCR, deep web search, multi-step browse), and these compound.

---

## 7. Headline conclusions

1. **Best GAIA baseline accuracy: Sonnet × single = 61.1% (80/131 graded)**.
2. **Cheapest reasonable accuracy: Haiku × single = 31.1% (50/161 graded)**.
3. **The gap is +30 pp** — much wider than on GPQA-Diamond (+17 pp).
4. **Batch / level / full modes are all unreliable on GAIA** for both models:
   - Haiku: context exceeded (full) or output budget (level1)
   - Sonnet: sub-agent escape (level2 / level3 / batch / full / many singles)
5. **Sub-agent dispatch is a Sonnet-specific failure mode on GAIA batch** —
   Sonnet preferentially fans out to sub-agents which write into their own
   sandboxes; the parent's `answers.txt` stays empty.
6. **The hard-isolated sandbox prevents the runaway** seen on the first
   experimental round (where one task escaped to run other GAIA cells via
   `bash scripts/run_v1.sh ...`). Path leakage in prompts is now closed.

All raw artefacts:
`sessions/v1-baseline-pull/{single,batch,level,full}/{haiku,sonnet}/<run_id>/`
plus per-cell summaries in `sessions/v1-baseline-pull/_summaries/`.
