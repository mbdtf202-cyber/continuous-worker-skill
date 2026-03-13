# Continuous Worker Skill

`continuous-worker` turns OpenClaw into a long-running, recoverable worker for one ongoing goal.

## Install

### Import a local `.skill` file

```bash
openclaw skills import __SKILL_FILE__
```

### Import directly from a GitHub release URL

```bash
openclaw skills import __SKILL_URL__
```

### Replace an existing install

```bash
openclaw skills import __SKILL_FILE__ --replace
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

- File: `__SKILL_FILE__`
- SHA256: `__SKILL_SHA256__`

## Publish to ClawHub

```bash
__CLAWHUB_PUBLISH_COMMAND__
```
