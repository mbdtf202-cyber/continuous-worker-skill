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
    goal = args.goal.strip()
    criteria = args.criterion or ["replace me with a concrete success criterion"]
    criteria_block = "\n".join(f"- {item}" for item in criteria)
    return f"""# Task Notes: {args.title}

Slug: {slug}
Canonical runtime: the `task` record for `{slug}` is the source of truth
Goal: {goal}
Success criteria:
{criteria_block}

Operator notes:
- add local-only notes here when they are useful
- do not duplicate runtime fields that already live in the `task` record

Preferred wake owner: {args.wake_owner}
Retry budget reference: {args.retry_budget}
Update policy reference: {args.update_policy}

Logs:
- logs/{slug}.log

Artifacts to watch:
- none yet

Recovery notes:
- read the runtime task record first on every wake
- use this file only for operator notes that are not already stored in the runtime task
- verify logs and artifacts before relaunching work

Last note update: pending
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
