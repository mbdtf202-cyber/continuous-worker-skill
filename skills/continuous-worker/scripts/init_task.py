#!/usr/bin/env python3
"""
Create a markdown task file for continuous-worker.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")
    return slug or "task"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a continuous-worker task file.")
    parser.add_argument("--title", required=True, help="Task title.")
    parser.add_argument("--goal", required=True, help="Task goal.")
    parser.add_argument(
        "--criterion",
        action="append",
        default=[],
        help="Success criterion. Repeat for multiple criteria.",
    )
    parser.add_argument("--slug", help="Stable task slug. Defaults to slugified title.")
    parser.add_argument(
        "--dir",
        default="tasks",
        help="Directory where the task file should be created. Default: tasks",
    )
    parser.add_argument(
        "--wake-owner",
        default="manual",
        help="Wake owner, for example heartbeat, cron:continuous-worker:my-task, or manual.",
    )
    parser.add_argument(
        "--retry-budget",
        default="3 attempts",
        help="Retry budget summary. Default: 3 attempts",
    )
    parser.add_argument(
        "--update-policy",
        default="blockers, milestones, completion only",
        help="User update policy summary.",
    )
    return parser.parse_args()


def render_task(args: argparse.Namespace, slug: str) -> str:
    criteria = args.criterion or ["replace me with a concrete success criterion"]
    criteria_block = "\n".join(f"- {item}" for item in criteria)
    return f"""# Task: {args.title}

Slug: {slug}
Status: active
Goal: {args.goal}
Success criteria:
{criteria_block}

Current state: newly created
Next action: confirm details with the user or start the first safe step
Next wake: unset
Wake owner: {args.wake_owner}
Retry budget: {args.retry_budget}
User update policy: {args.update_policy}
Progress: 0
Progress bar: [--------------------] 0%
Blockers:
- none

Background work:
- sessionId: none
  command: none
  log: logs/{slug}.log
  startedAt: none

Artifacts:
- none yet

Notify user when:
- blocked
- milestone reached
- done

Recovery notes:
- read this file first on every wake
- verify logs and artifacts before relaunching work

Last update: pending
"""


def main() -> int:
    args = parse_args()
    slug = args.slug.strip() if args.slug else slugify(args.title)
    task_dir = Path(args.dir)
    task_dir.mkdir(parents=True, exist_ok=True)
    path = task_dir / f"{slug}.md"
    if path.exists():
        raise SystemExit(f"task file already exists: {path}")
    path.write_text(render_task(args, slug), encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
