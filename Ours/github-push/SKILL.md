---
name: github-push
description: "Generic, repo-agnostic git push to GitHub. Use when the user asks to push, commit-and-push, create a PR, ship a release, or update a GitHub repo. Inherits the host's known network constraints: SSH-first transport because github.com HTTPS is throttled on this host (curl 28 timeouts, ~250 KB/s peak); falls back to HTTPS with resilience config + 600s timeout. Skips the review/version-anchor steps that are MinionsOS-specific. For MinionsOS pushes specifically, use minionsos-push instead."
---

# /github-push — Generic GitHub push procedure

A reusable, low-latency push procedure for any local repo. Use this when the target is **not** MinionsOS (which has its own review-gated workflow at [[minionsos-push]]).

Trigger phrases:
- "push to GitHub", "git push", "ship this", "do a PR", "commit and push"
- Any phrasing pointing at a non-MinionsOS repo

If the user names the repo (e.g. "push MinionsCode") use that. If unclear, ask.

---

## Host network facts (load-bearing)

These were learned the hard way on this host (verified 2026-05-14, still current 2026-05-17):

- `github.com` HTTPS is throttled — `git push` over HTTPS regularly stalls or fails with curl 28 timeouts. Peak ~250 KB/s, sustained much less.
- `api.github.com` is fine (~1 s) — `gh` CLI commands generally work.
- SSH to `git@github.com` works reliably. Identity on this host: `Hi PoorOtterBob!` (verified with `ssh -T git@github.com`).
- A global `git config` rewrite is in place: `url."git@github.com:".insteadOf "https://github.com/"`. This makes SwiftPM and any tool that uses HTTPS GitHub URLs transparently fall through SSH.

**Implication:** SSH is always the first choice. HTTPS is the documented fallback only.

---

## Step 1 — Snapshot the repo

```bash
cd <repo-path>
git status
git remote -v
git log @{u}..HEAD --oneline 2>/dev/null || git log --oneline -5
```

Three things to determine:

1. **Does origin exist?** If not, this is first push — see Step 2.
2. **Is origin SSH?** If it shows `https://...`, flip it:
   ```bash
   git remote set-url origin git@github.com:<owner>/<repo>.git
   ```
3. **What's unpushed / uncommitted?** Decide whether you need to commit before pushing.

If there's nothing to push and nothing to commit, tell the user the branch is in sync and stop. Don't invent work.

---

## Step 2 — First-time push (no remote yet)

If the repo has no `origin` and the user wants to push to a new GitHub repo:

```bash
gh repo view <owner>/<repo> 2>&1
```

**If the repo doesn't exist**, ask the user before creating it (visibility, description). Then:

```bash
gh repo create <owner>/<repo> --public --source=. --remote=origin --push
```

The `--push` flag does the initial push for you using the gh-authenticated channel — often more reliable than raw `git push` on first push.

**If the repo exists but origin is missing locally:**

```bash
git remote add origin git@github.com:<owner>/<repo>.git
git branch -M main
git push -u origin main
```

---

## Step 3 — Stage and commit (if dirty)

If `git status` showed uncommitted changes the user wants in this push:

1. Inspect the diff to confirm scope: `git diff --stat` and `git diff` for hot files.
2. Watch for files that should NOT be committed: `.env`, `*.pem`, `id_rsa`, anything in `~/.ssh/`, `node_modules/`, `.DS_Store`, large binaries (>5 MB). Flag and ask before adding them.
3. Stage explicitly when possible:
   ```bash
   git add <specific-files>
   ```
   Only `git add -A` if the working tree is clean of junk.
4. Compose a concise commit message. For non-MinionsOS repos, the strict "from V<x>" anchor is **not** required. A clear conventional-commit-style message is enough. Use HEREDOC with a unique sentinel (not the literal token used here as documentation), preserving formatting.

If a pre-commit hook fails, **fix the underlying issue and create a new commit** — never `--amend` and never `--no-verify`.

---

## Step 4 — Push (SSH primary)

```bash
git push -u origin <branch>
```

Expected success line: `<oldsha>..<newsha>  <branch> -> <branch>` or `* [new branch] <branch> -> <branch>`. Capture this for the report.

Bash-tool timeout: `300000` (5 min). SSH push is normally <2 s; the buffer is for slow network days.

---

## Step 5 — HTTPS fallback (only if SSH fails)

If SSH hangs or fails, apply the resilience recipe before retrying:

```bash
git remote set-url origin https://github.com/<owner>/<repo>.git
git config http.postBuffer 524288000      # 500 MB pack buffer
git config http.version HTTP/1.1          # HTTP/2 multiplexing hurts on throttled links
git config http.lowSpeedLimit 1000        # only abort if <1 KB/s ...
git config http.lowSpeedTime 300          # ...sustained for 5 min

git push -u origin <branch>               # Bash-tool timeout: 600000 (10 min)
```

If still failing after 1–2 retries:

1. **Re-flip to SSH** and retry — TLS handshake variance often clears with a fresh connection.
2. **Try `gh repo sync`** — uses the gh API token, sometimes works when raw git push hangs.
3. **Port-443 SSH** as last resort (only if port 22 is blocked, rare on this host):
   ```bash
   git remote set-url origin git@ssh.github.com:<owner>/<repo>.git
   ```

Never `--force`. Never `--no-verify`. Never delete-and-readd the remote as a "shortcut".

---

## Step 6 — PR creation (optional)

If the user wants a PR (not a direct push to main), they're working on a feature branch. After push, use `gh pr create` with a HEREDOC body. Include a Summary section, a Test plan checklist, and a Generated-with-Claude-Code footer. Return the PR URL.

---

## Step 7 — Report

One concise message to the user:
- Repo + branch + the `<oldsha>..<newsha>` line
- New commits in this push (if any)
- Any non-blocking observations (untracked files you skipped, hooks that ran, fallback used)

End-of-turn summary: one or two sentences. What got pushed and where.

---

## Pitfalls

- **Don't auto-push without an explicit request.** Each push is a deliberate event.
- **Don't blanket `git add -A`** when there's untracked junk. Stage explicitly.
- **Don't switch transport silently.** If SSH→HTTPS fallback was used, name it in the report so the user knows the remote URL changed.
- **Don't `git push --force` to main/master.** If a non-fast-forward shows up, fetch and investigate.
- **Don't skip hooks.** Pre-commit + pre-push hooks exist for a reason; if they fail, fix the cause.
- **Don't expose secrets in commit messages or PR bodies.**

---

## Why this skill exists

Repeated push attempts on this host wasted minutes on HTTPS retries before SSH was confirmed as the working path. This skill captures:

1. SSH-first as the default (instant on this host).
2. The exact HTTPS resilience config that has worked when SSH was unavailable.
3. The `gh repo create --push` shortcut for first pushes.
4. The minimal commit-message shape for non-MinionsOS repos (no version anchor required).

Anything more elaborate than this — code review gating, version anchors, mandatory test runs — belongs in a repo-specific skill (see [[minionsos-push]]).
