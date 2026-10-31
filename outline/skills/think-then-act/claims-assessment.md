# Think-Then-Act: Claims Assessment

## Claims We CAN Make (supported by evidence)

### Claim 1: Structured planning skills measurably improve Haiku-class agent decision quality
- **Evidence:** MetaHarness A/B — 65% of skills have measurable positive effect; sub-postures (first-principles, dialectics) scored "calibrates response"
- **Strength:** Strong (controlled A/B, blind judge, 49 skills tested)

### Claim 2: The "scope before act" pattern prevents over-execution errors
- **Evidence:** MetaHarness showed coding-methodology (which shares TTA's dispatch discipline) "prevents real failure" — baseline over-executes without it
- **Strength:** Strong (decision-level error caught by blind judge)

### Claim 3: Skills can be empirically improved through targeted A/B testing
- **Evidence:** v3→v6 evolution: 3 specific failures diagnosed, 4 targeted fixes applied, P2 re-test confirmed fix
- **Strength:** Moderate (only P2 re-tested; no held-out probe set)

### Claim 4: Concrete examples outperform prose rules for overriding model defaults
- **Evidence:** v5 prose rule failed to change P2 behavior; v6 worked example succeeded
- **Strength:** Moderate (single probe, single model class)

### Claim 5: Structure outperforms raw reasoning budget (ultrathink)
- **Evidence:** Ultrathink lost all 3 probes in competitor eval
- **Strength:** Moderate (3 probes, single model class, single session)

### Claim 6: The skill design process includes removal of harmful features
- **Evidence:** Self-assessment A/B showed 2/5 wins with confounds; feature removed
- **Strength:** Strong (controlled experiment, clear negative result, action taken)

## Claims We CANNOT Make (insufficient evidence)

### ❌ Think-then-act improves end-to-end scientific discovery outcomes
- **Gap:** No system-level experiment comparing projects with vs without TTA
- **What we'd need:** Two parallel projects, same task, one with TTA disabled

### ❌ Think-then-act works on Sonnet/Opus-class models
- **Gap:** MetaHarness explicitly notes Sonnet shows no differentiation
- **Honest position:** The skill is designed for and validated on Haiku-class executors

### ❌ The full 5-posture pipeline is better than any single posture
- **Gap:** No A/B comparing full pipeline vs single-posture usage
- **What we'd need:** Probes where full pipeline is tested against just Goal-Setting or just Unstated-Premises

### ❌ Plan persistence improves multi-session task completion
- **Gap:** No controlled experiment on context-reset recovery
- **What we'd need:** Tasks that span resets, measured completion rate with vs without persisted plans

### ❌ Think-then-act generalizes beyond MinionsOS's specific agent architecture
- **Gap:** All testing done within MinionsOS's EACN + Claude Code + Haiku stack
- **What we'd need:** Testing on other multi-agent frameworks

## Recommended Paper Framing

**Safe claim:** "We introduce a composable planning skill that provides structured reasoning postures for autonomous agents. Through iterative A/B evaluation against competitor prompts and a full-library behavioral harness, we show that (a) structured planning prevents over-execution errors in Haiku-class agents, (b) concrete examples outperform prose rules for behavioral correction, and (c) the skill design process itself is empirically driven, including removal of features that fail testing."

**Avoid:** "Think-then-act enables autonomous scientific discovery" (no system-level evidence), "outperforms all baselines" (lost P1 and P3 before fixes), "works across model scales" (explicitly doesn't).
