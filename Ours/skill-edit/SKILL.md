---
name: skill-edit
description: "Edit, refactor, or polish an existing SKILL.md without breaking its shape or trigger surface. Invoke when the user asks to clean up / smooth out / refactor / fix / tighten / restructure a skill, when a skill has grown rough seams from incremental edits, or when a skill's frontmatter no longer matches its body. Covers the conventions (frontmatter, trigger phrases, step structure, decision rules, pitfalls) so edits stay consistent across the skill library."
---

# /skill-edit — Edit a SKILL.md without making it worse

Skills accumulate seams: a step grows, a section is added, two sections start saying the same thing, the frontmatter description stops matching the body. This skill is the procedure for editing a skill so the result reads cleanly to a fresh agent.

Trigger phrases (treat as a request to run this skill):
- "clean up this skill", "smooth out this skill", "refactor this skill"
- "make this skill consistent", "tighten this skill", "the skill has rough edges"
- "the skill description doesn't match the body", "the steps don't flow"
- Any edit on a `*/skills/*/SKILL.md` file that is more than a typo fix

If the user only asked for a typo fix or a single-line addition, do that directly with `Edit` — don't run this whole procedure.

---

## Skill anatomy (load-bearing — every edit must respect this)

A SKILL.md has these elements, in this order:

| element | purpose | edit rules |
|---|---|---|
| YAML frontmatter (`name`, `description`) | Discovery + trigger matching. The harness shows `description` to the model when deciding whether to invoke. | Keep `description` < ~500 chars. The triggers in the body must match what `description` advertises. |
| H1 title | One-line "what this skill does." | Match the user-facing slash command (`/skill-name — …`). |
| Trigger phrases block | Natural-language phrases that should fire the skill. | Mirror the `description`. If a phrase is in the body, it must be implied by the description. |
| "Step 1 / Step 2 / …" sections | The actual procedure. | Numbered, sequential, each with a clear acceptance criterion. Don't reference a Step before it has appeared. |
| Decision rules | Tables or short bullet lists. | Use the same format throughout one skill (table OR bullet list, not both). |
| Pitfalls | Concrete failure modes the agent should avoid. | Each pitfall must reference an actual past failure or a specific harm. No generic advice. |
| Related memory | `[[name]]` links to memory entries. | Optional. Use to chain in operational context. |

A skill that violates any of these is "rough." This procedure smooths it.

---

## Step 1 — Read the whole file before editing

Use `Read` on the entire SKILL.md. Skills are short (usually <300 lines) so reading the whole thing is cheap and reading partials causes the very seams this skill exists to prevent.

While reading, build a one-paragraph mental model:
- What's the skill's job?
- What's the trigger surface?
- What's the procedure outline (just the Step headings)?
- Are there obvious duplications across sections?

Don't start editing until you can summarize all four out loud.

---

## Step 2 — Diagnose seams (before any edit)

Run through this checklist. Note every hit; don't fix yet.

| seam | how to spot it |
|---|---|
| **Description / body mismatch** | Frontmatter promises X but the body covers Y, or the body's trigger phrases aren't implied by `description`. |
| **List-shape drift** | A list says "three things" but has four items, or one bullet is 4× longer than the rest. |
| **Format drift** | Two decision rules in the same skill, one as a table and one as bullets. |
| **Forward references** | "See Step 3" appears in Step 2 but Step 3 hasn't been introduced yet, or vice versa. |
| **Duplication** | The same fact (a command, a path, a rule) appears in three sections with subtly different phrasing. |
| **Bolt-on prose** | A paragraph that reads like an interruption — usually because it was added later without rewriting the surrounding flow. Tell-tale signs: parenthetical asides longer than the main sentence, "(this used to be done by hand — don't duplicate it)" energy. |
| **Stale numbers** | "Run X test (≈17 s, expect 290+ passing)" when the test count has changed. |
| **Vague pitfalls** | "Be careful with paths." A real pitfall names what specifically goes wrong. |
| **Section order** | A "Pitfalls" section appearing before the procedure, or "Related memory" before "Pitfalls". |

Output of Step 2: a numbered list of seams. Show it to the user (one or two lines per seam) before editing if there are more than ~3, so they can prioritize. For 1-3 seams, proceed silently.

---

## Step 3 — Apply minimal edits, smallest scope first

Pick edits that resolve a seam without rewriting prose for style. Order:

1. **Single-line fixes** (stale number, broken cross-reference) — `Edit` with a tight `old_string` / `new_string`.
2. **Single-section fixes** (list-shape drift, format drift inside one section) — `Edit` the whole section.
3. **Cross-section fixes** (duplication, bolt-on prose, forward references) — these need careful sequencing. Do the "load-bearing" section first (the one others reference), then the satellites.
4. **Frontmatter** — edit last. The frontmatter description must reflect the body, so changing it before the body is settled is wasted work.

For each edit, state in one sentence what you're fixing. Don't batch unrelated fixes into one Edit — small Edits make the diff easier to read and the regression easier to bisect.

---

## Step 4 — Re-read and verify

Read the file again, in full. Check:

- The Step 2 seam list is fully resolved.
- No new seams introduced (a fix in Step 2 sometimes creates a new forward reference in Step 4, etc.).
- The frontmatter `description` still describes the body.
- All slash-command references (e.g. `/skill-name`) match the actual `name`.
- Trigger phrases in the body are subsumed by `description`.

If the harness has a registration in `~/.claude/CLAUDE.md` (most user-installed skills do), check that the registration line still describes the skill accurately. Update it if not.

---

## Step 5 — Report (appraisal-style)

One short message to the user, in **appraisal-style** format:

```
Diagnosis:   <N seams found, listed one-per-line>
Repaired:    <which seams are now fixed, with file:section pointers>
Left alone:  <what was deliberately untouched and why>
Open:        <questions only the user can decide>
```

The format matches how `skill-evaluator` reports its behavioral verdict, so the two skills produce visibly compatible artifacts when run in sequence.

End-of-turn summary: one sentence. What changed.

---

## Chain with skill-evaluator

`skill-edit` and `skill-evaluator` test two orthogonal layers:

| layer | tool | catches |
|---|---|---|
| Form (text seams, frontmatter, decision-rule shape) | `skill-edit` | description/body mismatch, list-shape drift, forward references, stale numbers |
| Effect (does adding the skill change agent behavior?) | `skill-evaluator` | skill not getting loaded, no behavior delta, "Overreaches" regressions |

Run them in that order:

1. **edit first** — text fixes are seconds; an unfixed `description` means MetaHarness's recall stage fails before behavior is even tested, wasting a paid run.
2. **evaluator after** — when the edit changed Procedure or Decision Rule, MetaHarness is your regression test for behavior. When the edit only touched cosmetics, evaluator is optional.

If a skill is brand new, do `skill-edit` once on the draft, then `skill-evaluator` once before publishing. After that, only re-run evaluator when Procedure/Decision-Rule changes.

---

## Pitfalls

- **Don't rewrite for style if the user only asked for a logic fix.** The user's edit ask is a contract; satisfying it without scope creep is more valuable than producing a "cleaner" skill they didn't request.
- **Don't drop load-bearing content.** URLs, exact commands, version anchors, model IDs, host-specific recipes — these are why the skill exists. If a section feels redundant, check whether the apparent redundancy is actually two different audiences (e.g. "Repo facts" advertises capabilities; "Step 1" tells the agent what to do with them).
- **Don't add new sections without checking what already exists.** A new "Verification" section should land inside an existing Step, not spawn a parallel structure.
- **Don't normalize section order across all your skills.** Different skills have different shapes for good reasons (a push skill has Steps; an analysis skill has Phases; a tool-design skill has Stages). Match the skill's existing shape unless that shape is itself the problem.
- **Don't break the trigger surface.** The frontmatter `description` is what the harness shows to the model when deciding whether to fire the skill. If you tighten the description and accidentally drop a trigger phrase, the skill stops firing on that phrase. Cross-check `description` against the body's trigger list before you finalize.
- **Don't confuse "rough" with "informal."** Some skills are intentionally conversational (e.g. brainstorming, dialectical-synthesis). "Smooth" doesn't mean "formal" — it means the seams are gone.

---

## Related memory

- [[reference_skill_evaluator]] — the orthogonal partner for behavioral A/B testing; chain `skill-edit` → `skill-evaluator` for full coverage of form + effect.
- [[reference_reliable_file_io_skill]] — for skills that grow past 200 lines, edit through the chunked workflow rather than a single Write.
- [[feedback_markdown_edit_reliability]] — markdown edits with code fences / CJK / smart quotes are fragile; if a skill body has those, prefer one-section-at-a-time Edit.
