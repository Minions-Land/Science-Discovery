---
name: minionsos-push
description: "End-to-end review-and-push for MinionsOS to https://github.com/Minions-Land/MinionsOS. Invoke when the user asks to push, commit-and-push, do a PR, ship a release, or update the GitHub repo for /Users/mjm/MinionsOS. Handles code review, SSH-first transport with HTTPS fallback for the throttled github.com link on this host, and the user's required 'from V<x>' + bulleted change-list commit-message shape."
---

# /minionsos-push — Review + push MinionsOS to GitHub

The user is the sole version manager for MinionsOS. Every PR commit and `git push` for that repo goes through Claude. This skill is the canonical procedure: review → commit (if needed) → push → report.

Trigger phrases (treat as a request to run this skill):
- "push to GitHub", "git push", "push it", "ship this", "release this", "do a PR"
- Anything similar pointing at `/Users/mjm/MinionsOS` or the `Minions-Land/MinionsOS` remote

If the request is ambiguous about whether to *only* push existing commits or *also* compose a new commit, check `git status` first — let the repo state guide the question you ask back.

---

## Repo facts (load-bearing, do not guess)

- Working dir: `/Users/mjm/MinionsOS`
- Remote: `git@github.com:Minions-Land/MinionsOS.git` (SSH) — this is the **current default**. SSH identity on this host: `Hi PoorOtterBob!` (verified with `ssh -T git@github.com`).
- Default branch: `main` on both sides. The user pushes directly to `main` — he treats each push as a deliberate release event, not a routine sync.
- Test command: `MINIONS_FAKE_CLAUDE=1 uv run pytest tests/unit/ -q` (≈20 s, expect 400+ passing).
- Lint: `uv run ruff check minions/` and `uv run ruff format --check minions/`.
- Contract audit: `uv run mos audit` (≈0.1 s, 13 invariants across whitelist / publish policy / MCP registry / CLAUDE.md table / FIXED_ROLES). Errors must be zero; warnings get evaluated case by case in Step 2.

---

## Step 1 — Snapshot the repo state

Run these in parallel — they're independent:

```bash
git -C /Users/mjm/MinionsOS status
git -C /Users/mjm/MinionsOS remote -v
git -C /Users/mjm/MinionsOS log origin/main..HEAD --oneline
cd /Users/mjm/MinionsOS && uv run mos audit --json
```

Determine four things, then act:

1. **Unpushed commits** (`log origin/main..HEAD`) — what this push will publish.
2. **Uncommitted work** (`status`) — if non-empty, see Step 3 (need version label + commit shape from the user).
3. **Remote scheme** (`remote -v`) — if `origin` is HTTPS, flip to SSH:
   ```bash
   git -C /Users/mjm/MinionsOS remote set-url origin git@github.com:Minions-Land/MinionsOS.git
   ```
4. **Contract surface** (`mos audit`). Decision rule:

   | severity in JSON | action |
   |---|---|
   | any `error` | STOP. Surface the error and ask the user before doing anything else. The push would publish a broken contract. |
   | new `warning` (not present on `origin/main`) | Forward to the Step 2 reviewer with the audit JSON; let the reviewer judge per-commit attribution. |
   | pre-existing `warning` / `info` | Mention in the Step 6 report, do not gate. |

Edge case: nothing unpushed, nothing uncommitted, audit clean → tell the user `main` is already in sync and stop.

---

## Step 2 — Code review of unpushed commits

Delegate to a `subagent_type: general-purpose` so the main context stays clean and the read is independent. Hand the subagent:

- The commit list (`git log origin/main..HEAD`).
- The `mos audit --json` output from Step 1.
- The expected output shape (below).

Ask the subagent to check:

- Secrets and credentials.
- `MINIONS_FAKE_CLAUDE=1 uv run pytest tests/unit/ -q` (expect 400+ green).
- `uv run ruff check minions/` and `uv run ruff format --check minions/`.
- Large or binary files, `.DS_Store`, `.env`, `node_modules`, hard-coded `/Users/mjm/...` paths.
- **Audit-delta**: which warnings in the JSON are *new* relative to `origin/main`, and which commit introduced each.

Don't re-do the contract cross-checks (whitelist ↔ CLAUDE.md table, publish policy ↔ write boundaries, etc.) — `mos audit` already covers those.

Required output shape:

```
VERDICT: APPROVED-FOR-PUSH | NEEDS-CHANGES | NEEDS-DISCUSSION
Blockers: …
Audit-delta: …          # warnings introduced by this push set, attributed per commit
Non-blocking: …         # cosmetic drift, pre-existing audit warnings, etc.
Secrets scan: …
Large files: …
```

**Decision rule:**

| verdict | next move |
|---|---|
| APPROVED-FOR-PUSH | proceed to Step 3 / 4. |
| NEEDS-DISCUSSION | surface the blockers to the user; do not push without confirmation. |
| NEEDS-CHANGES | stop, report, ask. |

Step 2 and Step 3 are independent — run prep for both in parallel.

---

## Step 3 — Commit any uncommitted work (if Step 1 found dirty tree)

Two pieces of information are required from the user, and both are user-only judgement calls — ask via `AskUserQuestion`, do not guess:

1. **Version label** — what version anchor does this commit start from? Options usually look like:
   - "from V5" (continuation polish under the same major version)
   - "from V5.1" (small bump to mark a meaningful sub-release)
   - "Bump to V6" (this change is itself a new major)
   - Or whatever the user names.
2. **Commit shape** — single commit covering all changes, or split into logical commits? Single is usually fine for tightly related polish; split when there are genuinely separable threads (e.g., new feature + unrelated bugfix).

**Commit message shape (the user's stated rule):**

```
v<version>: <one-line headline>

From V<source-version> (<source-sha-short>). <One-paragraph framing.>

1. <Thread one headline.>
   <Specific files / dirs / behaviour, not just a summary.>
   - <bullet>
   - <bullet>

2. <Thread two headline.>
   ...

Verification: <test count>/<test count> unit tests pass; ruff check clean.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

Required elements:
- **State the source version** (e.g. "From V5 (39d68e9)") in the body. This is the user's explicit convention — every commit message must name where the update started from.
- **Enumerate specific changes** — file groups, behavioural deltas, not a one-liner.
- **Verification line** with concrete test count and ruff status.

Stage and commit:
```bash
git -C /Users/mjm/MinionsOS add -A
git -C /Users/mjm/MinionsOS commit -m "<message>"
```

Watch for `git status` after the add: confirm the staged set matches what you expected (renames, new files, deletions). Don't `add -A` blindly if there's untracked junk in the tree — investigate first.

---

## Step 4 — Push

**Primary path (SSH, default):**

```bash
git -C /Users/mjm/MinionsOS push origin main
```

This should be effectively instant on a working SSH path. Give the Bash tool a generous timeout anyway (`timeout: 300000` = 5 min).

**Expected success output:** `<oldsha>..<newsha>  main -> main`. Capture this — it goes in the report to the user.

---

## Step 5 — If SSH fails, HTTPS fallback recipe

Network condition on this host (observed 2026-05-14): `github.com` HTTPS is throttled (curl error 28 on 10 s probes, ~250 KB/s peak), but `api.github.com` is fine (~1 s). Default `git push` over HTTPS can stall.

Recipe that worked once for the v5 bundle push (`39d68e9`):

```bash
# 1. Flip remote back to HTTPS
git -C /Users/mjm/MinionsOS remote set-url origin https://github.com/Minions-Land/MinionsOS

# 2. Set local HTTP resilience config (persists in .git/config)
git -C /Users/mjm/MinionsOS config http.postBuffer 524288000      # 500MB buffer for large packs
git -C /Users/mjm/MinionsOS config http.version HTTP/1.1          # HTTP/2 multiplexing hurts on throttled links
git -C /Users/mjm/MinionsOS config http.lowSpeedLimit 1000        # only abort if <1KB/s
git -C /Users/mjm/MinionsOS config http.lowSpeedTime 300          # ...sustained for 5 minutes

# 3. Push with a 10-minute timeout
git -C /Users/mjm/MinionsOS push origin main    # Bash tool: timeout: 600000
```

If that still stalls:
- Retry the push 1–2 times — TLS handshake variance often clears on a fresh connection.
- **Re-flip to SSH** and try again: `git remote set-url origin git@github.com:Minions-Land/MinionsOS.git`. SSH is currently the default precisely because HTTPS is unreliable on this host.
- **GitHub CLI:** `gh auth status` then `gh repo sync` — different token path; occasionally works when raw `git push` hangs.
- **Port-443 SSH** (only if port 22 itself is blocked, which is rare on this host): `git@ssh.github.com:Minions-Land/MinionsOS.git`.

Do **not** use `--force` or `--no-verify` as a shortcut. If a non-fast-forward happens, fetch and investigate — the remote may have moved.

---

## Step 6 — Report back

One concise message:

- The `<oldsha>..<newsha>  main -> main` line from `git push`.
- Review verdict and what got reviewed.
- Commit version anchor (e.g. "v5.1, from V5").
- **Audit posture**: `errors=0, warnings=N, info=M`; list any *new* warnings the user explicitly waved through.
- Non-blocking suggestions you noted but didn't gate on.
- Anything unusual (network retries, HTTPS fallback, etc.).

End-of-turn summary: one or two sentences. What got pushed, and the SHA.

---

## Pitfalls

- **Don't auto-push without an explicit request.** The user being the version manager means he asks for each push; pre-authorisation is for the *procedure* (review → push), not for unilateral pushes.
- **Don't skip the review step**, even for "small" changes. The user explicitly wants Claude as the gate.
- **Don't wave through `mos audit` errors.** An audit error means a contract surface (whitelist, publish policy, MCP registry) is provably broken. Warnings can be a judgement call; errors are not. If an error appears, fix it (or have Coder fix it via a system-maintenance task) before push, do not "carry it forward."
- **Don't compose a vague one-line commit message.** Every commit needs the "from V<x>" anchor and enumerated changes. If you're rushed, ask the user for the version label rather than guessing.
- **Don't `git add -A` blindly.** Check `git status` first — the user may have untracked files that are *not* meant for this push.
- **Don't switch the remote without telling the user.** SSH is current default; if you fall back to HTTPS, mention it.
- **Don't paper over a push failure.** If both SSH and HTTPS fail, report the failure with the actual error message and stop. Don't try `--force`, don't delete and re-add anything.

---

## Related memory

- [[feedback_minionsos_push_workflow]] — the workflow rule itself (review-first, version-anchored commit messages).
- [[reference_minionsos_github_push]] — the network observation and recipe details; this skill supersedes that reference as the operational entry point.
