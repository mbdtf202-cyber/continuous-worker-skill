# Continuous Worker Skill

`continuous-worker` turns OpenClaw into a long-running, recoverable worker for one ongoing goal.

## Install

### Import a local `.skill` file

```bash
openclaw skills import continuous-worker.skill
```

### Import directly from a GitHub release URL

```bash
openclaw skills import https://github.com/mbdtf202-cyber/continuous-worker-skill/releases/download/continuous-worker-skill-v0.1.0/continuous-worker.skill
```

### Replace an existing install

```bash
openclaw skills import continuous-worker.skill --replace
```

## Verify

```bash
openclaw skills list --eligible
openclaw skills info continuous-worker
```

## Use

```text
Use $continuous-worker. I want you to keep working on this task 24/7, confirm the operating contract with me first, then keep going until it is done.
```

The agent will:

1. confirm the goal and safety contract
2. create a durable runtime task
3. optionally create a local notes file if operator notes are useful
4. start the work
5. keep updating progress, health, and task statistics
6. report milestones, blockers, and completion

## Artifact integrity

- File: `continuous-worker.skill`
- SHA256: `2145501c75e769c81d58fd2d889b93a377dab4985919305fef950f1d79e551a9`

## Publish to ClawHub

```bash
clawhub publish ./skills/continuous-worker --slug continuous-worker --name "Continuous Worker" --version "0.1.0" --changelog "Release continuous-worker packaged skill"
```

## Notes

- Runtime task state is canonical; any workspace markdown note is optional operator context only.
- Heartbeat wakes depend on a live session; use cron when you need a more durable autonomous review loop.
