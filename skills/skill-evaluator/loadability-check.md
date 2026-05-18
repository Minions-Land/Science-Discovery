# Loadability Check

Can this skill enter the agent runtime?

## When to use

- First time evaluating any skill.
- After editing frontmatter or renaming files.
- Batch-checking a library for broken skills.

## Procedure

Parse the skill's `SKILL.md` and verify:

1. **Frontmatter parses.** `---` delimiters present, YAML content valid.
2. **`name` exists.** Non-empty string.
3. **`description` exists.** Non-empty string, ≤1024 characters.
4. **Referenced files exist.** Every path mentioned in the body (`references/*.md`, `bin/*.sh`, `agents/*.md`) resolves on disk.
5. **Symlinks resolve.** If the skill is symlinked into an agent directory, the target exists.

Any failure on items 1–3 is a **blocker** — the skill cannot load regardless of quality.

## Also flag (advisory)

- Security indicators: hardcoded secrets, `curl|sh` patterns, `rm -rf /`.
- Staleness: mtime > 180 days combined with references to deprecated tools or old model names.
- Backup remnants: `.backup.`, `.disabled-`, `.old` siblings in the same directory.

## Output

```
skill-name: PASS | BLOCKER (reason) | ADVISORY (reason)
```

One line per skill. That's it. Don't over-produce.

## Shell shortcut

If `skill-scan.sh` is installed:
```bash
bash ~/.agents/skills/skill-hygiene/bin/skill-scan.sh --json
```
Otherwise, read the file and check manually.
