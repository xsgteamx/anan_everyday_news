#!/usr/bin/env python3
"""Check archive conventions for anan_everyday_news."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE_FILE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
LEGACY_DIRS = ["daily", "afternoon", "weekly", "monthly", "raw"]
REQUIRED_SECTIONS = [
    "## 更新记录",
    "## 1. 8:30 主简报",
    "## 8. 10:30 喝水提醒与小补丁",
    "## 9. 15:30 下午增量更新",
]


def check_no_legacy_dirs(errors: list[str]) -> None:
    for name in LEGACY_DIRS:
        if (ROOT / name).exists():
            errors.append(f"legacy directory should not exist: {name}/")


def check_day_files(errors: list[str]) -> None:
    day_files = sorted(path for path in ROOT.glob("*.md") if DATE_FILE_RE.match(path.name))
    if not day_files:
        errors.append("no root date files found, expected files like 2026-06-25.md")
        return

    for path in day_files:
        text = path.read_text(encoding="utf-8")
        date = path.stem
        if f"# 安安每日信息流｜{date}" not in text:
            errors.append(f"{path.name}: missing expected H1 title with date")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{path.name}: missing section {section}")


def main() -> None:
    errors: list[str] = []
    check_no_legacy_dirs(errors)
    check_day_files(errors)

    if errors:
        print("Archive convention check failed:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print("Archive convention check passed.")


if __name__ == "__main__":
    main()
