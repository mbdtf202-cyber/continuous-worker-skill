# Continuous Worker Skill

`continuous-worker` is an OpenClaw skill for long-running, recoverable work on a single goal.

It is designed for users who want an agent to:

- confirm a task contract before starting
- keep working 24/7 across many recoverable runs
- report progress with a visible progress bar
- track task state, wake ownership, and background processes
- expose task status in the OpenClaw Control UI

## What it expects

This skill is intended for recent OpenClaw builds that include:

- the `task` runtime/tool
- `tasks.*` gateway methods
- the Control UI `Tasks` page

If you use an older OpenClaw build, import may succeed but the runtime features may be missing.

## Install

### Import a local `.skill` file

```bash
openclaw skills import ./continuous-worker.skill
```

### Replace an existing install

```bash
openclaw skills import ./continuous-worker.skill --replace
```

### Import directly from a GitHub release URL

```bash
openclaw skills import https://github.com/mbdtf202-cyber/continuous-worker-skill/releases/download/<tag>/continuous-worker.skill
```

## Verify

```bash
openclaw skills list --eligible
openclaw skills info continuous-worker
```

You should see `continuous-worker` as an eligible workspace skill.

## Use

Start a new OpenClaw session and ask the agent to use `$continuous-worker`.

Example prompt:

```text
Use $continuous-worker. I want you to keep working on this task 24/7. Confirm the operating contract with me first, then continue until it is done.
```

The agent should:

1. confirm the goal, success criteria, allowed actions, reporting cadence, and stop conditions
2. create a durable task record
3. start recoverable work
4. keep updating progress, stats, and wake ownership
5. report blockers, milestones, and completion

## Repository layout

- `skills/continuous-worker/`: skill source
- `scripts/package_skill.py`: create a distributable `.skill` archive
- `scripts/release_continuous_worker_skill.sh`: build release artifacts
- `templates/README.release.template.md`: template for release-facing install instructions

## Build a packaged `.skill`

```bash
python3 scripts/package_skill.py skills/continuous-worker dist
```

This creates:

- `dist/continuous-worker.skill`

## Build release artifacts

```bash
./scripts/release_continuous_worker_skill.sh --repo mbdtf202-cyber/continuous-worker-skill --tag continuous-worker-skill-v0.1.0 --clawhub-version 0.1.0
```

This creates:

- `dist/continuous-worker.skill`
- `dist/continuous-worker.skill.sha256`
- `dist/continuous-worker.README.md`

## Publish to ClawHub

```bash
clawhub publish ./skills/continuous-worker --slug continuous-worker --name "Continuous Worker" --version 0.1.0 --changelog "Release continuous-worker packaged skill"
```

## GitHub Releases

This repo includes a GitHub Actions workflow that can package the skill and attach release artifacts on tag push or manual dispatch.

Recommended tag format:

```text
continuous-worker-skill-v0.1.0
```

## License

This repository ships under the MIT license. See `LICENSE`.
