---
name: skill-evaluator
description: "Evaluate whether a skill works in production — toolkit of five checks for loadability, discoverability, narrative coherence, design quality, and behavioral impact. Use any combination. Trigger: 'test this skill', 'evaluate this skill', 'does this skill help', 'MetaHarness this', 'skill health check'."
---

# Skill Evaluator

Five evaluation postures available for judging whether a skill is worth keeping.
You decide which to use, how many, and in what order. The sequence below is a
recommendation for full evaluations — not a mandatory pipeline.

## When to consider this skill

- Deciding whether to keep / merge / drop a skill based on real impact.
- A skill was just rewritten and needs regression evidence.
- Auditing a skill library for dead weight.
- User asks "does this skill actually help?"

**Skip entirely** when the task is document-quality review (clarity, formatting)
or the skill is a pure reference catalogue with no decision boundary.

## The five postures (your toolkit)

| Posture | File | Use when | Skip when |
|---|---|---|---|
| **Loadability** | `loadability-check.md` | Any skill you haven't verified can enter the runtime | You just wrote it and know the frontmatter is valid |
| **Discoverability** | `discoverability-test.md` | Full-library eval, or a skill that "should fire but doesn't" | Single-skill test where you hand-load it into the prompt |
| **Narrative Coherence** | `narrative-coherence.md` | Skill was merged from multiple sources, or "feels long but unclear why" | Brand new skill written in one pass |
| **Design Audit** | `design-audit.md` | You want structural quality signal beyond pass/fail | User says "just run the A/B" or design hasn't changed |
| **Behavioral A/B** | `behavioral-ab.md` | The definitive test: does it change agent decisions? | Skill failed loadability or discoverability — fix those first |

Each posture is an independent skill. Read its file when you decide to use it.

## Default recommendation (not mandatory)

For a full evaluation of an unfamiliar skill:

1. **Loadability** — can it enter the runtime at all?
2. **Discoverability** — will agents find it at the right moment?
3. **Narrative Coherence** — does it read as one story or fragments stitched together?
4. **Design Audit** — is it well-made? What to fix?
5. **Behavioral A/B** — does it actually change behavior?

This is a funnel: each layer is cheaper than the next, and early failures
make later layers pointless. But this is ONE way to use the toolkit.

## Other valid patterns

- **Just Behavioral A/B**: Skill is known-good structurally, you only need impact evidence.
- **Loadability → Behavioral A/B**: Quick regression check — can it load, does it still help.
- **Narrative Coherence only**: Skill was just merged from multiple sources; check if it needs restructuring or splitting before deeper evaluation.
- **Design Audit only**: You're refining a skill and want the 12-dimension scorecard without spending tokens on A/B.
- **Discoverability only**: Library-wide triage to find skills with bad descriptions.
- **Skip all five**: You already have round data in `SkillTest/` and just need to read the verdict.

The agent decides. The skill does not decide for you.

## After the postures: close with decisions

When you have enough signal (from however many postures you used):

- **Bucket the skill** into one of four outcomes:

| Bucket | Meaning |
|---|---|
| **Prevents real failure** | Without it, baseline makes a concrete error. |
| **Calibrates** | Both correct; skill version is better defended. |
| **Matches baseline** | No difference. Re-test with hard probe before deleting. |
| **Overreaches** | Skill makes it worse. Treat as a bug. |

- **State three decisions**: keep / merge / drop / fix. No "more research needed" as a closing.
- **Output location**: `SkillTest/rounds/R<N>-<skill-slug>/` by default.

## Cost estimate per skill

| Posture | Tokens |
|---|---|
| Loadability | ~0 (filesystem only) |
| Discoverability | ~3k haiku per probe |
| Narrative Coherence | ~4k (one read-through + verdict) |
| Design Audit | ~8k sonnet |
| Behavioral A/B | ~52k per probe (35k haiku + 17k judge) |

Batch ≤14 agent spawns per message in Behavioral A/B to avoid context compaction.

## Hard rules

1. **Don't modify production skill libraries during evaluation.** SkillTest is research; production is production. Porting happens only by explicit user decision.
2. **Don't treat "matches baseline" as a delete verdict.** Standard probes underestimate 30–50% of the time. Always re-test with a hard probe.
3. **Don't run Behavioral A/B on Sonnet-class only.** Sonnet already does what most skills prescribe. Calibrate for haiku executors.
4. **Don't let skill vocabulary leak into the judge.** Redact or instruct to ignore.
5. **Don't score figures by code alone.** Open the rendered file and look.

