---
name: github-fetch
description: "Read content from any GitHub repo without cloning the whole thing. Use when the user asks to look at, summarize, port, or copy material from a GitHub URL — a single file, a sub-tree, a folder of skills, an example. Inherits the host's network constraints (github.com HTTPS throttled, api.github.com fine, gh CLI authenticated as PoorOtterBob). Default path: gh api → base64 -d. Fallbacks: gh repo clone --depth=1 for whole repos; raw.githubusercontent.com curl when gh is unavailable."
---

# /github-fetch — Read GitHub content without cloning the world

A reusable read-only counterpart to [[github-push]]. Use when the target is "look at this URL", "pull these skills", "what does this repo do" — not "give me a working checkout I'll edit". For pushing, see [[github-push]] / [[minionsos-push]].

Trigger phrases:
- "look at github.com/...", "fetch this repo", "pull these skills"
- "what's in github.com/owner/repo", "summarize this folder", "copy these files"
- A pasted GitHub URL with no other instruction

---

## Host facts (load-bearing)

Verified 2026-05-19, consistent with [[github-push]]:

- `gh` CLI is installed at `/opt/homebrew/bin/gh` and is **already authenticated** as `PoorOtterBob` (token has full repo + read scopes). Run `gh auth status` to confirm before trusting it.
- `api.github.com` is reachable in ~1 s. `gh api ...` is the fast path.
- `github.com` HTTPS is throttled (~250 KB/s peak, curl 28 timeouts on bigger transfers). Avoid raw HTTPS clones for anything large.
- SSH to `git@github.com` works reliably (used for clones when needed).
- Agent-side `WebFetch` / `WebSearch` are typically blocked on this host; use the Bash tool with `gh` or `curl` instead.

**Implication:** prefer `gh api` for individual files / sub-trees; use `gh repo clone` (which goes over SSH thanks to the global `insteadOf` rewrite) only when you need the whole repo.

---

## Step 1 — Decide the scope

From the user's request, pick one:

| Scope | Use |
|---|---|
| Single file (1 path) | `gh api` + `base64 -d` |
| A folder / sub-tree (≤30 files) | tree listing + bulk fetch |
| Whole repo (you'll grep / build) | `gh repo clone --depth=1` |
| Just metadata (stars, license, default branch) | `gh api repos/<o>/<r>` |

If the user gave a `github.com/<owner>/<repo>/tree/<branch>/<path>` URL, parse it: that's `repos/<owner>/<repo>/contents/<path>?ref=<branch>`.

---

## Step 2 — Confirm reachability

```bash
gh auth status 2>&1 | head -5
gh api "repos/<owner>/<repo>" --jq '{name, default_branch, stargazers_count, license: .license.spdx_id, updated_at}'
```

If `gh auth status` says not logged in, fall through to the `curl raw.githubusercontent.com` fallback in Step 5.

---

## Step 3 — Single-file or small set fetch

Each `gh api .../contents/<path>` returns `{content: <base64>, ...}`; pipe through `base64 -d`:

```bash
mkdir -p /tmp/<repo-slug> && cd /tmp/<repo-slug>
gh api "repos/<owner>/<repo>/contents/<path>" --jq '.content' | base64 -d > <local-name>
```

For a handful of files, write a tiny `fetch.sh` with an array of paths and loop. Avoid stuffing many `gh api` calls into one inline `for` loop in the Bash tool — multi-line continuations sometimes get mangled by zsh and you'll see a wall of `command not found`.

---

## Step 4 — Sub-tree listing (when you don't know the file names)

```bash
gh api "repos/<owner>/<repo>/git/trees/<branch_or_sha>?recursive=1" \
  --jq '.tree[] | select(.path | startswith("<subdir>")) | "\(.type)\t\(.path)"'
```

This gives you a flat `blob` / `tree` listing with full paths. From there, build the fetch script in Step 3. The recursive tree call counts as one API request regardless of size.

---

## Step 5 — Whole repo (you need to grep / run / build)

```bash
gh repo clone <owner>/<repo> /tmp/<repo-slug> -- --depth=1
```

`gh repo clone` rewrites to SSH on this host, which dodges the HTTPS throttle. `--depth=1` keeps the transfer small. Use this when:

- The user is going to edit and push back (in which case proceed to [[github-push]]).
- You need to actually run code or tests.
- You'll be doing many greps and the API call count would be wasteful.

If `gh` is unavailable and only HTTPS works, this is where you'll hit the slow path — set the resilience config from [[github-push]] Step 5 first.

---

## Step 6 — Last-resort raw fetch (no gh)

```bash
curl -sSL --max-time 30 \
  "https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>" \
  -o <local-name>
```

`raw.githubusercontent.com` is a separate CDN and is generally not throttled the way `github.com` is. Works without auth for public repos, but you don't get rate-limit headers — easy to silently get truncated on long files. Verify with `wc -l` against expected size when you can.

---

## Step 7 — Rate limit awareness

```bash
gh api rate_limit --jq '.resources.core | {limit, remaining, reset}'
```

Authenticated `gh` gets 5000 req/h on the core REST API. The recursive tree call + N file fetches eats N+1 of that budget. If you're doing a 100+ file sweep, do the recursive tree once and prefer `gh repo clone` over per-file fetches.

---

## Step 8 — Report

When handing back to the user, include:

- Repo + branch + commit SHA (`gh api repos/<o>/<r>/commits/<branch> --jq '.sha[:7]'`)
- What was downloaded and where (`/tmp/<repo-slug>/...`)
- Any noteworthy repo metadata (license, last commit, stars) so they know if it's stale or restrictively licensed before you build on it

If the content is going to be summarized or copied into project material, flag the license explicitly — CC BY-NC, GPL, "no LICENSE file" all change downstream choices.

---

## Pitfalls

- **Don't `WebFetch` on `github.com`** — it's blocked or throttled on this host. Use `gh api` or `curl raw.githubusercontent.com`.
- **Don't paste long multi-file `for` loops with `gh api ... base64 -d` chains directly into the Bash tool.** zsh continuations have eaten them in this environment. Write a `fetch.sh` and run it.
- **Don't forget to `base64 -d`.** The `.content` field is always base64; raw it looks like garbage and you'll waste time "debugging" the file.
- **Don't full-clone a multi-GB repo without `--depth=1`** — HTTPS will time out and SSH will still take minutes.
- **Don't skip license check** when the next step is "copy this into our skill library" or "ship this in the report".
- **Don't trust the `~/.claude/skills/` install instructions in random repos** without reading the SKILL.md frontmatter first — slugs and triggers vary, and a bad install can shadow one of ours.

---

## When this skill fails — self-update protocol

This skill encodes one user's working path on one host. Network constraints, tool versions, auth state, and rate limits drift. **If a path documented here stops working, the skill itself is what's stale — fix the document, not just this run.**

When you, as the executing agent, hit a step that does not work:

1. **Diagnose, don't give up.** Probe what actually broke:
   ```bash
   gh auth status
   gh api rate_limit --jq '.resources.core'
   curl -v --max-time 10 https://api.github.com/zen
   curl -v --max-time 10 https://github.com/ 2>&1 | head -20
   ```
   Identify the failing assumption: auth dropped, scope missing, rate limit hit, throttle worse than recorded, IP blocked, DNS issue, etc.
2. **Find the next working path.** Walk the fallback ladder (Steps 3 → 5 → 6 in this file), or invent a new rung. Capture the **exact command line** that finally returned the bytes.
3. **Patch THIS skill — both copies.** Edit:
   - `~/.claude/skills/github-fetch/SKILL.md` (user-global, used by Claude Code root sessions)
   - `/Users/mjm/MinionsOS/minions/roles/common/skills/github-fetch.md` (MinionsOS common layer, used by every Role)

   Add the new path as either a numbered rung in the fallback ladder, a new pitfall, or an updated "Host facts" line. Date-stamp the change (`verified 2026-MM-DD`). Keep the two files structurally aligned so a future Role on the MinionsOS side and a future root session both see the same fix.
4. **Tell the user.** One line in the report: "github-fetch updated: `<one-line diff summary>`" so the change can be audited and `git`-committed. Don't silently amend.

Treat this skill as the **cumulative log of how to get bytes off GitHub from this host as of the latest update**, not a fixed protocol. Every failure that took >2 minutes to work around is worth writing down.

## Why this skill exists

Pulling `lavinigam-gcp/build-with-adk/adk-skill-design-patterns` on 2026-05-19 went the long way: agent-side `WebFetch` was blocked, then a multi-line `gh api ... | base64 -d` `for` loop was eaten by the zsh interpreter and printed `command not found` for every iteration. The recipe that finally worked — `gh auth status` first, recursive tree once, `fetch.sh` with a path array — is captured here so the next session lands on it immediately instead of re-deriving. The self-update protocol above ensures the next surprise gets the same treatment.
