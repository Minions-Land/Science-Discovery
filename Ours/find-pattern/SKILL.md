---
name: find-pattern
description: "Find the right Claude Code design pattern for a specific agent engineering problem"
---

# /find-pattern — Pattern Finder

Usage: `/find-pattern <problem description>`

Example: `/find-pattern How do I let multiple agents share findings without passing huge text through prompts?`

---

## Your Role

Map the user's problem to one of Claude Code's 12 battle-tested design patterns. Be fast and precise — they just need to know WHAT to use and WHERE to find it.

---

## Step 1 — Read the patterns catalog

Read `/Users/mjm/Claude Code/_reference/en/09-PATTERNS.md`

---

## Step 2 — Output format

```
## Pattern Match: [Pattern Number] — [Pattern Name]

**Problem it solves**: [one sentence]

**How Claude Code does it**: [two sentences, concrete]

**The key insight**: [the non-obvious thing that makes it work]

**Read this next**: `/Users/mjm/Claude Code/_reference/[relevant file]`

**Quick start**: [the first concrete thing to implement]
```

If multiple patterns apply, list the PRIMARY one first, then briefly mention secondaries.

---

## Pattern→File Map

| Pattern | Toolkit Template | Reference Doc |
|---------|-----------------|---------------|
| #1 Tool Interface + Defaults | `toolkit/tool-template.md` | `en/01-TOOL-SYSTEM.md` |
| #2 Context Forking | `toolkit/agent-spawning-template.md` | `en/02-MULTI-AGENT.md` |
| #3 Fan-Out → Synthesize → Implement → Verify | `toolkit/coordinator-workflow-template.md` | `en/02-MULTI-AGENT.md` |
| #4 Two-Stage Validation | `toolkit/permission-system-template.md` | `en/05-COMMAND-SYSTEM.md` |
| #5 AsyncLocalStorage Isolation | `toolkit/task-system-template.md` | `en/03-TASK-SYSTEM.md` |
| #6 Progressive Result Delivery | `toolkit/tool-template.md` | `en/01-TOOL-SYSTEM.md` |
| #7 Deferred Tool Loading | `toolkit/tool-template.md` | `en/01-TOOL-SYSTEM.md` |
| #8 XML Async Notifications | `toolkit/agent-spawning-template.md` | `en/02-MULTI-AGENT.md` |
| #9 Shared Work Queue | `toolkit/swarm-team-template.md` | `en/02-MULTI-AGENT.md` |
| #10 Multi-Source Command Registry | `en/05-COMMAND-SYSTEM.md` | `tutorial/07-command-plugin-system.md` |
| #11 GC-Free Packed Buffers | `en/06-INK-UI.md` | `tutorial/06-terminal-ui.md` |
| #12 Coordinator + Scratchpad | `toolkit/coordinator-workflow-template.md` | `en/02-MULTI-AGENT.md` |

All files are under: `/Users/mjm/Claude Code/_reference/`
