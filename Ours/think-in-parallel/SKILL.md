---
slug: think-in-parallel
summary: Think in parallel — spawn K independent reasoning agents on the same hard problem, then synthesize by critique rather than majority vote. Use when a single reasoning chain is suspect: the task is counter-intuitive, the answer is verifiable, or a prior attempt produced contradictory or abandoned logic.
layer: logical
tools: Agent
version: 1
status: active
references: think-then-act, dialectical-synthesis
provenance: human+agent
---

# Skill — Think In Parallel

When one reasoning chain is not enough, run K independent ones and
synthesize by critique — not by vote.

## When to use

- A prior single-agent attempt produced contradictory reasoning, an
  abandoned proof, or an answer that "feels wrong".
- The problem is counter-intuitive (divergent expectations, unexpected
  edge-cases, known hallucination-prone domains).
- The answer is verifiable against a mathematical or logical ground truth.
- Two quick probes returned different answers — escalate rather than guess.

**Skip when:**
- The single-agent answer is clean, confident, and internally consistent.
- The problem is in the model's clear competence zone (routine code edits,
  well-known algorithms, simple probability).
- Speed matters more than correctness — the 3–4× cost must be justified.

## The two-stage protocol

### Stage 1 — Parallel sampling (K = 3 recommended; K = 5 for hardest cases)

Spawn K agents in a **single message** (parallel execution). Each agent
receives the same prompt and must reason completely independently.

**Agent prompt template:**
```
Solve the following problem step by step. Show your complete
reasoning chain and arrive at a final answer.

Problem: {query}

Think carefully and solve independently. Show all work.
```

Key rules for Stage 1:
- Agents must NOT share context or see each other's work.
- Do NOT add "watch out for X" warnings — that collapses diversity.
  Move known traps to Stage 2 instead.
- Encourage diversity implicitly: "use whatever approach you prefer."

### Stage 2 — Sequential deliberation (main agent does this, never delegated)

After all K trajectories return:

1. **Map the answer distribution** — list every distinct answer and its
   frequency.
2. **Audit each reasoning chain** — identify where logic is sound vs.
   where it breaks, assumes, or guesses.
3. **Cross-validate** — do independent approaches confirm the same result?
4. **Apply critical judgment** — majority is a signal, not proof.
   A minority answer with rigorous logic beats a flawed majority.
   All trajectories may be wrong — be ready to reason fresh.
5. **Synthesize** — produce the final answer with an explicit verdict on
   which chain(s) supported it and why the others were rejected.

**Deliberation prompt (use when delegating Stage 2 is unavoidable):**
```
Multiple independent thinkers attempted this problem.

Problem: {query}

Thinker #1: {trajectory_1}
Thinker #2: {trajectory_2}
...
Thinker #K: {trajectory_K}

Analyse each chain. Identify errors and gaps. Determine which
reasoning path(s) are most sound. If all are wrong, reason
independently from their mistakes. Provide the definitive answer.
```

## Trigger pattern: probe-then-escalate

The cheapest usage pattern — run TWO quick probes first:

1. Dispatch two single-agent solves in parallel.
2. If both agree and reasoning is clean → accept, done.
3. If they disagree OR one shows broken logic → escalate to K = 3
   full think-in-parallel with Stage 2 deliberation.

This avoids paying 3–4× on problems the model already handles correctly.

## Cost model

| Mode | Calls | When to use |
|---|---|---|
| Probe | 2 | Any suspect problem; cheap triage |
| Standard | 3 + Stage 2 | Confirmed disagreement or broken logic |
| Deep | 5 + Stage 2 | Open-ended hard problems, known failure domains |

## Output format

Present only the final synthesized answer in the domain's convention:
- Math / STEM: `\boxed{answer}`
- Code: fenced code block
- General reasoning: clean prose

The meta-analysis (which trajectories were correct, why) stays internal
unless the user explicitly asks for it.

## Relationship to think-then-act

Think-in-parallel is a **dispatch escalation tool**, not a planning
posture. Think-then-act handles *what problem to solve and why*;
think-in-parallel handles *getting the answer right* once the problem
is clear. The typical composition:

```
think-then-act (postures clarify the problem)
  → dispatch via delegate-heavy-task / subagent-driven-development
  → if answer returns suspect: escalate to think-in-parallel
```

Think-in-parallel can also be called directly without think-then-act
when the problem is well-scoped and the only question is correctness.
