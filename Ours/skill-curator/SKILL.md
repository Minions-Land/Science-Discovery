---
name: skill-curator
description: Distill raw trajectory and Draft (L1 process memory) into Skill / Agent evolution proposals — add, revise, merge, split, drop on the knowledge axis; spawn, dismiss, merge, split on the Agent axis. The proposal layer of the Skill family — does NOT write to the Library directly; outputs a proposal document that Ethics audits before skill-forge admits anything. Use when periodically scanning a project's trajectory for repeating patterns that deserve codification, or when an Expert/role footprint has visibly drifted. Trigger phrases include "curate skills", "propose skill changes", "review skill library", "scan for new skills", "skill-curator", "evolve skills", "audit Expert footprint".
metadata:
  version: 1.0.0
  layer: meta-orchestration
  references: [skill-forge, skill-evaluator, skill-edit]
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# skill-curator — Proposal layer of the Skill family

**What this does:** Reads raw trajectory (events, Draft, shared artefacts) and emits a *proposal document* describing how the Skill library and Expert population should evolve next. Never writes to the library or modifies Experts directly — that is gated behind Ethics audit + skill-forge.

**Position in the Skill family:**

```
                  raw trajectory
                       │
                       ▼
                ┌──────────────┐
                │ skill-curator │  ← proposes (this skill)
                └──────────────┘
                       │  proposal.md
                       ▼
                ┌──────────────┐
                │   Ethics      │  ← audits proposal
                │   skill-audit │
                └──────────────┘
                       │  approved subset
                       ▼
                ┌──────────────┐
                │  skill-forge  │  ← orchestrates form + behavior
                │   ├─ skill-edit
                │   └─ skill-evaluator
                └──────────────┘
                       │
                       ▼
                  Skill Library
```

This skill operates the leftmost box. The box is independent of the others by design (decorrelation): the proposer must not also be the validator.

## When to invoke

Open this skill when:

- The user types `/skill-curator`, says "curate skills", "propose skill changes", "review skill library", "evolve skills", "scan for new skills", "audit Expert footprint".
- A project has accumulated meaningful trajectory (Draft has tens of nodes; events log spans weeks) and no curation pass has run recently.
- A specific symptom is visible: repeated dead-ends with no Skill capturing the lesson; an Expert that consistently does work outside its declared domain; two Skills that have visibly converged in scope.
- Inside MinionsOS: the Noter periodic-wake skill `skill-curator-loop` calls this on a cadence — that is the canonical trigger surface.

Skip when:

- The trajectory is too thin (fewer than ~10 Draft nodes, or fewer than ~5 distinct Expert sessions). Proposals from sparse data are noise.
- A curation pass ran in the past 24 hours with no new patterns since.
- The user asks for a single new skill from a single example — that is the Create mode of skill-forge, not curation.

## What the curator looks at

Two axes of evolution, one trajectory source.

| Axis | What evolves | Inputs read |
|---|---|---|
| **Knowledge** | Individual Skills inside the library | Draft nodes, EACN messages, shared artefacts (especially repeating failure patterns and confirmed practices) |
| **Agent** | Expert population (count, scope, identity) | Expert participation patterns, domain-pack usage, EACN task acceptance/rejection rates, cross-Expert overlap |

Both axes feed off the same raw trajectory. A "merge" on the Knowledge axis collapses two redundant Skills into one; a "merge" on the Agent axis dismisses two Experts and spawns one with the union of their domains.

## Five operations on the Knowledge axis

| Op | Trigger pattern | Output shape |
|---|---|---|
| **add** | Repeated successful pattern (≥3 occurrences) with no Skill capturing it | Draft SKILL.md (will pass through skill-forge Stage 1 next) |
| **revise** | Existing Skill misfires, has stale anchors, or its description no longer matches body | Patch + rationale tied to specific failure cases |
| **merge** | Two Skills overlap ≥70% in trigger conditions or in cited evidence | Pair of skill paths + proposed combined name + scope statement |
| **split** | One Skill carries two different decision boundaries that have started conflicting | Original path + two child names + division rule |
| **drop** | Skill has not triggered in N curation cycles AND no failure case is unique to it | Path + last-trigger date + redundancy proof |

## Four operations on the Agent axis

These are *permanent topology changes*, not sub-agent dispatches. Sub-agents are temporary executors spawned within a single task; Agent-axis operations change who exists in the project across tasks.

| Op | Trigger pattern | Output shape |
|---|---|---|
| **spawn** | Recurring task class falls outside every existing Expert's stated domain (≥3 instances rejected/awkwardly handled) | Proposed Expert name + domain pack + initial Skill set |
| **dismiss** | Expert has not won a bid / completed a task in N curation cycles AND no domain it covers is unique | Expert id + last-active date + domain coverage proof |
| **merge** | Two Experts have converged on overlapping domains AND consistently bid on the same tasks | Pair of Expert ids + union domain pack + reason |
| **split** | One Expert is consistently doing work in two domains that conflict in method or evidence standards (e.g. theory + experiment), and the conflict surfaces as quality issues | Expert id + two child Expert specs + domain partition rule |

A *split* is distinct from spawning a sub-agent: a sub-agent is a within-task tool; a split changes the project's permanent Expert roster and creates two AgentCards on EACN where there was one.

## Procedure

### 1. Confirm scope

Before reading anything, confirm with the user (or with the Noter loop calling you):

- **Which project?** A specific `project_{port}/` or the global `~/.claude/skills/` library.
- **Which axis?** Knowledge only, Agent only, or both. Defaults to both.
- **Lookback window?** Default: since last curation pass, or 7 days if none.

### 2. Inventory the inputs

For Knowledge axis:
- List existing Skills in scope (`~/.claude/skills/` or `minions/roles/{role}/skills/`).
- Read each Skill's frontmatter description; do *not* read every body. Bodies are read only when a candidate touches that Skill.
- Glob the Draft, recent EACN events, recent shared artefacts.

For Agent axis:
- List Experts via `mos_list_roles` (or read `branches/main/state/role-registry.json`).
- For each Expert, sample its EACN message + task history.
- Note domain-pack assignments and bid-win rates if available.

### 3. Pattern-match in two passes

**Pass A — successes worth codifying.** Scan trajectory for *patterns that worked* and that no current Skill captures. Three or more occurrences is the working threshold; one-shot wins are usually too specific to generalise.

**Pass B — failures worth preventing.** Scan trajectory for *recurring failure modes*. The strongest candidates are failures the same role hits multiple times despite different prompts. If a failure was hit once and a Skill update fixed it, that already happened — no proposal needed.

For each candidate, record **lineage**: the specific events, Draft nodes, or artefact paths that motivated the proposal. Lineage is not optional. Without it, Ethics cannot audit and the proposal will be rejected.

### 4. Cross-check before emitting

Before adding a candidate to the proposal, run three checks:

- **Decorrelation check.** Does this proposal merely encode this curator's framing of the trajectory, or does it correspond to a behavioural pattern Ethics will be able to verify by reading the cited events independently? If the latter is doubtful, weaken the proposal or drop it.
- **Library coherence.** Does the candidate conflict with, duplicate, or undermine an existing Skill? If yes, reframe as `revise`, `merge`, or `split` rather than `add`.
- **Drop-conjugate check.** Every `add` should be accompanied (where possible) by a `drop` of a Skill the new one supersedes. Pure adds, never drops, are how libraries rot.

### 5. Emit the proposal

**Path convention.** All paths in proposal files and audit verdicts are written **relative to the project root** (`project_{port}/`), not absolute. Roles already operate inside their worktree so the project root is unambiguous. Absolute paths only appear in lineage `artefact:` entries that point outside `project_{port}/`.

Write to (project-scoped curation):

```
branches/shared/notes/skill-proposals.md
```

(Resolves to `project_{port}/branches/shared/notes/skill-proposals.md` from any Role's perspective.)

Or for the global library curation (no project context):

```
~/.claude/skills/_proposals/proposals-YYYY-MM-DD.md
```

Schema (one block per proposal). The **common fields** are required for every op; the **per-op fields** below are additionally required. Every numeric threshold cited in [[skill-audit]] must appear as a literal numeric value here — Ethics will reject proposals where the audit cannot verify the threshold from the proposal text alone.

**Common fields (always required):**

```markdown
## proposal-YYYYMMDD-NNNN

- **proposal_id**: proposal-YYYYMMDD-NNNN  ← stable across passes; never reuse
- **pass_id**: <ISO date of curation pass>
- **status**: proposed  ← lifecycle: proposed → audited-accepted | audited-rejected | audited-held → enacted | superseded
- **op**: add | revise | merge | split | drop | spawn | dismiss
- **axis**: knowledge | agent
- **target**: <skill path | expert id | "new">
- **rationale**: 1–3 sentences. State the decision, not the story.
- **lineage_source**: cross-role | noter-only
- **lineage**:
  - event: <event_id> (<one-line summary>)
  - draft: <node_id> (<one-line summary>)
  - artefact: <path>
- **predicted_effect**: what changes in agent behaviour if this is admitted
- **risk_flags**: reward-hacking patterns to watch (token bloat, universal hedging, etc.)
- **suggested_next**: skill-forge stage to enter, mos_spawn_role / mos_dismiss_role / Signboard, etc.
```

**Per-op required fields (in addition to the common block):**

| Op | Axis | Additional required fields |
|---|---|---|
| `add` | knowledge | `occurrence_count: <int ≥ 3>` · `comparison_set: [<list of skill paths searched>]` (proves no existing skill covers it) · `draft_skill_md: <inline draft of the proposed SKILL.md or path to it>` |
| `revise` | knowledge | `target_skill_path: <path>` · `failure_event_id: <event_id>` (the specific failure that motivates the revision) · `proposed_patch_summary: <2–3 sentences>` |
| `merge` | knowledge | `source_a: <path>` · `source_b: <path>` · `trigger_overlap_pct: <int ≥ 70>` · `verified_method: frontmatter-diff \| body-diff \| both` · `proposed_combined_name: <kebab-case>` |
| `split` | knowledge | `source: <path>` · `decision_class_a: <one-line>` · `decision_class_b: <one-line>` · `conflict_evidence: [<event_ids showing the same skill firing on the two classes with conflicting outputs>]` |
| `drop` | knowledge | `target_skill_path: <path>` · `last_trigger_date: <ISO>` · `cycles_since_trigger: <int>` · `unique_coverage_check: [<other skills shown to cover any of the dropped skill's cases>]` |
| `spawn` | agent | `proposed_expert_name: <kebab-case>` · `proposed_domain_pack: <path or inline>` · `proposed_tool_whitelist: [<tool names>]` · `overlap_pct_with_existing: {<expert_id>: <int>}` · `rejected_task_count: <int ≥ 3>` |
| `dismiss` | agent | `target_expert_id: <id>` · `last_active_date: <ISO>` · `cycles_inactive: <int>` · `coverage_replicated_by: [<other expert ids>]` |
| `merge` | agent | `expert_a: <id>` · `expert_b: <id>` · `bid_overlap_pct: <int ≥ 80>` · `union_domain_pack: <inline or path>` · `proposed_combined_name: <kebab-case>` |
| `split` | agent | `target_expert_id: <id>` · `domain_partition: {a: [<topics>], b: [<topics>]}` · `methodology_conflict_evidence: [<event_ids showing quality issues from mixing>]` · `requires_signboard: true` (always — Agent-axis split is the most consequential operation) |

**Numeric-field discipline.** Every "≥ N" requirement in the table is a literal: a `merge` proposal with `trigger_overlap_pct: 65` is auto-reject (Ethics does not have to check semantically — the number self-rejects). This makes the audit cheap and lets future tooling enforce schema mechanically.

**Lifecycle annotations.** Audit and enactment do **not** create a new file — they append a fenced sub-block under the original proposal:

```markdown
## proposal-YYYYMMDD-NNNN
...original block...

### audit (by ethics on YYYY-MM-DD)
- verdict: accepted | rejected | held
- reason: <one-line>
- audit_path: branches/shared/ethics/skill-audit-YYYY-MM-DD.md

### enactment (by gru on YYYY-MM-DD)
- result: <skill path admitted | expert id spawned | superseded by proposal-XXX>
```

This way `skill-proposals.md` is a single append-only ledger of every Skill/Agent change ever proposed. New curation passes append new proposals; never overwrite. Re-curation of a previously-rejected proposal must use a new `proposal_id` (rejected proposals do not re-open).

End the file with a manifest line: `total_proposals: N`, `axes: knowledge=K, agent=A`, `period_covered: <start>..<end>`.

### 6. Stop here

The curator does not write to the library, does not modify Experts, does not call skill-forge. Hand off to Ethics. Ethics' `skill-audit` skill walks the proposal file, accepts or rejects each entry, and forwards approved entries into skill-forge.

## Decision rules

| Situation | Action |
|---|---|
| Pattern occurred once, looked impressive | Note in Draft, do **not** propose. Wait for repetition. |
| Pattern occurred ≥3 times, no Skill covers it | Propose `add` |
| Existing Skill caused a failure | Propose `revise` with the failure event as lineage |
| Two Skills triggered on the same event in last N cycles | Propose `merge` (knowledge) |
| One Skill's last-modified is ≥3 cycles ago and no trigger fired since | Candidate `drop` — but verify no failure case is unique to it first |
| Expert keeps absorbing tasks outside its domain | Propose `revise` of its domain pack OR `split` if two distinct domains have grown |
| Two Experts always bid on the same tasks | Propose `merge` (agent) |
| Curator's own previous proposal was rejected by Ethics | Read the rejection reason. Adjust rule, do not re-propose the same thing |

## Pitfalls

- **Proposing every interesting pattern.** Most patterns are noise. The threshold (≥3 occurrences) exists because the Library is taxed by its own size — every Skill burns context at every wake-up. A proposal must clear the bar of being *worth that tax*.
- **Skipping lineage.** Lineage is the only thing that lets Ethics audit independently. A proposal without lineage is unreviewable and will be rejected. Include event ids, Draft node ids, and artefact paths verbatim.
- **Curator becoming the validator.** This skill must NEVER call skill-evaluator on its own proposals. The whole point of the architecture is that the proposer and the validator have decorrelated views of the trajectory. If you are tempted to "just check if the new Skill helps", stop — that is Ethics' (and via Ethics, skill-evaluator's) job.
- **Pure adds, never drops.** Adding without occasionally dropping is how libraries rot into 200-Skill graveyards. Every curation pass should produce at least one `drop` candidate when the library has more than ~30 Skills.
- **Confusing split with sub-agent dispatch.** Sub-agents are within-task; Agent-axis split is permanent. Never propose a `split` for transient task structure.
- **Citing the trajectory of the role you are running as.** If this skill is run from inside Noter, its proposals must be grounded in *other roles'* trajectories where possible — Noter looking at Noter is the most correlated possible review.

## Output habit

The curator's output is purely advisory. Mark every claim in the rationale with `[evidence: <event_id|path>]` or `[derived: <other_proposal>]`. Never `[speculation]` — speculative proposals waste Ethics' time. If something is speculative, it is not yet a proposal.

## Related skills

- [[skill-forge]] — receives approved proposals from Ethics; runs them through form + behavioral pipeline
- [[skill-evaluator]] — invoked by skill-forge for Stage 3 behavioral A/B; the curator must not call this directly
- [[skill-edit]] — invoked by skill-forge for Stage 2 form validation
- (MinionsOS only) `noter/skills/skill-curator-loop` — the periodic wake-up procedure that triggers this skill
- (MinionsOS only) `ethics/skills/skill-audit` — the audit procedure that gates proposals before skill-forge sees them
