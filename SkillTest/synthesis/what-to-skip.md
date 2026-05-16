# Synthesis — What to Skip

**Round:** R1 (R1.A + R1.B + R1.C)
**Date:** 2026-05-16
**Status:** SkillTest research zone — these were tested and explicitly
rejected. Documented here so future rounds don't re-test the same patterns
hoping for a different result.

## Skipped patterns

### 1. The "first move: backend selection" gate (from nature-figure)

nature-figure's SKILL.md opens with a hard blocking gate: "If the user has
not chosen Python or R, ask 'Python or R?' and stop." For MinionsOS Writer's
normal flow this is friction without value — Writer already operates in a
Python-first project context, and the gate would force a clarifying turn at
every figure call.

**Reason to skip:** The benefit (avoiding cross-render mistakes) is real but
narrow; the cost (interrupting every figure call with a question whose
answer is almost always "Python" in MinionsOS) is too high. If a project
genuinely needs R, the skill can document it as a one-time project-level
decision, not a per-call gate.

### 2. Privacy / template-attribution wording (from nature-figure)

nature-figure has a "User-facing privacy rule" section: "do not disclose
private local paths, private filenames, chat-attachment names, internal
reference filenames, template identifiers." Useful for the original
proprietary lab context this skill came from, but irrelevant for MinionsOS
which already has its own boundary rules under `minions/roles/SYSTEM.md`.

**Reason to skip:** Domain mismatch. MinionsOS skills cite their evidence
sources (artifact paths, EACN events) as a load-bearing convention; this
privacy rule directly contradicts that.

### 3. Custom asymmetric multi-panel hero recipes (from both figure skills)

R1.A nature-figure and R1.B scientific-figure-making both produce wrong
layouts on case-multi-panel using custom asymmetric grids. The user
explicitly preferred baseline's standard `width_ratios=[2,1,1] + gs[1, :]`
both times.

**Reason to skip:** The "asymmetric is more sophisticated" intuition that
both skills encode is wrong for 4-panel composites. Skipping the original
recipes; replacement default lives in `proposed-skills/figure-layout-defaults.md`.

### 4. The "academic-paper" 12-agent pipeline skill

Listed in `imported-paper-skill-catalog.md` as a candidate, but reviewed
during R1 planning and explicitly excluded from R1 testing.

**Reason to skip:** Violates user's "skill should guide, not lock the
workflow" rule. The 12-agent pipeline imposes a fixed sequence (intake →
literature → architecture → argument → drafting → citations → abstract →
peer review → format) that overrides MinionsOS Writer's existing
event-driven model. Importing it would mean replacing Writer's role-based
flow with a chain-of-agents flow; that's a system architecture change, not
a skill port.

If a future round wants to extract specific elements (e.g. the Style
Calibration intake from past papers, or the bilingual abstract requirement),
those are independent extractions, not a wholesale import.

### 5. Anti-AI-trace heuristics (from nature-polishing — partially)

The "no `crucial / delve into / important to note / substantial`" blacklist
was effective in R1.C but not load-bearing — both baseline and candidate
runners removed these terms in 2026 even without the skill. The blacklist
itself is fine to include for redundancy, but should not be presented as
the skill's main contribution.

**Reason to partially skip:** Don't elevate this to a top-level rule; it's
a defensive measure, not a transformative one. Keep as a quick-check
appendix.

### 6. Long lists of "phrasebank" formulas (from nature-polishing references)

The `references/phrasebank-playbook.md` file in nature-polishing is ~30 KB
of phrase families ("further investigation is required", "in keeping with
prior reports", etc). Useful as a search index for human authors; load-cost
is high for an LLM that already generates this register.

**Reason to skip the bulk:** The phrasebank's specific phrase families don't
add value over what an Opus / GPT-class model already produces. Keep only
the *categories* (hedging / transition / evidence / limitation / future-work)
as a checklist, not the specific phrases.

## What "skip" means operationally

For SkillTest purposes:
- "Skip" entries are not re-tested in future rounds unless someone identifies
  a new context where they might apply (e.g. R2 fixtures targeting a different
  audience).
- The original skill files in `/Users/mjm/Skill/` are unchanged. Skipping
  affects only what goes into `proposed-skills/` and `proposed-updates/`.
- If a future round disagrees with one of these decisions, document the
  reason and re-test before re-including.
