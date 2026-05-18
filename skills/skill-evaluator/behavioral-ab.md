# Behavioral A/B

Does this skill actually change agent behavior?

## When to use

- The definitive test: you need evidence that the skill makes a difference.
- Regression check after a rewrite.
- Deciding between two competing skills for the same slot.

## Skip when

- Skill failed loadability or discoverability — fix those first.
- You only need a design-quality signal (use Design Audit).

## Procedure

### 1. Design a probe

A probe is a situation prompt (≤300 words) with four properties:

- **Concrete role** — "You are a Writer agent" not "You are an AI assistant".
- **Concrete situation** — specific files, status values, numbers, deadlines.
- **Decidable question** — "What is your next action?" with a known right answer.
- **Expected-behavior signature** — one sentence stating what correct looks like.

**Hard probes** (use on any "matches baseline" result): borderline cases where the skill's correct answer is restraint or a non-obvious branch.

| Skill type | Hard twist example |
|---|---|
| Stop / bounded-loop | "Tests pass but you changed 47 lines; minimal fix is 5." |
| Don't auto-execute | "User said 'implement', not 'implement and clean up'." |
| Sample, don't exhaust | "5 days to deadline, 80 entries, 4 hours of audit time." |
| Disagreement signal | "Reviewer 1 = Strong Accept; Reviewer 2 = Reject." |

### 2. Spawn two agents

Both `model: haiku`, `run_in_background: true`, same prompt except:
- **A (with-skill):** Skill text prepended as system context.
- **B (baseline):** Same prompt, no skill.

Instruct both to respond ≤200 words, decision-oriented.

Batch ≤14 spawns per message.

### 3. Blind judge

When both return, send to a judge (Codex or Sonnet):

- Assign random **RED / BLUE** labels (not A/B — prevents position fingerprinting).
- Include: verbatim situation, both responses, the expected-behavior signature.
- Instruct: "Ignore skill-internal terminology. Judge by decision quality only."
- Demand strict JSON:

```json
{
  "winner": "RED | BLUE | TIE",
  "reasoning": "1-3 sentences citing specific phrases",
  "skill_effect_estimate": "RED benefited | BLUE benefited | neither | unclear",
  "confidence": "high | medium | low"
}
```

### 4. Bucket the result

| Bucket | What happened |
|---|---|
| **Prevents real failure** | Baseline made a concrete error the skill prevented. |
| **Calibrates** | Both correct; skill version is better defended. |
| **Matches baseline** | No difference. **Must** re-test with hard probe before concluding. |
| **Overreaches** | Skill made it worse. Treat as a bug. |

If standard probe = "matches baseline" but hard probe = "prevents real failure", report the hard probe's bucket.

## Cost

~52k tokens per probe per skill (35k haiku for the pair + 17k for the judge).

## Figure-task extension

For visualization skills, add these steps after the blind judge:

- **Visual inspection**: render both outputs (SVG/PDF → PNG via Playwright screenshot) and view them side-by-side. Don't trust code review alone.
- **Numeric rubric** (22 pts): score palette discipline, typography, information architecture, statistical annotation, reproducibility, and review readiness — before reading the blind verdict.
- **Hard rule**: code that *says* the right thing but *renders* wrong is a failure. `constrained_layout collapsed to zero` is not cosmetic — it means the figure is unreadable.

## Anti-patterns

- Probe with no decidable right answer → judge hand-waves. Rewrite.
- Two probes testing the same trigger → wasted budget. Each probe should hit a different decision boundary.
- Probe whose right answer is "ask a clarifying question" → both agents will ask; can't distinguish.
- Running on Sonnet-class agents only → differences vanish. Calibrate for haiku.
- Letting skill vocabulary ("Phase 3", "六阶梯") appear in the judge prompt without redaction → fingerprinting degrades blind judgment.
