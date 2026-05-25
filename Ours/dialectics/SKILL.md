---
name: dialectical-synthesis
description: "Open before publishing a confident claim, or when two positions conflict with evidence — thesis/antithesis/synthesis discipline that forces new predictions, not bland trade-offs."
---

# Skill — Dialectical Synthesis

Every strong position contains its own limitation. Surfacing the limitation before you commit is how you avoid overfitting to a single frame.

## When to invoke

- About to publish a confident claim — Expert defending a result, Writer drafting an abstract, Gru endorsing a feature decision, Reviewer recommending accept/reject, Ethics declaring a flag.
- Two roles (or two Experts, or Expert and Reviewer) disagree and both have evidence.
- Evaluating an experimental result that "just works" on your data — what regime would break it?
- Interpreting a surprising outcome: one frame overfits to the finding; the opposing frame guards against that.
- Shaping paper claims: a dialectically tested claim survives review better.

## Structure

Five-step protocol: thesis → antithesis → contradiction inventory → synthesis → verify. A genuine synthesis predicts new things that neither the thesis nor the antithesis alone predicts; if your synthesis predicts nothing new, it is probably a compromise, not a synthesis. Four dialectic patterns worth watching:

- **Scale-dependence.** Thesis holds small; antithesis appears large (or vice versa). Does this survive a 10× change in data / model / compute?
- **Distribution-dependence.** In-distribution thesis; OOD antithesis. What shift would flip it?
- **Metric dialectic.** Thesis wins metric A; antithesis wins metric B. What does the user care about?
- **Short / long-term.** Near-term optimisation thesis; long-term antithesis. Classic training-dynamics / RL trap.

## Procedure

1. **Thesis.** State the proposal as strongly as possible. Steelman — best version, not a convenient caricature.
2. **Antithesis.** Construct the most plausible opposing position. Not random doubt — a specific claim that, if true, would invalidate or substantially weaken the thesis. Where does it break?
3. **Contradiction inventory.** List the concrete points where thesis and antithesis conflict. Each conflict is either a testable claim (→ experiment) or a conditional assumption (→ scope statement). Do not paper over with "it depends."
4. **Synthesis.** Integrate by finding the higher-level statement that accounts for both. Often conditional: "Thesis holds when X; antithesis holds when ¬X." Sometimes a reframing that reveals the two positions were answering different questions.
5. **Verify.** A genuine synthesis makes new predictions. If none, it is a compromise, not a synthesis.
6. **Mark the claim.** `[derived: dialectical synthesis of <thesis> vs <antithesis>]` per the Evidence-first EACN convention (`CLAUDE.md` → "Evidence-first EACN communication"). Single-frame claims without a considered antithesis invite an Ethics flag for unmarked speculation.

## Pitfalls

- **False-balance trap.** Some theses are simply correct with no meaningful antithesis. Manufacturing one to look rigorous is worse than stating the thesis directly.
- **Relativism trap.** "Both sides have a point" is giving up, not synthesis. A synthesis is a concrete statement predicting new things.
- **Infinite regress.** Every synthesis becomes a new thesis. Stop when further decomposition stops changing your recommended action.
