---
name: codex
description: "Two-tier subagent dispatch. Tier 1 (Haiku alone) for trivial tasks. Tier 2 (Codex GPT-5.5 xhigh as the actor, wrapped in a thin Haiku Agent for first-class subagent plumbing) for everything else — Codex matches Opus 4.7 capability at lower cost than Sonnet, and the Haiku wrapper buys us run_in_background + wait_bg cache keepalive + clean summary. Triggers: /codex; user asks for codex / GPT-5.5 / second opinion / let GPT handle it / delegate this; ANY Agent dispatch the main session would otherwise route to Sonnet (refactor, multi-file edit, debug, implement-from-spec, code review, deep investigation) — these are Tier 2 by default, NOT Sonnet. Sonnet is only the degraded fallback when codex itself is unreachable."
---

# /codex — Two-tier subagent dispatch

Usage: `/codex <task description>`

Example: `/codex Fix the race condition in src/server.ts — tests are flaky under concurrent load`

---

## Mental model: two tiers, no Sonnet default

The right model layering on this host is:

| Difficulty | Subagent | Mechanism |
|---|---|---|
| **Trivial** (lookup, format, simple edit, narrow Q&A) | Haiku | `Agent(model: "haiku")` direct — Haiku alone is enough |
| **Everything else** | **Codex GPT-5.5 xhigh** (the actor) | `Agent(model: "haiku")` as a thin shell that calls the `codex` MCP tool. The Haiku wrapper is plumbing — its only purpose is to expose Codex through Claude Code's first-class Agent infrastructure, so we get `run_in_background`, cache keepalive, and a clean summary. The thinking happens inside Codex |

**Sonnet is no longer a default.** It only appears as the degraded fallback when Codex itself is unreachable (Step 5).

If you are tempted to dispatch `Agent(model: "sonnet")` because the task is "kind of medium-hard" — that is exactly the case where Tier 2 (Codex wrapped in Haiku) wins on both capability and price. Use Tier 2.

---

## Step 0 — Pick a tier

Ask one question: **can a Haiku-class model alone produce the answer reliably?**

- **Yes** → Tier 1 (Step 1).
- **No, or unsure** → Tier 2 (Step 2 or 3 depending on length).

Examples that are Tier 1:
- "What does function X return when arg is None?"
- "Reformat this list of imports."
- "Pull the URLs out of this log file."

Examples that are Tier 2:
- "Refactor this module for clarity."
- "Why are the tests flaky? Find and fix."
- "Implement this feature given the spec."
- "Code-review this PR for race conditions."

When in doubt, Tier 2.

---

## Step 1 — Tier 1: Haiku alone (trivial tasks)

```
Agent(
  description: "<3-5 word summary>",
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: "<self-contained task with all needed context>",
  mode: "auto"
)
```

Foreground is fine for most Tier 1 calls — they finish in seconds. If a Tier 1 task somehow drags past ~2 min, escalate to Tier 2.

---

## Step 2 — Tier 2A: foreground codex (short tasks ≤ 2 min)

Direct call:

```
codex(
  task: "<clear task description>",
  cwd: "<absolute path>"
)
```

### Defaults (do NOT override):
- `model`: gpt-5.5
- `sandbox`: danger-full-access
- `reasoning_effort`: xhigh

### Optional parameters (only when needed):
- `sandbox: "read-only"` — for analysis in non-git directories
- `skip_git_check: true` — when cwd is not a git repo
- `add_dirs: [...]` — extra directories Codex can access
- `timeout_seconds: N` — only when explicitly asked. **If you set this >300, switch to Step 3.**

---

## Step 3 — Tier 2B: background Codex (wrapped in Haiku Agent shell, long tasks > 2 min)

Why this exists: the `codex` MCP tool is synchronous; if codex runs 7 minutes the main session sits idle and the 5-min prompt cache expires, costing tens of thousands of uncached input tokens on the next real turn. The fix is to **wrap codex inside an `Agent(model: "haiku", run_in_background: true)`**, which upgrades Codex from "synchronous MCP tool" to "first-class Claude Code subagent". The main session immediately gets a task_id and can run a `wait_bg` loop to keep its cache warm. Haiku is just the wrapper — Codex is doing the work.

Bonus: the Haiku wrapper trims codex's raw output into a small structured summary, so the main session's context stays clean.

When to use Step 3 instead of Step 2:
- Predicted runtime > 2 minutes
- User says "long / large / many files / refactor / many tests / big change"
- You set `timeout_seconds > 300`

If unsure between Step 2 and Step 3: **prefer Step 3**. Cost of an extra Haiku relay is small (~5-10k Haiku tokens); cost of a 7-min idle main session is a full prompt-cache cold start (~50k+ uncached tokens) plus dead-air UX.

### Dispatch:

The Haiku here is **plumbing, not a thinker**. Its only jobs are: call codex with the verbatim args, copy back the structured fields codex returns, and — if codex errors — apply a narrow handbook-driven retry before giving up. Do not ask Haiku to interpret, evaluate, or improve the task. Codex itself runs at `reasoning_effort: xhigh`, so any reasoning about the task belongs there.

```
Agent(
  description: "<3-5 word summary>",
  subagent_type: "general-purpose",
  model: "haiku",
  run_in_background: true,
  prompt: """
HARD ROLE BINDING — read this twice before doing anything:

You are a mechanical relay. The main agent dispatched you for ONE reason: to
call mcp__codex-subagent__codex on its behalf. The codex MCP tool is the
actor; you are the postal worker. You do not think about the task, evaluate
codex's output, "verify what codex would have done", or attempt the task
yourself if it looks doable.

CONTRACT (violations = failed dispatch, reported as STATUS: relay_self_executed):
  1. Your FIRST tool call MUST be `mcp__codex-subagent__codex(...)`. Not Bash,
     not Read, not Write, not Edit, not Grep, not Glob, not Skill, not Agent.
     If your first tool call is anything else, you have already failed.
  2. You MUST NOT load any Skill (including the `codex` skill itself).
     Everything you need to know is in this prompt.
  3. You MUST NOT do the user's task with Bash + Read + Write yourself, even
     if it looks like a small task and you "could just do it". The whole
     point of this dispatch is that the main agent already decided codex
     should do it. Re-deciding that is out of scope for you.
  4. After codex returns, you copy its structured fields back. You do not
     add interpretation, do not run verification commands, do not "check
     codex's work". Codex is xhigh-reasoning; it does not need a Haiku
     audit.

STEP 1 — call mcp__codex-subagent__codex with these EXACT args (this MUST
be your first tool call):

  mcp__codex-subagent__codex(
    task: "<the user task — VERBATIM, no rewriting>",
    cwd: "<absolute path>",
    sandbox: "danger-full-access",
    reasoning_effort: "xhigh",
    timeout_seconds: <user-specified or 1800>
  )

If the codex tool is not available in your tool list, that itself is a
dispatch failure: skip directly to STEP 5 with STATUS: codex_unavailable
and ROOT_CAUSE: "mcp__codex-subagent__codex not registered in this session".
Do NOT fall back to doing the task yourself.

STEP 2 — branch on the result:

  IF codex.status == "success" AND codex.exit_code == 0:
    go to STEP 4 (success report).

  ELSE (error, timeout, or non-zero exit):
    go to STEP 3 (handbook lookup).

STEP 3 — handbook-driven recovery (max 2 retries total per dispatch):

  3a. Read ~/.claude/skills/codex/troubleshooting.md.
      (If that path is unreadable, fall back to
       <repo>/mcp-servers/codex-subagent/skills/codex/troubleshooting.md;
       if neither is readable, skip to STEP 5 with reason
       "handbook unreachable".)

  3b. Match the failure against the entries in order. Use the FIRST entry
      whose DETECT clause matches codex.message / status / exit_code. Always
      prefer CODEX_UNAVAILABLE / CODEX_ERROR prefix matches over substring
      matches inside codex.message.

  3c. If the matching entry has AUTO-FIX: NONE → skip to STEP 5.

  3d. If the matching entry has a concrete AUTO-FIX → apply it EXACTLY as
      written (only the args the entry names; never change task text,
      sandbox, or reasoning_effort). Re-call codex MCP. Track this as one
      retry.

  3e. After the retry, branch again:
      - success → STEP 4.
      - same failure mode → STEP 5 (do NOT retry the same fix twice).
      - new failure mode → repeat 3a-3d ONCE more (this is retry #2, the
        last allowed). After retry #2, regardless of outcome, go to STEP 4
        (if success) or STEP 5 (if still failing).

STEP 4 — SUCCESS report. Write these fields and nothing else:

  STATUS: success
  FILES_CHANGED: <codex.files_changed comma-joined, or "none">
  COMMANDS_RUN: <codex.commands_run length>
  TOKENS: input=<codex.tokens.input> output=<codex.tokens.output> cached=<codex.tokens.cached or 0>
  SUMMARY: <codex.message verbatim, truncate to 4 sentences if longer>
  KEY_FINDINGS: <if codex.message names specific files / functions / failures, list them as bullets; else "none">
  RETRIES_USED: <0, 1, or 2>
  RETRY_LOG: <if retries > 0, one line per retry: "retry N: <handbook entry name> applied <fix>"; else "none">

  End. Do not add anything after RETRY_LOG.

STEP 5 — FAILURE report. Codex could not be made to work for this dispatch.
Write these fields and nothing else. Do NOT add a recommendation about what
the main agent should do — that is the main agent's call.

  STATUS: <codex_unavailable | codex_error | codex_timeout — copy from the
           "STATUS to report" line of the matched handbook entry; if no
           entry matched, use codex_error>
  ROOT_CAUSE: <copy from the matched handbook entry; if no entry matched,
               use "unknown — see RAW_MESSAGE">
  HANDBOOK_ENTRY: <name of the matched entry, e.g. codex_cli_missing; or
                   "none" if nothing matched>
  ATTEMPTS: <count of codex invocations made: 1 if no retry, 2 or 3 if retried>
  RETRY_LOG: <one line per retry attempted: "retry N: <entry name> applied <fix> — outcome <success|same-failure|new-failure>">
  RAW_MESSAGE: <last 600 chars of codex.message from the final attempt>
  COMMANDS_RUN: <count of commands codex executed across all attempts; bounds
                 the blast radius — main agent uses this to decide whether
                 partial state needs cleanup>

  End. Do not add anything after COMMANDS_RUN. Do not include a NEXT_STEPS
  or RECOMMENDATION line — the main agent decides whether to fall back to
  Sonnet, split the task, surface a config error to the user, or abort.
""",
  mode: "auto"
)
```

### Step 3-Mini — compact relay for short / read-only tasks

When the task is read-only (analysis, lookup, "report X"), can't plausibly damage state, and the full Step-3 envelope feels heavyweight, use this stripped relay. It still gives you bg + wait_bg + a clean summary, just without the handbook-driven retry choreography. **First-attempt-or-fail**: any error escalates straight to the main agent's fallback decision (Step 5).

```
Agent(
  description: "<3-5 word summary>",
  subagent_type: "general-purpose",
  model: "haiku",
  run_in_background: true,
  prompt: """
HARD ROLE BINDING — read this twice before doing anything:

You are a mechanical relay. Your FIRST tool call MUST be
`mcp__codex-subagent__codex(...)`. Not Bash, not Read, not Skill, not Agent.
You do NOT do the task yourself, even if it looks small. The main agent
already decided codex should do it; re-deciding that is out of scope.
Do NOT load any Skill (including the `codex` skill itself) — everything
you need is in this prompt. No interpretation, no retries, no verification.

STEP 1 — call mcp__codex-subagent__codex with EXACT args (this MUST be
your first tool call):

  mcp__codex-subagent__codex(
    task: "<the user task — VERBATIM>",
    cwd: "<absolute path>",
    sandbox: "<read-only | danger-full-access>",
    reasoning_effort: "xhigh",
    timeout_seconds: <user-specified or 600>
  )

If the codex tool is not in your tool list, skip to STEP 2 with
STATUS: codex_unavailable, RAW_MESSAGE: "mcp__codex-subagent__codex not
registered in this session", EXIT_CODE: -1, COMMANDS_RUN: 0. Do NOT fall
back to doing the task yourself.

STEP 2 — report. No commentary.

  IF status == "success" AND exit_code == 0:
    STATUS: success
    FILES_CHANGED: <files_changed comma-joined, or "none">
    COMMANDS_RUN: <commands_run length>
    TOKENS: input=<tokens.input> output=<tokens.output> cached=<tokens.cached or 0>
    SUMMARY: <message verbatim, truncate to 4 sentences>

  ELSE:
    STATUS: codex_error
    RAW_MESSAGE: <last 600 chars of message>
    EXIT_CODE: <exit_code>
    COMMANDS_RUN: <commands_run length>

  End. Do not add anything else.
""",
  mode: "auto"
)
```

**When to prefer Step 3-Mini over the full Step 3:**
- Task is read-only (sandbox=read-only) or single-file write with low blast radius.
- You don't expect the handbook's auto-fixes to help (e.g., already passing `skip_git_check` pre-emptively for non-git cwd).
- You want minimal main-context cost on a routine dispatch.

**When to use the full Step 3 instead:**
- Multi-file refactor, multi-command debugging, anything where a transient 5xx retry meaningfully helps.
- First time hitting a new cwd / new task type — let the handbook catch surprises.
- Anything in danger-full-access mode that touches >2 files.

---

After the Agent dispatch returns its task_id, follow the wait_bg loop:

1. `wait_bg(deadline_seconds=45, bg_ids=[<agent_task_id>])`
2. When wait_bg ticks, check `early_exit` field:
   - If `early_exit=True`: task completed, call `TaskOutput(<agent_task_id>)` and process result.
   - If `early_exit=False`: call `TaskOutput(<agent_task_id>)` to check progress; loop if still running.
3. If still running: back to step 1.
4. If done: parse the structured summary the relay produced. The shape depends on which terminal step the relay hit:
   - **STEP 4 success** — fields starting with `STATUS: success` plus `FILES_CHANGED`, `SUMMARY`, `KEY_FINDINGS`, `RETRIES_USED`, `RETRY_LOG`. Treat the work as done and present results (Step 6).
   - **STEP 5 failure** — fields starting with `STATUS: codex_unavailable | codex_error | codex_timeout` plus `ROOT_CAUSE`, `HANDBOOK_ENTRY`, `ATTEMPTS`, `RETRY_LOG`, `RAW_MESSAGE`, `COMMANDS_RUN`. Go to Step 5 (fallback decision) below. Note the relay deliberately omits any `RECOMMENDATION` line — that decision is yours.

5. **Contract-violation check (BEFORE you trust a STEP 4 success record):** if
   the report says `STATUS: success` but the `TOKENS` line shows
   `input=0 output=0` (or the field is missing), the relay almost certainly
   did the task with its own Bash/Read/Write tools instead of calling codex.
   That is the `relay_self_executed` failure mode. Discard the report and
   apply the `relay_self_executed` row in Step 5's fallback table — do NOT
   present Haiku-quality work as though it came from codex xhigh. (For
   genuine read-only analysis dispatched via Step 3-Mini with `sandbox:
   read-only`, codex still spends input tokens reading the cwd, so
   `input=0` is the same red flag there.)

The `bg_keepalive_nudge` hook fires automatically when the Agent is dispatched in bg mode and reminds you of this loop. Trust it.

---

## Step 4 — Parallel splitting for complex tasks

When a task has 2+ independent sub-parts, split into multiple parallel calls instead of one serial mega-task.

**Default rule: one independent unit = one codex process.**

**How to split:**
- One codex call per independent work unit
- Launch all in parallel (multiple tool calls in the same response)
- Each gets a focused, self-contained prompt
- For long sub-tasks, each is its own Step-3 backgrounded Agent relay
- Merge results after all complete

**Example:** Three benchmark cases — baseline, nature-figure, scientific-figure-making:
- If each predicted < 2 min: three parallel codex MCP calls (Step 2)
- If each predicted > 2 min: three parallel Step-3 relays
- Never combine cases into a single call.

---

## Step 5 — Fallback when codex itself errors

This fires when:
- Step 2: `codex` returns `CODEX_UNAVAILABLE` or `CODEX_ERROR` directly to the main session.
- Step 3: relay's STEP 5 failure record arrives (`STATUS: codex_unavailable | codex_error | codex_timeout`). The relay has already exhausted handbook-allowed retries; do NOT re-dispatch another Haiku-wrapped codex call hoping for a different outcome.

**Hard rule: the main agent does not execute the task itself.** Tier 2 exists precisely because the main session should not be the actor for non-trivial work. When codex falls over, you still delegate — just to a different subagent. The only thing changing is the executor.

### Fallback decision (use ROOT_CAUSE from the relay's failure record):

| ROOT_CAUSE pattern | Action |
|---|---|
| `codex CLI not on PATH` / `codex auth missing or expired` / `API quota / billing block` | Surface this as a config issue to the user in the final summary AND dispatch a Sonnet subagent so the task still gets attempted. The user needs to know codex is broken at the install level, but the work shouldn't stall on it. |
| `cwd does not exist or is not accessible` | Stop. This is a caller error — confirm `cwd` with the user before any subagent dispatch. |
| `filesystem or sandbox permission denial` | Surface to the user; ask whether to retry with `add_dirs` or a different `cwd`. Do not silently fall back, because the permission wall likely also blocks Sonnet. |
| `cwd not a git repo, skip_git_check did not resolve` / `context length exceeded — task likely needs splitting` | Re-plan: split per Step 4, or restate the task. Do not blindly hand the same monolithic task to Sonnet. |
| `timeout or hang at <elapsed>s` | Decide: re-dispatch as Step 3 with a larger `timeout_seconds`, or split per Step 4. Consider the user's latency budget. |
| `API rate-limited` / `persistent upstream 5xx after one retry` | Wait briefly (the user is watching) and re-dispatch the same Step 3 call. If it fails twice in a row, fall back to Sonnet. |
| `unknown` / handbook had no entry | Fall back to Sonnet AND record the new failure mode at the end of the response so a handbook entry can be added later. |
| `relay_self_executed` (Haiku did the task itself instead of relaying to codex) | Discard the relay's output entirely — it was produced by a Haiku, not by codex xhigh, so depth-of-reasoning is wrong by construction. Re-dispatch the same task through Step 3 with an explicit reminder in the prompt header ("HAIKU PRIOR RUN BROKE CONTRACT — codex MCP is your first tool call, no exceptions"). If the second relay also self-executes, escalate to Sonnet AND surface the contract-violation event so the SKILL prompt can be hardened further. |

### Sonnet subagent fallback dispatch:

```
Agent(
  description: "<3-5 word summary> (codex fallback)",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "<same task prompt + specific files to read, commands to run, success criteria>",
  mode: "auto",
  run_in_background: <true if expected long, else omit>
)
```

For long fallback tasks, run the same wait_bg loop as Step 3.

In your final user-facing summary, note "codex unavailable (<ROOT_CAUSE>); fell back to Sonnet" so the user understands the executor swap. If the ROOT_CAUSE is a config issue (Entries 1, 2, 8 in the handbook), also tell the user explicitly what to fix — they likely want their codex install repaired even if the current task is now running on Sonnet.

---

## Step 6 — Present results

1. Summarize what was done in 2-3 sentences (use Haiku relay's SUMMARY field if Step 3 was used).
2. Show files changed and key findings.
3. If the task failed, explain why and suggest next steps.

---

## Tips for good task prompts (apply to all tiers)

- State the goal clearly in one sentence — be specific about scope and boundaries.
- Include what "done" looks like (tests pass, type-checks clean, file produced, etc.).
- Mention relevant files if the task is scoped.
- Include constraints (don't touch X, must be backwards-compatible, etc.).
- Spell out NON-GOALS explicitly for multi-file tasks — what NOT to touch / build / change. Often more useful than the goal list, because it stops Codex from drifting into "obviously also needed" adjacent work.
- Keep prompts focused: a precise, well-bounded task finishes faster and more reliably than a vague one.
