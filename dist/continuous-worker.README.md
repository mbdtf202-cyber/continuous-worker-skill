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

## Artifact integrity

- File: `continuous-worker.skill`
- SHA256: `6fcc0378f0d254a20a3c33c5db0b047aea79ed1823676c2103eb33aa650d9f0a`

## Publish to ClawHub

```bash
clawhub publish ./skills/continuous-worker --slug continuous-worker --name "Continuous Worker" --version "0.1.0" --changelog "Release continuous-worker packaged skill"
```
