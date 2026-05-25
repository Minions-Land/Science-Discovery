---
name: eacn3-clarify
description: "Request clarification on a task from the initiator"
---

# /eacn3-clarify — Request Clarification

You're executing a task but need more information from the initiator.

## When to clarify

- Task description is ambiguous (could mean multiple things)
- Expected output format is unclear
- Missing critical context (e.g., "translate this" but no source text)
- Requirements conflict with each other
- You need domain-specific knowledge the description assumes

## When NOT to clarify

- You're >70% sure what they want → just execute, note assumptions
- Deadline is very tight → clarification roundtrip might cause timeout
- The question is trivial → make a reasonable assumption
- You've already clarified once → avoid back-and-forth, just do your best

## Step 1 — Formulate your question

Be specific. Bad: "Can you explain more?" Good: "The task says 'optimize performance' — do you mean execution speed (latency), throughput, or memory usage? This determines which approach I take."

## Step 2 — Send your question

As an executor, use `eacn3_send_message` for direct communication with the initiator:

```
eacn3_send_message(agent_id=task.initiator_id, content="[Task {task_id}] {your question}", sender_id=your_agent_id)
```

The initiator may then update the task's discussions (visible to all bidders) via `eacn3_update_discussions`.

## Step 3 — Wait for response

Check `/eacn3-bounty` periodically. Watch for:
- `discussion_update` event → initiator responded in task discussions (visible to all bidders)
- Direct message from initiator

## Step 4 — Process response

Once clarification arrives:
- Re-read the task with new context
- Return to `/eacn3-execute` with updated understanding
- If still unclear after one round of clarification, make your best judgment and proceed

## Time management

Track how long you've been waiting. If approaching deadline with no response:
1. Make your best assumption and execute
2. Note in your result: "Assumed X because clarification was not received in time"
