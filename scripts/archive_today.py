#!/usr/bin/env python3
"""Archive the current homepage and reset index.html.

Intended schedule: daily at 01:00 Asia/Singapore.
Default behavior:
- archive yesterday's index.html to archive/YYYY/MM/YYYY-MM-DD.html
- reset index.html from templates/index.html for today's date

This script is useful for local/Codex/GitHub Actions workflows. ChatGPT Tasks can follow the same rules with GitHub write tools.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
TZ = ZoneInfo("Asia/Singapore")


def replace_date_tokens(text: str, date_str: str) -> str:
    year, month, _day = date_str.split("-")
    text = text.replace("YYYY-MM-DD", date_str)
    text = text.replace("YYYY/MM", f"{year}/{month}")
    return text


def mark_archived(html: str, archive_date: str) -> str:
    html = html.replace("<meta name=\"date\"", f"<meta name=\"archived-date\" content=\"{archive_date}\">\n  <meta name=\"date\"")
    html = html.replace("今日网页", "历史归档")
    html = html.replace("index.html", f"archive/{archive_date[:4]}/{archive_date[5:7]}/{archive_date}.html", 1)
    return html


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-date", help="Date to archive, default yesterday in Asia/Singapore, format YYYY-MM-DD")
    parser.add_argument("--new-date", help="New index date, default today in Asia/Singapore, format YYYY-MM-DD")
    args = parser.parse_args()

    now = datetime.now(TZ)
    archive_date = args.archive_date or (now - timedelta(days=1)).strftime("%Y-%m-%d")
    new_date = args.new_date or now.strftime("%Y-%m-%d")

    index = ROOT / "index.html"
    template = ROOT / "templates" / "index.html"
    if not index.exists():
        raise SystemExit("index.html not found")
    if not template.exists():
        raise SystemExit("templates/index.html not found")

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", archive_date):
        raise SystemExit("archive date must be YYYY-MM-DD")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", new_date):
        raise SystemExit("new date must be YYYY-MM-DD")

    year, month, _day = archive_date.split("-")
    archive_path = ROOT / "archive" / year / month / f"{archive_date}.html"
    archive_path.parent.mkdir(parents=True, exist_ok=True)

    current_html = index.read_text(encoding="utf-8")
    archive_path.write_text(mark_archived(current_html, archive_date), encoding="utf-8")

    new_html = replace_date_tokens(template.read_text(encoding="utf-8"), new_date)
    index.write_text(new_html, encoding="utf-8")

    print(f"Archived index.html to {archive_path.relative_to(ROOT)}")
    print(f"Reset index.html for {new_date}")


if __name__ == "__main__":
    main()
