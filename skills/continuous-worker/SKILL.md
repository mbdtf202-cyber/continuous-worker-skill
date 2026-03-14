---
name: continuous-worker
description: Keep one long-running goal moving without repeated human nudges. Use when a user wants an always-on agent, 24/7 background progress, continuous work on one task, autonomous follow-through, fewer reminder messages, or asks the agent to keep working until done. Prefer a durable task file plus heartbeat/cron wakeups and background process monitoring, not one endless agent turn.
metadata: { "openclaw": { "emoji": "⏳" } }
---

# continuous-worker

Treat the job as one logical task across many recoverable runs.

## Quick start

For a brand-new continuous task:

1. Read `references/confirmation-protocol.md`.
2. Confirm the goal, success criteria, allowed actions, report cadence, and escalation rules with the user.
3. Create the runtime task with the `task` tool. Use `action=create` after the user explicitly says to start.
4. Create the workspace task file with `python3 {baseDir}/scripts/init_task.py ...` or by following the inline template below.
5. Start the work in a recoverable way.
6. Immediately record a first checkpoint with `task(action=checkpoint)` and set the next wake with `task(action=ensure_wake)`.
7. Read `references/reporting-protocol.md` before sending progress updates.
8. Use `task(action=report)` or `python3 {baseDir}/scripts/render_progress.py ...` to render a progress bar for user-facing updates.
9. If Control UI is available, use the `Tasks` page to inspect health, timeline, background sessions, and wake ownership while the task is running.

## Core rules

- Do not rely on one endless agent turn as the primary solution.
- Keep the task alive in durable state, not only in chat memory.
- Before ending a run, either advance the work, mark it blocked, or schedule the next wake.
- Default to silent progress. Only message the user on blockers, approvals, milestones, or completion.
- If a shell command may outlive the current run, leave a disk log or artifact trail in the workspace. The in-memory `process` registry is useful but not durable across gateway restarts.
- Reuse the same task slug, task file, and cron job name for the same logical goal.
- On completion or permanent failure, clean up any wakeups so the task does not zombie-loop.
- Prefer the `task` tool as the source of truth for status, progress, stats, and wake ownership. The workspace task file is the human-readable companion, not the only runtime record.
- Assume background execution is recoverable but not magic: runtime metadata persists, background session state is reconciled, and overdue wakes may be auto-recovered, but you still need good logs, artifacts, and idempotent commands.

## When to use what

- **Heartbeat**: periodic review, lightweight supervision, low-urgency follow-through.
- **Main-session cron/system events**: resume with shared context when you want the main session to own the task.
- **Isolated cron**: precise or noisy recurring work. Read the task file first because isolated cron runs start fresh.
- **Background bash + process**: real long-running shell work such as builds, crawls, indexing, downloads, and test suites.
- **Control UI Tasks page**: operator surface for live progress, health, timeline, wake editing, and manual pause/resume/block/fail actions.

## Task state machine

Use explicit states in the task file:

- `active`: work should continue now or on the next wake.
- `waiting`: background work or an external dependency is in flight; check again later.
- `blocked`: the task needs user input, credentials, permission, or a non-retryable external fix.
- `done`: success criteria are met; remove wakeups and report completion.
- `failed`: terminal failure after retry budget is exhausted; remove wakeups and report the failure clearly.

Do not leave the state ambiguous.

## Workflow

### 1) Create or reuse a durable task file

Use a stable path such as `tasks/<slug>.md` or `memory/active-tasks/<slug>.md`.

Also create a runtime task record with the `task` tool:

```text
task action:create title:"<title>" goal:"<goal>" status:"active" successCriteria:["..."]
```

For predictable setup, prefer the bundled helper:

```bash
python3 {baseDir}/scripts/init_task.py \
  --title "<task title>" \
  --goal "<goal>" \
  --criterion "<done criterion 1>" \
  --criterion "<done criterion 2>"
```

Minimum template:

```md
# Task: <title>

Slug: <stable-slug>
Status: active
Goal: <what "done" means>
Success criteria:
- <criterion 1>
- <criterion 2>

Current state: <short factual summary>
Next action: <single next step>
Next wake: <timestamp or schedule rule>
Wake owner: <heartbeat | cron:<job-name> | manual>
Retry budget: <for example 3 attempts or 24h>
User update policy: blockers, milestones, completion only
Progress: <0-100 or unknown>
Progress bar: <render with scripts/render_progress.py>
Blockers:
- none

Background work:
- sessionId: <process session id or none>
  command: <command summary>
  log: <workspace-relative log path>
  startedAt: <timestamp>

Artifacts:
- <path>

Notify user when:
- blocked
- milestone reached
- done

Recovery notes:
- how to resume if this run ends or the gateway restarts

Last update: <timestamp>
```

Use one file per logical task. Do not split one task across many ad-hoc notes.

### 2) Start work in a recoverable way

- Prefer idempotent commands.
- If the command may run for a while, use background execution and also write logs to a workspace file.
- Record the command summary, `sessionId`, log path, expected artifact path, and next check time in the task file.
- If the command is not idempotent, write the safety conditions into `Recovery notes` before launching it.

Example pattern:

```text
bash background:true command:"<long command> > logs/<task>.log 2>&1"
```

Then save the returned `sessionId` in the task file.

Also attach it to the runtime task:

```text
task action:attach_process id:"<task-id>" processSessionId:"<sessionId>" processCommand:"<summary>" processLogPath:"logs/<task>.log"
```

If the runtime can infer a process pid, keep it attached. The supervisor and task service use pid/state reconciliation after restarts.

### 2.5) Do not start without explicit confirmation

Before launching long-running work, confirm:

- goal
- success criteria
- allowed side effects
- progress report cadence
- escalation rules
- stop conditions

Use `references/confirmation-protocol.md` as the default contract.

### 3) Re-arm the task before the run ends

Use a stable cron job name such as `continuous-worker:<slug>`. Edit an existing job instead of creating duplicates.

- Use heartbeat when a general review loop is enough.
- Use cron when you need exact wakeups or frequent polling.
- Use main-session wakeups when you want shared context.
- Use isolated cron when you want a clean run and the task file already contains the required state.
- Do not leave both heartbeat and aggressive cron polling fighting each other unless that overlap is intentional and documented in the task file.

Recommended defaults:

- Long build/test/index/download: cron poll every 5-15 minutes, or heartbeat if urgency is low.
- Human-dependent follow-up: heartbeat or sparse cron, not tight polling.
- Precise deadline or scheduled handoff: isolated cron at exact time.
- Multi-step research/planning with light supervision: heartbeat plus task file.

Preferred runtime pattern:

```text
task action:ensure_wake id:"<task-id>" wakeStrategy:"cron_every" scheduleEveryMs:300000
```

If Control UI is available, the same wake configuration can be edited from the `Tasks` page. The page now supports:

- changing wake strategy
- editing cron/every/at fields
- applying wake
- applying wake and running now
- cancelling wake

### 4) On every wake

Do this in order:

1. Read the task file first.
1.5 Read the runtime task record with `task(action=get)`.
2. Check any attached background `process` session with `poll` or `log`.
3. Read workspace logs and artifacts.
4. Update runtime state with `task(action=touch)` or `task(action=checkpoint)`.
5. Mirror the essential state into the task file.
6. Either take the next meaningful step or schedule the next wake.
6. If nothing needs attention, stay silent or return `HEARTBEAT_OK` during heartbeat runs.

If the stored `process` session is gone:

1. Check the log file and artifacts first.
2. Infer whether the work actually finished, failed, or needs relaunch.
3. If relaunching is safe, update `Recovery notes` and relaunch idempotently.
4. Never assume missing in-memory `process` state means the task failed.

If the runtime marks the task as `overdue`, assume the task service may attempt recovery by:

- reconciling background session state
- forcing an overdue wake
- rebuilding a missing cron wake when the task still has wake configuration

### 5) Escalate only when needed

Notify the user only for:

- missing credentials, permissions, or approvals
- repeated failures beyond the retry budget
- ambiguous fork-in-the-road decisions
- milestone completion
- final completion

When escalating, include:

- current state
- what was tried
- what evidence you checked
- the minimum user action needed

If the task is recoverable without user input, prefer updating runtime state and continuing over escalating immediately.

## Progress reporting

Keep progress visible in both the task file and user-facing updates.

- If you can estimate a real percentage, record it.
- If a true percentage is not defensible, derive progress from milestones or phases and label it as an estimate.
- Do not fake precision. `40% estimated` is better than an invented exact number.
- Prefer the runtime task record for progress state:

```text
task action:checkpoint id:"<task-id>" progressStep:2 progressTotal:5 phase:"testing" currentState:"Finished 2 of 5 milestones"
task action:report id:"<task-id>"
```

- Use the bundled renderer for consistency when you need a manual bar:

```bash
python3 {baseDir}/scripts/render_progress.py --percent 40 --label "Running tests"
python3 {baseDir}/scripts/render_progress.py --step 2 --total 5 --label "Milestones"
```

Default user-facing update shape:

- one-line summary
- progress bar
- current phase
- what changed since last update
- next checkpoint or blocker

Use `references/reporting-protocol.md` for the exact format.

Control UI expectation:

- progress bar should move when progress is measurable
- timeline should show wake/report/checkpoint/recovery activity
- health should stay `ok` or explain why not

## Before ending any run

Check all of these:

1. Is the task file updated?
2. Is the status explicit?
3. Is the next wake explicit, or is the task terminal?
4. If background work exists, are `sessionId`, log path, and artifact path recorded?
5. If the task is `done` or `failed`, did you disable or remove its wakeups?

## Recommended heartbeat checklist

If the user wants a 24/7 worker, keep `HEARTBEAT.md` small and stable.

Suggested pattern:

```md
# Continuous worker

- Review active task files under `tasks/` or `memory/active-tasks/`.
- Resume any task whose `Next wake` is due.
- Check attached background session ids, logs, and artifacts.
- If no active task needs attention, reply `HEARTBEAT_OK`.
```

## Completion and cleanup

When a task is complete:

- verify the success criteria against real outputs
- mark the runtime task complete with `task(action=complete)`
- write the final state to the task file
- disable or remove related cron jobs
- stop or clear background sessions if they are no longer needed
- send one completion update to the user

When a task is terminally failed:

- mark the runtime task failed with `task(action=fail)`
- record the evidence and last attempted recovery
- disable or remove related cron jobs
- avoid infinite retries
- notify the user once with the blocker or failure summary

## Runtime notes

Current runtime behavior you should rely on:

- durable task records persist independently of chat history
- background process metadata persists and is rehydrated after restart
- detached background sessions are reconciled against pid liveness
- task service derives `ok|warning|stale|overdue|terminal` health states
- task service may auto-recover overdue wakes or rebuild missing wake jobs
- task service may also nudge waiting tasks forward when declared artifacts already exist on disk and no background process is still running

Current runtime limits you should still plan around:

- old processes are not fully re-attached for interactive stdin/stdout control after restart
- a long-running shell command still needs durable logs and artifacts to be truly trustworthy
- auto-recovery helps, but does not replace careful task design

## Control UI checklist

If the Control UI `Tasks` page is available, treat it as an operator console:

- verify health is not `warning`, `stale`, or `overdue` without explanation
- inspect the timeline after automatic recovery
- edit wake strategy and save it from the task page if the default cadence is wrong
- update success criteria, cadence, escalation rules, stop conditions, and recovery notes when the task contract changes

## Anti-patterns

- Do not keep the entire plan only in conversation history.
- Do not ping the user on every wake.
- Do not assume isolated cron remembers prior turns.
- Do not assume `process` sessions survive gateway restart.
- Do not create many overlapping cron jobs for the same task.
- Do not declare success without checking artifacts, outputs, or exit status.
- Do not leave a task in `active` with no wake owner.
- Do not keep retrying a broken command forever without changing the plan.

## What this skill can and cannot do

- This skill can make OpenClaw behave like a persistent worker by combining task files, heartbeat, cron, and background commands.
- This skill cannot turn the current agent runtime into a truly durable single run that survives every restart or crash. For that, OpenClaw core needs a first-class task runtime.
