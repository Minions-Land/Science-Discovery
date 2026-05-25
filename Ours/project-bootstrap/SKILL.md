---
slug: project-bootstrap
summary: Project bootstrap — three-gate checklist before writing the first line of code. Ensures version control, documentation boundaries, and architecture contracts are in place so AI-generated code stays predictable and maintainable.
layer: logical
tools:
version: 2
status: active
references: coding-methodology, think-then-act, feature-implementation
provenance: human+agent
---

# Skill — Project Bootstrap

Three gates that must pass before the first implementation line is written.
The gates are sequential — each depends on the previous. Skip none.

## When to use

- Gru creates a new project and Coder receives the first implementation task.
- Inheriting an author repo that has no CLAUDE.md, no architecture doc, and
  no clear module boundaries.
- The user says "let's build X" and there is no existing scaffold.
- After a failed "vibe coding" session left unmaintainable code — reset
  and re-bootstrap properly.

**Skip when:**
- The project already has CLAUDE.md + architecture doc + git history
  (the `project_{port}/CLAUDE.md` written by Gru at project_create counts).
- You are making a change to an existing, well-structured project
  (use `coding-methodology` instead).
- The task is a one-off script that will never be maintained.

## The three gates

### Gate 1 — Version control

**Acceptance:** the project's `parent_repo.git/` is seeded, worktrees
exist under `branches/`, and the branching convention is operational.

**Procedure (MinionsOS context):**

1. Verify `project_{port}/parent_repo.git/` exists (Gru's `mos_project_create`
   handles this). If working outside MinionsOS, check `.git/` exists; if not,
   `git init`.
2. Confirm `.gitignore` is appropriate for the stack. For MinionsOS projects,
   the author repo's `.gitignore` is inherited at seed time.
3. Verify `branches/coder/` worktree is checked out and clean.
4. State the branching model in `project_{port}/CLAUDE.md`:
   - MinionsOS default: each role has its own branch, cross-role artifacts
     travel through `branches/shared/` via `mos_publish_to_shared`.
   - Solo project (outside MinionsOS): commit to `main`, tag releases.

**Why this gate exists:** AI-generated code iterates fast. Without git,
a single bad generation can destroy hours of work with no recovery path.
Every "undo" becomes a manual archaeology exercise.

### Gate 2 — Documentation boundaries

**Acceptance:** project-level guidance documents exist so every Role and
every future AI session shares the same context.

| Document | Location (MinionsOS) | Minimum viable content |
|---|---|---|
| `CLAUDE.md` | `project_{port}/CLAUDE.md` | Stack, commands, module responsibilities, coding conventions |
| `AGENTS.md` | `project_{port}/AGENTS.md` | Mirror for Codex sub-agent sessions |
| Architecture doc | `branches/shared/docs/architecture.md` | Module list + dependency direction + one diagram |
| Roadmap | `branches/shared/docs/roadmap.md` | Numbered phases, each with deliverable + acceptance |

**Procedure:**

1. Read Gru's project narrative in `project_{port}/CLAUDE.md`. If it only
   has a high-level description, enrich it with: build/test/lint commands,
   module map, coding conventions, extension points.
2. Generate `docs/architecture.md` with: layer diagram (ASCII or Mermaid),
   module responsibilities, dependency rules (who can import whom),
   data flow for the primary use case.
3. Generate `docs/roadmap.md` with: phased plan, each phase has a
   deliverable and a "done when" criterion.
4. Publish docs to `branches/shared/docs/` via `mos_publish_to_shared`.
5. Commit enriched `CLAUDE.md` on `branches/main/`.

**Why this gate exists:** without explicit boundaries, AI fills every gap
with its own assumptions. Two sessions later, the codebase has three
competing patterns for the same concern. Documentation is not bureaucracy —
it is the constraint surface that keeps AI-generated code coherent across
Roles and across context resets.

### Gate 3 — Architecture contracts

**Acceptance:** the codebase has enforceable module boundaries — not just
documented, but structurally present in the file system and (where
possible) in tooling.

**Procedure:**

1. Create the directory structure on `branches/coder/` matching
   `docs/architecture.md`:
   ```
   src/
     module-a/
     module-b/
     shared/        # only things that genuinely cross boundaries
   ```
2. Each module gets a barrel file or `__init__.py` that defines its
   public API. Internal files are private by convention.
3. State dependency rules as a one-way graph:
   - `module-a` may import from `shared/` but NOT from `module-b/`.
   - Violations are detectable by grep or lint rule.
4. If the stack supports it, add a lint rule or import restriction
   (ESLint `no-restricted-imports`, Python `import-linter`, Rust
   `pub(crate)` boundaries).
5. Add a minimal test scaffold: one test file per module, even if the
   test is just "module imports without error".
6. Commit on `branches/coder/`: "scaffold: module boundaries + test stubs".

**Why this gate exists:** low coupling and clear responsibility are not
emergent properties — they must be designed in from day one. Once modules
start importing each other freely, untangling them costs 10x more than
preventing the tangle. The directory structure IS the architecture; if
the structure doesn't enforce the boundaries, the boundaries don't exist.

## After the gates: hand off to coding-methodology

Once all three gates pass, the project is ready for implementation.
From this point forward, use `coding-methodology` (Plan → Review →
Simplify) for each change, and `feature-implementation` for each
feature task from Gru. The bootstrap skill does not re-run unless
the project undergoes a major restructure (adding/removing top-level
modules, changing dependency graph direction, or switching stacks).

## Ongoing governance (the gates are not one-shot)

The three gates produce artifacts that **stay alive** throughout the
project. Two rules keep them from rotting:

**Docs-before-code rule.** Any change that alters module boundaries,
adds a new module, changes dependency direction, or introduces a new
pattern must update `docs/architecture.md` and/or `CLAUDE.md` BEFORE
the implementation commit. The doc change and the code change may be
in the same PR, but the doc diff must come first in commit order. This
prevents "architecture drift" where the docs describe a system that no
longer exists.

**Decision log.** Add a `## Decision Log` section to `project_{port}/CLAUDE.md`
(or a separate `branches/shared/docs/decisions.md`). Each entry is one line:

```
- YYYY-MM-DD: <what was decided> — <why> — <alternatives rejected>
```

This serves the same role as ADRs (Architecture Decision Records) but
at minimal ceremony. When a future Role session asks "why is it done this
way?", the answer is in the log, not lost to context compaction.

## Scaling (match ceremony to complexity)

Not every project needs the full three-gate treatment:

| Project size | Gate 1 | Gate 2 | Gate 3 |
|---|---|---|---|
| **Small** (≤3 modules, <500 LOC expected) | Full | CLAUDE.md only (skip architecture.md, roadmap.md) | Flat `src/` with no barrel files; skip lint rules |
| **Medium** (4–10 modules, 500–5000 LOC) | Full | CLAUDE.md + architecture.md | Directory structure + dependency direction stated; lint rules optional |
| **Large** (>10 modules or multi-role project) | Full | All four documents | Full enforcement: barrel files, lint rules, test scaffold |

The agent judges size from Gru's project narrative or the user's
description. When in doubt, start at Medium — it is cheaper to skip a
doc than to untangle a codebase that grew past its scaffold.

## When gates partially fail

Not every gate can pass cleanly on the first attempt:

- **User/Gru won't answer architecture questions:** Infer from the stated
  goal. Propose a 2–3 module split, state your assumptions explicitly in
  CLAUDE.md, and mark them `[assumed — confirm with user]`. Proceed; do
  not block indefinitely. Send an EACN message to Gru noting the
  assumptions made.
- **Stack doesn't support import linting:** Skip step 4 of Gate 3.
  Document the dependency direction as a convention in CLAUDE.md and rely
  on code review (human or AI) to enforce it. The directory structure
  still provides the primary boundary.
- **Project is too early to know the modules:** Use a single `src/` with
  no internal boundaries. Gate 3 acceptance becomes: "directory exists,
  one test file exists, CLAUDE.md states that module extraction is
  deferred until the first 3 features land." Revisit after feature 3.

The principle: **a partially-passed gate is better than no gate at all.**
Document what was skipped and why; don't silently drop the requirement.

## The "predictability" principle

The three gates serve one meta-goal: **make the system predictable**.

- When something breaks, you know which module to look at (Gate 3).
- When you forget what was decided, you read the docs (Gate 2).
- When you need to undo, you check git history (Gate 1).

A predictable system is one where problems are **localizable**. An
unpredictable system is one where every bug could be anywhere, every
change could break anything, and every Role session starts from scratch
because there is no shared context to build on.

## Anti-patterns this skill prevents

| Anti-pattern | How it manifests | Which gate prevents it |
|---|---|---|
| "Freestyle coding" | AI generates code with no plan; each session contradicts the last | Gate 2 (docs define the plan) |
| "God module" | Everything in one file/folder; no boundaries | Gate 3 (directory = architecture) |
| "Lost work" | User says "undo that" but there's no commit to revert to | Gate 1 (git from minute one) |
| "Competing patterns" | Three different auth approaches in the same codebase | Gate 2 (CLAUDE.md states the one pattern) |
| "Untestable tangle" | Can't test module A without spinning up modules B, C, D | Gate 3 (dependency direction enforced) |
| "Context amnesia" | New Role session doesn't know what was decided before | Gate 2 (CLAUDE.md + Decision Log) |

## Customization

The three gates are fixed, but the specific artifacts are stack-dependent:

- **Web app (React + Node):** `CLAUDE.md` includes component conventions,
  API route patterns, state management choice. Gate 3 uses
  `src/features/` or `src/modules/` layout.
- **Python package:** `CLAUDE.md` includes `pyproject.toml` conventions,
  test runner, type checker. Gate 3 uses `src/<pkg>/` with `__init__.py`
  public APIs.
- **Monorepo:** Gate 3 creates `packages/` or `apps/` with explicit
  dependency declarations between packages.
- **MinionsOS project:** Gate 2 docs go to `branches/shared/docs/`.
  Gate 3 structure lives on `branches/coder/`. Cross-role handoffs
  use `mos_publish_to_shared`. Architecture decisions are recorded in
  the exploration DAG via `mos_dag_append` in addition to the decision log.

The skill adapts to the stack; the gates do not change.
