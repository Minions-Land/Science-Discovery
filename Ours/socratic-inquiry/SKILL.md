---
name: unstated-premises
description: "Open when a task arrives with unstated constraints, or when the team is about to act on premises nobody examined — inventory premises, classify each as explicit/implicit/smuggled, expose what is NOT said."
---

# Skill — Unstated Premises

What are we assuming that nobody said out loud? The most expensive mistakes come from premises the team did not know it had.

## When to invoke

- A task or event batch arrives and you are about to plan a response — but the request leaves important things unsaid.
- The team is converging on a direction and nobody has asked "why do we believe X?"
- You notice yourself filling in blanks with "obviously" or "surely" — those are hidden premises.
- Before any Gate 2 (first-principles) work: you cannot derive from primitives if you haven't surfaced what you're taking for granted.

Not every question rewards this. If the task is fully specified and you can verify every premise from available artifacts, skip to first-principles directly.

## Structure

Three-step exposure: inventory premises → classify each → identify what is NOT said. The most valuable output is the specific question whose answer would change the plan if answered differently.

## Procedure

1. **Inventory premises.** List every assumption the task depends on. Include assumptions about scope, timeline, success criteria, who consumes the output, what "done" means, and what constraints are inherited from context vs. explicitly stated.
2. **Classify each premise.** For each, mark:
   - `[explicit]` — stated in the event or available artifacts.
   - `[implicit]` — reasonable inference from context but not stated.
   - `[smuggled]` — assumed without evidence; would change the plan if wrong.
3. **Identify what is NOT said.** Write 2-3 questions whose answers would materially change your approach. These are the premises that matter.
4. **Resolve or escalate.** For each `[smuggled]` premise:
   - Can you resolve it by reading an artifact, checking git history, or calling a non-destructive EACN read? → Do so.
   - Cannot resolve locally? → Send a targeted `eacn3_send_message` to the role that owns that knowledge. State the specific question and why it matters. Then exit this wake; MinionsOS re-wakes you on reply.
5. **Mark the output.** `[evidence: unstated-premises — premises verified from <source>]` or `[speculation — premise X unverified, proceeding conditionally]`.

## Pitfalls

- **Analysis paralysis.** The goal is 3-5 premises in 2-3 minutes, not an exhaustive philosophical audit. If you're past 5 minutes, you're overthinking.
- **Asking questions you can answer yourself.** Check artifacts and git history before escalating to EACN. Most premises are resolvable locally.
- **Treating implicit as smuggled.** Reasonable inferences from well-established project context are fine. Only flag premises that would change the plan if wrong.
- **Blocking on non-critical premises.** If a premise is smuggled but the plan works regardless of the answer, note it and proceed. Only block on premises that are load-bearing for the plan.
