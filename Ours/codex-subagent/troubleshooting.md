---
name: codex-troubleshooting
description: "Failure mode handbook for the codex MCP tool, consumed by the Haiku wrapper relay in /codex Step 3. Each entry pairs a detection rule with either a single safe AUTO-FIX or NONE (escalate). The Haiku wrapper applies AT MOST one auto-fix retry per failure, and AT MOST 2 retries total per dispatch."
---

# codex-subagent troubleshooting handbook

This file is read by the Haiku relay inside `/codex` Step 3 when the `codex` MCP tool returns an error, hangs, or finishes with a non-success status. It exists so that the relay can apply narrow, well-understood environment fixes without inventing strategies on its own.

**Hard rules for the relay (do not violate even if a fix looks tempting):**

- At most **2 retries** in total per `/codex` dispatch (so up to 3 codex invocations including the original call).
- A retry is allowed **only** when the matching entry below has an `AUTO-FIX:` line. Entries with `AUTO-FIX: NONE` are terminal — escalate to main immediately.
- An auto-fix may **only** change the args listed in the entry. Do not change the `task` text, do not change `sandbox` from `danger-full-access` to anything weaker, do not change `reasoning_effort`, do not edit `cwd` to a different directory.
- If two entries both match, prefer the more specific one (string match beats regex; CODEX_UNAVAILABLE / CODEX_ERROR prefixes always win because they come from the MCP wrapper itself, not from codex).
- After all retries are exhausted, emit the structured failure record described in `SKILL.md` Step 3. Do not include recommendations — main agent decides.

---

## Detection inputs

The relay sees these fields from the codex MCP `structuredContent`:

- `status`: `success` | `error` | `timeout`
- `exit_code`: number, 0 means success
- `message`: codex's final message OR a `CODEX_UNAVAILABLE: …` / `CODEX_ERROR: …` envelope from the MCP wrapper
- `files_changed`: array
- `commands_run`: array of `{command, exit_code}`

Match against `message` (case-insensitive substring unless noted). The first matching entry wins.

---

## Entry 1 — `codex_cli_missing`

**DETECT:** `message` starts with `CODEX_UNAVAILABLE:` OR contains `codex CLI not found` OR contains `Failed to spawn codex: ENOENT`.

**DIAGNOSIS:** The `codex` CLI is not on PATH for the MCP server process. This is an installer problem (`npm i -g @openai/codex` was never run, or the global node bin is not on PATH for the user that started Claude Code).

**AUTO-FIX:** NONE. The MCP server cannot install codex from inside a sandboxed subagent.

**STATUS to report:** `codex_unavailable` with `ROOT_CAUSE: codex CLI not on PATH for MCP server`.

---

## Entry 2 — `codex_not_authenticated`

**DETECT:** `message` contains any of: `auth.json`, `not authenticated`, `please run codex login`, `OPENAI_API_KEY`, `401 Unauthorized`, `invalid_api_key`.

**DIAGNOSIS:** Codex CLI is installed but cannot reach the OpenAI API because no credential is configured. Either `~/.codex/auth.json` is missing, the env var `OPENAI_API_KEY` is unset, or the stored token has expired and `codex login` needs to be re-run.

**AUTO-FIX:** NONE. Credential setup is interactive and outside the relay's authority.

**STATUS to report:** `codex_unavailable` with `ROOT_CAUSE: codex auth missing or expired`.

---

## Entry 3 — `cwd_not_git_repo`

**DETECT:** `message` contains `not a git repository` OR `not inside a git work tree` OR `git repo check` (and `skip_git_check` was NOT already set in the failed call).

**DIAGNOSIS:** Codex refused to run because `cwd` is not inside a git repo and `skip_git_check` was not set. This is a known recoverable case — codex's git check exists for safety in `danger-full-access` mode, but for analysis tasks in `/tmp`, scratch dirs, or freshly seeded folders we explicitly want to bypass it.

**AUTO-FIX:** Retry the same call with `skip_git_check: true` added. Keep `task`, `cwd`, `sandbox`, `reasoning_effort`, `timeout_seconds` identical.

**STATUS to report (if retry also fails):** `codex_error` with `ROOT_CAUSE: cwd not a git repo, skip_git_check did not resolve`.

---

## Entry 4 — `cwd_invalid_path`

**DETECT:** `message` contains `No such file or directory` AND mentions a path AND `Failed to spawn codex` OR exit_code != 0 with `chdir` / `ENOENT.*cwd` patterns.

**DIAGNOSIS:** The `cwd` argument points to a directory that does not exist or is not accessible. Almost always a typo or stale path passed by the caller.

**AUTO-FIX:** NONE. The relay does not have authority to invent a substitute `cwd`.

**STATUS to report:** `codex_error` with `ROOT_CAUSE: cwd does not exist or is not accessible`.

---

## Entry 5 — `permission_denied`

**DETECT:** `message` contains `EACCES` OR `Permission denied` OR `read-only file system` OR `sandbox denied`. This may show up either at spawn time or inside a codex command-execution event surfaced in the final message.

**DIAGNOSIS:** Codex (or a command codex tried to run) hit a filesystem or sandbox permission wall. Could be: a write inside a read-only mount, a path codex was not granted access to, or an OS-level permission on `cwd`.

**AUTO-FIX:** NONE. Changing `sandbox` to a weaker level would bypass an intentional safety boundary; adding `add_dirs` requires knowing what path codex was trying to reach. Both are decisions for the main agent.

**STATUS to report:** `codex_error` with `ROOT_CAUSE: filesystem or sandbox permission denial`.

---

## Entry 6 — `timeout_or_hang`

**DETECT:** any of:
- `status == "timeout"`,
- `exit_code` is 143 or 137 or null/undefined and `commands_run` is non-empty (codex was actively working when killed),
- `message` is empty or just stderr fragments AND elapsed wall time was within 5 % of the requested `timeout_seconds`.

**DIAGNOSIS:** Codex either hit the timeout or was hung inside a non-terminating reasoning/tool loop. The MCP wrapper sent SIGTERM, then SIGKILL after 5 s.

**AUTO-FIX:** NONE. Re-running with a longer timeout is a policy decision (cost, latency budget) the relay must not make. The main agent may choose to re-dispatch with a larger `timeout_seconds` or split the task.

**STATUS to report:** `codex_timeout` with `ROOT_CAUSE: timeout or hang at <elapsed>s`.

---

## Entry 7 — `api_rate_limit`

**DETECT:** `message` contains any of: `rate limit`, `429`, `Too Many Requests`, `RPM`, `TPM`, `please retry after`.

**DIAGNOSIS:** OpenAI API throttled the request. This is transient but with a backoff window the relay does not know.

**AUTO-FIX:** NONE. Retrying immediately would hit the same wall; sleeping inside a subagent burns wall-clock budget for the main session.

**STATUS to report:** `codex_error` with `ROOT_CAUSE: API rate-limited, suggested by codex message`.

---

## Entry 8 — `api_quota_exhausted`

**DETECT:** `message` contains any of: `quota`, `billing`, `insufficient_quota`, `exceeded your current quota`, `payment required`, `402`.

**DIAGNOSIS:** OpenAI account is out of credit, the org's budget is exhausted, or a billing issue is blocking the account.

**AUTO-FIX:** NONE. The relay cannot top up an account.

**STATUS to report:** `codex_unavailable` with `ROOT_CAUSE: API quota / billing block`.

---

## Entry 9 — `context_length_exceeded`

**DETECT:** `message` contains any of: `context length`, `context_length_exceeded`, `maximum context length`, `tokens > limit`, `request too large`.

**DIAGNOSIS:** The task prompt plus codex's accumulated tool output overflowed the model context window. This usually means the task is too large to attempt as one codex call and should be split.

**AUTO-FIX:** NONE. Splitting the task is a Step 4 (parallel splitting) decision for the main agent, not the relay.

**STATUS to report:** `codex_error` with `ROOT_CAUSE: context length exceeded — task likely needs splitting`.

---

## Entry 10 — `transient_5xx`

**DETECT:** `message` contains any of: `500 Internal`, `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout`, `upstream connect error`. Must NOT also match Entry 7 (rate limit) or Entry 8 (quota).

**DIAGNOSIS:** Transient upstream failure on the OpenAI side. These usually clear within seconds and a single retry has a high success rate.

**AUTO-FIX:** Retry the same call **once** with identical args. No backoff.

**STATUS to report (if retry also fails):** `codex_error` with `ROOT_CAUSE: persistent upstream 5xx after one retry`.

---

## Entry 11 — `unknown_codex_failure`

**DETECT:** none of the above match, but `status != "success"` or `exit_code != 0`.

**DIAGNOSIS:** Codex finished with a non-success status that this handbook does not yet recognise.

**AUTO-FIX:** NONE — do not guess.

**STATUS to report:** `codex_error` with `ROOT_CAUSE: unknown — see ATTEMPTS for raw message excerpt`.

---

## Adding a new entry

When a new failure mode shows up in practice:

1. Capture a real `message` excerpt that triggered it.
2. Decide whether a **safe, narrow** auto-fix exists. The bar is high: "safe" means it cannot change task semantics, weaken safety, or hide a config bug from the user.
3. Add an entry above with `DETECT`, `DIAGNOSIS`, `AUTO-FIX`, `STATUS to report`. Place it before Entry 11 (`unknown_codex_failure`) which is always last.
4. Mirror the change to the other copy of this file (`~/.claude/skills/codex/troubleshooting.md` and `MinionsOS/mcp-servers/codex-subagent/skills/codex/troubleshooting.md` — they must stay byte-identical).
