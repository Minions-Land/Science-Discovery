---
name: first-principles
description: 'Open when "everyone does it that way" is the strongest argument, or when a baseline / metric / benchmark may be the wrong proxy — re-derive from primitives, name the smuggled assumption.'
---

# Skill — First-Principles Thinking

What is actually true here, independent of what everyone already assumes? Analogy can suggest hypotheses; it cannot justify them.

## When to invoke

- A proposal sounds reasonable but "because everyone does it that way" is the strongest argument for it.
- The team is stuck in a local optimum defined by the conventional framing.
- Evaluating a baseline, metric, or benchmark — is it measuring the thing we care about, or a proxy inherited from prior work?
- Decomposing a goal into subproblems: prefer causal / mechanistic seams over the organisational / chapter structure of prior work.

Not every question rewards this. Engineering details (library, optimizer) usually do not — conventions are load-bearing for good reason. Reserve for the ~20 % of questions where framing itself is the problem.

## Structure

Four-step reconstruction: strip assumptions → reduce to primitives → rebuild → name the divergence. The most valuable output is the specific assumption the standard practice smuggled in that your reconstruction drops. Divergence from literature is a flag, not a license; first-principles reasoning that rejects the field's accumulated evidence without new data is almost always wrong.

## Procedure

1. **Strip assumptions.** List every premise the proposal depends on. For each, ask: "Why do I believe this? First-principle fact, or convention / authority / aesthetic?" Mark the convention-based ones as load-bearing but unverified.
2. **Reduce to primitives.** Decompose until you hit quantities or mechanisms you cannot further decompose within the domain (information-theoretic bounds, physical limits, provable guarantees, raw statistical properties of the data).
3. **Rebuild.** Re-assemble a solution starting only from the primitives. If the re-assembly matches the convention, the convention is justified. If it diverges, you have a candidate improvement — or a missed constraint.
4. **Name the divergence.** When your reconstruction disagrees with standard practice, articulate *exactly* which assumption standard practice smuggled in that your reconstruction drops. This is the valuable output.
5. **Mark the claim.** `[derived: first-principles from <primitive-list>]` per the Evidence-first EACN convention (`CLAUDE.md` → "Evidence-first EACN communication") so Ethics and the team see the reasoning chain.

## Pitfalls

- Treating every question as first-principles material. Most engineering details are not.
- Discarding empirical evidence. First-principles ≠ ignoring literature. Re-derive from primitives, then check against what has been observed.
- Crank mode. Rejecting an entire field's evidence without new data is almost always wrong.
