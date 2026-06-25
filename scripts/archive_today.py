#!/usr/bin/env python3
"""Archive today's JSON data and reset data/today.json.

HTML is now a fixed renderer. We archive JSON, not full HTML.
Review old days with: index.html?date=YYYY-MM-DD
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
TZ = ZoneInfo("Asia/Singapore")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def reset_today(new_date: str) -> dict:
    template = load_json(ROOT / "data" / "template.json")
    template["date"] = new_date
    template["status"] = "today"
    template["summary"] = "待 08:30 主简报更新。"
    return template


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-date", help="Date to archive, default yesterday in Asia/Singapore, format YYYY-MM-DD")
    parser.add_argument("--new-date", help="New today date, default today in Asia/Singapore, format YYYY-MM-DD")
    args = parser.parse_args()

    now = datetime.now(TZ)
    archive_date = args.archive_date or (now - timedelta(days=1)).strftime("%Y-%m-%d")
    new_date = args.new_date or now.strftime("%Y-%m-%d")

    if not DATE_RE.match(archive_date):
        raise SystemExit("archive date must be YYYY-MM-DD")
    if not DATE_RE.match(new_date):
        raise SystemExit("new date must be YYYY-MM-DD")

    today_path = ROOT / "data" / "today.json"
    if not today_path.exists():
        raise SystemExit("data/today.json not found")

    data = load_json(today_path)
    data["date"] = archive_date
    data["status"] = "archived"

    year, month, _day = archive_date.split("-")
    archive_path = ROOT / "archive" / year / month / f"{archive_date}.json"
    write_json(archive_path, data)

    write_json(today_path, reset_today(new_date))

    print(f"Archived data/today.json to {archive_path.relative_to(ROOT)}")
    print(f"Reset data/today.json for {new_date}")


if __name__ == "__main__":
    main()
