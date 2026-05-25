---
name: goal-setting
description: "Open before dispatching any execution — define sensor, metric, feedback period, and stopping rule so every task has a closed verification loop."
---

# Skill — Goal Setting

No task without a way to know it worked. If you cannot say "I will know success because X changes by Y within Z," the task is not ready to dispatch.

## When to invoke

- You have decided WHAT to do (after first-principles + dialectical-synthesis) and are about to decide HOW to verify it.
- Writing acceptance criteria for a plan, a subagent prompt, or an EACN task.
- Designing an experiment's success/failure boundary.
- Any time you are about to dispatch work to a subagent or Codex — the goal is what you hand them as their stopping condition.

Not every task needs a complex metric. A one-line binary check ("test passes") is a valid goal for a simple fix. Reserve the full procedure for multi-step or ambiguous work.

## Structure

Five-element loop definition: sensor → metric → threshold → feedback period → stopping rule. The most valuable output is the stopping rule — it prevents runaway execution and gives the subagent permission to declare done (or declare blocked).

## Procedure

1. **Sensor.** What observable thing do you measure? Must be something the executor can actually read (a test output, a file diff, a benchmark number, a response from another role, a log line). Not "code quality" — that's a judgment, not a sensor.
2. **Metric.** How do you quantify the sensor reading? Binary (pass/fail), numeric (latency in ms, accuracy %), or categorical (accepted/rejected/needs-revision). Pick the simplest metric that distinguishes success from failure.
3. **Threshold.** What value means success? Be specific: "P95 latency < 500ms", "all 12 tests pass", "reviewer does not flag the claim as unsupported." If you cannot name a threshold, the task is underspecified — return to unstated-premises.
4. **Feedback period.** How long until you can read the sensor? Immediately (run tests), minutes (wait for experiment), hours (wait for reviewer wake), days (wait for external response). This determines whether you block or exit the wake.
5. **Stopping rule.** When does the executor declare done or pivot?
   - **Success**: sensor meets threshold → commit, report result, move on.
   - **Failure**: sensor misses threshold after N attempts → report blocker, do not retry indefinitely.
   - **Timeout**: feedback period expires without reading → escalate or exit wake.
6. **Hand off.** Pass the goal (all 5 elements) to the subagent/Codex as its success criterion. The executor verifies its own output against the metric before returning.

## Output format

When writing goals into a plan or subagent prompt, use this compact shape:

```
Goal: <one-sentence description>
Sensor: <what to measure>
Metric: <how to quantify>  Threshold: <success value>
Feedback: <when readable>  Stop: <success | failure | timeout rules>
```

## Pitfalls

- **Vanity metrics.** "Code is clean" is not a sensor. "Ruff reports 0 errors" is.
- **Missing failure path.** A goal without a failure/timeout rule lets the executor loop forever. Always define when to stop trying.
- **Over-engineering simple tasks.** A one-liner fix needs "test passes" as its goal, not a 5-element loop. Scale the ceremony to the ambiguity.
- **Confusing the goal with the plan.** The goal says WHAT success looks like. The plan says HOW to get there. This skill produces goals; `writing-plans` produces plans.
