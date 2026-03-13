#!/usr/bin/env python3
"""
Package a skill folder into a distributable .skill zip archive.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


def validate_skill_dir(skill_dir: Path) -> None:
    if not skill_dir.exists():
      raise SystemExit(f"Skill folder not found: {skill_dir}")
    if not skill_dir.is_dir():
      raise SystemExit(f"Path is not a directory: {skill_dir}")
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
      raise SystemExit(f"SKILL.md not found in {skill_dir}")


def package_skill(skill_dir: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"{skill_dir.name}.skill"
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(skill_dir.rglob("*")):
            if file_path.is_symlink():
                continue
            if file_path.is_dir():
                continue
            arcname = Path(skill_dir.name) / file_path.relative_to(skill_dir)
            zf.write(file_path, arcname)
    return archive_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir")
    parser.add_argument("output_dir", nargs="?", default="dist")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    validate_skill_dir(skill_dir)
    archive_path = package_skill(skill_dir, output_dir)
    print(archive_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
