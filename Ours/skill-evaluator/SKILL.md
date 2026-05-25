---
name: skill-evaluator
description: Validate AND iteratively improve a skill (or skill library) using haiku-as-executor and codex-as-blind-judge, with eval-set hill-climbing. Use when the user wants to know whether a skill changes agent behavior (validation) OR wants a structured loop for tightening a skill over cycles without regression (improvement). Trigger phrases include "test this skill", "evaluate this skill", "does this skill help", "MetaHarness this", "check skill effect", "iterate on this skill", "tune this skill against evals".
---

# Skill Evaluator by MetaHarness

## When to invoke

Open this skill when any of these is true:

- The user wants behavioral evaluation of a skill file (not document-quality review).
- The user asks "does this skill actually help?" or "is this skill load-bearing?".
- A skill was just rewritten and the user wants regression evidence.
- The user is deciding whether to keep / merge / drop skills based on real impact.
- The user wants to **iterate** a skill against an eval set — hill-climb the harness, not just score it once.
- A skill has been edited several times and it's unclear whether each edit actually helped.
- The user explicitly invokes `/skill-evaluator` or names "MetaHarness".

Do NOT use this for:
- Document-quality review (clarity, structure, frontmatter completeness) — that is a separate Sonnet doc-review pass.
- Skills that have no decision boundary to test (e.g. pure reference catalogues).
- Comparing models — this harness measures harness changes, not model swaps.

## What MetaHarness does

For each tested skill, the harness runs one or more **probes** (situation prompts). Each probe spawns two Haiku agents in parallel: one with the skill text injected (A), one without (B). Codex blind-judges the two responses without knowing which was which, and reports a winner plus a skill-effect estimate.

The output is a behavioural report classifying each skill into one of four buckets:

| Bucket | Meaning |
|---|---|
| **Prevents real failure** | Without the skill, baseline makes a wrong decision (invents fake API names, double-drains, executes when user only asked to scope, etc). |
| **Calibrates response** | Both responses reach the right decision; with-skill version is better defended (concrete weights, conditional synthesis, canonical sources). |
| **Matches baseline** | No measurable difference. Either probe was too easy, or the skill is genuinely low-leverage for haiku-class executors. |
| **Overreaches** | With-skill response is *worse* than baseline (e.g. auto-triggers cleanup the user did not request). Rare; treat as a real bug. |

## Three stages — recall, then behaviour, then iteration

Stages 0 and 1 **validate** a skill (does it surface; does it change behavior). Stage 2 **improves** it over cycles using the eval set as a learning signal. Run them in order:

| Stage | Tests | Method |
|---|---|---|
| **0 — SSL recall** | Can the skill be discovered when it should be? | Show an LLM all skills' frontmatter summaries (no bodies); ask it to pick top-3 for each probe scenario; check whether the target skill is in top-3. |
| **1 — Behavioural A/B** | When loaded, does the skill change agent behaviour? | Haiku × 2 + codex blind judge. |
| **2 — Iteration loop** | After validation, how do we make it better without regression? | Hill-climb: tag evals, split Optimization/Holdout, one explainable change per cycle, human review before merge. |

If a skill fails Stage 0, **fix the summary before running Stage 1** — rewrite it to name the trigger condition explicitly, distinguish it from peer summaries, and put concrete keywords up front. Running Stage 1 on a non-recallable skill burns compute on a result that doesn't reflect reality. Stage 2 is only worth running on skills that pass Stage 1 and are expected to keep evolving.

You can skip Stage 0 in two cases: (a) a single-skill test where the skill is hand-loaded by the test setup, or (b) a regression run where you already verified recall in a prior run. For full-library evaluations, always run Stage 0 first.

See `references/ssl-recall-test.md` for the recall protocol.

## Stage 1 procedure (behavioural A/B)

### 1. Scope the run with the user

Before spawning anything, confirm three things:

- **Which skills?** Single file, role-scoped batch, or full library? (1–60 files.)
- **One probe per skill or two (standard + hard)?** Hard probes catch ~50% of false-negatives where standard probes are too generous to baseline.
- **Output location?** Default `<repo>/_behavioral_evals/SKILL_BEHAVIORAL_EVAL.md`.

Estimate cost: each skill costs roughly 35 k tokens haiku + 17 k tokens codex per probe. Tell the user the estimate before spawning.

### 2. Design the probe(s)

For each skill, design a situation prompt under 300 words that:

- States the role the agent is playing.
- Sets up a concrete scenario where the skill's procedure would apply.
- Ends with a specific question ("What is your next action?" / "Which tool?" / "Should you X or Y?").

The probe must have a **decidable right answer** — otherwise judging is hand-wavy.

For "hard" probes, design a borderline case where the skill's rule is non-obvious — e.g. user has not explicitly asked for cleanup, two reviewers disagree, deadline is tight enough that fast-path looks tempting. Hard probes surface skills whose value is in restraint, not action.

See `references/probe-design.md` for templates.

### 3. Spawn Haiku pairs (parallel, background)

For each probe, dispatch two Agent calls in the same message, both `model: haiku`, `subagent_type: general-purpose`, `run_in_background: true`. The only difference between A and B is whether the loaded skill text appears at the top of the prompt.

Batch size: 8–14 spawns per message is reliable. Larger batches risk hitting per-turn tool-call limits.

Each agent should be instructed to respond ≤200 words, decision-oriented, in the role's voice.

### 4. Wait for completions, then blind-judge

When all agents return, dispatch one Codex call per probe via the `codex-bridge` MCP. Use `reasoning_effort: low`, `sandbox: read-only`, `cwd: <inside a git-tracked repo>` (Codex refuses to run in untrusted dirs).

The Codex prompt must:

- Use random RED/BLUE labels (not A/B) so Codex cannot fingerprint by position.
- Quote the situation verbatim.
- Quote both responses verbatim.
- Tell Codex what the right answer is and what the wrong patterns to watch for are.
- Explicitly tell Codex: "ignore skill-internal terminology when judging; rate by decision quality."
- Demand strict JSON output: `{winner, reasoning, skill_effect_estimate, confidence}`.

### 5. Aggregate into a report

Walk the per-probe verdicts and bucket each skill into one of the four categories. Write a markdown report with:

- A summary table (skill, winner, bucket, confidence).
- Per-cluster narrative (which sub-libraries are highest-ROI).
- Failure-mode catalogue (the specific wrong patterns baseline produces — invented tool names, double-drain, etc).
- Methodology recap and cost.

If the user requests an HTML editorial version, invoke the `editorial-html` skill on the markdown.

### 6. Hand back with three concrete decisions

Always close the report with three actionable decisions: which skills to keep / merge / drop / fix. Avoid "more research needed" as a closing — give the user a defensible recommendation per skill.

## Stage 2 — Harness iteration loop

The A/B harness (Stage 1) answers "does this skill help when loaded?" Stage 2 answers "how do I make it better over time?" It treats the eval set as a learning signal and the skill as a harness to hill-climb.

**Two-layer model:** every agent is a model (generates, reasons) plus a harness (system prompt, skills, tool descriptions, memory rules). When behavior is wrong, a harness tweak is usually faster than swapping models. Stage 2 is the engineering loop for that.

### Eval sourcing — three channels

| Source | Value | Action |
|---|---|---|
| Hand-crafted probes | High-value, covers exact decision boundaries you care about | Write 20 first; these anchor the regression core |
| Production traces | Real failures; user corrections are especially valuable (they name the expected behavior) | Convert failing traces to eval cases; keep only those that are reproducible and explainable |
| External datasets | Broadens coverage | Must be rewritten to fit the probe template and test a real decision boundary — not just "looks like the task" |

Tag every eval case with a behavior label (e.g. `tool_selection`, `restraint`, `multi_step`, `format_compliance`). Tags are the index for stratified splits and per-cluster analysis. Keep the tag vocabulary small (≤8 tags); more than that and the splits become too thin to be meaningful.

### Optimization / Holdout split

Split by tag, not randomly. Every tag must have representation in Holdout. Holdout must match production distribution — don't leave out the hard cases. Holdout is read-only during iteration; it only validates generalization at the end of a cycle.

### The six-step loop

1. **Clean the eval set** — remove saturated cases (pass every cycle), stale cases (failure no longer happens in production), and gameable cases (agent found a shortcut). Goal: every case is still informative.
2. **Bucket by tag, cut Optimization/Holdout** — ensure each tag has holdout coverage.
3. **Run baseline** — score current skill on Optimization + Holdout. Save traces. No trace = no diagnostic value.
4. **Make one explainable change** — one change per cycle. Mixing variables makes regression analysis impossible. Common high-ROI changes:
   - Prompt/instruction: clarify a strategy rule, add a concrete example of the wrong pattern to avoid
   - Tool description: add "when NOT to use", add failure-handling guidance
   - Tool deduplication: if two tools overlap ≥80% of use cases, collapse to one
5. **Verify gain + regression** — re-score Optimization + Holdout. For every regression: write a one-sentence explanation. If you can't explain it, the change is not safe to merge.
6. **Human review before merge** — scan winning traces for reward-hacking patterns: token bloat, universal hedging, verbatim eval phrasing, punting to user, format-only wins. If the skill grew disproportionately large relative to the score gain, reject.

### Regression core

Maintain a small `evals/splits/regression_core.txt` — the highest-stakes cases (forbidden tool calls, permission violations, double-drain, etc.). These must hit 100% pass before any merge. The broader eval set can fluctuate, but every regression must be explainable and restored in the next cycle.

### When to skip Stage 2

- Skill is frozen (no planned edits).
- Fewer than 15 eval cases across 3+ tags — holdout is too noisy.
- Pure reference catalogue with no decision boundary.
- You are comparing models, not iterating a harness.

### Repo layout

```
harness/
  system.md
  tools.yaml
  policies.md
  prompts/

evals/
  cases.jsonl          # one JSON object per line: {id, tag, situation, expected, source}
  tags.yaml
  splits/
    optimization.txt
    holdout.txt
    regression_core.txt

runs/
  2026-05-21_001_baseline/
    metrics.json
    traces/
    change.patch
    rationale.md
    review_checklist.md
```

See `references/probe-design.md` for eval sourcing, tagging, and split guidance.

## Chain with skill-edit

This harness tests **effect** (does the skill change agent behavior?). It does not fix **form** (frontmatter / step structure / decision-rule shape). The two are orthogonal:

| layer | tool | when |
|---|---|---|
| Form (text seams, frontmatter) | `skill-edit` | seconds, free; run before any evaluator pass |
| Effect (behavioral A/B) | `skill-evaluator` | minutes + tokens; run when Procedure or Decision Rule changed |

Run `skill-edit` first on any draft skill: an inconsistent `description` makes Stage 0 (recall) fail before behavior is tested, which wastes a paid run. After `skill-edit` settles the form, this harness produces a clean behavioral signal. The two skills emit compatible appraisal-style reports — Diagnosis / Repaired / Verdict / Recommendation — so the chained output reads as one document.

## Pitfalls

- **Skipping Stage 0.** A skill can win every Stage-1 A/B and still be useless in production if its summary doesn't surface it from the library at the right moment. Always run recall first on full-library evaluations. The MinionsOS run that motivated this harness skipped Stage 0; the SSL-recall failure mode showed up later when summary text was directly tested.
- **Spawning too many Haiku at once.** Each notification costs 200–500 tokens of context. 60-skill double-probe runs (240 agents) will compact your context mid-run; batch ≤14 per spawn message and process notifications as they arrive.
- **Probe ambiguity.** A probe with no clear right answer makes Codex hand-wave. If you can't write the "expected behaviour signature" in one sentence, the probe is too soft — rewrite it.
- **Letting the with-skill response leak skill vocabulary.** When `Phase 3` or `六阶梯` appears verbatim, Codex can fingerprint A vs B and the blind judgement degrades. Either redact those phrases before judging, or add explicit "ignore terminology" guidance to the Codex prompt (the latter is what the original MinionsOS run used).
- **Treating "matches baseline" as a verdict to delete.** Standard probes underestimate skill value 30–50% of the time. Always re-test "matches baseline" skills with a hard probe before recommending deletion.
- **Running this on Sonnet-class agents.** Sonnet already does most of what skills prescribe; differences vanish in the noise. The harness is calibrated for Haiku-class executors. If the production target is Sonnet, this harness will under-estimate skill value.
- **Stage 2 without holdout.** Iterating on Optimization-only is hill-climbing into overfit. Holdout must be reserved before the first change and must match production distribution.
- **Mixing changes in one Stage 2 cycle.** "I tightened the trigger AND added a new step AND removed a tool" — when score moves, you can't tell which change caused it. One change per cycle.
- **Shipping on score gain alone.** Reward hacking shows up as token bloat, universal hedging, verbatim eval phrasing, punting to the user, or format-only wins. Always run human review on winning traces before merging.
- **Letting eval sets grow unboundedly.** Saturated cases (pass every cycle) lose diagnostic value. Prune them and keep a small regression core that always passes; let the broader set rotate as production failure modes shift.
- **Updating the description but not the body (or vice versa).** A change that touches only the trigger surface without changing behavior — or only the procedure without updating the trigger — is a half-edit. Stage 0 catches the first; Stage 1 catches the second. Run both before declaring done.

## Reference: original full-library run

The first complete library run (49 skills × 1–2 probes) lives at `/Users/mjm/MinionsOS/minions/roles/common/SKILL_BEHAVIORAL_EVAL.md` (markdown) and `.html` (Chinese editorial version). Use it as a worked example of probe design, codex prompt shape, and aggregate report structure. The raw transcripts are in `_evals/` and `_behavioral_evals/` next to it.
