# Narrative Coherence

Does this skill read as one coherent story, or as fragments stitched together?

## When to use

- After merging content from multiple sources into one skill.
- When a skill "feels long" but you can't pinpoint why.
- Before finalizing a skill that went through multiple rounds of additions.
- As a quality gate after Design Audit flags low Structure or Granularity scores.

## Skip when

- The skill is brand new and written in one pass (coherence is usually fine).
- You're only checking loadability or behavioral impact.

## The core test

Read the skill top-to-bottom as a first-time reader. Ask one question:

**Can I summarize what this skill does in one sentence, and does every section
serve that sentence?**

If yes → coherent. If sections exist that serve a *different* sentence → fragmented.

## Symptoms of fragmentation

| Symptom | What it looks like |
|---|---|
| **Appendix syndrome** | New content appended at the bottom with its own headers, disconnected from the flow above. |
| **Repeated framing** | Multiple sections each re-explain "when to use" or "purpose" in slightly different words. |
| **Vocabulary drift** | The same concept gets different names in different sections (e.g. "stage" vs "layer" vs "phase" for the same thing). |
| **Orphan constraints** | A "hard rule" or "pitfall" that only makes sense if you read a specific section — but it's listed in a generic catch-all block far away. |
| **Parallel structure where there should be sequence** | Sections that look like siblings (same heading level, same format) but are actually steps in a pipeline. |
| **No single reading path** | Reader must jump around to understand the skill; no linear path works. |

## Procedure

1. **Read the skill end-to-end.** Note where your attention breaks — where you feel "wait, why is this here?" or "didn't I already read this?"

2. **Identify the one-sentence story.** What is this skill's single job? Write it down.

3. **For each section, ask:** Does this section advance the story, or is it a separate story that got stapled on?

4. **Verdict — one of three:**

| Verdict | Meaning | Action |
|---|---|---|
| **Coherent** | One story, every section serves it. | No structural change needed. |
| **Fixable** | The pieces belong together but the narrative thread is broken. Rewrite can unify them. | Restructure: find the logical sequence, rewrite transitions, merge redundant sections, move constraints next to the steps they constrain. |
| **Must split** | The skill contains 2+ genuinely independent jobs that cannot share one narrative. | Apply progressive disclosure: keep a thin orchestration layer (like Think-then-Act) and push each job into its own sub-skill file. |

5. **If "Must split" — apply the toolkit pattern:**
   - The parent SKILL.md becomes an orchestration layer: defines what sub-skills exist, when to use each, recommended sequence, and valid combinations.
   - Each sub-skill gets its own file with its own when-to-use / procedure / output.
   - The parent does NOT contain procedure details — only routing logic.
   - Reference: `think-then-act` (4 postures as independent files) and `skill-evaluator` itself (4 checks as independent files).

## What "fixable" restructuring looks like

Before (fragmented):
```
# My Skill
## When to use
## Procedure (steps 1-5)
## Pitfalls
## New Feature X (added later)
### When to use X
### Procedure for X
### Pitfalls for X
## Hard rules
```

After (coherent):
```
# My Skill
## When to use (covers both original + X as one story)
## Procedure (steps 1-7, X integrated at the right point in the sequence)
## Hard rules (all constraints in one place, each next to what it constrains)
```

The key move: X is not a separate feature — it's a step in the same workflow.
If it truly IS a separate feature, it should be a separate file.

## Cost

~4k tokens (one read-through + verdict). No subagent needed — this is a judgment call, not a measurement.
