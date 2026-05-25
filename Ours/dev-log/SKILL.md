---
name: dev-log
description: "Append a development-session journal entry to dev-log/<YYYY-MM>.md for an active project. Use when finishing a substantive dev session that touched code, design, or decisions whose reasoning would be lost between sessions; when the user says 'log this', 'record the session', '落盘一下', '写一条 dev-log'; or before reporting back at end of a session that ran red-team / refactor / multi-attacker / cross-session-reasoning work. Skip for trivial single-edit fixes."
---

# /dev-log — Append-only development journal

Sessions accumulate decisions, dead ends, and red-team findings that don't show up in the diff. This skill captures those for the next session — and for the human reviewing before commit.

Trigger phrases (treat as a request to run this skill):
- "log this", "record this session", "write a dev-log entry"
- "落盘一下", "写一条 dev-log", "记一笔"
- End of any session that ran red-team / refactor / multi-attacker work, or where reasoning would be lost on compaction

Also fire proactively at end-of-session, **only when the session actually produced things diff-invisible to a future reader**: rejected approaches with reasons, attacker findings that didn't all become commits, cross-cutting design choices, open follow-ups. Skip for sessions that were just typo fixes or single-file edits.

---

## What dev-log is (and isn't)

| | dev-log | commit message | CLAUDE.md | memory | EACN message |
|---|---|---|---|---|---|
| **Audience** | next dev session, human pre-commit reviewer | the world after release | every future agent | every future Claude session | other Roles in a project |
| **Records** | reasoning + dead ends + open Qs | the snapshot the user shipped | stable architecture | stable user/project facts | cross-Role coordination |
| **Lifetime** | append-only, never rewritten | immutable once pushed | edited as architecture changes | edited as facts change | per-task |
| **Visible to Roles?** | NO — dev-log is dev-only | yes (via git log) | yes | no | yes |

dev-log is **not** a contract surface — `mos audit` does not gate on it. It is **not** in any Role's system prompt. It is **not** read by EACN. It exists for the human + the next dev session, full stop.

---

## File layout

```
MinionsOS/
└── dev-log/
    └── YYYY-MM.md       # one file per month, append-only
```

One file per month keeps each file scannable. New months start a new file (no automatic rollover — just write into the right one). The file's first entry creates the file.

---

## Entry shape

Each entry is a level-2 heading + 5–7 short blocks. Aim for **15–30 lines per entry**. If it's longer, you're writing too much.

```markdown
## YYYY-MM-DD HH:MM — <one-line topic>

**Trigger**: <what the user asked, in one sentence>

**Diff-invisible findings**:
- <thing the next session needs to know that the diff won't say>
- <e.g. "approach X was rejected because Y; if you're tempted, see attacker-runtime report">

**Decisions**:
- <decision + the reasoning that won>
- <e.g. "ethics keeps codex; documented as exception in audit.py:_CODEX_INTENTIONAL_RESTRICTED_ROLES">

**Open** (← future-session prompts):
- <thing this session deferred, with enough hint to resume>

**Evidence**:
- <pointer to subagent transcripts, files, audit JSON, etc.>
- <e.g. "attacker reports archived in this session's transcript; main context only kept summaries">
```

Optional blocks if relevant:
- **Rejected approaches** — what was tried and why it didn't fit
- **Pivot** — when the session changed direction mid-flight, why

Skip blocks that don't apply. A one-liner under each used header beats padding.

---

## Procedure

### Step 1 — Decide whether to write

Ask: *"If a fresh session opened the diff right now, would they understand WHY?"*

- Yes → skip dev-log; the diff + commit message are enough.
- No → write an entry.

Common WHY-not-in-diff signals: red-team / multi-attacker work, rejected approaches, cross-cutting design choices, deferred work, surprising findings about user preferences or system behavior.

### Step 2 — Resolve the file path

Today's date determines the file. Use absolute date format `YYYY-MM` for the filename and `YYYY-MM-DD HH:MM` for the entry header.

```bash
ls /Users/mjm/MinionsOS/dev-log/
```

If `<YYYY-MM>.md` exists → append. If not → create with this header:

```markdown
# Dev log — YYYY-MM

Append-only journal of MinionsOS development sessions. Conventions in
`~/.claude/skills/dev-log/SKILL.md`.
```

### Step 3 — Compose the entry

Follow the entry shape above. Keep blocks short. Cite evidence by file path / subagent transcript ID / commit SHA, not by paraphrase.

If you delegated work to subagents in this session, **mention which findings only exist in those transcripts** — main-context summaries lose detail, and the next session won't see the original report.

### Step 4 — Append, never rewrite

Use the `Read` tool on the full file first — `Edit` will refuse with "File must be read first" otherwise. Do **not** substitute `tail -5` / `head` / `cat` via Bash; those don't register the file as read in the session, so `Edit` will still fail. Then `Edit` with the file's last non-empty line as the unique `old_string` anchor and `<that line>\n\n<new entry>` as `new_string`.

Never edit a previous entry — if a past entry turns out wrong, write a new entry referencing it ("entry of 2026-05-19 was incorrect on X — see attacker-runtime report; correct understanding is Y"). Append-only is the discipline that makes dev-log honest.

### Step 5 — Report

One sentence: "logged: dev-log/YYYY-MM.md, entry `<topic>`."

---

## Pitfalls

- **Don't summarize the diff.** The diff is in git. dev-log records what's *not* in the diff: reasoning, alternatives, dead ends, deferred work.
- **Don't write dev-log for trivial sessions.** A one-line typo fix doesn't need an entry. Use judgement; "would the next session benefit?" is the test.
- **Don't put dev-log content into any Role-facing surface.** Not in `roles/*/SYSTEM.md`, not in `roles/SYSTEM.md`, not in `_BOUNDARY_TEXT`, not in EACN messages. dev-log is invisible to the autonomous research loop by design — keep it that way.
- **Don't gate `mos audit` on dev-log.** dev-log is a journal, not a contract. Adding "must have a dev-log entry for this commit" turns it into bureaucracy.
- **Don't rewrite past entries.** Append-only or it stops being a faithful record. Corrections go in new entries that link back.
- **Don't make entries 100 lines long.** If you have that much to say, the session was probably two or three logical sessions; split into separate entries with separate timestamps.
- **Don't drop subagent context silently.** If you spawned attacker / explorer / reviewer subagents and only their summaries entered main context, mention that explicitly in **Evidence** so the next session knows to re-spawn rather than read the (lossy) summary.

---

## Related memory

- [[reference_skill_evaluator]] — separate concern: evaluates whether a skill works behaviorally; has nothing to do with this dev journal.
- [[feedback_minionsos_push_workflow]] — push workflow is the *deliberate release* event; dev-log captures what happens *between* pushes.
