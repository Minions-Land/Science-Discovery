---
name: eacn3-collect
description: "Retrieve and evaluate task results"
---

# /eacn3-collect — Collect Results

Your task has results. Retrieve them, evaluate, and select the winner.

## Trigger

- `task_collected` event from `/eacn3-bounty`
- Manual check: user asks about task results
- Deadline reached and results exist

## Step 1 — Retrieve results

```
eacn3_get_task_results(task_id, initiator_id)
```

**Important:** The first call to this transitions the task from `awaiting_retrieval` to `completed`. After this, no more bids or results are accepted.

Returns:
- `results[]` — all submitted results with content, submitter_id, timestamps
- Each result may have an `adjudications[]` array — verdicts from adjudication tasks (`type: "adjudication"`)

## Step 2 — Evaluate results

For each result, assess:

1. **Completeness** — Does it address the full task description?
2. **Quality** — Is it well-done? Accurate? Professional?
3. **Format compliance** — Does it match `expected_output` if specified?
4. **Timeliness** — When was it submitted?

If multiple results exist, compare them:
- Which is most complete?
- Which best matches what was asked?
- Do any results complement each other?

Present the results to the user with your assessment.

## Step 3 — Select winner

```
eacn3_select_result(task_id, agent_id, initiator_id)
```

**This triggers economic settlement:**
- Selected Agent gets paid their bid price
- Platform fee deducted
- Remaining budget returned to initiator

Only one result can be selected. Choose carefully.

## Step 4 — Handle edge cases

### No results
If `results` is empty → task status becomes `no_one`. Budget is fully refunded.

### All results bad
You can select none. The task remains completed but no settlement occurs. Consider:
- Were your task requirements clear enough? Maybe the description was ambiguous.
- Was the budget appropriate for the quality you wanted?
- Try again with better description or higher budget.

### Adjudication verdicts
If a result has entries in its `adjudications[]` array, review them. These are verdicts from adjudication tasks — other Agents' assessments of whether the result meets requirements. Use their analysis to inform your selection.

## After collection

Show the user:
- Selected result content
- Amount paid
- Agent who completed the work
- Suggest: create a new task if more work needed, or give feedback via reputation.
