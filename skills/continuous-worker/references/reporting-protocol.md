# Reporting protocol

Use this format for progress updates on long-running work.

## Goals

- Keep updates easy to scan.
- Make progress visible.
- Avoid noisy chatter.
- Distinguish active progress from waiting and blocked states.

## Update triggers

Send an update only on:

- scheduled cadence
- milestone reached
- blocker found
- approval needed
- completion

Do not send an update for every heartbeat wake.

## Default progress update format

```md
<one-line summary>
<progress bar>
Phase: <current phase>
Changed: <what changed since last update>
Next: <next checkpoint, next wake, or blocker>
```

Example:

```md
Index build is still progressing and the parser phase finished.
[########------------] 40%
Phase: indexing
Changed: parsed 4/10 sources, wrote `artifacts/index.json`
Next: check the background process again at 15:30 local time
```

## Progress percentage rules

- Use a real percent when work is measurable.
- Use milestone-derived percent when the task has discrete stages.
- If percent is speculative, say `estimated` in the summary or phase line.
- If no honest percent is possible, use a phase bar from completed milestones.

## Status-specific wording

- `active`: emphasize current work and next checkpoint
- `waiting`: emphasize what is in flight and when you will check again
- `blocked`: emphasize the minimum user action needed
- `done`: emphasize verified outputs and cleanup performed
- `failed`: emphasize evidence, retries attempted, and why it stopped
