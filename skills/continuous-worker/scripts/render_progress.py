#!/usr/bin/env python3
"""
Render a compact ASCII progress bar for continuous-worker updates.
"""

from __future__ import annotations

import argparse
import json
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a compact progress bar.")
    parser.add_argument("--percent", type=float, help="Progress percent from 0 to 100.")
    parser.add_argument("--step", type=int, help="Completed milestone count.")
    parser.add_argument("--total", type=int, help="Total milestone count.")
    parser.add_argument("--width", type=int, default=20, help="Bar width in characters.")
    parser.add_argument("--label", default="", help="Optional prefix label.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    return parser.parse_args()


def clamp_percent(value: float) -> int:
    return max(0, min(100, int(round(value))))


def resolve_percent(args: argparse.Namespace) -> int:
    if args.percent is not None:
        return clamp_percent(args.percent)
    if args.step is None or args.total is None:
        raise ValueError("pass --percent or both --step and --total")
    if args.total <= 0:
        raise ValueError("--total must be greater than 0")
    if args.step < 0:
        raise ValueError("--step must be >= 0")
    return clamp_percent((args.step / args.total) * 100)


def render_bar(percent: int, width: int) -> str:
    if width <= 0:
        raise ValueError("--width must be greater than 0")
    filled = round((percent / 100) * width)
    return f"[{'#' * filled}{'-' * (width - filled)}] {percent}%"


def main() -> int:
    args = parse_args()
    try:
        percent = resolve_percent(args)
        bar = render_bar(percent, args.width)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    label = args.label.strip()
    text = f"{label} {bar}".strip()
    if args.format == "json":
        print(json.dumps({"label": label, "percent": percent, "bar": bar, "text": text}))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
