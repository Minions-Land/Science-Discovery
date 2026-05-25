---
name: coding-methodology
description: "Three-phase coding pipeline — Plan → Review → Simplify — each gated by a fixed smoke test. Open before any change that touches shared state, public APIs, or ≥2 files, or adds any new public function or class."
---

# Skill — Coding Methodology

A discipline for writing code that works on the first commit and stays clean. The work moves through three phases — **Plan**, **Review**, **Simplify** — and each phase exits through the same gate: a fast, fixed local check suite. You do not advance to the next phase until the gate is green.

The phases are not a checklist. They are a sequence of *decisions*: what to write, what was actually written, what to leave behind. Each phase exists because skipping it produces a specific class of bug. Phase 1 is where assumptions hide, Phase 2 is where the diff lies to you, Phase 3 is where cleanup quietly changes behavior.

## When to invoke

Run the methodology by default for any non-trivial code change. Phase 1 and Phase 2 always run together; Phase 3 runs once the implementation is accepted or cleanup is explicitly requested. The triggers below decide whether the methodology applies at all.

Apply when:

- the change touches shared state, public APIs, lifecycle, or more than one file;
- the edit changes more than 20 lines in one module;
- you are about to add a new public function, class, or module;
- you are about to dispatch the work to a non-trivial subagent;
- the request has multiple reasonable interpretations;
- you are tempted to "just refactor this quickly while I'm here."

Skip for single-file, single-function edits with no caller impact: comment fixes, typo corrections, isolated one-line bug fixes.

If the user has explicitly limited scope ("just implement, don't clean up", "just review the diff"), the user's scope wins. Do not auto-launch cleanup the user did not ask for.

## The Gate

Every phase exits through the same fast local check suite — adapted to the project's toolchain:

```
<lint>          # ruff check, eslint, golangci-lint, ...
<format-check>  # ruff format --check, prettier --check, gofmt -l, ...
<typecheck>     # mypy, pyright, tsc --noEmit, ...   (skip cleanly if the project has none)
<unit-tests>    # pytest tests/unit/, npm test, go test ./..., ...
```

Slow integration, end-to-end, and GPU tests are deliberately out of scope: the gate has to be fast enough to run after every phase without thinking about it. Heavy verification belongs to a later stage.

The gate has one strict rule: **a check that did not run is not a passing check.** A missing tool, a timed-out command, a skipped step — none of these count as green. The message reporting the gate must name every check that ran and every check that didn't, and why.

When a phase is delegated to a subagent, the gate commands belong in the subagent's prompt. Verification does not transfer by reference: a subagent that returns "done" without having run the gate has not completed the phase.

## Procedure

### Phase 1 — Plan

Decide how to write the code before writing any of it. Planning is an act of *reading*: the plan is only as good as your understanding of the territory it will land in.

1. **Read the territory.** Open the file you'll touch — its exports, its immediate callers, the shared helper modules it depends on. Depth is proportional to the change: a one-line patch reads the function and its callers; a cross-module change reads the module's exports and any helper it shares with siblings. The most expensive phrase in any codebase is "looks orthogonal to me" — duplicate helpers, conflicting state writers, and double-handled errors all begin there. If after reading you still don't understand why nearby code is shaped the way it is, that confusion *is* the assumption you need to surface.

2. **Surface assumptions.** State explicitly what you're taking for granted about the request, the file, and the contract you're about to touch. If genuinely uncertain, ask. If the request has multiple plausible interpretations, present them — do not silently pick one. Reading well in step 1 makes this step honest; without it you will surface only the assumptions you already knew you were making.

3. **Choose the simplest approach.** The minimum code that satisfies the verifiable success criterion. No features beyond what was asked. No abstractions for single-use code. No "flexibility" not requested. No error handling for impossible scenarios. If a senior engineer reading the diff would call it overcomplicated, simplify before writing it.

4. **Pick a side when the territory is divided.** When step 1 turns up *two contradicting patterns* in the same module or package for the thing you're about to write — two error-handling styles, two state-writer shapes, two test conventions — pick the side with more recent activity or more callers, write your code in that style, and record the other as a separate cleanup item. Code that splits the difference satisfies neither convention and forces every future reader to relearn the disagreement.

5. **Scope the change surgically.** Touch only what your plan requires; do not improve adjacent code; match the style you aligned to in step 4 (or, if no division, the existing style). Every changed line traces back to the request.

6. **Define verifiable success.** Convert the task into a concrete check the gate or a new test will exercise:
   - "Add validation" → tests for invalid inputs that fail today and pass after.
   - "Fix the bug" → a test that reproduces the bug today and passes after.
   - "Refactor X" → the existing tests pass before and after, unchanged.

**Output of Phase 1**: a 3–6 line plan, naming the files you've read, the assumptions, the chosen approach, the pattern you're aligning to (when relevant), and the verification criterion.

**Phase 1 exits when**: the plan exists, the assumptions are explicit, no ambiguity remains, the success criterion is concrete enough to run.

### Phase 2 — Review

Implement the plan, then read your own diff before calling it done.

1. **Implement step by step against the plan.** Take one planned step at a time and verify its criterion before moving on. Resist drifting outside the plan; if you discover something genuinely necessary that wasn't planned, treat it as a re-plan, not as scope creep.

2. **Self-review the diff along five axes**, in priority order:
   - **Behavior correctness** — logic errors, state corruption, broken edge cases, missing error propagation.
   - **Boundary fit** — did you stay inside the write scope you set in Phase 1? Did you bypass the project's intended interfaces? Did you touch generated state, lockfiles, or migrations unnecessarily?
   - **Configuration and persistence** — migration behavior, default values, environment isolation, backward compatibility on persisted shapes.
   - **Test coverage** — changed behavior either has a fast local test or a clear reason it doesn't.
   - **Style** — only when it affects maintainability or contracts.

3. **Fix high-confidence issues; defer the rest.** If you're sure something is wrong, fix it now. If you're unsure, write it down for later rather than churning the diff with speculative changes.

**Phase 2 exits when**: the gate passes.

### Phase 3 — Simplify

Focused cleanup on code that already works. The boundary is sharp: cleanup must not change observable behavior or public contracts. Anything that *would* change them is not cleanup — it is a new task, and it needs to start over from Phase 1.

1. **Stay inside Phase 2's footprint.** Touch only the files you changed in Phase 2; do not wander into adjacent modules. Pre-existing dead code is not in scope unless the user asked for it.

2. **Read nearby patterns again.** The reading in Phase 1 was for understanding; this reading is for *style alignment*. Match local naming, helper APIs, error handling, typing conventions, and test style — your code should look like the code around it.

3. **Simplify by reduction.** Remove duplication, flatten unnecessary nesting, clarify names, replace clever one-liners with readable code, delete stale comments that just narrate obvious code, consolidate scattered related logic. Stop when each remaining piece is doing one thing clearly.

4. **Hold the line on contracts.** Public function signatures, CLI behavior, file formats, network message shapes, persisted state semantics — these stay byte-identical through Phase 3. If a cleanup move would change one, drop the move.

5. **Choose clarity over brevity.** Don't collapse three readable steps into one nested ternary. Don't merge concerns to save a function. Don't strip an abstraction that was paying for itself. Cleanup that future-you can't debug is not cleanup.

6. **Re-run Phase 2's gate verbatim** — same commands, same fixtures. Phase 2's gate is the comparison point, not just any green smoke run. A check that passed before cleanup and fails after means the simplification changed behavior; revert that part and try again.

**Phase 3 exits when**: every check that passed at the end of Phase 2 still passes.

## Pitfalls

- **Skipping Phase 1 because the task feels obvious.** The obvious-looking tasks are exactly where the load-bearing assumptions hide; the feeling of obviousness is the warning sign, not the all-clear.
- **Editing a file you have not read this session.** Reading 200 lines before a 5-line change is not overhead; *not* reading them is the overhead, paid later in the form of a duplicate helper or a contract violation you didn't see.
- **Calling the gate green when one of its commands didn't actually run.** This is the failure mode that survives review most reliably: the message says "all green" and the diff merges. Silent skip is not a pass.
- **Treating the three phases as a ritual to rush through.** Each phase produces an artifact (a plan, a diff, a clean diff) — but the artifact is downstream of the thinking. Rushing produces the artifact without the thinking, and the bugs land later.
