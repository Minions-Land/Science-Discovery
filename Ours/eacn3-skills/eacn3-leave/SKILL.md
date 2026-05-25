---
name: eacn3-leave
description: "Disconnect from the EACN3 network"
---

# /eacn3-leave — Disconnect from Network

Gracefully disconnect from the EACN3 network.

## What happens

1. All WebSocket connections closed
2. Server unregistered from network (cascade removes all Agents from network discovery)
3. Background heartbeat stops
4. Local state cleared (server_card, agents)

## Steps

### Step 1 — Confirm with user

Before disconnecting, show current state:

```
eacn3_server_info()
```

Tell the user:
- How many Agents will go offline
- Any active tasks will lose this server's execution slots

Ask: "Disconnect? Your Agents will be removed from network discovery."

### Step 2 — Disconnect

```
eacn3_disconnect()
```

### Step 3 — Confirm

"Disconnected. Server and all Agents removed from network."

## Decision: when NOT to leave

- If there are tasks in "executing" state for your Agents, disconnecting will cause those bids to timeout — **reputation penalty**. Warn the user and suggest finishing or rejecting active tasks first.

If the user decides NOT to disconnect after seeing this warning:
- Suggest `/eacn3-execute` to finish active tasks, or `eacn3_reject_task` to gracefully exit them
- Suggest `/eacn3-dashboard` to review what's in progress before deciding again
