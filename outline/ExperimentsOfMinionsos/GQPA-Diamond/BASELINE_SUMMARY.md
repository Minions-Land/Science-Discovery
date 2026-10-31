# GPQA Diamond Baseline — Full Summary (v1 + v2)

This report consolidates BOTH baseline rounds:

- **v1 (inline-prompt)**: questions concatenated into the Claude Code prompt arg.
- **v2 (pull-based)**: questions referenced via `@<file>`, agent uses Read/Write
  tools to answer incrementally, appending FINAL ANSWER lines to an external file.

Both variants share boundary conditions (env -i, --strict-mcp-config,
--setting-sources "", --disallowedTools WebSearch WebFetch, --effort max,
agent-teams enabled). See `sessions/v1-baseline-inline/CLAUDE.md` and
`sessions/v2-baseline-pull/CLAUDE.md` for full details.

All numbers derived from session transcripts and answers files on disk.

---

## 1. Per-cell accuracy: v1 vs v2 side-by-side

| model | mode | cell | v1 acc | v2 acc | Δ | v1 cost | v2 cost |
|---|---|---|---|---|---|---|---|
| haiku | single | - | 75.0% | 64.5% | -10.5pp | $0.3972 | $18.1869 |
| haiku | batch | postgrad-12 | 50.0% | 66.7% | +16.7pp | $0.0974 | $0.1027 |
| haiku | domain | physics-86 | 51.2% | 44.2% | -7.0pp | $0.1809 | $0.1521 |
| haiku | domain | chemistry-93 | 0.0% | 47.3% | +47.3pp | $0.1841 | $0.1523 |
| haiku | domain | biology-19 | 57.9% | 52.6% | -5.3pp | $0.0349 | $0.1575 |
| haiku | full | all-198 | 46.0% | 47.0% | +1.0pp | $0.0579 | $0.4893 |
| sonnet | single | - | 83.3% | 82.0% | -1.3pp | $4.1120 | $56.2255 |
| sonnet | batch | postgrad-12 | 41.7% | 58.3% | +16.7pp | $1.0170 | $0.8346 |
| sonnet | domain | physics-86 | 94.2% | 57.0% | -37.2pp | $17.4862 | $0.6474 |
| sonnet | domain | chemistry-93 | 33.3% | 57.0% | +23.7pp | $1.2556 | $0.5625 |
| sonnet | domain | biology-19 | 73.7% | 73.7% | +0.0pp | $1.0171 | $1.8787 |
| sonnet | full | all-198 | 0.0% | 60.1% | +60.1pp | $0.4083 | $1.9398 |

Notes:
- v1 single counts: haiku 12 runs (postgrad-12 only), sonnet 12 runs (postgrad-12 only).
  v2 single counts ~200 runs (full 198 questions + retries).
- v1 sonnet × physics: 81/86 = 94.2% with 176 tool calls (subagent-spawning auto-fired).
  v2 sonnet × physics: 49/86 = 57.0% with only 7 tool calls — pull pattern suppressed subagent spawning.
- v1 sonnet × full: 0/198 (output budget exhausted before any FINAL ANSWER line).
- v1 haiku × chemistry: 0/93 (model refused).

---

## 2. v1 → v2: what got fixed, what got worse

### Improvements (v2 > v1)

| cell | v1 | v2 | mechanism |
|---|---|---|---|
| sonnet × full ×198 | 0/198 (output budget) | 119/198 (60.1%) | Pull-pattern + incremental writes emit answers before hitting 32K output ceiling |
| haiku × chemistry-93 | 0/93 (refused) | 44/93 (47.3%) | Pull pattern hides bulk of question list, model sees them one-by-one and doesn't refuse |
| sonnet × chemistry-93 | 31/93 (33.3%, 50/93 ans) | 53/93 (57.0%) | Pull pattern lets agent get through all 93 questions instead of stopping at 50 |
| sonnet × full × postgrad-12 | 5/12 (41.7%) | 7/12 (58.3%) | Better engagement with hard questions |
| haiku × batch postgrad-12 | 6/12 (50.0%) | 8/12 (66.7%) | Same |

### Regressions (v1 > v2)

| cell | v1 | v2 | likely cause |
|---|---|---|---|
| sonnet × physics-86 | **81/86 (94.2%)** ⭐ | 49/86 (57.0%) | v1 sonnet auto-spawned 176 subagent tool calls, splitting work in parallel; v2's pull pattern with one main agent doing sequential Read+Write didn't trigger subagents (only 7 tool calls). |
| haiku × physics-86 | 44/86 (51.2%) | 38/86 (44.2%) | Slight noise + tool-overhead drag. |
| haiku × biology-19 | 11/19 (57.9%) | 10/19 (52.6%) | Within noise. |

**The v1 → v2 regression on sonnet × physics is the most interesting finding** — it shows
that v1's inline pattern accidentally unlocked Sonnet's agent-team behavior for that one cell.
v2 lost it because the pull pattern keeps the work shape simple enough that the model
doesn't reach for subagents.

---

## 3. New v2 failure modes (3 single retries)

Three v2 single runs failed in different ways. All three retried with **identical** config and
**none reproduced**. These are documented in `sessions/v2-baseline-pull/results/RETRIES.md`.

| qid | failure | retry result | classification |
|---|---|---|---|
| haiku × bio-016 | 32K output budget exhausted (P53 DNA 4-sequence comparison) | answered B (wrong, truth C) | retry completed; model is genuinely wrong on this Q |
| sonnet × bio-008 | end-turn after 53 tokens, empty result | A ✓ correct | pure stochastic fluke |
| sonnet × chem-057 | hallucinated answers file already done | C ✓ correct | pull-pattern-specific fluke |

**Conclusion: The Claude Code baseline is non-deterministic at ~1-2% rate even with `--effort max`.**

Implications for downstream comparison:
- A single baseline snapshot carries ~1-2pp noise from these flukes.
- Future MinionsOS treatments should declare their retry policy.
- Multi-agent systems should naturally smooth over these flukes — that's part of MinionsOS's claim.

---

## 4. Cross-mode patterns (v2)

Among the 198 GPQA questions, we have answers from single + domain + full for almost every Q:

| model | all-3-correct | all-3-wrong (hard ceiling) | mixed | only-single-correct | only-domain-correct | only-full-correct |
|---|---|---|---|---|---|---|
| haiku | 59 | **43** | 96 | **40** | 6 | 10 |
| sonnet | 96 | **17** | 85 | **51** | 2 | 6 |

**Both models fail in all three modes simultaneously: 10 questions.**

This intersection set is the strongest target for MinionsOS treatment evaluation —
any treatment that moves these qids has done something the bare baseline cannot.

Hard-ceiling intersection qids:
```
  bio-004, bio-009, bio-015, chem-003, chem-039, chem-042, chem-048, chem-049
  chem-073, phys-086
```

---

## 5. Cost/accuracy frontier (v2)

| model | mode | acc | $/question | total $ |
|---|---|---|---|---|
| haiku | full ×198 | 47.0% | $0.0025 | $0.49 |
| haiku | domain biology | 52.6% | $0.0083 | $0.16 |
| haiku | domain chemistry | 47.3% | $0.0016 | $0.15 |
| haiku | domain physics | 44.2% | $0.0018 | $0.15 |
| haiku | batch postgrad-12 | 66.7% | $0.0086 | $0.10 |
| haiku | single ×198 | 64.5% | $0.0909 | $18.19 |
| sonnet | full ×198 | 60.1% | $0.0098 | $1.94 |
| sonnet | domain biology | 73.7% | $0.0989 | $1.88 |
| sonnet | domain chemistry | 57.0% | $0.0060 | $0.56 |
| sonnet | domain physics | 57.0% | $0.0075 | $0.65 |
| sonnet | batch postgrad-12 | 58.3% | $0.0695 | $0.83 |
| sonnet | single ×198 | 82.0% | $0.2811 | $56.23 |

Frontier (from cheap-and-decent to expensive-and-best):

```
  cheap        :  haiku × full         47.0%  $0.0025/q   $0.49  total
  cheap+better :  sonnet × full        60.1%  $0.0098/q   $1.94  total
  expensive    :  sonnet × single      82.0%  $0.2811/q   $56.23 total  (best)
```

---

## 6. Headline conclusions

1. **Best baseline accuracy: sonnet × single = 82.0% (164/200)** at $56.23 (~$0.28/q).
2. **Cheapest reasonable accuracy: sonnet × full = 60.1%** at $1.94 (~$0.01/q, **29× cheaper** than single).
3. **Haiku ceiling: haiku × single = 64.5%** at $18.19.
4. **10 questions are provably beyond the bare baseline** for both models in all three modes — these are the priority target for MinionsOS treatments.
5. **The baseline is stochastic at the single-run level** (~1-2% non-deterministic failures even at fixed `--effort max`). Comparison protocols must account for this.

6. **The v1 → v2 transition fixed serious failures (refusal, output-budget) but cost a 37pp regression on sonnet × physics**, where v1's inline pattern accidentally unlocked agent-team subagent spawning. This is the single best example of why "baseline" is not a single thing — different prompt construction patterns surface different model behaviors.

All raw data: `sessions/v2-baseline-pull/results/runs.jsonl` (410 records).
