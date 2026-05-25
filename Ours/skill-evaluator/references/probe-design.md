# Probe Design Templates

This file gives concrete templates for writing probe situations. Read it from `SKILL.md` step 2 when designing situations for new skills.

## The probe contract

A good probe has four properties:

1. **Concrete role** — "You are a Coder agent" not "You are an AI assistant".
2. **Concrete situation** — specific files, specific status values, specific numbers. No "imagine you have a project".
3. **Decidable question** — ends in a single concrete question whose right answer is known to the harness operator. "What is your next action?" / "Which tool do you use?" / "Should you X or Y?".
4. **≤300 words total.** Longer probes drift; shorter probes don't anchor enough.

## Standard probe template

```
You are a {ROLE} agent in MinionsOS. Respond concise, decision-oriented, ≤200 words.

## Loaded skill   ← only in the with-skill prompt; remove for baseline
```
{COMPACT SKILL TEXT — frontmatter stripped, ≤30 lines}
```

## Situation
{2–4 sentences setting up concrete state: file paths, status values, numbers, deadline.}

{Specific question. End with "What is your next action?" or equivalent.}
```

## Hard probe template

A hard probe is the same shape but tweaks the situation so a naïve baseline reads it as "obvious — just do X" while the skill's correct answer is restraint or a non-obvious branch.

Examples of "hard" twists:

| Skill type | Hard twist |
|---|---|
| Stop / bounded-loop | "Tests pass after 2 iterations, but you changed 47 lines and the minimal fix would be 5." |
| Don't auto-execute | "User said 'just implement', not 'implement and clean up'." |
| Sample, don't exhaust | "5 days to deadline, 80 entries, 4 hours of audit time." |
| Disagreement signal | "Reviewer 1 = Strong Accept; reviewer 2 = Reject. Continue or stop?" |
| Need_info, not guess | "All required fields present, but feasibility checks reveal a hidden conflict." |

## Codex blind-judge prompt template

```
Blind judge two AI responses. STRICT JSON only — no markdown, no prose outside JSON.

# Situation
"{verbatim situation prompt}"

Note: {one paragraph stating what the right answer is and which wrong patterns to watch for. Be specific — name fake tool names, banned actions, sequencing errors.}

# Response RED
{verbatim response from one of A/B, randomized}

# Response BLUE
{verbatim response from the other}

Notes:
- {brief observation about what each response did differently — what RED got right or wrong, what BLUE got right or wrong. Be neutral.}
- {explicit instruction: "Ignore skill-internal terminology like 'Phase 3' or '六阶梯'; judge by decision quality, not vocabulary fingerprint."}

Output STRICT JSON:
- winner: "RED" | "BLUE" | "TIE"
- reasoning: 1-3 sentences referring to specific phrases
- skill_effect_estimate: "RED appears to have benefited from a skill" | "BLUE appears to have benefited from a skill" | "neither shows skill influence" | "unclear"
- confidence: "high" | "medium" | "low"
```

## Bucket assignment rules

After collecting all per-probe verdicts, bucket each skill:

- **Prevents real failure** if: with-skill response avoided a concrete error baseline made (invented API name, called forbidden tool, double-drained queue, executed unrequested work, violated FSM state, leaked Pass A independence, etc).
- **Calibrates** if: both responses chose the same correct decision but with-skill version cited the right canonical source / sampling weight / structural form.
- **Matches baseline** if: TIE or both responses are equivalent in correctness.
- **Overreaches** if: with-skill response is judged worse than baseline by Codex with high confidence — usually because the skill's auto-trigger fires when the user did not request that work.

If a skill has a standard probe in "matches baseline" but a hard probe in "prevents real failure", report the hard probe's bucket and note the standard probe was insufficient.

## Eval sourcing and tagging (for Stage 2 iteration)

When building an eval set for iterative harness improvement, each case needs a tag and a source label.

**Minimal case schema (JSONL):**
```json
{"id": "tool_sel_001", "tag": "tool_selection", "source": "trace", "situation": "...", "expected": "call mos_scratchpad_append, not mos_publish_to_shared"}
```

**Tag vocabulary (keep ≤8):**

| Tag | Tests |
|---|---|
| `tool_selection` | Picks the right tool vs a plausible wrong one |
| `restraint` | Does NOT act when the skill says to hold back |
| `multi_step` | Sequences multiple tool calls correctly |
| `format_compliance` | Output shape matches required structure |
| `followup_quality` | Asks the right clarifying question (or none) |
| `boundary_respect` | Stays within role/permission boundary |

**Converting a production trace to an eval case:**
1. Find a trace where the agent was corrected or escalated.
2. Extract the situation (≤300 words, concrete state).
3. Write the expected behavior in one sentence — this becomes the "right answer" for the Codex judge.
4. Assign a tag. If it fits two tags, pick the primary failure mode.
5. Mark `"source": "trace"` so you can filter by source when pruning.

**Stratified split rule:** every tag must appear in both Optimization and Holdout. A tag with only 2 cases: put 1 in each. Never put all hard cases in Optimization — that makes Holdout trivially easy and hides overfitting.

## Anti-patterns in probe design

- **"You wake up and there are events."** — too vague. Name the events, the count, the agent_id.
- **"Help the user with their paper."** — no decidable question.
- **"What would you do?"** — open-ended; force a specific decision.
- **Two probes that test the same trigger.** — wastes budget. Each probe should hit a different decision boundary of the skill.
- **A probe whose right answer is "ask a clarifying question".** — both A and B will probably ask questions; you can't distinguish skill effect.
