#!/usr/bin/env python3
"""Check archive conventions for the HTML homepage workflow."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_DIRS = ["daily", "afternoon", "weekly", "monthly", "raw"]
ROOT_DATE_FILES = [re.compile(r"^\d{4}-\d{2}-\d{2}\.md$"), re.compile(r"^\d{4}-\d{2}-\d{2}\.html$")]
REQUIRED_SECTIONS = [
    'id="update-log"',
    'id="overview"',
    'id="top-stories"',
    'id="ai-tech"',
    'id="freebies"',
    'id="games-community"',
    'id="devops"',
    'id="risk-policy"',
    'id="actions"',
    'id="afternoon-update"',
    'id="media-assets"',
]


def check_no_legacy_dirs(errors: list[str]) -> None:
    for name in LEGACY_DIRS:
        if (ROOT / name).exists():
            errors.append(f"legacy directory should not exist: {name}/")


def check_no_root_date_files(errors: list[str]) -> None:
    for path in ROOT.iterdir():
        if not path.is_file():
            continue
        if any(pattern.match(path.name) for pattern in ROOT_DATE_FILES):
            errors.append(f"daily date file should not be in repo root: {path.name}; use index.html or archive/YYYY/MM/YYYY-MM-DD.html")


def check_index_html(errors: list[str]) -> None:
    index = ROOT / "index.html"
    if not index.exists():
        errors.append("index.html is missing")
        return
    text = index.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"index.html missing required section marker: {section}")


def check_template(errors: list[str]) -> None:
    template = ROOT / "templates" / "index.html"
    if not template.exists():
        errors.append("templates/index.html is missing")


def main() -> None:
    errors: list[str] = []
    check_no_legacy_dirs(errors)
    check_no_root_date_files(errors)
    check_index_html(errors)
    check_template(errors)

    if errors:
        print("Archive convention check failed:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print("Archive convention check passed.")


if __name__ == "__main__":
    main()
