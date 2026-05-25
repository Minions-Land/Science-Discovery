---
name: multi-agent-workflow
description: "Design a multi-agent workflow using Claude Code's coordinator/swarm patterns"
---

# /multi-agent-workflow — Multi-Agent Workflow Designer

Usage: `/multi-agent-workflow <describe the complex task you need agents to accomplish>`

Example: `/multi-agent-workflow I need to analyze a large codebase, find all security vulnerabilities, and generate a fix for each one`

---

## Your Role

Design a complete multi-agent workflow using Claude Code's proven orchestration patterns. You will select the right coordination model, define each agent's role, and specify how they communicate.

---

## Step 1 — Read the reference material

Read these files (in order):
1. `/Users/mjm/Claude Code/_reference/toolkit/coordinator-workflow-template.md`
2. `/Users/mjm/Claude Code/_reference/toolkit/swarm-team-template.md`
3. `/Users/mjm/Claude Code/_reference/toolkit/agent-spawning-template.md`
4. `/Users/mjm/Claude Code/_reference/en/02-MULTI-AGENT.md` (sections 3-5)

---

## Step 2 — Choose a coordination model

**Model A: Coordinator + Workers (Sequential phases)**
- Best when: task has clear phases (research → synthesize → implement → verify)
- Uses: `coordinatorMode.ts` pattern, fan-out research, fresh-agent verification
- Template: `coordinator-workflow-template.md`

**Model B: Swarm (Parallel autonomous workers)**
- Best when: task is embarrassingly parallel (many independent items to process)
- Uses: shared TaskList, agents self-claim work, no leader micromanagement
- Template: `swarm-team-template.md`

**Model C: Fork-Execute (Context inheritance)**
- Best when: child agent needs parent's full research context
- Uses: `forkSubagent.ts`, byte-exact prompt cache sharing
- Template: `agent-spawning-template.md`

---

## Step 3 — Produce the workflow design

Output a complete design document:

````
## Workflow Design: [Name]

### Coordination Model
**Model**: [A/B/C] — [reason]

---

### Agents

| Agent | Role | Tools | Spawning Mode | Output |
|-------|------|-------|---------------|--------|
| Coordinator | [role] | read-only | main thread | synthesis |
| [Agent A] | [role] | [tools] | background/fork | [output] |
| [Agent B] | [role] | [tools] | background/fork | [output] |
| Verifier | independent review | read-only | fresh (no context) | verdict |

---

### Communication

**Coordinator → Workers**: [how tasks are assigned]
- TaskList / direct spawn / SendMessage

**Workers → Coordinator**: [how results come back]  
- `<task-notification>` XML / scratchpad files / TaskOutputTool

**Shared State**: [how agents share findings]
- Scratchpad dir: `.claude/scratchpad/`
- OR: pass via task output
- OR: shared TaskList with result fields

---

### Phase Breakdown

**Phase 1: [Name]** *(~N agents, parallel)*
```
Coordinator spawns:
  Agent A → [specific task]
  Agent B → [specific task]
  Agent C → [specific task]
Collect via: [notification/scratchpad]
```

**Phase 2: [Name]** *(coordinator only)*
```
Read all Phase 1 results
Synthesize into: [spec/plan/list]
```

**Phase 3: [Name]** *(N agents)*
```
[how implementation is distributed]
```

**Phase 4: Verification** *(1 FRESH agent)*
```
New agent with NO implementation context
Only sees: [original requirements]
Checks: [what it verifies]
```

---

### Prompt Cache Strategy

- Fork from coordinator: yes/no — [reason]
- Shared prefix size estimate: ~[N]k tokens
- Cache savings: [estimate if forking]

---

### Permission Model

- Workers need: [list permissions]
- Leader grants: [permission sync approach]
- Bubbling needed for: [sensitive operations]

---

### Failure Handling

| Failure | Recovery |
|---------|----------|
| Worker crashes | [how coordinator detects + recovers] |
| Coordinator crashes | [session recovery approach] |
| Verification fails | [what happens] |

---

### Anti-Patterns to Avoid

- [ ] Do NOT have the verifier see the implementation plan (confirmation bias)
- [ ] Do NOT put all work in one agent (context overflow)
- [ ] Do NOT skip synthesis phase (worker results need to be merged)
````

---

## Built-in Agent Types (ready to use)

| Type | Tools | Best for |
|------|-------|----------|
| `general-purpose` | All tools | Research, implementation, multi-step |
| `Explore` | Read-only | Fast codebase exploration |
| `Plan` | Read-only | Architecture planning |
| `verification` | Read-only | Independent review |

Custom agents go in `.claude/agents/[name].md` with frontmatter:
```yaml
---
name: my-agent
description: what it does
model: claude-opus-4-6  # optional override
tools: [Bash, Read, Grep, Glob]  # restrict tools
---
System prompt for this agent...
```
