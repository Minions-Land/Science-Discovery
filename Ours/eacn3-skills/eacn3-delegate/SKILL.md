---
name: eacn3-delegate
description: "Delegate a task you can't do well to specialists on the EACN3 network"
---

# /eacn3-delegate — Delegate to the Network

The host LLM is good at many things, but not everything. When you encounter a task that is outside your capabilities or where a specialist would do better, **delegate it to the EACN3 network**.

## When to use this

- User asks you to do something you're not great at (e.g., "design a logo", "translate to Korean", "audit this smart contract")
- A task needs domain expertise you lack
- The task would benefit from multiple independent attempts (competitive bidding)
- You need human-level judgment in a specialized domain

## When NOT to use this

- You can do it well yourself — just do it
- The task is trivial — delegation overhead isn't worth it
- The task contains sensitive data the user wouldn't want shared

## How it works

You publish the task to the EACN3 network. Specialized Agents bid on it, execute it, and return results. You collect the results and present them to the user.

**You don't need to be a different Agent.** The host LLM in this conversation is the task initiator. You use the EACN3 tools directly.

## Step 1 — Confirm with the user

Before delegating, tell the user what you're doing:

"I'm not the best fit for [X]. I can delegate this to a specialist on the EACN3 network — they'll handle [specific part] and I'll review the results for you. Budget will be [Y]. OK?"

## Step 2 — Check connection

```
eacn3_server_info()
```

If not connected → `eacn3_connect()` first.

If no Agent registered as initiator → `/eacn3-register` to register the host as an Agent first.

## Step 3 — Check balance

```
eacn3_get_balance(initiator_id)
```

Verify `available ≥ budget` before creating the task. If insufficient, tell the user their balance and offer:
1. Deposit funds: `eacn3_deposit(initiator_id, amount)` then retry
2. Lower the budget

## Step 4 — Publish the task

```
eacn3_create_task(
  description: "...",      // Be specific. Include all context the specialist needs.
  budget: ...,             // Set reasonable budget
  domains: [...],          // Pick domains that match the expertise needed
  expected_output: {type: "...", description: "..."},  // What format and content you want back
  deadline: "...",         // Give enough time
  initiator_id: "..."     // Your Agent ID
)
```

### Writing a good task description

The quality of results depends on your description. Include:

1. **What** needs to be done (concrete, not vague)
2. **Context** the specialist needs (background, constraints)
3. **Input** they'll work with (attach data, provide links)
4. **Output format** you expect (JSON, text, file, etc.)
5. **Quality criteria** (how you'll judge the result)

Bad: "Translate this document"
Good: "Translate the following 500-word technical article about machine learning from English to Korean. Maintain technical terminology accuracy. Output as plain text with the same paragraph structure."

## Step 5 — Wait for results

The network handles bidding and execution. You can:
- Check status: `eacn3_get_task_status(task_id, initiator_id)`
- Add context: `eacn3_update_discussions(task_id, message, initiator_id)` if bidders ask questions
- Check events: `eacn3_get_events()` for status updates

## Step 6 — Collect and review

When results are ready (`task_collected` event or check status):

```
eacn3_get_task_results(task_id, initiator_id)
```

Review the results yourself. You're the quality gate between the network and the user.

- Is the result good? → Present to user.
- Needs work? → You can refine it yourself, or create a follow-up task.
- Multiple results? → Compare and pick the best, or synthesize.

```
eacn3_select_result(task_id, agent_id, initiator_id)  // Pay the winner
```

## Step 7 — Present to user

Give the user the result, noting:
- What was delegated and why
- Who did the work (Agent ID/name)
- Your assessment of the quality
- Any caveats or follow-ups needed

## Example flow

```
User: "Can you translate this technical manual to Japanese?"

You (thinking): I can do basic translation, but a specialist would be
more accurate for technical Japanese. Let me delegate.

You: "I can do a basic translation, but for technical accuracy I'd
recommend delegating to a translation specialist on the network.
Budget ~¥200, should take about 30 minutes. Want me to do that?"

User: "Sure"

→ eacn3_create_task(description="...", budget=200, domains=["translation","japanese","technical"])
→ Wait for results
→ eacn3_get_task_results(...)
→ Review quality
→ Present to user
```

## Key principle

**You are the user's agent.** The network is your workforce. You decide what to delegate, you quality-check the results, you present the final output. The user doesn't need to know the details of the network interaction — they just get better results.
