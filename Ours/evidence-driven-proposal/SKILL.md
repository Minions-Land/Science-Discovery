---
name: evidence-driven-proposal
description: "Open before submitting a proposal-shaped output (recommendation, root-cause claim, fix recipe, refutation). At least one load-bearing assertion must be backed by a fresh probe (≤5 s) embedded next to the claim. Practice over assertion."
---

# Skill — Evidence-Driven Proposal

When you are about to tell the user "I recommend X" / "the root cause is Y" / "this is broken because Z", at least one load-bearing assertion in that proposal must carry a freshly-run probe. Reasoning chains drift; commands return whatever the system actually does.

## When to invoke

This is the publication gate at the end of any `think-then-act` cycle (after the subagent returns and before you publish the finding), but it also fires standalone — any moment you are about to make a confident claim, planning or no planning.

- Recommending a fix, design choice, refactor, library, or process change.
- Asserting a root cause, mechanism, or system behavior the user has not directly observed.
- Refuting an earlier judgment (yours or the user's) — "actually it's not X, it's Y".
- Disagreeing with another agent's report or with documentation.
- Closing a debug session with a "so the bug was…" summary.

**Skip** when: the user only asked for analysis or summary (no action proposed); the change is trivial single-file (typo, comment, rename); every claim is already a direct quote of a file just read; the proposal is itself a research question, not an answer.

## The discipline

For each load-bearing assertion in the proposal, take exactly one of three lanes — and **say which one** in the body, using exactly these tokens (do not substitute `[smuggled]`, `[implicit]`, or other vocab):

1. **Anchor probe** (default). A ≤5-second command — `grep`, single unit test, micro-script, `python -c`, `head` of a config — that the user can re-run to reproduce. Embed the command and its output (or the relevant fragment) next to the claim. Mark the sentence as `[evidence: <command + 1-line outcome>]`.
2. **`[derived: …]` marker.** State the basis explicitly: `[derived: file X line Y]`, `[derived: framework guarantee]`, `[derived: command output above]`. Use when probing would duplicate work the user already saw.
3. **`[speculation]` marker.** When you cannot probe and cannot derive — say so. Lets the user calibrate trust instead of mistaking a guess for a finding.

Three lanes is the whole rule.

### Smell catalog — sentences that need a lane

Any sentence containing **likely**, **probably**, **typically**, **usually**, **should** (in the predictive sense), **generally**, **tends to**, or **in past projects** is unmarked speculation. Either replace with a probe + `[evidence: …]`, derive it, or label `[speculation]`. The English hedge words are the most reliable trigger; if you wrote one, the next sentence must include a marker.

**Self-applied — meta-claim smells.** The discipline applies equally to claims you make about *your own* work, design, or sanity check — not just to user-facing fixes. The phrases below are recall flags identical in weight to the hedge words above; if you write one, run the probe or label `[speculation]`.

- "sanity check" / "let me make sure" / "I want to verify" — followed by reasoning, not a probe
- "I don't think there's an issue with X"
- "X and Y are not in conflict because …" (assertion about skill / module / design interaction)
- "Looking at this, X should be fine"
- "On reflection, …" / "but actually …"
- "This is unlikely to be a problem"

The cost of a probe is ≤5 s. The cost of a wrong armchair sanity check is design contradiction shipping silently — the lesson lives here because it has happened and was caught only by the user pushing back.

## Procedure

1. **Draft the proposal.** Write the recommendation/diagnosis as you would today.
2. **Underline load-bearing sentences.** A sentence is load-bearing if the user's next decision depends on it being true. Three to five per proposal is normal; if everything looks load-bearing, you have not separated claims from setup.
3. **Pick a lane per sentence.** Anchor-probe by default. Reach for derived/speculation only when honest.
4. **Run the probes.** They should be cheap. If a probe needs >5 s or a real environment, that is a sign the claim is bigger than a proposal — escalate to a real test, do not skip the probe.
5. **Embed and ship.** Put each probe's command + output (≤5 lines) next to the claim it backs. Long output goes in a fenced block; do not paste 200 lines of log.

## Pitfalls

- **Read-as-probe.** Reading a file is derivation, not a probe. A probe asks the running system a question whose answer you do not already know.
- **Ceremony probes.** A probe whose output you already knew is theatre. Anchor on the claim that would *change* if the system answered differently.
- **Probe spam.** Five trivial greps on every proposal trains the user to skim past evidence. Aim for the one or two assertions whose truth most steers the user's next action.
- **Stale probe.** If you ran the probe ten turns ago and the codebase has changed since, re-run it. "I checked earlier" is not evidence.
- **Probe under tool-mock.** A mocked subprocess is not a probe of the real system. State the mock boundary or run the probe outside the mock.
- **Dispatching the probe.** Inside a `think-then-act` cycle, do **not** route a ≤5s anchor probe through a subagent — that turns evidence into ceremony. The think-then-act dispatch rule applies to implementation work, not to verification probes; run them inline.

## Output habit

In every proposal, mark load-bearing sentences inline using the EACN evidence-first convention (`CLAUDE.md` → "Evidence-first EACN communication"): `[evidence: <command + 1-line outcome>]`, `[derived: <basis>]`, or `[speculation]`. The user (and Ethics audit, where relevant) reads the markers to calibrate which sentences to verify before acting on them.

Related: [[think-then-act]] (planning toolkit; this skill is its publication gate), [[goal-setting]] (verification contract for execution), [[dialectical-synthesis]] (predict before publishing), [[think-in-parallel]] (multi-chain disagreement), [[skill-evaluator]] (A/B harness used to validate this skill itself).
