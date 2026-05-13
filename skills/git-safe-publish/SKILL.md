---
name: git-safe-publish
description: Use when the user asks to commit, push, save current work to GitHub, preserve repository changes, or publish repository edits safely without overwriting other collaborators' work.
---

# Git Safe Publish

Use this workflow when saving repository work to git and pushing it to the remote. The goal is fast publishing without accidentally staging unrelated changes or overwriting another agent's edits.

## Workflow

1. Inspect the repository state before staging:
   ```bash
   git status --short
   git branch --show-current
   git remote -v
   git diff --stat
   ```

2. Identify exactly which files belong to the user's requested change. If other files are modified, treat them as collaborator/user work unless the user explicitly asks to include them.

3. Review the target diff before staging:
   ```bash
   git diff -- path/to/file
   ```
   For generated or large files, use `git diff --stat` plus targeted text checks.

4. Run lightweight validation relevant to the changed files. Examples:
   ```bash
   python3 -m html.parser research-report.html
   python3 - <<'PY'
   from pathlib import Path
   import re
   s = Path("research-report.html").read_text()
   ids = set(re.findall(r'id="([^"]+)"', s))
   links = re.findall(r'href="#([^"]+)"', s)
   missing = [x for x in links if x not in ids]
   if missing:
       raise SystemExit(f"missing anchors: {missing}")
   print("anchors ok")
   PY
   ```

5. Stage only the intended files:
   ```bash
   git add path/to/file
   ```
   Avoid `git add .` when collaborators may be editing in parallel.

6. Commit with a short imperative message:
   ```bash
   git commit -m "Update research report"
   ```

7. Push the current branch:
   ```bash
   git push origin "$(git branch --show-current)"
   ```

8. Confirm the result:
   ```bash
   git status --short
   ```
   Report the commit hash and push range if available.

## Collaboration Rules

- Never run `git restore`, `git reset`, or broad cleanup to remove changes unless the user explicitly asks.
- If another agent has modified the same file, preserve those edits and apply only targeted follow-up changes.
- If the working tree contains unrelated files, either leave them unstaged or ask whether to include them.
- If push fails because the remote advanced, inspect with `git fetch` / `git status` before deciding whether to pull, rebase, or ask the user.
