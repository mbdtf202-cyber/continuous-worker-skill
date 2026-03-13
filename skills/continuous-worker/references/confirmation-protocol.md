# Confirmation protocol

Use this protocol before starting a long-running task for the user.

## Default contract

Confirm these items in one compact message:

1. Goal
2. Definition of done
3. Allowed side effects
4. Report cadence
5. Escalation rules
6. Stop conditions

Do not start background work until the user has explicitly approved the plan.

## Default wording pattern

Use short, direct language. A good shape is:

```md
Continuous task contract

- Goal: <goal>
- Done means: <success criteria>
- I am allowed to: <allowed actions>
- I will report: <cadence>
- I will interrupt you only for: <blockers/approvals/milestones/completion>
- I will stop if: <stop conditions>

Reply `start` to begin, or tell me what to change.
```

## Defaults when the user does not specify

- Report cadence: every 30-60 minutes for active work, less often for waiting states.
- Escalation: blockers, approvals, milestones, completion only.
- Stop conditions: explicit user stop, success criteria met, or terminal failure after retry budget.
- Allowed actions: read/write within the workspace, run safe project commands, schedule wakeups, and monitor logs.

## When to ask follow-up questions

Ask follow-up questions only if one of these is unclear:

- the goal is ambiguous
- success criteria cannot be verified
- the task may cause meaningful side effects
- progress cadence materially affects cost or noise
- the task needs credentials or approvals that are not available

If the task is straightforward, propose the defaults and ask for a single explicit `start`.
