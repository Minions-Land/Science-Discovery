---
name: tool-design
description: "Design a new tool using Claude Code's buildTool pattern — produces a complete tool spec"
---

# /tool-design — Tool Designer

Usage: `/tool-design <what the tool should do>`

Example: `/tool-design A tool that queries a PostgreSQL database and returns results`

---

## Your Role

Design a complete tool using Claude Code's `buildTool()` pattern. Read the template, then produce a filled-in spec the user can implement immediately.

---

## Step 1 — Read the template

Read `/Users/mjm/Claude Code/_reference/toolkit/tool-template.md`

Also read `/Users/mjm/Claude Code/_reference/en/01-TOOL-SYSTEM.md` for the full Tool interface.

---

## Step 2 — Fill in the tool spec

Produce a complete tool design in this format:

````
## Tool Design: [ToolName]

### Overview
- **Name**: `[ToolName]`  
- **Purpose**: [one sentence]
- **Is read-only?**: yes/no — [reason]
- **Is destructive?**: yes/no — [reason]
- **Is concurrency-safe?**: yes/no — [reason]
- **Max result size**: [e.g., 50_000 chars] — [reason]
- **Defer loading?**: yes/no — [reason]

---

### Input Schema (Zod)

```typescript
z.object({
  // required params
  [param]: z.string().describe("[description]"),
  // optional params  
  [param]: z.number().optional().describe("[description]"),
})
```

---

### Two-Stage Validation

**validateInput** — logic checks:
- [ ] [check 1, e.g., "connection string is valid format"]
- [ ] [check 2]

**checkPermissions** — authorization:
- Behavior: `'allow'` / `'ask'` / always-ask
- Rule pattern: `[ToolName]([key param] pattern)`
- [reason why this permission level is appropriate]

---

### call() Implementation Plan

```
1. [First step, e.g., "Create database connection"]
2. [Second step]
3. [Third step]
4. Format output as: [string/JSON/table]
5. Return { data: [type] }
```

Edge cases to handle:
- [edge case 1]
- [edge case 2]

---

### Progress Reporting

```typescript
// During execution, report:
onProgress({ toolUseID, data: { type: '[tool-name]', stage: '...' } })
```

Stages: [list stages if long-running, or "N/A — fast operation"]

---

### Rendering

**renderToolUseMessage**: Show `[param] — [brief description]`  
**renderToolResultMessage**: Show [how to display the result]  
**isResultTruncated**: [yes/no, and why]

---

### Security Considerations

- [Any special security concern]
- [Path validation needed? Input sanitization?]
- [Should this be sandboxed?]

---

### searchHint

`"[3-10 keywords for ToolSearch discovery]"`
````

---

## Key decisions to make explicit

For every tool, document WHY:
- `isReadOnly`: matters for plan mode (read-only tools allowed, write tools blocked)
- `isConcurrencySafe`: if false, this tool will serialize with other non-concurrent tools
- `maxResultSizeChars`: if result exceeds this, it auto-persists to disk — choose based on typical output size
- `shouldDefer`: set true if this tool is used less than 20% of the time — saves prompt tokens
